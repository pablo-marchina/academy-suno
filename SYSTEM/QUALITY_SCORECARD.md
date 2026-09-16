# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0010`

`QUALITY_STATUS: CALIBRATION_GATE_EXECUTABLE_DIAGNOSTIC_ONLY`

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

W003-T008 implementou o release gate de calibration/ablation com anti-circularity e anti-gaming. A qualidade do mecanismo é comprovada por 8/8 focused tests e CI do worker, mas a qualidade calibrada por audiência ainda não pode receber thresholds finais: gold-v001 não possui human gold labels/agreement independentes suficientes. `DIAGNOSTIC_ONLY` é a conclusão correta, não uma lacuna escondida.

## Hard gates

Status: `ACTIVE_END_TO_END_PROOF`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`;
2. cobertura 3 níveis × 3 formatos — `FOUNDATION_PASS / REAL_PROVIDER_QUALITY_PENDING`;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `CORE_PASS_PARTIAL_SCOPE`;
7. auto-correção mensurável — `CONTROLLED_PROOF_PASS`;
8. interface comparativa com métricas/rastreabilidade — `DESIGNED_NOT_BUILT`;
9. testes automatizados/reprodutíveis — `STRONG_PASS_CORE`;
10. matriz de confusão dos níveis — `HARNESS_PASS / OBSERVED_MATRIX_NOT_COMPUTABLE_WITH_CURRENT_GOLD`;
11. análise custo/latência — `TELEMETRY_CONTRACT_PASS / REAL_PROVIDER_COST_PENDING`;
12. README/documentação reproduzível — `PENDING`;
13. vídeo real comprovando código/interface — `PENDING`;
14. vídeo <=5:00 — `CONTROLLED_BY_PLAN`.

## New evidence

- T008 focused suite 8/8 PASS;
- held-out rows are structurally rejected from tuning/calibration;
- generation target→human and human→evaluator are separate metric surfaces;
- mandatory anti-gaming cases PASS;
- semantic signal cannot compensate source/factual/policy hard failures;
- synthetic pricing is excluded from provider-cost evidence;
- current audience confusion metrics are NOT_COMPUTABLE because valid independent human labels are absent;
- threshold freeze remains false; semantic/provider/backend decisions remain neutral.

## Open quality gaps

1. W003-T009 end-to-end mechanics proof and synthesis.
2. Independent blinded human annotations/agreement before any threshold freeze or observed audience confusion-matrix claim.
3. Measured semantic-off/on ablation and real provider/model quality-latency-cost comparison when evidence exists.
4. Expanded parser bakeoff over raw bytes/structural provenance.
5. Evidence cockpit, README/report, release/video proof and final reviews.

## Next quality action

Executar W003-T009 e usar sua síntese para fechar W003 e gerar W004 sem transformar `NOT_COMPUTABLE/NOT_RUN` em escolhas arbitrárias.
