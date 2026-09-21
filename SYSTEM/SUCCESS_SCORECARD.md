# SUCCESS SCORECARD

`SUCCESS_MODEL_VERSION: 1.0`

`SUCCESS_SCORECARD_VERSION: 0020`

`SUCCESS_STATUS: W004_VIDEO_PACKAGE_DURABILITY_PASS_GROQ_PERMISSION_AND_HUMAN_GATES_OPEN`

`SUCCESS_STOP_CONDITION: FAIL`

`TRACEABILITY_STATUS: PARTIAL_EXECUTABLE`

`CRITICAL_ASSUMPTIONS_STATUS: OPEN`

`BLIND_REVIEW: PASS_VIDEO_PACKAGE_SCOPE`

## Current success model

W003 mechanics and W004 trust/evidence controls remain strong. T019 produced the accepted real-browser final demo at `69.12s <= 300s`; T020 independently downloaded the exact artifacts, reverified ZIP/MP4/source hashes, remeasured duration, inspected representative frames, and concluded `VIDEO_PACKAGE_REVIEW: PASS` with zero new CRITICAL/HIGH internal findings. T021 then preserved the exact accepted MP4 in repository-controlled storage and verified the persisted copy through a fresh remote clone with matching SHA-256, size and byte-for-byte `cmp`. F-001/F-002/F-003/F-007/F-008 therefore pass in the video/package review scope with the retention dependency removed.

The provider blocker is now materially better characterized but not satisfied: A04 defensibly identified the supplied credential as Groq and reached the official Responses endpoint, which returned HTTP 403; A05 then performed a read-only `GET /openai/v1/models` preflight and also received HTTP 403 before any generation. This proves the remaining provider blocker is external access/permission at or before the Groq project/organization API boundary, not merely absence of a credential. No usage/cost/model response was observed, so F-006 remains blocked and no provider preference is authorized.

## Dimensions

| Dimension | Status | Score | Confidence | Main gap |
|---|---|---:|---|---|
| Partner Outcome | VALUE_HYPOTHESIS_SUPPORTED | — | MEDIUM | ROI/workflow/owner internos e incrementality real ainda não medidos |
| Brief / Evaluation Fit | VIDEO_PACKAGE_SCOPE_PASS | — | HIGH | human evidence + Groq permission correction + final dependent fan-in |
| Evidence & Analytical Rigor | FAIL_CLOSED_EVIDENCE_STRONG | — | HIGH | independent human labels/agreement and accepted real provider mechanics absent |
| Solution Strength & Differentiation | TRUST_REPAIR_AUDIT_INTERACTIVE_PATH_PROVEN | — | HIGH | audience separation/model quality still lack independent ground truth |
| Feasibility & Adoption | RECIPIENT_APP_RUNNABLE_GROQ_ACCESS_BLOCKED | — | HIGH | Groq API permission/access, internal workflow unknown |
| Deliverable & Artifact Excellence | VIDEO_PACKAGE_DURABLE_REPOSITORY_COPY_PASS | — | HIGH | external evidence-dependent final QA remains |
| Communication & Defense | INDEPENDENT_VIDEO_PACKAGE_PASS | — | HIGH | defense/submission logistics and external evidence remain |
| Execution Robustness | CLEAN_CI_REAL_BROWSER_DURABLE_ARTIFACT_PROVEN | — | HIGH | external T005 + Groq T004 evidence + downstream T008 |

## Global hard gates

- 3 níveis × 3 formatos funcionais;
- factuality/grounding sem falha crítica;
- sofisticação mensurável sem trivialização;
- evals determinísticos reproduzíveis;
- refinement loop com FAIL→feedback→repair;
- interface comparativa + source traceability;
- testes automatizados;
- matriz de confusão somente quando human gold válido existir;
- custo/latência sem custo inventado;
- README/reprodutibilidade;
- vídeo real demonstrando código/UI, <=5 min e evaluator-usable;
- traceability completa e assumptions críticas controladas antes do final.

## Evidence through STATE 0032

- T019 accepted run `35636285651`; final MP4 SHA `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`; duration `69.12s`; primary artifact `10656720873`; provenance artifact `10656775849`; success-first 9/9 + repair lineage + BCB fail-closed negative-control.
- T020 independently verified artifact ZIP digests, MP4 hash/duration, BCB source hash and representative frames, and returned `VIDEO_PACKAGE_REVIEW: PASS`, `NEW_CRITICAL_FINDINGS: 0`, `NEW_HIGH_FINDINGS: 0`.
- T021 accepted attempt A02 / Actions run `35651949452` re-downloaded artifact `10656720873`, verified source SHA `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5` and `1388430` bytes, persisted `artifacts/submission/final-demo.mp4`, then fresh-cloned the worker branch and verified the same SHA/size plus byte-identical `cmp` PASS. Persistence commit: `8216b56edef7a666e08aab7c6dc37ea1a6ec3781`.
- The original Actions artifacts expire `2026-12-20T18:06:45Z`, but their expiry is no longer an availability dependency for the accepted MP4.
- T004 A04 / Actions run `35661547702`: credential classified as Groq (`gsk_`), official `openai/gpt-oss-20b` Responses request returned HTTP 403 after `74.928 ms`; no usage/cost/model response.
- T004 A05 / Actions run `35661903374`: read-only Groq Models API preflight returned HTTP 403 after `83.516 ms`; generation was not attempted; artifact `10666594714`, persistence commit `e439bd4263b4b3d678f63975702185a793513c37`.
- F-005 independent human calibration remains `BLOCKED/PENDING`; F-006 provider evidence remains `BLOCKED/GROQ_PERMISSION_EXTERNAL`.

## Critical bottleneck

`EXTERNAL_HUMAN_GROQ_PERMISSION_EVIDENCE`

## Next success action

Correct/confirm Groq organization/project/key API permissions, then execute T004 with a fresh attempt ID. In parallel, obtain two genuinely independent human annotation streams and advance T005. Only after accepted provider mechanics + valid human evidence should T006/T007/T008 and the remaining final reviews proceed. Do not convert `PASS_VIDEO_PACKAGE_SCOPE`, durable artifact preservation, or a 403-reaching provider request into overall release/production PASS.
