# Blind / adversarial video review — W004-T018-A01

`TASK_ID: W004-T018`
`ATTEMPT_ID: A01`
`BASE_STATE_VERSION: 0027`
`BASE_COMMIT_SHA: abd1c5c470719a68545023bbbf65cab46e708dd5`
`REVIEW_DISPOSITION: NOT_PASS_AS_FINAL_EVALUATOR_DEMO`
`TECHNICAL_CAPTURE_GATE: PASS`
`DURATION_GATE: PASS`
`CONFIDENCE: HIGH`

## Executive disposition

The concrete T017 artifact is a real, provenance-bound Playwright/Chromium browser recording, and its MP4 duration is genuinely below the five-minute hard cap. That is materially stronger than the prior storyboard/manual-capture posture.

However, the artifact should **not** be treated as the final evaluator-facing demo. Direct inspection shows a 7.200-second, silent capture whose final public-BCB-PDF path lands in `SOURCE_BLOCKED / REVIEW_REQUIRED` with `LOW` source trust because table-role ambiguity is detected. The 3×3 rows visible for that PDF are consequently `BLOCKED_SOURCE`. This is a valid and useful fail-closed safety demonstration, but it is not an intelligible final demonstration of a successful end-to-end recipient workflow.

The correct distinction is therefore:

- real recording exists: **PASS**;
- exact MP4 is <=300s: **PASS**;
- code/interface is real and is exercised: **PASS**;
- final evaluator can comfortably understand the intended success path from this 7.2s recording alone: **NOT PASS**;
- final project/release readiness: **NOT PASS / still blocked by independent human/provider gates and downstream fan-in**.

## Evidence directly inspected

Primary GitHub Actions artifact:

- run: `35625349017`;
- artifact: `10652146281`;
- file: `browser-demo.mp4`;
- expected SHA-256: `f04852fb11183e4e6bc8690d80c5ef26d6993edc6aa7ec71660b9e3b670c3bc4`;
- observed local SHA-256 after artifact download: exact match;
- observed duration via `ffprobe`: `7.200000s`;
- video: H.264, `1280x720`, `25 fps`;
- audio stream: none detected;
- BCB PDF SHA-256 after artifact download: `4ac6a958cbff7571aad3f0125042f4b71890a70ec36e9ad9009b537e6458ce68`, exact match to T017 provenance.

Representative directly inspected frames:

- around `0.2s`: recipient-facing input screen, no file selected;
- around `1.0–4.0s`: BCB PDF selected on the input screen; evidence-boundary labels are visible;
- around `5.6s`: result screen shows `Input: PDF`, parser `pypdf 5.9.0`, confidence `0.960`, `Status: SOURCE_BLOCKED`, `Hard gate: REVIEW_REQUIRED`, `Source trust: LOW`, `Table-role ambiguity: True`, exact BCB input SHA-256, and warning `TABLE_ROLE_AMBIGUITY:TEXT_LAYER_HAS_NO_CELL_ROLE_PROVENANCE`;
- around `5.6–6.5s`: 3×3 rows visible as `BLOCKED_SOURCE`, followed by integrated evidence/repair and non-claim sections.

T017's persisted manifest also states that a text-ingestion path reached `SOURCE_READY/PASS` and nine mechanics-only cells while recording was active. That DOM/content assertion is credible technical evidence that the path was reached. It does **not** by itself make the fleeting 7.2-second video an understandable final narrative for an external evaluator.

## Re-evaluation of W004-T013 findings

### F-001 — final real demo video absent / discoverability gap

**Reclassified, but not closed as a final-demo criterion.**

The statement “no real video exists” is no longer true: the T017 Actions artifact is concrete, hash-bound and directly inspectable. The technical existence portion is therefore remediated.

The evaluator-facing/discoverability portion remains open because:

1. `docs/submission/SUBMISSION_PACKET.md` still states `F-001 final real demo video absent | CRITICAL | OPEN`;
2. the packet does not point the evaluator to T017 run/artifact/hash/duration;
3. the concrete 7.2s artifact is too compressed to function as a convincing final walkthrough;
4. the most legible final state is a correctly blocked PDF path, not a clearly explained successful primary journey.

Disposition: **PARTIAL — technical existence PASS; final evaluator demo NOT PASS.**

### F-002 — raw PDF/text ingestion not demonstrated

**Technically remediated; submission-facing proof remains weak/stale.**

T014 implemented real recipient-facing text/PDF input, raw-byte hashing and provenance. T017 used the actual app and uploaded the real BCB PDF bytes with the expected hash visible in the UI. Thus the original “no recipient-facing raw PDF/text entry point” finding is no longer valid at implementation level.

Residual issue: the concrete public BCB PDF ends fail-closed (`SOURCE_BLOCKED`) because table-role provenance is ambiguous. This is defensible safety behavior, but a final demo should also visibly and slowly demonstrate a successful `SOURCE_READY/PASS` input that proceeds to nine 3×3 cells. The current submission packet still marks F-002 OPEN and does not bind the T014/T017 evidence.

Disposition: **IMPLEMENTATION PASS; FINAL DEMO/PACKET UPDATE REQUIRED.**

### F-003 — interactive app/dashboard adherence risk

**Technically remediated.**

The recipient app is a real interactive HTTP surface and the T017 browser artifact visibly exercises it. The original concern that the evaluator-facing surface was only a read-only HTML snapshot is superseded by T014/T017 evidence.

Residual issue: the submission packet and top-level README do not make this new recipient app the obvious evaluator entry point, so discoverability/narrative alignment remains a packaging risk.

Disposition: **TECHNICAL PASS; PACKAGING UPDATE REQUIRED.**

### F-007 — no consolidated final experimental report

**Remediated at artifact level.**

`docs/report/EXPERIMENTAL_REPORT.md` and `docs/submission/SUBMISSION_PACKET.md` exist and provide the intended consolidated reporting layer. They correctly preserve blocked human/provider evidence rather than inventing it.

Residual issue: the packet is now temporally stale relative to T014/T017 and therefore contradicts current implementation/video evidence on F-001/F-002/F-003/F-008.

Disposition: **PASS AS ARTIFACT; REFRESH REQUIRED.**

### F-008 — actual <=5:00 compliance unverified

**Closed for the concrete T017 MP4.**

Direct measurement confirms `7.200s`, so the <=300s duration criterion is objectively satisfied for this file.

This is not equivalent to saying the artifact is a good final demo; here the unusually short duration is itself part of the usability problem.

Disposition: **PASS — concrete duration verified.**

### F-005 / F-006 — external human/provider evidence

**Unchanged.**

No independent human-gold calibration/confusion matrices or authorized observed provider quality/latency/usage/cost evidence are added by T014/T017/T018. They remain external hard blockers, and no production-readiness claim is authorized.

## New / elevated risks

### N-001 — evaluator-video usability mismatch — HIGH

A 7.2-second silent recording can prove that browser actions occurred, but it does not give a human evaluator adequate time to understand the problem, success path, provenance, 3×3 behavior, repair evidence and evidence-boundary semantics. Technical capture success and communication success are different gates.

### N-002 — public-PDF path visually demonstrates a blocked outcome — HIGH

The final visible BCB PDF state is a legitimate fail-closed result caused by table-role ambiguity. Without explanation, a reviewer can reasonably interpret this as “the PDF flow does not work.” The safety behavior should be shown as an explicit secondary negative-control example, not as the primary final state of the demo.

### N-003 — submission packet / README drift — HIGH

The current submission packet still declares F-001/F-002/F-003/F-008 open in their pre-T014/T017 form, and the root README does not surface the recipient app or the T017 artifact as the main evaluator journey. A reviewer following the packet can miss capabilities that now exist or encounter contradictory claims.

### N-004 — artifact retention horizon — MEDIUM

The accepted T017 Actions artifacts report expiry on `2026-12-20T16:24:02Z`. If evaluation/submission can occur later, the exact accepted MP4 must be copied to durable submission storage while preserving SHA-256 and provenance.

## Prioritized fixes

### P0 — produce a new evaluator-facing recording using the existing T017 capture infrastructure

Keep it well below five minutes, but deliberately paced. The recording should visibly show, in order:

1. the recipient-facing input surface and what is being demonstrated;
2. a successful real input path reaching `SOURCE_READY/PASS`;
3. the exact 3×3 output surface with nine cells;
4. provenance/hash/source-trust evidence;
5. the persisted `FAIL → repair → PASS` evidence panel;
6. explicit `MECHANICS_ONLY / DIAGNOSTIC_ONLY / PRODUCTION_UNKNOWN` boundaries;
7. optionally, the BCB complex PDF as a **separate negative-control** demonstrating fail-closed table-role ambiguity;
8. a brief closing screen stating what is proven versus still blocked.

Narration is not strictly required, but the final artifact needs either narration or sufficiently persistent on-screen framing/captions so that a cold evaluator can follow it at normal playback speed.

### P0 — refresh the submission packet

Replace stale F-001/F-002/F-003/F-008 wording with the current evidence split. Bind the exact T017/new-final-video run, artifact/link, SHA-256, duration and retention information. Make the recipient app the explicit evaluator entry point.

### P1 — update the root README / evaluator start path

Surface the recipient app command/documentation and link the consolidated report, refreshed submission packet and accepted final video from one obvious “review this” section.

### P1 — preserve the BCB fail-closed example

Do not weaken the source-trust gate merely to make the demo green. The BCB result is valuable evidence that ambiguous table-role provenance is not silently promoted. Present it as a safety/control example after a separately demonstrated success path.

### P1 — durable video storage

Copy the accepted final MP4 to submission-controlled durable storage before Actions retention becomes a risk, recording the exact hash and provenance binding.

## Final review disposition

`BLIND_REVIEW: NOT_PASS`

The internal implementation/remediation story is materially better than at T013:

- F-002 technical input boundary: remediated;
- F-003 interactive app existence: remediated;
- F-007 consolidated report: remediated;
- F-008 concrete duration: remediated;
- F-001 real recording existence: remediated technically.

But the concrete 7.2s MP4 should **not** be promoted as the final evaluator demo, and the packet is stale relative to the current implementation/evidence. Independent human and provider evidence remain unresolved external blockers, so final project/release PASS is not available regardless of video remediation.
