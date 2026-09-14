# DECISION LOG

Somente o Orchestrator com lease ativo pode alterar este arquivo.

## D-0001 — GitHub como fonte canônica
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: GitHub é a fonte de verdade.

## D-0002 — Escrita exclusiva do Orchestrator
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: workers não atualizam estado canônico.

## D-0003 — Waves paralelas versionadas
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: tarefas independentes são paralelizadas com identidade/base explícitas.

## D-0004 — Guardrails executáveis
- Status: `LOCKED`
- Estado de origem: `STATE-v0003`
- Decisão: governança é validada por CI/PR.

## D-0005 — Lease atômico do Orchestrator
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: somente holder do lease pode integrar.

## D-0006 — Proveniência por tentativa
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: toda execução usa `TASK_ID + ATTEMPT_ID + BASE_STATE_VERSION + BASE_COMMIT_SHA`.

## D-0007 — Checkpoints e DAG
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: estados têm snapshots imutáveis e waves usam DAG executável.

## D-0008 — Função objetivo dominante do projeto
- Status: `LOCKED`
- Estado de origem: `STATE-v0005`
- Decisão: o objetivo máximo é entregar o melhor case possível segundo objetivo do briefing, entregáveis obrigatórios, critérios reais de avaliação, restrições e evidências. Velocidade/paralelismo são meios subordinados.
- Motivo: impedir otimização local por número de tarefas, velocidade ou complexidade que não aumente a avaliação final.

## D-0009 — Quality loop obrigatório até stop condition
- Status: `LOCKED`
- Estado de origem: `STATE-v0005`
- Decisão: após existir solução avaliável, o Orchestrator reavalia o case completo, identifica os gaps de maior impacto, gera novas tarefas/dispatches e repete até hard gates e stop condition do Quality Model passarem. Completude de wave não encerra o projeto.
- Motivo: alinhar autonomia e iteração ao resultado final, não ao processo.

## Próximo ID disponível

`D-0010`
