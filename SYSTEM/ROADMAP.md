# PROJECT ROADMAP

`ROADMAP_VERSION: 2.9`

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
- [ ] provider/model real com latency/usage/cost observados — credencial Groq identificada, mas `/openai/v1/models` retorna HTTP 403 antes de geração aceita
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
- [x] authorized Groq credential/provider identity characterized without secret exposure; A04/A05 isolated HTTP 403 access/permission blocker
- [x] README/demo/release hardening + smoke runner (`W004-T011`)
- [x] clean release-smoke CI observado (`W004-T012`)
- [x] recipient-facing interactive PDF/text ingest + evidence app (`W004-T014`)
- [x] consolidated experimental report/submission packet (`W004-T015`)
- [x] real automated browser video artifact + measured duration (`W004-T017`) — technical evidence pass
- [x] paced evaluator-facing final demo + current packet/README (`W004-T019`)
- [x] independent cold-evaluator review of concrete final demo/package (`W004-T020`) — video/package scope PASS
- [x] exact accepted final MP4 preserved in repository-controlled storage with fresh-clone byte-identity verification (`W004-T021`)
- [ ] representative human calibration executada em novo attempt de T005
- [ ] real credentialed provider evidence aceita após correção externa das permissões Groq e novo T004 attempt
- [ ] clean-E2E release proof final T008
Status: `ADVANCED_INTERNAL_DELIVERABLE_DURABILITY_PASS_EXTERNAL_EVIDENCE_BLOCKED`

## Phase 6 — Adversarial Optimization
Objetivo: quebrar solução e case até eliminar gaps materiais.

Gate:
- [x] primeiro blind/adversarial review executado (`W004-T013`) — NOT_PASS
- [x] F-002/F-003/F-007 corrigidos no nível de implementação/artefato
- [x] F-001/F-008 receberam concrete technical video/duration evidence via T017
- [x] T018 inspecionou o artifact concreto — F-008 PASS, F-001 PARTIAL / evaluator usability NOT_PASS
- [x] T019 produziu demo real paced `69.12s`, success-path-first, BCB fail-closed negative-control e packet/README atualizado
- [x] T020 reexecutou blind review independente — `VIDEO_PACKAGE_REVIEW: PASS`, 0 novos CRITICAL/HIGH findings
- [x] T021 eliminou dependência de retenção do Actions para o MP4 aceito sem alterar seus bytes
- [x] T004 blocker foi reduzido de “provider desconhecido/sem credential” para Groq permission/access HTTP 403 reproduzível no próprio Models API
- [ ] Partner Jury PASS global após external evidence aplicável
- [ ] Partner Scorecard PASS
- [ ] Quality Scorecard PASS
- [ ] Success Scorecard sem bottleneck abaixo do floor
- [ ] critical assumptions controladas
Status: `INTERNAL_VIDEO_PACKAGE_AND_DURABILITY_PASS_EXTERNAL_GATES_OPEN`

## Phase 7 — Blind Review, Final Deliverable & Defense
Objetivo: garantir que aquilo que será realmente visto funcione sem contexto interno.

Gate:
- [ ] Traceability obrigatória completa
- [ ] FINAL_REVIEW_PROTOCOL Pass 1 PASS global
- [x] final Blind Review PASS sobre pacote real + vídeo no escopo video/package (`W004-T020`)
- [ ] consistency/artifact QA global após external evidence
- [ ] Q&A/defense rehearsal PASS
- [ ] submission checklist PASS
- [x] artifact de vídeo preservado em storage durável pelo horizonte de avaliação (`W004-T021`)
- [ ] finalization reserve/deadline respeitado
- [ ] Success + Partner + Quality stop conditions PASS
Status: `ACTIVE_EXTERNAL_HUMAN_GROQ_PERMISSION_EVIDENCE`

## Project Complete
Somente quando todos os gates aplicáveis passarem e STATE registrar `PROJECT_STATUS: COMPLETE`.
