# SUCCESS SCORECARD

`SUCCESS_MODEL_VERSION: 1.0`

`SUCCESS_SCORECARD_VERSION: 0015`

`SUCCESS_STATUS: W004_REAL_CI_VIDEO_TECHNICAL_GATE_PROVEN_BLIND_USABILITY_REVIEW_PENDING`

`SUCCESS_STOP_CONDITION: FAIL`

`TRACEABILITY_STATUS: PARTIAL_EXECUTABLE`

`CRITICAL_ASSUMPTIONS_STATUS: OPEN`

`BLIND_REVIEW: NOT_PASS`

## Current success model

W003 mechanics e W004 trust/evidence controls permanecem fortes. T012 provou release-smoke em clean CI; T014/T015 fecharam app recipient-facing e relatório consolidado. T017 agora adiciona evidência concreta de gravação real: GitHub Actions executou app real + PDF público BCB + browser Playwright, visitou via DOM assertions a ingestão texto/PDF, 3×3, repair lineage e evidence labels, gravou MP4 real e mediu `7.200s <= 300s` com hashes/provenance. Isso resolve a incerteza técnica de “existe gravação real sob o teto?”, mas não autoriza concluir que 7,2s sejam suficientes como demo final inteligível/convincente. T018 fará essa revisão cega. Human gold independente e provider run observado continuam blockers externos.

## Dimensions

| Dimension | Status | Score | Confidence | Main gap |
|---|---|---:|---|---|
| Partner Outcome | VALUE_HYPOTHESIS_SUPPORTED | — | MEDIUM | ROI/workflow/owner internos e incrementality real ainda não medidos |
| Brief / Evaluation Fit | TECHNICAL_VIDEO_AND_RECIPIENT_FLOW_EVIDENCE_AVAILABLE | — | HIGH | human-calibrated confusion matrix, provider evidence e evaluator-facing video adequacy |
| Evidence & Analytical Rigor | CLEAN_RELEASE_REAL_BROWSER_PROVEN_EXTERNAL_VALIDITY_OPEN | — | HIGH | independent human labels/agreement e real provider comparison ausentes |
| Solution Strength & Differentiation | TRUST_REPAIR_AUDIT_INTERACTIVE_PATH_PROVEN | — | HIGH | audience separation/model quality ainda sem independent ground truth |
| Feasibility & Adoption | RECIPIENT_APP_RUNNABLE_PROVIDER_RUNTIME_OPEN | — | HIGH | provider execution real, OCR/parser winner e workflow interno |
| Deliverable & Artifact Excellence | REPORT_PLUS_REAL_VIDEO_ARTIFACT_AVAILABLE | — | HIGH | video usability/blind acceptance + durable retention + external evidence |
| Communication & Defense | REAL_7_2S_CAPTURE_EXISTS_BLIND_USABILITY_PENDING | — | HIGH | T018 must judge whether the concrete recording communicates enough |
| Execution Robustness | CLEAN_CI_REAL_BROWSER_ARTIFACT_PROVEN | — | HIGH | external T005/T004 evidence + final downstream T008 |

## Global hard gates

- 3 níveis × 3 formatos funcionais;
- factuality/grounding sem falha crítica;
- sofisticação mensurável sem trivialização;
- evals determinísticos reproduzíveis;
- refinement loop com FAIL→feedback→repair;
- interface comparativa + source traceability;
- testes automatizados;
- matriz de confusão de níveis quando human gold válido existir;
- custo/latência documentados sem custo inventado;
- README/reprodutibilidade;
- vídeo real demonstrando código/UI, operacionalmente <=5 min e evaluator-usable;
- traceability completa e assumptions críticas controladas antes do final.

## Evidence gained through W004 video remediation

- T016: blocked truthfully, producing deterministic exact-SHA/public-PDF/hash/duration capture tooling instead of a fake video;
- T017: Actions run `35625349017` success on task SHA `f95bd26f178b21314aa5d4b3eb8b086643490aee`; real BCB PDF SHA `4ac6a958cbff7571aad3f0125042f4b71890a70ec36e9ad9009b537e6458ce68`; real MP4 SHA `f04852fb11183e4e6bc8690d80c5ef26d6993edc6aa7ec71660b9e3b670c3bc4`; duration `7.200s`; DOM/content assertions for required flow; primary artifact `10652146281` + provenance artifact `10652031268`; evidence boundaries remain MECHANICS_ONLY / DIAGNOSTIC_ONLY / PRODUCTION_UNKNOWN/BLOCKED.

## Critical bottleneck

`BLIND_VIDEO_USABILITY_REVIEW_PLUS_EXTERNAL_HUMAN_PROVIDER_EVIDENCE`

## Next success action

Execute W004-T018 against the concrete package + T017 artifact. Do not promote `BLIND_REVIEW` from `NOT_PASS` merely because the technical capture exists. If T018 accepts F-001/F-008, preserve/copy the accepted artifact before its current Actions expiry (`2026-12-20T16:24:02Z`) if needed for submission. Human/provider gates remain independent and cannot be substituted by the video.
