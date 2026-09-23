# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0057`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W006-T009-A01-REJECTED-TOOLCHAIN-BYPASS-A02-READY`

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
- accepted toolchain constraint for the current single-project Python graph is Python `3.13.15` + `uv@0.12.18` + committed `pyproject.toml`/`uv.lock`; broader runtime/database/parser/frontend/deployment/vendor decisions remain open/evidence-gated.

## W006-T009-A01 — COMPLETE BUT NOT ACCEPTED

A01 ran with valid lifecycle from original provenance STATE 0047 / `0fa1fd46d02d8fb2ad3410823ba417d83b596eac` after `CONTINUITY_CHECK: PASS` against STATE 0056 / main `975009cae927a952589e1a757f77f4097054a524`.

It persisted `SYSTEM/RESULTS/W006-T009-A01.md` at `b21d690f64814e6673dad0ddca6de108381ac82f`, opened PR #225, and produced green final-head CI:

- W006 T009 Vertical Slice `35898275855`: SUCCESS;
- System Integrity `35898275841`: SUCCESS;
- Foundation Regression `35898276258`: SUCCESS;
- W006 T008 Supply Chain `35898276199`: SUCCESS.

A01 produced useful reference integration evidence: controlled PDF bytes upload/provenance, exact durable 3×3 fan-out, pause/resume, branch-local retry/repair isolation, authoritative state/event replay, telemetry-outage isolation and backup/restore mechanics. Its local/plain-async/SQLite/pypdf/projector adapters were explicitly marked reference/non-production, and no production-ready claim was made.

A01 is **not accepted/integrated** because its dedicated clean-checkout workflow bypassed the accepted T008-A03 toolchain constraint carried by STATE 0056 and Issue #196. `.github/workflows/w006-t009-vertical-slice.yml` used `actions/setup-python@v5` with `python-version: '3.13'` and installed a hand-selected subset via `python -m pip install`, rather than proving the vertical slice from exact Python `3.13.15` + `uv@0.12.18` + committed `pyproject.toml`/`uv.lock` using the frozen dependency graph. Therefore green A01 CI is not accepted proof under the canonical toolchain.

PR #225 is closed without merge. A01 remains immutable diagnostic/reference evidence only.

## W006-T009-A02 — READY

Fresh retry A02 is READY on `worker/W006-T009-A02`.

Base provenance is `STATE 0056 / 975009cae927a952589e1a757f77f4097054a524`. Before substantive work the worker must continuity-check against STATE 0057/current main, use a fresh A02 branch, emit exactly one protocol-valid `TASK_STARTED`, persist its own RESULT/evidence, then emit exactly one terminal signal.

A02 may reuse A01 only as diagnostic implementation input. It must independently prove the same real product path under the accepted frozen toolchain. Its clean-checkout validation must use exact Python `3.13.15`, exact `uv@0.12.18`, committed `pyproject.toml` and `uv.lock`, fail if the lock is stale, and execute the task/regression tests from that locked environment rather than a hand-selected direct-pip dependency subset.

A02 must preserve the same product-path hard gates:

- same real path, not a parallel/disposable demo: auth → workspace → controlled PDF bytes upload/quarantine/provenance → parse/trust boundary → durable exact 3×3 workflow → eval/repair → aggregate → durable authoritative product/domain events → live cockpit;
- accepted provenance missing = `0`;
- exact branch coverage = `9/9`;
- accepted branch loss/duplication = `0`;
- silent stale overwrite accepted = `0`;
- duplicate accepted retry/republication output = `0`;
- arbitrary untrusted server filesystem-path production route = `0`;
- cross-tenant unauthorized success in defined regressions = `0`;
- replay/reconnect = `PASS`;
- cursor never acts as authorization authority;
- telemetry outage corruption/blocking of authoritative product state = `0`;
- static W004 cockpit used as production live truth = `0`;
- runtime/database/parser/frontend/deployment/vendor winner manufactured without compliant evidence = `0`;
- production-ready claim = `NOT_AUTHORIZED`.

If A02 introduces any new material technology default beyond the accepted T008 toolchain, the Decision Research Gate applies; otherwise it must keep unresolved technology boundaries open.

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
- `W006-T009-A02`: READY;
- `W006-T010-A01`: INTEGRATED foundation; empirical human evidence remains external/pending;
- `W006-T011-A01`: PLANNED, T010 satisfied but gated on an accepted T009 attempt;
- `W006-T012-A01`: PLANNED, gated on an accepted T009 attempt;
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
- accepted T009 production vertical slice: none yet;
- submission completed: not claimed.

## Current success bottleneck

`W006-T009_A02_VERTICAL_SLICE_UNDER_FROZEN_TOOLCHAIN`

## Next action

Execute `W006-T009-A02` in an independent worker chat. T011 and T012 remain gated until a T009 attempt is accepted/integrated.

## Recovery point

Resume from STATE 0057. Ready queue: `W006-T009-A02`. Blanket production readiness remains false.
