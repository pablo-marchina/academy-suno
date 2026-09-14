# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.0.0`

`STATE_VERSION: 0001`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 0 — System Bootstrap`

`LAST_COMMITTED_WAVE: NONE`

## Objective

Construir o case Academy Suno com máxima velocidade usando múltiplos chats/agentes em paralelo, preservando continuidade exata por meio de estado canônico versionado no GitHub.

## Current truth

- Repositório canônico: `pablo-marchina/academy-suno`.
- O protocolo multi-chat está sendo inicializado.
- O enunciado completo do case ainda não foi incorporado ao estado.
- Nenhuma wave de desenvolvimento do case foi executada ainda.

## Locked decisions

- `D-0001` — GitHub será a fonte canônica de verdade; memória de chats não será usada como mecanismo primário de continuidade.
- `D-0002` — Workers não atualizam arquivos canônicos; integração é responsabilidade exclusiva do Orchestrator.
- `D-0003` — Tarefas independentes serão executadas em waves paralelas e rastreadas por `TASK_ID` + `BASE_STATE_VERSION`.

## Active hypotheses

Nenhuma.

## Open blockers

- `B-0001` — Falta incorporar o briefing/enunciado completo do case e seus materiais de entrada.

## Active tasks

- `BOOT-T001` — Revisar e fazer merge do bootstrap do sistema.
- `BOOT-T002` — Incorporar o briefing completo do case após o bootstrap.

## Pending decisions

- Definir prazo final e formato do deliverable após leitura do case.
- Definir stack/arquitetura técnica caso o case exija implementação de software.

## Next action

1. Revisar o PR de bootstrap.
2. Fazer merge.
3. Abrir um novo Orchestrator a partir do `STATE_VERSION 0001`.
4. Ingerir o case e converter requisitos em Phase 1.
5. Gerar a primeira wave paralela.

## Recovery point

Se qualquer chat ou wave falhar agora, retomar a partir de `STATE_VERSION 0001` e das Issues abertas. Nenhuma conclusão não integrada deve ser considerada canônica.
