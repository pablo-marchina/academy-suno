# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0051`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W006-T002-T004-T006-INTEGRATED-T005-A02-T010-READY`

## Objective

Implementar e qualificar o produto real multiusuário sob os contratos/evidências aceitos em W005, preservando hard gates determinísticos e usando adaptação somente onde evidence-backed.

## Preserved truth

- W004 permanece baseline/evidência histórica e não autoriza production readiness.
- W005 está complete/accepted como autoridade de planejamento para implementação; não constitui prova de production readiness.
- human gold/agreement/preference continuam não observados; production audience thresholds permanecem `DIAGNOSTIC_ONLY` até evidência humana independente + held-out replication.
- external deadline, submission mechanism, named Suno owner/internal workflow, SSO/SCIM/procurement/residency e ROI baseline permanecem `UNKNOWN` salvo futura evidência externa.
- escolhas `NO_PREFERENCE/PENDING_EVIDENCE` não viram winners por conveniência durante implementação.

## W006-T001 — ACCEPTED FOUNDATION

`W006-T001-A02` permanece accepted/integrated desde STATE 0050. Seus contratos versionados de tenant/resource/command/state/event/replay/provenance/persistence/telemetry e o registry `dr://DR-####` continuam autoridade de boundary para as tasks downstream. Isso não seleciona database, workflow runtime, parser/OCR, provider/model, frontend framework, observability backend, deployment class ou package manager.

## W006-T002-A01 — ACCEPTED / INTEGRATED

Identity/tenancy/session/SSE security substrate integrado via PR #207 / merge `410e75c2cfe8407e6b42b37ba4687a2cfe8b0da8`.

Evidence accepted:

- valid lifecycle/provenance with `CONTINUITY_CHECK: PASS`;
- RESULT `SYSTEM/RESULTS/W006-T002-A01.md` at `4141c9583a7923a74637ac6df061672f60cf76e6`;
- defined adversarial suite `12/12 PASS` locally;
- RESULT-bearing `System Integrity` run `35802692868`: success;
- RESULT-bearing `Foundation Regression` run `35802692787`: success;
- defined cross-tenant unauthorized success across API/data/object/event/trace = `0`;
- revoked session/membership resume success = `0`;
- prior-tenant access after org/workspace switch = `0`;
- cross-tenant cursor replay success = `0`;
- credential-canary leakage = `0`.

Boundary: in-process directory/cursor vault is reference/security-harness evidence only. IdP, durable session store, data/RLS substrate, object store, durable cursor/event backend and deployment IAM remain evidence-gated.

## W006-T003-A01 — ACCEPTED / INTEGRATED

Durable state↔event reference substrate + common failure harness integrado via PR #209 / merge `cf5413ddf5d888b34278114d6e02ddc078f32fb3`.

Evidence accepted:

- valid lifecycle/provenance with `CONTINUITY_CHECK: PASS`;
- RESULT `SYSTEM/RESULTS/W006-T003-A01.md` at `06ed75554717ffaa7c59b279e449f55a4e058e99`;
- common failure harness `14/14 PASS`;
- silent stale same-run overwrite = `0`;
- permanent logical event gap after reconciliation = `0`;
- event without authoritative committed transition = `0`;
- duplicate logical projection = `0`;
- cross-tenant replay success = `0`;
- defined restart/replay/repair = `100% PASS`;
- defined backup/restore = `100% PASS`;
- RESULT-bearing `System Integrity` run `35802838755`: success;
- RESULT-bearing `Foundation Regression` run `35802838738`: success.

Boundary: SQLite is an executable reference candidate only. No distributed production database/event/workflow technology winner is inferred.

## W006-T004-A01 — ACCEPTED / INTEGRATED

Controlled upload/quarantine + parser/OCR bakeoff integrado via PR #210 / merge `4fe5a40250d0eb5dda65876835df58c1b49d0cba`.

Evidence accepted:

- valid lifecycle/provenance with `CONTINUITY_CHECK: PASS`;
- RESULT `SYSTEM/RESULTS/W006-T004-A01.md` at `f7f00425b60844567026cb9401b10e7131d54238`;
- controlled PDF preflight/quarantine with immutable SHA-256 provenance and source-group accounting;
- encrypted/malformed variants quarantined before parser in the observed harness = `4/4`;
- benchmark result rows with source-group identity + SHA = `20/20`;
- accepted evidence missing required source hash/provenance = `0`;
- ambiguous table/OCR role promoted as trusted evidence = `0` by routing/tests;
- hard-gate eligibility + uncertainty + Pareto method preserved; arbitrary scalar utility = `0`;
- `System Integrity` run `35802830511`: success;
- `Foundation Regression` run `35802830495`: success.

Decision remains `NO_PRODUCTION_PARSER_WINNER`: source-original public-PDF bytes were not executed in this local bakeoff, source-group N was only 2, managed document-AI candidates were not executed, and the hard-gate eligible/Pareto set was empty. `pdfplumber` success on digital reconstructions is not a production parser lock.

## W006-T006-A01 — ACCEPTED / INTEGRATED

Authenticated same-slice live-cockpit bakeoff integrado via PR #208 / merge `7139b482a3e61e70b957a2573f11a1cbf7e0d3a5`.

Evidence accepted:

- valid lifecycle/provenance with `CONTINUITY_CHECK: PASS`;
- RESULT `SYSTEM/RESULTS/W006-T006-A01.md` at `72846aaf329df5393887b5a7d97b01b167217a22`;
- task-specific live-cockpit workflow run `35802941347`: success;
- `System Integrity` run `35802941260`: success;
- `Foundation Regression` run `35802941259`: success;
- canonical v1 command/event/authorized-stream contract is consumed by both tested rendering shells;
- live projection derives only from authoritative snapshot + accepted canonical events;
- static W004 recipient route is unavailable as fallback;
- cross-tenant source/event/trace projection success in defined tests = `0`;
- failed/review-required cells remain explicit;
- accessibility/dynamic-update assertions persisted.

Boundary: both shells are framework-neutral evidence candidates. Frontend/editor framework, package manager, runtime and deployment class remain evidence-gated.

## W006-T005-A01 — BLOCKED / NOT ACCEPTED

A01 started validly on Issue #192 and emitted terminal `TASK_BLOCKED` with RESULT `SYSTEM/RESULTS/W006-T005-A01.md` at `27b31c6caf3881321010a2ce05aadca818c27f74`.

Blocker is evidence-valid rather than a task failure disguised as success: the worker environment lacked `langgraph`, `dbos` and `temporalio`, and external package resolution failed with DNS errors. Because the dispatch explicitly required executed side-by-side common-workload evidence, A01 correctly refused to substitute documentation or framework reputation and selected no winner.

A01 is immutable blocked evidence and will not be reused.

## W006-T005-A02 — READY RETRY

Fresh retry dispatch: `SYSTEM/DISPATCH/W006-T005-A02.md`.

Retry provenance is `STATE 0050 / main 7139b482a3e61e70b957a2573f11a1cbf7e0d3a5`, representing the observed canonical state plus the four accepted sibling worker merges before STATE 0051 reconciliation.

A02 must use a dependency-capable execution path, with GitHub Actions clean-checkout execution as the default unblock path if suitable. It must pin exact challenger versions, execute the same Academy 3×3 workload and common failure matrix, persist raw per-candidate evidence, and keep any database/service container used by the harness explicitly benchmark-only rather than a production technology lock.

Minimum comparative set remains custom/CAS-capable control + LangGraph + DBOS. Temporal remains a challenger to execute when needed to close unresolved runtime hypotheses or when the minimum set cannot produce a valid decision surface. No documentation-only substitution and no convenience winner are allowed.

## W006-T010-A01 — READY

T001 and T004 are now accepted/integrated, so the original `W006-T010-A01` attempt becomes READY. Its original provenance remains `STATE 0047 / 0fa1fd46d02d8fb2ad3410823ba417d83b596eac`; worker must continuity-check against STATE 0051/current main before substantive work.

T010 may establish source-group partitions, human-calibration protocol/agreement/adjudication contracts, secondary judge calibration and paired experiment contracts. Actual independent human annotation remains an external evidence dependency if unavailable; automated/model-only labels must never be called human gold and audience thresholds remain `DIAGNOSTIC_ONLY` until independent calibration + held-out replication.

## W006 dependency gates

- `W006-T002-A01`: INTEGRATED;
- `W006-T003-A01`: INTEGRATED;
- `W006-T004-A01`: INTEGRATED;
- `W006-T005-A02`: READY retry;
- `W006-T006-A01`: INTEGRATED;
- `W006-T007-A01`: still PLANNED/gated only on accepted T005 in addition to the four already accepted siblings;
- `W006-T010-A01`: READY;
- downstream tasks remain dependency-gated by `SYSTEM/WAVES/W006.json`.

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

- W005: complete/accepted as implementation authority;
- W006-T001-A02/T002-A01/T003-A01/T004-A01/T006-A01: accepted/integrated task evidence;
- W006-T005-A01: valid BLOCKED diagnostic, not accepted dependency;
- W006-T005-A02: READY;
- W006-T010-A01: READY;
- production-ready claim: `FALSE`;
- human gold: not observed;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- runtime/database/parser/frontend vendor winners: not inferred beyond exact evidence-backed invariants;
- submission completed: not claimed.

## Current success bottleneck

`W006-T005-A02_RUNTIME_BAKEOFF_AND_W006-T010_HUMAN_CALIBRATION_FOUNDATION`

## Next action

Run `W006-T005-A02` and `W006-T010-A01` in independent worker chats. T007 unlocks only after an accepted T005 retry; T010 can proceed independently now.

## Recovery point

Resume from STATE 0051. Ready queue: `W006-T005-A02`, `W006-T010-A01`. Blanket production readiness remains false.