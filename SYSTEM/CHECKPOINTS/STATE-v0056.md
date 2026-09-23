# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0056`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W006-T008-A03-ACCEPTED-T009-READY`

## Objective

Implementar e qualificar o produto real multiusuário sob os contratos/evidências aceitos em W005, preservando hard gates determinísticos e usando adaptação somente onde evidence-backed.

## Preserved truth

- W004 permanece baseline/evidência histórica e não autoriza production readiness.
- W005 permanece autoridade de planejamento/arquitetura, não prova de production readiness.
- W005-T009-A02 `W005-BENCHMARK-METHODOLOGY-V002` permanece autoridade metodológica: hard gates não compensatórios → métricas multidimensionais brutas → incerteza quando aplicável → point Pareto; scalar/business utility só é permitido com evidência humana/business representativa + sensitivity estável.
- human gold/agreement/preference empíricos continuam não observados; production audience thresholds permanecem `DIAGNOSTIC_ONLY`.
- escolhas `NO_PREFERENCE/PENDING_EVIDENCE` não viram winners por conveniência durante implementação.
- production-ready claim permanece `FALSE`.

## W006 accepted substrate through STATE 0056

- `W006-T001-A02` through `W006-T007-A01` required substrate/fan-in tasks are accepted/integrated.
- `W006-T010-A01` eval/human-calibration foundation is accepted/integrated, but independent human streams remain `0`, adjudicated human gold remains `0`, HELD_OUT remains `NOT_RUN`, and audience thresholds remain `DIAGNOSTIC_ONLY`.
- `W006-T008-A03` is accepted/integrated via PR #223 after fresh DRG-compliant hard-gate/raw-metric/uncertainty/point-Pareto evidence and green result-bearing CI.

## W006-T008 disposition

A01 remains diagnostic/not accepted because its material uv package-manager `LOCK` lacked the complete mandatory Decision Research record. A02 remains diagnostic/not accepted because its material package-manager promotion used unsupported scalar weights/synthetic neutral scores despite accepted W005 benchmark methodology v002.

A03 repaired both failure modes. It persisted `SYSTEM/RESULTS/W006-T008-A03.md` and canonical `docs/decisions/research/DR-6009-reproducible-toolchain-supply-chain-pareto.md` on `worker/W006-T008-A03`, with one protocol-valid `TASK_STARTED`, exactly one terminal `TASK_COMPLETE`, and `CONTINUITY_CHECK: PASS` against STATE 0055.

Accepted scoped decision:

- Python `3.13.15`;
- package manager `uv@0.12.18`;
- committed `pyproject.toml` + `uv.lock`;
- current single-project Python repository graph only;
- repository topology remains `NO_MIGRATION_FOR_CURRENT_GRAPH`;
- no Node package manager/task graph introduced.

Binding fresh A03 evidence:

- all uv/Poetry/PDM candidates passed non-compensatory hard gates;
- predeclared lower-is-better median objectives `(first lock, first sync, warm sync)` yielded uv `(0.0207, 0.0392, 0.0096)`, Poetry `(2.3400, 2.4442, 0.8529)`, PDM `(29.1955, 14.1363, 0.5791)` seconds;
- point-Pareto frontier = `[uv]`, with uv dominating both alternatives on all three required comparable objectives;
- scalar weights, synthetic utility, neutral imputation and hard-gate compensation used for preference = `0`;
- selected-baseline clean locked install/Foundation Regression/deterministic double-build/SPDX/local provenance/GitHub attestation verification = PASS;
- movable third-party release Action refs = `0`;
- unnecessarily broad release token permissions = `0`.

Result-bearing final-head checks on `19b7e7fb7b54cb8d01cfdfd668ebc6e494b6f8f4`:

- System Integrity `35890079558`: SUCCESS;
- Foundation Regression `35890079456`: SUCCESS;
- W006 T008 Supply Chain `35890079552`: SUCCESS;
- W006 T008 Toolchain Bakeoff `35890079536`: SUCCESS.

PR #223 merged into main as `f6a1cd7a7e8f8971e27c1632d68560357b9aae16`.

The accepted toolchain lock is narrow. Production workflow/runtime, database/shared state, parser/OCR, frontend/editor, identity/data/object vendors, observability backend, deployment class, business utility and overall production readiness remain evidence-gated/open as previously recorded.

## W006-T009-A01 — READY

Dependencies `W006-T007` and accepted `W006-T008-A03` are now satisfied, so `W006-T009-A01` is READY.

T009 must integrate the same real product path rather than a parallel demo: auth → workspace → secure upload → parse/provenance → durable exact 9-way workflow → eval/repair → aggregate → durable product/domain events → authoritative live cockpit.

Continuity requirements:

- preserve dispatch provenance `STATE 0047 / 0fa1fd46d02d8fb2ad3410823ba417d83b596eac`;
- perform fresh `CONTINUITY_CHECK` against STATE 0056/current main before substantive work;
- use `worker/W006-T009-A01`;
- emit exactly one protocol-valid `TASK_STARTED` and exactly one terminal signal;
- no worker edits to canonical coordination surfaces.

T009 hard acceptance includes current live run correlation by source/run/job/attempt/event identities, accepted provenance missing = `0`, exact `9/9` with zero accepted loss/duplication, arbitrary untrusted server filesystem-path production route = `0`, replay/reconnect PASS, tenant adversarial suite PASS, and telemetry outage not corrupting or blocking the authoritative product result.

The accepted T008 toolchain is an implementation constraint for T009, not permission to manufacture unresolved runtime/database/parser/frontend/deployment winners. Any new material technology default still requires exact DRG-compliant evidence.

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
- `W006-T008-A03`: INTEGRATED;
- `W006-T009-A01`: READY;
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
- accepted production toolchain lock: `uv@0.12.18` + Python `3.13.15` for current single-project Python graph;
- production runtime/database lock: none;
- production parser winner: none;
- concrete frontend/framework winner: none;
- deployment/observability/vendor winners: none;
- submission completed: not claimed.

## Current success bottleneck

`W006-T009_REAL_PRODUCTION_VERTICAL_SLICE`

## Next action

Execute `W006-T009-A01` in an independent worker chat. T011 and T012 remain gated until T009 is accepted/integrated.

## Recovery point

Resume from STATE 0056. Ready queue: `W006-T009-A01`. Blanket production readiness remains false.
