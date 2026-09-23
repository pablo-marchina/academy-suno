from __future__ import annotations

import json
import shutil
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


CONTRACT_VERSION = "1.0.0"


class DurableStateEventError(RuntimeError):
    pass


class StaleWriteError(DurableStateEventError):
    pass


class OwnershipEpochError(DurableStateEventError):
    pass


class ResourceNotFoundError(DurableStateEventError):
    pass


class InjectedFailure(DurableStateEventError):
    pass


class UncommittedEventError(DurableStateEventError):
    pass


@dataclass(frozen=True, slots=True)
class ResourceSnapshot:
    org_id: str
    workspace_id: str
    run_id: str
    resource_type: str
    resource_id: str
    revision: int
    ownership_epoch: int
    state: dict[str, Any]
    updated_at: str


@dataclass(frozen=True, slots=True)
class CommittedTransition:
    org_id: str
    workspace_id: str
    run_id: str
    resource_type: str
    resource_id: str
    transition_id: str
    mutation_id: str
    previous_revision: int
    result_revision: int
    ownership_epoch: int
    event_id: str
    event_type: str
    event_revision: int
    occurred_at: str
    state: dict[str, Any]
    payload: dict[str, Any]

    def event_envelope(self) -> dict[str, Any]:
        return {
            "contract_version": CONTRACT_VERSION,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "run_id": self.run_id,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_schema_version": 1,
            "transition_id": self.transition_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "result_revision": self.result_revision,
            "event_revision": self.event_revision,
            "occurred_at": self.occurred_at,
            "payload": dict(self.payload),
        }


@dataclass(frozen=True, slots=True)
class ProjectionReceipt:
    consumer_id: str
    transition_id: str
    event_id: str
    event_revision: int
    applied: bool


class SQLiteDurableStateEventStore:
    """Reference durable state/event substrate for the Phase 9 failure harness.

    This class intentionally proves logical semantics without promoting SQLite as a
    production backend. Authoritative state, transition audit history, and an outbox
    row are committed in one transaction. Replay is reconstructed from immutable
    transitions, so outbox delivery failure cannot create a permanent logical gap.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(str(self.path), timeout=30.0, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    @contextmanager
    def _transaction(self):
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @contextmanager
    def _read(self):
        connection = self._connect()
        try:
            yield connection
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._transaction() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS resources (
                    org_id TEXT NOT NULL,
                    workspace_id TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    resource_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    revision INTEGER NOT NULL CHECK (revision >= 0),
                    ownership_epoch INTEGER NOT NULL CHECK (ownership_epoch >= 0),
                    state_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (org_id, workspace_id, resource_type, resource_id)
                );

                CREATE TABLE IF NOT EXISTS run_event_sequence (
                    org_id TEXT NOT NULL,
                    workspace_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    last_event_revision INTEGER NOT NULL CHECK (last_event_revision >= 0),
                    PRIMARY KEY (org_id, workspace_id, run_id)
                );

                CREATE TABLE IF NOT EXISTS transitions (
                    org_id TEXT NOT NULL,
                    workspace_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    resource_id TEXT NOT NULL,
                    transition_id TEXT NOT NULL,
                    mutation_id TEXT NOT NULL,
                    previous_revision INTEGER NOT NULL,
                    result_revision INTEGER NOT NULL,
                    ownership_epoch INTEGER NOT NULL,
                    event_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_revision INTEGER NOT NULL,
                    occurred_at TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    PRIMARY KEY (org_id, workspace_id, transition_id),
                    UNIQUE (org_id, workspace_id, resource_type, resource_id, mutation_id),
                    UNIQUE (org_id, workspace_id, run_id, event_revision),
                    UNIQUE (org_id, workspace_id, event_id)
                );

                CREATE TABLE IF NOT EXISTS outbox (
                    org_id TEXT NOT NULL,
                    workspace_id TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    transition_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    event_revision INTEGER NOT NULL,
                    dispatched INTEGER NOT NULL DEFAULT 0 CHECK (dispatched IN (0, 1)),
                    delivery_attempts INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    dispatched_at TEXT,
                    PRIMARY KEY (org_id, workspace_id, event_id),
                    UNIQUE (org_id, workspace_id, transition_id),
                    FOREIGN KEY (org_id, workspace_id, transition_id)
                        REFERENCES transitions(org_id, workspace_id, transition_id)
                );

                CREATE TABLE IF NOT EXISTS projection_receipts (
                    consumer_id TEXT NOT NULL,
                    org_id TEXT NOT NULL,
                    workspace_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    transition_id TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    event_revision INTEGER NOT NULL,
                    applied_at TEXT NOT NULL,
                    PRIMARY KEY (consumer_id, org_id, workspace_id, transition_id)
                );

                CREATE TRIGGER IF NOT EXISTS transitions_no_update
                BEFORE UPDATE ON transitions
                BEGIN
                    SELECT RAISE(ABORT, 'transitions are append-only');
                END;

                CREATE TRIGGER IF NOT EXISTS transitions_no_delete
                BEFORE DELETE ON transitions
                BEGIN
                    SELECT RAISE(ABORT, 'transitions are append-only');
                END;
                """
            )

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _encode(value: Mapping[str, Any]) -> str:
        try:
            return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        except (TypeError, ValueError) as exc:
            raise DurableStateEventError("value must be JSON-serializable") from exc

    @staticmethod
    def _decode(value: str) -> dict[str, Any]:
        decoded = json.loads(value)
        if not isinstance(decoded, dict):
            raise DurableStateEventError("stored JSON must decode to an object")
        return decoded

    @staticmethod
    def _require_id(name: str, value: str) -> str:
        normalized = str(value).strip()
        if not normalized:
            raise DurableStateEventError(f"{name} must not be empty")
        return normalized

    @staticmethod
    def _fault(fault: str | None, point: str) -> None:
        if fault == point:
            raise InjectedFailure(point)

    def _existing_mutation(
        self,
        connection: sqlite3.Connection,
        *,
        org_id: str,
        workspace_id: str,
        resource_type: str,
        resource_id: str,
        mutation_id: str,
    ) -> CommittedTransition | None:
        row = connection.execute(
            """
            SELECT * FROM transitions
            WHERE org_id = ? AND workspace_id = ? AND resource_type = ?
              AND resource_id = ? AND mutation_id = ?
            """,
            (org_id, workspace_id, resource_type, resource_id, mutation_id),
        ).fetchone()
        return None if row is None else self._transition_from_row(row)

    def _allocate_event_revision(
        self, connection: sqlite3.Connection, *, org_id: str, workspace_id: str, run_id: str
    ) -> int:
        row = connection.execute(
            """
            SELECT last_event_revision FROM run_event_sequence
            WHERE org_id = ? AND workspace_id = ? AND run_id = ?
            """,
            (org_id, workspace_id, run_id),
        ).fetchone()
        if row is None:
            event_revision = 1
            connection.execute(
                """
                INSERT INTO run_event_sequence(org_id, workspace_id, run_id, last_event_revision)
                VALUES (?, ?, ?, ?)
                """,
                (org_id, workspace_id, run_id, event_revision),
            )
        else:
            event_revision = int(row["last_event_revision"]) + 1
            connection.execute(
                """
                UPDATE run_event_sequence SET last_event_revision = ?
                WHERE org_id = ? AND workspace_id = ? AND run_id = ?
                """,
                (event_revision, org_id, workspace_id, run_id),
            )
        return event_revision

    def commit(
        self,
        *,
        org_id: str,
        workspace_id: str,
        run_id: str,
        resource_type: str,
        resource_id: str,
        expected_revision: int,
        expected_ownership_epoch: int,
        mutation_id: str,
        state: Mapping[str, Any],
        event_type: str,
        payload: Mapping[str, Any] | None = None,
        transition_id: str | None = None,
        event_id: str | None = None,
        fault: str | None = None,
    ) -> CommittedTransition:
        org_id = self._require_id("org_id", org_id)
        workspace_id = self._require_id("workspace_id", workspace_id)
        run_id = self._require_id("run_id", run_id)
        resource_type = self._require_id("resource_type", resource_type)
        resource_id = self._require_id("resource_id", resource_id)
        mutation_id = self._require_id("mutation_id", mutation_id)
        event_type = self._require_id("event_type", event_type)
        if expected_revision < 0 or expected_ownership_epoch < 0:
            raise DurableStateEventError("expected revisions must be non-negative")
        state_json = self._encode(state)
        payload_json = self._encode(payload or {})
        occurred_at = self._now()

        with self._transaction() as connection:
            existing = self._existing_mutation(
                connection,
                org_id=org_id,
                workspace_id=workspace_id,
                resource_type=resource_type,
                resource_id=resource_id,
                mutation_id=mutation_id,
            )
            if existing is not None:
                return existing

            self._fault(fault, "before_state_write")
            row = connection.execute(
                """
                SELECT run_id, revision, ownership_epoch FROM resources
                WHERE org_id = ? AND workspace_id = ? AND resource_type = ? AND resource_id = ?
                """,
                (org_id, workspace_id, resource_type, resource_id),
            ).fetchone()

            if row is None:
                if expected_revision != 0:
                    raise StaleWriteError(
                        f"expected revision {expected_revision}; resource does not yet exist"
                    )
                if expected_ownership_epoch != 0:
                    raise OwnershipEpochError(
                        f"expected ownership epoch {expected_ownership_epoch}; new resource requires 0"
                    )
                previous_revision = 0
                result_revision = 1
                ownership_epoch = 0
                connection.execute(
                    """
                    INSERT INTO resources(
                        org_id, workspace_id, resource_type, resource_id, run_id,
                        revision, ownership_epoch, state_json, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        org_id,
                        workspace_id,
                        resource_type,
                        resource_id,
                        run_id,
                        result_revision,
                        ownership_epoch,
                        state_json,
                        occurred_at,
                    ),
                )
            else:
                current_revision = int(row["revision"])
                current_epoch = int(row["ownership_epoch"])
                if str(row["run_id"]) != run_id:
                    raise DurableStateEventError("resource run_id is immutable")
                if current_revision != expected_revision:
                    raise StaleWriteError(
                        f"expected revision {expected_revision}; current revision is {current_revision}"
                    )
                if current_epoch != expected_ownership_epoch:
                    raise OwnershipEpochError(
                        f"expected ownership epoch {expected_ownership_epoch}; current epoch is {current_epoch}"
                    )
                previous_revision = current_revision
                result_revision = current_revision + 1
                ownership_epoch = current_epoch
                cursor = connection.execute(
                    """
                    UPDATE resources
                    SET revision = ?, state_json = ?, updated_at = ?
                    WHERE org_id = ? AND workspace_id = ? AND resource_type = ? AND resource_id = ?
                      AND revision = ? AND ownership_epoch = ?
                    """,
                    (
                        result_revision,
                        state_json,
                        occurred_at,
                        org_id,
                        workspace_id,
                        resource_type,
                        resource_id,
                        expected_revision,
                        expected_ownership_epoch,
                    ),
                )
                if cursor.rowcount != 1:
                    raise StaleWriteError("compare-and-swap failed")

            self._fault(fault, "after_state_write")
            event_revision = self._allocate_event_revision(
                connection, org_id=org_id, workspace_id=workspace_id, run_id=run_id
            )
            transition_id = transition_id or f"tr-{uuid.uuid4().hex}"
            event_id = event_id or f"ev-{uuid.uuid4().hex}"
            connection.execute(
                """
                INSERT INTO transitions(
                    org_id, workspace_id, run_id, resource_type, resource_id,
                    transition_id, mutation_id, previous_revision, result_revision,
                    ownership_epoch, event_id, event_type, event_revision, occurred_at,
                    state_json, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    org_id,
                    workspace_id,
                    run_id,
                    resource_type,
                    resource_id,
                    transition_id,
                    mutation_id,
                    previous_revision,
                    result_revision,
                    ownership_epoch,
                    event_id,
                    event_type,
                    event_revision,
                    occurred_at,
                    state_json,
                    payload_json,
                ),
            )
            self._fault(fault, "after_transition_write")
            connection.execute(
                """
                INSERT INTO outbox(
                    org_id, workspace_id, event_id, transition_id, run_id,
                    event_revision, dispatched, delivery_attempts, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?)
                """,
                (
                    org_id,
                    workspace_id,
                    event_id,
                    transition_id,
                    run_id,
                    event_revision,
                    occurred_at,
                ),
            )
            self._fault(fault, "after_outbox_write")

        committed = CommittedTransition(
            org_id=org_id,
            workspace_id=workspace_id,
            run_id=run_id,
            resource_type=resource_type,
            resource_id=resource_id,
            transition_id=transition_id,
            mutation_id=mutation_id,
            previous_revision=previous_revision,
            result_revision=result_revision,
            ownership_epoch=ownership_epoch,
            event_id=event_id,
            event_type=event_type,
            event_revision=event_revision,
            occurred_at=occurred_at,
            state=self._decode(state_json),
            payload=self._decode(payload_json),
        )
        self._fault(fault, "after_commit")
        return committed

    def load(
        self, *, org_id: str, workspace_id: str, resource_type: str, resource_id: str
    ) -> ResourceSnapshot:
        with self._read() as connection:
            row = connection.execute(
                """
                SELECT * FROM resources
                WHERE org_id = ? AND workspace_id = ? AND resource_type = ? AND resource_id = ?
                """,
                (org_id, workspace_id, resource_type, resource_id),
            ).fetchone()
        if row is None:
            raise ResourceNotFoundError(resource_id)
        return ResourceSnapshot(
            org_id=str(row["org_id"]),
            workspace_id=str(row["workspace_id"]),
            run_id=str(row["run_id"]),
            resource_type=str(row["resource_type"]),
            resource_id=str(row["resource_id"]),
            revision=int(row["revision"]),
            ownership_epoch=int(row["ownership_epoch"]),
            state=self._decode(str(row["state_json"])),
            updated_at=str(row["updated_at"]),
        )

    def history(
        self, *, org_id: str, workspace_id: str, resource_type: str, resource_id: str
    ) -> tuple[CommittedTransition, ...]:
        with self._read() as connection:
            rows = connection.execute(
                """
                SELECT * FROM transitions
                WHERE org_id = ? AND workspace_id = ? AND resource_type = ? AND resource_id = ?
                ORDER BY result_revision ASC
                """,
                (org_id, workspace_id, resource_type, resource_id),
            ).fetchall()
        return tuple(self._transition_from_row(row) for row in rows)

    def replay_events(
        self,
        *,
        org_id: str,
        workspace_id: str,
        run_id: str,
        after_event_revision: int = 0,
    ) -> tuple[dict[str, Any], ...]:
        if after_event_revision < 0:
            raise DurableStateEventError("after_event_revision must be non-negative")
        with self._read() as connection:
            rows = connection.execute(
                """
                SELECT * FROM transitions
                WHERE org_id = ? AND workspace_id = ? AND run_id = ? AND event_revision > ?
                ORDER BY event_revision ASC
                """,
                (org_id, workspace_id, run_id, after_event_revision),
            ).fetchall()
        return tuple(self._transition_from_row(row).event_envelope() for row in rows)

    def pending_outbox(
        self, *, org_id: str, workspace_id: str, run_id: str
    ) -> tuple[dict[str, Any], ...]:
        with self._read() as connection:
            rows = connection.execute(
                """
                SELECT t.*
                FROM outbox o
                JOIN transitions t
                  ON t.org_id = o.org_id AND t.workspace_id = o.workspace_id
                 AND t.transition_id = o.transition_id
                WHERE o.org_id = ? AND o.workspace_id = ? AND o.run_id = ? AND o.dispatched = 0
                ORDER BY o.event_revision ASC
                """,
                (org_id, workspace_id, run_id),
            ).fetchall()
        return tuple(self._transition_from_row(row).event_envelope() for row in rows)

    def mark_dispatched(self, *, org_id: str, workspace_id: str, event_id: str) -> None:
        with self._transaction() as connection:
            row = connection.execute(
                """
                SELECT dispatched FROM outbox
                WHERE org_id = ? AND workspace_id = ? AND event_id = ?
                """,
                (org_id, workspace_id, event_id),
            ).fetchone()
            if row is None:
                raise DurableStateEventError(f"outbox event not found: {event_id}")
            connection.execute(
                """
                UPDATE outbox
                SET dispatched = 1,
                    delivery_attempts = delivery_attempts + 1,
                    dispatched_at = COALESCE(dispatched_at, ?)
                WHERE org_id = ? AND workspace_id = ? AND event_id = ?
                """,
                (self._now(), org_id, workspace_id, event_id),
            )

    def reconcile_outbox(self, *, org_id: str, workspace_id: str, run_id: str) -> int:
        with self._transaction() as connection:
            rows = connection.execute(
                """
                SELECT t.*
                FROM transitions t
                LEFT JOIN outbox o
                  ON o.org_id = t.org_id AND o.workspace_id = t.workspace_id
                 AND o.transition_id = t.transition_id
                WHERE t.org_id = ? AND t.workspace_id = ? AND t.run_id = ?
                  AND o.transition_id IS NULL
                ORDER BY t.event_revision ASC
                """,
                (org_id, workspace_id, run_id),
            ).fetchall()
            for row in rows:
                connection.execute(
                    """
                    INSERT INTO outbox(
                        org_id, workspace_id, event_id, transition_id, run_id,
                        event_revision, dispatched, delivery_attempts, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?)
                    """,
                    (
                        row["org_id"],
                        row["workspace_id"],
                        row["event_id"],
                        row["transition_id"],
                        row["run_id"],
                        row["event_revision"],
                        row["occurred_at"],
                    ),
                )
            return len(rows)

    def project_once(self, *, consumer_id: str, event: Mapping[str, Any]) -> ProjectionReceipt:
        required = (
            "org_id",
            "workspace_id",
            "run_id",
            "transition_id",
            "event_id",
            "event_revision",
            "result_revision",
        )
        for field in required:
            if field not in event:
                raise DurableStateEventError(f"event missing {field}")
        applied_at = self._now()
        with self._transaction() as connection:
            authoritative = connection.execute(
                """
                SELECT 1 FROM transitions
                WHERE org_id = ? AND workspace_id = ? AND run_id = ?
                  AND transition_id = ? AND event_id = ?
                  AND event_revision = ? AND result_revision = ?
                """,
                (
                    event["org_id"],
                    event["workspace_id"],
                    event["run_id"],
                    event["transition_id"],
                    event["event_id"],
                    int(event["event_revision"]),
                    int(event["result_revision"]),
                ),
            ).fetchone()
            if authoritative is None:
                raise UncommittedEventError("event has no matching authoritative committed transition")
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO projection_receipts(
                    consumer_id, org_id, workspace_id, run_id, transition_id,
                    event_id, event_revision, applied_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    consumer_id,
                    event["org_id"],
                    event["workspace_id"],
                    event["run_id"],
                    event["transition_id"],
                    event["event_id"],
                    int(event["event_revision"]),
                    applied_at,
                ),
            )
        return ProjectionReceipt(
            consumer_id=consumer_id,
            transition_id=str(event["transition_id"]),
            event_id=str(event["event_id"]),
            event_revision=int(event["event_revision"]),
            applied=cursor.rowcount == 1,
        )

    def projection_count(self, *, consumer_id: str, org_id: str, workspace_id: str) -> int:
        with self._read() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS count FROM projection_receipts
                WHERE consumer_id = ? AND org_id = ? AND workspace_id = ?
                """,
                (consumer_id, org_id, workspace_id),
            ).fetchone()
        return int(row["count"])

    def backup_to(self, destination: str | Path) -> Path:
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        source = self._connect()
        target = sqlite3.connect(str(destination), timeout=30.0)
        try:
            source.backup(target)
            result = target.execute("PRAGMA integrity_check").fetchone()
            if result is None or str(result[0]).lower() != "ok":
                raise DurableStateEventError("backup integrity_check failed")
        finally:
            target.close()
            source.close()
        return destination

    @classmethod
    def restore_from(cls, backup_path: str | Path, destination: str | Path) -> "SQLiteDurableStateEventStore":
        backup_path = Path(backup_path)
        destination = Path(destination)
        if not backup_path.exists():
            raise DurableStateEventError(f"backup does not exist: {backup_path}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            destination.unlink()
        shutil.copy2(backup_path, destination)
        store = cls(destination)
        with store._read() as connection:
            result = connection.execute("PRAGMA integrity_check").fetchone()
            if result is None or str(result[0]).lower() != "ok":
                raise DurableStateEventError("restored database integrity_check failed")
        return store

    def audit_invariants(self) -> dict[str, int]:
        with self._read() as connection:
            state_without_latest_transition = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM resources r
                LEFT JOIN transitions t
                  ON t.org_id = r.org_id AND t.workspace_id = r.workspace_id
                 AND t.resource_type = r.resource_type AND t.resource_id = r.resource_id
                 AND t.result_revision = r.revision
                WHERE t.transition_id IS NULL
                """
            ).fetchone()["count"]
            transition_without_state = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM transitions t
                LEFT JOIN resources r
                  ON r.org_id = t.org_id AND r.workspace_id = t.workspace_id
                 AND r.resource_type = t.resource_type AND r.resource_id = t.resource_id
                WHERE r.resource_id IS NULL OR r.revision < t.result_revision
                """
            ).fetchone()["count"]
            transition_without_outbox = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM transitions t
                LEFT JOIN outbox o
                  ON o.org_id = t.org_id AND o.workspace_id = t.workspace_id
                 AND o.transition_id = t.transition_id
                WHERE o.transition_id IS NULL
                """
            ).fetchone()["count"]
        return {
            "state_without_latest_transition": int(state_without_latest_transition),
            "transition_without_state": int(transition_without_state),
            "transition_without_outbox": int(transition_without_outbox),
        }

    def _transition_from_row(self, row: sqlite3.Row) -> CommittedTransition:
        return CommittedTransition(
            org_id=str(row["org_id"]),
            workspace_id=str(row["workspace_id"]),
            run_id=str(row["run_id"]),
            resource_type=str(row["resource_type"]),
            resource_id=str(row["resource_id"]),
            transition_id=str(row["transition_id"]),
            mutation_id=str(row["mutation_id"]),
            previous_revision=int(row["previous_revision"]),
            result_revision=int(row["result_revision"]),
            ownership_epoch=int(row["ownership_epoch"]),
            event_id=str(row["event_id"]),
            event_type=str(row["event_type"]),
            event_revision=int(row["event_revision"]),
            occurred_at=str(row["occurred_at"]),
            state=self._decode(str(row["state_json"])),
            payload=self._decode(str(row["payload_json"])),
        )
