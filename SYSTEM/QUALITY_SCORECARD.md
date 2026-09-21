# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0018`

`QUALITY_STATUS: PACED_FINAL_DEMO_TASK_SCOPE_PASS_INDEPENDENT_REVIEW_PENDING`

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

T018 directly inspected the original T017 video and found that technical existence/duration were valid but evaluator-facing usability was not. T019 has now implemented that remediation with a real browser recording in GitHub Actions, deliberately paced at `69.12s`, with visible explanatory captions/hold-times. It shows a genuine `SOURCE_READY/PASS` success path first, exact source hash/provenance, 9/9 audience×format mechanics cells, persisted `FAIL→repair→PASS`, explicit non-claim boundaries, then the real BCB PDF as a labelled fail-closed safety negative-control. Nine representative frames decoded from the final MP4 passed post-encode validation. README and submission packet were refreshed. Quality still does not mark the final demo accepted until T020 independently reviews the concrete artifact.

## Hard gates

Status: `ACTIVE_FINAL_BLIND_REVIEW_HUMAN_PROVIDER`

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
12. README/documentação/reporte reproduzível — `CONSOLIDATED_AND_REFRESHED_T019`;
13. vídeo real comprovando código/interface — `T019_REAL_BROWSER_TASK_SCOPE_PASS / INDEPENDENT_REVIEW_T020_PENDING`;
14. vídeo <=5:00 — `ACTUAL_DURATION_PASS_T019_69_12S`.

## T019 evidence

- accepted Actions run `35636285651` on capture commit `ffaa235e31667d1aab9a1f24253e647579e394e1`;
- final H.264 MP4 SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`;
- observed duration `69.12s <= 300s`, 1280×720, 25 fps;
- primary artifact `10656720873`, provenance artifact `10656775849`, both expiring `2026-12-20T18:06:45Z` unless durably copied;
- success text path: `SOURCE_READY/PASS`, exact hash, 9/9 `PLANNED_MECHANICS_ONLY` cells;
- repair evidence and non-claim boundaries visible;
- real BCB PDF remains `SOURCE_BLOCKED/REVIEW_REQUIRED/LOW` with `TABLE_ROLE_AMBIGUITY` and all 9 rows blocked;
- 9/9 representative post-encode frame validations PASS;
- root README and `docs/submission/SUBMISSION_PACKET.md` refreshed.

## Open quality gaps

1. independent blind/adversarial review of T019 concrete final artifact/package (T020);
2. durable submission storage if Actions retention is insufficient;
3. two genuinely independent human annotation streams + agreement/adjudication and confusion matrices;
4. semantic ablation on the same valid human development gold;
5. credentialed comparable provider/model runs;
6. final T008 clean-E2E release proof after external prerequisites.

## Next quality action

Execute T020. Treat T019 as strong task-scope remediation, not self-certified final acceptance. T020 must directly inspect the concrete MP4 and updated package, preserve external human/provider blockers, and separate video/package review from overall release readiness.
