# W005-T014 — document parsing bakeoff

This directory is the reproducible measurement package for `W005-T014-A01`.
It tests the failure mode that matters most to Academy Suno: **numbers can be present while their financial role is wrong or unprovable**.

## Scope

The local micro-benchmark generates two role-sensitive tables based on the semantics of public financial sources already represented by repository corruption fixtures:

- Banco Central do Brasil, Copom 277: columns `Índice de preços | 2026 | 3º tri 2027` with IPCA rows including `3,9` and `3,3`.
- Petrobras 2T26: `Lucro líquido - Acionistas Petrobras = 52.445` and `EBITDA ajustado = 93.843` in the 2T26 column.

The generated PDF is **synthetic diagnostic data, not source evidence**. A rasterized image-only derivative exercises the scanned-document path. The public PDFs remain the required real-corpus bakeoff targets:

- BCB Copom 277: https://www.bcb.gov.br/content/copom/atascopom/Copom277-not20260318277.pdf
- Petrobras 2T26 performance report: https://api.mziq.com/mzfilemanager/v2/d/25fdf098-34f5-4608-b7fa-17d60b2de47d/857e970b-1bf4-9ea4-093f-b93bfc2bac95?origin=2

## Run

Install the diagnostic dependencies in an isolated environment and run:

```bash
python experiments/document_parsing_w005/benchmark.py --out artifacts/document_parsing_w005
```

Observed worker environment for the committed raw result: Python 3.13.5, pypdf 5.9.0, PyMuPDF 1.26.7, pdfplumber 0.11.9, pytesseract 0.3.13, ReportLab 4.4.9, Pillow 12.3.0, Poppler `pdftotext` 25.06.0, Tesseract 5.5.0.

## Metrics

`anchor_recall` measures only whether role-sensitive strings/numbers survived extraction. It is intentionally insufficient for a PASS.

`role_pair_recall_structured` requires a parser to return structured table rows in which a metric label and its value remain in the same extracted row. Text-only output receives no structural credit even when strings appear adjacent. This directly guards the repository's `earnings_metric_role_swap` and `table_role_drop` silent-corruption cases.

The production bakeoff must add cell topology metrics such as GriTS, exact numeric/entity/date preservation, page/table/cell provenance resolvability, OCR word/character error where applicable, malformed-input rejection, p50/p95 latency, peak memory, and current per-page cost.

## Raw observation summary

| Variant | Candidate | Anchor recall | Structured role-pair recall | Median latency, 1-page fixture | Interpretation |
|---|---|---:|---:|---:|---|
| digital | pypdf text | 1.00 | 0.00 | 2.62 ms | content present; table roles unproven |
| digital | pdftotext `-layout` | 1.00 | 0.00 | 14.21 ms | visual spacing is not cell provenance |
| digital | PyMuPDF `find_tables()` | 1.00 | 1.00 | 32.37 ms | structured local candidate on this fixture |
| digital | pdfplumber tables | 1.00 | 1.00 | 15.70 ms | structured local candidate on this fixture |
| digital | Tesseract text OCR | 0.85 | 0.00 | 739.72 ms | OCR text alone cannot establish roles |
| scanned | pypdf text | 0.00 | 0.00 | 0.44 ms | correctly demonstrates no text layer |
| scanned | pdftotext `-layout` | 0.00 | 0.00 | 10.41 ms | no OCR path |
| scanned | PyMuPDF `find_tables()` | 0.00 | 0.00 | 0.66 ms | no OCR in this invocation |
| scanned | pdfplumber tables | 0.00 | 0.00 | 1.41 ms | no OCR path |
| scanned | Tesseract text OCR | 0.55 | 0.00 | 676.78 ms | partial OCR, still no safe table semantics |

The exact raw records are in `raw_observations.json`. These timings are diagnostic only: one synthetic page, one machine, no warm/cold separation, and no managed-service network latency.

## Required real-corpus matrix before any production parser lock

Run the same normalized parser contract on a versioned public corpus with at least these strata: digitally born simple tables; multi-level headers/merged cells; multi-page tables; dense financial statements; scanned/image-only pages; mixed text+image/OCR; malformed/corrupt PDFs; very large pages/files; rotated tables; and documents containing repeated numbers that make role swaps hard to detect by value presence alone.

For every candidate, persist raw parser output plus normalized `ParsedDocument`. A candidate can pass source trust only when every promoted claim can resolve to `(source_hash, page, span_id)` or `(source_hash, page, table_id, row_index, column_index)` and table-role ambiguity is false. Any missing/ambiguous role remains `REVIEW_REQUIRED` regardless of text recall.

Managed candidates (Textract, Azure Document Intelligence, Google Document AI) were documentation-researched in this attempt but not executed because no cloud credentials/billing context were available to the worker. Docling was not installed in the worker runtime. Those are explicit evidence gaps, not inferred failures.
