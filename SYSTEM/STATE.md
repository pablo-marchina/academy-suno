# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0058`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W006-T009-A02-ACCEPTED-T011-T012-READY`

## Objective

Implementar e qualificar o produto real multiusuário sob os contratos/evidências aceitos em W005, preservando hard gates determinísticos e usando adaptação somente onde evidence-backed.

## Preserved truth

- W004 permanece baseline/evidência histórica e não autoriza production readiness.
- W005 permanece autoridade de planejamento/arquitetura, não prova de production readiness.
- W005-T009-A02 `W005-BENCHMARK-METHODOLOGY-V002` permanece autoridade metodológica: hard gates não compensatórios → métricas multidimensionais brutas → incerteza quando aplicável → point Pareto; scalar/business utility só é permitido com evidência humana/business representativa + sensitivity estável.
- human gold/agreement/preference empíricos continuam não observados; production audience thresholds permanecem `DIAGNOSTIC_ONLY`.
- escolhas `NO_PREFERENCE/PENDING_EVIDENCE` não viram winners por conveniência durante implementação.
- production-ready claim permanece `FALSE`.

## W006 accepted substrate through STATE 0058

- `W006-T001-A02` through `W006-T008-A03` required substrate/toolchain tasks are accepted/integrated.
- `W006-T010-A01` eval/human-calibration foundation is accepted/integrated, but independent human streams remain `0`, adjudicated human gold remains `0`, HELD_OUT remains `NOT_RUN`, and audience thresholds remain `DIAGNOSTIC_ONLY`.
- accepted toolchain constraint for the current single-project Python graph remains Python `3.13.15` + `uv@0.12.18` + committed `pyproject.toml`/`uv.lock`; broader runtime/database/parser/frontend/deployment/vendor decisions remain open/evidence-gated.
- `W006-T009-A02` is accepted/integrated via PR #227 after valid lifecycle and exact frozen-toolchain proof on the same real/reference product path.

## W006-T009 disposition

A01 remains diagnostic/not accepted because its dedicated validation workflow bypassed the accepted T008-A03 frozen toolchain with non-exact Python `3.13` plus a hand-selected direct-pip dependency subset.

A02 repaired that failure on fresh lifecycle/provenance. It persisted `SYSTEM/RESULTS/W006-T009-A02.md` and machine-readable evidence, used exact Python `3.13.15`, exact `uv@0.12.18`, `uv lock --check`, frozen `uv sync --locked`, and executed task/regression tests from that locked environment. Final-head task, Foundation Regression, System Integrity and T008 Supply Chain workflows were green.

Accepted A02 integration evidence includes:

- same real/reference product path: auth → workspace → controlled PDF bytes upload/quarantine/provenance → parser contract/trust boundary → durable exact 3×3 workflow → eval/branch-local repair → aggregate → durable authoritative product/domain events → live cockpit replay/reconnect;
- accepted provenance missing = `0`;
- exact branch coverage = `9/9`;
- accepted branch loss/duplication = `0`;
- silent stale same-run overwrite accepted = `0` under accepted durable-state/event regressions;
- duplicate accepted retry/republication output = `0`;
- arbitrary untrusted server filesystem-path production route = `0`;
- controlled upload/quarantine/provenance = `PASS` fail-closed;
- cross-tenant unauthorized success in accepted regressions = `0`;
- authoritative replay/reconnect = `PASS`;
- cursor used as authorization authority = `0` under accepted cockpit/security regressions;
- telemetry outage corruption/blocking = `0`;
- static W004 cockpit used as production live truth = `0`;
- hard-gate compensation = `0`;
- production-ready claim = `NOT_AUTHORIZED`.

The A02 runtime/database/parser/frontend surfaces remain explicit reference/non-production evidence. `LockedFixturePdfAdapter` is integration-fixture evidence only and is not parser-quality evidence. No production runtime/database/parser/frontend/deployment/vendor winner is promoted by T009.

PR #227 merged into main as `aa9eab34a436c8e4eedc4e71df74e978083ba0d6`.

## W006-T011-A01 — READY

Dependencies `W006-T009` and `W006-T010` are now satisfied. T011 is READY for independent AI Runtime + Eval + FinOps work.

It must refresh provider/model/pricing/lifecycle facts and run representative same-corpus comparisons across eligible static candidates, deterministic cascades and learned shadow routing only where justified. Material provider/model/routing defaults require DRG-valid evidence; unresolved Pareto tradeoffs must remain unresolved rather than forcing a winner.

Hard boundaries include hard-gate violating output accepted for cost/latency = `0`, capability-ineligible fallback = `0`, blind retry of invalid auth/config/tenant/policy = `0`, accepted run missing policy/catalog/pricing identity = `0`, and critical-failure canary rollback = `PASS`.

## W006-T012-A01 — READY

Dependency `W006-T009` is now satisfied. T012 is READY in parallel with T011 for Observability + SRE + Security work.

It must integrate W3C propagation, OTel instrumentation, OTLP-compatible export, provider/eval/repair spans, bounded metrics, authorized cockpit trace links and backend comparison on the real workload while preserving the authoritative product-event plane independently from sampled telemetry.

Hard boundaries include raw credentials/secrets in telemetry = `0`, raw private content emitted by default = `0`, high-cardinality tenant/run/job IDs as default metric labels = `0`, controlled 9-branch traceability = `PASS`, telemetry backend/export outage leaving product path healthy, and no backend/collector topology promotion without evidence.

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
- `W006-T009-A01`: RESULT_RECEIVED / diagnostic-not-accepted;
- `W006-T009-A02`: INTEGRATED;
- `W006-T010-A01`: INTEGRATED foundation; empirical human evidence remains external/pending;
- `W006-T011-A01`: READY;
- `W006-T012-A01`: READY;
- `W006-T013-A01`: PLANNED, gated on T011+T012 in addition to accepted T009;
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
- accepted T009 end-to-end reference integration: yes, under frozen toolchain;
- production runtime/database lock: none;
- production parser winner: none;
- concrete frontend/framework winner: none;
- provider/model/routing winner: none yet from T011;
- deployment/observability/vendor winners: none;
- submission completed: not claimed.

## Current success bottlenecks

`W006-T011_PROVIDER_MODEL_ROUTING_EVIDENCE`

`W006-T012_OBSERVABILITY_SRE_SECURITY`

## Next action

Execute `W006-T011-A01` and `W006-T012-A01` in independent worker chats in parallel. T013 remains gated until both are accepted/integrated.

## Recovery point

Resume from STATE 0058. Ready queue: `W006-T011-A01`, `W006-T012-A01`. Blanket production readiness remains false.
