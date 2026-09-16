# Foundation regression — clean-checkout gate

This directory closes the W002-T010 execution limitation: the accepted W002 foundation is exercised together from a clean repository checkout, independently from the canonical `System Integrity` workflow.

## What the gate runs

`run_foundation_regression.py` is the single reproducible entry point. It:

1. compiles `src`, `tests`, and `experiments`;
2. runs the critical W002 suites together: domain, factual, policy, formats, generation, orchestration smoke, and the cross-package foundation integration test;
3. replays the frozen factual oracle against the persisted observed results;
4. reruns the deterministic offline parser/source-trust bakeoff and asserts that table-role loss remains review-required and wrong-role silent corruption remains a hard failure;
5. reruns the orchestration benchmark and persists its report;
6. writes logs plus a machine-readable `manifest.json` to an artifact directory.

The new integration test deliberately composes one canonical source through domain/provenance, factual backbone, policy, 3×3 planning, and native-format generation boundaries. It also verifies that a policy hard fail cannot be laundered by a disclaimer.

## Reproduce locally from a clean checkout

The CI environment is intentionally minimal and pins the dependency versions already used as W002 runtime evidence:

```bash
python -m pip install --disable-pip-version-check --no-cache-dir \
  'pydantic==2.13.4' 'pytest==9.0.2'
python experiments/foundation_regression/run_foundation_regression.py
```

Optional artifact location:

```bash
FOUNDATION_ARTIFACT_DIR=/tmp/foundation-regression \
  python experiments/foundation_regression/run_foundation_regression.py
```

No live source fetch is required. The parser bakeoff runs in its deterministic observed-behavior mode.

## Deliberate non-workarounds

This gate does **not** weaken or bypass source, factual, policy, or format hard gates. A cross-package incompatibility must fail the runner and appear in its logs/manifest.

LangGraph is also not installed merely to make this gate green. W002 left the LangGraph challenger as `PENDING_RUNTIME_RECHECK`; the orchestration smoke suite may therefore retain its explicit skip while the benchmark records LangGraph as unavailable. The executed plain-async proof remains part of the regression gate. A later task can install and re-run the unchanged challenger as evidence without changing the foundation acceptance semantics.

## CI separation

`.github/workflows/foundation-tests.yml` owns application/foundation regression. `.github/workflows/system-integrity.yml` continues to own canonical-system validation. They are intentionally separate checks with separate failure domains.
