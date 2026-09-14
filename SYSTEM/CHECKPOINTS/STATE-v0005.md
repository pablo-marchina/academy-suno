# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.3.0`

`STATE_VERSION: 0005`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case Intake & Problem Framing`

`LAST_COMMITTED_WAVE: SYSTEM-QUALITY-LOOP-V1.3`

## Objective

Entregar o melhor case possível segundo o objetivo real do briefing, os entregáveis obrigatórios, os critérios de avaliação e as restrições, usando múltiplos chats/agentes para acelerar a busca e a iteração sem sacrificar qualidade.

## Current truth

- GitHub é a fonte canônica de verdade.
- O sistema opera com lease exclusivo, provenance por tentativa, checkpoints, DAG e dispatches.
- `QUALITY_MODEL_VERSION 1.0` define a função objetivo dominante e o quality loop.
- `QUALITY_SCORECARD` está `AWAITING_CASE_CONTRACT`: ainda não é válido atribuir nota antes de ingerir o briefing.
- O Orchestrator deve gerar prompts/dispatches automaticamente; o usuário não deve projetar tasks/prompts manualmente.
- Phase 1 está aberta e a Issue #2 (`BOOT-T002`) é a tarefa canônica para ingestão do briefing e construção do Case Contract.
- Nenhuma wave de desenvolvimento do case foi executada.

## Locked decisions

- `D-0001` — GitHub é a fonte canônica.
- `D-0002` — Workers não integram estado.
- `D-0003` — Tarefas independentes são paralelizadas.
- `D-0004` — Guardrails são executáveis.
- `D-0005` — Lease exclusivo do Orchestrator.
- `D-0006` — Proveniência/idempotência por tentativa.
- `D-0007` — Checkpoints e DAG executável.
- `D-0008` — Função objetivo dominante = melhor case possível conforme avaliação real.
- `D-0009` — Quality loop obrigatório até hard gates/stop condition.

## Open blockers

- `B-0001` — Falta briefing/enunciado e materiais para construir Case Contract.
- `B-0002` — Proteção administrativa do `main` ainda deve ser ativada.
- `B-0003` — Repositório público: confirmar confidencialidade antes de versionar materiais.

## Active tasks

- `BOOT-T002` — `READY` — Issue #2 — ingerir briefing, construir Case Contract, calibrar Quality Scorecard e preparar W001.

## Pending decisions

- Prazo final/formato conforme briefing.
- Visibilidade público/privado conforme confidencialidade.
- Stack técnica se aplicável ao case.
- Pesos/thresholds finais da rubrica após leitura dos critérios reais.

## Next action

1. Resolver blockers administrativos aplicáveis.
2. Revalidar lease do Orchestrator.
3. Executar `BOOT-T002` sobre `STATE 0005`.
4. Extrair Case Contract e calibrar `QUALITY_SCORECARD` sem inventar critérios.
5. Criar W001 a partir dos maiores gaps/unknowns de qualidade.
6. Gerar dispatches e iniciar o autopilot quality loop.

## Recovery point

Retomar de `STATE_VERSION 0005` e `SYSTEM/CHECKPOINTS/STATE-v0005.md`. Nenhuma conclusão fora do main é canônica.
