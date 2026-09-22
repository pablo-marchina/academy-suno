# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0048`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 9 — Multi-user Production Foundation`

`LAST_COMMITTED_WAVE: W005-COMPLETE-W006-BOOTSTRAPPED-T001-READY`

## Objective

Implementar e qualificar o produto real multiusuário sob os contratos/evidências aceitos em W005, preservando hard gates determinísticos e usando adaptação somente onde evidence-backed.

## Preserved truth

- W004 permanece baseline/evidência histórica e não autoriza production readiness.
- W005 concluiu research → synthesis → independent red-team → final fan-in; sua conclusão autoriza implementação, não um claim de produção.
- human gold/agreement/preference continuam não observados; production audience thresholds permanecem `DIAGNOSTIC_ONLY` até evidência humana independente + held-out replication.
- external deadline, submission mechanism, named Suno owner/internal workflow, SSO/SCIM/procurement/residency e ROI baseline permanecem `UNKNOWN` salvo futura evidência externa.
- escolhas `NO_PREFERENCE/PENDING_EVIDENCE` não viram winners por conveniência durante implementação.

## W005 final fan-in — ACCEPTED / COMPLETE

`W005-T012-A01` completou lifecycle/provenance, `CONTINUITY_CHECK: PASS`, RESULT e PR #187. System Integrity run `35741191725` passou antes da integração.

Accepted artifacts:
- `SYSTEM/RESULTS/W005-T012-A01.md`;
- `docs/production/W005_FINAL_FANIN_PHASE9_IMPLEMENTATION_PLAN.md`.

T012 corrige a autoridade de T010/T011:
- repository topology permanece `PENDING_EVIDENCE`; lock somente `NO_REPOSITORY_MIGRATION_WITHOUT_EVIDENCE`;
- state ↔ durable product-event consistency exige atomicidade/outbox ou reconciliação determinística equivalente + failure injection;
- static W004 cockpit é `DIAGNOSTIC_ONLY / COUNTERFACTUAL`, nunca production/final-evidence fallback;
- SSE permanece default one-way browser transport condicionado a auth/resume/revocation/org-switch/cross-tenant-cursor tests;
- bare ambiguous DR IDs não são autoridade; exact repo-relative decision refs são obrigatórios até normalização global;
- observability lock é estreito: W3C + OTel semantic/instrumentation + OTLP-compatible export boundary;
- provider/job execution assume at-least-once remote execution + idempotent local acceptance com immutable attempts/late-result handling/duplicate-cost accounting;
- event cursor é autorizado junto de tenant/resource/run stream.

`PRODUCTION_PASS_COUNT_FROM_T012: 0`.

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

## W006 — Phase 9 implementation wave MATERIALIZED

Canonical wave: `SYSTEM/WAVES/W006.json`.

- `W006-T001` / #188 — contract/schema + DR traceability normalization — `READY`;
- `W006-T002` / #189 — identity/tenancy/session/SSE security substrate — `PLANNED`, depends T001;
- `W006-T003` / #190 — durable state↔event consistency substrate + failure harness — `PLANNED`, depends T001;
- `W006-T004` / #191 — secure source ingestion + parser/OCR real-corpus bakeoff — `PLANNED`, depends T001;
- `W006-T005` / #192 — workflow/shared-state + idempotent-attempt bakeoff — `PLANNED`, depends T001;
- `W006-T006` / #193 — frontend/editor same-slice live-cockpit bakeoff — `PLANNED`, depends T001;
- `W006-T007` / #194 — production substrate evidence fan-in / decision promotion — `PLANNED`, depends T002..T006;
- `W006-T008` / #195 — reproducible toolchain + repository-topology evidence freeze — `PLANNED`, depends T007;
- `W006-T009` / #196 — real production vertical slice — `PLANNED`, depends T007,T008;
- `W006-T010` / #197 — eval/human-calibration foundation — `PLANNED`, depends T001,T004;
- `W006-T011` / #198 — provider/model/adaptive runtime benchmark & promotion — `PLANNED`, depends T009,T010;
- `W006-T012` / #199 — observability/live-ops integration — `PLANNED`, depends T009;
- `W006-T013` / #200 — security/reliability/capacity/recovery qualification — `PLANNED`, depends T009,T011,T012;
- `W006-T014` / #201 — final live evidence + production-claim audit — `PLANNED`, depends T010,T011,T013.

After T001 integration, T002–T006 can fan out in parallel. Primary critical path: `T001 → {T002..T006} → T007 → T008 → T009 → T011/T012 → T013 → T014`. T010 joins through the human/eval evidence path.

## W006-T001 — READY

- `TASK_ID: W006-T001`
- `ATTEMPT_ID: A01`
- `ISSUE: #188`
- `WORKER_BRANCH: worker/W006-T001-A01`
- dispatch: `SYSTEM/DISPATCH/W006-T001-A01.md`
- original provenance base: `STATE 0047 / 0fa1fd46d02d8fb2ad3410823ba417d83b596eac`.

Worker must execute `CONTINUITY_CHECK` against STATE 0048/current main before substantive work and must not silently choose evidence-gated vendors/frameworks.

## Evidence boundary

- W005: complete/accepted as implementation authority;
- W006 implementation wave: authorized/materialized; substantive worker implementation is claimed only after `TASK_STARTED` is observed;
- production-ready claim: `FALSE`;
- human gold: not observed;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- unresolved material stack winners: evidence-gated;
- submission completed: not claimed.

## Current success bottleneck

`W006-T001_CONTRACT_SCHEMA_AND_TRACEABILITY_FOUNDATION`

## Next action

Execute `W006-T001-A01`. After accepted integration, unlock T002–T006 in parallel. Do not begin downstream tasks whose persisted dependencies are not integrated.

## Recovery point

Resume from STATE 0048. Ready queue: `W006-T001-A01` only. W005 is complete; blanket production readiness remains false.
