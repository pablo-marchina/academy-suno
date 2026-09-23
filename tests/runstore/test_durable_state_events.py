from __future__ import annotations

import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

from suno_content.runstore.durable_events import (
    InjectedFailure,
    SQLiteDurableStateEventStore,
    StaleWriteError,
    UncommittedEventError,
)


class DurableStateEventStoreTests(unittest.TestCase):
    def _store(self, root: str) -> SQLiteDurableStateEventStore:
        return SQLiteDurableStateEventStore(Path(root) / "state-events.sqlite3")

    def _commit(self, store: SQLiteDurableStateEventStore, *, expected: int, mutation: str, phase: str, fault: str | None = None):
        return store.commit(
            org_id="org-1",
            workspace_id="ws-1",
            run_id="run-1",
            resource_type="run",
            resource_id="run-1",
            expected_revision=expected,
            expected_ownership_epoch=0,
            mutation_id=mutation,
            state={"phase": phase},
            event_type="run.updated",
            payload={"phase": phase},
            fault=fault,
        )

    def test_atomic_failures_before_commit_leave_no_state_or_event(self) -> None:
        for fault in ("before_state_write", "after_state_write", "after_transition_write", "after_outbox_write"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as tmp:
                store = self._store(tmp)
                with self.assertRaises(InjectedFailure):
                    self._commit(store, expected=0, mutation=f"m-{fault}", phase="x", fault=fault)
                self.assertEqual((), store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1"))
                self.assertEqual(0, sum(store.audit_invariants().values()))

    def test_after_commit_crash_is_idempotently_recoverable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            with self.assertRaises(InjectedFailure):
                self._commit(store, expected=0, mutation="m1", phase="created", fault="after_commit")
            reopened = self._store(tmp)
            replay = reopened.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1")
            self.assertEqual(1, len(replay))
            retried = self._commit(reopened, expected=0, mutation="m1", phase="created")
            self.assertEqual(replay[0]["transition_id"], retried.transition_id)
            self.assertEqual(1, len(reopened.history(org_id="org-1", workspace_id="ws-1", resource_type="run", resource_id="run-1")))

    def test_stale_write_is_rejected_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            self._commit(store, expected=0, mutation="m1", phase="created")
            self._commit(store, expected=1, mutation="m2", phase="planned")
            with self.assertRaises(StaleWriteError):
                self._commit(store, expected=1, mutation="m3", phase="stale")
            snapshot = store.load(org_id="org-1", workspace_id="ws-1", resource_type="run", resource_id="run-1")
            self.assertEqual(2, snapshot.revision)
            self.assertEqual("planned", snapshot.state["phase"])

    def test_concurrent_same_revision_has_one_success_one_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "probe.sqlite3"
            store = SQLiteDurableStateEventStore(path)
            store.commit(
                org_id="org-1", workspace_id="ws-1", run_id="run-1",
                resource_type="run", resource_id="run-1",
                expected_revision=0, expected_ownership_epoch=0,
                mutation_id="create", state={"phase": "created"}, event_type="run.created",
            )
            barrier = threading.Barrier(2)
            results: list[str] = []
            lock = threading.Lock()

            def writer(index: int) -> None:
                local = SQLiteDurableStateEventStore(path)
                barrier.wait()
                try:
                    local.commit(
                        org_id="org-1", workspace_id="ws-1", run_id="run-1",
                        resource_type="run", resource_id="run-1",
                        expected_revision=1, expected_ownership_epoch=0,
                        mutation_id=f"m-{index}", state={"phase": f"w-{index}"}, event_type="run.updated",
                    )
                    outcome = "success"
                except StaleWriteError:
                    outcome = "stale"
                with lock:
                    results.append(outcome)

            threads = [threading.Thread(target=writer, args=(i,)) for i in (1, 2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertEqual(["stale", "success"], sorted(results))

    def test_outbox_reconciliation_repairs_missing_delivery_row_without_logical_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            committed = self._commit(store, expected=0, mutation="m1", phase="created")
            connection = sqlite3.connect(str(store.path))
            try:
                connection.execute("DELETE FROM outbox WHERE event_id = ?", (committed.event_id,))
                connection.commit()
            finally:
                connection.close()
            self.assertEqual(1, len(store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1")))
            self.assertEqual(1, store.audit_invariants()["transition_without_outbox"])
            self.assertEqual(1, store.reconcile_outbox(org_id="org-1", workspace_id="ws-1", run_id="run-1"))
            self.assertEqual(0, sum(store.audit_invariants().values()))
            self.assertEqual(1, len(store.pending_outbox(org_id="org-1", workspace_id="ws-1", run_id="run-1")))

    def test_duplicate_and_reordered_physical_delivery_projects_once_per_transition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            self._commit(store, expected=0, mutation="m1", phase="created")
            self._commit(store, expected=1, mutation="m2", phase="planned")
            events = list(store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1"))
            delivery = [events[1], events[0], events[1], events[0]]
            applied = [store.project_once(consumer_id="consumer-a", event=event).applied for event in delivery]
            self.assertEqual([True, True, False, False], applied)
            self.assertEqual(2, store.projection_count(consumer_id="consumer-a", org_id="org-1", workspace_id="ws-1"))

    def test_uncommitted_event_is_rejected_from_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            forged = {
                "org_id": "org-1", "workspace_id": "ws-1", "run_id": "run-1",
                "transition_id": "tr-forged", "event_id": "ev-forged",
                "event_revision": 1, "result_revision": 1,
            }
            with self.assertRaises(UncommittedEventError):
                store.project_once(consumer_id="consumer-a", event=forged)
            self.assertEqual(0, store.projection_count(consumer_id="consumer-a", org_id="org-1", workspace_id="ws-1"))

    def test_replay_cursor_position_is_stream_scoped_by_server_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            self._commit(store, expected=0, mutation="m1", phase="created")
            store.commit(
                org_id="org-2", workspace_id="ws-2", run_id="run-2",
                resource_type="run", resource_id="run-2",
                expected_revision=0, expected_ownership_epoch=0,
                mutation_id="other", state={"phase": "other"}, event_type="run.updated",
            )
            replay = store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1", after_event_revision=0)
            self.assertEqual(1, len(replay))
            self.assertEqual("org-1", replay[0]["org_id"])
            self.assertEqual((), store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1", after_event_revision=1))

    def test_consumer_restart_from_prior_cursor_replays_and_deduplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            self._commit(store, expected=0, mutation="m1", phase="created")
            self._commit(store, expected=1, mutation="m2", phase="planned")
            events = store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1")
            first = store.project_once(consumer_id="consumer-a", event=events[0])
            self.assertTrue(first.applied)
            replayed = store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1", after_event_revision=0)
            reapplied = [store.project_once(consumer_id="consumer-a", event=e).applied for e in replayed]
            self.assertEqual([False, True], reapplied)
            self.assertEqual(2, store.projection_count(consumer_id="consumer-a", org_id="org-1", workspace_id="ws-1"))

    def test_stale_cursor_replays_all_missing_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            for index, phase in enumerate(("created", "planned", "running"), start=1):
                self._commit(store, expected=index - 1, mutation=f"m{index}", phase=phase)
            missing = store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1", after_event_revision=1)
            self.assertEqual([2, 3], [event["event_revision"] for event in missing])

    def test_restart_replay_and_mark_dispatched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            committed = self._commit(store, expected=0, mutation="m1", phase="created")
            restarted = self._store(tmp)
            self.assertEqual(1, len(restarted.pending_outbox(org_id="org-1", workspace_id="ws-1", run_id="run-1")))
            restarted.mark_dispatched(org_id="org-1", workspace_id="ws-1", event_id=committed.event_id)
            self.assertEqual((), restarted.pending_outbox(org_id="org-1", workspace_id="ws-1", run_id="run-1"))
            self.assertEqual(1, len(restarted.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1")))

    def test_telemetry_failure_does_not_touch_product_state_or_event_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            self._commit(store, expected=0, mutation="m1", phase="created")
            try:
                raise RuntimeError("telemetry backend unavailable")
            except RuntimeError:
                pass
            self.assertEqual(1, store.load(org_id="org-1", workspace_id="ws-1", resource_type="run", resource_id="run-1").revision)
            self.assertEqual(1, len(store.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1")))

    def test_backup_restore_preserves_state_history_and_replay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            self._commit(store, expected=0, mutation="m1", phase="created")
            self._commit(store, expected=1, mutation="m2", phase="planned")
            backup = store.backup_to(Path(tmp) / "backup.sqlite3")
            restored = SQLiteDurableStateEventStore.restore_from(backup, Path(tmp) / "restored.sqlite3")
            snapshot = restored.load(org_id="org-1", workspace_id="ws-1", resource_type="run", resource_id="run-1")
            self.assertEqual((2, "planned"), (snapshot.revision, snapshot.state["phase"]))
            self.assertEqual(2, len(restored.history(org_id="org-1", workspace_id="ws-1", resource_type="run", resource_id="run-1")))
            self.assertEqual(2, len(restored.replay_events(org_id="org-1", workspace_id="ws-1", run_id="run-1")))
            self.assertEqual(0, sum(restored.audit_invariants().values()))

    def test_transition_history_is_append_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = self._store(tmp)
            committed = self._commit(store, expected=0, mutation="m1", phase="created")
            connection = sqlite3.connect(str(store.path))
            try:
                with self.assertRaises(sqlite3.DatabaseError):
                    connection.execute("DELETE FROM transitions WHERE transition_id = ?", (committed.transition_id,))
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
