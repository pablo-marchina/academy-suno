# DR-6008 — Reproducible toolchain and software supply-chain freeze

`TASK_ID: W006-T008`
`ATTEMPT_ID: A02`
`RESEARCH_DATE: 2026-09-23`
`STATUS: EVALUATION_IN_PROGRESS`
`CONFIDENCE: PENDING_A02_MEASUREMENTS`

## 1. Decision question

For the current Academy Suno Python repository graph, which dependency/package-manager baseline, repository topology, cache policy, release workflow controls, SBOM format, and provenance controls should be frozen so a clean checkout can install, test, build and verify the same release inputs without silently closing unrelated production runtime/database/parser/frontend/deployment choices?

The material package-manager question is evaluated across at least three viable current candidates: uv, Poetry and PDM. Repository topology and task-graph tooling are evaluated separately; absence of evidence for extra topology/tooling is not converted into a hidden platform choice.

## 2. Workload and constraints

Observed repository workload at preregistration:

- Python-only production/test dependency graph declared from one root project;
- Python 3.13 line required by the current implementation substrate;
- CI on GitHub Actions / Ubuntu 24.04;
- exact lock freshness check and clean locked install required;
- foundation regression must execute from the selected frozen environment if a package-manager LOCK is justified;
- release-path third-party Actions must be immutable full commit SHA references;
- least-privilege `GITHUB_TOKEN` permissions;
- cache key material must derive from lock/toolchain inputs and low-trust PRs must not be able to seed reusable trusted caches;
- release artifact must have machine-verifiable SPDX 2.3 SBOM and digest-bound provenance/attestation;
- production-ready claim remains unauthorized by this task.

A01 (`4d98952405a9c478dcf1c82aa47531ebbc4e7c1c`, PR #218) is diagnostic only. Its outcome is not reused as the A02 decision. A02 re-runs representative experiments on its own head and stores new evidence.

## 3. Scope and non-goals

### In scope

- Python package/dependency manager and committed lock strategy;
- authoritative Python version for this repository baseline;
- single-repository vs extra task-graph tooling for the observed graph;
- GitHub Actions pinning and token permission policy on release paths;
- cache trust boundary;
- deterministic release evidence;
- SPDX SBOM generation/validation;
- local digest-bound provenance plus GitHub artifact attestation/verification;
- explicit online dependency-install vs offline verification contract.

### Out of scope / preserved open choices

No decision here selects a production workflow/runtime, database, parser/OCR winner, frontend framework/editor, identity provider, object-storage vendor, observability backend, cloud/deployment target, or multi-project topology not represented by the current repository. T007 authority remains binding for those boundaries.

## 4. Gate criteria declared before A02 result interpretation

### 4.1 Hard gates — package-manager candidate

A candidate is ineligible for scoring if any required gate fails in the same-runner experiment:

1. current installable candidate version is source-evidenced on the research date;
2. can resolve the identical declared dependency graph;
3. lock operation succeeds;
4. install/sync from the generated lock succeeds;
5. required imports execute from the installed environment;
6. warm re-sync succeeds;
7. repeated lock without input change succeeds and preserves lock digest;
8. candidate supports a committed lock/freshness-check workflow appropriate to CI;
9. no repository migration or unrelated production choice is required merely to adopt it.

### 4.2 Hard gates — selected baseline

If a package-manager `LOCK` is promoted, the selected baseline must also pass on the A02 head:

- exact Python/tool version verification;
- lock freshness check;
- clean locked install;
- compile/build/test/foundation regression required by the repository;
- deterministic release artifact built twice byte-identically;
- SPDX 2.3 SBOM produced and verified against the exact artifact/dependency lock;
- local provenance subject digest equals the built artifact digest and records lock digest;
- GitHub artifact attestation is created and `gh attestation verify` succeeds where repository permissions support it;
- release-path movable third-party Action references = 0;
- unnecessarily broad release-token permissions = 0;
- low-trust PR cache cannot write/promote a reusable trusted cache.

No weighted score can compensate for a failed hard gate.

### 4.3 Decision criteria after hard gates

For eligible package-manager candidates only, use these predeclared dimensions:

| Criterion | Weight | Measurement / evidence |
|---|---:|---|
| Reproducibility/integrity | 0.40 | lock stability, freshness-check semantics, exact sync/install, lock contents/hash behavior |
| Operational simplicity | 0.25 | number of moving repository/tooling surfaces and CI commands needed for the current graph |
| Measured execution efficiency | 0.20 | same-runner first lock + first sync and warm sync medians across repeats |
| Standards/portability posture | 0.10 | standards-based `pyproject.toml`, interoperability path, documented lock semantics |
| Supply-chain fit | 0.05 | compatibility with frozen CI, cache isolation, SBOM/provenance pipeline |

Scoring scale is 0–1 per dimension. Quantitative performance normalization uses observed eligible candidates only; qualitative dimensions must cite explicit evidence/observations. Weighted total is advisory after hard gates, not a substitute for them.

### 4.4 Sensitivity predeclaration

Run at least these alternate weight sets after collecting A02 data:

- S1 reproducibility-heavy: reproducibility 0.55, simplicity 0.20, efficiency 0.10, standards 0.10, supply-chain 0.05;
- S2 efficiency-heavy: reproducibility 0.30, simplicity 0.20, efficiency 0.35, standards 0.10, supply-chain 0.05;
- S3 portability-heavy: reproducibility 0.35, simplicity 0.20, efficiency 0.15, standards 0.25, supply-chain 0.05.

A unique `LOCK` requires the same eligible leader under the base matrix and all three sensitivity runs, plus no material source-evidence contradiction. Otherwise the package-manager result is `NO_PREFERENCE` or `PENDING_EVIDENCE`.

## 5. Systematic source-search strategy

Research date: 2026-09-23.

Primary-source-first categories and queries:

1. current candidate releases: PyPI project/release metadata for uv, Poetry and PDM;
2. lock/sync semantics: official uv, Poetry and PDM documentation;
3. interoperable Python lock standard: PEP 751 (`pylock.toml`);
4. GitHub Actions immutability and token hardening: GitHub security documentation;
5. cache poisoning / low-trust triggers: GitHub dependency-caching security documentation;
6. provenance and subject binding: GitHub artifact-attestation documentation;
7. SBOM format: SPDX 2.3 specification;
8. repository-specific prior evidence: A01 result/artifacts and accepted T007 cache contract, used as diagnostic inputs only.

Stopping rule: source search reaches saturation when (a) all three candidate versions and lock/freshness semantics have primary-source coverage, (b) GitHub primary docs cover SHA pinning, least privilege, cache trust and attestation, (c) SPDX primary specification covers the selected SBOM version, and (d) another search iteration adds no material candidate or hard-gate requirement for the observed single-project Python graph. Candidate ecosystem breadth that requires a different workload (for example Nix/Bazel/Conda multi-language/system-environment management) is recorded as excluded rather than silently scored against an unrepresentative microbenchmark.

Freshness rule: package-manager release evidence must be current on 2026-09-23; security/specification guidance is acceptable when currently published and not superseded. Re-run research on version/toolchain change or within 30 days before a material production release decision.

## 6. Source table

| Source | Type / date checked | Authority / supported claim | Limitation |
|---|---|---|---|
| uv 0.12.18 PyPI — https://pypi.org/project/uv/0.12.18/ | Package index primary metadata; checked 2026-09-23; release uploaded 2026-09-22 | uv 0.12.18 exists/current in the observed search and publishes platform artifacts via trusted publishing | Package metadata does not prove repository-specific performance |
| uv locking/sync docs — https://docs.astral.sh/uv/concepts/projects/sync/ | Official docs; checked 2026-09-23 | `uv lock --check`, `--locked`, exact sync semantics; new upstream versions do not silently make an existing lock stale | Tool-specific semantics |
| Poetry 2.5.1 PyPI — https://pypi.org/project/poetry/2.5.1/ | Package index primary metadata; checked 2026-09-23; release 2026-09-20 | Poetry 2.5.1 current in observed search; Python 3.13 supported | Does not prove repository-specific performance |
| PDM project metadata — https://pypi.org/pypi/pdm/json | Package index primary metadata; checked 2026-09-23 | Current PDM package metadata and upstream identity | JSON page is broad; experiment independently verifies exact provisioned version |
| PDM lock docs — https://pdm-project.org/latest/usage/lockfile/ | Official docs; checked 2026-09-23 | committed `pdm.lock`, `pdm lock --check`, locked sync semantics; optional PEP 751 pylock support | PDM-specific; pylock support maturity may evolve |
| PEP 751 — https://peps.python.org/pep-0751/ | Python standards track, Final; checked 2026-09-23 | standard `pylock.toml` format exists to support installation reproducibility without install-time resolution | Does not require this repository to migrate immediately; tool support differs |
| GitHub security hardening — https://docs.github.com/en/code-security/tutorials/secure-your-organization/protect-against-threats | Platform primary security docs; checked 2026-09-23 | declare least privilege; full commit SHA pins protect against movable-tag substitution | GitHub-specific control plane |
| GitHub Actions settings — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository | Platform primary docs; checked 2026-09-23 | repository policy can require full-length commit SHA pins | Administrative policy may not be available to this worker connection |
| GitHub dependency caching reference — https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | Platform primary security docs; checked 2026-09-23 | low-trust cache poisoning risk; trusted-trigger writes/read-only low-trust guidance | Cache contents remain untrusted even when keying is correct |
| GitHub artifact attestations — https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | Platform primary docs; checked 2026-09-23 | build provenance via OIDC-backed attestation; subject path/digest binding and verification | Availability/permissions depend on repository plan/visibility and token grants |
| SPDX 2.3 — https://spdx.github.io/spdx-spec/v2.3/ | SPDX primary specification; checked 2026-09-23 | machine-readable SPDX 2.3 document semantics | SBOM completeness still depends on correct dependency traversal |
| A01 diagnostic RESULT / PR #218 | Repository evidence, 2026-09-23 | provides counterfactual timings and implementation substrate to rerun, not an accepted decision | Rejected for incomplete DRG; cannot establish A02 outcome |
| W006-T007 accepted cache contract | Repository accepted evidence | trusted-lane-only reusable cache writes; no worker/PR fallback/promotion | Applies to repository cache policy, not package-manager performance |

## 7. Coverage and candidate universe

### Included in measured package-manager shortlist

- uv 0.12.18;
- Poetry 2.5.1;
- PDM 2.29.2, subject to A02 provisioning confirming the exact version is still installable/current enough for the run.

These are materially different current Python dependency-management implementations, all capable of consuming a Python project graph and producing a lock/install flow. Three candidates satisfy the DRG minimum where alternatives are available.

### Considered but excluded from this benchmark

- pip-tools: compiler-style requirements workflow rather than an equivalent project manager for this repository's desired one-command lock/sync baseline; remains a viable fallback pattern if project-manager assumptions reverse;
- PEP 751-native `pylock.toml`: interoperability format, not itself a resolver/package manager; evaluated as portability direction rather than a fourth manager;
- Conda/Mamba: environment/system-package scope not represented by current workload;
- Nix: full environment/system reproducibility scope materially exceeds the observed repository need;
- Bazel/rules_python: build graph/monorepo system not justified by current single Python project;
- Rye: not selected as a fresh candidate because current ecosystem direction has shifted to uv and a current maintained independent baseline is required.

Coverage judgment at preregistration: `ADEQUATE_FOR_CURRENT_SINGLE_PYTHON_PROJECT`, conditional on A02 experiment completion. This does not claim coverage for polyglot monorepos, GPU/system dependency stacks or deployment-image reproducibility.

## 8. Experiment protocol — preregistered

Canonical experiment log: `experiments/w006_t008_toolchain/A02_EXPERIMENT_LOG.md`.
Canonical synthesized candidate/observation dataset: `experiments/w006_t008_toolchain/a02-candidate-observation-dataset.json`.
Raw A02 workflow artifacts are immutable GitHub Actions artifacts referenced by run/artifact ID/digest and summarized under `artifacts/w006-t008/a02/` after execution.

### Experiment E1 — same-runner real-graph package-manager bakeoff

Environment: GitHub-hosted `ubuntu-24.04`, authoritative Python 3.13.15. Provision exact candidate versions in isolated venvs. Feed each candidate the same direct dependency set extracted from the A02 root manifest. Run three repeats unless infrastructure failure prevents it.

Per repeat collect: first lock duration/exit, first sync duration/exit, import verification, warm sync duration/exit, second lock duration/exit, first/second lock SHA-256 and equality. Preserve candidate lock files for the first repeat. No candidate receives a different dependency graph.

### Experiment E2 — selected-baseline supply-chain/reproducibility contract

Only if E1 leaves an eligible candidate suitable for a provisional selection, execute from clean checkout:

1. exact Python/package-manager version assertion;
2. lock freshness check;
3. clean locked install;
4. compile/foundation regression;
5. static release workflow audit for movable third-party Actions and token permissions;
6. deterministic release evidence build twice and byte comparison;
7. artifact/SBOM/provenance verifier;
8. capture artifact and lock digests;
9. GitHub build provenance attestation and `gh attestation verify` when allowed;
10. upload evidence with immutable workflow run/artifact identity.

### Online/offline contract

`ONLINE_INSTALL`: provisioning candidate managers and installing missing dependencies may contact the configured package index. Resolution is not allowed to rewrite the selected committed lock when `--locked`/freshness checking is in force.

`OFFLINE_VERIFY`: once artifact, SPDX SBOM, provenance statement, lock and verifier code are present, digest/SBOM/provenance verification must not require dependency resolution or package-index access. A completely cold dependency installation with no local package cache is explicitly **not** claimed offline-capable by this decision.

## 9. Security, reliability, cost, operational burden and lock-in

### Security

- Full-SHA Action pins are mandatory on the release path because mutable tags can move.
- Workflow-level default permission is `contents: read`; OIDC/attestation write permissions are isolated to the attestation job.
- Low-trust PRs do not save/promote reusable trusted caches; restored cache bytes are never treated as provenance.
- Release provenance binds the artifact subject digest; SBOM and lock digest are verification inputs, not trust substitutes for the artifact digest.
- Candidate managers are bootstrapped at exact versions. This does not eliminate upstream registry compromise risk; index provenance/hashes and future Sigstore/TUF-style controls remain separate layers.

### Reliability

- committed lock + freshness check prevents silent dependency re-resolution in locked CI;
- deterministic artifact double-build detects nondeterministic repository packaging inputs for the tested source bundle;
- attestation verification provides independent workflow/repository identity evidence when GitHub attestation service is available;
- package-index outage still affects cold online install; build verification of already-produced evidence remains possible offline.

### Cost

No paid third-party tool is introduced by this baseline. GitHub-hosted runner minutes/artifact storage are the direct CI costs; no reliable monetary comparison is possible without organization billing data, so cost is treated as operational surface rather than invented currency values.

### Operational burden

Prefer the smallest tool surface that meets all hard gates for the current graph. Adding a monorepo/task graph, separate environment manager, or new service requires new evidence rather than convenience-driven adoption.

### Lock-in

All candidates use `pyproject.toml`; lock formats differ. PEP 751 provides an interoperability direction, but the repository must not claim lockfile interchangeability that was not tested. GitHub attestation is platform-specific; the local SPDX + digest-bound provenance verifier is retained as a platform-independent evidence layer.

## 10. A01 and T007 diagnostic/counterfactual use

A01 recorded successful diagnostic same-runner measurements and supply-chain evidence, but its package-manager `LOCK` is explicitly not accepted. A02 uses those values only to:

- verify the new experiment exercises at least the same correctness dimensions;
- identify regression/outlier conditions;
- confirm that the implementation substrate is reproducible enough to rerun.

A02 must produce a distinct workflow run on an A02 commit. A large timing difference from A01 is treated as environment noise/drift to explain, not a reason to copy A01 medians.

T007's accepted cache invariant is a hard compatibility constraint: trusted lanes may populate reusable caches; worker/PR lanes do not create a worker→main cache promotion path.

## 11. Decision matrix and sensitivity

`PENDING_A02_MEASUREMENTS`.

The base and S1/S2/S3 weights are fixed in §4 before experiment execution. Candidate hard-gate status, normalized measurements, per-criterion rationale and totals will be filled from the A02 synthesized dataset after the workflow completes.

## 12. Decision / no-preference rule

Current preregistration state: `PENDING_EVIDENCE`.

Allowed terminal gate values:

- `PROMOTE`: one unique candidate passes all hard gates and remains the unique leader under base + S1 + S2 + S3, with no source-evidence contradiction;
- `NO_PREFERENCE`: two or more eligible candidates remain materially tied/unstable under sensitivity;
- `PENDING_EVIDENCE`: experiment/source freshness is insufficient or a required hard gate cannot be exercised.

No fallback winner is inferred from A01.

## 13. Implementation / rollout plan if PROMOTE

1. commit authoritative Python version, manager version, root manifest and lock;
2. run locked CI without implicit lock mutation;
3. full-SHA-pin release Actions and fail closed on movable refs;
4. enforce least privilege at workflow/job level;
5. use lock-derived trusted cache keys and no low-trust cache promotion;
6. produce deterministic source artifact + SPDX 2.3 SBOM + digest-bound provenance;
7. verify GitHub attestation where enabled;
8. retain local verifier so artifact/SBOM/provenance can be checked without network resolution;
9. do not alter unrelated production choices.

## 14. Fallback / rollback

If the promoted package manager later fails lock freshness, platform support, security or reproducibility gates:

- freeze dependency changes;
- retain the last verified artifact/lock/evidence bundle;
- rerun this DR with current candidate releases and the same workload;
- if no candidate qualifies, revert the manager default to `NO_PREFERENCE/PENDING_EVIDENCE` rather than silently switching;
- a pip/requirements-style fallback is permitted only with a new lock/integrity experiment proving equivalent reproducibility.

Rollback of workflow hardening is not part of package-manager rollback: full-SHA pinning, least privilege, cache trust boundaries, SBOM and provenance remain independent supply-chain controls unless separately superseded by stronger evidence.

## 15. Revalidation triggers

Re-run/review when any occurs:

- Python minor baseline changes;
- selected manager major/minor behavior or lock format changes materially;
- direct dependency graph grows by >25% or adds native/system/GPU dependencies;
- repository becomes multi-project/polyglot;
- PEP 751 support becomes the production-ready default across shortlisted tools;
- GitHub changes cache trust or attestation semantics;
- release workflow adds a new third-party Action;
- deterministic double-build, SBOM/provenance verification, or attestation verification fails;
- 30 days elapse before a material production release decision based on this DR.

## 16. Traceability

Affected artifacts/controls:

- `pyproject.toml`, `uv.lock`, `.python-version`, `toolchain.lock.json` if uv is ultimately promoted;
- `.github/workflows/w006-t008-toolchain-bakeoff.yml`;
- `.github/workflows/w006-t008-supply-chain.yml`;
- `.github/workflows/release-smoke-w004-t012.yml`;
- `scripts/supply_chain/audit_release_workflows.py`;
- `scripts/supply_chain/build_release_evidence.py`;
- `scripts/supply_chain/verify_release_evidence.py`;
- A02 experiment log, synthesized dataset and raw workflow artifacts;
- W006 hard acceptance: clean locked install/build/test, immutable release Actions, least privilege, cache safety, SBOM/provenance and no unauthorized production-ready claim.

## 17. Adversarial review / postmortem prompts

Before terminalizing A02, explicitly answer:

1. Did a candidate appear faster only because of cache/network ordering?
2. Did the experiment give any candidate a different graph or install semantics?
3. Can a fork/low-trust PR write or promote bytes later trusted by main?
4. Does provenance verify the exact artifact digest, or merely name a path?
5. Does the SBOM describe the releasable artifact/runtime dependency closure rather than test-only noise?
6. Did any third-party Action remain tag/branch pinned?
7. Did a package-manager choice smuggle in runtime/database/parser/frontend/deployment decisions?
8. Are all source-version claims still current as of the A02 run?
9. Could the same data support a different leader under reasonable predeclared weights?
10. Is there exactly one canonical DR record, experiment log and synthesized candidate dataset for this A02 question?

## 18. Evidence saturation status

At preregistration, source coverage is `SATURATED_FOR_PROTOCOL_DESIGN` but decision coverage is `PENDING_A02_EXECUTION`. All required primary-source categories are represented and three viable candidates are defined; the stopping rule is not fully satisfied until A02 empirical artifacts and adversarial review are recorded.
