# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0019`

`QUALITY_STATUS: VIDEO_PACKAGE_BLIND_REVIEW_PASS_EXTERNAL_EVIDENCE_PENDING`

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

T019 remediou o gap de comunicação com uma gravação real de browser em GitHub Actions, deliberadamente paced em `69.12s`, com captions/hold-times, success path primeiro, provenance, 9/9 mechanics, `FAIL→repair→PASS`, evidence boundaries e BCB fail-closed negative-control. T020 então baixou e verificou diretamente os artifacts aceitos, revalidou digests/hashes/duração, inspecionou frames do MP4 e aprovou independentemente o escopo `VIDEO_PACKAGE_REVIEW`, sem findings CRITICAL/HIGH novos. Isso fecha F-001/F-002/F-003/F-007/F-008 no escopo de vídeo/pacote; não fecha human calibration, provider evidence ou overall release readiness.

## Hard gates

Status: `ACTIVE_EXTERNAL_HUMAN_PROVIDER_AND_FINAL_FANIN`

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
13. vídeo real comprovando código/interface — `INDEPENDENT_VIDEO_PACKAGE_REVIEW_PASS_T020`;
14. vídeo <=5:00 — `INDEPENDENT_ACTUAL_DURATION_PASS_69_120S`.

## T020 evidence

- primary/provenance ZIP digests independently reverified against GitHub metadata;
- final MP4 SHA-256 independently reverified as `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`;
- ffprobe independently measured `69.120000s <= 300s`, H.264 1280×720/25fps;
- representative frames independently inspected: positive SOURCE_READY/PASS path precedes safety negative-control, repair/evidence boundaries are visible, BCB source trust remains fail-closed;
- `VIDEO_PACKAGE_REVIEW: PASS`; `NEW_CRITICAL_FINDINGS: 0`; `NEW_HIGH_FINDINGS: 0`;
- residual MEDIUM: accepted Actions artifacts expire `2026-12-20T18:06:45Z`; T021 addresses durable byte-identical preservation;
- residual MEDIUM: successful 3×3 table is taller than the viewport, but exact 9/9 is bound by caption/DOM/artifact evidence and is not a hard gate failure.

## Open quality gaps

1. durable preservation of the exact accepted final MP4/package (T021);
2. two genuinely independent human annotation streams + agreement/adjudication and observed confusion matrices;
3. semantic ablation on the same valid human development gold;
4. credentialed comparable provider/model runs;
5. final T008 clean-E2E release proof after external prerequisites;
6. submission logistics/deadline/ownership remain externally unknown.

## Next quality action

Execute T021 without transcoding/regenerating the accepted binary. Then the remaining material gates are human/provider evidence and their dependent T006/T007/T008 fan-ins. Preserve `VIDEO_PACKAGE_REVIEW: PASS` as scope-specific; do not relabel it as overall production/release PASS.
