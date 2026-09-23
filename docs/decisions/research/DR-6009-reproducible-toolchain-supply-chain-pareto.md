# DR-6009 — Reproducible toolchain and supply-chain decision under raw-metric Pareto

`TASK_ID: W006-T008`  
`ATTEMPT_ID: A03`  
`RESEARCH_DATE: 2026-09-23`  
`STATUS: LOCK`  
`PREFERRED: uv@0.12.18`  
`CONFIDENCE: HIGH_FOR_CURRENT_GRAPH`  
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`

## 1. Decision question and scope

For the current Academy Suno single-project Python repository graph, which dependency/package-manager baseline, if any, may be frozen so that a clean checkout can resolve/lock, install, import, warm-resync and reproduce its lock, while the selected baseline also passes clean locked build/test and release supply-chain controls?

The package-manager comparison is scoped to uv 0.12.18, Poetry 2.5.1 and PDM 2.29.2 on the same seven-dependency graph. Repository topology/task-graph tooling is a separate question. This record does not decide production runtime, database/shared state, parser/OCR, frontend/editor, identity/data/object vendors, observability backend, deployment class, production SLOs or overall production readiness.

## 2. Provenance / preregistration

Dispatch provenance: STATE 0054 / `869e94a8694c96ee460b8f27d9678623838fa61e`.

A03 observed canonical STATE 0055 / main `eb3513cbed16d759c053b3788ba07fd7d29d5f7c`, whose state transition records A02 as diagnostic/not accepted and opens A03 under the accepted Pareto methodology. `CONTINUITY_CHECK: PASS`.

Decision protocol was frozen before the binding A03 result inspection:

- DR preregistration commit: `bec4fd2d948d35f407647b89a0eb1cf1194dbd40`;
- machine-readable protocol commit: `bbd226d46e45e7bfce86e400f8c0956208202497`;
- protocol: `experiments/w006_t008_toolchain/a03-preregistered-pareto-protocol.json`.

A01/A02 remain diagnostic/counterfactual only. No A01/A02 numeric result establishes the A03 decision.

## 3. Alternatives

Package/dependency managers:

1. uv 0.12.18;
2. Poetry 2.5.1;
3. PDM 2.29.2.

Repository/task-graph alternatives considered separately:

1. preserve current single repository with no additional task graph;
2. add Python-oriented task/build orchestration;
3. migrate to a broader environment/monorepo system such as Bazel or Nix.

No representative current multi-project/polyglot requirement justifies migration, so repository topology remains `NO_MIGRATION_FOR_CURRENT_GRAPH`, with future recheck conditions rather than a permanent rejection of alternatives.

## 4. Predeclared decision surface

A03 follows accepted `W005-BENCHMARK-METHODOLOGY-V002`:

1. non-compensatory hard gates;
2. raw multidimensional objectives with units/direction;
3. explicit missingness/non-comparability;
4. repeat/range uncertainty where meaningful;
5. point Pareto among eligible candidates;
6. no scalar weights, weighted utility, composite score, min-max normalization for preference, synthetic neutral values, hard-gate compensation, invented practical-effect threshold or invented lexicographic priority;
7. `NO_PREFERENCE` / `PENDING_EVIDENCE` if a valid unique frontier cannot be established.

Package-manager hard gates required exact version provisioning, same graph resolution, first lock, install/sync, import verification, warm resync, second lock, byte-stable repeat lock, fail-closed lock freshness behavior and no unrelated technology choice.

For candidates passing every gate, the three predeclared lower-is-better objectives are:

- median `first_lock_seconds`;
- median `first_sync_seconds`;
- median `warm_sync_seconds`.

Each objective requires at least three successful comparable repeats. Missing required observations are never imputed.

Candidate A dominates B iff A is no worse on all three medians and strictly better on at least one. A scoped `LOCK` additionally requires selected-baseline supply-chain hard gates to pass.

## 5. Fresh A03 measurement

Binding workflow: `W006 T008 Toolchain Bakeoff`, run `35888663207` — `SUCCESS`.

- binding branch head: `bbd226d46e45e7bfce86e400f8c0956208202497`;
- PR merge ref exercised by Actions: `331eb513c5a27166b5dade81e5f8ccd049a4f3f7`;
- artifact: `10764356042`;
- artifact digest: `sha256:70e5e5de89b308a48f2e19d54650a6dcc5a484eca6be744cfc9b9d4425051b18`;
- `manager-benchmark.json` SHA-256: `4d390a2154364ae5ce108e42bc62b22a0a1767ccf4fa6f31801a279599a9b249`;
- runner: `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39`;
- Python: 3.13.15;
- same direct graph: dbos==2.31.0, jsonschema==4.25.1, langgraph-checkpoint-sqlite==3.1.1, langgraph==1.2.12, pydantic==2.13.4, pypdf==5.9.0, pytest==9.0.2.

All three candidates passed every measured hard gate and preserved byte-identical lock digests across all three repeats.

### Raw timing observations

| candidate | first lock repeats s | median | first sync repeats s | median | warm sync repeats s | median |
|---|---|---:|---|---:|---|---:|
| uv | 0.3539, 0.0207, 0.0203 | 0.0207 | 0.3195, 0.0383, 0.0392 | 0.0392 | 0.0096, 0.0098, 0.0093 | 0.0096 |
| Poetry | 3.3691, 2.3400, 2.2941 | 2.3400 | 3.0787, 2.4442, 2.4254 | 2.4442 | 0.8559, 0.8521, 0.8529 | 0.8529 |
| PDM | 30.2820, 29.1955, 29.1529 | 29.1955 | 14.5888, 14.0700, 14.1363 | 14.1363 | 0.5756, 0.5791, 0.5915 | 0.5791 |

Observed ranges expose hosted-runner/cache variability and are retained in `a03-candidate-observation-dataset.json`; no range is converted into a business-materiality threshold.

## 6. Point Pareto result

Median vectors `(first_lock, first_sync, warm_sync)`:

- uv: `(0.0207, 0.0392, 0.0096)` seconds;
- Poetry: `(2.3400, 2.4442, 0.8529)` seconds;
- PDM: `(29.1955, 14.1363, 0.5791)` seconds.

Under the preregistered lower-is-better point-Pareto rule:

- uv dominates Poetry on all three objectives;
- uv dominates PDM on all three objectives;
- `PARETO_FRONTIER = [uv]`.

No scalar aggregation or unsupported objective was needed. The unique non-dominated candidate criterion is satisfied.

## 7. Selected-baseline supply-chain hard gates

Fresh binding supply-chain workflow run `35888663048` — `SUCCESS`.

Immutable workflow artifacts:

- supply-chain artifact `10764027447`, digest `sha256:68b9c088272ccfb91cf9b697daa582e5236e6cd60195bf0e2758a0c59c90af79`;
- attestation verification artifact `10764306756`, digest `sha256:94eb54cd4a909b0820d1de26b4cc7c56129a8e1319ffe39dc3d814faca234cd3`.

Observed hard gates:

- exact Python 3.13.15 / uv 0.12.18 assertion: PASS;
- `uv lock --check`: PASS;
- clean locked install: PASS;
- compile + Foundation Regression: PASS;
- deterministic double-build byte comparison: PASS;
- movable third-party release Action refs: `0`;
- unnecessarily broad release token permissions: `0`;
- reusable cache write on pull request: skipped by design;
- SPDX 2.3 verification: PASS;
- digest-bound local provenance verification: PASS;
- GitHub build-provenance attestation: PASS;
- `gh attestation verify`: PASS.

Evidence digests:

- source artifact: `d238dd414b6bd214e9dc4ee934595523c6eb7b94c4287641b6da02df5c7b3f66`;
- `uv.lock`: `cf1ecfeab5d4a6d01868db8ae45339e3cfc77f0e77d7ebb27a21dba6ef8036ea`;
- SPDX SBOM: `1efa3b71c13520fcfd1941c32868e774629417dc210211c465b33ca998decc2a`;
- local provenance: `a6be4770a0ed2910d30fa7e99acf59c6be9e00f00f0402ada500d027b65279ca`.

The local provenance encodes `production_ready_claim: false`.

## 8. Research sources / saturation

Fresh primary-source-first review on 2026-09-23 covered:

| Source | Authority supported | Limitation |
|---|---|---|
| `https://pypi.org/project/uv/0.12.18/` | uv release identity | package metadata does not prove repository-specific behavior |
| `https://docs.astral.sh/uv/concepts/projects/sync/` | uv lock freshness / locked sync semantics | uv-specific |
| `https://pypi.org/project/poetry/2.5.1/` | Poetry release identity | metadata does not prove repository-specific behavior |
| `https://python-poetry.org/docs/basic-usage/` | Poetry lock/install semantics | Poetry-specific |
| `https://pdm-project.org/latest/dev/changelog/` | PDM 2.29.2 release identity | release notes do not prove benchmark behavior |
| `https://pdm-project.org/latest/usage/lockfile/` | PDM lock/freshness and pylock direction | PDM-specific |
| `https://peps.python.org/pep-0751/` | Final `pylock.toml` interoperability standard | standard does not choose a manager |
| GitHub Actions security/cache/attestation docs | immutable Action refs, least privilege, cache trust, provenance verification | GitHub-specific control plane |
| `https://spdx.github.io/spdx-spec/v2.3/` | SPDX 2.3 format semantics | completeness depends on traversal |
| `SYSTEM/RESULTS/W005-T009-A02.md` | accepted hard-gate/raw-metric/Pareto methodology | no task-specific tool winner |
| `SYSTEM/RESULTS/W006-T007-A01.md` | downstream evidence boundary | package manager intentionally pending there |

Search stopped after every candidate had current release/lock semantics coverage, Python lock interoperability direction was covered, GitHub release controls/attestation were covered, SPDX was covered, and another search pass added no materially different candidate or hard gate for the current single-project Python graph.

## 9. Security, reliability, cost, operational burden and lock-in

Security and reproducibility are non-compensatory hard gates. Timing cannot offset a failure.

No paid third-party platform is introduced by this package-manager choice. Organization-specific labor/billing evidence is unavailable, so A03 does not invent currency cost or convert seconds into money.

Candidate-specific operational burden has no validated common representative numeric unit in this attempt, so no synthetic/equal operational score is assigned.

All compared native lock formats remain manager-specific. PEP 751 is treated as an interoperability/recheck direction, not as proof that native locks are interchangeable today.

## 10. Decision

`LOCK: uv@0.12.18` for the **current single-project Python repository graph**.

The lock is supported by:

1. fresh A03 hard-gate eligibility for all candidates;
2. a unique raw-metric point-Pareto frontier `[uv]`;
3. fresh selected-baseline supply-chain hard gates all passing.

Repository topology: `NO_MIGRATION_FOR_CURRENT_GRAPH`. No Node package manager or additional task graph is introduced.

This is not a global claim that uv dominates every workload, nor a production-runtime/database/parser/frontend/deployment decision.

## 11. Reversal / recheck conditions

Reopen when any occurs:

- Python minor baseline changes;
- selected manager lock/sync semantics materially change;
- direct dependency graph grows materially or gains native/system/GPU dependencies;
- repository becomes multi-project/polyglot;
- PEP 751 becomes the stable/common default path across relevant candidates;
- GitHub cache or attestation trust semantics change;
- a new third-party release Action is added;
- deterministic build, SBOM, provenance or attestation verification fails;
- a material candidate-specific security/operational/portability trade-off appears that this workload did not measure;
- 30 days elapse before a material production release decision relies on this record.

## 12. Open boundaries

Production workflow/runtime, database/shared-state, frontend/editor, identity/data/object vendors, observability backend and deployment class remain evidence-gated. Parser/OCR remains `NO_PRODUCTION_PARSER_WINNER`. Scalar/business utility remains `PENDING_EVIDENCE`.

`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`.
