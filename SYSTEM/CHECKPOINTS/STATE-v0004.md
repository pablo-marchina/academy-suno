# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.2.0`

`STATE_VERSION: 0004`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case Intake & Problem Framing`

`LAST_COMMITTED_WAVE: SYSTEM-ORCHESTRATION-V1.2`

## Objective

Construir o case Academy Suno com máxima velocidade usando múltiplos chats/agentes em paralelo, preservando continuidade exata por meio de estado canônico versionado no GitHub.

## Current truth

- Repositório canônico: `pablo-marchina/academy-suno`.
- O protocolo operacional está em `1.2.0` com proveniência por tentativa, checkpoints e manifests de wave/DAG.
- O lease exclusivo do Orchestrator é controlado na branch `control/orchestrator-lease` por update atômico baseado no blob SHA observado.
- Todo novo estado exige snapshot em `SYSTEM/CHECKPOINTS/`.
- Tasks usam `TASK_ID + ATTEMPT_ID + BASE_STATE_VERSION + BASE_COMMIT_SHA`.
- Phase 0 está concluída e Phase 1 está aberta.
- A Issue #2 (`BOOT-T002`) continua sendo a tarefa canônica de ingestão do briefing.
- O enunciado completo do case ainda não foi incorporado ao estado.
- Nenhuma wave de desenvolvimento do case foi executada ainda.

## Locked decisions

- `D-0001` — GitHub é a fonte canônica de verdade.
- `D-0002` — Workers não atualizam arquivos canônicos; integração é responsabilidade do Orchestrator autorizado.
- `D-0003` — Tarefas independentes são executadas em paralelo e rastreadas por identidade/versionamento.
- `D-0004` — Guardrails do sistema são executáveis no repositório.
- `D-0005` — Autoridade de integração exige lease atômico exclusivo do Orchestrator.
- `D-0006` — Toda tentativa possui proveniência imutável por `ATTEMPT_ID` e `BASE_COMMIT_SHA`.
- `D-0007` — Estado é checkpointado e execução paralela é governada por manifests de wave/DAG.

## Active hypotheses

Nenhuma.

## Open blockers

- `B-0001` — Falta incorporar o briefing/enunciado completo do case e seus materiais de entrada.
- `B-0002` — A proteção administrativa do branch `main` ainda precisa ser ativada no GitHub para exigir PR/status check e bloquear bypass acidental.
- `B-0003` — Como o repositório é público, confirmar que o briefing não contém conteúdo confidencial antes de versioná-lo; caso contenha, tornar o repositório privado primeiro.

## Active tasks

- `BOOT-T002` — `READY` — Issue #2 — incorporar briefing completo e preparar a primeira wave.

## Pending decisions

- Definir prazo final e formato do deliverable após leitura do case.
- Definir stack/arquitetura técnica caso o case exija implementação de software.
- Refinar o roadmap genérico para o case real.
- Confirmar política de visibilidade (público/privado) após receber o briefing.

## Next action

1. Ativar proteção/ruleset do `main` exigindo Pull Request e `validate-canonical-system`, sem force-push/deleção.
2. Confirmar se o briefing pode permanecer em repositório público.
3. Abrir/usar o chat Orchestrator e adquirir o lease na branch `control/orchestrator-lease`.
4. Executar `CONTINUITY_CHECK` esperando `PROTOCOL_VERSION: 1.2.0` e `STATE_VERSION: 0004`.
5. Atualizar a Issue #2 com `BASE_STATE_VERSION 0004`, `BASE_COMMIT_SHA` atual e `ATTEMPT_ID A01`.
6. Ingerir o briefing/material completo do case.
7. Criar `W001.json` e disparar a ready queue com máximo paralelismo seguro.

## Recovery point

Se qualquer chat, worker, Orchestrator ou wave falhar, retomar a partir de `STATE_VERSION 0004` e de `SYSTEM/CHECKPOINTS/STATE-v0004.md`. Nenhuma conclusão não integrada no `main` é canônica.
