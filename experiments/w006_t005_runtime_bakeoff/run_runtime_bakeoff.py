from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import math
import os
import platform
import sqlite3
import statistics
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from runtime_bakeoff_adapters import ADAPTERS, SideEffectProbe
from suno_content.runstore.durable_events import (
    OwnershipEpochError,
    SQLiteDurableStateEventStore,
    StaleWriteError,
    UncommittedEventError,
)

TASK_ID = "W006-T005"
ATTEMPT_ID = "A02"
BASE_STATE_VERSION = "0050"
BASE_COMMIT_SHA = "7139b482a3e61e70b957a2573f11a1cbf7e0d3a5"
AUDIENCES = ("beginner", "intermediate", "advanced")
FORMATS = ("article", "carousel", "short_video")
BRANCHES = tuple(f"{audience}:{fmt}" for audience in AUDIENCES for fmt in FORMATS)
ORG_ID = "org-bakeoff"
WORKSPACE_ID = "ws-bakeoff"
RUN_ID = "run-w006-t005-a02"
RESOURCE_TYPE = "branch_output"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - pos) + ordered[hi] * (pos - lo)


def accept_result(
    store: SQLiteDurableStateEventStore,
    *,
    candidate: str,
    branch_id: str,
    execution_id: str,
    expected_revision: int,
    expected_ownership_epoch: int = 0,
    mutation_id: str | None = None,
    sequence: int | None = None,
):
    audience, fmt = branch_id.split(":", 1)
    return store.commit(
        org_id=ORG_ID,
        workspace_id=WORKSPACE_ID,
        run_id=RUN_ID,
        resource_type=RESOURCE_TYPE,
        resource_id=branch_id,
        expected_revision=expected_revision,
        expected_ownership_epoch=expected_ownership_epoch,
        mutation_id=mutation_id or f"accept:{candidate}:{execution_id}",
        state={
            "candidate": candidate,
            "branch_id": branch_id,
            "audience": audience,
            "format": fmt,
            "execution_id": execution_id,
            "sequence": sequence,
        },
        event_type="branch.accepted",
        payload={
            "candidate": candidate,
            "branch_id": branch_id,
            "execution_id": execution_id,
            "sequence": sequence,
        },
    )


def replay_membership(store: SQLiteDurableStateEventStore) -> list[str]:
    events = store.replay_events(org_id=ORG_ID, workspace_id=WORKSPACE_ID, run_id=RUN_ID)
    return [
        str(event.get("payload", {}).get("branch_id"))
        for event in events
        if event.get("event_type") == "branch.accepted"
    ]


def load_t003_floor(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "tests" / "runstore" / "failure_harness_w006_t003.py"
    spec = importlib.util.spec_from_file_location("w006_t003_floor", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load T003 semantic floor: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    result = module.run()
    if result.get("overall_status") != "PASS":
        raise AssertionError("accepted T003 semantic floor did not pass")
    return result


def scenario_exact_3x3(adapter: Any, root: Path) -> dict[str, Any]:
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    durations = []
    for branch_id in BRANCHES:
        execution_id = f"baseline:{branch_id}"
        invocation = adapter.invoke(execution_id, branch_id)
        durations.append(invocation.elapsed_ms)
        accept_result(
            store,
            candidate=adapter.name,
            branch_id=branch_id,
            execution_id=execution_id,
            expected_revision=0,
        )
    membership = replay_membership(store)
    unique = set(membership)
    missing = sorted(set(BRANCHES) - unique)
    unexpected = sorted(unique - set(BRANCHES))
    duplicates = len(membership) - len(unique)
    assert len(unique) == 9 and not missing and not unexpected and duplicates == 0
    return {
        "status": "PASS",
        "accepted_membership": sorted(unique),
        "accepted_count": len(unique),
        "join_branch_loss": len(missing),
        "join_branch_duplication": duplicates,
        "unexpected_branch_ids": unexpected,
        "invocation_latency_ms": durations,
    }


def scenario_duplicate_delivery(adapter: Any, root: Path) -> dict[str, Any]:
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    branch_id, execution_id = BRANCHES[0], "duplicate-delivery"
    probe = SideEffectProbe(adapter.root / "provider-effects.sqlite3")
    before = probe.summary()
    first = adapter.invoke(execution_id, branch_id)
    second = adapter.invoke(execution_id, branch_id)
    t1 = accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id=execution_id, expected_revision=0)
    t2 = accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id=execution_id, expected_revision=0)
    event = store.replay_events(org_id=ORG_ID, workspace_id=WORKSPACE_ID, run_id=RUN_ID)[0]
    projections = [store.project_once(consumer_id="candidate-projection", event=event).applied for _ in range(2)]
    history = store.history(org_id=ORG_ID, workspace_id=WORKSPACE_ID, resource_type=RESOURCE_TYPE, resource_id=branch_id)
    after = probe.summary()
    assert len(history) == 1 and t1.transition_id == t2.transition_id and projections == [True, False]
    return {
        "status": "PASS",
        "physical_runtime_invocations": 2,
        "accepted_transitions": 1,
        "replayed_result_deliveries": 2,
        "logical_projections": 1,
        "duplicate_accepted_output": 0,
        "side_effect_attempt_delta": after["physical_attempts"] - before["physical_attempts"],
        "side_effect_duplicate_attempt_delta": after["duplicate_attempts"] - before["duplicate_attempts"],
        "elapsed_ms": [first.elapsed_ms, second.elapsed_ms],
    }


def scenario_timeout_after_effect(adapter: Any, root: Path) -> dict[str, Any]:
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    branch_id, execution_id = BRANCHES[1], "timeout-after-effect"
    probe = SideEffectProbe(adapter.root / "provider-effects.sqlite3")
    before = probe.summary()
    adapter.invoke(execution_id, branch_id)
    # Simulate transport timeout after runtime/provider side effect and before authoritative acceptance.
    adapter.invoke(execution_id, branch_id)
    accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id=execution_id, expected_revision=0)
    after = probe.summary()
    history = store.history(org_id=ORG_ID, workspace_id=WORKSPACE_ID, resource_type=RESOURCE_TYPE, resource_id=branch_id)
    assert len(history) == 1
    return {
        "status": "PASS",
        "retry_count": 1,
        "accepted_transitions": 1,
        "duplicate_accepted_output": 0,
        "side_effect_attempt_delta": after["physical_attempts"] - before["physical_attempts"],
        "side_effect_duplicate_attempt_delta": after["duplicate_attempts"] - before["duplicate_attempts"],
        "externally_billed_cost": "NOT_OBSERVED",
    }


def scenario_cas_contention(adapter: Any, root: Path) -> dict[str, Any]:
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    branch_id = BRANCHES[3]
    accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id="cas-base", expected_revision=0)
    adapter.invoke("cas-writer-a", branch_id)
    adapter.invoke("cas-writer-b", branch_id)
    barrier = threading.Barrier(2)
    lock = threading.Lock()
    outcomes: list[str] = []

    def writer(execution_id: str) -> None:
        local = SQLiteDurableStateEventStore(store.path)
        barrier.wait()
        try:
            accept_result(local, candidate=adapter.name, branch_id=branch_id, execution_id=execution_id, expected_revision=1)
            outcome = "accepted"
        except StaleWriteError:
            outcome = "stale_rejected"
        with lock:
            outcomes.append(outcome)

    threads = [threading.Thread(target=writer, args=(eid,)) for eid in ("cas-writer-a", "cas-writer-b")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    snapshot = store.load(org_id=ORG_ID, workspace_id=WORKSPACE_ID, resource_type=RESOURCE_TYPE, resource_id=branch_id)
    assert sorted(outcomes) == ["accepted", "stale_rejected"] and snapshot.revision == 2
    return {
        "status": "PASS",
        "outcomes": sorted(outcomes),
        "silent_stale_overwrite": 0,
        "accepted_revision": snapshot.revision,
        "rejected_runtime_outputs": 1,
    }


def scenario_ownership_fencing(adapter: Any, root: Path) -> dict[str, Any]:
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    branch_id = BRANCHES[4]
    accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id="owner-base", expected_revision=0)
    conn = sqlite3.connect(store.path)
    try:
        conn.execute(
            "UPDATE resources SET ownership_epoch = 1 WHERE org_id = ? AND workspace_id = ? AND resource_type = ? AND resource_id = ?",
            (ORG_ID, WORKSPACE_ID, RESOURCE_TYPE, branch_id),
        )
        conn.commit()
    finally:
        conn.close()
    adapter.invoke("owner-stale", branch_id)
    stale_rejected = False
    try:
        accept_result(
            store,
            candidate=adapter.name,
            branch_id=branch_id,
            execution_id="owner-stale",
            expected_revision=1,
            expected_ownership_epoch=0,
        )
    except OwnershipEpochError:
        stale_rejected = True
    adapter.invoke("owner-current", branch_id)
    accept_result(
        store,
        candidate=adapter.name,
        branch_id=branch_id,
        execution_id="owner-current",
        expected_revision=1,
        expected_ownership_epoch=1,
    )
    snapshot = store.load(org_id=ORG_ID, workspace_id=WORKSPACE_ID, resource_type=RESOURCE_TYPE, resource_id=branch_id)
    assert stale_rejected and snapshot.revision == 2 and snapshot.ownership_epoch == 1
    return {
        "status": "PASS",
        "stale_owner_rejected": True,
        "silent_stale_writer": 0,
        "current_revision": snapshot.revision,
        "ownership_epoch": snapshot.ownership_epoch,
    }


def scenario_stale_late(adapter: Any, root: Path) -> dict[str, Any]:
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    branch_id = BRANCHES[5]
    for execution_id, expected in (("late-v1", 0), ("late-v2", 1)):
        adapter.invoke(execution_id, branch_id)
        accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id=execution_id, expected_revision=expected)
    adapter.invoke("late-stale", branch_id)
    rejected = False
    try:
        accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id="late-stale", expected_revision=1)
    except StaleWriteError:
        rejected = True
    snapshot = store.load(org_id=ORG_ID, workspace_id=WORKSPACE_ID, resource_type=RESOURCE_TYPE, resource_id=branch_id)
    assert rejected and snapshot.revision == 2 and snapshot.state["execution_id"] == "late-v2"
    return {
        "status": "PASS",
        "late_result_rejected": True,
        "stale_late_overwrite": 0,
        "accepted_execution_id": snapshot.state["execution_id"],
        "accepted_revision": snapshot.revision,
    }


def scenario_uncommitted_rejection(root: Path) -> dict[str, Any]:
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    forged = {
        "org_id": ORG_ID,
        "workspace_id": WORKSPACE_ID,
        "run_id": RUN_ID,
        "transition_id": "tr-forged",
        "event_id": "ev-forged",
        "event_revision": 1,
        "result_revision": 1,
    }
    rejected = False
    try:
        store.project_once(consumer_id="projection", event=forged)
    except UncommittedEventError:
        rejected = True
    assert rejected
    return {"status": "PASS", "uncommitted_event_accepted": 0, "forged_event_rejected": True}


def scenario_out_of_order(adapter: Any, root: Path) -> dict[str, Any]:
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    branch_id = BRANCHES[6]
    adapter.invoke("order-1", branch_id)
    adapter.invoke("order-2", branch_id)
    early_rejected = False
    try:
        accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id="order-2", expected_revision=1, sequence=2)
    except StaleWriteError:
        early_rejected = True
    accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id="order-1", expected_revision=0, sequence=1)
    accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id="order-2", expected_revision=1, sequence=2)
    history = store.history(org_id=ORG_ID, workspace_id=WORKSPACE_ID, resource_type=RESOURCE_TYPE, resource_id=branch_id)
    sequence = [row.state["sequence"] for row in history]
    assert early_rejected and sequence == [1, 2]
    return {
        "status": "PASS",
        "early_out_of_order_acceptance": 0,
        "accepted_sequence": sequence,
        "replayed_result_duplicate_acceptance": 0,
    }


def scenario_durable_replay(adapter: Any, root: Path) -> dict[str, Any]:
    path = root / "acceptance.sqlite3"
    store = SQLiteDurableStateEventStore(path)
    for branch_id in BRANCHES:
        execution_id = f"replay:{branch_id}"
        adapter.invoke(execution_id, branch_id)
        accept_result(store, candidate=adapter.name, branch_id=branch_id, execution_id=execution_id, expected_revision=0)
    restarted = SQLiteDurableStateEventStore(path)
    membership = replay_membership(restarted)
    assert set(membership) == set(BRANCHES) and len(membership) == 9
    return {
        "status": "PASS",
        "replayed_branch_count": 9,
        "restart_resume_replay_pass": True,
        "join_branch_loss": 0,
        "join_branch_duplication": 0,
    }


def run_crash_child(candidate: str, candidate_root: Path, branch_id: str, execution_id: str, output: Path):
    return subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--child-candidate",
            candidate,
            "--child-root",
            str(candidate_root),
            "--child-branch",
            branch_id,
            "--child-execution-id",
            execution_id,
            "--child-output",
            str(output),
            "--child-crash-once",
        ],
        env=os.environ.copy(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )


def scenario_process_crash_restart(candidate: str, candidate_root: Path, root: Path) -> dict[str, Any]:
    branch_id, execution_id = BRANCHES[2], "process-crash-after-effect"
    probe = SideEffectProbe(candidate_root / "provider-effects.sqlite3")
    before = probe.summary()
    first = run_crash_child(candidate, candidate_root, branch_id, execution_id, root / "child-first.json")
    if first.returncode != 91:
        raise AssertionError(f"expected injected process exit 91, got {first.returncode}: {first.stderr[-2000:]}")
    second_output = root / "child-second.json"
    second = run_crash_child(candidate, candidate_root, branch_id, execution_id, second_output)
    if second.returncode != 0:
        raise AssertionError(f"restart child failed {second.returncode}: {second.stderr[-4000:]}")
    recovered = json.loads(second_output.read_text(encoding="utf-8"))
    store = SQLiteDurableStateEventStore(root / "acceptance.sqlite3")
    accept_result(store, candidate=candidate, branch_id=branch_id, execution_id=execution_id, expected_revision=0)
    after = probe.summary()
    assert recovered["result"]["branch_id"] == branch_id
    return {
        "status": "PASS",
        "first_process_exit_code": 91,
        "restart_process_exit_code": 0,
        "restart_count": 1,
        "retry_count": 1,
        "recovered_branch_id": branch_id,
        "side_effect_attempt_delta": after["physical_attempts"] - before["physical_attempts"],
        "side_effect_duplicate_attempt_delta": after["duplicate_attempts"] - before["duplicate_attempts"],
        "accepted_transitions": 1,
        "duplicate_accepted_output": 0,
        "externally_billed_cost": "NOT_OBSERVED",
    }


def latency_probe(adapter: Any) -> dict[str, Any]:
    samples = [
        adapter.invoke(f"latency:{repeat}:{branch_id}", branch_id).elapsed_ms
        for repeat in range(2)
        for branch_id in BRANCHES
    ]
    return {
        "sample_count": len(samples),
        "samples_ms": samples,
        "mean_ms": statistics.fmean(samples),
        "median_ms": statistics.median(samples),
        "p95_ms": percentile(samples, 0.95),
        "stdev_ms": statistics.pstdev(samples),
        "min_ms": min(samples),
        "max_ms": max(samples),
    }


def candidate_result(candidate: str, work_root: Path) -> dict[str, Any]:
    candidate_root = work_root / candidate / "runtime"
    scenario_root = work_root / candidate / "scenarios"
    candidate_root.mkdir(parents=True, exist_ok=True)
    scenario_root.mkdir(parents=True, exist_ok=True)
    adapter = ADAPTERS[candidate](candidate_root)
    results: dict[str, Any] = {}
    try:
        results["exact_3x3"] = scenario_exact_3x3(adapter, scenario_root / "exact")
        results["duplicate_and_replayed_delivery"] = scenario_duplicate_delivery(adapter, scenario_root / "duplicate")
        results["timeout_after_effect_before_acceptance"] = scenario_timeout_after_effect(adapter, scenario_root / "timeout")
        results["cas_contention"] = scenario_cas_contention(adapter, scenario_root / "cas")
        results["ownership_fencing"] = scenario_ownership_fencing(adapter, scenario_root / "ownership")
        results["stale_late_result"] = scenario_stale_late(adapter, scenario_root / "stale")
        results["reject_uncommitted_event"] = scenario_uncommitted_rejection(scenario_root / "uncommitted")
        results["out_of_order_result"] = scenario_out_of_order(adapter, scenario_root / "order")
        results["durable_replay"] = scenario_durable_replay(adapter, scenario_root / "replay")
        latency = latency_probe(adapter)
    finally:
        adapter.close()
    results["process_crash_restart"] = scenario_process_crash_restart(candidate, candidate_root, scenario_root / "crash")
    provider = SideEffectProbe(candidate_root / "provider-effects.sqlite3").summary()
    gates = {
        "exact_accepted_branch_membership_9_of_9": results["exact_3x3"]["accepted_count"] == 9,
        "accepted_join_branch_loss_zero": results["exact_3x3"]["join_branch_loss"] == 0 and results["durable_replay"]["join_branch_loss"] == 0,
        "accepted_join_branch_duplication_zero": results["exact_3x3"]["join_branch_duplication"] == 0 and results["durable_replay"]["join_branch_duplication"] == 0,
        "duplicate_accepted_output_zero": results["duplicate_and_replayed_delivery"]["duplicate_accepted_output"] == 0 and results["timeout_after_effect_before_acceptance"]["duplicate_accepted_output"] == 0 and results["process_crash_restart"]["duplicate_accepted_output"] == 0,
        "stale_late_overwrite_zero": results["cas_contention"]["silent_stale_overwrite"] == 0 and results["stale_late_result"]["stale_late_overwrite"] == 0,
        "uncommitted_event_acceptance_zero": results["reject_uncommitted_event"]["uncommitted_event_accepted"] == 0,
        "defined_restart_resume_replay_100_percent": results["process_crash_restart"]["status"] == "PASS" and results["durable_replay"]["restart_resume_replay_pass"],
        "fencing_prevents_silent_stale_writer": results["ownership_fencing"]["silent_stale_writer"] == 0,
        "duplicate_side_effect_counts_persisted_raw": "duplicate_attempts" in provider,
        "critical_schema_provenance_violations_zero": results["exact_3x3"]["unexpected_branch_ids"] == [],
    }
    eligible = all(gates.values())
    return {
        "candidate": candidate,
        "status": "PASS" if eligible else "FAIL",
        "hard_gate_eligible": eligible,
        "hard_gates": gates,
        "scenarios": results,
        "latency": latency,
        "provider_side_effect_accounting": provider,
        "externally_billed_cost": "NOT_OBSERVED",
        "failure_taxonomy": [],
    }


def point_pareto(rows: list[dict[str, Any]]) -> list[str]:
    eligible = [row for row in rows if row["hard_gate_eligible"]]
    points = {
        row["candidate"]: (
            float(row["latency"]["median_ms"]),
            float(row["provider_side_effect_accounting"]["duplicate_attempts"]),
        )
        for row in eligible
    }
    frontier = []
    for name, point in points.items():
        dominated = False
        for other_name, other in points.items():
            if other_name == name:
                continue
            if other[0] <= point[0] and other[1] <= point[1] and (other[0] < point[0] or other[1] < point[1]):
                dominated = True
                break
        if not dominated:
            frontier.append(name)
    return sorted(frontier)


def runner_metadata() -> dict[str, Any]:
    return {
        "generated_at": utc_now(),
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "sqlite": sqlite3.sqlite_version,
        "runner_os": os.environ.get("RUNNER_OS", platform.system()),
        "image_os": os.environ.get("ImageOS", "NOT_EXPOSED"),
        "image_version": os.environ.get("ImageVersion", "NOT_EXPOSED"),
        "github_sha": os.environ.get("GITHUB_SHA", "LOCAL_OR_NOT_EXPOSED"),
        "github_ref": os.environ.get("GITHUB_REF", "LOCAL_OR_NOT_EXPOSED"),
        "packages": {
            package: importlib.metadata.version(package)
            for package in ("langgraph", "langgraph-checkpoint-sqlite", "dbos")
        },
    }


def main(output_dir: Path) -> int:
    repo_root = Path(__file__).resolve().parents[2]
    output_dir.mkdir(parents=True, exist_ok=True)
    work_root = output_dir / "work"
    work_root.mkdir(parents=True, exist_ok=True)
    floor = load_t003_floor(repo_root)
    candidates = [candidate_result(name, work_root) for name in ("custom_cas", "langgraph", "dbos")]
    runner = runner_metadata()
    observations = {
        "artifact": "W006-T005-A02 runtime/shared-state bakeoff raw observations",
        "task_id": TASK_ID,
        "attempt_id": ATTEMPT_ID,
        "base_state_version": BASE_STATE_VERSION,
        "base_commit_sha": BASE_COMMIT_SHA,
        "generated_at": utc_now(),
        "workload": {
            "audiences": list(AUDIENCES),
            "formats": list(FORMATS),
            "branch_ids": list(BRANCHES),
            "branch_count": 9,
        },
        "shared_semantic_floor": {
            "source": "tests/runstore/failure_harness_w006_t003.py",
            "overall_status": floor["overall_status"],
            "metrics": floor["metrics"],
            "scenario_count": len(floor["results"]),
            "scope": "accepted T003 logical/CAS/outbox reference semantics; SQLite is benchmark-only",
        },
        "runner": runner,
        "candidates": candidates,
    }
    frontier = point_pareto(candidates)
    decision = {
        "artifact": "W006-T005-A02 runtime decision artifact",
        "generated_at": utc_now(),
        "method": [
            "non_compensatory_hard_gates",
            "raw_multidimensional_metrics",
            "uncertainty_where_meaningful",
            "point_pareto",
        ],
        "hard_gate_eligible": {row["candidate"]: row["hard_gate_eligible"] for row in candidates},
        "pareto_objectives": [
            {"metric": "median_runtime_invocation_ms", "direction": "lower_is_better", "unit": "ms"},
            {"metric": "duplicate_side_effect_attempts", "direction": "lower_is_better", "unit": "attempts"},
        ],
        "point_pareto_set": frontier,
        "uncertainty": {
            row["candidate"]: {
                "sample_count": row["latency"]["sample_count"],
                "median_ms": row["latency"]["median_ms"],
                "p95_ms": row["latency"]["p95_ms"],
                "stdev_ms": row["latency"]["stdev_ms"],
            }
            for row in candidates
        },
        "decision_state": "PENDING_EVIDENCE",
        "production_runtime_lock": None,
        "rationale": [
            "The minimum comparative set executed on the exact 3x3 workload and produced an auditable hard-gate/Pareto surface.",
            "The accepted-state layer is intentionally the common T003 SQLite reference substrate, so this attempt does not test a distributed production database or multi-replica topology.",
            "Provider effects are benchmark probes with durable idempotency keys; externally billed cost is NOT_OBSERVED.",
            "Observed clean-runner latency is raw evidence, not a representative production SLO/capacity result, so it cannot justify a production runtime lock by itself.",
        ],
        "temporal": {
            "status": "OPEN_CHALLENGER_NOT_EXECUTED_THIS_ATTEMPT",
            "reason": "The minimum set produced a valid decision surface; the remaining blocker is representative distributed/topology evidence rather than absence of a fourth framework datapoint. Temporal remains open for a future production-topology challenger run.",
        },
        "database_scope": "SQLite files are benchmark/reference infrastructure only; no production database winner is selected.",
        "externally_billed_cost": "NOT_OBSERVED",
        "recheck_conditions": [
            "run eligible candidates on the intended multi-replica/shared-state production topology",
            "measure representative concurrency, failover, recovery, saturation and operational overhead",
            "execute Temporal if a remaining orchestration-semantics hypothesis could alter the eligible/Pareto set",
            "do not introduce scalar utility weights without representative business evidence",
        ],
    }
    (output_dir / "candidate-observations.json").write_text(json.dumps(observations, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "decision.json").write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "runner.json").write_text(json.dumps(runner, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if all(row["hard_gate_eligible"] for row in candidates) else 2


def child_main(args: argparse.Namespace) -> int:
    root = Path(args.child_root)
    adapter = ADAPTERS[args.child_candidate](root)
    try:
        invocation = adapter.invoke(args.child_execution_id, args.child_branch, crash_once=bool(args.child_crash_once))
    finally:
        adapter.close()
    payload = {
        "candidate": args.child_candidate,
        "result": invocation.result,
        "elapsed_ms": invocation.elapsed_ms,
    }
    output = Path(args.child_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--child-candidate", choices=sorted(ADAPTERS))
    parser.add_argument("--child-root")
    parser.add_argument("--child-branch")
    parser.add_argument("--child-execution-id")
    parser.add_argument("--child-output")
    parser.add_argument("--child-crash-once", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    parsed = parse_args()
    if parsed.child_candidate:
        raise SystemExit(child_main(parsed))
    if parsed.output_dir is None:
        raise SystemExit("--output-dir is required")
    raise SystemExit(main(parsed.output_dir))
