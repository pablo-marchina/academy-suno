# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0052`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W006-T005-A02-T010-A01-INTEGRATED-T007-READY`

## Objective

Implementar e qualificar o produto real multiusuário sob os contratos/evidências aceitos em W005, preservando hard gates determinísticos e usando adaptação somente onde evidence-backed.

## Preserved truth

- W004 permanece baseline/evidência histórica e não autoriza production readiness.
- W005 permanece autoridade de planejamento/arquitetura, não prova de production readiness.
- human gold/agreement/preference empíricos continuam não observados; production audience thresholds permanecem `DIAGNOSTIC_ONLY` até independent human calibration + HELD_OUT replication.
- external deadline, submission mechanism, named Suno owner/internal workflow, SSO/SCIM/procurement/residency e ROI baseline permanecem `UNKNOWN` salvo futura evidência externa.
- escolhas `NO_PREFERENCE/PENDING_EVIDENCE` não viram winners por conveniência durante implementação.

## W006 accepted foundation through STATE 0051

- `W006-T001-A02`: versioned tenant/resource/command/state/event/replay/provenance/persistence/telemetry contracts + globally unique `dr://DR-####` registry; no unresolved technology winner.
- `W006-T002-A01`: portable identity/tenancy/session/SSE security substrate; defined cross-tenant/revocation/cursor/canary hard gates pass; infrastructure vendors remain open.
- `W006-T003-A01`: durable state↔event reference semantics + common failure harness `14/14 PASS`; SQLite remains reference-only, not production authority.
- `W006-T004-A01`: controlled upload/quarantine/provenance + parser/OCR evidence; decision remains `NO_PRODUCTION_PARSER_WINNER`.
- `W006-T006-A01`: authenticated live-cockpit projection/replay/security mechanics; concrete frontend/editor framework remains evidence-gated.

## W006-T005-A01 — BLOCKED DIAGNOSTIC

A01 remains immutable blocked evidence. Its worker environment could not install/resolve challenger runtimes and correctly refused documentation-only substitution. It selected no runtime winner.

## W006-T005-A02 — ACCEPTED / INTEGRATED

Dependency-capable runtime/shared-state comparative evidence is accepted via PR #213 / merge `d9ba7f688b75162ed2929ee776caeabc691bf99a`.

Accepted evidence:

- valid lifecycle/provenance with `CONTINUITY_CHECK: PASS`;
- RESULT `SYSTEM/RESULTS/W006-T005-A02.md` at `157ca304ec26585c5ea9bd55af19c5e750d08192`;
- executed minimum comparative set: custom/CAS control, LangGraph `1.2.12` + checkpoint-sqlite `3.1.1`, DBOS `2.31.0`;
- accepted T003 semantic floor `14/14 PASS`;
- exact accepted branch membership `9/9` for all three candidates;
- accepted join loss = `0`, accepted join duplication = `0`, duplicate accepted output = `0`, stale/late overwrite = `0`, uncommitted event acceptance = `0` in defined scenarios;
- restart/resume/replay = `100% PASS` in the defined harness;
- real separate-process crash after provider-side effect and fresh-process recovery executed for every candidate;
- duplicate provider-side attempts persisted raw instead of hidden; externally billed provider cost remains `NOT_OBSERVED`;
- RESULT-bearing `System Integrity` run `35809922455`: success;
- RESULT-bearing `Foundation Regression` run `35809922459`: success;
- task workflow `W006 T005 A02 Runtime Bakeoff` run `35809922476`: success.

Decision boundary:

- local declared-objective point Pareto set is `[custom_cas]` for this hosted-runner/SQLite-backed benchmark only;
- `DECISION_STATE: PENDING_EVIDENCE`;
- `PRODUCTION_RUNTIME_LOCK: NONE`;
- `PRODUCTION_DATABASE_LOCK: NONE`;
- production-topology/multi-replica/failover/network-partition/saturation/ops/security/cost evidence remains missing;
- Temporal remains an open conditional challenger where production-topology hypotheses justify it.

The local Pareto singleton is explicitly not a production winner.

## W006-T010-A01 — ACCEPTED / INTEGRATED FOUNDATION

Evaluation/human-calibration foundation is accepted via PR #212 / merge `feb9412011a1fc35d41f524a8295ac45a71e68c7`.

Accepted foundation evidence:

- valid lifecycle/provenance with `CONTINUITY_CHECK: PASS`;
- RESULT `SYSTEM/RESULTS/W006-T010-A01.md` at `f229b723380b7696903ff4b48a5d7911aec01b1d`;
- versioned DEV/CALIBRATION/HELD_OUT partitions at `source_group_id` granularity;
- 3×3 siblings and parser-derived variants do not inflate independent source N;
- blind dual-primary human annotation + triggered distinct adjudication contract;
- model-generated/automated labels structurally excluded from human-evidence classes;
- secondary judge calibration requires independent human reference and cannot override critical hard gates;
- paired baseline/candidate contract requires same dataset version, exact source_group×audience×format pairing, source-group clustering, fail-closed missing pairs, no scalar compensation and no HELD_OUT tuning;
- local foundation validation `36/36 PASS`, unit tests `5/5 PASS`;
- model-only label accepted as human gold = `0`;
- hard-gate compensation paths = `0`;
- RESULT-bearing `System Integrity` run `35809640984`: success;
- RESULT-bearing `Foundation Regression` run `35809640964`: success.

Evidence boundary remains explicit:

- independent human primary streams observed = `0`;
- adjudicated human-gold items observed = `0`;
- HELD_OUT replication = `NOT_RUN`;
- empirical agreement/kappa/confusion/judge-vs-human performance is not claimed;
- audience thresholds remain `DIAGNOSTIC_ONLY`;
- actual human annotation/qualification/budget/retention remain external evidence dependencies.

Acceptance of T010 means the foundation contracts are valid and executable; it does not mean human calibration has been empirically completed.

## W006-T007-A01 — READY

All dependencies T002–T006 now have accepted/integrated attempts, so the original `W006-T007-A01` is READY.

Its original provenance remains `STATE 0047 / 0fa1fd46d02d8fb2ad3410823ba417d83b596eac`. Worker must preserve that provenance and run `CONTINUITY_CHECK` against STATE 0052/current main before substantive work.

T007 must fan in the Phase 9 substrate evidence using the Decision Research Gate and W005 benchmark v002. It must preserve `NO_PREFERENCE/PENDING_EVIDENCE` where evidence is insufficient or alternatives are incomparable. In particular:

- the T005 local `[custom_cas]` point Pareto singleton cannot be promoted to a production runtime/database lock without representative production-topology evidence;
- T004 remains `NO_PRODUCTION_PARSER_WINNER`;
- concrete frontend/editor, infrastructure, deployment, observability-backend and package-manager choices remain evidence-gated unless exact new evidence closes them;
- material winner lacking exact DR evidence = `0`;
- hard-gate violator eligible = `0`;
- unsupported scalar utility = `0`;
- W005-T011/T012 correction contracts remain binding.

## W006 dependency gates

- `W006-T001-A02`: INTEGRATED;
- `W006-T002-A01`: INTEGRATED;
- `W006-T003-A01`: INTEGRATED;
- `W006-T004-A01`: INTEGRATED;
- `W006-T005-A02`: INTEGRATED;
- `W006-T006-A01`: INTEGRATED;
- `W006-T007-A01`: READY;
- `W006-T010-A01`: INTEGRATED foundation, with human evidence still external/pending;
- `W006-T008-A01`: PLANNED, gated on T007;
- `W006-T009-A01`: PLANNED, gated on T007+T008;
- `W006-T011-A01`: PLANNED, T010 dependency satisfied but still gated on T009;
- `W006-T012-A01`: PLANNED, gated on T009;
- `W006-T013-A01`: PLANNED, gated on T009+T011+T012;
- `W006-T014-A01`: PLANNED, T010 dependency satisfied but still gated on T011+T013.

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

Quality/audience/latency/cost/capacity/retention/sampling/SLO/RTO/RPO numeric thresholds remain evidence/external-owner gated unless representative evidence supports them.

## Evidence boundary

- production-ready claim: `FALSE`;
- human gold: not observed;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- production runtime/database lock: none;
- production parser winner: none;
- concrete frontend/framework winner: none;
- submission completed: not claimed.

## Current success bottleneck

`W006-T007_PHASE9_SUBSTRATE_EVIDENCE_FANIN`

## Next action

Execute `W006-T007-A01` in an independent worker chat. Downstream T008 remains gated until T007 is accepted/integrated.

## Recovery point

Resume from STATE 0052. Ready queue: `W006-T007-A01`. Blanket production readiness remains false.