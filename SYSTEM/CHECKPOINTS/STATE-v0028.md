# CHECKPOINT STATE v0028

`STATE_VERSION: 0028`
`PROTOCOL_VERSION: 1.6.0`
`PROJECT_STATUS: ACTIVE`
`CURRENT_PHASE: 6 — Adversarial Optimization`

## Canonical facts

- W004-T018-A01 is integrated from Issue #118 / PR #120 after direct inspection of the concrete T017 video artifact.
- T018 verdict: `BLIND_REVIEW: NOT_PASS` for evaluator-facing usability. The T017 MP4 is real and measured at `7.200s <= 300s`, but is silent/too compressed to explain the full journey to a cold evaluator.
- The real BCB PDF negative-control correctly fails closed as `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` because cell-role provenance is unavailable; this behavior must not be weakened for demo purposes.
- F-002 raw text/PDF ingestion and F-003 interactive interface are technically remediated; F-007 consolidated report exists but evaluator-facing README/submission narrative requires refresh.
- W004-T019-A01 is READY after post-merge binding: produce a deliberately paced real-browser final demo with a genuine `SOURCE_READY/PASS` success path first, then frame the BCB fail-closed path as a safety negative-control, and refresh README/submission packet with exact final artifact provenance.
- W004-T020-A01 is PLANNED and depends on T019 for independent blind/adversarial re-review.
- W004-T004 provider evidence and W004-T005 independent human evidence remain external blockers; T006/T007/T008 stay dependency-blocked.
- No production-readiness, human-calibration, provider-selection, semantic-backend, or parser-winner claim is authorized.

## Recovery

Resume from canonical `SYSTEM/STATE.md` at `STATE_VERSION: 0028`, then bind Issue #121 to the exact post-merge `main` SHA and execute W004-T019-A01. Release W004-T020 only after T019 integration.
