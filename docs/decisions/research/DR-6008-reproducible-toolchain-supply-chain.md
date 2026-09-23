# DR-6008 — Reproducible toolchain and software supply-chain freeze

`TASK_ID: W006-T008`  
`ATTEMPT_ID: A02`  
`RESEARCH_DATE: 2026-09-23`  
`STATUS: LOCK / PROMOTE`  
`PREFERRED: uv@0.12.18`  
`CONFIDENCE: HIGH_FOR_CURRENT_GRAPH`

## 1. Decision question

For the current Academy Suno single-project Python repository graph, which dependency/package-manager baseline, repository topology, cache policy, release-workflow controls, SBOM format and provenance controls should be frozen so that a clean checkout can install, test, build and verify the same release inputs without silently closing unrelated production runtime/database/parser/frontend/deployment choices?

The material package-manager comparison is uv vs Poetry vs PDM. Repository topology/task-graph tooling is evaluated separately. The conclusion is scoped to the observed Python workload only.

## 2. Workload and constraints

Observed workload and hard constraints:

- one root Python project and no Node production manifest;
- Python `3.13.15` on GitHub-hosted `ubuntu-24.04`;
- exact committed lock and a fail-closed freshness check;
- clean locked install and foundation regression;
- release third-party Actions pinned to immutable full commit SHAs;
- least-privilege `GITHUB_TOKEN` permissions;
- cache key derived from lock/toolchain inputs, with no low-trust PR → trusted-main cache promotion;
- deterministic releasable artifact;
- machine-verifiable SPDX 2.3 SBOM;
- digest-bound local provenance plus GitHub build-provenance attestation and verification;
- production-ready claim remains unauthorized by this task.

A01 (`4d98952405a9c478dcf1c82aa47531ebbc4e7c1c`, PR #218) remains diagnostic only because its material package-manager lock lacked a complete DRG record. A02 preregistered criteria and protocol before running new measurements.

## 3. Alternatives

### Package/dependency manager candidates

1. **uv 0.12.18** — standards-based `pyproject.toml`, tool-specific `uv.lock`, exact locked sync/freshness workflow.
2. **Poetry 2.5.1** — project/dependency manager with committed `poetry.lock` and lock/install workflow.
3. **PDM 2.29.2** — project/dependency manager with committed `pdm.lock`; upstream also documents PEP 751 support, but A02 did not benchmark a pylock migration.

All three were installed at exact versions and exercised against the same seven direct dependencies.

### Repository/task-graph alternatives considered

- existing single repository with no extra task graph;
- add a Python-oriented task/build orchestration layer;
- migrate to a broader build/monorepo/environment system such as Bazel or Nix.

The current graph has one Python project and no measured multi-project/polyglot requirement. No representative A02 evidence justified a repository migration or extra task graph, so the topology decision is `NO_ADDITIONAL_TOOLING_FOR_CURRENT_GRAPH` rather than a permanent rejection of those systems.

### Other package/environment approaches considered but not measured as equivalent manager candidates

- pip-tools: compiler-style requirements workflow rather than an equivalent project manager for the selected one-manifest/one-lock path;
- PEP 751 `pylock.toml`: interoperability lock standard, not itself a resolver/package manager;
- Conda/Mamba: system/environment scope not represented by this workload;
- Nix: environment/system reproducibility scope materially exceeds this repository need;
- Bazel/rules_python: build graph/monorepo scope not represented by this repository;
- Rye: not used as a fresh independent candidate because current ecosystem direction has shifted toward uv.

## 4. Evaluation criteria preregistered before A02 interpretation

Protocol was committed in `b40e5fdf1840398f8557ec79c946ab504ad302f9` before PR-triggered measurement.

### Hard gates

A package-manager candidate is ineligible if any fails:

1. exact candidate version can be provisioned;
2. same declared dependency graph can be resolved;
3. first lock succeeds;
4. install/sync from generated lock succeeds;
5. required imports succeed;
6. warm sync succeeds;
7. repeat lock succeeds;
8. repeat lock preserves the exact lock digest;
9. CI-compatible lock freshness/locked-install contract exists;
10. adoption does not require unrelated repository/runtime choices.

A promoted selected baseline additionally must pass exact tool version verification, committed lock freshness check, clean locked install, compile/foundation regression, deterministic double-build, release Action immutability, least privilege, low-trust cache safety, SPDX verification, digest-bound local provenance and GitHub attestation verification.

No weighted score can compensate for a hard-gate failure.

### Base decision weights

| criterion | weight |
|---|---:|
| reproducibility / integrity | 0.40 |
| operational simplicity | 0.25 |
| measured execution efficiency | 0.20 |
| standards / portability posture | 0.10 |
| supply-chain fit | 0.05 |

### Sensitivity sets

- S1 reproducibility-heavy: `0.55 / 0.20 / 0.10 / 0.10 / 0.05`;
- S2 efficiency-heavy: `0.30 / 0.20 / 0.35 / 0.10 / 0.05`;
- S3 portability-heavy: `0.35 / 0.20 / 0.15 / 0.25 / 0.05`.

A unique `PROMOTE` requires the same eligible leader under base + S1 + S2 + S3 and no material source-evidence contradiction. Otherwise the result is `NO_PREFERENCE` or `PENDING_EVIDENCE`.

## 5. Systematic source search

Research date: `2026-09-23`.

Primary-source-first coverage:

1. current candidate package/release metadata for uv, Poetry and PDM;
2. official lock/sync/freshness semantics for compared tools;
3. Python lock interoperability standard (PEP 751);
4. GitHub Actions immutable pinning and least-privilege guidance;
5. GitHub dependency-cache trust/poisoning guidance;
6. GitHub artifact-attestation guidance;
7. SPDX 2.3 specification;
8. repository A01 diagnostic evidence and accepted T007 cache contract as local counterfactual/constraint evidence.

Stopping rule: evidence saturation is reached when all three measured candidates have current version + lock/freshness coverage, GitHub primary docs cover SHA pinning/least privilege/cache trust/attestation, SPDX primary specification covers the chosen SBOM version, and another search pass adds no material candidate or hard-gate requirement for the observed single-project Python workload. Broader systems requiring a materially different workload are documented as exclusions rather than compared with an unrepresentative microbenchmark.

Freshness rule: manager release evidence was checked on the research date. Re-run on material toolchain/version/workload change or within 30 days before a material production release decision based on this record.

## 6. Source table

| Source | Type/date checked | Authority / claim supported | Limitation |
|---|---|---|---|
| https://pypi.org/project/uv/0.12.18/ | PyPI primary package metadata, checked 2026-09-23 | uv 0.12.18 exists/current for this run | package metadata does not prove repository-specific performance |
| https://docs.astral.sh/uv/concepts/projects/sync/ | official uv docs, checked 2026-09-23 | lock freshness and locked/exact sync semantics | uv-specific |
| https://pypi.org/project/poetry/2.5.1/ | PyPI primary package metadata, checked 2026-09-23 | Poetry 2.5.1 exists/current for this run | package metadata does not prove repository-specific performance |
| https://python-poetry.org/docs/basic-usage/ | official Poetry docs, checked 2026-09-23 | lock/install workflow | Poetry-specific |
| https://pypi.org/pypi/pdm/json | PyPI primary metadata, checked 2026-09-23 | current PDM upstream package identity; exact 2.29.2 provision is independently verified by A02 run | broad JSON metadata; experiment supplies exact version proof |
| https://pdm-project.org/latest/usage/lockfile/ | official PDM docs, checked 2026-09-23 | committed lock, lock check/locked sync semantics and pylock support direction | PDM-specific; pylock migration not benchmarked |
| https://peps.python.org/pep-0751/ | Python standards, Final, checked 2026-09-23 | standard `pylock.toml` exists for reproducible installation inputs | does not itself select a resolver/manager |
| https://docs.github.com/en/code-security/tutorials/secure-your-organization/protect-against-threats | GitHub primary security docs, checked 2026-09-23 | least privilege and immutable full-SHA Action pinning | GitHub control-plane specific |
| https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository | GitHub primary docs, checked 2026-09-23 | repository policy can require full-length SHA pins | admin policy enforcement is outside this worker's scope |
| https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | GitHub primary docs, checked 2026-09-23 | cache keys/trust behavior; low-trust cache poisoning must be treated as a threat | cache bytes are not provenance even with correct keying |
| https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | GitHub primary docs, checked 2026-09-23 | OIDC-backed build provenance and verification | service availability/permissions are GitHub-specific |
| https://spdx.github.io/spdx-spec/v2.3/ | SPDX primary specification, checked 2026-09-23 | machine-readable SPDX 2.3 semantics | completeness depends on correct dependency traversal |
| `SYSTEM/RESULTS/W006-T008-A01.md` at historical A01 commit | repository diagnostic evidence, 2026-09-23 | counterfactual prior timing and implementation substrate | rejected for DRG incompleteness; cannot establish A02 decision |
| accepted W006-T007 cache contract | repository accepted evidence | trusted-lane-only reusable cache writes; no PR/worker → main promotion | constrains cache policy, not manager performance |

## 7. Primary-evidence-first coverage and saturation

Primary docs/specifications were used for version, lock semantics, Action security, cache trust, attestation and SPDX. A02 workflow artifacts provide the repository-specific empirical evidence. A01 was never treated as authoritative for the A02 package-manager decision.

Final saturation judgment: `SATURATED_FOR_CURRENT_SINGLE_PYTHON_PROJECT`. There is adequate primary-source coverage plus fresh representative execution for the observed workload. This does not imply saturation for polyglot monorepos, native/GPU/system dependency stacks or deployment-image reproducibility.

## 8. Experiment E1 — same-runner real-graph package-manager bakeoff

Canonical log: `experiments/w006_t008_toolchain/A02_EXPERIMENT_LOG.md`.  
Canonical synthesized dataset: `experiments/w006_t008_toolchain/a02-candidate-observation-dataset.json`.

Workflow run: `35878273774` — SUCCESS.  
Artifact: `10760260339`.  
Artifact digest: `sha256:837e99855b0063b3e7a419daab0be7cd9b1b3475f6157ec4a24a877e871ccd37`.

Observed environment:

- `ubuntu-24.04` GitHub-hosted runner;
- Linux `6.17.0-1022-azure`, glibc 2.39;
- Python `3.13.15`;
- identical direct graph: dbos 2.31.0, jsonschema 4.25.1, langgraph-checkpoint-sqlite 3.1.1, langgraph 1.2.12, pydantic 2.13.4, pypdf 5.9.0, pytest 9.0.2;
- three repeats per candidate.

Exact version probes:

- uv `0.12.18`;
- Poetry `2.5.1`;
- PDM `2.29.2`.

All candidates passed all package-manager hard gates and preserved byte-identical lock digests across all repeats.

Median results:

| candidate | first lock s | first sync s | warm sync s | efficiency composite s |
|---|---:|---:|---:|---:|
| uv | 0.0259 | 0.3592 | 0.0108 | 0.3959 |
| Poetry | 2.2657 | 2.2784 | 0.8149 | 5.3590 |
| PDM | 25.4147 | 13.1153 | 0.5609 | 39.0909 |

Raw per-repeat observations and lock digests are persisted in the canonical dataset and immutable workflow artifact.

### Uncertainty / limitations

- hosted-runner package/network caches cannot be perfectly controlled;
- uv's first repeat visibly included package downloads, hence medians rather than one cold result are used;
- candidate-specific ecosystem features outside this workload are not credited speculatively;
- the identical benchmark manifest contains `[tool.pdm] distribution = false` for PDM compatibility; it does not change dependencies for the other candidates;
- no deployment-image, system-package, native/GPU or polyglot graph was tested.

## 9. Matrix and sensitivity

After all candidates passed hard gates, A02 avoided inventing subjective numerical differences. Reproducibility/integrity, operational simplicity, standards/portability and supply-chain-fit scores are held neutral/equal at `1.0` because no representative candidate-specific A02 evidence distinguished the eligible candidates on those dimensions. Only measured execution efficiency differentiates them.

Efficiency composite = median first lock + median first sync + median warm sync. Lower-is-better min-max normalization across eligible candidates:

`(max_composite - candidate_composite) / (max_composite - min_composite)`

Efficiency score:

- uv `1.000000`;
- Poetry `0.871738`;
- PDM `0.000000`.

Final weighted results:

| weight set | uv | Poetry | PDM | leader |
|---|---:|---:|---:|---|
| base | 1.000000 | 0.974348 | 0.800000 | uv |
| S1 reproducibility-heavy | 1.000000 | 0.987174 | 0.900000 | uv |
| S2 efficiency-heavy | 1.000000 | 0.955108 | 0.650000 | uv |
| S3 portability-heavy | 1.000000 | 0.980761 | 0.850000 | uv |

Sensitivity: the same unique leader remains under all four preregistered weight sets.

## 10. Experiment E2 — selected-baseline supply-chain contract

Workflow run: `35878273770` — SUCCESS.  
Supply artifact: `10759372264`, digest `sha256:3f61f6b2bba7bff59e7ca4563397598a797cd7fbc188cd580e07e9c104ac8905`.  
Attestation verification artifact: `10758079792`, digest `sha256:33a57ba225179ffae4037486217c4589cd0dcdf8b532c0bf45b29786150e55bf`.

Observed:

- exact Python/uv check: PASS;
- `uv lock --check`: PASS;
- clean locked install: PASS;
- compile + foundation regression: PASS;
- release-path workflow audit: PASS;
- movable third-party release Action refs: `0`;
- unnecessarily broad release token permissions: `0`;
- pull-request reusable cache action: skipped, preserving the low-trust boundary;
- deterministic artifact built twice and compared byte-for-byte: PASS;
- SPDX 2.3 verifier: PASS;
- digest-bound local provenance verifier: PASS;
- GitHub build-provenance attestation: PASS;
- `gh attestation verify`: PASS.

Evidence digests:

- artifact: `d238dd414b6bd214e9dc4ee934595523c6eb7b94c4287641b6da02df5c7b3f66`;
- `uv.lock`: `cf1ecfeab5d4a6d01868db8ae45339e3cfc77f0e77d7ebb27a21dba6ef8036ea`;
- SPDX SBOM: `1efa3b71c13520fcfd1941c32868e774629417dc210211c465b33ca998decc2a`;
- local provenance JSON: `494a657b8c58d37b96ad8be9f0cc6440f3689bfa855bd11c121464cccd7c9606`.

The local provenance's artifact subject digest equals the actual artifact digest. The verifier observed SPDX package count `6`, forbidden runtime packages `[]`, and `production_ready_claim: false`.

Independent measurement-head checks:

- System Integrity run `35878273746`: SUCCESS;
- Foundation Regression run `35878273843`: SUCCESS.

## 11. Security / reliability / cost / operational burden / lock-in

### Security

- release third-party Actions are pinned to full commit SHAs;
- workflow defaults to `contents: read`, with `id-token: write` and `attestations: write` isolated to the attestation job;
- low-trust PR run does not execute the reusable cache action, eliminating a PR → trusted-main cache write/promotion path in this workflow;
- artifact provenance binds the subject digest, while cache contents are never treated as provenance;
- managers are bootstrapped at exact versions.

Residual risk: exact package versions and locks reduce drift but do not eliminate registry/upstream compromise. Future stronger package-source provenance/TUF/Sigstore controls require separate evidence.

### Reliability

- committed lock + freshness check prevents silent re-resolution in locked CI;
- byte-stable repeat locks were observed for all candidates;
- double-build comparison catches nondeterministic source-release construction for this artifact path;
- local verification survives GitHub attestation-service unavailability once evidence files are present;
- cold dependency installation still depends on package availability/network unless a complete trusted package cache/mirror exists.

### Cost

No paid third-party platform/tool is introduced. Direct costs are GitHub runner minutes/artifact storage already used by the repository. Organization billing data was unavailable, so no fabricated currency comparison is made.

### Operational burden

For the observed graph, adding a new monorepo/task/environment system would add surfaces without a measured need. The selected baseline keeps one root manifest, one committed dependency lock and one canonical sync path.

### Lock-in

All measured managers consume standards-based `pyproject.toml`, but their native lockfiles differ. PEP 751 provides a portability direction; A02 does not claim lockfile interchangeability. GitHub attestation is platform-specific, so local SPDX + digest-bound provenance verification is retained as a platform-independent evidence layer.

## 12. Online/offline reproducibility contract

`ONLINE_INSTALL`: provisioning managers and cold dependency acquisition may contact the configured package index. A locked CI run must not rewrite the committed selected lock.

`OFFLINE_VERIFY`: once the artifact, SPDX SBOM, local provenance, lock and verifier are present, artifact/SBOM/provenance/lock digest verification requires no resolver or package-index access.

Not claimed: cold, no-cache dependency installation with zero network access.

## 13. Decision

### Package manager

`PROMOTE / LOCK: uv 0.12.18` with Python `3.13.15`, root `pyproject.toml`, committed `uv.lock` and locked/frozen CI for the current single-project Python graph.

Justification:

- all three candidates passed correctness/reproducibility hard gates;
- uv is the unique leader under the base matrix and all three preregistered sensitivity sets using the only empirically differentiating dimension;
- the selected uv baseline separately passed the full clean-checkout supply-chain/release evidence contract;
- the conclusion does not depend on A01's rejected decision record.

### Repository topology / task graph

`NO_ADDITIONAL_TOOLING_FOR_CURRENT_GRAPH`: retain the existing single repository and do not add a Node/package/task graph absent representative need. This is reversible if the repository becomes multi-project/polyglot.

### Release/supply-chain controls

`LOCK` the following controls for this release path:

- full-SHA third-party Actions;
- least-privilege token permissions;
- lock/toolchain-derived trusted cache keys with no PR cache promotion;
- deterministic source artifact;
- SPDX 2.3 runtime SBOM;
- local digest-bound provenance;
- GitHub build-provenance attestation + verification where supported;
- local verifier retained independently of GitHub attestation.

### Explicit non-decisions

Remain open/unchanged:

- production runtime/workflow: `PENDING_EVIDENCE`;
- production database/shared-state: `PENDING_EVIDENCE`;
- parser/OCR: `NO_PRODUCTION_PARSER_WINNER`;
- frontend/editor: `PENDING_EVIDENCE`;
- identity/data/object vendors: unchanged/open;
- observability backend: unchanged/open;
- deployment class/cloud target: `PENDING_EVIDENCE`;
- blanket production readiness: `NOT_AUTHORIZED`.

## 14. Confidence

`HIGH_FOR_CURRENT_GRAPH` because:

- criteria and sensitivity sets were preregistered;
- three materially different current Python managers were measured on the same real dependency graph;
- all hard gates and three repeats were recorded;
- the leader is stable under all preregistered sensitivity sets;
- the selected implementation passed an independent supply-chain workflow including attestation verification;
- primary sources cover the security/specification controls.

Confidence is not generalized to workloads not measured here.

## 15. Rollout

1. freeze Python `3.13.15`, uv `0.12.18`, `pyproject.toml`, `uv.lock` and `toolchain.lock.json`;
2. use `uv lock --check` and `uv sync --locked --no-install-project --group test` in CI;
3. use full-SHA release Actions and fail closed on movable refs;
4. keep workflow-level least privilege and isolate OIDC/attestation grants;
5. allow reusable cache writes only on trusted lanes with lock-derived keys;
6. build deterministic source release, SPDX 2.3 SBOM and local provenance;
7. verify GitHub attestation where supported;
8. retain local artifact/SBOM/provenance verifier;
9. do not modify unrelated production technology choices.

## 16. Fallback / rollback

If uv later fails lock freshness, supported-Python, security or reproducibility gates:

- freeze dependency changes;
- retain the last verified lock/artifact/evidence bundle;
- re-run this DR with current releases and the same representative workload;
- if no unique candidate satisfies the gate, return to `NO_PREFERENCE`/`PENDING_EVIDENCE` rather than silently selecting a fallback;
- a pip/requirements-style fallback requires a new experiment proving equivalent lock/integrity behavior.

Supply-chain hardening (immutable Action pins, least privilege, cache trust, SBOM/provenance) is independent of package-manager rollback and should remain unless superseded by stronger evidence.

## 17. Revalidation triggers

Re-run/review on any of:

- Python minor baseline change;
- material uv lock/sync format/behavior change;
- >25% growth in direct dependency graph or addition of native/system/GPU dependencies;
- repository becomes multi-project/polyglot;
- PEP 751 becomes a production-ready default across relevant shortlisted tools;
- GitHub changes cache trust or attestation semantics;
- a new third-party release Action is added;
- deterministic double-build, SBOM/provenance verification or attestation verification fails;
- 30 days elapse before a material production release decision relies on this record.

## 18. Traceability

Primary implementation/evidence surfaces:

- `.python-version`;
- `pyproject.toml`;
- `uv.lock`;
- `toolchain.lock.json`;
- `experiments/w006_t008_toolchain/benchmark_real_graph.py`;
- `experiments/w006_t008_toolchain/A02_EXPERIMENT_LOG.md`;
- `experiments/w006_t008_toolchain/a02-candidate-observation-dataset.json`;
- `.github/workflows/w006-t008-toolchain-bakeoff.yml`;
- `.github/workflows/w006-t008-supply-chain.yml`;
- `.github/workflows/release-smoke-w004-t012.yml`;
- `scripts/supply_chain/audit_release_workflows.py`;
- `scripts/supply_chain/build_release_evidence.py`;
- `scripts/supply_chain/verify_release_evidence.py`;
- `artifacts/w006-t008/a02/manager-benchmark-summary.json`;
- `artifacts/w006-t008/a02/supply-chain-verification.json`.

Hard acceptance trace:

- complete applicable DRG record: this record;
- material lock without DRG: `0`;
- clean locked install/build/test: PASS;
- movable release Action refs: `0`;
- broad release token permissions: `0`;
- verifiable SBOM + provenance/attestation: PASS;
- repository migration without DRG: `0`;
- hard-gate compensation: `0`;
- production-ready claim: `NOT_AUTHORIZED`.

## 19. Adversarial review

1. **Cache/network ordering bias?** Yes, hosted-runner variance exists; medians were used and uv's first cold-ish repeat was preserved. The performance separation remains large.
2. **Different dependency graph?** No. The same seven direct dependencies were supplied to all candidates.
3. **Low-trust cache promotion?** No in this workflow: the reusable cache action is skipped for `pull_request`; trusted non-PR cache keys include OS, exact Python/uv and lock hash.
4. **Provenance binds exact artifact?** Yes. Local provenance artifact SHA equals the built artifact SHA; GitHub attestation verification passed.
5. **SBOM scope?** Runtime closure for the releasable artifact; test-only packages are not silently treated as runtime. Verifier observed six packages and no forbidden runtime package.
6. **Movable release Actions?** `0` after release-path audit.
7. **Hidden runtime/database/parser/frontend/deployment choice?** No; each remains explicitly open.
8. **Current source/version evidence?** Checked 2026-09-23 and exact provisioned versions independently recorded by the A02 run.
9. **Reasonable weight changes alter leader?** No across all preregistered sensitivity sets.
10. **Single canonical evidence surfaces?** Yes: DR-6008, one A02 experiment log and one A02 candidate-observation dataset.

## 20. Evidence saturation conclusion

`SATURATED_FOR_CURRENT_SINGLE_PYTHON_PROJECT`.

Primary-source categories are covered, all three viable shortlist candidates were freshly executed on the same representative graph, the selected baseline passed an independent release/supply-chain validation, and no further source-search iteration identified a material alternative or hard-gate requirement appropriate to this current workload. Revalidation triggers above bound the lifetime of this conclusion.
