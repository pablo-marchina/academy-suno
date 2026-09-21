# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0020`

`QUALITY_STATUS: VIDEO_PACKAGE_AND_DURABILITY_PASS_EXTERNAL_EVIDENCE_PENDING`

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

T019 remediou o gap de comunicação com uma gravação real de browser em GitHub Actions, deliberadamente paced em `69.12s`, com captions/hold-times, success path primeiro, provenance, 9/9 mechanics, `FAIL→repair→PASS`, evidence boundaries e BCB fail-closed negative-control. T020 baixou e verificou diretamente os artifacts aceitos, revalidou digests/hashes/duração, inspecionou frames do MP4 e aprovou independentemente o escopo `VIDEO_PACKAGE_REVIEW`, sem findings CRITICAL/HIGH novos. T021 A02 eliminou o residual de retenção ao persistir o mesmo MP4 em storage controlado pelo repositório e confirmar a cópia por fresh-clone, SHA-256, size e `cmp` byte-a-byte. Isso fecha F-001/F-002/F-003/F-007/F-008 e o residual de durabilidade no escopo de vídeo/pacote; não fecha human calibration, provider evidence ou overall release readiness.

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
12. README/documentação/reporte reproduzível — `CONSOLIDATED_REFRESHED_AND_DURABLE_ARTIFACT_LINKED`;
13. vídeo real comprovando código/interface — `INDEPENDENT_VIDEO_PACKAGE_REVIEW_PASS_T020`;
14. vídeo <=5:00 — `INDEPENDENT_ACTUAL_DURATION_PASS_69_120S`;
15. disponibilidade durável do vídeo aceito — `BYTE_IDENTICAL_REPOSITORY_COPY_PASS_T021`.

## T021 evidence

- accepted attempt: `W004-T021-A02`; Actions run `35651949452`;
- source artifact `10656720873` re-downloaded and checked before persistence;
- source and durable copy SHA-256: `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`;
- exact size: `1388430` bytes;
- durable path: `artifacts/submission/final-demo.mp4`;
- fresh remote clone/read-back verified SHA/size and `cmp` equality against the freshly downloaded accepted source;
- persistence commit: `8216b56edef7a666e08aab7c6dc37ea1a6ec3781`;
- no transcode, regeneration, remux or content modification occurred;
- original Actions artifact expiry is no longer a binary-availability dependency.

## Open quality gaps

1. two genuinely independent human annotation streams + agreement/adjudication and observed confusion matrices;
2. semantic ablation on the same valid human development gold;
3. credentialed comparable provider/model runs;
4. final T008 clean-E2E release proof after external prerequisites;
5. submission logistics/deadline/ownership remain externally unknown.

## Next quality action

Obtain the independent human labels and authorized provider run, then execute the dependent T005/T006/T007/T008 chain and remaining global QA. Preserve `VIDEO_PACKAGE_REVIEW: PASS` and T021 durability as scope-specific evidence; do not relabel either as overall production/release PASS.
