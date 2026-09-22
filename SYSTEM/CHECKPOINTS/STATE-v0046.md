# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0046`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 8 — Production Scope & Decision Research Foundation`

`LAST_COMMITTED_WAVE: W005-T010-SYNTHESIS-ACCEPTED-T011-READY`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução — elevando o alvo para produto real multiusuário, production-grade no escopo comprovado, quantitative/eval-driven, adaptive onde seguro e integralmente observável.

## Preserved truth

- W004 permanece baseline/evidência histórica válida e não autoriza production readiness.
- human gold/agreement/preference continuam not observed; production audience thresholds continuam `DIAGNOSTIC_ONLY` até stronger evidence.
- external deadline, submission mechanism, named Suno owner/workflow e ROI baseline permanecem `UNKNOWN`.
- accepted W005 research/synthesis não converte `NO_PREFERENCE/PENDING_EVIDENCE` em winner por consenso.

## W005 required research fan-in — COMPLETE 11/11

Todos os onze inputs obrigatórios permanecem aceitos/integrados:

`T001,T002,T003,T004,T005,T006,T007,T008,T009-A02,T013,T014`.

`W005-BENCHMARK-METHODOLOGY-V002` permanece o default decision surface: non-compensatory hard gates → raw multidimensional metrics → uncertainty where meaningful → point Pareto; scalar/business utility somente com representative evidence + predeclared sensitivity stability.

## W005-T010 production architecture synthesis — ACCEPTED

`W005-T010-A01` completou lifecycle/provenance, RESULT e PR #183. O worker preservou a base original STATE 0040, observou STATE 0045/main no início e passou `CONTINUITY_CHECK` antes do trabalho substantivo. O PR alterou apenas os três artefatos de síntese e System Integrity passou antes da integração.

Accepted artifacts:

- `SYSTEM/RESULTS/W005-T010-A01.md`;
- `docs/production/W005_TARGET_PRODUCTION_ARCHITECTURE.md`;
- `docs/production/W005_IMPLEMENTATION_DAG_AND_ACCEPTANCE_GATES.md`.

### Accepted synthesis boundary

T010 mapeia `PROD-001..017` em `17/17` sem relabelar arquitetura definida como production-PASS e preserva decisões por evidência:

- `LOCK`: typed/versioned HTTP + OpenAPI; SSE live feed com durable cursor/replay/snapshot; server-side authz/redaction; app-owned tenant/resource authorization; private quarantine/validate/promote + immutable provenance; parser-independent fail-closed source trust; exact 9-way workflow semantics; deterministic hard-gate envelope around adaptive routing; human-calibration method; W005 benchmark v002; durable product events separados de sampled telemetry; W3C Trace Context + OpenTelemetry + OTLP/Collector boundary; metadata-first telemetry; deployment/recovery/idempotency/backpressure invariants; GitHub Actions + CI/supply-chain hardening; single-repository initial migration.
- `NO_PREFERENCE`: identity vendor; object-store/scanner vendor; provider/model overall winner; observability backend; managed-container vs cluster-scheduler; native pinned environment vs Dev Container; SBOM encoding.
- `PENDING_EVIDENCE`: API framework; frontend/editor; production data engine/PostgreSQL-RLS choice; parser/OCR route; workflow/runtime/shared-state implementation; learned routing default; audience thresholds; external eval framework; scalar business utility; sampling/retention/SLO/capacity/RTO/RPO values; Python/JS package managers/task graph.

### Critical implementation constraints carried forward

- current `SQLiteRunStore` is explicitly disqualified as multi-replica production authority in its present stale-write form;
- sampled observability is never authoritative product/live state;
- flat-text numeric recall cannot substitute for semantic table/cell provenance;
- adaptive optimization cannot bypass deterministic eligibility/hard gates;
- arbitrary untrusted server filesystem-path input is prohibited in production;
- unsupported practical thresholds from task-local experiments do not become production locks.

### Accepted hard quantitative gates

- hard-gate compensation = `0`;
- cross-tenant unauthorized success in defined tests = `0`;
- required provenance missing = `0`;
- branch coverage = exact `9/9`;
- accepted join loss/duplication = `0`;
- critical schema false PASS = `0`;
- silent stale same-run overwrite in selected production state path = `0`;
- arbitrary untrusted server-path production input = `0`;
- private quarantine bypass in defined tests = `0`;
- secret/credential canary leakage in product events/telemetry = `0`;
- defined restart/resume scenarios = `100% PASS` before production claim;
- defined backup/restore scenarios = `100% PASS` before production claim;
- final technical video = `<=5:00`.

Quality/audience/latency/cost/capacity/retention/sampling/SLO/RTO/RPO thresholds permanecem evidence/external-owner gated.

## W005-T011 — READY

A dependência `W005-T010` está agora accepted/integrated.

- `TASK_ID: W005-T011`
- `ATTEMPT_ID: A01`
- `ISSUE: #161`
- `WORKER_BRANCH: worker/W005-T011-A01`
- `STATUS: READY`
- dispatch: `SYSTEM/DISPATCH/W005-T011-A01.md`

O attempt preserva sua provenance base original `STATE 0040 / 1cfeb9803036767f4b2cf14320e885751c266f10`. O worker deve executar `CONTINUITY_CHECK` contra STATE 0046/current main antes do trabalho substantivo.

T011 deve red-team independentemente a síntese de T010: procurar unearned locks, single-user/local assumptions, tenant/security gaps, reliability/recovery gaps, eval circularity, observability leakage, missing counterfactuals e fake-demo drift. Qualquer nova alternativa material sem DRG suficiente deve gerar follow-up evidence requirement, não seleção silenciosa.

## Downstream gates

- `W005-T012` permanece `PLANNED`; depende de T010 + T011 accepted/integrated.
- Phase 9 production implementation continua proibida antes do final fan-in T012.

## Current success bottleneck

`W005-T011_INDEPENDENT_PRODUCTION_ARCHITECTURE_RED_TEAM`

## Evidence boundary

- W005 research inputs accepted: `11/11`;
- T010 synthesis: accepted/integrated;
- T011: `READY`;
- T012: gated;
- human gold: not observed;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- blanket production readiness: false;
- submission completed: not claimed.

## Next action

Execute `W005-T011-A01` from its persisted dispatch. After an evidence-valid independent red-team result is accepted/integrated, unlock T012 final fan-in. Do not start Phase 9 implementation before T012 closes.

## Recovery point

Resume from STATE 0046. Ready queue: `W005-T011-A01` only. Gated downstream: `W005-T012-A01`. T010 production architecture synthesis is accepted; production implementation remains gated by red-team + final fan-in.