from __future__ import annotations

import json
import os
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict

from dbos import DBOS, DBOSConfig, SetWorkflowID
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SideEffectProbe:
    """Benchmark-only durable provider probe.

    Physical attempts are always recorded. Logical effects are deduplicated by a
    stable effect key so duplicate-cost exposure is visible without inventing a
    real provider price.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path)
        try:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    effect_key TEXT NOT NULL,
                    occurred_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS unique_effects (
                    effect_key TEXT PRIMARY KEY,
                    first_seen_at TEXT NOT NULL
                );
                """
            )
            conn.commit()
        finally:
            conn.close()

    def record(self, effect_key: str) -> dict[str, Any]:
        conn = sqlite3.connect(self.path, timeout=30.0, isolation_level=None)
        try:
            conn.execute("BEGIN IMMEDIATE")
            now = utc_now()
            conn.execute("INSERT INTO attempts(effect_key, occurred_at) VALUES (?, ?)", (effect_key, now))
            conn.execute(
                "INSERT OR IGNORE INTO unique_effects(effect_key, first_seen_at) VALUES (?, ?)",
                (effect_key, now),
            )
            attempts = int(
                conn.execute("SELECT COUNT(*) FROM attempts WHERE effect_key = ?", (effect_key,)).fetchone()[0]
            )
            conn.commit()
            return {
                "effect_key": effect_key,
                "attempt_number_for_key": attempts,
                "duplicate_attempt": attempts > 1,
            }
        finally:
            conn.close()

    def summary(self) -> dict[str, Any]:
        conn = sqlite3.connect(self.path)
        try:
            total = int(conn.execute("SELECT COUNT(*) FROM attempts").fetchone()[0])
            unique = int(conn.execute("SELECT COUNT(*) FROM unique_effects").fetchone()[0])
        finally:
            conn.close()
        return {
            "physical_attempts": total,
            "unique_effects": unique,
            "duplicate_attempts": total - unique,
            "externally_billed_cost": "NOT_OBSERVED",
        }


def provider_effect(candidate: str, root: str | Path, execution_id: str, branch_id: str, crash_once: bool) -> dict[str, Any]:
    root = Path(root)
    probe = SideEffectProbe(root / "provider-effects.sqlite3")
    effect = probe.record(f"{candidate}:{execution_id}:{branch_id}")
    marker = root / f"crash-once-{execution_id}.marker"
    if crash_once and not marker.exists():
        marker.write_text("crashed-after-provider-effect-before-runtime-checkpoint\n", encoding="utf-8")
        os._exit(91)
    return {
        "candidate": candidate,
        "execution_id": execution_id,
        "branch_id": branch_id,
        "effect": effect,
    }


@DBOS.step()
def dbos_provider_step(root: str, execution_id: str, branch_id: str, crash_once: bool) -> dict[str, Any]:
    return provider_effect("dbos", root, execution_id, branch_id, crash_once)


@DBOS.workflow()
def dbos_branch_workflow(root: str, execution_id: str, branch_id: str, crash_once: bool) -> dict[str, Any]:
    return dbos_provider_step(root, execution_id, branch_id, crash_once)


class LangGraphState(TypedDict, total=False):
    root: str
    execution_id: str
    branch_id: str
    crash_once: bool
    result: dict[str, Any]


@dataclass
class Invocation:
    result: dict[str, Any]
    elapsed_ms: float


class CustomCASAdapter:
    name = "custom_cas"

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = self.root / "runtime.sqlite3"
        conn = sqlite3.connect(self.db)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS executions (execution_id TEXT PRIMARY KEY, branch_id TEXT NOT NULL, result_json TEXT NOT NULL)"
            )
            conn.commit()
        finally:
            conn.close()

    def invoke(self, execution_id: str, branch_id: str, *, crash_once: bool = False) -> Invocation:
        started = time.perf_counter_ns()
        conn = sqlite3.connect(self.db, timeout=30.0)
        try:
            row = conn.execute("SELECT result_json FROM executions WHERE execution_id = ?", (execution_id,)).fetchone()
            if row is not None:
                result = json.loads(str(row[0]))
                result["runtime_replay"] = True
            else:
                result = provider_effect(self.name, self.root, execution_id, branch_id, crash_once)
                conn.execute(
                    "INSERT INTO executions(execution_id, branch_id, result_json) VALUES (?, ?, ?)",
                    (execution_id, branch_id, json.dumps(result, sort_keys=True)),
                )
                conn.commit()
                result["runtime_replay"] = False
        finally:
            conn.close()
        return Invocation(result, (time.perf_counter_ns() - started) / 1_000_000)

    def close(self) -> None:
        return None


class LangGraphAdapter:
    name = "langgraph"

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.root / "langgraph-checkpoints.sqlite3", check_same_thread=False)
        self.checkpointer = SqliteSaver(self.conn)

        def execute(state: LangGraphState) -> dict[str, Any]:
            return {
                "result": provider_effect(
                    self.name,
                    state["root"],
                    state["execution_id"],
                    state["branch_id"],
                    bool(state.get("crash_once", False)),
                )
            }

        builder = StateGraph(LangGraphState)
        builder.add_node("execute", execute)
        builder.add_edge(START, "execute")
        builder.add_edge("execute", END)
        self.graph = builder.compile(checkpointer=self.checkpointer)

    def invoke(self, execution_id: str, branch_id: str, *, crash_once: bool = False) -> Invocation:
        started = time.perf_counter_ns()
        state = self.graph.invoke(
            {
                "root": str(self.root),
                "execution_id": execution_id,
                "branch_id": branch_id,
                "crash_once": crash_once,
            },
            config={"configurable": {"thread_id": execution_id}},
        )
        return Invocation(dict(state["result"]), (time.perf_counter_ns() - started) / 1_000_000)

    def close(self) -> None:
        self.conn.close()


def safe_dbos_destroy(timeout: int = 1) -> None:
    try:
        DBOS.destroy(workflow_completion_timeout_sec=timeout)
    except Exception:
        pass


class DBOSAdapter:
    name = "dbos"

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        safe_dbos_destroy(1)
        config: DBOSConfig = {
            "name": "academy-w006-t005-a02",
            "application_version": "w006-t005-a02-v1",
            "system_database_url": f"sqlite:///{self.root / 'dbos-system.sqlite3'}",
        }
        DBOS(config=config)
        DBOS.launch()

    def invoke(self, execution_id: str, branch_id: str, *, crash_once: bool = False) -> Invocation:
        started = time.perf_counter_ns()
        with SetWorkflowID(execution_id):
            result = dbos_branch_workflow(str(self.root), execution_id, branch_id, crash_once)
        return Invocation(dict(result), (time.perf_counter_ns() - started) / 1_000_000)

    def close(self) -> None:
        safe_dbos_destroy(2)


ADAPTERS = {
    "custom_cas": CustomCASAdapter,
    "langgraph": LangGraphAdapter,
    "dbos": DBOSAdapter,
}
