# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0055`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W006-T008-A02-REJECTED-SCALAR-UTILITY-A03-READY`

## Objective

Implementar e qualificar o produto real multiusuário sob os contratos/evidências aceitos em W005, preservando hard gates determinísticos e usando adaptação somente onde evidence-backed.

## Preserved truth

- W004 permanece baseline/evidência histórica e não autoriza production readiness.
- W005 permanece autoridade de planejamento/arquitetura, não prova de production readiness.
- W005-T009-A02 `W005-BENCHMARK-METHODOLOGY-V002` permanece autoridade metodológica: hard gates não compensatórios → métricas multidimensionais brutas → incerteza quando aplicável → point Pareto; scalar/business utility só é permitido com evidência humana/business representativa + sensitivity estável.
- W006-T007-A01 preserva explicitamente scalar/business weights como `PENDING_EVIDENCE` e proíbe preferência por pesos inventados.
- human gold/agreement/preference empíricos continuam não observados; production audience thresholds permanecem `DIAGNOSTIC_ONLY`.
- escolhas `NO_PREFERENCE/PENDING_EVIDENCE` não viram winners por conveniência durante implementação.
- production-ready claim permanece `FALSE`.

## W006 accepted substrate through STATE 0053

- `W006-T001-A02` through `W006-T007-A01` required substrate/fan-in tasks are accepted/integrated.
- `W006-T010-A01` eval/human-calibration foundation is accepted/integrated, but independent human streams remain `0`, adjudicated human gold remains `0`, HELD_OUT remains `NOT_RUN`, and audience thresholds remain `DIAGNOSTIC_ONLY`.
- T007 carries evidence-backed contracts/invariants only; production runtime/database/frontend/infrastructure/deployment/observability/package-manager choices remain evidence-gated unless separately closed by compliant Decision Research.

## W006-T008-A01 — DIAGNOSTIC / NOT ACCEPTED

A01 completed valid terminal lifecycle and produced strong executable toolchain/supply-chain evidence on PR #218, but its material uv package-manager `LOCK` lacked the complete mandatory Decision Research record. PR #218 remains closed without merge.

## W006-T008-A02 — COMPLETE BUT NOT ACCEPTED

A02 ran from STATE 0054 on `worker/W006-T008-A02`, persisted `SYSTEM/RESULTS/W006-T008-A02.md` at `f687c00a7e02b6f82a0ec845d7d021a5ea17f3ea`, opened PR #221, and produced green result-bearing CI:

- System Integrity `35880827837`: SUCCESS;
- Foundation Regression `35880828453`: SUCCESS;
- W006 T008 Supply Chain `35880828248`: SUCCESS;
- W006 T008 Toolchain Bakeoff `35880827832`: SUCCESS.

A02 repaired A01's DRG structure and produced useful fresh evidence, including current primary-source coverage, same-runner uv/Poetry/PDM measurements, clean locked validation, deterministic release, SPDX verification and provenance/attestation verification.

A02 is **not accepted/integrated** because its package-manager promotion still violates accepted W005 benchmark methodology v002 and the A02 dispatch. It introduced preregistered scalar weights (`0.40/0.25/0.20/0.10/0.05` plus sensitivity sets) without representative human/business utility evidence. Pre-registration prevents post-hoc tuning but does not make unsupported scalar utility evidence-backed. It also assigned synthetic neutral `1.0` values to decision dimensions where no representative candidate-specific evidence differentiated candidates, rather than preserving raw objectives/missingness/non-comparability.

This conflicts with:

- W005-T009-A02: no universal scalar score/weights; utility remains `BUSINESS_UTILITY_PENDING_EVIDENCE`;
- W006-T007-A01: hard gates → raw multidimensional evidence → uncertainty → Pareto, and scalar/business weighting unavailable until representative evidence exists;
- W006-T008-A02 dispatch: `no arbitrary scalar utility`.

PR #221 is closed without merge. A02 remains immutable diagnostic evidence. Two `TASK_STARTED` comments were observed for A02; one is protocol-valid and exactly one terminal signal exists. The duplicate start is recorded as lifecycle-noise/hygiene evidence, not the rejection basis.

## W006-T008-A03 — READY

Fresh retry A03 is READY on `worker/W006-T008-A03`.

Base provenance is `STATE 0054 / 869e94a8694c96ee460b8f27d9678623838fa61e`. The worker must continuity-check against STATE 0055/current main before substantive work.

A03 may cite A01/A02 only as diagnostic/counterfactual evidence. It must independently persist its own RESULT, canonical research record and fresh representative validation. The package-manager decision surface is fixed to accepted methodology:

1. predeclare non-compensatory hard gates;
2. predeclare raw measurable objectives and directions;
3. preserve missingness explicitly — do not replace unmeasured objectives with neutral synthetic scores;
4. report raw observations/repeats/uncertainty;
5. compute point Pareto only across valid comparable required objectives;
6. no scalar weights, synthetic utility, practical-effect thresholds or lexicographic priority unless representative business/human evidence exists and was frozen before outcomes;
7. `LOCK` only if an eligible candidate is uniquely supported by the evidence under this multidimensional surface; otherwise `NO_PREFERENCE` / `PENDING_EVIDENCE`.

A03 must use a fresh unique canonical Decision Research record (use `DR-6009` if still available at worker start) and preserve all unrelated T007 technology boundaries.

Hard acceptance:

- complete applicable DRG record for every material `LOCK`/default = `100%`;
- scalar/business utility without representative evidence = `0`;
- synthetic neutral scoring of missing required objectives = `0`;
- hard-gate compensation = `0`;
- clean locked install/build/test = `PASS` if a lock is promoted;
- movable third-party release Actions = `0`;
- unnecessarily broad release token permissions = `0`;
- releasable artifact has verifiable SBOM + provenance/attestation = `PASS`;
- repository migration without DRG evidence = `0`;
- unresolved runtime/database/parser/frontend/deployment choices remain unchanged;
- production-ready claim = `NOT_AUTHORIZED`.

## W006 dependency gates

- `W006-T001-A02`: INTEGRATED;
- `W006-T002-A01`: INTEGRATED;
- `W006-T003-A01`: INTEGRATED;
- `W006-T004-A01`: INTEGRATED;
- `W006-T005-A02`: INTEGRATED;
- `W006-T006-A01`: INTEGRATED;
- `W006-T007-A01`: INTEGRATED;
- `W006-T008-A01`: RESULT_RECEIVED / diagnostic-not-accepted;
- `W006-T008-A02`: RESULT_RECEIVED / diagnostic-not-accepted;
- `W006-T008-A03`: READY;
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

`W006-T008_A03_MULTIDIMENSIONAL_PARETO_TOOLCHAIN_FREEZE`

## Next action

Execute `W006-T008-A03` in an independent worker chat. T009 remains gated until a T008 attempt is accepted/integrated.

## Recovery point

Resume from STATE 0055. Ready queue: `W006-T008-A03`. Blanket production readiness remains false.
