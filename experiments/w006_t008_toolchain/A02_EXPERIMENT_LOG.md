# W006-T008-A02 — Canonical Experiment Log

`TASK_ID: W006-T008`
`ATTEMPT_ID: A02`
`REGISTERED_AT_UTC: 2026-09-23T14:51:46Z`
`PROTOCOL_COMMIT: b40e5fdf1840398f8557ec79c946ab504ad302f9`
`STATUS: PREREGISTERED / EXECUTION_PENDING`

This is the single canonical A02 experiment log. The accepted protocol is defined in `docs/decisions/research/DR-6008-reproducible-toolchain-supply-chain.md`. A01 evidence is diagnostic only and is never substituted for A02 observations.

## Environment contract

- runner: GitHub-hosted `ubuntu-24.04`;
- Python: `3.13.15`;
- package-manager candidates: `uv==0.12.18`, `poetry==2.5.1`, `pdm==2.29.2`;
- candidate tools provisioned in separate venvs;
- real dependency graph: identical direct dependencies extracted from the A02 root `pyproject.toml`;
- repeats: 3 per candidate;
- raw candidate locks: preserve first-repeat lock inputs/outputs;
- no package-manager result is accepted if lock/sync/import/relock hard gates fail.

## E1 — Same-runner package-manager bakeoff

Canonical command executed by workflow:

```bash
python experiments/w006_t008_toolchain/benchmark_real_graph.py \
  --repeats 3 \
  --output /tmp/w006-t008-evidence/manager-benchmark.json \
  --locks-dir /tmp/w006-t008-evidence/candidate-locks
```

Preconditions:

```bash
python -m venv /tmp/w006-t008-tools/uv
/tmp/w006-t008-tools/uv/bin/python -m pip install --disable-pip-version-check --no-cache-dir 'uv==0.12.18'
python -m venv /tmp/w006-t008-tools/poetry
/tmp/w006-t008-tools/poetry/bin/python -m pip install --disable-pip-version-check --no-cache-dir 'poetry==2.5.1'
python -m venv /tmp/w006-t008-tools/pdm
/tmp/w006-t008-tools/pdm/bin/python -m pip install --disable-pip-version-check --no-cache-dir 'pdm==2.29.2'
```

Measurements to record per repeat: first lock seconds/exit, first sync seconds/exit, import verification exit, warm sync seconds/exit, repeat lock seconds/exit, lock SHA-256 before/after and equality.

Raw artifact destination: GitHub Actions artifact `w006-t008-toolchain-bakeoff-<A02_HEAD_SHA>`.

A02 observations: **PENDING**.

## E2 — Frozen supply-chain/reproducibility contract

Canonical selected-baseline commands, if E1 supports a provisional lock:

```bash
uv lock --check
uv sync --locked --no-install-project --group test
uv run --no-sync python -m compileall -q src tests experiments scripts
uv run --no-sync python experiments/foundation_regression/run_foundation_regression.py
uv run --no-sync python scripts/supply_chain/audit_release_workflows.py --output /tmp/w006-t008-evidence/release-workflow-audit.json
uv run --no-sync python scripts/supply_chain/build_release_evidence.py --output-dir /tmp/w006-t008-evidence/release
uv run --no-sync python scripts/supply_chain/build_release_evidence.py --output-dir /tmp/w006-t008-evidence/release-repeat
cmp /tmp/w006-t008-evidence/release/academy-suno-source.tar.gz /tmp/w006-t008-evidence/release-repeat/academy-suno-source.tar.gz
cmp /tmp/w006-t008-evidence/release/academy-suno-source.tar.gz.spdx.json /tmp/w006-t008-evidence/release-repeat/academy-suno-source.tar.gz.spdx.json
cmp /tmp/w006-t008-evidence/release/academy-suno-source.tar.gz.provenance.json /tmp/w006-t008-evidence/release-repeat/academy-suno-source.tar.gz.provenance.json
uv run --no-sync python scripts/supply_chain/verify_release_evidence.py --artifact /tmp/w006-t008-evidence/release/academy-suno-source.tar.gz --sbom /tmp/w006-t008-evidence/release/academy-suno-source.tar.gz.spdx.json --provenance /tmp/w006-t008-evidence/release/academy-suno-source.tar.gz.provenance.json --lockfile uv.lock
```

GitHub attestation control:

```bash
gh attestation verify /tmp/w006-t008-evidence/release/academy-suno-source.tar.gz --repo "$GITHUB_REPOSITORY"
```

Raw artifact destinations:

- `w006-t008-supply-chain-<A02_HEAD_SHA>`;
- `w006-t008-attestation-<A02_HEAD_SHA>` when the attestation job is eligible.

A02 observations: **PENDING**.

## Online/offline reproducibility boundary

- `ONLINE_INSTALL`: candidate provisioning and cold dependency install may contact the package index. The committed selected lock may not be rewritten in locked CI.
- `OFFLINE_VERIFY`: artifact SHA-256, SPDX document, local provenance subject digest and lock digest can be validated from already-present files without resolver/index access.
- not claimed: cold no-cache package installation with zero network access.

## A01 counterfactual reference

A01 diagnostic benchmark artifact: `artifacts/w006-t008/a01/manager-benchmark.json` and historical workflow run `35869987042`. It is retained only to detect gross A02 drift and coverage regressions. It is not copied into the A02 result row or used as a substitute for A02 measurements.

## Execution records

### Record A02-E1

- head SHA: PENDING
- workflow run: PENDING
- artifact ID/digest: PENDING
- runner image: PENDING
- exact provisioned candidate versions: PENDING
- raw benchmark path: PENDING
- result: PENDING

### Record A02-E2

- head SHA: PENDING
- workflow run: PENDING
- supply-chain artifact ID/digest: PENDING
- attestation artifact ID/digest: PENDING
- lock check: PENDING
- clean locked install: PENDING
- compile/foundation regression: PENDING
- deterministic double-build: PENDING
- movable release Action refs: PENDING
- broad token permissions: PENDING
- SBOM verification: PENDING
- local provenance digest binding: PENDING
- GitHub attestation verification: PENDING
- result: PENDING
