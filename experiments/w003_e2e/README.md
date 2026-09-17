# W003 end-to-end mechanics proof

`run_proof.py` composes the integrated W003 orchestration, RunStore, grounding hard-gate semantics, audience diagnostics, targeted repair directives and telemetry around an explicitly deterministic stub provider.

The run is **mechanics evidence only**. It must not be read as provider/model quality, latency, cost, calibrated audience-threshold, semantic-backend or production-readiness evidence.

Run from repository root:

```bash
PYTHONPATH=src python experiments/w003_e2e/run_proof.py --output-dir /tmp/w003-e2e-evidence
python -m unittest discover -s tests/integration/w003 -v
```

The proof deliberately injects one factual/audience failure on `beginner:carousel`, one transport timeout on `advanced:short_video`, pauses after all nine branches settle, reopens the SQLite RunStore, resumes through join/aggregate/complete, and records run/job/attempt telemetry. It also executes a non-compensation probe where audience diagnostics are clean but the factual hard gate fails; the terminal evaluation remains non-PASS.

Generated evidence files are intentionally written outside version control by default during validation. Persisted release claims belong in the task RESULT with the exact evidence classification.
