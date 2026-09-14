# PROJECT ROADMAP

`ROADMAP_VERSION: 1.2`

O roadmap controla avanço de fase. A função objetivo e os critérios de finalização vêm de `SYSTEM/QUALITY_MODEL.md`.

## Phase 0 — System Bootstrap
Objetivo: sistema multi-chat operacional.

Gate de saída:
- [x] governança, state, tasks/waves, handoff e papéis definidos
- [x] guardrails, lease, checkpoints e DAG definidos
- [x] Quality Model e autopilot definidos

Status: `COMPLETE`

## Phase 1 — Case Intake & Problem Framing
Objetivo: transformar o briefing em Case Contract e rubrica de avaliação defensável.

Gate de saída:
- [ ] enunciado original armazenado/referenciado
- [ ] objetivo central e decisão/pergunta do case definidos
- [ ] entregáveis obrigatórios/opcionais definidos
- [ ] critérios explícitos de avaliação extraídos
- [ ] pesos/escala registrados quando disponíveis
- [ ] expectativas implícitas justificáveis e audiência registradas
- [ ] restrições, prazo e penalidades definidos
- [ ] perguntas críticas/unknowns registradas
- [ ] `QUALITY_SCORECARD` calibrado e Case Contract pronto

Status: `IN_PROGRESS`

## Phase 2 — Discovery & Evidence
Objetivo: preencher gaps de informação com maior impacto esperado na avaliação.

Gate de saída:
- [ ] mapa de evidências ligado à rubrica
- [ ] pesquisas prioritárias executadas
- [ ] fontes/benchmarks indexados
- [ ] claims materiais suportados ou explicitamente tratados como hipótese
- [ ] lacunas críticas explicitadas

Status: `NOT_STARTED`

## Phase 3 — Analysis & Diagnosis
Objetivo: testar hipóteses e construir diagnóstico robusto para os critérios relevantes.

Gate de saída:
- [ ] hipóteses prioritárias testadas
- [ ] drivers identificados
- [ ] análises quantitativas validadas
- [ ] sensibilidades/cenários relevantes testados
- [ ] diagnóstico sintetizado e ligado ao objetivo do case

Status: `NOT_STARTED`

## Phase 4 — Solution / Strategy
Objetivo: selecionar a solução de maior qualidade esperada dadas evidências/restrições.

Gate de saída:
- [ ] alternativas materiais comparadas
- [ ] critérios de escolha explícitos
- [ ] recomendação definida
- [ ] trade-offs, riscos e mitigadores mapeados
- [ ] impactos estimados
- [ ] recomendação superior às alternativas consideradas

Status: `NOT_STARTED`

## Phase 5 — Build / Implementation Design
Objetivo: produzir todos os artefatos necessários para tornar a solução executável e avaliável.

Gate de saída:
- [ ] plano/arquitetura definido
- [ ] artefatos obrigatórios produzidos
- [ ] dependências/recursos identificados
- [ ] sequência de execução definida
- [ ] métricas de acompanhamento definidas

Status: `NOT_STARTED`

## Phase 6 — Quality Optimization & Red Team
Objetivo: iterar sobre o case completo até hard gates e stop condition passarem.

Gate de saída:
- [ ] avaliação completa contra rubrica executada
- [ ] Red Team atacou premissas, números, estratégia e defesa
- [ ] gaps materiais priorizados por expected quality uplift
- [ ] nenhum finding crítico aberto
- [ ] hard gates = PASS
- [ ] `QUALITY_STATUS: PASS`
- [ ] `STOP_CONDITION: PASS`

Status: `NOT_STARTED`

## Phase 7 — Final Deliverable & Defense
Objetivo: entregar versão final top-tier e defendê-la.

Gate de saída:
- [ ] deliverables completos e conformes ao Case Contract
- [ ] narrativa final coerente
- [ ] números/fontes revisados
- [ ] mensagens-chave e Q&A preparados
- [ ] simulação de avaliador/banca concluída
- [ ] revisão final contra briefing sem gap material

Status: `NOT_STARTED`

## Project Complete

Somente quando todos os gates aplicáveis estiverem PASS e `SYSTEM/STATE.md` registrar `PROJECT_STATUS: COMPLETE`, com Quality Scorecard em PASS.
