from __future__ import annotations

import ast
import json
from pathlib import Path
from time import perf_counter

from . import durability_probe, plain_async

ROOT = Path(__file__).parent


def logical_loc(path: Path) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return sum(1 for node in ast.walk(tree) if isinstance(node, (ast.stmt, ast.ExceptHandler)))


def run_benchmark() -> dict:
    started = perf_counter()
    plain_state, plain_history = plain_async.run()
    plain_ms = (perf_counter() - started) * 1000

    report = {
        "plain_async": {
            "runtime_ms": round(plain_ms, 3),
            "history_snapshots": len(plain_history),
            "joined_outputs": len(plain_state["outputs"]),
            "repair_count": sum(v["repair_count"] for v in plain_state["outputs"].values()),
            "orchestration_logical_loc": logical_loc(ROOT / "plain_async.py"),
        },
        "production_durability": durability_probe.run_bakeoff(),
        "langgraph": {
            "orchestration_logical_loc": logical_loc(ROOT / "langgraph_stategraph.py"),
        },
    }

    try:
        from . import langgraph_hazards, langgraph_stategraph
    except ImportError as exc:
        report["langgraph"]["runtime_status"] = f"UNAVAILABLE: {exc}"
        return report

    started = perf_counter()
    state, history = langgraph_stategraph.run()
    hazard = langgraph_hazards.run_hazard_probe()
    report["langgraph"].update(
        {
            "runtime_ms": round((perf_counter() - started) * 1000, 3),
            "runtime_status": "PASS",
            "history_snapshots": len(history),
            "joined_outputs": len(state["outputs"]),
            "repair_count": sum(v["repair_count"] for v in state["outputs"].values()),
            "missing_reducer_probe": hazard,
        }
    )
    return report


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2, sort_keys=True))
