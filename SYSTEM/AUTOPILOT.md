# AUTOPILOT — Total Success Optimization Loop

## Objective

Minimizar intervenção humana enquanto o sistema maximiza `expected_total_success` conforme `SYSTEM/SUCCESS_MODEL.md`.

## Orchestrator loop

1. ler STATE, Success/Partner/Quality models e scorecards;
2. reconstruir lifecycle das tasks ativas a partir de `SYSTEM/TASK_SIGNALS.md`, comentários das Issues, branches e RESULTs;
3. validar Case Contract, Partner Contract, Traceability e Assumption/Risk Register;
4. se houver hard gate FAIL, atacar o mais crítico;
5. senão identificar a dimensão/bottleneck que mais limita sucesso;
6. gerar automaticamente tasks/Issues/DAG/dispatches;
7. executar em paralelo tudo que for independente e útil;
8. validar provenance/staleness e integrar apenas melhoria defensável;
9. atualizar traceability/assumptions/scorecards;
10. executar juries/red-team/evaluator quando material;
11. reavaliar caso+solução completos;
12. repetir até Success stop condition PASS.

## Runtime task reconstruction

O Orchestrator não pergunta ao usuário se um worker começou. Para cada attempt ativo:

```text
no valid start/result             -> READY
TASK_STARTED/PROGRESS, no terminal -> RUNNING
TASK_COMPLETE + valid RESULT       -> RESULT_RECEIVED
TASK_BLOCKED                       -> BLOCKED
TASK_STALE / invalid provenance    -> STALE
accepted canonical integration     -> INTEGRATED
```

Branch/commit/result sem signals pode ser usado como fallback legado para attempts anteriores ao protocolo 1.6.0. Para attempts novos, missing signal é finding de protocolo.

`RUNNING` significa “iniciado, sem terminal observado”, não promessa de execução em background. Se liveness ficar incerta em ciclos posteriores, o Orchestrator pode inspecionar branch/commits e abrir novo attempt quando o risco de critical path justificar; nunca reutilizar attempt ID.

## Task priority

Prioridade aproximada:

```text
hard_gate_criticality
+ expected_total_success_uplift
+ uncertainty_reduction
+ critical_path_value
- time_cost
- execution_risk
```

Não use fórmula como precisão falsa; use-a para ordenar decisões explicitamente.

## Human involvement

Reservado a: materiais inacessíveis, permissões/admin, decisão externa genuína, abrir novos workers quando necessário e `HUMAN_DECISION_REQUIRED`. O usuário não desenha prompts, não escolhe workers rotineiramente e não transporta status/resultados entre chats.

## Dispatch requirement

Cada dispatch informa `SUCCESS_TARGETS`, requirement/pain refs, assumption refs, objetivo, dependências, evidências, DoD, persistência, Issue e formato RESULT. Em protocolo 1.6.0+, inclui a obrigação explícita de `TASK_STARTED` e terminal conforme `TASK_SIGNALS.md`.

## Deadline mode

Quando deadline/finalization reserve estiver ativo, priorizar hard gates, integração, artifact QA, blind review e submission. Não abrir exploração especulativa sem impacto material esperado.

## Finalization

Rodar `FINAL_REVIEW_PROTOCOL.md`. Só finalizar com Success + Partner + Quality PASS.
