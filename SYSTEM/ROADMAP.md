# PROJECT ROADMAP

`ROADMAP_VERSION: 1.8`

## Phase 0 — System Bootstrap
Objetivo: sistema operacional. Status: `COMPLETE`

## Phase 1 — Case + Partner Intake
Objetivo: entender o que precisa ser resolvido e como o sucesso será julgado.

Gate:
- [x] material/enunciado referenciado
- [x] Case Contract completo
- [x] Partner Contract suficientemente completo com unknowns explícitos
- [x] stakeholders/decisores/owners mapeados como conhecidos ou `UNKNOWN`
- [x] dor/outcome/status quo entendidos em nível suficiente para o case; workflow interno Suno permanece `UNKNOWN` e controlado como limitação de produção
- [x] entregáveis/critérios/restrições conhecidos; deadline/submission permanecem `UNKNOWN` e devem ser resolvidos antes da finalização
- [x] Traceability Matrix inicializada
- [x] Assumption/Risk Register inicializado
- [x] Scorecards calibrados sem inventar precisão
Status: `COMPLETE`

## Phase 2 — Discovery & Evidence
Objetivo: reduzir unknowns que mais ameaçam sucesso e validar decisões antes de lock final.

Gate:
- [x] pesquisas prioritárias W001 executadas
- [x] foundation W002 executada
- [x] W003 gold protocol, grounding, graph/RunStore, audience diagnostics, repair, telemetry e calibration guard implementados
- [x] W003 mechanics proof source→9→eval→repair→aggregate executado
- [x] held-out isolation/anti-circularity/anti-gaming guardrails executáveis
- [ ] representative independent human labels/agreement adquiridos
- [ ] real provider/model quality-latency-usage-cost evidence comparável
- [ ] expanded parser/source generalization evidence
Status: `ADVANCED_IN_PROGRESS`

## Phase 3 — Diagnosis & Root Cause
Objetivo: explicar dor/mecanismo e localizar alavancas.

Gate:
- [x] source trust, factual drift, policy drift e format mismatch validados
- [x] audience sophistication drivers instrumentados e anti-gaming
- [ ] audience sophistication drivers calibrados contra human gold independente
- [x] status quo/counterfactual simples modelado
- [x] mechanisms/traceability atualizados por W003 mechanics proof
Status: `ADVANCED_PARTIAL`

## Phase 4 — Solution Portfolio & Selection
Objetivo: gerar, comparar e selecionar solução forte e diferenciada.

Gate:
- [x] foundation invariants selecionados por evidência
- [x] plain async provisional runtime leader por evidence; no framework lock by preference
- [x] provider/parser/semantic identities mantidas desbloqueadas sem proof
- [ ] provider/model comparison sobre evidence comparável
- [ ] parser implementation lock only if bakeoff separates candidates
- [ ] value incrementality medida contra baseline
Status: `PARTIAL`

## Phase 5 — Build, Implementation & Adoption
Objetivo: transformar recomendação em entrega e caminho real de uso.

Gate:
- [x] foundation contracts/source trust/factual backbone implementados
- [x] 3×3 planning + evaluator + targeted repair mechanics integrados end-to-end
- [x] explicit graph/state RunStore + telemetry integrados
- [x] W003 mechanics proof 9/9 com resume/retry/repair lineage
- [ ] evidence cockpit construído
- [ ] representative human calibration executada
- [ ] real provider evidence executada/comparada
- [ ] expanded parser bakeoff concluído
- [ ] clean-E2E release proof + README/report packet
- [ ] owner/dependências/recursos definidos ou explicitamente tratados como external unknowns
Status: `IN_PROGRESS_W004`

## Phase 6 — Adversarial Optimization
Objetivo: quebrar solução e case até eliminar gaps materiais.

Gate:
- [ ] Partner Jury PASS
- [ ] Red Team/Evaluator PASS em findings críticos
- [ ] Partner Scorecard PASS
- [ ] Quality Scorecard PASS
- [ ] Success Scorecard sem bottleneck abaixo do floor
- [ ] critical assumptions controladas
Status: `NOT_STARTED`

## Phase 7 — Blind Review, Final Deliverable & Defense
Objetivo: garantir que aquilo que será realmente visto funcione sem contexto interno.

Gate:
- [ ] Traceability obrigatória completa
- [ ] FINAL_REVIEW_PROTOCOL Pass 1 PASS
- [ ] Blind Review PASS
- [ ] consistency/artifact QA PASS
- [ ] Q&A/defense rehearsal PASS
- [ ] submission checklist PASS
- [ ] finalization reserve/deadline respeitado
- [ ] Success + Partner + Quality stop conditions PASS
Status: `NOT_STARTED`

## Project Complete
Somente quando todos os gates aplicáveis passarem e STATE registrar `PROJECT_STATUS: COMPLETE`.
