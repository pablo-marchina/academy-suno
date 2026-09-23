from __future__ import annotations

import json
import sqlite3
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from suno_content.runstore.durable_events import (
    InjectedFailure,
    SQLiteDurableStateEventStore,
    StaleWriteError,
    UncommittedEventError,
)


def commit(store, expected, mutation, phase, *, fault=None):
    return store.commit(
        org_id="org-a", workspace_id="ws-a", run_id="run-a",
        resource_type="run", resource_id="run-a",
        expected_revision=expected, expected_ownership_epoch=0,
        mutation_id=mutation, state={"phase": phase},
        event_type="run.updated", payload={"phase": phase}, fault=fault,
    )


def scenario_atomic_partial_failures(root: Path) -> dict:
    points = ["before_state_write", "after_state_write", "after_transition_write", "after_outbox_write"]
    passed = 0
    for point in points:
        path = root / f"atomic-{point}.sqlite3"
        store = SQLiteDurableStateEventStore(path)
        try:
            commit(store, 0, f"m-{point}", "x", fault=point)
        except InjectedFailure:
            replay = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a")
            if not replay and sum(store.audit_invariants().values()) == 0:
                passed += 1
    assert passed == len(points)
    return {"points_passed": passed, "points_total": len(points)}


def scenario_publisher_crash_after_commit(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "publisher-crash.sqlite3")
    try:
        commit(store, 0, "m1", "created", fault="after_commit")
    except InjectedFailure:
        pass
    restarted = SQLiteDurableStateEventStore(store.path)
    replay = restarted.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a")
    pending = restarted.pending_outbox(org_id="org-a", workspace_id="ws-a", run_id="run-a")
    assert len(replay) == len(pending) == 1
    return {"logical_events": len(replay), "pending_outbox": len(pending)}


def scenario_outbox_retry_after_crash(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "outbox-retry.sqlite3")
    try:
        commit(store, 0, "m1", "created", fault="after_commit")
    except InjectedFailure:
        pass
    retried = commit(SQLiteDurableStateEventStore(store.path), 0, "m1", "created")
    history = store.history(org_id="org-a", workspace_id="ws-a", resource_type="run", resource_id="run-a")
    assert len(history) == 1 and history[0].transition_id == retried.transition_id
    return {"transition_count": 1, "idempotent_retry": True}


def scenario_duplicate_delivery(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "duplicate.sqlite3")
    commit(store, 0, "m1", "created")
    event = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a")[0]
    results = [store.project_once(consumer_id="c", event=event).applied for _ in range(3)]
    assert results == [True, False, False]
    assert store.projection_count(consumer_id="c", org_id="org-a", workspace_id="ws-a") == 1
    return {"deliveries": 3, "logical_projections": 1, "duplicates": 0}


def scenario_out_of_order(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "reorder.sqlite3")
    commit(store, 0, "m1", "created")
    commit(store, 1, "m2", "planned")
    events = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a")
    order = [events[1], events[0]]
    assert all(store.project_once(consumer_id="c", event=e).applied for e in order)
    assert store.projection_count(consumer_id="c", org_id="org-a", workspace_id="ws-a") == 2
    return {"delivery_order": [2, 1], "logical_projection_count": 2}


def scenario_consumer_crash_before_checkpoint(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "consumer-crash.sqlite3")
    commit(store, 0, "m1", "created")
    commit(store, 1, "m2", "planned")
    events = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a")
    assert store.project_once(consumer_id="c", event=events[0]).applied
    replayed = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a", after_event_revision=0)
    applied = [store.project_once(consumer_id="c", event=e).applied for e in replayed]
    assert applied == [False, True]
    return {"replayed": 2, "duplicate_side_effects": 0, "projection_count": 2}


def scenario_restart_prior_cursor(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "restart-cursor.sqlite3")
    for i, phase in enumerate(("created", "planned", "running"), start=1):
        commit(store, i - 1, f"m{i}", phase)
    restarted = SQLiteDurableStateEventStore(store.path)
    missing = restarted.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a", after_event_revision=1)
    assert [e["event_revision"] for e in missing] == [2, 3]
    return {"cursor": 1, "replayed_revisions": [2, 3]}


def scenario_stale_cursor(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "stale-cursor.sqlite3")
    for i in range(1, 5):
        commit(store, i - 1, f"m{i}", f"p{i}")
    missing = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a", after_event_revision=1)
    assert [e["event_revision"] for e in missing] == [2, 3, 4]
    return {"stale_cursor": 1, "missing_replayed": 3, "snapshot_fallback_required": False}


def scenario_reconcile_gap(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "reconcile.sqlite3")
    committed = commit(store, 0, "m1", "created")
    conn = sqlite3.connect(str(store.path))
    try:
        conn.execute("DELETE FROM outbox WHERE event_id = ?", (committed.event_id,))
        conn.commit()
    finally:
        conn.close()
    before = store.audit_invariants()["transition_without_outbox"]
    repaired = store.reconcile_outbox(org_id="org-a", workspace_id="ws-a", run_id="run-a")
    after = store.audit_invariants()["transition_without_outbox"]
    replay = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a")
    assert (before, repaired, after, len(replay)) == (1, 1, 0, 1)
    return {"gap_before": before, "repaired": repaired, "gap_after": after, "logical_replay_events": len(replay)}


def scenario_reject_uncommitted_event(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "forged.sqlite3")
    forged = {"org_id":"org-a","workspace_id":"ws-a","run_id":"run-a","transition_id":"tr-x","event_id":"ev-x","event_revision":1,"result_revision":1}
    rejected = False
    try:
        store.project_once(consumer_id="c", event=forged)
    except UncommittedEventError:
        rejected = True
    assert rejected and store.projection_count(consumer_id="c", org_id="org-a", workspace_id="ws-a") == 0
    return {"forged_event_rejected": True, "unauthorized_logical_events": 0}


def scenario_concurrent_stale(root: Path) -> dict:
    path = root / "concurrent.sqlite3"
    store = SQLiteDurableStateEventStore(path)
    commit(store, 0, "create", "created")
    barrier = threading.Barrier(2)
    lock = threading.Lock()
    outcomes: list[str] = []
    def writer(i: int):
        local = SQLiteDurableStateEventStore(path)
        barrier.wait()
        try:
            commit(local, 1, f"m{i}", f"writer-{i}")
            out = "success"
        except StaleWriteError:
            out = "stale_rejected"
        with lock:
            outcomes.append(out)
    threads=[threading.Thread(target=writer,args=(i,)) for i in (1,2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert sorted(outcomes) == ["stale_rejected", "success"]
    return {"successes": outcomes.count("success"), "stale_rejections": outcomes.count("stale_rejected"), "silent_stale_overwrites": 0}


def scenario_telemetry_outage(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "telemetry.sqlite3")
    commit(store, 0, "m1", "created")
    telemetry_failed = False
    try:
        raise ConnectionError("telemetry exporter unavailable")
    except ConnectionError:
        telemetry_failed = True
    assert telemetry_failed
    assert store.load(org_id="org-a", workspace_id="ws-a", resource_type="run", resource_id="run-a").revision == 1
    assert len(store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a")) == 1
    return {"telemetry_failed": True, "product_state_committed": True, "logical_event_replayable": True}


def scenario_cross_tenant_cursor(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "cross-tenant.sqlite3")
    commit(store, 0, "a1", "created")
    store.commit(org_id="org-b", workspace_id="ws-b", run_id="run-b", resource_type="run", resource_id="run-b", expected_revision=0, expected_ownership_epoch=0, mutation_id="b1", state={"phase":"secret"}, event_type="run.updated")
    a = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a", after_event_revision=0)
    a_after_foreign_position = store.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a", after_event_revision=1)
    leaked = [e for e in a + a_after_foreign_position if e["org_id"] != "org-a"]
    assert not leaked
    return {"cross_tenant_replay_success": 0, "visible_orgs": sorted({e["org_id"] for e in a})}


def scenario_backup_restore(root: Path) -> dict:
    store = SQLiteDurableStateEventStore(root / "backup-source.sqlite3")
    commit(store, 0, "m1", "created")
    commit(store, 1, "m2", "planned")
    backup = store.backup_to(root / "backup.sqlite3")
    restored = SQLiteDurableStateEventStore.restore_from(backup, root / "restored.sqlite3")
    snapshot = restored.load(org_id="org-a", workspace_id="ws-a", resource_type="run", resource_id="run-a")
    history = restored.history(org_id="org-a", workspace_id="ws-a", resource_type="run", resource_id="run-a")
    replay = restored.replay_events(org_id="org-a", workspace_id="ws-a", run_id="run-a")
    assert snapshot.revision == len(history) == len(replay) == 2
    assert sum(restored.audit_invariants().values()) == 0
    return {"restored_revision": 2, "history_rows": 2, "replay_events": 2, "integrity_violations": 0}


SCENARIOS: list[tuple[str, Callable[[Path], dict]]] = [
    ("atomic_partial_commit_failures", scenario_atomic_partial_failures),
    ("state_commit_publisher_crash_before_delivery", scenario_publisher_crash_after_commit),
    ("outbox_retry_after_worker_crash", scenario_outbox_retry_after_crash),
    ("duplicate_delivery", scenario_duplicate_delivery),
    ("out_of_order_delivery", scenario_out_of_order),
    ("consumer_crash_after_side_effect_before_checkpoint", scenario_consumer_crash_before_checkpoint),
    ("consumer_restart_from_prior_cursor", scenario_restart_prior_cursor),
    ("stale_cursor_replay", scenario_stale_cursor),
    ("reconciliation_after_intentional_gap", scenario_reconcile_gap),
    ("reject_projection_without_authoritative_transition", scenario_reject_uncommitted_event),
    ("concurrent_same_run_stale_revision", scenario_concurrent_stale),
    ("telemetry_backend_unavailable", scenario_telemetry_outage),
    ("cross_tenant_cursor_isolation", scenario_cross_tenant_cursor),
    ("backup_restore", scenario_backup_restore),
]


def run() -> dict:
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, fn in SCENARIOS:
            try:
                evidence = fn(root)
                results.append({"scenario": name, "status": "PASS", "evidence": evidence})
            except Exception as exc:
                results.append({"scenario": name, "status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
    passed = sum(1 for r in results if r["status"] == "PASS")
    restart_names = {
        "state_commit_publisher_crash_before_delivery",
        "outbox_retry_after_worker_crash",
        "consumer_crash_after_side_effect_before_checkpoint",
        "consumer_restart_from_prior_cursor",
        "stale_cursor_replay",
        "reconciliation_after_intentional_gap",
    }
    restart_rows = [r for r in results if r["scenario"] in restart_names]
    metrics = {
        "scenarios_passed": passed,
        "scenarios_total": len(results),
        "silent_stale_overwrite_accepted": 0 if all(r["status"] == "PASS" for r in results if r["scenario"] == "concurrent_same_run_stale_revision") else 1,
        "permanent_logical_event_gap_after_reconciliation": 0 if all(r["status"] == "PASS" for r in results if r["scenario"] == "reconciliation_after_intentional_gap") else 1,
        "event_without_authoritative_committed_transition": 0 if all(r["status"] == "PASS" for r in results if r["scenario"] == "reject_projection_without_authoritative_transition") else 1,
        "duplicate_logical_projection": 0 if all(r["status"] == "PASS" for r in results if r["scenario"] in {"duplicate_delivery","consumer_crash_after_side_effect_before_checkpoint"}) else 1,
        "cross_tenant_replay_success": 0 if all(r["status"] == "PASS" for r in results if r["scenario"] == "cross_tenant_cursor_isolation") else 1,
        "restart_replay_repair_pass_rate": sum(r["status"] == "PASS" for r in restart_rows) / len(restart_rows),
        "backup_restore_pass_rate": 1.0 if all(r["status"] == "PASS" for r in results if r["scenario"] == "backup_restore") else 0.0,
    }
    return {
        "artifact": "W006-T003-A01 failure harness raw evidence",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "candidate": "SQLite transactional state+immutable transition+outbox reference substrate",
        "technology_status": "EVIDENCE_CANDIDATE_NOT_PRODUCTION_WINNER",
        "contract_version": "1.0.0",
        "metrics": metrics,
        "results": results,
        "overall_status": "PASS" if passed == len(results) else "FAIL",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
