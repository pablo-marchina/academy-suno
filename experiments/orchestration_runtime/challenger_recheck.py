from __future__ import annotations

import json


def main() -> None:
    """Run the W002 LangGraph challenger unchanged; never substitute a local rewrite."""
    try:
        from experiments.orchestration_smoke.langgraph_stategraph import run

        final, history = run()
    except ModuleNotFoundError as exc:
        print(json.dumps({"challenger": "W002 unchanged", "runtime_status": f"UNAVAILABLE: {exc}"}))
        return

    print(
        json.dumps(
            {
                "challenger": "W002 unchanged",
                "runtime_status": "PASS",
                "joined_outputs": len(final["outputs"]),
                "history_snapshots": len(history),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
