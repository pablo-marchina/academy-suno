# START HERE — Operação Multi-Chat

Este repositório é a memória externa e o plano de execução do projeto. O objetivo é permitir muitos chats ChatGPT em paralelo sem depender do tamanho de uma conversa.

## Arquitetura operacional

```text
main (verdade canônica)
   ↓
STATE + checkpoint + wave DAG
   ↓
ready queue
   ↓
workers em branches/issues independentes
   ↓
resultados persistidos no GitHub
   ↓
Orchestrator com lease ativo
   ↓
fan-in / red-team / auditoria
   ↓
PR canônico + CI
   ↓
STATE vN+1
```

## Como iniciar uma sessão Orchestrator

1. Leia `AGENTS.md`, `SYSTEM/CONSTITUTION.md`, `SYSTEM/STATE.md`, `SYSTEM/ROADMAP.md`, `SYSTEM/DECISIONS.md`, `SYSTEM/TASK_LEDGER.md` e waves ativas.
2. Resolva o SHA atual do `main`.
3. Leia `SYSTEM/ORCHESTRATOR_LEASE.md`.
4. Leia a branch `control/orchestrator-lease` e adquira/transfira o lease usando o blob SHA observado.
5. Execute `CONTINUITY_CHECK` incluindo `main_commit_sha` e o `holder_session_id` do lease.
6. Só então planeje/integre trabalho canônico.

## Como iniciar um Worker

1. Leia `AGENTS.md`, `SYSTEM/CONSTITUTION.md`, `SYSTEM/STATE.md` e a Issue atribuída.
2. Confirme `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION` e `BASE_COMMIT_SHA`.
3. Execute `CONTINUITY_CHECK`.
4. Se for modificar arquivos, use branch exclusiva da tentativa.
5. Execute somente o escopo pedido e persista o resultado na Issue/PR/artefato.

## Convenção de chats

```text
00 — ORCHESTRATOR — ORCH-G### — S###
10 — RESEARCH — W###-T### — A##
20 — ANALYSIS — W###-T### — A##
30 — SYNTHESIS — W###
40 — RED TEAM — W###
50 — AUDITOR — W###
60 — WRITER / BUILD — W###-T### — A##
```

Não é necessário manter os mesmos chats. O GitHub preserva a continuidade.

## Ready queue em vez de rodadas rígidas

Cada wave tem um manifest `SYSTEM/WAVES/W###.json` com dependências explícitas. O Orchestrator dispara todas as tarefas `READY` em paralelo. Quando uma dependência termina, o dependente pode começar imediatamente; não é necessário esperar todas as tarefas da wave.

## Rotação preventiva

- Orchestrator: após 6–8 waves por padrão ou antes se houver perda de precisão contextual.
- Worker: preferencialmente um chat por tarefa grande/tentativa.
- Synthesizer/Critic/Auditor: após 8–10 waves.

Ao rotacionar Orchestrator, faça handoff e transfira o lease. Nunca deixe dois chats com o mesmo `holder_session_id` operando em paralelo.

## Regra de integração

Uma mudança canônica só é considerada integrada após:

1. lease do Orchestrator revalidado;
2. resultados obrigatórios recebidos e persistidos;
3. `TASK_ID + ATTEMPT_ID` validados;
4. checagem de `BASE_STATE_VERSION + BASE_COMMIT_SHA`;
5. síntese/red-team conforme aplicável;
6. checkpoint `STATE-v####` criado;
7. `STATE_VERSION` incrementado exatamente em 1;
8. PR aprovado pelo `System Integrity`;
9. merge no `main`.

Se a execução for interrompida antes do merge, o último estado no `main` continua válido.

## Comando padrão para novo Orchestrator

```text
Você é o Orchestrator deste projeto. Use o GitHub como fonte de verdade.
Leia AGENTS.md e os arquivos canônicos em SYSTEM/.
Resolva o SHA atual do main e leia o lease em control/orchestrator-lease.
Adquira/transfira o lease conforme SYSTEM/ORCHESTRATOR_LEASE.md.
Execute CONTINUITY_CHECK.
Depois identifique o caminho crítico, atualize a ready queue do DAG e dispare o máximo de tarefas independentes com segurança.
Antes de qualquer integração canônica, revalide o lease.
Não altere decisões LOCKED silenciosamente.
```

## Comando padrão para Worker

```text
Você é um worker deste projeto. Use o GitHub como fonte de verdade.
Leia AGENTS.md, SYSTEM/CONSTITUTION.md, SYSTEM/STATE.md e a Issue atribuída.
Valide TASK_ID, ATTEMPT_ID, BASE_STATE_VERSION e BASE_COMMIT_SHA.
Execute CONTINUITY_CHECK.
Faça somente a tarefa pedida e finalize no formato RESULT.
Persista o resultado no GitHub. Não altere arquivos canônicos.
```
