# W004-T017 — real browser demo capture in CI

This package attempts the final-video hard gate with a real GitHub-hosted Chromium session against the integrated recipient-facing application.

## What the workflow proves mechanically

The workflow checks out the triggering task commit, downloads the public Banco Central do Brasil `Relatório de Estabilidade Financeira — maio 2026` PDF, validates `%PDF-` magic bytes, hashes the exact raw bytes, starts `app/recipient/server.py`, and drives the UI with Playwright Chromium while browser video recording is enabled.

The recorded path must visit and assert:

1. home evidence boundaries (`MECHANICS_ONLY`, `DIAGNOSTIC_ONLY`, `PRODUCTION_UNKNOWN`);
2. real text ingestion reaching `SOURCE_READY/PASS` and all 9 cells of the 3×3 mechanics view;
3. persisted T012 `FAIL → repair → PASS` evidence, fresh-gate/sibling-immutability truth values, and non-claim labels;
4. real BCB PDF upload, with the recipient UI displaying the exact SHA-256 computed over the downloaded raw PDF bytes;
5. the PDF 3×3 view and repair/evidence sections.

Playwright's browser recording is converted to MP4 with `ffmpeg`; `ffprobe` measures the resulting duration and the run hard-fails if it exceeds 300 seconds. The manifest persists task/CI provenance, source/video hashes, duration, runtime/browser/tool versions, DOM/content assertions, and evidence boundaries.

## Fail-closed behavior

There is no synthetic PDF fallback. If BCB download, PDF magic validation, application startup, browser recording, DOM/content assertions, conversion, hashing, or duration measurement fails, the capture is not considered successful.

A screenshot, storyboard, metadata-only package, or an empty/invalid video must never be promoted as satisfying the video gate.

## Evidence boundaries

A successful recording is technical/mechanical evidence of the recipient-facing flow only. It does **not** create human calibration evidence, real provider/model quality evidence, provider latency/cost evidence, a parser-winner claim, or production/release readiness. Those remain independently governed by their existing blockers and gates.

## Local equivalent

With Chromium/Playwright, `ffmpeg`, `ffprobe`, `pydantic`, and `pypdf` installed:

```bash
python scripts/demo_capture_ci/run_capture.py
python -m pytest -q tests/demo_capture_ci/test_capture_helpers.py
```

The default output directory is `/tmp/w004-t017-demo-ci` and can be changed with `DEMO_CI_OUTPUT_DIR`.
