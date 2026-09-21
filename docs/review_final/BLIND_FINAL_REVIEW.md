# Blind / adversarial final package review — W004-T020-A01

`TASK_ID: W004-T020`  
`ATTEMPT_ID: A01`  
`BASE_STATE_VERSION: 0029`  
`BASE_COMMIT_SHA: ea6dbcdab3ca7b61117824b0527e45252370bae9`  
`WORKER_BRANCH: worker/W004-T020-A01`  
`VIDEO_PACKAGE_REVIEW: PASS`  
`OVERALL_PROJECT_RELEASE_READINESS: PENDING_EXTERNAL_GATES`  
`CONFIDENCE: HIGH`

## Executive disposition

I reviewed the current evaluator-facing package as a cold evaluator and directly downloaded and inspected the concrete T019 Actions artifacts rather than accepting T019's own conclusion.

The **video/package scope passes this independent review**. The accepted 69.12-second browser capture is paced and intelligible enough to communicate the intended journey: a positive `SOURCE_READY / PASS` text path comes first, provenance/source trust is exposed, the 3×3 mechanics surface is introduced as 9/9 mechanics-only, persisted `FAIL → repair → PASS` evidence is shown, evidence boundaries remain explicit, and the real Banco Central do Brasil PDF is then framed as a separate fail-closed safety negative-control. The prior T018 `HIGH` communication/packaging findings are materially remediated.

This is **not an overall project/release PASS**. F-005/F-006 remain external blockers, W004-T008/final fan-in remains pending, and no human-calibration, provider-selection, provider-quality or production-readiness claim is authorized.

No new `CRITICAL` or `HIGH` finding was identified in this review. Two `MEDIUM` residual risks remain: Actions artifact retention, and the fact that the successful 3×3 table is taller than the 720p viewport so all nine successful rows are not simultaneously visible even though the video caption and independently bound DOM/manifest evidence establish the exact 9/9 count.

## Continuity and review independence

- protocol observed: `1.6.0`;
- canonical state observed: `STATE_VERSION 0029`;
- Issue #122 bound A01 to `ea6dbcdab3ca7b61117824b0527e45252370bae9`;
- observed `main` SHA at start matched that bound SHA exactly;
- W004-T019 was already integrated in the bound base;
- isolated branch `worker/W004-T020-A01` was created from the exact bound SHA;
- mandatory `TASK_STARTED` was persisted before substantive work;
- the T019 primary and provenance artifacts were downloaded directly from GitHub Actions for this review;
- no canonical coordination/state/ledger/wave file is modified by this worker.

`CONTINUITY_CHECK: PASS`

## Direct artifact and provenance validation

Accepted Actions run inspected: `35636285651`.

### Primary artifact

- artifact ID: `10656720873`;
- downloaded ZIP SHA-256 observed independently: `7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`;
- GitHub-reported digest: `sha256:7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`;
- exact digest match: **PASS**;
- GitHub-reported expiry: `2026-12-20T18:06:45Z`.

### Provenance artifact

- artifact ID: `10656775849`;
- downloaded ZIP SHA-256 observed independently: `0f8e8e786afca176a19b9d0c70c18b9134a37ee91d234dc53a87286b38c692b0`;
- GitHub-reported digest: `sha256:0f8e8e786afca176a19b9d0c70c18b9134a37ee91d234dc53a87286b38c692b0`;
- exact digest match: **PASS**;
- GitHub-reported expiry: `2026-12-20T18:06:45Z`.

The downloaded provenance data binds the accepted run to capture commit `ffaa235e31667d1aab9a1f24253e647579e394e1`, primary artifact identity/digest/expiry, final-video byte hash and the declared source identities. The repository CI-evidence JSON is consistent with the downloaded provenance artifact.

### Concrete final MP4

`final-demo.mp4` was inspected from the downloaded primary artifact.

- observed SHA-256: `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5` — exact expected match;
- observed size: `1,388,430` bytes;
- observed duration via `ffprobe`: `69.120000 s`;
- hard cap: `300 s`;
- duration gate: **PASS**;
- codec: H.264;
- dimensions: `1280×720`;
- frame rate: `25 fps`;
- streams: one video stream, no audio stream.

This closes the narrow integrity/duration question using the actual accepted MP4 bytes, not task prose or metadata alone.

### Real BCB negative-control source

The primary artifact contains `bcb-financial-source.pdf` with independently observed SHA-256:

`4ac6a958cbff7571aad3f0125042f4b71890a70ec36e9ad9009b537e6458ce68`

This exactly matches the source binding used by T019. The public BCB source URL resolves to the Banco Central do Brasil `Relatório de Estabilidade Financeira`, May 2026, and the downloaded artifact preserves the real PDF bytes rather than a synthetic fallback.

## Cold-evaluator review of the actual video

Representative frames were extracted independently from the final MP4 across its timeline. The sequence is understandable without relying on hidden task context:

1. **Opening / recipient app.** The real recipient-facing text/PDF input surface is visible with an on-screen caption explaining the app → provenance → source-trust → 3×3 → repair journey and preserving external blockers.
2. **Positive path first.** A controlled text source is explicitly framed as the positive path before the PDF negative-control.
3. **Successful provenance.** The result visibly reaches `SOURCE_READY`, hard-gate `PASS`, `HIGH` source trust and displays the exact source SHA-256.
4. **3×3 mechanics.** The successful audience × format table is shown under a caption that states `9/9` and explicitly says this is mechanics, not provider-quality evidence. The exact 9-row count is also bound by the artifact DOM assertions/manifest.
5. **Persisted repair.** The evidence panel visibly shows `FAIL → repair → PASS`, distinct before/after hashes, fresh-gate truth and accepted-sibling immutability.
6. **Evidence boundaries.** `MECHANICS_ONLY`, `DIAGNOSTIC_ONLY`, `PRODUCTION_UNKNOWN / BLOCKED` and production-readiness pending states remain visible rather than being averaged into a green release claim.
7. **BCB negative-control.** The real public PDF is explicitly introduced as a safety negative-control. The result visibly remains `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW`, shows `Table-role ambiguity: True`, the exact PDF hash and the table-role-provenance warning.
8. **Fail-closed downstream state.** The video closes by showing the nine downstream rows as `BLOCKED_SOURCE` and explicitly frames this as safety behavior, not a masked success.

### Intelligibility and pacing

The 69.12-second duration and deliberate hold times materially fix the T017/T018 usability failure. Captions remain on screen long enough to orient a cold reviewer, and the successful path is shown before the blocked PDF example. Lack of audio is not a blocker because the visual captions provide the necessary framing.

### 3×3 visual-completeness residual

The successful 3×3 table is taller than the 720p viewport. During the reviewed hold, only the upper portion is simultaneously visible; the video does not slowly scroll every successful row before moving to repair. The exact 9/9 count is still strongly evidenced by the caption, actual rendered table, artifact DOM assertions and CI manifest, so this does not rise to a `HIGH` evidence or comprehension failure. It remains a `MEDIUM` presentation refinement for a maximally self-contained evaluator video.

## README and submission-packet review

The root `README.md` is current relative to T019 and provides an obvious `Evaluator quick start — recipient app`, local launch command, exact run/artifact/hash/duration binding, final-demo documentation link and explicit non-claims.

`docs/submission/SUBMISSION_PACKET.md` is also current relative to T019. It points the reviewer to the recipient app, final paced demo docs, machine-readable CI binding, T019 result, experimental report, evidence packet and final-review checklist. Its claim register correctly separates task-scope evidence from human/provider/production claims and binds the accepted artifact IDs, digests, expiry, MP4 hash/duration and both source hashes.

The package no longer has the T018 `HIGH` drift where the README/packet contradicted the actual recipient app/video state.

## Re-evaluation of requested findings

### F-001 — final real demo / evaluator usability / discoverability

`PASS — VIDEO_PACKAGE_SCOPE`.

A concrete, hash-bound real-browser MP4 exists, is directly discoverable from the root evaluator path, is deliberately paced, and presents the success journey before the safety negative-control. The prior T018 evaluator-usability blocker is remediated.

Residual: artifact retention remains `MEDIUM` because the exact accepted video is currently stored as an expiring Actions artifact rather than as a durable repository/submission-controlled binary.

### F-002 — recipient-facing PDF/text ingestion demonstration

`PASS — REVIEW_SCOPE`.

The final video visibly demonstrates the successful text-ingest path and then the real PDF upload path. The PDF's blocked result is correct fail-closed source-trust behavior, not a missing ingestion implementation.

### F-003 — interactive app/dashboard adherence and evaluator entry path

`PASS — REVIEW_SCOPE`.

The evaluator sees and interacts with a real HTTP recipient app in the browser, and the root README makes that app the first evaluator quick-start path. The prior read-only/discoverability concern is no longer `HIGH`.

### F-007 — consolidated report / submission package

`PASS`.

The consolidated report/submission layer exists and the submission packet is refreshed to the accepted final-demo evidence while preserving open blockers and evidence boundaries.

### F-008 — actual <=5:00 duration

`PASS`.

Independent `ffprobe` inspection of the accepted MP4 measured exactly `69.120000 s <= 300 s`.

### F-005 — independent human calibration

`BLOCKED / PENDING — unchanged external blocker`.

Two genuinely independent primary human streams, valid agreement/adjudication and observed confusion matrices remain absent. Nothing in the demo is treated as human calibration.

### F-006 — real provider evidence

`BLOCKED / PRODUCTION_UNKNOWN — unchanged external blocker`.

No authorized observed provider quality/latency/usage/cost evidence is introduced by the demo. No provider/model selection is authorized.

## Critical/high finding check

`NEW_CRITICAL_FINDINGS: 0`  
`NEW_HIGH_FINDINGS: 0`

The three prior T018 high risks — unusably compressed final video, unframed blocked PDF outcome, and README/submission drift — are independently observed as remediated in the accepted T019 package.

## Residual risks

### R-020-01 — accepted-video retention — MEDIUM

Both accepted Actions artifacts report expiry at `2026-12-20T18:06:45Z`. A recursive inspection of the bound repository tree found no committed `.mp4` path. Therefore the exact accepted video remains dependent on expiring Actions retention unless it has separately been copied to submission-controlled durable storage outside the repository.

Required mitigation before that horizon matters: copy the exact accepted MP4/package to durable submission-controlled storage and preserve the MP4 SHA-256, ZIP digest, run ID, artifact ID and capture commit binding.

### R-020-02 — positive 3×3 simultaneous viewport coverage — MEDIUM

The successful table's upper rows and 9/9 framing are visible, but all nine successful rows do not fit simultaneously in the 720p viewport and the recording does not traverse every row. This is a presentation-strength refinement rather than a provenance/mechanics gap because the exact count is independently bound by DOM assertions and artifact manifests.

### R-020-03 — external submission logistics — MEDIUM / external

Deadline, final submission mechanism and named decision/ownership workflow remain operational unknowns in canonical state. This does not invalidate the video/package review but should remain visible for final delivery planning.

## Evidence boundaries preserved

```text
video/package blind review:          PASS
mechanics:                           MECHANICS_ONLY
audience thresholds:                 DIAGNOSTIC_ONLY
human calibration:                   BLOCKED / PENDING
provider quality/latency/usage/cost: PRODUCTION_UNKNOWN / BLOCKED
provider/model preference:           NOT_AUTHORIZED
W004-T008 final fan-in:               PENDING
production/release readiness:        PENDING_EXTERNAL_GATES
```

## Final disposition

`VIDEO_PACKAGE_REVIEW: PASS`

The concrete accepted T019 video and refreshed evaluator package satisfy the independent final-demo/package review scope. The result may close the **internal video/package blind-review gap** after orchestrator integration.

`OVERALL_PROJECT_RELEASE_READINESS: PENDING_EXTERNAL_GATES`

This review must not be converted into an overall project, release or production PASS. F-005/F-006 and their dependent work remain unresolved, W004-T008 remains pending, and external final-delivery logistics are not established.
