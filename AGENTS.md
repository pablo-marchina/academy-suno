# AGENTS.md — Academy Suno

Estas instruções valem para qualquer chat/agente que trabalhe neste repositório.

## Regra zero

O histórico de uma conversa **não é a fonte de verdade**. A fonte de verdade é o repositório, nesta ordem:

1. `SYSTEM/CONSTITUTION.md` — protocolo e regras de operação.
2. `SYSTEM/STATE.md` — estado canônico atual do projeto.
3. `SYSTEM/ROADMAP.md` — fases, gates e critérios de conclusão.
4. `SYSTEM/DECISIONS.md` — decisões aceitas/reabertas.
5. `SYSTEM/TASK_LEDGER.md` — índice canônico de tarefas.
6. `SYSTEM/WAVES/W###.json` — manifests executáveis das waves.
7. GitHub Issues/PRs — fila operacional e resultados ainda não integrados.
8. `SYSTEM/KNOWLEDGE_INDEX.md` — índice de conhecimento/evidências.

## Bootstrap obrigatório de qualquer novo chat

Antes de trabalhar:

1. Leia `AGENTS.md` e os arquivos canônicos aplicáveis.
2. Identifique `PROTOCOL_VERSION`, `STATE_VERSION` e o SHA atual do `main`.
3. Identifique seu papel, `TASK_ID` e `ATTEMPT_ID`, quando houver.
4. Confirme explicitamente:

```text
CONTINUITY_CHECK
protocol_version: <valor>
state_version: <valor>
main_commit_sha: <40 hex>
role: <papel>
task_id: <id ou NONE>
attempt_id: <A## ou NONE>
orchestrator_lease: <lease/session ou N/A>
status: PASS | FAIL
```

Se qualquer referência da tarefa divergir do estado/commit esperado, marque `STALE_INPUT` e não integre conclusões automaticamente.

## Autoridade e lease do Orchestrator

- Existe no máximo um Orchestrator com autoridade de integração por vez.
- O lease dinâmico vive na branch `control/orchestrator-lease`, arquivo `SYSTEM/ORCHESTRATOR_LEASE.json`.
- O lease é adquirido/transferido por update baseado no blob SHA observado (compare-and-swap). Conflito de SHA significa que outro agente venceu; recarregue e não prossiga.
- Antes de abrir/atualizar PR que altere estado canônico, o Orchestrator deve reler o lease e confirmar `status=ACTIVE` e seu `holder_session_id`.
- Workers, Synthesizer, Critic e Auditor nunca adquirem lease de integração.
- **Orchestrator ativo**: único papel autorizado a atualizar `SYSTEM/STATE.md`, `SYSTEM/ROADMAP.md`, `SYSTEM/DECISIONS.md`, `SYSTEM/TASK_LEDGER.md`, checkpoints e manifests canônicos.
- **Workers**: nunca alteram arquivos canônicos. Trabalham na Issue/branch atribuída e entregam resultado estruturado.

Detalhes completos: `SYSTEM/ORCHESTRATOR_LEASE.md`.

## Proveniência obrigatória de task

Toda tentativa de tarefa precisa declarar:

- `TASK_ID`
- `ATTEMPT_ID` (`A01`, `A02`, ...)
- `BASE_STATE_VERSION`
- `BASE_COMMIT_SHA` (SHA completo do `main` usado no dispatch)
- dependências
- papel responsável
- objetivo
- definição de pronto
- formato de saída

`TASK_ID + ATTEMPT_ID` é a chave idempotente de execução. Uma nova tentativa nunca reutiliza o mesmo `ATTEMPT_ID`.

## Paralelismo e branches

- Tarefas independentes devem ser executadas em paralelo.
- Workers não esperam por tarefas sem dependência explícita.
- Trabalho em arquivos deve usar branch isolada por tentativa, preferencialmente `task/<TASK_ID>-<ATTEMPT_ID>-<slug>`.
- Nunca use vários workers escrevendo na mesma branch.
- O Orchestrator usa o manifest de wave/DAG para disparar tudo que estiver `READY`; não precisa esperar a wave inteira para liberar dependentes já desbloqueados.

## Entrega de worker

Toda entrega deve terminar com:

```text
RESULT
TASK_ID: ...
ATTEMPT_ID: A##
BASE_STATE_VERSION: ...
BASE_COMMIT_SHA: <40 hex>
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

ARTIFACT_REFS:
- Issue/PR/path: ...

NEXT_ACTIONS:
- ...
```

O resultado deve existir no GitHub (Issue/PR/artefato), nunca exclusivamente no chat.

## Checkpoints e recuperação

Todo incremento de `STATE_VERSION` exige um snapshot idêntico em `SYSTEM/CHECKPOINTS/STATE-v####.md`. O `STATE.md` corrente é mutável; checkpoints são append-only. Se uma integração falhar, o último checkpoint presente no `main` permanece o recovery point.

## Preservação de contexto

Nunca dependa de “lembrar” uma conversa antiga. Ao rotacionar um chat, gere um handoff usando `SYSTEM/TEMPLATES.md`; o novo chat reconstrói o contexto dos arquivos canônicos e valida o lease se for Orchestrator.

## Segurança contra drift

Uma decisão marcada `LOCKED` só pode ser alterada por `DECISION_REVIEW` explícita do Orchestrator com justificativa e nova evidência.

## Princípio de velocidade

O objetivo operacional é minimizar o caminho crítico: maximizar fan-out de tarefas independentes, liberar dependentes assim que suas dependências fecharem, fazer micro-fan-ins quando útil e evitar que um chat monopolize pesquisa, análise e revisão sequencialmente.
