# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0063`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W007-T001-T004-INTEGRATED-T005-BLOCKED-T002-READY`

## Objective

Close the production blockers identified by the independent W006-T014 audit using representative deployed evidence without relaxing deterministic hard gates or manufacturing technology/evidence winners.

## Preserved authority

- W006 remains complete only for `EVIDENCE_COMPLETE_FOR_ACHIEVED_REFERENCE_SCOPE`; its final audit remains the blocker authority via `artifacts/w006-t014/a01/audit-matrix.json` and `EVIDENCE_MANIFEST.md`.
- Production Contract classification remains `17/17` audited, with only `PROD-015` full-production PASS at the W007 entry boundary and the other rows requiring production evidence.
- W005-T009-A02 `W005-BENCHMARK-METHODOLOGY-V002` remains binding: non-compensatory hard gates → raw multidimensional metrics → uncertainty/missingness → point Pareto. Scalar business utility requires representative human/business evidence and stable sensitivity.
- `SYSTEM/DECISION_RESEARCH_GATE.md` applies to every material production technology/default decision.
- Frozen current Python graph remains Python `3.13.15` + `uv@0.12.18` + committed `pyproject.toml`/`uv.lock` unless separately research-gated.
- production readiness remains `FALSE / NOT_AUTHORIZED`.

## W007-T001-A01 — ACCEPTED / INTEGRATED

T001 completed valid lifecycle from original provenance STATE 0061 / `3146b06323f8b15a6feef2ae2e6802d7fb7cafef` after `CONTINUITY_CHECK: PASS` against STATE 0062 / `6fbe0cd430a5c9090b92eb8d555d1cf0bd5fdb45`. It emitted exactly one `TASK_STARTED` and one terminal `TASK_COMPLETE`; terminal/result head is `0a18fa71a53273bee6ef44f547785a564b992552`.

PR #248 changed only six task-owned research/qualification files, had final-head `System Integrity` PASS run `36044342091`, and was merged by the Orchestrator as `97b26c8d151330eec23a09438dd802db8a84d022`.

Accepted outcome:

- baseline + three materially different topology classes advance to deployed comparison: Cloud Run + Cloud SQL, ECS Fargate + RDS PostgreSQL, and GKE Autopilot + Cloud SQL;
- exact shared qualification protocol covers multi-replica durability, ownership/fencing/idempotency, backpressure/load, failure/restart, backup/PITR restore, migration/rollback, security, observability, operations and cost;
- `DECISION_STATE: PENDING_DEPLOYED_EVIDENCE`;
- `PRODUCTION_TOPOLOGY_LOCK: NONE`;
- documentation/capability research is not treated as production performance evidence.

This acceptance closes qualification-plan ambiguity only. It does not close the production topology blocker. `W007-T002-A01` is now READY to execute the representative deployed comparison.

## W007-T004-A01 — ACCEPTED / INTEGRATED

T004 completed valid lifecycle from the same STATE 0061 provenance after `CONTINUITY_CHECK: PASS` against STATE 0062. It emitted exactly one `TASK_STARTED` and one terminal `TASK_COMPLETE`; terminal/result head is `c50c2ce59c8beeb74de7da04e17263d236f452de`.

PR #247 changed only task-owned parser qualification code/evidence plus its dedicated workflow. On the terminal head, `System Integrity` run `36044886091`, `Foundation Regression` run `36044886074`, and `W007 T004 Parser Qualification` run `36044886075` all completed SUCCESS. PR #247 was merged by the Orchestrator as `4ce2722b66c79bee2decbc3301911acb97bab8a3`.

Accepted evidence boundary:

- three hashed source-original public-financial groups executed: Petrobras 2T26, Banco Central RPM 1T26 and FRASER Federal Reserve 1914;
- five materially different local paths executed with repeated observations: pypdf, pdftotext, PyMuPDF tables, pdfplumber tables and Tesseract OCR;
- PyMuPDF alone passed the bounded Petrobras table-role hard gate, but only as a diagnostic bounded-slice point-Pareto member;
- accepted source missing hash/provenance = `0`, ambiguous OCR/table role promoted trusted = `0`, quarantined/unsupported promoted trusted generation = `0`;
- a genuine source-original pure image-only slice, managed document-AI executions, structured table/cell provenance through the production ingestion contract, and total compute-cost evidence remain missing;
- production Pareto remains `PARETO_NOT_COMPUTABLE` and governed decision remains `NO_PREFERENCE/PENDING_EVIDENCE`;
- production parser/OCR lock remains unauthorized.

T004 is accepted as bounded, truthful qualification evidence; its missingness remains an explicit production blocker and may not be converted into a parser winner.

## W007-T005-A01 — VALID BLOCKED TERMINAL ATTEMPT

T005 emitted one valid `TASK_STARTED` followed by exactly one terminal `TASK_BLOCKED`, preserving STATE 0061 provenance and `CONTINUITY_CHECK: PASS`. Result commit is `06995b5cadf8f219aee90e301db2db80708af82b`. Comparison against the readiness base shows only two task-owned files: `SYSTEM/RESULTS/W007-T005-A01.md` and `artifacts/w007-t005/a01/human-evidence-blocker.json`.

The blocker is external and binding: this environment has no access to two actual independent blinded human primary annotators per item plus a distinct actual human adjudicator. Model/LLM substitution is forbidden and no human record was fabricated.

Therefore:

- independent human primary streams observed = `0`;
- adjudicated human gold = `0`;
- agreement/calibration statistics = `NOT_COMPUTABLE`;
- HELD_OUT human replication = `NOT_RUN`;
- audience/tone/factuality/domain thresholds remain `DIAGNOSTIC_ONLY`;
- `W007-T006-A01` remains dependency-gated;
- any retry of T005 requires a fresh attempt ID only after real independent human annotation/adjudication capability exists.

## W007 execution graph after fan-in

### READY now

- `W007-T002-A01` — representative deployed topology bakeoff + substrate lock/no-preference. Depends on accepted T001.

### BLOCKED / gated

- `W007-T005-A01` — BLOCKED on real independent human annotators/adjudicator. Attempt is immutable.
- `W007-T003-A01` depends T002.
- `W007-T006-A01` depends accepted T004 plus a future successful fresh T005 attempt with real human evidence.
- `W007-T007-A01` depends T002+T003.
- `W007-T008-A01` depends T002+T003+T004+T006+T007.
- `W007-T009-A01` depends T008.
- `W007-T010-A01` depends human calibration evidence plus T009.

## Hard invariants

- hard-gate compensation = `0`;
- cross-tenant unauthorized success in defined tests = `0`;
- accepted required provenance missing = `0`;
- exact branch coverage = `9/9`;
- accepted join branch loss/duplication = `0`;
- critical schema violations promoted = `0`;
- silent stale same-run overwrite = `0`;
- duplicate accepted branch output = `0`;
- static/counterfactual evidence used as production live truth = `0`;
- arbitrary untrusted server filesystem-path production input = `0`;
- private quarantine bypass = `0`;
- secret/credential canary leakage = `0`;
- defined restart/resume = `100% PASS` before production claim;
- defined backup/restore = `100% PASS` before production claim;
- final technical video = `<=5:00`.

## Evidence boundary at STATE 0063

- production-ready claim = `FALSE / NOT_AUTHORIZED`;
- production topology lock = none; T001 is planning/qualification authority only;
- production parser/OCR winner = none; T004 remains `NO_PREFERENCE/PENDING_EVIDENCE`;
- real human calibration = blocked; human gold remains absent and thresholds remain `DIAGNOSTIC_ONLY`;
- fresh current provider/model representative comparison = not yet run;
- concrete production frontend/observability backend winner = none;
- deployed production migration/rollback, saturation, SLO/RTO/RPO and supported-user evidence remain missing.

## Current success bottleneck

`W007_T002_DEPLOYED_TOPOLOGY_EXECUTION_PLUS_EXTERNAL_HUMAN_CALIBRATION_BLOCKER`

## Next action

Kick off `W007-T002-A01` in an independent worker chat. In parallel, obtain access to real independent human annotators plus a distinct adjudicator before creating a fresh T005 attempt. Do not start T003/T006/T007/T008/T009/T010 early.

## Recovery point

Resume from STATE 0063. Ready queue: `W007-T002-A01`. T005-A01 is immutable BLOCKED. Production readiness remains false.
