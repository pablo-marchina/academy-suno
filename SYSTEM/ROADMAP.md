# PROJECT ROADMAP

`ROADMAP_VERSION: 1.6`

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
- [x] entregáveis/critérios/restrições conhecidos; deadline/submission permanecem `UNKNOWN` e devem ser resolvidos antes da finalização, sem bloquear build técnico
- [x] Traceability Matrix inicializada com requisitos/pains
- [x] Assumption/Risk Register inicializado
- [x] Success/Partner/Quality Scorecards calibrados sem inventar precisão
Status: `COMPLETE`

## Phase 2 — Discovery & Evidence
Objetivo: reduzir os unknowns que mais ameaçam sucesso e validar decisões antes de lock final.

Gate:
- [ ] evidence map completo para claims materiais
- [x] pesquisas prioritárias e W001 discovery/eval foundations executadas
- [x] fontes/evidências primárias e resultados W001 persistidos/indexáveis
- [ ] high-impact/high-uncertainty assumptions testadas ou controladas
- [x] benchmarks/counterfactuals relevantes mapeados, inclusive baseline simples
- [ ] EXP-A parser/source-trust e EXP-B graph-vs-async executados
- [ ] factual/policy adversarial gate suite executada
Status: `IN_PROGRESS`

## Phase 3 — Diagnosis & Root Cause
Objetivo: explicar dor/mecanismo e localizar alavancas.

Gate:
- [x] hipóteses prioritárias do problema técnico mapeadas em W001
- [ ] causas/drivers validados por experimento onde necessário
- [ ] análise quantitativa/qualitativa validada
- [x] status quo/counterfactual simples modelado como prompt/manual/plain-async baseline
- [ ] traceability atualizada para insights-chave após experimentos
Status: `PARTIAL`

## Phase 4 — Solution Portfolio & Selection
Objetivo: gerar, comparar e selecionar solução forte e diferenciada.

Gate:
- [x] alternativa principal e baseline deliberadamente simples comparados conceitualmente
- [x] Partner Value + evaluation fit + feasibility considerados
- [x] recomendação candidata e trade-offs documentados em W001-T010
- [ ] valor incremental medido contra baseline
- [x] assumptions críticas da recomendação explicitadas
- [ ] solução não dominada por alternativa materialmente melhor após mandatory experiments
Status: `PARTIAL`

## Phase 5 — Build, Implementation & Adoption
Objetivo: transformar recomendação em entrega e caminho real de uso.

Gate:
- [ ] foundation contracts/source trust/factual backbone implementados
- [ ] 3×3 generation + evaluator + targeted repair implementados
- [ ] artefatos/protótipo/modelos necessários produzidos
- [ ] owner/dependências/recursos definidos ou explicitamente tratados como external unknowns
- [ ] rollout/piloto e time-to-value definidos
- [ ] métricas/kill-pivot criteria definidos e executados
- [ ] números/fontes reconciliados entre artefatos
Status: `NOT_STARTED`

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