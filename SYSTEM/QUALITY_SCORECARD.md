# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0009`

`QUALITY_STATUS: REPAIR_TELEMETRY_CORE_EXECUTABLE`

`STOP_CONDITION: FAIL`

## Case Contract status

- Objective: `KNOWN`
- Mandatory deliverables: `6 DELIVERABLES IDENTIFIED`
- Explicit evaluation criteria: `REQUIREMENTS/HARD GATES IDENTIFIED`
- Evaluation weights/scale: `NOT PROVIDED`
- Audience: `3 OUTPUT AUDIENCES KNOWN / FINAL EVALUATOR UNKNOWN`
- Constraints/deadline: `SCOPE + VIDEO HARD GATE KNOWN / DATE UNKNOWN`
- Partner Outcome linkage: `VALUE_HYPOTHESIS_SUPPORTED_EXECUTION_PARTIAL`

## Current evaluation

W003-T006/T007 provaram targeted repair mensurável e telemetry auditável sem relaxar hard gates. O próximo gate de qualidade é calibration/ablation: confusion matrices reproduzíveis, anti-gaming e decisão explícita sobre quais audience/semantic signals permanecem diagnósticos.

## Hard gates

Status: `ACTIVE_CALIBRATION_RELEASE_GATE`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`: explicit graph/state + persistent RunStore;
2. cobertura 3 níveis × 3 formatos — `FOUNDATION_PASS`: 9-job planner + native schemas; provider generation quality ainda não medida;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`: source/factual/policy precedence + claim HybridDecision; semantic sensor secundário;
4. legibilidade PT-BR calibrada — `IMPLEMENTED_DIAGNOSTIC_ONLY`: versão controlada existe; T008 decide calibration posture;
5. densidade/contextualização de termos financeiros — `IMPLEMENTED_DIAGNOSTIC_ONLY`: ontology + ACV + anti-gaming existem;
6. factuality/grounding contra fonte — `CORE_PASS_PARTIAL_SCOPE`: deterministic + claim layer; semantic incremental value pendente ablation;
7. auto-correção com feedback mensurável — `CONTROLLED_PROOF_PASS`: failure-code-driven targeted repair, fresh hard-gate re-runs, immutable siblings, bounded stops;
8. interface comparativa com métricas/rastreabilidade — `DESIGNED_NOT_BUILT`;
9. testes automatizados/reprodutíveis — `STRONG_PASS_CORE`: Foundation Regression/System Integrity + focused suites;
10. matriz de confusão dos níveis — `T008 READY`;
11. análise custo/latência — `TELEMETRY_CONTRACT_PASS / REAL_PROVIDER_COST_PENDING`;
12. README/documentação reproduzível — `PENDING`;
13. vídeo real comprovando código/interface — `PENDING`;
14. vídeo <=5:00 — `CONTROLLED_BY_PLAN`.

## New evidence

- targeted repair focused suite 7/7 PASS; controlled one-attempt acceptance after fresh source/factual/policy re-evaluation;
- telemetry focused suite 6/6 PASS; latency/retry/repair/usage/cost semantics versioned and auditável;
- no cost is invented when provider usage/pricing is absent; demo price is synthetic only;
- T006 and T007 worker heads both passed System Integrity and Foundation Regression before integration.

## Open quality gaps

1. Calibration/ablation/confusion matrix sobre development gold, held-out isolado e anti-gaming release gate.
2. Independent human agreement suficiente para qualquer threshold freeze; se ausente, manter diagnóstico.
3. Provider/model measured comparison somente quando houver evidence suficiente.
4. Evidence cockpit, README/report, end-to-end release proof, video e final reviews.

## Next quality action

Executar W003-T008; depois liberar T009 para proof/synthesis end-to-end sem promover thresholds/provider/backend por preferência.
