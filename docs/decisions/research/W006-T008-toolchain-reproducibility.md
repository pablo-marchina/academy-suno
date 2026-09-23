# W006-T008 — Reproducible toolchain and supply-chain decision research

Research date: 2026-09-23  
Task: `W006-T008`  
Attempt: `A01`  
Gate: `SYSTEM/DECISION_RESEARCH_GATE.md`

This record resolves only choices for which this attempt produced representative repository evidence. It does not select a production runtime, database, parser, frontend, cloud, or deployment topology.

## DR-W006-T008-01 — Python package manager

**Domain:** Python dependency/package management  
**Status:** `LOCK`  
**Decision:** uv `0.12.18` with a committed root `pyproject.toml` + `uv.lock`, Python `3.13.15`, and locked/frozen CI installs.

### Evidence and alternatives

The comparison used one clean `ubuntu-24.04` GitHub-hosted runner and the same seven direct repository dependencies/challengers for all candidates: `pydantic==2.13.4`, `jsonschema==4.25.1`, `pytest==9.0.2`, `pypdf==5.9.0`, `dbos==2.31.0`, `langgraph==1.2.12`, and `langgraph-checkpoint-sqlite==3.1.1`.

Predeclared hard gates were non-compensatory: resolve, locked install, import verification, warm re-sync, and byte-stable repeated locking. All three candidates passed every hard gate over three repeats.

| Candidate | Version | Hard gates | Median first lock | Median first sync | Median warm sync |
|---|---:|---|---:|---:|---:|
| uv | 0.12.18 | PASS | 0.0200 s | 0.0340 s | 0.0086 s |
| Poetry | 2.5.1 | PASS | 2.0448 s | 1.9621 s | 0.7090 s |
| PDM | 2.29.2 | PASS | 18.8626 s | 10.0973 s | 0.4866 s |

Primary repository evidence:

- workflow run `35869987042`;
- artifact `10754189048`, digest `sha256:dda7bf276e5c74f3a7cc00542a7d1478185efd269ebfefbae0489a9905956b3c`;
- persisted summary `artifacts/w006-t008/a01/manager-benchmark.json`;
- executable harness `experiments/w006_t008_toolchain/benchmark_real_graph.py`.

The performance difference is used only after all correctness/reproducibility gates passed. uv additionally preserves the lowest operational surface for this Python-only production repository: one manifest, one lock, one sync path, and no additional task graph.

### Canonical lock scope

The root application/test lock contains the accepted application dependency (`pydantic`) and accepted test dependencies (`jsonschema`, `pytest`). Historical `pypdf` and runtime-bakeoff challengers remain in the toolchain bakeoff scope under `tool.academy-suno.toolchain-bakeoff`, but are deliberately excluded from the canonical application lock until their owning technology decisions are resolved.

### Canonical commands

- lock verification: `uv lock --check`
- clean test install: `uv sync --locked --no-install-project --group test`
- foundation regression: `uv run --no-sync python experiments/foundation_regression/run_foundation_regression.py`
- deterministic release evidence: `uv run --no-sync python scripts/supply_chain/build_release_evidence.py --output-dir dist/release`
- release evidence verification: command frozen in `toolchain.lock.json`

### Confidence and reversal

**Confidence:** `HIGH` for the current Python repository graph.

Re-open if any of the following occurs:

1. `uv lock --check` or locked sync cannot reproduce on a supported target environment while a challenger can;
2. the authoritative dependency graph changes materially enough to invalidate the measured comparison;
3. a packaging/deployment target requires semantics not supported by the selected uv path;
4. correctness or lock stability regresses on representative CI.

Rollback is bounded: `pyproject.toml` is standards-based, and the repository retains the benchmark harness for Poetry/PDM re-evaluation.

---

## DR-W006-T008-02 — Repository topology and task graph

**Domain:** repository/build graph  
**Status:** `NO_ADDITIONAL_TOOLING`  
**Decision:** keep the existing single repository and do not add Nx, Turborepo, a JS package manager, or another task graph in this attempt.

### Evidence

The repository baseline observed no production Node package manifest and no existing build-graph configuration. The accepted production surface remains Python-first. The package-manager bakeoff and locked foundation regression execute without an additional task graph.

No measured repeated-work or multi-deployable bottleneck was produced that would compensate for another cache/configuration/execution layer. Therefore W005-T013's adoption gate remains unsatisfied.

**Confidence:** `HIGH` that no task-graph addition is justified now; `LOW` about future topology after frontend/deployment decisions.

Re-open only when a real Node/TypeScript production surface, multiple independently deployable projects, or measured CI duplication provides evidence for a graph/cache layer.

---

## DR-W006-T008-03 — Release reproducibility and supply-chain controls

**Domain:** CI/release supply chain  
**Status:** `LOCK`

**Decision:** retain GitHub Actions; pin third-party release Actions to full commit SHAs; default workflows to `contents: read`; isolate `id-token: write` + `attestations: write` to the attestation job; use lock-derived cache keys and suppress reusable cache writes on pull-request runs; generate deterministic source artifacts, an SPDX 2.3 runtime SBOM, local digest-bound provenance, and GitHub build-provenance attestation.

### Evidence / implementation

Frozen Action SHAs are recorded in `toolchain.lock.json`. The release-path audit in `scripts/supply_chain/audit_release_workflows.py` fails closed if a third-party release Action is movable or top-level release permissions broaden beyond `contents: read`.

`w006-t008-supply-chain.yml` performs:

1. clean checkout and Python `3.13.15` setup;
2. exact uv `0.12.18` bootstrap;
3. committed lock checksum + `uv lock --check`;
4. locked install and foundation regression;
5. release workflow pin/permission audit;
6. two independent deterministic artifact/SBOM/provenance builds with byte comparison;
7. fail-closed digest/SBOM/provenance verification;
8. GitHub provenance attestation in a separate least-privilege job and `gh attestation verify`.

The runtime SBOM follows only the root production dependency closure from `uv.lock`; test-only dependencies are explicitly rejected by the verifier.

**Confidence:** `HIGH` in the controls once the final CI run is green; `MEDIUM` in portability to future package/container release formats, which may require an additional SBOM/signing format.

Re-open if a registry/consumer requires container-native signing, CycloneDX specifically, a different provenance verifier, or target-platform identity semantics beyond GitHub-native attestations. Adding Cosign remains an escalation, not a current requirement.

---

## Non-decisions preserved

This attempt does **not** promote any runtime-bakeoff dependency to production. The following remain explicitly open: production runtime, production database, production parser, Node/JS production surface, cloud/deployment target, and any multi-project task graph.
