# AUTOPILOT — Total Success Optimization Loop

## Objective

Minimizar intervenção humana enquanto o sistema maximiza `expected_total_success` conforme `SYSTEM/SUCCESS_MODEL.md`, obedecendo `SYSTEM/PRODUCTION_CONTRACT.md` e `SYSTEM/DECISION_RESEARCH_GATE.md`.

## Orchestrator loop

1. ler STATE, Success/Partner/Quality models e scorecards + Production Contract;
2. reconstruir lifecycle das tasks ativas a partir de `SYSTEM/TASK_SIGNALS.md`, comentários das Issues, branches e RESULTs;
3. validar Case Contract, Partner Contract, Production Contract, Traceability e Assumption/Risk Register;
4. se houver hard gate FAIL, atacar o mais crítico;
5. se a próxima implementação depender de decisão material ainda não research-gated, gerar primeiro research/bakeoff tasks conforme DRG;
6. senão identificar a dimensão/bottleneck que mais limita sucesso;
7. gerar automaticamente tasks/Issues/DAG/dispatches;
8. executar em paralelo tudo que for independente e útil;
9. validar provenance/staleness e integrar apenas melhoria defensável;
10. executar regression/evals quantitativos quando a mudança afetar comportamento probabilístico ou produção;
11. atualizar traceability/assumptions/scorecards/decision records;
12. executar juries/red-team/evaluator/security/reliability review quando material;
13. reavaliar caso+produto+evidência completos;
14. repetir até Success stop condition PASS.

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

## Material decision gate

Antes de congelar ou implementar como produção uma escolha material ainda aberta:

```text
question → alternatives → systematic research → representative benchmark
→ hard gates → trade-off evidence → decision/no-preference → reversal conditions
```

Spikes/benchmarks podem ser executados em branches isoladas. Nenhum worker promove sua própria tecnologia. O Orchestrator integra a decisão somente quando o DRG passa.

## Quantitative-first policy

Quando mensurável, tarefas devem persistir dados e não apenas opinião: factual/numeric/entity/concept preservation, confusion/calibration, latency p50/p95/p99, throughput, cost, errors/retries, queue time, resource use, recovery e security/authz outcomes conforme escopo. Valores arbitrários não viram production thresholds.

## Adaptive-vs-deterministic policy

- deterministic/fail-closed: source trust, factual criticals, policy/compliance, schema, provenance, tenant isolation, authz;
- adaptive candidates: model/provider, prompt, retrieval, repair strategy, budget, parallelism, semantic sensor sampling;
- toda adaptação é versionada/telemetrada e não pode relaxar hard gates.

## Production path

Priorizar a evolução do único produto real. Não criar frontend/demo paralelo com respostas fake. O vídeo obrigatório deve capturar o produto real. `PRODUCTION_READY` só pode existir com evidência operacional do Production Contract.

## Task priority

Prioridade aproximada:

```text
hard_gate_criticality
+ expected_total_success_uplift
+ uncertainty_reduction
+ critical_path_value
+ production_risk_reduction
- time_cost
- execution_risk
```

Não use fórmula como precisão falsa; use-a para ordenar decisões explicitamente.

## Human involvement

Reservado a: materiais inacessíveis, permissões/admin, decisão externa genuína, evidência humana quando uma classe `HUMAN_GOLD` for realmente necessária, abrir novos workers quando necessário e `HUMAN_DECISION_REQUIRED`. O usuário não desenha prompts, não escolhe workers rotineiramente e não transporta status/resultados entre chats.

## Dispatch requirement

Cada dispatch informa `SUCCESS_TARGETS`, requirement/pain/production refs, assumption refs, objetivo, dependências, evidências, DRG applicability, DoD, persistência, Issue e formato RESULT. Em protocolo 1.6.0+, inclui a obrigação explícita de `TASK_STARTED` e terminal conforme `TASK_SIGNALS.md`.

## Deadline mode

Quando deadline/finalization reserve estiver ativo, priorizar hard gates, integração, artifact QA, blind review e submission. Não abrir exploração especulativa sem impacto material esperado.

## Finalization

Rodar `FINAL_REVIEW_PROTOCOL.md`. Só finalizar com Success + Partner + Quality PASS e Production Contract PASS aplicável aos claims finais.
