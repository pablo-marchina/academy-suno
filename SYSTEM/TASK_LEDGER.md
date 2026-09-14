# TASK LEDGER

Somente o Orchestrator com lease ativo pode alterar este arquivo. GitHub Issues/PRs são a fila operacional; este ledger é o índice canônico resumido.

## Status permitidos

`PLANNED | READY | RUNNING | BLOCKED | RESULT_RECEIVED | INTEGRATED | CANCELLED | STALE`

## Bootstrap

| Task ID | Attempt | Base State | Base Commit | Role | Status | Dependencies | Issue / PR | Integrated State |
|---|---|---:|---|---|---|---|---|---|
| BOOT-T001 | A01 | 0001 | legacy | Orchestrator | INTEGRATED | none | PR #1 | 0002 |
| BOOT-T002 | A01 | 0004 | resolve-at-dispatch | Orchestrator | READY | BOOT-T001 | Issue #2 | — |

## Regras

1. Toda tentativa possui `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION` e `BASE_COMMIT_SHA`.
2. A Issue deve conter `TASK_ID` e `ATTEMPT_ID` no corpo; título deve conter pelo menos `TASK_ID`.
3. `RESULT_RECEIVED` não significa integrado.
4. Apenas após fan-in e commit do Orchestrator autorizado a tarefa muda para `INTEGRATED`.
5. Dependências usam IDs explícitos.
6. Resultado stale é classificado como `SAFE_TO_INTEGRATE`, `REVALIDATE` ou `DISCARD`.
7. Reexecução cria novo `ATTEMPT_ID`; tentativa anterior não é apagada.
8. Para waves, o manifest `SYSTEM/WAVES/W###.json` é a fonte do DAG e este ledger é o índice resumido.

## Próxima wave

Ainda não criada. Após incorporar o briefing, o Orchestrator deve criar `W001.json`, registrar o SHA base do `main` e disparar todas as tarefas inicialmente `READY`.
