# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0016`

`QUALITY_STATUS: REAL_BROWSER_VIDEO_TECHNICAL_EVIDENCE_PASS_BLIND_USABILITY_AND_EXTERNAL_EVIDENCE_PENDING`

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

Core mechanics, hard gates, repair, telemetry, cockpit, parser/source-trust and recipient-facing ingest survive clean CI. T017 additionally produced a real browser recording in GitHub Actions against the integrated app and real BCB PDF, with exact task-SHA checkout, DOM/content assertions, source/video hashes, immutable artifact provenance and measured `7.200s` duration. This is strong technical evidence for real-code/UI capture and the <=5:00 ceiling. Quality does not yet mark the evaluator-facing video as finally accepted because 7.2 seconds may be too compressed to communicate the required demonstration; T018 must judge the concrete recording rather than infer from metadata. Human calibration/provider evidence remain absent.

## Hard gates

Status: `ACTIVE_VIDEO_BLIND_REVIEW_HUMAN_PROVIDER`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`;
2. cobertura 3 níveis × 3 formatos — `MECHANICS_PASS / REAL_PROVIDER_QUALITY_PENDING`;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `CORE_PASS_PARTIAL_SCOPE`;
7. auto-correção mensurável — `E2E_CONTROLLED_PROOF_PASS`;
8. interface comparativa com métricas/rastreabilidade — `RECIPIENT_INTERACTIVE_APP_IMPLEMENTED_AND_VISITED_T017`;
9. testes automatizados/reprodutíveis — `CLEAN_TASK_SPECIFIC_RELEASE_CI_PASS`;
10. matriz de confusão dos níveis — `OPERATOR_READY / OBSERVED_HUMAN_MATRIX_PENDING_T005`;
11. análise custo/latência — `MANUAL_PATH_READY / REAL_PROVIDER_RUN_BLOCKED_EXTERNAL`;
12. README/documentação/reporte reproduzível — `CONSOLIDATED_T015`;
13. vídeo real comprovando código/interface — `TECHNICAL_EVIDENCE_PASS_T017 / EVALUATOR_USABILITY_PENDING_T018`;
14. vídeo <=5:00 — `ACTUAL_DURATION_PASS_T017_7_200S / FINAL_DEMO_USABILITY_PENDING_T018`.

## W004 video evidence

- T017 Actions run `35625349017` concluded success;
- exact task SHA `f95bd26f178b21314aa5d4b3eb8b086643490aee` checked out and asserted;
- real public BCB PDF, magic validation and raw-byte SHA-256 passed with no synthetic fallback;
- Playwright/Chromium drove text ingestion, PDF upload, 3×3/evidence and persisted FAIL→repair→PASS path while recording;
- MP4 SHA-256 `f04852fb11183e4e6bc8690d80c5ef26d6993edc6aa7ec71660b9e3b670c3bc4`, ffprobe duration `7.200s`;
- primary artifact `10652146281`, provenance artifact `10652031268`; both currently expire `2026-12-20T16:24:02Z`;
- evidence boundaries explicitly retained human/provider/production unknowns.

## Open quality gaps

1. blind/adversarial evaluator review of the concrete T017 video and current package (T018);
2. durable submission storage for the accepted video if Actions retention is insufficient;
3. two genuinely independent human annotation streams + agreement/adjudication and confusion matrices;
4. semantic-on/off ablation on the same independent development gold;
5. credentialed comparable provider/model runs with observed quality/latency/usage/cost;
6. final T008 clean-E2E release proof and final review;
7. OCR/same-raw-byte parser comparison only if a parser implementation winner is needed.

## Next quality action

Execute T018. Treat T017 as concrete technical evidence, not as automatic proof of communication quality. If T018 cannot inspect playback/frames directly, it must state that limitation rather than infer visual sufficiency from DOM assertions and duration alone.
