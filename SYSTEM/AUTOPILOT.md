# AUTOPILOT — Total Success Optimization Loop

## Objective

Minimizar intervenção humana enquanto o sistema maximiza `expected_total_success` conforme `SYSTEM/SUCCESS_MODEL.md`.

## Orchestrator loop

1. ler STATE, Success/Partner/Quality models e scorecards;
2. validar Case Contract, Partner Contract, Traceability e Assumption/Risk Register;
3. se houver hard gate FAIL, atacar o mais crítico;
4. senão identificar a dimensão/bottleneck que mais limita sucesso;
5. gerar automaticamente tasks/Issues/DAG/dispatches;
6. executar em paralelo tudo que for independente e útil;
7. validar provenance/staleness e integrar apenas melhoria defensável;
8. atualizar traceability/assumptions/scorecards;
9. executar juries/red-team/evaluator quando material;
10. reavaliar caso+solução completos;
11. repetir até Success stop condition PASS.

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

Reservado a: materiais inacessíveis, permissões/admin, decisão externa genuína, abrir novos workers quando necessário e `HUMAN_DECISION_REQUIRED`. O usuário não desenha prompts nem escolhe workers rotineiramente.

## Dispatch requirement

Cada dispatch informa `SUCCESS_TARGETS`, requirement/pain refs, assumption refs, objetivo, dependências, evidências, DoD, persistência e formato RESULT.

## Deadline mode

Quando deadline/finalization reserve estiver ativo, priorizar hard gates, integração, artifact QA, blind review e submission. Não abrir exploração especulativa sem impacto material esperado.

## Finalization

Rodar `FINAL_REVIEW_PROTOCOL.md`. Só finalizar com Success + Partner + Quality PASS.
