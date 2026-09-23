# DR-6009 — Reproducible toolchain and supply-chain decision under raw-metric Pareto

`TASK_ID: W006-T008`  
`ATTEMPT_ID: A03`  
`RESEARCH_DATE: 2026-09-23`  
`PROTOCOL_STATE: PREREGISTERED_BEFORE_A03_RESULT_INSPECTION`  
`DECISION_STATE: PENDING_EVIDENCE`  
`CONFIDENCE: PENDING_A03_OBSERVATIONS`  
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`

## 1. Exact decision question

For the current Academy Suno single-project Python repository graph, which dependency/package-manager baseline, if any, may be frozen so that a clean checkout can resolve/lock, install, import, warm-resync and reproduce its lock, while a selected baseline also passes clean locked build/test and the repository's release supply-chain controls? Separately, should the repository topology gain another task graph/build system?

The package-manager comparison is scoped to uv 0.12.18, Poetry 2.5.1 and PDM 2.29.2 on the same declared dependency graph. A03 does not decide production runtime, database/shared state, parser/OCR, frontend/editor, identity/data/object vendors, observability backend, deployment class, production SLOs or production readiness.

## 2. Provenance and continuity

Dispatch provenance is STATE 0054 / `869e94a8694c96ee460b8f27d9678623838fa61e`. A03 observed canonical STATE 0055 / main `eb3513cbed16d759c053b3788ba07fd7d29d5f7c`; that commit records A02 as diagnostic/not accepted and opens A03 under the accepted Pareto methodology. `CONTINUITY_CHECK: PASS`.

A01 and A02 are immutable diagnostic/counterfactual attempts. A03 reuses only harness/source-search structure and must bind any decision to fresh A03 observations.

## 3. Workload and constraints

Observed repository workload before A03 result inspection:

- one root Python project; no representative multi-project/polyglot requirement;
- Python 3.13 line on GitHub-hosted Ubuntu 24.04 for the comparison;
- same direct dependency graph for every candidate;
- committed lock and fail-closed freshness behavior required for a promoted baseline;
- clean install/sync plus required import verification;
- at least three repeats when timing variability is used;
- lock byte stability across repeat locking;
- selected-baseline clean locked build/test plus Foundation Regression;
- release-path third-party Actions pinned to full commit SHA;
- least-privilege release token permissions;
- low-trust pull requests must not publish reusable trusted caches;
- deterministic releasable artifact;
- machine-verifiable SPDX SBOM;
- digest-bound local provenance plus GitHub build-provenance attestation and verification;
- no repository migration without a separate evidence-bearing decision;
- production-ready claim remains unauthorized.

## 4. Alternatives

### Package/dependency-manager candidates

1. **uv 0.12.18** — project manager using `pyproject.toml` and uv-managed lock/sync semantics.
2. **Poetry 2.5.1** — project/dependency manager with Poetry lock/install semantics.
3. **PDM 2.29.2** — project/dependency manager with PDM lock/install semantics and a documented PEP 751 direction.

These are materially different implementations while serving the same current Python project graph.

### Repository/task-graph alternatives

1. preserve the existing single repository without an additional task graph;
2. add Python-oriented task/build orchestration;
3. migrate to a broader monorepo/environment system such as Bazel or Nix.

The current workload contains no representative multi-project/polyglot requirement. A03 therefore treats repository migration as a separate evidence question and will not infer a migration winner from package-manager timings.

## 5. Mandatory decision surface — frozen before A03 outcomes

A03 follows accepted `W005-BENCHMARK-METHODOLOGY-V002`:

1. non-compensatory hard gates;
2. raw multidimensional objectives with units and direction;
3. explicit missingness/non-comparability;
4. uncertainty/repeats where meaningful;
5. point Pareto among eligible candidates;
6. no scalar weights, weighted utility, synthetic composite score, synthetic neutral values, invented practical-effect threshold or invented lexicographic priority;
7. if the required objective set is not fully valid/comparable, or eligible candidates remain in a trade-off frontier, return `NO_PREFERENCE` / `PENDING_EVIDENCE` rather than manufacturing a winner.

### 5.1 Package-manager hard gates

A candidate is ineligible if any applicable gate fails:

1. exact candidate version can be provisioned;
2. identical declared dependency graph can be resolved;
3. first lock succeeds;
4. install/sync from the generated lock succeeds;
5. required imports succeed;
6. warm resync succeeds;
7. repeat lock succeeds;
8. repeat lock preserves byte-identical lock digest within that candidate;
9. lock freshness / locked-install behavior is compatible with fail-closed CI;
10. adoption does not require an unrelated production/runtime/repository choice.

No timing advantage can compensate for any hard-gate failure.

### 5.2 Predeclared raw comparable objectives

For candidates that pass every package-manager hard gate, the A03 point used for Pareto comparison is the vector of **three separately retained raw wall-clock metrics**, all lower-is-better:

- `first_lock_seconds` — median across at least 3 repeats;
- `first_sync_seconds` — median across at least 3 repeats;
- `warm_sync_seconds` — median across at least 3 repeats.

Raw per-repeat values remain canonical evidence; medians define the point comparison because hosted-runner/network/cache noise makes a single observation unrepresentative. No sum, normalization, score, weight or utility is permitted for the decision.

These three objectives are predeclared because they are directly observed under the same runner and same repository graph. Reproducibility/integrity, install/import correctness and lock stability are hard gates rather than compensable objectives. Supply-chain controls are post-selection hard gates. Candidate-specific portability/lock-in or business-operational burden without a common representative raw unit is **not assigned a synthetic number**.

### 5.3 Missingness policy

A required Pareto objective is valid only when the candidate has at least three successful comparable repeats for that metric under the same A03 protocol. Missing/failed required observations are recorded as missing/failure, never as a neutral value. If a candidate remains hard-gate eligible but a required objective is not valid/comparable, the package-manager preference is `PENDING_EVIDENCE` because the required Pareto comparison is not computable.

### 5.4 Uncertainty policy

For each timing objective persist all repeats, median, minimum, maximum and range. With only three repeats, no claim of population-level performance precision is authorized. Point Pareto uses the preregistered medians only; ranges are reported to expose runner variability and are not converted into an invented practical-effect threshold.

### 5.5 Point-Pareto rule

Candidate A dominates B iff A is no worse than B on all three valid median timing objectives and strictly better on at least one. A scoped `LOCK` is eligible only if:

- all compared candidates have valid required objective vectors;
- exactly one eligible candidate is non-dominated; and
- no sourced material contradiction or selected-baseline supply-chain hard-gate failure remains.

If the frontier contains multiple candidates, the decision is `NO_PREFERENCE`. If required evidence is missing/non-comparable, the decision is `PENDING_EVIDENCE`.

## 6. Selected-baseline supply-chain hard gates

If the package-manager Pareto rule yields one eligible non-dominated candidate, that candidate is not frozen until a clean-checkout A03 supply-chain run passes all of:

- exact Python/manager version assertion;
- committed-lock freshness check;
- clean locked install;
- compile/build and Foundation Regression;
- deterministic double-build byte comparison;
- movable third-party release Action refs = 0;
- unnecessarily broad release token permissions = 0;
- low-trust PR reusable-cache write/promotion absent;
- machine-verifiable SPDX 2.3 SBOM PASS;
- digest-bound local provenance verification PASS;
- GitHub build-provenance attestation generation and `gh attestation verify` PASS.

A failure here converts the scoped package-manager lock to `PENDING_EVIDENCE`/blocked rather than being compensated by benchmark speed.

## 7. Systematic primary-source-first search

Research date: 2026-09-23. A03 performed a fresh primary-source-first review before inspecting A03 measurement outcomes.

Search coverage:

1. current package/release identity for uv, Poetry and PDM;
2. official lock/freshness/install semantics for the candidates;
3. PEP 751 interoperability direction;
4. GitHub Actions immutability, least privilege, cache trust and artifact-attestation controls;
5. SPDX 2.3 specification;
6. accepted repository methodology/authority from W005-T009-A02 and W006-T007-A01;
7. A01/A02 only as diagnostic/counterfactual prior evidence.

Freshness rule: recheck upstream tool/version/control semantics on material toolchain/workload change and within 30 days before any material production release decision relies on this record.

Stopping rule: source review is saturated for this decision when all three candidates have current release/lock semantics coverage, Python interoperability direction is covered, GitHub primary documentation covers release-path controls/attestation, SPDX defines the SBOM format, and another search pass adds no materially different candidate or hard gate for the current single-project Python workload. Broader systems requiring a different workload are recorded as recheck triggers, not benchmarked on an unrepresentative slice.

## 8. Source table

| Source | Authority / claim supported | Limitation |
|---|---|---|
| `https://pypi.org/project/uv/0.12.18/` | primary package metadata; uv 0.12.18 release identity checked 2026-09-23 | package metadata does not prove repo-specific behavior |
| `https://docs.astral.sh/uv/concepts/projects/sync/` | official uv lock freshness, `--locked`, `uv lock --check`, exact sync semantics | uv-specific |
| `https://pypi.org/project/poetry/2.5.1/` | primary package metadata; Poetry 2.5.1 release identity checked 2026-09-23 | metadata does not prove repo-specific behavior |
| `https://python-poetry.org/docs/basic-usage/` | official Poetry project/lock/install semantics | Poetry-specific |
| `https://pdm-project.org/latest/dev/changelog/` | official PDM changelog; release 2.29.2 dated 2026-09-17 | release notes do not prove benchmark behavior |
| `https://pdm-project.org/latest/usage/lockfile/` | official PDM committed lock, freshness check and pylock direction | PDM-specific; interoperability remains tool/version dependent |
| `https://peps.python.org/pep-0751/` | Python standard: `pylock.toml` reproducible-installation format is Final | standard does not itself select a resolver/manager |
| `https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations` | GitHub artifact attestation permissions/provenance flow | GitHub control-plane specific |
| GitHub Actions security/repository policy docs | immutable full-SHA Action pinning and least privilege | repository-admin enforcement is outside worker scope |
| GitHub Actions dependency-caching docs | cache keys/trust behavior | cache bytes are not provenance |
| `https://spdx.github.io/spdx-spec/v2.3/` | SPDX 2.3 machine-readable SBOM specification | completeness depends on correct dependency traversal |
| `SYSTEM/RESULTS/W005-T009-A02.md` | accepted hard-gate -> raw metrics -> uncertainty -> point-Pareto methodology | no task-specific toolchain winner |
| `SYSTEM/RESULTS/W006-T007-A01.md` | accepted downstream authority and open technology boundaries | toolchain/package manager intentionally left pending |
| A01/A02 T008 artifacts | diagnostic harness/counterfactual evidence only | cannot establish A03 decision |

## 9. Security, reliability, cost, operational burden and lock-in treatment

### Security / supply chain

Security is non-compensatory. Release Action immutability, token least privilege, cache trust separation, SBOM verification and provenance/attestation are hard gates on the selected baseline. A faster manager does not offset a failure.

### Reliability / reproducibility

Resolution/lock/install/import/warm-resync/repeat-lock stability are hard gates. Selected-baseline clean locked install, regression and deterministic release build are additional hard gates.

### Cost

No paid third-party platform is introduced by the candidate comparison itself. Organization-specific labor/billing data is unavailable; A03 will not invent currency cost or convert timing to money without representative business evidence. Timing stays in seconds.

### Operational burden

Candidate-specific operational burden has no validated common representative numeric unit in this attempt. A03 therefore does not assign equal/neutral scores. The decision scope is deliberately narrow: current repository graph + measured lock/install/resync mechanics + hard-gate supply-chain contract. Material operational complexity encountered during the fresh run is recorded as evidence/limitation and can invalidate promotion if it breaks a hard gate.

### Lock-in / portability

All candidate-native lockfiles are manager-specific. PEP 751 is a standards direction and a recheck trigger, not evidence that native locks are interchangeable today. No synthetic portability score is used. A repository migration or multi-project toolchain choice remains separate and evidence-gated.

## 10. Repository topology decision protocol

A03 does not use package-manager speed to choose a repository topology. For the current one-project Python graph, preserve the existing repository/task-graph shape unless fresh representative evidence demonstrates a concrete unmet requirement that an added orchestration/migration solves and a DRG-compliant comparison supports that material change. Otherwise the topology state is `NO_MIGRATION / PENDING_FUTURE_EVIDENCE`, scoped to the current graph rather than a permanent technology rejection.

## 11. Traceability and open boundaries

Traceability: PROD-015, PROD-016; RISK-0034, RISK-0040; accepted W005-T009-A02; accepted W006-T007-A01.

Preserved boundaries:

- production workflow/runtime: `PENDING_EVIDENCE`;
- production database/shared-state: `PENDING_EVIDENCE`;
- parser/OCR: `NO_PRODUCTION_PARSER_WINNER`;
- frontend/editor: open;
- identity/data/object vendors: open;
- observability backend: open;
- deployment class/cloud target: open;
- scalar/business utility: `PENDING_EVIDENCE`;
- production-ready claim: `NOT_AUTHORIZED`.

## 12. Reversal / recheck conditions

Reopen this scoped toolchain decision when any occurs:

- Python minor baseline changes;
- selected manager lock/sync semantics materially change;
- direct dependency graph grows materially or gains native/system/GPU dependencies;
- repository becomes multi-project/polyglot;
- PEP 751 becomes the stable default/common interchange path across relevant shortlisted tools;
- GitHub cache or attestation trust semantics change;
- a new third-party release Action is added;
- deterministic build, SBOM, provenance or attestation verification fails;
- a candidate-specific material operational/security/portability trade-off appears that this current workload did not measure;
- 30 days elapse before a material production release decision relies on this record.

## 13. Pre-outcome decision status

`PENDING_EVIDENCE`.

No candidate preference has been recorded in this preregistration. Final status may be `LOCK`, `NO_PREFERENCE` or `PENDING_EVIDENCE` only after fresh A03 raw observations and selected-baseline supply-chain evidence are persisted and evaluated exactly under Sections 5-6.
