# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0054`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W006-T008-A01-REJECTED-DRG-A02-READY`

## Objective

Implementar e qualificar o produto real multiusuário sob os contratos/evidências aceitos em W005, preservando hard gates determinísticos e usando adaptação somente onde evidence-backed.

## Preserved truth

- W004 permanece baseline/evidência histórica e não autoriza production readiness.
- W005 permanece autoridade de planejamento/arquitetura, não prova de production readiness.
- human gold/agreement/preference empíricos continuam não observados; production audience thresholds permanecem `DIAGNOSTIC_ONLY` até independent human calibration + HELD_OUT replication.
- escolhas `NO_PREFERENCE/PENDING_EVIDENCE` não viram winners por conveniência durante implementação.
- production-ready claim permanece `FALSE`.

## W006 accepted substrate through STATE 0053

- `W006-T001-A02` through `W006-T007-A01` required substrate/fan-in tasks are accepted/integrated.
- `W006-T010-A01` eval/human-calibration foundation is accepted/integrated, but independent human streams remain `0`, adjudicated human gold remains `0`, HELD_OUT remains `NOT_RUN`, and audience thresholds remain `DIAGNOSTIC_ONLY`.
- T007 carries evidence-backed contracts/invariants only; production runtime/database/frontend/infrastructure/deployment/observability/package-manager choices remain evidence-gated unless separately closed by compliant Decision Research.

## W006-T008-A01 — COMPLETE BUT NOT ACCEPTED

A01 executed substantial toolchain/supply-chain work on branch `worker/W006-T008-A01` and emitted exactly one terminal `TASK_COMPLETE` with RESULT `SYSTEM/RESULTS/W006-T008-A01.md` at `4d98952405a9c478dcf1c82aa47531ebbc4e7c1c` / PR #218.

Useful diagnostic evidence includes:

- valid lifecycle and `CONTINUITY_CHECK: PASS` against STATE 0053;
- same-runner package-manager bakeoff across uv 0.12.18, Poetry 2.5.1 and PDM 2.29.2, with all predeclared correctness/reproducibility gates passing;
- observed median first-lock/first-sync seconds: uv `0.0200/0.0340`, Poetry `2.0448/1.9621`, PDM `18.8626/10.0973`;
- clean locked install/build/test PASS;
- movable third-party release Actions = `0`;
- unnecessarily broad release token permissions = `0`;
- deterministic artifact + SPDX SBOM + digest-bound local provenance PASS;
- GitHub/Sigstore build attestation created and `gh attestation verify` exit `0`;
- RESULT-bearing System Integrity run `35873747013`: success.

A01 is **not accepted/integrated** because it promoted uv to a material package-manager `LOCK` without a research record satisfying the mandatory `SYSTEM/DECISION_RESEARCH_GATE.md` record contract. The A01 file `docs/decisions/research/W006-T008-toolchain-reproducibility.md` contains benchmark/reversal evidence but omits required systematic source-search strategy/date/stopping rule, source table, primary-evidence-first coverage, explicit relevant security/reliability/cost/lock-in treatment and traceability, and does not use the required `docs/decisions/research/DR-####-<slug>.md` form.

PR #218 is closed without merge. A01 remains immutable diagnostic evidence; its successful CI does not waive DRG.

## W006-T008-A02 — READY

Fresh retry A02 is READY on `worker/W006-T008-A02`.

Base provenance is `STATE 0053 / edef0ba740de4b82c70dbb28024258b6f5aa7df7`. The worker must run `CONTINUITY_CHECK` against STATE 0054/current main before substantive work.

A02 may use A01 outputs as diagnostic/counterfactual evidence, but must independently persist its own RESULT and any implementation/toolchain changes on the fresh branch. Before any package-manager/toolchain/repository-topology choice becomes `LOCK`/default, A02 must satisfy every applicable DRG field, including a canonical `DR-####-<slug>.md` record, at least three alternatives where available, predeclared criteria, systematic primary-source search, source table, evidence-saturation stopping rule, relevant security/reliability/cost/lock-in analysis, representative reproducible benchmark, raw results/uncertainty, confidence, reversal conditions and traceability.

Hard acceptance remains:

- clean locked install/build/test PASS;
- movable third-party release Actions = `0`;
- unnecessarily broad release token permissions = `0`;
- releasable artifact has verifiable SBOM + provenance/attestation;
- repository migration occurs only with compliant DRG evidence;
- material toolchain/default LOCK lacking complete DRG record = `0`;
- unresolved production runtime/database/parser/frontend/deployment choices remain unchanged.

## W006 dependency gates

- `W006-T001-A02`: INTEGRATED;
- `W006-T002-A01`: INTEGRATED;
- `W006-T003-A01`: INTEGRATED;
- `W006-T004-A01`: INTEGRATED;
- `W006-T005-A02`: INTEGRATED;
- `W006-T006-A01`: INTEGRATED;
- `W006-T007-A01`: INTEGRATED;
- `W006-T008-A01`: RESULT_RECEIVED / diagnostic-not-accepted;
- `W006-T008-A02`: READY;
- `W006-T009-A01`: PLANNED, gated on an accepted T008 attempt;
- `W006-T010-A01`: INTEGRATED foundation; empirical human evidence remains external/pending;
- `W006-T011-A01`: PLANNED, T010 satisfied but gated on T009;
- `W006-T012-A01`: PLANNED, gated on T009;
- `W006-T013-A01`: PLANNED, gated on T009+T011+T012;
- `W006-T014-A01`: PLANNED, T010 satisfied but gated on T011+T013.

## Hard invariants carried into Phase 9

- hard-gate compensation = `0`;
- cross-tenant unauthorized success in defined tests = `0`;
- accepted required provenance missing = `0`;
- exact branch coverage = `9/9`;
- accepted join branch loss/duplication = `0`;
- critical schema violations promoted = `0`;
- silent stale same-run overwrite = `0`;
- duplicate accepted branch output from retry/delivery = `0`;
- static/counterfactual evidence used as production live truth = `0`;
- arbitrary untrusted server filesystem-path production input = `0`;
- private quarantine bypass in defined tests = `0`;
- secret/credential canary leakage in product events/telemetry = `0`;
- defined restart/resume scenarios = `100% PASS` before production claim;
- defined backup/restore scenarios = `100% PASS` before production claim;
- final technical video = `<=5:00`.

## Evidence boundary

- production-ready claim: `FALSE`;
- human gold: not observed;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- production runtime/database lock: none;
- production parser winner: none;
- concrete frontend/framework winner: none;
- accepted production package-manager/toolchain lock from T008: none yet;
- submission completed: not claimed.

## Current success bottleneck

`W006-T008_A02_DRG_COMPLIANT_REPRODUCIBLE_TOOLCHAIN_FREEZE`

## Next action

Execute `W006-T008-A02` in an independent worker chat. T009 remains gated until a T008 attempt is accepted/integrated.

## Recovery point

Resume from STATE 0054. Ready queue: `W006-T008-A02`. Blanket production readiness remains false.
