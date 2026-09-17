# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0011`

`QUALITY_STATUS: W003_E2E_MECHANICS_PROVEN_RELEASE_EVIDENCE_PENDING`

`STOP_CONDITION: FAIL`

## Case Contract status

- Objective: `KNOWN`
- Mandatory deliverables: `6 DELIVERABLES IDENTIFIED`
- Explicit evaluation criteria: `REQUIREMENTS/HARD GATES IDENTIFIED`
- Evaluation weights/scale: `NOT PROVIDED`
- Audience: `3 OUTPUT AUDIENCES KNOWN / FINAL EVALUATOR UNKNOWN`
- Constraints/deadline: `SCOPE + VIDEO HARD GATE KNOWN / DATE UNKNOWN`
- Partner Outcome linkage: `VALUE_HYPOTHESIS_SUPPORTED_EXECUTION_ADVANCED`

## Current evaluation

W003-T009 fechou o proof mechanics end-to-end: exact 3×3, evaluation, one local repair, one independent transport retry, persistent RunStore reopen/resume, hard-gate non-compensation e telemetry lineage. A execução é explicitamente mechanics-only; não prova provider/model quality, calibrated audience thresholds, real cost ou production readiness.

## Hard gates

Status: `ACTIVE_REPRESENTATIVE_EVIDENCE_AND_RELEASE_PROOF`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`;
2. cobertura 3 níveis × 3 formatos — `MECHANICS_PASS / REAL_PROVIDER_QUALITY_PENDING`;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `CORE_PASS_PARTIAL_SCOPE`;
7. auto-correção mensurável — `E2E_CONTROLLED_PROOF_PASS`;
8. interface comparativa com métricas/rastreabilidade — `W004-T001 READY`;
9. testes automatizados/reprodutíveis — `STRONG_PASS_CORE`; task-specific release E2E CI ainda pendente;
10. matriz de confusão dos níveis — `HARNESS_PASS / OBSERVED_MATRIX_NOT_COMPUTABLE_WITH_CURRENT_GOLD`;
11. análise custo/latência — `TELEMETRY_CONTRACT_PASS / REAL_PROVIDER_COST_PENDING`;
12. README/documentação reproduzível — `PENDING_RELEASE_FANIN`;
13. vídeo real comprovando código/interface — `PENDING`;
14. vídeo <=5:00 — `CONTROLLED_BY_PLAN`.

## W003 closure evidence

- source→9 jobs→eval→repair→join/aggregate mechanics PASS;
- one quality repair and one transport retry remain separate;
- RunStore reopen/resume and accepted sibling immutability preserved;
- hard factual fail cannot be masked by clean audience/soft signals;
- usage/cost remain null when unobserved;
- T009 worker head passed System Integrity and Foundation Regression;
- current Foundation workflow still does not explicitly target the new W003 E2E test; W004-T008 must add task-specific clean release CI before any release-readiness claim.

## Open quality gaps

1. evidence cockpit/UI with visible unknown/N/A/failure states;
2. representative independent human annotations/agreement;
3. semantic ablation and provider/model quality-latency-cost comparison on comparable evidence;
4. parser generalization over broader raw/source families;
5. task-specific clean-E2E release proof, README/report, video and final reviews.

## Next quality action

Execute W004-T001..T004 in parallel; release T005..T008 only when their dependencies supply valid evidence.