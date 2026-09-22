# W005-T013 — Production developer platform / toolchain decision research

Research date: 2026-09-22
Task: `W005-T013`
Attempt: `A01`

This record follows `SYSTEM/DECISION_RESEARCH_GATE.md`. It deliberately separates decisions that can be locked from choices that depend on the unresolved production frontend/API and runtime research in W005-T002/W005-T003.

## Baseline evidence

The W004-era repository is Python-first and GitHub-hosted. The current branch contains 16 workflow YAML files under `.github/workflows/`. At repository root there is no `pyproject.toml`, no standard Python lock file (`uv.lock`, `poetry.lock`, `pdm.lock`, `pylock.toml`), and no Node workspace manifest/lock file. `foundation-tests.yml` installs `pydantic` and `pytest` directly with `python -m pip install` and references `actions/checkout@v4` and `actions/setup-python@v5` through movable major-version tags.

Migration-cost floor from that baseline:

- Python reproducibility requires at least one project manifest plus one committed lock file and a CI install-path change.
- Every one of the 16 workflow files is a review touch point for action pinning/permissions/cache policy, although reusable workflows can reduce the final number of duplicated edits.
- JavaScript package/workspace migration cost is currently zero because no production Node package topology exists yet; choosing one before W005-T002 resolves the frontend/API boundary would create avoidable churn.
- There is no existing build graph/orchestrator configuration to migrate.

The executable inventory and package-manager benchmark harness is in `experiments/w005_toolchain/benchmark_toolchain.py`.

---

## DR-W005-T013-01 — CI orchestration platform

**Domain:** CI platform

**Candidate decision:** Keep GitHub Actions as the production CI orchestration platform for this repository.

**Status:** `LOCK`

### Why decision matters

CI is already the main execution surface for validation, demo capture, provider checks, release smoke, and system-integrity workflows. Migrating CI would create immediate operational work without removing an evidenced blocker.

### Sources consulted

Primary:
- GitHub Actions reusable workflows: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
- GitHub dependency caching: https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching
- GitHub secure-use guidance: https://docs.github.com/en/actions/reference/security/secure-use

Repository evidence:
- `.github/workflows/foundation-tests.yml`
- the 16 current workflow definitions under `.github/workflows/`

### Alternatives considered

1. GitHub Actions — native to the current repository; current implementation already depends on it.
2. Buildkite — credible hosted/self-hosted execution model, but introduces a second control plane and migration with no current requirement for dedicated agents.
3. CircleCI — mature caching/orchestration, but duplicates repository integration and requires migration of existing workflows.

### Evidence summary

GitHub Actions already satisfies repository-triggered CI, reusable workflow composition, dependency caching, OIDC-based identity, and artifact-attestation integration. The current problems are configuration quality (dependency reproducibility, pinning, duplication, permissions), not a demonstrated limitation of the CI platform.

### Compatibility with repo/architecture

Highest compatibility: zero platform migration and preserves all W004 workflow entry points.

### Operational burden

Lower than alternatives because repository, auth boundary, workflow history, and existing automation stay in one platform.

### Migration / rollback

Migration: none for platform choice. Hardening changes are incremental per workflow. Rollback is per commit/workflow.

### Benchmark / POC needed

No platform bakeoff is required before implementation. Cache/reusable-workflow changes must still be measured with the benchmark plan in `experiments/w005_toolchain/README.md`.

### Decision

Keep GitHub Actions for W005 production implementation. Revisit only if an evidenced requirement cannot be met by GitHub-hosted or approved self-hosted runners.

**Confidence:** High

---

## DR-W005-T013-02 — Python dependency/package management

**Domain:** Python package/dependency management

**Candidate decision:** Choose a lockfile-first project manager for the production Python surface, with uv as the current lead candidate.

**Status:** `PENDING_EVIDENCE`

### Why decision matters

The current inline `pip install` model does not give the product a committed, reviewable dependency resolution. The eventual runtime, packaging shape, native dependencies, and deployment target are still being researched by parallel W005 tasks.

### Sources consulted

Primary:
- uv locking/sync: https://docs.astral.sh/uv/concepts/projects/sync/
- uv workspaces: https://docs.astral.sh/uv/concepts/projects/workspaces/
- uv caching / CI guidance: https://docs.astral.sh/uv/concepts/cache/
- uv GitHub Actions guidance: https://docs.astral.sh/uv/guides/integration/github/
- Poetry basic/project usage: https://python-poetry.org/docs/basic-usage/
- PDM lock file: https://pdm-project.org/latest/usage/lockfile/
- PDM workspaces: https://pdm-project.org/latest/usage/workspace/

### Alternatives considered

1. **uv** — native lock/sync model, shared-lock workspaces, aggressive cache, direct GitHub Actions guidance; current lead.
2. **Poetry** — mature project/dependency workflow and lock file; broad existing Python adoption.
3. **PDM** — standards-oriented project metadata and lock files, including hashes; workspace support exists but is currently documented as experimental.
4. **pip + requirements/pip-tools** — lowest conceptual migration, but retains more fragmented project/environment/workspace tooling.

### Evidence summary

All finalists can improve reproducibility relative to inline pip. uv has the strongest current fit for speed, lock/sync, workspace capability, and CI cache integration; PDM has strong lock metadata and evolving workspace support; Poetry remains a mature comparator. The unresolved production runtime means performance and native-build behavior must be measured against the actual dependency set before a lock.

### Compatibility with repo/architecture

All three can consume standard `pyproject.toml`. uv offers a low-friction bridge because it also supports pip-compatible flows, but adopting its workspace model before the package topology is known would be premature.

### Operational burden

A new manager adds one bootstrap tool and one lockfile. The operational burden is acceptable only if CI/local commands are reduced to one documented path and frozen/locked installs are enforced.

### Migration / rollback

Migration can be staged: introduce `pyproject.toml`, generate candidate locks on a branch, compare resolution/test output, then change CI. Rollback is a return to the previous pip install commands until the production implementation is cut over.

### Benchmark / POC needed

Run `experiments/w005_toolchain/benchmark_toolchain.py python-managers` on the resolved production dependency set. Required evidence: cold lock/install, warm sync/install, repeat-lock byte stability, test pass rate, lock/hash characteristics, and CI cache footprint.

### Decision

Do not lock a Python package manager in T013. Carry **uv as lead**, Poetry and PDM as live challengers. Promote only after T002/T003 dependencies are known and the executable bakeoff has no correctness regressions.

**Confidence:** Medium-high on the requirement; medium on the eventual tool winner.

---

## DR-W005-T013-03 — JavaScript dependency/workspace management

**Domain:** JS/TS package and workspace management

**Candidate decision:** If W005-T002 selects a Node/TypeScript frontend or tooling surface, benchmark pnpm, npm workspaces, and Yarn; pnpm is the current lead for a multi-package workspace.

**Status:** `PENDING_EVIDENCE`

### Why decision matters

There is currently no production Node package topology in the repository. A package-manager lock before the frontend/API architecture is known would constrain a surface that may not exist or may remain a single package.

### Sources consulted

Primary:
- pnpm workspaces: https://pnpm.io/workspaces
- pnpm storage/install model: https://pnpm.io/motivation
- npm workspaces: https://docs.npmjs.com/cli/v12/using-npm/workspaces
- Yarn workspaces: https://yarnpkg.com/features/workspaces

Practical adoption evidence:
- pnpm's workspace documentation lists production OSS adopters including Next.js, Vite, Vue, SvelteKit, Prisma, Vercel and Turborepo, with migration commits.

### Alternatives considered

1. **pnpm** — built-in workspaces, shared workspace lock, strict dependency visibility, content-addressed store.
2. **npm workspaces** — minimal extra tooling and native npm support; attractive for a simple/single-package topology.
3. **Yarn** — mature workspace model and advanced dependency constraints/options.

### Evidence summary

All candidates support workspaces. pnpm has strong multi-package ergonomics and practical adoption; npm minimizes tool count; Yarn is credible where its workspace/constraint features are specifically needed. There is no repository evidence yet that distinguishes them.

### Compatibility with repo/architecture

Unknown until W005-T002 resolves whether a Node package is required and whether the frontend is independently deployable.

### Operational burden

Adding any JS manager creates a second language/package ecosystem next to Python. That cost should be paid only if the chosen frontend/API architecture requires it.

### Migration / rollback

No current Node migration is needed. If introduced, keep the package manager's lock file authoritative and make CI use frozen installs. Rollback before release is deleting the new Node surface/configuration.

### Benchmark / POC needed

On the W005-T002 selected frontend: compare clean install, warm install, lock stability, workspace filtering, CI cache size/time, and compatibility with the selected deployment platform.

### Decision

No JS package manager is locked by T013. pnpm is the lead only if a multi-package JS/TS workspace is actually selected; npm remains a strong simplicity baseline for a single package.

**Confidence:** High that a lock now would be premature.

---

## DR-W005-T013-04 — Repository/workspace/build strategy

**Domain:** Repository layout, task graph, build orchestration

**Candidate decision:** Keep a single Git repository and defer adding a build-graph product until the production app/package graph demonstrates value.

**Status:** `PENDING_EVIDENCE`

### Why decision matters

Task-graph tools can improve affected builds and caching, but they also add configuration, cache correctness/security concerns, and another execution layer. The current repository is primarily one Python codebase plus experiments and workflows rather than an evidenced multi-app monorepo.

### Sources consulted

Primary:
- Nx caching/task hashing: https://nx.dev/docs/concepts/how-caching-works
- Nx task pipelines: https://nx.dev/docs/concepts/task-pipeline-configuration
- Turborepo caching: https://github.com/vercel/turborepo/blob/main/apps/docs/content/docs/crafting-your-repository/caching.mdx
- Vercel/Turborepo remote caching: https://vercel.com/docs/monorepos/remote-caching
- uv Python workspaces: https://docs.astral.sh/uv/concepts/projects/workspaces/

### Alternatives considered

1. **Plain repository + language-native package/workspace commands + reusable GitHub workflows** — lowest complexity and current baseline evolution.
2. **Nx** — explicit project/task graph with input hashing and local/remote cache; strongest candidate if production becomes a heterogeneous multi-project workspace.
3. **Turborepo** — focused task caching/orchestration for JS/TS-centric monorepos, with remote cache support.
4. **Language-native workspaces only (uv / pnpm)** — middle ground when multiple packages exist but cross-language build orchestration is not yet needed.

### Evidence summary

Nx/Turborepo offer real graph/cache capabilities, but their benefit depends on repeated expensive deterministic tasks across multiple projects. Today the repo does not show that topology. W005-T002/T003 can materially change this conclusion.

### Compatibility with repo/architecture

The plain approach is fully compatible today. Nx has broader heterogeneous-project applicability than Turborepo, while Turborepo is a natural fit only if the final architecture becomes JS/TS-centric.

### Operational burden

Graph tools require graph configuration, cache-input correctness, upgrades, and potentially remote-cache credentials/storage. Native workflows impose less burden until scale warrants them.

### Migration / rollback

Start without a graph product. If thresholds are crossed, add one above existing package scripts so it can be removed without changing application semantics.

### Benchmark / POC needed

After T002/T003: measure clean CI duration, changed-file CI duration, number of independently deployable packages, repeated deterministic tasks, and cacheable output volume. Trial Nx and/or Turborepo only if the native pipeline becomes a measurable bottleneck.

### Decision

Single repository remains the baseline. No build-graph tool is locked yet.

**Confidence:** High on deferral; medium on future tool.

---

## DR-W005-T013-05 — Local development environment

**Domain:** Local developer environment

**Candidate decision:** Define a reproducible command contract first; allow native environments and Dev Containers to coexist until production services make containerization materially useful.

**Status:** `NO_PREFERENCE`

### Why decision matters

The project needs repeatable setup, but forcing every contributor into a container now would add Docker/runtime overhead before the production service graph is known.

### Sources consulted

Primary:
- Development Containers specification: https://containers.dev/
- Dev Container reference: https://github.com/devcontainers/spec/blob/main/docs/specs/devcontainer-reference.md

### Alternatives considered

1. **Native environment** using the selected pinned runtimes/package managers.
2. **Dev Container** (`devcontainer.json`) for a reproducible containerized environment.
3. **Nix-style environment manager** for stronger host reproducibility, at the cost of another ecosystem.

### Evidence summary

Dev Containers are an open specification designed to make development environments repeatable and can also support CI/testing. The current repo does not yet require multiple local infrastructure services, so the evidence does not justify making containers mandatory.

### Compatibility with repo/architecture

Native Python is already compatible. A Dev Container can be added later without changing application code if production dependencies warrant it.

### Operational burden

Native setup is lighter; Dev Containers reduce host variance but require a compatible container runtime/editor or CLI. Nix adds the highest learning/configuration burden.

### Migration / rollback

Document one canonical setup/test command independent of the shell environment. Add a Dev Container as an optional adapter if/when services or native dependencies justify it. Removal is low-risk because application commands remain environment-neutral.

### Benchmark / POC needed

If a Dev Container is proposed as mandatory, measure clean-machine time-to-first-green-test and image build/pull size against native setup on at least Linux and one developer desktop OS.

### Decision

No mandatory local-environment technology preference today; reproducibility requirements are locked, environment wrapper is not.

**Confidence:** High

---

## DR-W005-T013-06 — CI hardening and cache strategy

**Domain:** CI implementation policy

**Candidate decision:** Standardize reusable workflows, least-privilege tokens, immutable action references, lockfile-keyed dependency caches, and cache write restrictions.

**Status:** `LOCK`

### Why decision matters

The existing CI has avoidable duplication and supply-chain exposure. These controls are independent of the eventual app framework.

### Sources consulted

Primary:
- GitHub secure-use reference: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub dependency caching reference: https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
- GitHub reusable workflows: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
- GITHUB_TOKEN least privilege: https://docs.github.com/en/actions/tutorials/authenticate-with-github_token
- uv GitHub Actions cache example (candidate-specific): https://docs.astral.sh/uv/guides/integration/github/

### Alternatives considered

1. Keep current per-workflow setup and movable action tags.
2. Harden GitHub Actions in-place with reusable workflows and dependency-aware cache.
3. Add a separate CI/build-cache platform.

### Evidence summary

GitHub states that a full-length commit SHA is the only immutable way to reference an action. GitHub also supports reusable workflows, least-privilege `GITHUB_TOKEN` permissions, and dependency caching, while warning that caches should be treated as untrusted input and low-trust triggers should not gain unnecessary cache write access.

### Compatibility with repo/architecture

Directly compatible with the current 16 workflows and future package managers.

### Operational burden

Moderate one-time refactor, then lower maintenance through centralized setup. SHA pin updates should be automated rather than manual.

### Migration / rollback

Migrate one foundational workflow first, verify runtime/test parity, then fan out. Each workflow can roll back independently.

### Benchmark / POC needed

Measure median wall time over at least 5 cold-cache and 5 warm-cache runs for the representative foundation/test workflow. Keep dependency caching when median warm runtime improves >=20% without changing test results; otherwise prefer simplicity.

### Decision

Production CI must:

- pin third-party actions to verified full commit SHAs (with version comments for readability),
- declare minimal `permissions`,
- use committed dependency lock files and frozen/locked install modes,
- key dependency caches from the authoritative lock file plus runtime/OS as needed,
- limit cache writes on low-trust triggers,
- factor repeated setup into repository-local reusable workflows/composite actions after the package manager is selected.

**Confidence:** High

---

## DR-W005-T013-07 — Dependency updates and software supply-chain provenance

**Domain:** Dependency automation, SBOM, provenance, release integrity

**Candidate decision:** Use GitHub-native dependency automation and artifact attestations as the default control plane; add direct Cosign usage only when a consumer/registry requires it.

**Status:** `LOCK`

### Why decision matters

A production build needs reviewable dependency drift, verifiable build provenance, and a dependency inventory without creating an unnecessary parallel security platform.

### Sources consulted

Primary:
- Dependabot version updates: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates
- Dependabot grouping/options: https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference
- GitHub artifact attestations: https://docs.github.com/en/actions/concepts/security/artifact-attestations
- GitHub artifact-attestation usage / SLSA: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations
- SLSA v1.2: https://slsa.dev/spec/v1.2/
- Sigstore Cosign: https://docs.sigstore.dev/quickstart/quickstart-cosign/
- CycloneDX: https://cyclonedx.org/

### Alternatives considered

1. Manual dependency upgrades + unsigned artifacts.
2. GitHub-native Dependabot + GitHub artifact attestations/SBOM.
3. Renovate + direct Sigstore/Cosign pipeline.
4. Dedicated external supply-chain platform.

### Evidence summary

Dependabot can update package ecosystems and GitHub Actions and can group updates. GitHub artifact attestations bind build provenance to workflow/repository/commit/event metadata and use Sigstore; GitHub can also attach an SBOM. SLSA v1.2 defines provenance-oriented build levels, and GitHub documents a path using reusable workflows plus attestations toward SLSA Build Level 3. Cosign remains available for direct signing/verifying when an external consumer needs Sigstore-native bundles or registry semantics.

### Compatibility with repo/architecture

High because source and CI already live on GitHub. Package-specific Dependabot entries wait until package manifests exist.

### Operational burden

Low-to-moderate. Dependabot configuration is repository-local. Attestation generation adds release-workflow steps and permissions, but avoids a separate signing key for GitHub OIDC/Sigstore-based flows.

### Migration / rollback

Enable GitHub Actions update automation first, then package ecosystems after manifests exist. Add attestations only to release artifacts initially. Rollback removes workflow/config steps without changing artifact format.

### Benchmark / POC needed

Security controls are primarily correctness/policy gates, not speed contests. POC must verify that a produced release artifact can be verified from a clean environment and that its provenance resolves to the expected repository, commit, workflow, and subject digest. SBOM generation must cover direct and transitive production dependencies selected by the final package topology.

### Decision

Production baseline:

- automate GitHub Actions dependency updates and, once manifests exist, package updates; group routine low-risk updates to control PR noise,
- generate an SBOM for release artifacts (CycloneDX or SPDX; format is `NO_PREFERENCE` until downstream consumer requirements are known),
- generate and verify GitHub artifact attestations for releasable binaries/images/packages,
- target SLSA provenance properties incrementally rather than claiming a level without verification,
- use direct Cosign only when deployment/consumer requirements need explicit Sigstore signing/verification beyond GitHub-native attestations.

**Confidence:** High

---

## Decision summary

| Area | Status | Outcome |
|---|---|---|
| CI platform | `LOCK` | GitHub Actions |
| Python dependency manager | `PENDING_EVIDENCE` | uv leads; Poetry/PDM remain challengers |
| JS package manager | `PENDING_EVIDENCE` | pnpm leads for multi-package; npm simplicity baseline |
| Repo/build graph | `PENDING_EVIDENCE` | single repo; no graph tool until topology/perf justify it |
| Local dev wrapper | `NO_PREFERENCE` | native and Dev Container both acceptable behind one command contract |
| CI hardening/cache | `LOCK` | SHA pinning, least privilege, lockfile/frozen install, measured cache, reusable setup |
| Supply chain | `LOCK` | Dependabot + SBOM + GitHub artifact attestations; Cosign only when required |
| SBOM encoding | `NO_PREFERENCE` | CycloneDX or SPDX pending consumer requirement |

## Reversal conditions

Re-open a `LOCK` only if one of these appears:

- GitHub Actions cannot satisfy a measured runner/performance/compliance requirement even with appropriate runners and reusable workflows.
- The release target cannot consume/verify GitHub attestations and requires a different signing/provenance mechanism.
- Security policy or platform constraints make GitHub-native dependency automation or OIDC-based attestation unavailable.

Promote `PENDING_EVIDENCE` choices only after W005-T002/W005-T003 provide the actual app/runtime topology and the reproducible benchmarks in `experiments/w005_toolchain/` are run against it.
