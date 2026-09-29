# DR-7004 — Source-original parser/OCR production qualification

- **Task:** W007-T004-A01
- **Date:** 2026-09-24
- **Decision state:** `NO_PREFERENCE/PENDING_EVIDENCE`
- **Production parser lock:** **NOT AUTHORIZED**
- **Methodology:** `W005-BENCHMARK-METHODOLOGY-V002` + `SYSTEM/DECISION_RESEARCH_GATE.md`

## Decision question

Which document parsing/OCR path, if any, has enough representative source-original public-financial evidence to become the production default while preserving content identity, page/node provenance, table roles, trust state, and fail-closed handling?

## Alternatives exercised

Five materially different local paths were executed on the same bounded source groups: `pypdf` text extraction, Poppler `pdftotext -layout`, PyMuPDF table extraction, pdfplumber table extraction, and rendered-page Tesseract OCR. Managed document-AI providers were intentionally not executed because this worker has no authorized credentials/billing context; their absence is evidence missingness, not evidence of inferiority.

## Representative evidence

Three source-original public-financial PDFs were hashed and executed: Petrobras 2T26 (digital/table-heavy), Banco Central do Brasil RPM 1T26 presentation (digital/chart-heavy), and the Federal Reserve Board 1914 annual report hosted by FRASER (historical scan/OCR candidate). Exact hashes, byte sizes, repeated latencies, role metrics, failure controls, environment versions, workflow run and artifact digest are persisted in `artifacts/w007-t004/a01/raw-evidence.json`.

The FRASER item is visibly a historical scan but contains an OCR/text layer. Therefore this attempt does **not** claim a pure image-only source-original slice. This is a material evidence gap for a production OCR lock.

## Table-role hard gate

On Petrobras table 1/page 5, the required gold assertions were:

- `Receita de vendas` × `2T26` = `169.530`
- `Lucro líquido - Acionistas Petrobras` × `2T26` = `52.445`
- `EBITDA ajustado` × `2T26` = `93.843`

PyMuPDF 1.26.7 was the only exercised path to preserve all three row/column/value relations with 1.00 recall, 1.00 precision and cell-level anchors (141 cells on the target table). Its table geometry split each logical source row across two physical extracted rows; the corrected scorer permits only a local adjacent-row span while still requiring the named header, row label, and exact value. pdfplumber emitted 125 cell anchors but did not preserve the required row labels in the table matrix, so it failed the non-compensatory role gate. Text-only and OCR paths did not emit cells and also failed the role gate.

This makes `pymupdf-tables` the **diagnostic** quality/latency point-Pareto member for the bounded Petrobras slice. It does not make it a production winner.

## Real ingestion-contract implication

The current `PdfExtraction` contract is flat text plus confidence/warnings/table ambiguity; `PypdfAdapter` and `PdftotextAdapter` explicitly do not claim table-role preservation. The controlled ingestion route sends scan/no-text to OCR and table-role ambiguity to review, and it never promotes ambiguous table evidence to trusted `SOURCE_READY`.

The source-original benchmark therefore exposed a concrete integration blocker: PyMuPDF can preserve the tested cell relations, but the production `PdfExtraction` contract has no cell/table provenance payload through which those relations can reach the trusted ingestion path. No candidate was wired around this fail-closed contract in this attempt.

## Operational and licensing constraints

- **pypdf:** BSD-3-Clause; pure Python and operationally simple, but this benchmark has no table-role output for the target table.
- **Poppler/pdftotext:** external system dependency; fast text-layout baseline here, but no cell-role provenance.
- **PyMuPDF:** dual AGPL/commercial licensing according to current PyMuPDF documentation; a commercial deployment must resolve license posture before any lock. It is the only exercised candidate that passed the bounded table-role hard gate.
- **pdfplumber:** MIT; Python 3.13 supported. Its own project positions it primarily for machine-generated PDFs; the tested table matrix failed the required role assertions.
- **Tesseract:** Apache-2.0 OCR engine; useful as an image text recognizer, but this run did not establish table-role structuring and lacked a pure image-only source-original selection slice.

Primary reference URLs used for license/operations review: `https://pypdf.readthedocs.io/`, `https://pymupdf.readthedocs.io/en/latest/about.html`, `https://github.com/jsvine/pdfplumber`, `https://github.com/tesseract-ocr/tesseract`.

## Hard acceptance

Observed acceptance counters for this qualification remain zero:

- accepted source missing provenance/hash: **0**
- ambiguous OCR/table role promoted trusted: **0**
- quarantined/unsupported source promoted to trusted generation: **0**

Malformed and encrypted cases were derived mechanics controls from source-original Petrobras bytes. All five exercised candidates failed to parse those controls, and the controls are explicitly excluded from parser selection evidence.

## Pareto and decision

A full production Pareto frontier is **not computable** because total compute cost is unpriced and managed candidates were not executed. The methodology forbids silently deleting a required objective. In addition, the pure image-only source-original OCR slice and the structured-ingestion adapter are missing.

Therefore the governed decision is:

`NO_PREFERENCE/PENDING_EVIDENCE`

No `production-parser-lock` change is authorized.

## Evidence required to reopen production selection

1. Implement/qualify a structured ingestion adapter that carries page/table/cell provenance through the real trust contract without bypassing review gates.
2. Add at least one genuine source-original image-only public-financial document (not merely a scan with embedded OCR text) and evaluate OCR routing on it.
3. Execute managed candidates on the same source groups under authorized credentials and record billed/compute costs, failure modes, and provenance behavior.
4. Price local runner compute sufficiently to restore the required cost objective and recompute the production Pareto frontier.
5. Re-run source-grouped uncertainty/robustness checks before any parser lock.
