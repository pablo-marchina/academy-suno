# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.1.0`

`STATE_VERSION: 0003`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case Intake & Problem Framing`

`LAST_COMMITTED_WAVE: SYSTEM-HARDENING`

## Objective

Construir o case Academy Suno com máxima velocidade usando múltiplos chats/agentes em paralelo, preservando continuidade exata por meio de estado canônico versionado no GitHub.

## Current truth

- Repositório canônico: `pablo-marchina/academy-suno`.
- O protocolo multi-chat foi integrado ao `main` pelo PR #1.
- Phase 0 está concluída e Phase 1 está aberta.
- O sistema possui guardrails executáveis: workflow de integridade, validador e CODEOWNERS.
- A Issue #2 (`BOOT-T002`) é a tarefa canônica de ingestão do briefing.
- O enunciado completo do case ainda não foi incorporado ao estado.
- Nenhuma wave de desenvolvimento do case foi executada ainda.

## Locked decisions

- `D-0001` — GitHub será a fonte canônica de verdade; memória de chats não será usada como mecanismo primário de continuidade.
- `D-0002` — Workers não atualizam arquivos canônicos; integração é responsabilidade exclusiva do Orchestrator.
- `D-0003` — Tarefas independentes serão executadas em waves paralelas e rastreadas por `TASK_ID` + `BASE_STATE_VERSION`.
- `D-0004` — Guardrails do sistema são executáveis no repositório e mudanças canônicas devem passar por validação automática.

## Active hypotheses

Nenhuma.

## Open blockers

- `B-0001` — Falta incorporar o briefing/enunciado completo do case e seus materiais de entrada.
- `B-0002` — A proteção administrativa do branch `main` ainda precisa ser ativada no GitHub para exigir o status check e bloquear bypass acidental.

## Active tasks

- `BOOT-T002` — `READY` — Issue #2 — incorporar briefing completo e preparar a primeira wave.

## Pending decisions

- Definir prazo final e formato do deliverable após leitura do case.
- Definir stack/arquitetura técnica caso o case exija implementação de software.
- Refinar o roadmap genérico para o case real.

## Next action

1. Ativar proteção/ruleset do `main` exigindo Pull Request e o check `validate-canonical-system`, sem force-push/deleção.
2. Abrir/usar o chat Orchestrator.
3. Ler `AGENTS.md`, arquivos canônicos e Issue #2.
4. Executar `CONTINUITY_CHECK` esperando `PROTOCOL_VERSION: 1.1.0` e `STATE_VERSION: 0003`.
5. Ingerir o briefing/material completo do case.
6. Atualizar framing da Phase 1 e gerar `W001` com o máximo de paralelismo seguro.

## Recovery point

Se qualquer chat, worker ou wave falhar, retomar a partir de `STATE_VERSION 0003` no `main` e da Issue #2. Nenhuma conclusão não integrada deve ser considerada canônica.
