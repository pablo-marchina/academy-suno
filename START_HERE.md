# START HERE — Operação Multi-Chat

Este repositório é a memória externa do projeto. O objetivo é permitir muitos chats ChatGPT em paralelo sem depender do tamanho de uma conversa.

## Como iniciar uma sessão

1. Abra o repositório conectado no ChatGPT.
2. No chat Orchestrator, peça para ler `AGENTS.md`, `SYSTEM/CONSTITUTION.md`, `SYSTEM/STATE.md`, `SYSTEM/ROADMAP.md`, `SYSTEM/DECISIONS.md` e as Issues abertas.
3. O Orchestrator calcula a próxima **wave** de tarefas paralelizáveis.
4. Cada tarefa vira uma GitHub Issue com `TASK_ID` e `BASE_STATE_VERSION`.
5. Abra um chat por tarefa/Issue e mande o worker executar sua Issue.
6. Cada worker publica/retorna um `RESULT` estruturado.
7. O Orchestrator faz fan-in, valida resultados, roda crítica/auditoria e atualiza os arquivos canônicos.
8. Comece a próxima wave.

## Convenção de chats

```text
00 — ORCHESTRATOR — v01
10 — RESEARCH — R001-T001
11 — RESEARCH — R001-T002
20 — ANALYSIS — R001-T003
30 — SYNTHESIS — R001
40 — RED TEAM — R001
50 — AUDITOR — R001
60 — WRITER / BUILD — conforme fase
```

Não é necessário manter sempre os mesmos chats. O nome identifica papel e escopo; o repositório preserva continuidade.

## Rotação preventiva

Não esperamos o chat chegar ao limite. Recomenda-se:

- Orchestrator: rotacionar após 6–8 waves ou quando respostas começarem a perder precisão contextual.
- Worker: preferencialmente um chat por tarefa grande ou por pequeno conjunto de tarefas relacionadas.
- Synthesizer/Critic/Auditor: rotacionar após 8–10 waves.

Na troca, o chat antigo gera `HANDOFF`; o novo faz `CONTINUITY_CHECK` contra o estado canônico.

## Regra de commit

Uma wave só é considerada integrada após:

1. resultados das tarefas obrigatórias recebidos;
2. checagem de staleness;
3. síntese;
4. red-team quando aplicável;
5. decisão do Orchestrator;
6. atualização de `STATE`, `DECISIONS` e `TASK_LEDGER`;
7. incremento de `STATE_VERSION`.

Se a execução for interrompida antes disso, o último `STATE_VERSION` permanece válido e a wave pode ser retomada/reexecutada.

## Comando padrão para um novo Orchestrator

```text
Você é o Orchestrator deste projeto. Use o GitHub como fonte de verdade.
Leia AGENTS.md e todos os arquivos canônicos em SYSTEM/.
Leia as Issues abertas.
Execute CONTINUITY_CHECK.
Depois identifique o caminho crítico, monte a próxima wave com o máximo de paralelismo seguro e crie/especifique as tarefas necessárias.
Não altere decisões LOCKED silenciosamente.
```

## Comando padrão para um Worker

```text
Você é um worker deste projeto. Use o GitHub como fonte de verdade.
Leia AGENTS.md, SYSTEM/CONSTITUTION.md, SYSTEM/STATE.md e a Issue atribuída.
Execute CONTINUITY_CHECK.
Faça somente a tarefa pedida, maximize profundidade dentro do escopo e finalize no formato RESULT definido em AGENTS.md.
Não altere arquivos canônicos.
```
