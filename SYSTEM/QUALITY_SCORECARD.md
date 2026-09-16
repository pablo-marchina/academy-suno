# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0008`

`QUALITY_STATUS: GRAPH_GROUNDING_AUDIENCE_CORE_EXECUTABLE`

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

W003-T001…T005 provaram explicit graph/state persistence, claim grounding core, audience diagnostics anti-gaming e clean-checkout regression. Gold protocol existe, mas n=3 e ausência de independent human agreement impedem freeze de thresholds. A próxima qualidade crítica é targeted repair + telemetry e depois calibration/ablation.

## Hard gates

Status: `ACTIVE_REPAIR_TELEMETRY_CALIBRATION`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`: explicit graph/state + SQLite RunStore; 9/9 join, checkpoint/reopen/resume e persistent history demonstrados;
2. cobertura 3 níveis × 3 formatos — `FOUNDATION_PASS`: planner 9 jobs + native schemas passam; provider generation quality ainda não medida;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`: source/factual/policy precedence + claim HybridDecision; semantic sensor secundário;
4. legibilidade PT-BR calibrada — `IMPLEMENTED_DIAGNOSTIC_ONLY`: versão controlada existe; thresholds aguardam gold/agreement;
5. densidade/contextualização de termos financeiros — `IMPLEMENTED_DIAGNOSTIC_ONLY`: ontology + ACV multidimensional + anti-gaming existem;
6. factuality/grounding contra fonte — `CORE_PASS_PARTIAL_SCOPE`: deterministic backbone + claim-level grounding; broader calibrated semantic value ainda pendente;
7. auto-correção com feedback mensurável — `PARTIAL`: branch-local proof existe; T006 fará failure-code-driven repair/re-eval;
8. interface comparativa com métricas/rastreabilidade — `DESIGNED_NOT_BUILT`;
9. testes automatizados/reprodutíveis — `STRONG_PASS_FOUNDATION`: clean-checkout Foundation Regression + System Integrity PASS;
10. matriz de confusão dos níveis — `T008 BLOCKED_ON_T007`;
11. análise custo/latência — `T007 READY`;
12. README/documentação reproduzível — `PENDING`;
13. vídeo real comprovando código/interface — `PENDING`;
14. vídeo <=5:00 — `CONTROLLED_BY_PLAN`.

## New evidence

- gold-v001 protocol/split/rubric/validator com leakage controls; sem threshold freeze;
- grounding focused suite 8/8 PASS e hard-gate non-compensation regression;
- graph/state + RunStore proof: 9/9 outputs, local quality repair, separate transport retry, reopen/resume, 28 history snapshots;
- audience feature harness: 15 focused tests PASS, ACV permanece vetor multidimensional;
- clean-checkout Foundation Regression e System Integrity PASS no GitHub Actions.

## Open quality gaps

1. Targeted repair driven por failure codes + re-evaluation sem regressão factual/policy.
2. Telemetry de run/job/attempt, latência/retries/repairs e custo somente quando observável.
3. Calibration/ablation/confusion matrix sobre development gold, held-out isolado e anti-gaming release gate.
4. Provider/model measured comparison quando houver evidência suficiente.
5. Evidence cockpit, README/report, release/video proof e final reviews.

## Next quality action

Executar W003-T006 e T007 em paralelo; liberar T008 após T007 integrar e manter thresholds/provider/backend unlocked até evidência.
