# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0053`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W006-T007-INTEGRATED-T008-READY`

## Objective

Implementar e qualificar o produto real multiusuário sob os contratos/evidências aceitos em W005, preservando hard gates determinísticos e usando adaptação somente onde evidence-backed.

## Preserved truth

- W004 permanece baseline/evidência histórica e não autoriza production readiness.
- W005 permanece autoridade de planejamento/arquitetura, não prova de production readiness.
- human gold/agreement/preference empíricos continuam não observados; production audience thresholds permanecem `DIAGNOSTIC_ONLY` até independent human calibration + HELD_OUT replication.
- escolhas `NO_PREFERENCE/PENDING_EVIDENCE` não viram winners por conveniência durante implementação.
- production-ready claim permanece `FALSE`.

## W006 accepted substrate through STATE 0052

- `W006-T001-A02`: contratos versionados de tenant/resource/command/state/event/replay/provenance/persistence/telemetry + registry `dr://DR-####`.
- `W006-T002-A01`: invariantes portáveis de identity/tenancy/session/SSE security aceitos; vendors permanecem abertos.
- `W006-T003-A01`: durable state↔event reference semantics + common failure harness `14/14 PASS`; SQLite continua reference-only.
- `W006-T004-A01`: controlled ingestion/quarantine/provenance aceito; parser/OCR permanece `NO_PRODUCTION_PARSER_WINNER`.
- `W006-T005-A02`: custom/CAS + LangGraph + DBOS executados no 3×3 com hard gates PASS; local point Pareto `[custom_cas]`, mas production runtime/database continuam `PENDING_EVIDENCE` / sem lock.
- `W006-T006-A01`: authoritative live-cockpit snapshot/event/replay/security mechanics aceitos; concrete frontend/editor permanece evidence-gated.
- `W006-T010-A01`: eval/human-calibration foundation aceita; independent human streams = `0`, adjudicated human gold = `0`, HELD_OUT = `NOT_RUN`, thresholds = `DIAGNOSTIC_ONLY`.

## W006-T007-A01 — ACCEPTED / INTEGRATED

Production substrate evidence fan-in integrado via PR #216 / merge `b665f62a78ff39a7cc6bbc29f7c07fad6d562d1f`.

Accepted evidence:

- valid lifecycle/provenance with `CONTINUITY_CHECK: PASS`;
- RESULT `SYSTEM/RESULTS/W006-T007-A01.md` at `9412256cc896eff331c8c6001199f2ef7f5d6273`;
- decision fan-in `docs/production/W006_T007_PRODUCTION_SUBSTRATE_DECISION_FANIN.md`;
- RESULT-bearing `System Integrity` run `35866254381`: success;
- material production/default winner lacking exact DR evidence = `0`;
- hard-gate violator retained as eligible = `0`;
- unsupported scalar utility = `0`;
- T005 local `[custom_cas]` Pareto point converted into production lock = `0`;
- SQLite reference converted into production database lock = `0`;
- unsupported parser/frontend/infrastructure/deployment/observability/package-manager winner = `0`;
- W005-T011/T012 corrections weakened = `0`.

Carried authority is limited to evidence-backed contracts/invariants, including typed/versioned HTTP/OpenAPI, SSE+durable replay/snapshot boundary, server-side authz/redaction, stable tenant/provenance identity, state↔event consistency, CAS/ownership/stale-write rejection, at-least-once execution with idempotent authoritative acceptance, fail-closed document ingestion, exact 3×3 branch identity/lossless join, and authoritative live-cockpit snapshot/event projection.

Explicitly unresolved after T007:

- production workflow/runtime: `PENDING_EVIDENCE`;
- production database/shared-state: `PENDING_EVIDENCE`;
- production parser/OCR: `NO_PRODUCTION_PARSER_WINNER`;
- frontend framework/editor: `PENDING_EVIDENCE`;
- identity/data/object infrastructure vendors: `NO_PREFERENCE/PENDING_EVIDENCE`;
- observability backend/sampling/retention: `NO_PREFERENCE/PENDING_EVIDENCE`;
- deployment/cloud/runtime class: `NO_PREFERENCE`;
- package managers/task graph/repository topology: `PENDING_EVIDENCE`;
- SLO/capacity/RTO/RPO numeric targets and scalar business utility: `PENDING_EVIDENCE`.

`PRODUCTION_READY_FROM_T007: FALSE`.

## W006-T008-A01 — READY

T007 is accepted/integrated, so `W006-T008-A01` is READY.

Original provenance remains `STATE 0047 / 0fa1fd46d02d8fb2ad3410823ba417d83b596eac`; worker must continuity-check against STATE 0053/current main before substantive work.

T008 must benchmark/freeze the reproducible developer/release toolchain only from the actual repository/dependency graph. It must preserve T007's evidence boundaries and must not use package-manager familiarity or repository-topology preference as a substitute for measured need.

Hard acceptance remains:

- clean locked install/build/test PASS;
- movable third-party release Actions = `0`;
- unnecessarily broad release token permissions = `0`;
- releasable artifact has verifiable SBOM + provenance/attestation;
- repository migration occurs only with DRG evidence.

## W006 dependency gates

- `W006-T001-A02`: INTEGRATED;
- `W006-T002-A01`: INTEGRATED;
- `W006-T003-A01`: INTEGRATED;
- `W006-T004-A01`: INTEGRATED;
- `W006-T005-A02`: INTEGRATED;
- `W006-T006-A01`: INTEGRATED;
- `W006-T007-A01`: INTEGRATED;
- `W006-T008-A01`: READY;
- `W006-T009-A01`: PLANNED, gated on T008 in addition to integrated T007;
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
- submission completed: not claimed.

## Current success bottleneck

`W006-T008_REPRODUCIBLE_TOOLCHAIN_AND_SUPPLY_CHAIN_FREEZE`

## Next action

Execute `W006-T008-A01` in an independent worker chat. T009 remains gated until T008 is accepted/integrated.

## Recovery point

Resume from STATE 0053. Ready queue: `W006-T008-A01`. Blanket production readiness remains false.
