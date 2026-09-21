# Final demo capture package — W004-T016-A01

This directory is the deterministic fallback required by the dispatch when the worker runtime cannot create a trustworthy real recording.

## Terminal state for this attempt

`TASK_BLOCKED_MANUAL_CAPTURE_REQUIRED`

The worker runtime could not resolve `github.com`, so it could not obtain/run the full repository checkout and record the recipient-facing application. No substitute animation, synthetic screenshot sequence, or fabricated provider/human evidence is accepted as a video artifact.

The package below makes the remaining manual capture reproducible and auditable on a normal workstation.

## Exact provenance boundary

The corrected recipient-facing application was integrated at:

`0980534866ed84c2f6af28453f6cb20cd1c7efba`

`prepare_capture.py` refuses a checkout that is not a descendant of that commit. It records the actual capture `HEAD` SHA rather than pretending the base SHA is the recording version.

## Public financial PDF

Default source:

- **Banco Central do Brasil — Relatório de Estabilidade Financeira — maio 2026**
- public page: `https://www.bcb.gov.br/publicacoes/ref/202605`
- PDF: `https://www.bcb.gov.br/content/publicacoes/ref/202605/RELESTAB202605-refPub.pdf`

The capture preflight downloads the PDF, validates `%PDF-` magic bytes, computes SHA-256 over the exact raw bytes, and persists URL/hash/size in `artifacts/demo/capture_preflight.json`. The app must show the same raw-input SHA-256 after PDF ingestion.

## One-path operator sequence

From the exact checkout to be recorded:

```bash
python -m pip install 'pydantic==2.13.4' 'pypdf>=5,<6'
python scripts/demo_capture/prepare_capture.py
PYTHONPATH=src python app/recipient/server.py --host 127.0.0.1 --port 8765
```

Then record the single take in `CAPTURE_RUNBOOK.md`. Keep a visible clock or recorder timer. The target is `04:40`; the hard cap is `05:00`.

After recording:

```bash
python scripts/demo_capture/finalize_capture.py /absolute/path/to/final-demo.mp4
python scripts/demo_capture/verify_capture.py \
  --video /absolute/path/to/final-demo.mp4 \
  --pdf artifacts/demo/source_document.pdf
```

`finalize_capture.py` uses `ffprobe` to measure the container duration and rejects anything above `300.000s`. It also SHA-256 hashes the video. It intentionally leaves visual-content review as `REQUIRES_HUMAN_VISUAL_REVIEW`; duration/hash automation cannot prove what is visible in the frames.

## Required final evidence

A terminal task completion is allowed only after a real video exists (or an immutable/discoverable submission-ready reference exists) and the final manifest records:

- exact recording `HEAD` SHA;
- source PDF URL + raw-byte SHA-256;
- video SHA-256;
- measured duration `<=300s`;
- visible real recipient UI;
- text path and public PDF path;
- source provenance/hash and source-trust gate;
- canonical 3×3 view;
- persisted `FAIL → repair → PASS` lineage;
- visible `MECHANICS_ONLY`, `DIAGNOSTIC_ONLY`, and `PRODUCTION_UNKNOWN/BLOCKED` boundaries.

No human annotations, confusion matrices, provider quality, latency, usage, cost, parser winner, or production readiness may be invented to make the demo look more complete.
