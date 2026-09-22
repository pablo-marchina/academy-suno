# W005-T013 toolchain evidence harness

This directory makes the developer-platform recommendations reproducible instead of prose-only.

## Baseline inventory

Run from the repository root:

```bash
python experiments/w005_toolchain/benchmark_toolchain.py baseline --repo . > /tmp/w005-t013-baseline.json
```

The inventory measures:

- number and names of GitHub Actions workflow files;
- Python and Node project manifests;
- known package lock files;
- inline `pip install` commands in workflows;
- total `uses:` references and how many are pinned to full 40-character Git SHAs;
- explicit `permissions:` declarations.

The research-time repository tree on 2026-09-22 showed 16 workflow YAML files, no root `pyproject.toml`, no standard Python lockfile, and no production `package.json`/Node lockfile. `foundation-tests.yml` is a concrete current example of inline pip installation and movable action tags.

## Python manager bakeoff

The harness compares installed candidates without silently installing tools:

```bash
python experiments/w005_toolchain/benchmark_toolchain.py python-managers --repeats 3 > /tmp/w005-t013-python-managers.json
```

Candidate set:

- uv
- Poetry
- PDM

Each available manager gets an isolated temporary PEP 621 project with the same Python requirement and dependency set. The harness records lock time, first sync/install time, warm sync/install time, import verification, a second lock, and whether the lockfile is byte-stable across the repeated lock operation.

For decision evidence, run the harness on the same clean runner image and then repeat it with the real dependency set selected by W005-T002/W005-T003. Do not compare numbers collected on different machines as if they were equivalent.

### Promotion gate

A Python manager can move from `PENDING_EVIDENCE` to `LOCK` only when:

1. all production/test dependencies resolve and the existing suite passes;
2. CI can fail on a stale/missing lock (`--locked`, lock freshness check, or equivalent);
3. repeated locking with unchanged inputs is stable enough for review (no unexplained dependency churn);
4. package hashes/artifact identity are recorded by the lock mechanism or equivalent control;
5. local and CI workflows use one documented command contract;
6. operational complexity does not increase without a measured compensating benefit;
7. if candidates are otherwise equivalent, measured runtime is used as a tie-breaker rather than brand preference.

uv is the research lead, not a locked winner.

## JS manager bakeoff

Do not run until W005-T002 establishes a production Node/TypeScript surface. Compare pnpm, npm workspaces, and Yarn on the selected frontend using:

- clean install wall time;
- second/warm install wall time;
- lockfile stability;
- workspace filtering/linking correctness;
- dependency visibility/isolation;
- CI cache size and restoration time;
- deployment-platform compatibility.

Use the same application commit and runner image for all candidates. pnpm is the lead only for a demonstrated multi-package workspace; npm is the simplicity baseline for a single package.

## Build/workspace orchestration gate

Start with package-manager/native scripts plus GitHub Actions. Only POC Nx/Turborepo if the post-T002/T003 topology has multiple independently deployable projects or CI measurements show repeated deterministic work is a material bottleneck.

Collect at minimum:

- clean CI median duration (5 runs);
- one-leaf-change CI median duration (5 runs);
- number of tasks skipped/restored from cache;
- remote-cache upload/download bytes if enabled;
- configuration LOC and new credentials/services introduced;
- correctness test showing environment/config changes invalidate cached outputs when they should.

A graph tool must demonstrate meaningful saved wall time on representative changes without weakening cache correctness. If the difference is small, retain the native setup.

## GitHub Actions cache gate

For the representative foundation/test workflow, record at least five cold-cache and five warm-cache successful runs after the authoritative lockfile exists.

Adopt dependency caching when median warm runtime improves by at least 20% and test output is unchanged. Cache keys must include the authoritative lockfile plus runtime/OS dimensions where they affect artifacts. Low-trust triggers should not get unnecessary cache write access.

## Local-development environment gate

Native setup and Dev Containers are currently `NO_PREFERENCE` wrappers around the same command contract. If a mandatory Dev Container is proposed later, compare clean-machine time-to-first-green-test and environment size/boot cost against native setup on Linux and at least one developer desktop OS.

## Supply-chain verification POC

For each releasable artifact once a release artifact exists:

1. produce an SBOM (CycloneDX or SPDX);
2. generate a GitHub artifact attestation/provenance record;
3. from a clean verifier environment, verify the subject digest and provenance identity;
4. confirm provenance resolves to the expected repository, commit SHA, workflow, and trigger;
5. fail the verification probe after intentionally changing the artifact bytes.

Direct Cosign is an escalation path when the target registry/consumer requires explicit Sigstore signing semantics beyond GitHub-native attestations.

## Sources

Research record and source URLs: `docs/decisions/research/W005-T013-developer-platform.md`.
