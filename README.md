# Academy Suno

Repositório canônico para o desenvolvimento do case Academy Suno.

O projeto será operado com múltiplos chats/agentes ChatGPT em paralelo, coordenados por um protocolo versionado e checkpoints persistidos neste repositório. A memória de uma conversa não é usada como fonte principal de continuidade.

## Comece aqui

1. Leia [`START_HERE.md`](START_HERE.md).
2. Todo chat deve obedecer [`AGENTS.md`](AGENTS.md).
3. O estado oficial está em [`SYSTEM/STATE.md`](SYSTEM/STATE.md).
4. As regras permanentes estão em [`SYSTEM/CONSTITUTION.md`](SYSTEM/CONSTITUTION.md).
5. As fases e gates estão em [`SYSTEM/ROADMAP.md`](SYSTEM/ROADMAP.md).

## Control plane

| Arquivo | Função |
|---|---|
| `SYSTEM/CONSTITUTION.md` | protocolo, autoridade, concorrência, rotação e recovery |
| `SYSTEM/STATE.md` | ponto exato atual e próxima ação |
| `SYSTEM/ROADMAP.md` | fases e critérios de passagem |
| `SYSTEM/DECISIONS.md` | decisões versionadas e protegidas contra drift |
| `SYSTEM/TASK_LEDGER.md` | índice canônico de tasks/waves |
| `SYSTEM/KNOWLEDGE_INDEX.md` | evidências e conhecimento consolidado |
| `SYSTEM/AGENT_ROLES.md` | papéis e prompts-base dos chats |
| `SYSTEM/TEMPLATES.md` | Task, Result, Wave, Handoff, Audit e Decision Review |

## Modelo de execução

```text
STATE vN
   ↓
Orchestrator cria DAG + Wave
   ↓
┌────────┬────────┬────────┬────────┐
│Worker A│Worker B│Worker C│Worker D│  ← paralelo
└────────┴────────┴────────┴────────┘
   ↓
Synthesis → Red Team → Audit
   ↓
Orchestrator integra
   ↓
STATE vN+1
```

GitHub Issues são a fila operacional de tarefas. Workers entregam resultados na Issue ou em artefatos isolados; somente o Orchestrator modifica os arquivos canônicos.

## Princípio de continuidade

Qualquer chat pode ser descartado e recriado. O novo chat lê os arquivos canônicos, executa `CONTINUITY_CHECK` e retoma do último `STATE_VERSION` comprometido.
