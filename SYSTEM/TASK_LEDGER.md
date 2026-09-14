# TASK LEDGER

Somente o Orchestrator com lease ativo pode alterar este arquivo.

## Status permitidos
`PLANNED | READY | RUNNING | BLOCKED | RESULT_RECEIVED | INTEGRATED | CANCELLED | STALE`

## Bootstrap

| Task ID | Attempt | Base State | Base Commit | Role | Status | Dependencies | Issue / PR | Integrated State |
|---|---|---:|---|---|---|---|---|---|
| BOOT-T001 | A01 | 0001 | legacy | Orchestrator | INTEGRATED | none | PR #1 | 0002 |
| BOOT-T002 | A01 | 0005 | resolve-at-dispatch | Orchestrator | READY | BOOT-T001 | Issue #2 | — |

## Regras

1. Toda tentativa possui identidade e proveniência completas.
2. `RESULT_RECEIVED` não significa integrado.
3. Integração exige Orchestrator autorizado.
4. Reexecução cria novo attempt.
5. Wave manifest é fonte do DAG.
6. Toda tarefa deve apontar para requisito, dependência, hard gate ou gap do Quality Scorecard; tarefas sem contribuição identificável devem ser despriorizadas.

## Próxima wave

Após `BOOT-T002`, criar `W001.json` a partir dos gaps de maior impacto do Case Contract/Quality Scorecard e disparar toda ready queue segura.
