# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0017`

`QUALITY_STATUS: REAL_VIDEO_TECHNICAL_PASS_FINAL_DEMO_USABILITY_NOT_PASS`

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

T018 directly inspected the T017 artifact, not just CI metadata. The technical recording is valid and the measured duration `7.200s` satisfies the <=5:00 cap, but the clip is silent/too compressed to serve as a cold-evaluator walkthrough. The visible BCB PDF path is correctly `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` because cell-role provenance is unavailable; this is a quality/safety success, not a defect to bypass. A final demo must make the success path legible first and then explicitly frame the BCB path as a negative-control.

## Hard gates

Status: `ACTIVE_FINAL_DEMO_HUMAN_PROVIDER`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`;
2. cobertura 3 níveis × 3 formatos — `MECHANICS_PASS / REAL_PROVIDER_QUALITY_PENDING`;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `CORE_PASS_PARTIAL_SCOPE`;
7. auto-correção mensurável — `E2E_CONTROLLED_PROOF_PASS`;
8. interface comparativa com métricas/rastreabilidade — `RECIPIENT_INTERACTIVE_APP_PASS`;
9. testes automatizados/reprodutíveis — `CLEAN_TASK_SPECIFIC_RELEASE_CI_PASS`;
10. matriz de confusão dos níveis — `OPERATOR_READY / OBSERVED_HUMAN_MATRIX_PENDING_T005`;
11. análise custo/latência — `MANUAL_PATH_READY / REAL_PROVIDER_RUN_BLOCKED_EXTERNAL`;
12. README/documentação/reporte reproduzível — `CONSOLIDATED_T015 / CURRENT_EVALUATOR_NARRATIVE_REFRESH_REQUIRED_T019`;
13. vídeo real comprovando código/interface — `TECHNICAL_EVIDENCE_PASS_T017 / EVALUATOR_USABILITY_NOT_PASS_T018`;
14. vídeo <=5:00 — `ACTUAL_DURATION_PASS_T017_7_200S`.

## T018 review findings

- F-001: `PARTIAL` — real recording exists, final-demo quality/discoverability not pass.
- F-002: `IMPLEMENTATION PASS / FINAL-DEMO-PACKET UPDATE REQUIRED`.
- F-003: `TECHNICAL PASS / PACKAGING UPDATE REQUIRED`.
- F-007: `PASS AS ARTIFACT / REFRESH REQUIRED`.
- F-008: `PASS` for concrete T017 MP4 duration.
- F-005/F-006: unchanged external human/provider blockers.

## Open quality gaps

1. evaluator-usable final demo with deliberate pacing/captions and a genuine successful path before the fail-closed BCB negative-control (T019);
2. root README/submission packet refreshed and bound to the exact final artifact (T019);
3. independent blind review of T019 concrete output (T020);
4. durable submission storage if Actions retention is insufficient;
5. two genuinely independent human annotation streams + agreement/adjudication and confusion matrices;
6. semantic ablation on the same valid human development gold;
7. credentialed comparable provider/model runs;
8. final T008 clean-E2E release proof after external prerequisites.

## Next quality action

Execute T019. Do not bypass `TABLE_ROLE_AMBIGUITY`; instead make fail-closed behavior explicit as a safety feature. T020 must independently inspect the concrete final artifact before any video/package review can pass.
