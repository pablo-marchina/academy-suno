# W006-T014-A01 — Final evidence manifest

`TASK_ID: W006-T014`  
`ATTEMPT_ID: A01`  
`EVIDENCE_SCOPE: ACCEPTED_REAL_REFERENCE_PRODUCT_PATH_NON_PRODUCTION`  
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`  
`STATIC_W004_FALLBACK_USED: 0`  
`HARD_GATE_COMPENSATION: 0`

## Binding clean-checkout execution

- Worker implementation head: `65500b40708992825ff19be3f88d7634bf14dcdb`
- PR: `#234`
- PR merge ref executed by Actions: `d7be2f16ff1dce2198d9abf68d2bba6e2b114934`
- Workflow: `W006 T014 Final Evidence`
- Workflow run: `36033260520`
- Job: `107746992691` (`audit-capture-video-verify`)
- Job conclusion: `success`
- Same-head `System Integrity`: run `36033260599`, `success`
- Same-head `Foundation Regression`: run `36033260503`, `success`
- Actions artifact id: `10823827694`
- Artifact name: `w006-t014-a01-final-evidence-d7be2f16ff1dce2198d9abf68d2bba6e2b114934`
- Artifact digest: `sha256:90ad3bc0eb304e5132be1766f725f4e07c41ed8f6ca4ed26c6e331bc00c8a2f4`
- Artifact expiry recorded by GitHub: `2026-12-23T17:17:26Z`

The bundle contains the executed SQLite reference run state/event stores, backup and restored copies, raw capture JSON, capture summary, slide text, rendered segments, exact duration verification, SHA-256 manifest and the final MP4.

## Final technical video

- File: `w006-t014-a01-final-technical-demo.mp4`
- Duration: `180.0 s` (`03:00`)
- Required maximum: `300 s` (`05:00`)
- Duration gate: `PASS`
- Video SHA-256: `3403a37b279cf145cd4ff439032a54a56e629340393c8d77e9a6c26058f21666`
- `video-verification.json` SHA-256: `41155c559df5ee2e434d5ed34c505f6b50985aa49af684460e9111cc6e12fec2`
- `demo-capture.json` SHA-256: `c8ea3533923d46e46f82b0788d83885d9d50344d4b794a71c4da68d21f33ce2b`
- `capture-summary.txt` SHA-256: `213e7e31265f567b699a5027c2b870c7bcf811ae5c50bcbff09edf43f74ed4b7`

The video is generated only after executing the accepted `ReferenceVerticalSlice` in the same workflow. The slide material is generated from that run's observed identities plus the explicit audit boundary. It does not use the static W004 cockpit as live truth and does not claim a deployed production system.

## Source identity

- Run id: `run-w006-t014-a01-final-demo`
- Source id: `source-026273fcf1b04d5f`
- Source group id: `sg-bad1f0c16b84da8f`
- Source SHA-256: `026273fcf1b04d5f1110ef8db3cc85b41979a39ecec56a00e1b67f2abf12754f`
- Provenance ref: `sha256:026273fcf1b04d5f1110ef8db3cc85b41979a39ecec56a00e1b67f2abf12754f`
- Artifact label: `copom-277-reconstruction.pdf`
- Parser: `locked-fixture-pdf-adapter` / `reference-test-v1`
- Parser evidence class: `NONE_REFERENCE_CONTRACT_ONLY`

The parser adapter exists only to exercise the accepted parser/trust contract inside the frozen dependency graph. It is not source-original parser-quality evidence and does not select a production parser.

## Run / aggregate / live identity

- Phase: `complete`
- Accepted branches: `9/9`
- Branch loss: `0`
- Branch duplication: `0`
- Aggregate digest: `536c01f6eec35e53e3e3441e08462a95ed4d9307b5b9c562b3ce2aa3e10893b5`
- Authoritative event count: `11`
- Authoritative event revision: `1..11`
- Event republication duplication: `0`
- Live projection phase: `complete`
- Live projection cells: `9`
- All captured cells state: `PROVEN`
- Backup/restore: `PASS_REFERENCE_SCOPE`
- Restored events/cells/revision: `11 / 9 / 11`
- Production qualification fail-closed: `PASS`

## Job / attempt identity

| Audience | Format | Job id | Attempt id |
|---|---|---|---|
| ADVANCED | ARTICLE | `job-advanced-article-d4209ee1a13a72e6e9e6` | `job-advanced-article-d4209ee1a13a72e6e9e6:attempt:1` |
| ADVANCED | CAROUSEL | `job-advanced-carousel-a3f51ce099a8ec6c51fa` | `job-advanced-carousel-a3f51ce099a8ec6c51fa:attempt:1` |
| ADVANCED | SHORT_VIDEO | `job-advanced-short-video-152ec5870c2c3e69d32c` | `job-advanced-short-video-152ec5870c2c3e69d32c:attempt:1` |
| BEGINNER | ARTICLE | `job-beginner-article-189371ab3d3c7ad3f594` | `job-beginner-article-189371ab3d3c7ad3f594:attempt:1` |
| BEGINNER | CAROUSEL | `job-beginner-carousel-7d7c505e07935a7ce518` | `job-beginner-carousel-7d7c505e07935a7ce518:attempt:1` |
| BEGINNER | SHORT_VIDEO | `job-beginner-short-video-df579760dafca537c298` | `job-beginner-short-video-df579760dafca537c298:attempt:1` |
| INTERMEDIATE | ARTICLE | `job-intermediate-article-f6fbf5eaf6db88a6ec05` | `job-intermediate-article-f6fbf5eaf6db88a6ec05:attempt:1` |
| INTERMEDIATE | CAROUSEL | `job-intermediate-carousel-66617e6b2c94dcfbaf0e` | `job-intermediate-carousel-66617e6b2c94dcfbaf0e:attempt:1` |
| INTERMEDIATE | SHORT_VIDEO | `job-intermediate-short-video-ff17afd6125e0561dc1d` | `job-intermediate-short-video-ff17afd6125e0561dc1d:attempt:1` |

Every row binds back to source `source-026273fcf1b04d5f` and the same source SHA-256 above.

## Authoritative event identity

| Rev | Type | Event id | Transition id | Resource |
|---:|---|---|---|---|
| 1 | `source.updated` | `ev-627de9eae9964889b989c99eebb795bd` | `tr-64e5c16c1f864204924824568d4dc701` | `source-026273fcf1b04d5f` |
| 2 | `cell.updated` | `ev-67c54723f3954fcf882dcbc68386b2b9` | `tr-04872b9d48574855a1dcd7d188b3c82f` | `job-advanced-article-d4209ee1a13a72e6e9e6` |
| 3 | `cell.updated` | `ev-7a132d7fe4d445f08c3d43d344f76ee8` | `tr-ccab51e68d414627be29305699ab291d` | `job-advanced-carousel-a3f51ce099a8ec6c51fa` |
| 4 | `cell.updated` | `ev-e3bac0cda6ea4d758f32ec074e37c4de` | `tr-5824ca096b064e5289d09a3ebcaa2090` | `job-advanced-short-video-152ec5870c2c3e69d32c` |
| 5 | `cell.updated` | `ev-ebb777ed9cbb4877adbae07c96ac80fa` | `tr-b759ab8acc7344a5bab7ab023a0181be` | `job-beginner-article-189371ab3d3c7ad3f594` |
| 6 | `cell.updated` | `ev-29f48383c0d24dc0ab60a40e0707717d` | `tr-b71e82606dc14b1481f6dce6d74ece5f` | `job-beginner-carousel-7d7c505e07935a7ce518` |
| 7 | `cell.updated` | `ev-19a80d2b6f93490f9bd5e1852b72c810` | `tr-022056978b4b48898ab582b676ae8507` | `job-beginner-short-video-df579760dafca537c298` |
| 8 | `cell.updated` | `ev-b5f6bde0f52e4adc9b599a11df798713` | `tr-dac5c17ee4194797be96a2b573baa497` | `job-intermediate-article-f6fbf5eaf6db88a6ec05` |
| 9 | `cell.updated` | `ev-b6a8f389a97e4d7fbd2b1c3b51cf6cb1` | `tr-2a003a540c75492697ef23a374ee95dc` | `job-intermediate-carousel-66617e6b2c94dcfbaf0e` |
| 10 | `cell.updated` | `ev-f1092f5ce1de466dab32dfcefbf35dfc` | `tr-cf32cc32c7b046388592d4c39091f909` | `job-intermediate-short-video-ff17afd6125e0561dc1d` |
| 11 | `run.phase_changed` | `ev-c62a3e6e5829413eae9739bf845c7dcc` | `tr-00b15bd6c26c4c8ba3f44f36f8c3a880` | `run-w006-t014-a01-final-demo` |

Each event has `result_revision=1` for its own resource mutation. The ordered product event revision is the `1..11` column above.

## Config / toolchain identity

- `data/evals/production/w006/evaluator_config_v001.json`: `sha256:4430300193715c3745424dffa011d970e7662b5c9ff2c67493ed05e38c76d2c5`
- `data/evals/production/w006/partition_manifest_v001.json`: `sha256:1272581035f092da62100d65565aa87b160324afeaafe1dcb2d2ae496ed1309d`
- `pyproject.toml`: `sha256:cd23fde7ba48562be54f2e5ec93921841ed9ecfb3314d3601852c94adc7d0af6`
- `toolchain.lock.json`: `sha256:4f7be5bcf6ecd8e04d38686d3c11f4fb22f1fb062df3f5a0b03526b70b73f0de`
- `uv.lock`: `sha256:cf1ecfeab5d4a6d01868db8ae45339e3cfc77f0e77d7ebb27a21dba6ef8036ea`
- Python: `3.13.15`
- uv: `0.12.18`

## Build / deploy identity boundary

Build identity exists and is bound above through the exact PR merge ref, workflow run/job, toolchain and configuration hashes.

Deployment identity does **not** exist for representative production because no production runtime/database/deployment topology is locked and available. The capture records:

- runtime lock: `NONE`
- database lock: `NONE`
- parser lock: `NONE`
- frontend lock: `NONE`
- deployment lock: `NONE`
- deploy evidence status: `MISSING_PRODUCTION_EVIDENCE`

No deploy id, supported-user count, production SLO, RTO or RPO is fabricated from the reference execution.

## Independent audit linkage

The complete `PROD-001..017` classification is persisted at `artifacts/w006-t014/a01/audit-matrix.json`.

Independent conclusion:

- full-production contract rows classified `PASS`: `1` (`PROD-015`, research-gated architecture governance);
- rows classified `PRODUCTION_UNKNOWN/BLOCKER`: `16`;
- W006 achieved accepted reference scope: evidence-complete for that bounded scope;
- blanket production readiness: `FALSE / NOT_AUTHORIZED`;
- follow-up required: representative production-topology qualification, independent human calibration + HELD_OUT replication, and fresh representative provider/model comparison.
