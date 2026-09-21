# PROJECT ROADMAP

`ROADMAP_VERSION: 2.5`

## Phase 0 — System Bootstrap
Objetivo: sistema operacional. Status: `COMPLETE`

## Phase 1 — Case + Partner Intake
Objetivo: entender o que precisa ser resolvido e como o sucesso será julgado.

Gate:
- [x] material/enunciado referenciado
- [x] Case Contract completo
- [x] Partner Contract suficientemente completo com unknowns explícitos
- [x] stakeholders/decisores/owners mapeados como conhecidos ou `UNKNOWN`
- [x] dor/outcome/status quo entendidos em nível suficiente para o case; workflow interno Suno permanece `UNKNOWN`
- [x] entregáveis/critérios/restrições conhecidos; deadline/submission permanecem `UNKNOWN`
- [x] Traceability Matrix e Assumption/Risk Register inicializados
Status: `COMPLETE`

## Phase 2 — Discovery & Evidence
Objetivo: reduzir unknowns que mais ameaçam sucesso e validar decisões antes de lock final.

Gate:
- [x] W001 research/synthesis
- [x] W002 foundation
- [x] W003 mechanics proof, gold protocol, grounding, RunStore, audience diagnostics, repair e telemetry
- [x] held-out isolation/anti-circularity/anti-gaming guardrails
- [x] W004 corpus preparation: 6 sources / 36 frozen development outputs / blind annotation tooling
- [x] expanded parser/source-trust behavior evidence Copom/CVM/Petrobras
- [ ] duas streams humanas independentes + agreement/adjudication
- [ ] provider/model real com latency/usage/cost observados
Status: `ADVANCED_EXTERNAL_EVIDENCE_BLOCKED`

## Phase 3 — Diagnosis & Root Cause
Objetivo: explicar dor/mecanismo e localizar alavancas.

Gate:
- [x] source trust, factual drift, policy drift e format mismatch validados
- [x] audience sophistication drivers instrumentados e anti-gaming
- [ ] audience sophistication calibrada contra human gold independente
- [x] status quo/counterfactual simples modelado
Status: `ADVANCED_PARTIAL`

## Phase 4 — Solution Portfolio & Selection
Objetivo: gerar, comparar e selecionar solução forte e diferenciada.

Gate:
- [x] foundation invariants selecionados por evidência
- [x] plain async provisional runtime leader; no framework lock by preference
- [x] provider/parser/semantic identities desbloqueadas sem proof
- [x] parser behavior contract expandido; implementation continua unlocked
- [ ] semantic backend ablation sobre human development gold
- [ ] provider/model comparison sobre runs comparáveis
- [ ] value incrementality com evidence real
Status: `PARTIAL_EXTERNAL_EVIDENCE_BLOCKED`

## Phase 5 — Build, Implementation & Adoption
Objetivo: transformar recomendação em entrega e caminho real de uso.

Gate:
- [x] foundation + 3×3 + evaluator + targeted repair + RunStore + telemetry
- [x] evidence cockpit com provenance/unknown/fail/review states
- [x] expanded parser behavior/source-trust bakeoff
- [x] provider-neutral execution/telemetry harness + pricing guardrails
- [x] blind human-calibration preparation e agreement tooling
- [x] blind annotation operator/handoff (`W004-T009`)
- [x] manual credential-safe provider execution/import path (`W004-T010`)
- [x] README/demo/release hardening + smoke runner (`W004-T011`)
- [x] clean release-smoke CI observado (`W004-T012`)
- [x] recipient-facing interactive PDF/text ingest + evidence app (`W004-T014`)
- [x] consolidated experimental report/submission packet (`W004-T015`)
- [x] real automated browser video artifact + measured duration (`W004-T017`) — technical evidence pass
- [ ] paced evaluator-facing final demo + current packet/README (`W004-T019`)
- [ ] representative human calibration executada em novo attempt de T005
- [ ] real credentialed provider evidence executada/comparada
- [ ] clean-E2E release proof final T008
Status: `ADVANCED_FINAL_DEMO_AND_EXTERNAL_EVIDENCE`

## Phase 6 — Adversarial Optimization
Objetivo: quebrar solução e case até eliminar gaps materiais.

Gate:
- [x] primeiro blind/adversarial review executado (`W004-T013`) — NOT_PASS
- [x] F-002/F-003/F-007 corrigidos no nível de implementação/artefato
- [x] F-001/F-008 receberam concrete technical video/duration evidence via T017
- [x] T018 inspecionou o artifact concreto — F-008 PASS, F-001 PARTIAL / evaluator usability NOT_PASS
- [ ] T019 corrige demo evaluator-facing sem enfraquecer fail-closed source trust
- [ ] T020 reexecuta blind review independente sobre o artifact final
- [ ] Partner Jury PASS
- [ ] Red Team/Evaluator PASS em findings críticos
- [ ] Partner Scorecard PASS
- [ ] Quality Scorecard PASS
- [ ] Success Scorecard sem bottleneck abaixo do floor
- [ ] critical assumptions controladas
Status: `ACTIVE_FINAL_DEMO_REMEDIATION_AND_EXTERNAL_GATES`

## Phase 7 — Blind Review, Final Deliverable & Defense
Objetivo: garantir que aquilo que será realmente visto funcione sem contexto interno.

Gate:
- [ ] Traceability obrigatória completa
- [ ] FINAL_REVIEW_PROTOCOL Pass 1 PASS
- [ ] final Blind Review PASS sobre pacote real + vídeo
- [ ] consistency/artifact QA PASS
- [ ] Q&A/defense rehearsal PASS
- [ ] submission checklist PASS
- [ ] artifact de vídeo preservado em storage durável pelo horizonte de avaliação
- [ ] finalization reserve/deadline respeitado
- [ ] Success + Partner + Quality stop conditions PASS
Status: `BLOCKED_BY_FINAL_DEMO_AND_EXTERNAL_EVIDENCE`

## Project Complete
Somente quando todos os gates aplicáveis passarem e STATE registrar `PROJECT_STATUS: COMPLETE`.
