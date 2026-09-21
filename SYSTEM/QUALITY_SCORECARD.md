# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0015`

`QUALITY_STATUS: RECIPIENT_APP_AND_REPORT_IMPLEMENTED_FINAL_VIDEO_EXTERNAL_EVIDENCE_PENDING`

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

Core mechanics, hard gates, repair, telemetry, cockpit and parser/source-trust behavior survive clean CI. T014 closes the recipient-facing code/interface gap with a real local HTTP application accepting text/PDF input and fail-closing ambiguous extraction. T015 closes the fragmented-report gap with a consolidated experimental report and submission packet. `BLIND_REVIEW` remains `NOT_PASS` until an actual video artifact is produced/measured and the external human/provider evidence gates are resolved or explicitly accepted as remaining limitations.

## Hard gates

Status: `ACTIVE_FINAL_VIDEO_HUMAN_PROVIDER`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`;
2. cobertura 3 níveis × 3 formatos — `MECHANICS_PASS / REAL_PROVIDER_QUALITY_PENDING`;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `CORE_PASS_PARTIAL_SCOPE`; parser role hard gates strengthened;
7. auto-correção mensurável — `E2E_CONTROLLED_PROOF_PASS`;
8. interface comparativa com métricas/rastreabilidade — `RECIPIENT_INTERACTIVE_APP_IMPLEMENTED_T014`;
9. testes automatizados/reprodutíveis — `CLEAN_TASK_SPECIFIC_RELEASE_CI_PASS`;
10. matriz de confusão dos níveis — `OPERATOR_READY / OBSERVED_HUMAN_MATRIX_PENDING_T005`;
11. análise custo/latência — `MANUAL_PATH_READY / REAL_PROVIDER_RUN_BLOCKED_EXTERNAL`;
12. README/documentação/reporte reproduzível — `CONSOLIDATED_T015`;
13. vídeo real comprovando código/interface — `CRITICAL_PENDING_T016`;
14. vídeo <=5:00 — `STORYBOARD_CONTROLLED / ACTUAL_DURATION_UNVERIFIED`.

## W004 recipient/report evidence

- T014: local interactive HTTP app accepts text, PDF path and PDF upload; exposes raw SHA-256/provenance/parser/confidence/source-trust; low confidence/table-role ambiguity cannot become SOURCE_READY/PASS; canonical 3×3 planning is reused; 7 focused tests + System Integrity + Foundation Regression PASS on worker head;
- T015: consolidated experimental report and submission packet cover architecture, source trust, factual/grounding, audience/anti-gaming, repair, telemetry, parser evidence, clean smoke, trade-offs, traceability and reproducibility; human matrices remain `BLOCKED/PENDING`, provider metrics `PRODUCTION_UNKNOWN/BLOCKED`.

## Open quality gaps

1. actual final demo artifact, bound to exact integrated version and measured <=5:00 (T016);
2. two genuinely independent human annotation streams + agreement/adjudication and confusion matrices;
3. semantic-on/off ablation on the same independent development gold;
4. credentialed comparable provider/model runs with observed quality/latency/usage/cost;
5. final T008 clean-E2E release proof and final blind re-review;
6. OCR/same-raw-byte parser comparison only if a parser implementation winner is needed.

## Next quality action

Execute T016 on the integrated T014/T015 commit. The recording must exercise the real recipient app and a public PDF/text path, show evidence states/repair lineage, and be measured <=5:00. If capture is impossible in the worker environment, return an explicit manual-capture blocker package rather than false completion.
