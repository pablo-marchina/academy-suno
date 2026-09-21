# W004-T016-A01 — real capture still required

`STATUS: TASK_BLOCKED_MANUAL_CAPTURE_REQUIRED`

No video is stored here because this worker runtime could not obtain/run the full checkout and therefore could not truthfully record the real recipient-facing UI.

Do not replace the missing recording with a storyboard, generated animation, fabricated screenshot sequence, or claimed duration.

Use:

- `docs/demo/final/README.md`
- `docs/demo/final/CAPTURE_RUNBOOK.md`
- `scripts/demo_capture/prepare_capture.py`
- `scripts/demo_capture/finalize_capture.py`
- `scripts/demo_capture/verify_capture.py`

Expected runtime artifacts after a real capture (not committed by this blocked attempt):

- `artifacts/demo/source_document.pdf`
- `artifacts/demo/capture_preflight.json`
- `artifacts/demo/final_capture_manifest.json`
- the real video file or an immutable/discoverable submission-ready reference.
