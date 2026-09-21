# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0014`

`QUALITY_STATUS: CLEAN_RELEASE_CI_PASS_BLIND_REVIEW_NOT_PASS_INTERNAL_ADHERENCE_FIXES_READY`

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

Core mechanics, hard gates, repair, telemetry, cockpit and parser/source-trust behavior now survive an explicit task-specific clean GitHub Actions release smoke. The first blind recipient-facing review nevertheless remains `NOT_PASS`: final video is absent, raw PDF/text ingestion is not shown in the submission-facing flow, the current cockpit is a read-only HTML projection rather than an unmistakably interactive app, and the experimental report is not consolidated. These are internal deliverable/adherence gaps and are being separated from external human/provider evidence blockers.

## Hard gates

Status: `ACTIVE_RECIPIENT_ADHERENCE_HUMAN_PROVIDER_AND_FINAL_VIDEO`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`;
2. cobertura 3 níveis × 3 formatos — `MECHANICS_PASS / REAL_PROVIDER_QUALITY_PENDING`;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `CORE_PASS_PARTIAL_SCOPE`; parser role hard gates strengthened;
7. auto-correção mensurável — `E2E_CONTROLLED_PROOF_PASS`;
8. interface comparativa com métricas/rastreabilidade — `READ_ONLY_COCKPIT_PROVEN / INTERACTIVE_RECIPIENT_APP_PENDING_T014`;
9. testes automatizados/reprodutíveis — `CLEAN_TASK_SPECIFIC_RELEASE_CI_PASS`;
10. matriz de confusão dos níveis — `OPERATOR_READY / OBSERVED_HUMAN_MATRIX_PENDING_T005`;
11. análise custo/latência — `MANUAL_PATH_READY / REAL_PROVIDER_RUN_BLOCKED_EXTERNAL`;
12. README/documentação reproduzível — `IMPLEMENTED / CONSOLIDATED_REPORT_PENDING_T015`;
13. vídeo real comprovando código/interface — `CRITICAL_PENDING_T016`;
14. vídeo <=5:00 — `STORYBOARD_CONTROLLED / ACTUAL_DURATION_UNVERIFIED`.

## W004 release-review evidence

- T012 clean CI run executed the actual release-smoke runner and focused test; exact 9/9 mechanics, persisted FAIL→PASS lineage, fresh hard gates, sibling immutability, cockpit markers and parser gates passed while external unknowns stayed unpromoted;
- T013 blind review returned `NOT_PASS`; F-001 video absent is CRITICAL; F-002 raw ingest, F-003 interactive UI interpretation and F-007 consolidated report are HIGH internal findings; F-005/F-006 remain external human/provider blockers; F-008 actual <=5:00 duration remains unobserved.

## Open quality gaps

1. recipient-facing real PDF/text ingestion + unmistakably interactive local app (T014);
2. consolidated experimental report/submission packet with blocked sections explicit (T015);
3. actual final demo artifact, bound to exact version and measured <=5:00 (T016);
4. two genuinely independent human annotation streams + agreement/adjudication and confusion matrices;
5. semantic-on/off ablation on the same independent development gold;
6. credentialed comparable provider/model runs with observed quality/latency/usage/cost;
7. final T008 clean-E2E release proof and final blind re-review.

## Next quality action

Execute T014/T015 in parallel. After both integrate, release T016 for the actual measured video. Keep T005/T006/T007 external-evidence dependencies unchanged; do not convert clean mechanics or packaging improvements into provider/human calibration claims.
