# EXP-B — orchestration smoke test

Two baselines share the same deterministic mock contracts in `common.py`:

- `plain_async.py`: `asyncio.gather` + a tiny explicit in-memory checkpoint store.
- `langgraph_stategraph.py`: LangGraph `StateGraph` + `Send` fan-out + keyed reducer + `InMemorySaver` + static breakpoint/resume.

The experiment creates all 9 audience×format jobs. `beginner:carousel` deliberately fails first-pass quality and is repaired locally; the other eight branches are never repaired. Join invariants require all nine keyed outputs.

Run with Python 3.12+:

```bash
python -m pip install -r experiments/orchestration_smoke/requirements.txt
python -m experiments.orchestration_smoke.benchmark
pytest -q tests/experiments/orchestration
```

`langgraph_hazards.py` also runs an unsafe parallel-state probe without a reducer. Current LangGraph is expected to reject concurrent writes rather than silently select one; the resulting error makes reducer/state-loss risk explicit.
