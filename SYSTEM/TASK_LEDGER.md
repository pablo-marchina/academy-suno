# TASK LEDGER

Somente o Orchestrator pode alterar este arquivo. GitHub Issues são a fila operacional; este ledger é o índice canônico resumido.

## Status permitidos

`PLANNED | READY | RUNNING | BLOCKED | RESULT_RECEIVED | INTEGRATED | CANCELLED | STALE`

## Bootstrap

| Task ID | Base State | Role | Status | Dependencies | Issue | Integrated State |
|---|---:|---|---|---|---|---|
| BOOT-T001 | 0001 | Orchestrator | RUNNING | none | PR bootstrap | — |
| BOOT-T002 | 0001 | Orchestrator | BLOCKED | BOOT-T001 | — | — |

## Regras

1. Uma Issue deve conter o `TASK_ID` no título ou no início do corpo.
2. O worker deve declarar o `BASE_STATE_VERSION` no resultado.
3. `RESULT_RECEIVED` não significa integrado.
4. Apenas após fan-in e commit do Orchestrator a tarefa muda para `INTEGRATED` e recebe `Integrated State`.
5. Dependências devem ser IDs explícitos, nunca descrições vagas.
6. Tarefa stale não é descartada automaticamente: o Orchestrator classifica como `SAFE_TO_INTEGRATE`, `REVALIDATE` ou `DISCARD`.

## Próxima wave

Ainda não criada. O Orchestrator deve criá-la após incorporar o briefing do case.
