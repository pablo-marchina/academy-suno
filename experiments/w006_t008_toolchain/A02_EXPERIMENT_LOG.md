# W006-T008-A02 — Canonical Experiment Log

`TASK_ID: W006-T008`  
`ATTEMPT_ID: A02`  
`REGISTERED_AT_UTC: 2026-09-23T14:51:46Z`  
`PROTOCOL_COMMIT: b40e5fdf1840398f8557ec79c946ab504ad302f9`  
`MEASUREMENT_HEAD_SHA: 8dbd473e43306c3f15092b3742e91c23981d2317`  
`STATUS: COMPLETE`

This is the single canonical A02 experiment log. Criteria, weights, hard gates, sensitivity sets, source-search plan and stopping rule were committed in `docs/decisions/research/DR-6008-reproducible-toolchain-supply-chain.md` before the PR-triggered measurements. A01 evidence remained diagnostic only.

## Environment contract

- GitHub-hosted runner: `ubuntu-24.04`;
- observed platform: `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39`;
- Python: `3.13.15`;
- package-manager candidates: `uv==0.12.18`, `poetry==2.5.1`, `pdm==2.29.2`;
- manager tools provisioned in separate venvs;
- same seven direct dependencies extracted from the A02 root `pyproject.toml` for every candidate;
- repeats: `3`;
- raw first-repeat candidate locks preserved in the workflow artifact;
- no candidate-specific dependency graph changes were allowed.

Observed direct graph:

- `dbos==2.31.0`
- `jsonschema==4.25.1`
- `langgraph-checkpoint-sqlite==3.1.1`
- `langgraph==1.2.12`
- `pydantic==2.13.4`
- `pypdf==5.9.0`
- `pytest==9.0.2`

Root `pyproject.toml` SHA-256: `cd23fde7ba48562be54f2e5ec93921841ed9ecfb3314d3601852c94adc7d0af6`.

## E1 — Same-runner real-graph package-manager bakeoff

Workflow: `W006 T008 Toolchain Bakeoff`  
Run: `35878273774` — `SUCCESS`  
Artifact: `10760260339`  
Artifact digest: `sha256:837e99855b0063b3e7a419daab0be7cd9b1b3475f6157ec4a24a877e871ccd37`  
Artifact name: `w006-t008-toolchain-bakeoff-c79665bc2d0d70593a5789a94f75a458fe10bb66`

Canonical command:

```bash
python experiments/w006_t008_toolchain/benchmark_real_graph.py \
  --repeats 3 \
  --output /tmp/w006-t008-evidence/manager-benchmark.json \
  --locks-dir /tmp/w006-t008-evidence/candidate-locks
```

### Exact version probes

- uv: `uv 0.12.18 (x86_64-unknown-linux-gnu)`
- Poetry: `Poetry (version 2.5.1)`
- PDM: `PDM, version 2.29.2`

### Hard-gate outcome

All three candidates: `PASS` for availability, lock, locked/specified sync, import verification, warm sync, second lock and repeat lock byte stability on all 3 repeats.

### Raw timing observations

| candidate | repeat | first lock s | first sync s | warm sync s | second lock s | lock byte-stable |
|---|---:|---:|---:|---:|---:|---|
| uv | 1 | 0.3573 | 0.3592 | 0.0110 | 0.0085 | yes |
| uv | 2 | 0.0258 | 0.5235 | 0.0108 | 0.0088 | yes |
| uv | 3 | 0.0259 | 0.0311 | 0.0107 | 0.0087 | yes |
| Poetry | 1 | 3.1589 | 2.9666 | 0.8169 | 1.0461 | yes |
| Poetry | 2 | 2.2657 | 2.2784 | 0.8105 | 1.0435 | yes |
| Poetry | 3 | 2.2384 | 2.2522 | 0.8149 | 1.0470 | yes |
| PDM | 1 | 26.5778 | 13.8149 | 0.5614 | 25.4675 | yes |
| PDM | 2 | 25.4147 | 13.1153 | 0.5609 | 24.7006 | yes |
| PDM | 3 | 25.1480 | 12.9513 | 0.5601 | 24.9258 | yes |

Median observations used by the predeclared matrix:

| candidate | first lock s | first sync s | warm sync s | composite s |
|---|---:|---:|---:|---:|
| uv | 0.0259 | 0.3592 | 0.0108 | 0.3959 |
| Poetry | 2.2657 | 2.2784 | 0.8149 | 5.3590 |
| PDM | 25.4147 | 13.1153 | 0.5609 | 39.0909 |

Lock SHA-256 remained constant within every candidate across all repeats:

- uv: `a677c876a22fde37c40376ecbae6bc07c19ec3f76d8d3ff86807f552f15bd21e`
- Poetry: `6e8993ed60e5083dae4ea9704f091a88a465c8622c5f61b0ba2456f97d35f021`
- PDM: `30ca730a40b564cdfc73fab5e7fa33b8e0e23251e8ce9d007946dcc77bc5663e`

### Uncertainty / fairness notes

- package-index/network/cache state is not perfectly controllable on a hosted runner; therefore medians, not a single cold observation, are used;
- uv repeat 1 included package downloads and shows visible timing variance, but remained far below the other candidate medians;
- the benchmark project includes `[tool.pdm] distribution = false` for PDM compatibility, identically present for all candidates; it does not change the declared dependency graph;
- manager-specific features unrelated to this single-project workload were not assigned speculative benefits;
- no claim is made for polyglot monorepos, native/GPU/system packages, or deployment-image reproducibility.

## Decision matrix calculation

To avoid post-hoc subjective scores, all eligible candidates receive neutral `1.0` on non-efficiency criteria because A02 did not produce representative candidate-specific evidence distinguishing them after hard gates. Efficiency uses the preregistered measured dimensions and lower-is-better min-max normalization across eligible candidates:

`efficiency = (max_composite - candidate_composite) / (max_composite - min_composite)`

Efficiency scores:

- uv `1.000000`
- Poetry `0.871738`
- PDM `0.000000`

Totals:

| weights | uv | Poetry | PDM | unique leader |
|---|---:|---:|---:|---|
| base | 1.000000 | 0.974348 | 0.800000 | uv |
| S1 reproducibility-heavy | 1.000000 | 0.987174 | 0.900000 | uv |
| S2 efficiency-heavy | 1.000000 | 0.955108 | 0.650000 | uv |
| S3 portability-heavy | 1.000000 | 0.980761 | 0.850000 | uv |

Sensitivity result: stable unique leader in all 4 predeclared sets.

## E2 — Frozen supply-chain/reproducibility contract

Workflow: `W006 T008 Supply Chain`  
Run: `35878273770` — `SUCCESS`  
Supply artifact: `10759372264`, digest `sha256:3f61f6b2bba7bff59e7ca4563397598a797cd7fbc188cd580e07e9c104ac8905`  
Attestation-verification artifact: `10758079792`, digest `sha256:33a57ba225179ffae4037486217c4589cd0dcdf8b532c0bf45b29786150e55bf`

Observed gates:

- `uv lock --check`: PASS;
- clean `uv sync --locked --no-install-project --group test`: PASS;
- accepted Python surface compile: PASS;
- foundation regression from frozen environment: PASS;
- release workflow audit: PASS;
- movable third-party release Action refs: `0`;
- unnecessarily broad release token permissions: `0`;
- reusable cache step on pull request: SKIPPED by design;
- deterministic release build twice + byte comparison: PASS;
- SPDX/local provenance verifier: PASS;
- GitHub build provenance attestation: PASS;
- `gh attestation verify`: PASS.

Evidence digests:

- releasable source artifact: `d238dd414b6bd214e9dc4ee934595523c6eb7b94c4287641b6da02df5c7b3f66`;
- `uv.lock`: `cf1ecfeab5d4a6d01868db8ae45339e3cfc77f0e77d7ebb27a21dba6ef8036ea`;
- SPDX 2.3 SBOM: `1efa3b71c13520fcfd1941c32868e774629417dc210211c465b33ca998decc2a`;
- local provenance JSON: `494a657b8c58d37b96ad8be9f0cc6440f3689bfa855bd11c121464cccd7c9606`.

The local provenance subject digest equals the releasable artifact digest. SBOM package count is `6`; forbidden runtime packages observed: `[]`. `production_ready_claim` is `false`.

## Independent repository checks on measurement head

- `System Integrity` run `35878273746`: SUCCESS.
- `Foundation Regression` run `35878273843`: SUCCESS.

## Online/offline reproducibility boundary

- `ONLINE_INSTALL`: candidate provisioning and cold dependency acquisition may contact the configured package index. Locked CI may not rewrite the selected committed lock.
- `OFFLINE_VERIFY`: once artifact, SPDX SBOM, local provenance, lock and verifier code are present, digest/SBOM/provenance verification requires no dependency resolution or package-index access.
- not claimed: cold no-cache dependency installation with zero network access.

## Gate result

`PROMOTE: uv@0.12.18` for the current single-project Python graph, with Python `3.13.15`, committed `pyproject.toml` + `uv.lock`, locked CI, full-SHA release Actions, least privilege, trusted-lane-only reusable cache writes, deterministic artifact + SPDX 2.3 + digest-bound local/GitHub provenance.

This result does not authorize any production runtime/database/parser/frontend/deployment winner and does not authorize a blanket production-ready claim.
