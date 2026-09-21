# Recipient-facing interactive app — W004-T014

This is the minimal local application added to close blind-review findings F-002/F-003 without weakening the project evidence posture.

## What it proves

The app accepts **raw text**, a **local PDF path**, or a **PDF upload**; hashes the raw input bytes; records parser identity/version; applies a fail-closed source-trust gate; and, only when the source is ready, invokes the canonical `build_3x3_variant_specs` contract for `BEGINNER / INTERMEDIATE / ADVANCED × ARTICLE / CAROUSEL / SHORT_VIDEO`. It also projects the integrated W004-T012 repair lineage and evidence posture.

The 3×3 content shown by this app is deliberately labeled `MECHANICS_ONLY`. Audience thresholds remain `DIAGNOSTIC_ONLY`; real provider/model quality, latency, usage and cost remain `PRODUCTION_UNKNOWN/BLOCKED`; production release readiness remains pending the canonical downstream gates.

## Run locally

From a clean repository checkout:

```bash
python -m pip install 'pydantic==2.13.4' 'pypdf>=5,<6'
PYTHONPATH=src python app/recipient/server.py --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765`.

`pypdf` is the recommended local PDF text-layer adapter for this demo. If it is absent, the app can fall back to a system `pdftotext` executable. The adapter boundary is replaceable and this task makes **no parser-winner claim**.

## Demonstration path

1. Paste a real public financial-document text excerpt and process it. Confirm the raw-input SHA-256, parser identity (`plain-text`), `SOURCE_READY`/hard-gate state and the nine canonical 3×3 job IDs.
2. Process a locally downloaded real public financial PDF either via file upload or by entering its path. Confirm that the SHA-256 is over the raw PDF bytes and that parser/version/confidence are visible.
3. Use a PDF/text sample whose extraction is low-confidence or table-like without resolvable row/column roles. Confirm it becomes `SOURCE_BLOCKED` / non-PASS and all 3×3 jobs are disabled.
4. Inspect the W004-T012 panel: the persisted controlled lineage remains `FAIL → PASS`, with fresh hard gates and sibling immutability. This lineage is inherited evidence, not fabricated per-input provider evidence.

## Focused tests

```bash
PYTHONPATH=src python -m pytest -q tests/recipient_app
```

The tests cover text ingestion, raw PDF-path hashing through an injected replaceable adapter, low-confidence fail-closed behavior, table-role ambiguity fail-closed behavior, exact 3×3 planning, recipient-facing provenance rendering, and repair/evidence-state rendering.

## Evidence boundaries

- `SOURCE_READY/PASS` applies only to the **source-ingestion gate** implemented here; it is not a provider-quality or production-readiness PASS.
- The mechanical previews are not LLM/provider outputs and do not establish content quality.
- No human annotations, confusion matrices, provider usage, latency or commercial cost are created by this app.
- PDF text extraction without table-cell role provenance is intentionally blocked when table-like structure is detected. OCR and parser-quality selection remain outside this task and must not be inferred from a successful text-layer extraction.
