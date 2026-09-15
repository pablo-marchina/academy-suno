# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0004`

`QUALITY_STATUS: ARCHITECTURE_READY_NO_BASELINE`

`STOP_CONDITION: FAIL`

## Case Contract status

- Objective: `KNOWN`
- Mandatory deliverables: `6 DELIVERABLES IDENTIFIED`
- Explicit evaluation criteria: `REQUIREMENTS/HARD GATES IDENTIFIED`
- Evaluation weights/scale: `NOT PROVIDED`
- Audience: `3 OUTPUT AUDIENCES KNOWN / FINAL EVALUATOR UNKNOWN`
- Constraints/deadline: `SCOPE + VIDEO HARD GATE KNOWN / DATE UNKNOWN`
- Partner Outcome linkage: `VALUE_HYPOTHESIS_SUPPORTED`

## Current evaluation

W001 fechou a arquitetura candidata, Hybrid Evaluator, UX/evidence cockpit, mandatory experiments e kill criteria. Ainda não há baseline executável suficiente para pontuar qualidade ou validar thresholds.

## Hard gates

Status: `ACTIVE`

1. pipeline funcional baseado em estado/grafo;
2. cobertura de 3 níveis × 3 formatos;
3. framework híbrido com componente determinístico;
4. legibilidade PT-BR calibrada;
5. densidade/contextualização de termos financeiros;
6. factuality/grounding contra fonte;
7. auto-correção com feedback mensurável;
8. interface comparativa com métricas e rastreabilidade;
9. testes automatizados/reprodutíveis;
10. matriz de confusão dos níveis;
11. análise custo/latência;
12. README/documentação reproduzível;
13. vídeo real comprovando código e interface;
14. regra operacional de duração <=5:00 devido ao conflito registrado em A-0001.

## Quality architecture now designed

- source trust precede generation;
- factual/policy/material-concept gates are non-compensatory;
- audience complexity is multidimensional and calibratable;
- semantic judge is secondary sensor, not truth source;
- generation target, human gold and evaluator prediction are separated;
- held-out is frozen before final evaluation;
- repair is targeted by failure code/job_id and re-evaluated;
- article/carousel/video have distinct structured contracts;
- evidence cockpit must show source lineage and FAIL→repair→PASS.

## Open quality gaps

1. Implementar versioned domain/provenance contracts e real-source parsing/source trust.
2. Executar factual/policy adversarial hard-gate tests.
3. Implementar 3×3 structured generation and format contracts.
4. Executar EXP-A parser bakeoff e EXP-B LangGraph-vs-plain-async.
5. Construir gold/development benchmark e calibrar audience/evaluator sem held-out leakage.
6. Provar targeted repair sem regressão factual/policy.
7. Construir evidence cockpit e rehearsal <=5:00.
8. Resolver deadline/submission quando informação existir.

## Next quality action

W002 deve priorizar foundation correctness e mandatory experiments antes de soft-metric sophistication ou UI polish.