# AGENTS.md — Academy Suno

Estas instruções valem para qualquer chat/agente que trabalhe neste repositório.

## Regra zero

O histórico de uma conversa **não é a fonte de verdade**. A fonte de verdade é o repositório, nesta ordem:

1. `SYSTEM/CONSTITUTION.md` — protocolo e regras imutáveis de operação.
2. `SYSTEM/STATE.md` — estado canônico atual do projeto.
3. `SYSTEM/ROADMAP.md` — fases, gates e critérios de conclusão.
4. `SYSTEM/DECISIONS.md` — decisões aceitas/reabertas.
5. GitHub Issues abertas — tarefas ativas e resultados ainda não integrados.
6. `SYSTEM/TASK_LEDGER.md` — índice de tarefas integradas e status global.

## Bootstrap obrigatório de qualquer novo chat

Antes de trabalhar:

1. Leia os cinco arquivos acima.
2. Identifique `PROTOCOL_VERSION` e `STATE_VERSION`.
3. Identifique seu papel e a tarefa/Issue atribuída.
4. Confirme explicitamente:

```text
CONTINUITY_CHECK
protocol_version: <valor>
state_version: <valor>
role: <papel>
task_id: <id ou NONE>
status: PASS | FAIL
```

Se o estado da tarefa for anterior ao estado canônico, marque `STALE_INPUT` e não integre conclusões automaticamente.

## Autoridade

- **Orchestrator**: único papel autorizado a atualizar `SYSTEM/STATE.md`, `SYSTEM/ROADMAP.md`, `SYSTEM/DECISIONS.md` e `SYSTEM/TASK_LEDGER.md`.
- **Workers**: nunca alteram arquivos canônicos. Trabalham na Issue atribuída e entregam resultado estruturado como comentário ou artefato próprio.
- **Synthesizer**: consolida resultados, mas não faz commit canônico sem ação do Orchestrator.
- **Critic/Red Team**: procura falhas, contradições, evidência ausente e risco.
- **Auditor**: verifica conformidade do protocolo e continuidade; não redefine estratégia.

## Concorrência

Tarefas independentes devem ser executadas em paralelo. Cada tarefa precisa declarar:

- `TASK_ID`
- `BASE_STATE_VERSION`
- dependências
- papel responsável
- objetivo
- definição de pronto
- formato de saída

Workers não devem esperar por tarefas sem dependência explícita.

## Entrega de worker

Toda entrega deve terminar com:

```text
RESULT
TASK_ID: ...
BASE_STATE_VERSION: ...
STATUS: COMPLETE | PARTIAL | BLOCKED | STALE
CONFIDENCE: 0-100

FINDINGS:
- ...

EVIDENCE:
- ...

STATE_DELTA_PROPOSED:
- ...

DECISIONS_PROPOSED:
- ...

OPEN_RISKS:
- ...

NEXT_ACTIONS:
- ...
```

## Preservação de contexto

Nunca dependa de “lembrar” uma conversa antiga. Ao rotacionar um chat, gere um handoff usando `SYSTEM/TEMPLATES.md` e inicie o novo chat a partir dos arquivos canônicos.

## Segurança contra drift

Uma decisão marcada `LOCKED` só pode ser alterada por `DECISION_REVIEW` explícita do Orchestrator com justificativa e nova evidência.

## Princípio de velocidade

O objetivo operacional é minimizar o caminho crítico: maximizar fan-out de tarefas independentes, fazer fan-in somente quando necessário e evitar que um chat monopolize pesquisa, análise e revisão sequencialmente.
