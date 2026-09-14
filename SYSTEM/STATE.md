# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.0.0`

`STATE_VERSION: 0002`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case Intake & Problem Framing`

`LAST_COMMITTED_WAVE: BOOTSTRAP`

## Objective

Construir o case Academy Suno com máxima velocidade usando múltiplos chats/agentes em paralelo, preservando continuidade exata por meio de estado canônico versionado no GitHub.

## Current truth

- Repositório canônico: `pablo-marchina/academy-suno`.
- O protocolo multi-chat foi integrado ao `main` pelo PR #1.
- Phase 0 está concluída.
- Phase 1 está aberta.
- A Issue #2 (`BOOT-T002`) é a tarefa canônica de ingestão do briefing.
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

- `BOOT-T002` — `READY` — Issue #2 — incorporar briefing completo e preparar a primeira wave.

## Pending decisions

- Definir prazo final e formato do deliverable após leitura do case.
- Definir stack/arquitetura técnica caso o case exija implementação de software.
- Refinar o roadmap genérico para o case real.

## Next action

1. Abrir/usar o chat Orchestrator.
2. Ler `AGENTS.md`, arquivos canônicos e Issue #2.
3. Executar `CONTINUITY_CHECK` esperando `STATE_VERSION: 0002`.
4. Ingerir o briefing/material completo do case.
5. Atualizar framing da Phase 1.
6. Gerar `W001` com o máximo de paralelismo seguro.

## Recovery point

Se qualquer chat falhar, retomar a partir de `STATE_VERSION 0002` e da Issue #2. Nenhuma conclusão não integrada deve ser considerada canônica.
