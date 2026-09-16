from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


class RunStoreError(RuntimeError):
    pass


class RunNotFoundError(RunStoreError):
    pass


class RunAlreadyExistsError(RunStoreError):
    pass


@dataclass(frozen=True, slots=True)
class RunSnapshot:
    run_id: str
    sequence: int
    reason: str
    created_at: str
    state: dict[str, Any]


class SQLiteRunStore:
    """Durable run-state store with append-only snapshot history."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(str(self.path), timeout=30.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def _connection(self):
        connection = self._connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS run_state (
                    run_id TEXT PRIMARY KEY,
                    sequence INTEGER NOT NULL,
                    state_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS run_history (
                    run_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (run_id, sequence),
                    FOREIGN KEY (run_id) REFERENCES run_state(run_id) ON DELETE CASCADE
                )
                """
            )

    @staticmethod
    def _encode(state: Mapping[str, Any]) -> str:
        try:
            return json.dumps(state, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        except (TypeError, ValueError) as exc:
            raise RunStoreError("run state must be JSON-serializable") from exc

    @staticmethod
    def _decode(payload: str) -> dict[str, Any]:
        value = json.loads(payload)
        if not isinstance(value, dict):
            raise RunStoreError("stored run state must decode to an object")
        return value

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def create(self, state: Mapping[str, Any], *, reason: str = "run_created") -> RunSnapshot:
        run_id = str(state.get("run_id", "")).strip()
        if not run_id:
            raise RunStoreError("state.run_id must not be empty")
        payload = self._encode(state)
        created_at = self._now()
        with self._connection() as connection:
            try:
                connection.execute(
                    "INSERT INTO run_state(run_id, sequence, state_json, updated_at) VALUES (?, 1, ?, ?)",
                    (run_id, payload, created_at),
                )
            except sqlite3.IntegrityError as exc:
                raise RunAlreadyExistsError(f"run already exists: {run_id}") from exc
            connection.execute(
                "INSERT INTO run_history(run_id, sequence, reason, state_json, created_at) VALUES (?, 1, ?, ?, ?)",
                (run_id, reason, payload, created_at),
            )
        return RunSnapshot(run_id, 1, reason, created_at, self._decode(payload))

    def checkpoint(self, state: Mapping[str, Any], *, reason: str) -> RunSnapshot:
        run_id = str(state.get("run_id", "")).strip()
        if not run_id:
            raise RunStoreError("state.run_id must not be empty")
        if not reason.strip():
            raise RunStoreError("checkpoint reason must not be empty")
        payload = self._encode(state)
        created_at = self._now()
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT sequence FROM run_state WHERE run_id = ?", (run_id,)
            ).fetchone()
            if row is None:
                raise RunNotFoundError(f"run not found: {run_id}")
            sequence = int(row["sequence"]) + 1
            connection.execute(
                "UPDATE run_state SET sequence = ?, state_json = ?, updated_at = ? WHERE run_id = ?",
                (sequence, payload, created_at, run_id),
            )
            connection.execute(
                "INSERT INTO run_history(run_id, sequence, reason, state_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (run_id, sequence, reason, payload, created_at),
            )
        return RunSnapshot(run_id, sequence, reason, created_at, self._decode(payload))

    def load(self, run_id: str) -> dict[str, Any]:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT state_json FROM run_state WHERE run_id = ?", (run_id,)
            ).fetchone()
        if row is None:
            raise RunNotFoundError(f"run not found: {run_id}")
        return self._decode(str(row["state_json"]))

    def history(self, run_id: str) -> tuple[RunSnapshot, ...]:
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT run_id, sequence, reason, state_json, created_at
                FROM run_history
                WHERE run_id = ?
                ORDER BY sequence ASC
                """,
                (run_id,),
            ).fetchall()
        if not rows:
            raise RunNotFoundError(f"run not found: {run_id}")
        return tuple(
            RunSnapshot(
                run_id=str(row["run_id"]),
                sequence=int(row["sequence"]),
                reason=str(row["reason"]),
                created_at=str(row["created_at"]),
                state=self._decode(str(row["state_json"])),
            )
            for row in rows
        )
