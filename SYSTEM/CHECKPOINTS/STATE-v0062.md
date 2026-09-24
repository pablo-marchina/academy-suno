# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0062`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W007-PLANNED-T001-T004-T005-READY`

## Objective

Close the 16 production blockers identified by the independent W006-T014 audit using representative deployed evidence without relaxing deterministic hard gates or manufacturing technology/evidence winners.

## Canonical authority entering W007

- W006 is complete only for `EVIDENCE_COMPLETE_FOR_ACHIEVED_REFERENCE_SCOPE`.
- T014 audit authority: `artifacts/w006-t014/a01/audit-matrix.json` and `artifacts/w006-t014/a01/EVIDENCE_MANIFEST.md`.
- Current Production Contract classification: `17/17` audited, `1/17` full-production PASS (`PROD-015`), `16/17` `PRODUCTION_UNKNOWN/BLOCKER`.
- Production readiness remains `FALSE / NOT_AUTHORIZED`.
- W005-T009-A02 benchmark methodology remains authoritative: non-compensatory hard gates → raw multidimensional metrics → uncertainty/missingness → point Pareto; scalar business utility requires representative human/business evidence and stable sensitivity.
- `SYSTEM/DECISION_RESEARCH_GATE.md` applies to every material production technology/default decision.
- Frozen current Python graph remains Python `3.13.15` + `uv@0.12.18` + committed `pyproject.toml`/`uv.lock` unless separately research-gated.

## W007 execution graph

### READY now — independent fan-out

- `W007-T001-A01` — production topology candidates + representative qualification protocol. Issue #236.
- `W007-T004-A01` — source-original financial parser/OCR production qualification. Issue #239.
- `W007-T005-A01` — independent human calibration + adjudication + HELD_OUT. Issue #240. If real independent humans are unavailable, the correct terminal state is `TASK_BLOCKED`; simulated/LLM records cannot substitute for human gold.

### Gated fan-in / downstream

- `W007-T002-A01` depends T001 — representative deployed topology bakeoff + substrate lock/no-preference.
- `W007-T003-A01` depends T002 — production identity/session/object/secret/IAM adapters + security qualification.
- `W007-T006-A01` depends T004+T005 — fresh current provider/model paired benchmark + routing/default decision.
- `W007-T007-A01` depends T002+T003 — concrete production frontend/live cockpit + observability backend integration.
- `W007-T008-A01` depends T002+T003+T004+T006+T007 — single full deployed production integration path.
- `W007-T009-A01` depends T008 — deployed security/SRE/capacity/recovery/migration/rollback qualification.
- `W007-T010-A01` depends T005+T009 — independent final production audit + <=5:00 same-path technical video.

## Blocker groups W007 must close or preserve explicitly

1. representative production runtime/shared persistence/event/deployment topology plus migration/rollback;
2. production identity/session/object-storage/scanning/secret/IAM controls;
3. source-original parser/OCR production evidence;
4. independent human calibration, adjudicated gold and HELD_OUT;
5. fresh representative current provider/model evidence and any adaptive routing policy;
6. concrete production frontend/live cockpit and observability backend/topology;
7. deployed production security/reliability/capacity/recovery evidence, including measured saturation and only evidence-backed SLO/RTO/RPO/capacity claims.

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

## Evidence boundary at W007 start

- human primary streams observed = `0`; adjudicated human gold = `0`; HELD_OUT = `NOT_RUN`; thresholds = `DIAGNOSTIC_ONLY`;
- fresh current-provider representative comparison = `NOT_RUN`; `PARETO_NOT_COMPUTABLE`; provider/model/routing = `NO_PREFERENCE`;
- production runtime/database/deployment lock = none;
- production parser/OCR winner = none;
- concrete production frontend/observability backend winner = none;
- deployed production migration/rollback qualification = missing;
- production SLO/RTO/RPO/supported-user evidence = missing;
- production-ready claim = `FALSE / NOT_AUTHORIZED`.

## Current success bottleneck

`W007_T001_T004_T005_PARALLEL_EVIDENCE_ACQUISITION`

## Next action

Kick off W007-T001-A01, W007-T004-A01 and W007-T005-A01 in independent worker chats after canonical STATE 0062 is merged. Do not start downstream tasks early.

## Recovery point

Resume from STATE 0062. Ready queue: `W007-T001-A01`, `W007-T004-A01`, `W007-T005-A01`. Production readiness remains false.
