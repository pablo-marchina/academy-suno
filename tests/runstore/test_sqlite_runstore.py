from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from suno_content.runstore import RunAlreadyExistsError, SQLiteRunStore


class SQLiteRunStoreTests(unittest.TestCase):
    def test_persists_latest_state_and_append_only_history_across_instances(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "runs.sqlite3"
            first = SQLiteRunStore(path)
            state = {"run_id": "run-1", "phase": "created", "nested": {"value": 1}}
            first.create(state)
            state["phase"] = "planned"
            state["nested"]["value"] = 2
            first.checkpoint(state, reason="planned")

            second = SQLiteRunStore(path)
            loaded = second.load("run-1")
            history = second.history("run-1")

            self.assertEqual("planned", loaded["phase"])
            self.assertEqual(2, loaded["nested"]["value"])
            self.assertEqual([1, 2], [snapshot.sequence for snapshot in history])
            self.assertEqual(["run_created", "planned"], [snapshot.reason for snapshot in history])
            self.assertEqual(1, history[0].state["nested"]["value"])
            self.assertEqual(2, history[1].state["nested"]["value"])

    def test_create_rejects_duplicate_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteRunStore(Path(tmp) / "runs.sqlite3")
            store.create({"run_id": "same", "phase": "created"})
            with self.assertRaises(RunAlreadyExistsError):
                store.create({"run_id": "same", "phase": "created"})


if __name__ == "__main__":
    unittest.main()
