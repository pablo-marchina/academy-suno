# PROJECT ROADMAP

`ROADMAP_VERSION: 3.1`

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
Status: `ACTIVE_EXTERNAL_FINALIZATION_FACTS`

## Project Complete
Somente quando todos os hard gates globais do Success Model passarem e STATE registrar `PROJECT_STATUS: COMPLETE`. O W004 interno está concluído; o projeto não pode ser marcado COMPLETE enquanto deadline/submission/finalization facts permanecerem UNKNOWN.
