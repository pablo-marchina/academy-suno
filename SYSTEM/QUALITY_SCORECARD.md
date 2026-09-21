# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0021`

`QUALITY_STATUS: VIDEO_PACKAGE_DURABILITY_AND_PROVIDER_MECHANICS_PASS_HUMAN_EVIDENCE_PENDING`

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

T019 remediou o gap de comunicação com uma gravação real de browser em GitHub Actions, deliberadamente paced em `69.12s`, com captions/hold-times, success path primeiro, provenance, 9/9 mechanics, `FAIL→repair→PASS`, evidence boundaries e BCB fail-closed negative-control. T020 baixou e verificou diretamente os artifacts aceitos, revalidou digests/hashes/duração, inspecionou frames do MP4 e aprovou independentemente o escopo `VIDEO_PACKAGE_REVIEW`, sem findings CRITICAL/HIGH novos. T021 A02 eliminou o residual de retenção ao persistir o mesmo MP4 em storage controlado pelo repositório e confirmar a cópia por fresh-clone, SHA-256, size e `cmp` byte-a-byte.

T004 A08 fechou o provider-mechanics gate com uma execução real Groq: cliente OpenAI Python `2.11.0` em configuração compatível documentada, Models preflight HTTP `200`, `13` modelos ativos, `openai/gpt-oss-120b` selecionado, Responses HTTP `200`, `349.694 ms`, `84/61/145` tokens e custo derivado `4.92e-05 USD` de pricing oficial versionado. O artifact sanitizado passou strict T007 import e fresh-clone verification. Isso comprova auth/runtime/latency/usage/cost, mas não substitui human quality evidence nem autoriza provider preference.

## Hard gates

Status: `ACTIVE_EXTERNAL_HUMAN_AND_FINAL_FANIN`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`;
2. cobertura 3 níveis × 3 formatos — `MECHANICS_PASS / HUMAN-CALIBRATED QUALITY PENDING`;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `CORE_PASS_PARTIAL_SCOPE`;
7. auto-correção mensurável — `E2E_CONTROLLED_PROOF_PASS`;
8. interface comparativa com métricas/rastreabilidade — `RECIPIENT_INTERACTIVE_APP_PASS`;
9. testes automatizados/reprodutíveis — `CLEAN_TASK_SPECIFIC_RELEASE_CI_PASS`;
10. matriz de confusão dos níveis — `OPERATOR_READY / OBSERVED_HUMAN_MATRIX_PENDING_T005`;
11. análise custo/latência — `OBSERVED_GROQ_A08_PASS / COMPARATIVE_QUALITY_PENDING_T005_T007`;
12. README/documentação/reporte reproduzível — `CONSOLIDATED_REFRESHED_AND_DURABLE_ARTIFACT_LINKED`;
13. vídeo real comprovando código/interface — `INDEPENDENT_VIDEO_PACKAGE_REVIEW_PASS_T020`;
14. vídeo <=5:00 — `INDEPENDENT_ACTUAL_DURATION_PASS_69_120S`;
15. disponibilidade durável do vídeo aceito — `BYTE_IDENTICAL_REPOSITORY_COPY_PASS_T021`.

## T004 A08 evidence

- accepted attempt: `W004-T004-A08`; Actions run `35664987180`; artifact `10668547182`;
- transport: `openai-python 2.11.0` with Groq-compatible base URL;
- Models preflight HTTP `200`, `13` active models, selected `openai/gpt-oss-120b`;
- Responses HTTP `200`; observed latency `349.694 ms`;
- observed usage: input `84`, output `61`, total `145` tokens;
- official-pricing-derived cost: `4.92e-05 USD`;
- provider-returned model: `openai/gpt-oss-120b`;
- response SHA-256: `5a3466faf9d179f5da92cde5ad5de9e2227e9821c7260976040db466e7b8d3fc`;
- strict T007 mechanics importer exit `0`; fresh remote clone/read-back verification PASS;
- secret material and raw generated output text were not persisted.

## T021 evidence

- accepted attempt: `W004-T021-A02`; Actions run `35651949452`;
- source artifact `10656720873` re-downloaded and checked before persistence;
- source and durable copy SHA-256: `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`;
- exact size: `1388430` bytes;
- durable path: `artifacts/submission/final-demo.mp4`;
- fresh remote clone/read-back verified SHA/size and `cmp` equality against the freshly downloaded accepted source;
- persistence commit: `8216b56edef7a666e08aab7c6dc37ea1a6ec3781`;
- no transcode, regeneration, remux or content modification occurred.

## Open quality gaps

1. two genuinely independent human annotation streams + agreement/adjudication and observed confusion matrices;
2. semantic ablation on the same valid human development gold (`T006`);
3. provider/model **quality comparison** on valid human gold using observed provider mechanics (`T007`); T004 runtime/mechanics prerequisite is now satisfied;
4. final T008 clean-E2E release proof after T005/T006/T007;
5. submission logistics/deadline/ownership remain externally unknown.

## Next quality action

Obtain the independent human labels and execute a fresh T005 attempt. Then run T006/T007 and T008 in dependency order, followed by remaining global QA. Preserve provider mechanics and video/package PASS as scope-specific evidence; do not relabel either as overall production/release PASS.
