# Orchestration runtime proof

This directory exercises B06 without changing the W002 challenger.

- `runtime_demo.py` runs the provisional plain-async leader end to end with an explicit graph, 9 keyed branches, one transport retry, one branch-local quality repair, a durable SQLite checkpoint, process-style reopen/resume, lossless join, aggregation, and persistent history.
- `challenger_recheck.py` imports and executes `experiments.orchestration_smoke.langgraph_stategraph` directly. It intentionally contains no rewritten LangGraph implementation: promotion requires runtime evidence from the unchanged challenger.

Run from repository root:

```bash
PYTHONPATH=src:. python experiments/orchestration_runtime/runtime_demo.py
PYTHONPATH=src:. python experiments/orchestration_runtime/challenger_recheck.py
PYTHONPATH=src python -m unittest discover -s tests/orchestration -v
PYTHONPATH=src python -m unittest discover -s tests/runstore -v
```

If LangGraph is absent, the challenger command reports `UNAVAILABLE` and plain async remains provisional; absence is not evidence against LangGraph.
