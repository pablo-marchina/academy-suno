# TASK LEDGER

Somente o Orchestrator com lease ativo pode alterar este arquivo.

## Status permitidos
`PLANNED | READY | RUNNING | BLOCKED | RESULT_RECEIVED | INTEGRATED | CANCELLED | STALE`

## Bootstrap

| Task ID | Attempt | Base State | Base Commit | Role | Status | Dependencies | Issue / PR | Integrated State |
|---|---|---:|---|---|---|---|---|---|
| BOOT-T001 | A01 | 0001 | legacy | Orchestrator | INTEGRATED | none | PR #1 | 0002 |
| BOOT-T002 | A01 | 0006 | resolve-at-dispatch | Orchestrator | READY | BOOT-T001 | Issue #2 | — |

## Regras

1. Toda tentativa possui identidade e proveniência completas.
2. `RESULT_RECEIVED` não significa integrado.
3. Integração exige Orchestrator autorizado.
4. Reexecução cria novo attempt.
5. Wave manifest é fonte do DAG.
6. Toda tarefa deve apontar primeiro para Partner Value gap/hard gate/unknown material, ou para requisito obrigatório/Quality gap; tarefas sem contribuição identificável são despriorizadas.
7. Uma tarefa de apresentação nunca toma precedência sobre um gap crítico de dor, causa, valor, viabilidade ou adoção.

## Próxima wave

Após `BOOT-T002`, criar `W001.json` a partir dos unknowns/gaps de maior impacto no Partner Contract e Case Contract, calibrar ambos scorecards e disparar toda ready queue segura.
