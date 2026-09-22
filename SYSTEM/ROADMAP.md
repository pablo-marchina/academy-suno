# PROJECT ROADMAP

`ROADMAP_VERSION: 4.2`

## Phase 0 — System Bootstrap
Objetivo: sistema operacional. Status: `COMPLETE`

## Phase 1 — Case + Partner Intake
Objetivo: entender o que precisa ser resolvido e como o sucesso será julgado.

Gate:
- [x] briefing/material e Case Contract
- [x] Partner Contract com unknowns explícitos
- [x] stakeholders/owners conhecidos ou `UNKNOWN`
- [x] requisitos, entregáveis e restrições técnicas mapeados
- [x] Traceability + Assumption/Risk inicializados
Status: `COMPLETE`

## Phase 2 — Discovery & Evidence
Objetivo: reduzir unknowns materiais e obter evidência representativa.

Gate:
- [x] W001 research/synthesis
- [x] W002 foundation
- [x] W003 mechanics/eval/repair/telemetry
- [x] W004 6-source / 36 DEVELOPMENT frozen corpus
- [x] provider mechanics observado T004-A08
- [x] automated blind calibration T005-A02 aceita sob D-0017
- [x] held-out isolation e anti-circularity preservados
Status: `COMPLETE_EVIDENCE_BOUNDED`

## Phase 3 — Diagnosis & Root Cause
Objetivo: localizar mecanismos de factual/source/audience/format failure.

Gate:
- [x] source trust/factual/policy/format mechanisms instrumentados
- [x] audience diagnostics e anti-gaming
- [x] automated blind calibration aceita sob D-0017
- [x] ausência de human gold explicitamente preservada
Status: `COMPLETE_DIAGNOSTIC_ONLY_AUDIENCE_THRESHOLDS`

## Phase 4 — Solution Portfolio & Selection
Objetivo: comparar alternativas sem lock por preferência.

Gate:
- [x] evidence-backed foundation invariants
- [x] plain async evidence leader sem rewrite especulativo
- [x] T006 semantic ablation: delta +0.000000 → `NO_BACKEND_PREFERENCE`
- [x] T007-A05 bounded provider/model comparison → `NO_OVERALL_MODEL_PREFERENCE`
- [x] no human preference/model superiority claim
Status: `COMPLETE_NO_UNGROUNDED_SELECTION`

## Phase 5 — Build, Implementation & Adoption
Objetivo: transformar recomendação em entrega executável.

Gate:
- [x] 3×3 + evaluator + targeted repair + RunStore + telemetry
- [x] evidence cockpit + source trust + parser behavior
- [x] provider harness + observed Groq mechanics
- [x] recipient-facing text/PDF app
- [x] consolidated report/submission packet
- [x] final real browser demo + durable exact binary
- [x] T008-A02 clean-E2E release proof
Status: `COMPLETE_INTERNAL_EXECUTION`

## Phase 6 — Adversarial Optimization
Objetivo: quebrar a solução e eliminar gaps materiais internos.

Gate:
- [x] adversarial review T013
- [x] recipient/app/report remediations T014/T015
- [x] real capture T017, review T018, final demo T019
- [x] independent video/package review T020: zero new CRITICAL/HIGH
- [x] durable artifact T021
- [x] T005/T006/T007/T008 evidence fan-in concluído com provenance válida
Status: `COMPLETE_INTERNAL_SCOPE`

## Phase 7 — Blind Review, Final Deliverable & Defense
Objetivo: garantir que aquilo que será visto funcione sem contexto interno.

Gate:
- [x] internal requirement traceability reconciliada
- [x] independent final package/video review `PASS_VIDEO_PACKAGE_SCOPE`
- [x] consistency/artifact QA técnico via T008-A02 clean checkout
- [x] final demo <=5:00 e durável
- [ ] deadline/finalization reserve verificados — `UNKNOWN_EXTERNAL`
- [ ] submission mechanism/format verificado — `UNKNOWN_EXTERNAL`
- [ ] Success + Partner + Quality stop conditions globais PASS
Status: `PRESERVED_W004_FINALIZATION_OPEN`

## Phase 8 — Production Scope & Decision Research Foundation
Objetivo: converter o novo escopo do operador em contratos executáveis e pesquisar sistematicamente as decisões que condicionam a arquitetura de produção.

Gate:
- [x] Production Contract + DRG incorporados ao protocolo
- [x] W005 wave/Issues/dispatches/ledger vinculados à base canônica e readiness review concluído
- [x] research coverage reconciliada antes do kick-off, incluindo developer platform/toolchain/CI (T013) e document parsing/source-grounding (T014)
- [ ] W005-T001..T009 + T013..T014 research/bakeoffs concluídos e aceitos
- [ ] W005-T010 arquitetura alvo sintetizada sem lock por preferência
- [ ] W005-T011 red-team independente concluído e findings materiais tratados
- [ ] W005-T012 production requirements/risks/traceability reconciliados + implementation DAG aceito
- [ ] candidate stack decisions com DR records ou `NO_PREFERENCE/PENDING_EVIDENCE`
Status: `ACTIVE_READY_FOR_RESEARCH_EXECUTION`

## Phase 9 — Multi-user Production Foundation
Objetivo: construir identity/tenancy/API/shared persistence/object storage/deployment foundation após DRG e fan-in W005.

Entry gate:
- [ ] W005-T012 aceito com arquitetura/DAG evidence-backed
- [ ] material technology decisions requeridas para o primeiro increment estão `LOCK` ou explicitamente `PENDING_EVIDENCE` com spike definido
- [ ] parser/source-grounding path necessário ao primeiro increment tem decisão evidence-backed ou spike explícito
- [ ] manifest/toolchain reproduzível do produto definido como parte do primeiro implementation increment a partir de T013/T010/T012, sem lock anterior ao DRG

Build gate:
- [ ] authn/authz + tenant/workspace model
- [ ] cross-tenant tests PASS
- [ ] shared durable persistence + migrations
- [ ] secure object/document ingestion
- [ ] production API boundary + idempotency/backpressure
- [ ] reproducible deployment baseline
Status: `PLANNED_GATED_BY_W005`

## Phase 10 — Real Adaptive AI Runtime
Objetivo: ligar o produto recipient-facing ao workflow/provider/eval/repair reais e introduzir adaptação segura orientada por métricas.

Gate:
- [ ] real provider path no produto
- [ ] source→9→eval→repair→aggregate real
- [ ] adaptive policy versionada/telemetrada
- [ ] no hard-gate relaxation
- [ ] resume/recovery em shared runtime
Status: `PLANNED`

## Phase 11 — Evaluation Science & Evidence Cockpit
Objetivo: elevar calibração, experimentação e visualização live a padrão de produção.

Gate:
- [ ] human-calibration protocol executado ou blocker explicitamente preservado
- [ ] dataset ampliado/versionado com held-out
- [ ] offline eval + regression gates
- [ ] live graph/3×3/source/repair/trace/cost/latency UI
- [ ] online eval sampling strategy
Status: `PLANNED`

## Phase 12 — Reliability, Security & Production Validation
Objetivo: provar capacidade operacional em vez de alegá-la.

Gate:
- [ ] load/saturation curve
- [ ] restart/resume/failure tests
- [ ] backup/restore PASS
- [ ] threat model + authz/tenant/upload/secrets tests PASS
- [ ] observability coverage + SLO evidence
- [ ] production deployment evidence no escopo declarado
Status: `PLANNED`

## Phase 13 — Final Scientific Report, Defense & Submission
Objetivo: reconciliar o produto real, pesquisa, evals, arquitetura, evidência e briefing em uma entrega final reproduzível.

Gate:
- [ ] relatório experimental/decision research consolidado
- [ ] README/runbooks/reproducibility atualizados
- [ ] final product blind review PASS
- [ ] vídeo obrigatório <=5:00 do produto real
- [ ] deadline/submission mechanism/finalization reserve verificados
- [ ] Success + Partner + Quality + Production gates PASS
Status: `PLANNED`

## Project Complete
Somente quando todos os hard gates globais do Success Model passarem e STATE registrar `PROJECT_STATUS: COMPLETE`. O W004 permanece evidência válida do case, mas a expansão D-0018 abriu novo critical path de produção; o projeto não pode ser marcado COMPLETE enquanto Production Contract, finalization e demais stop conditions permanecerem abertas.
