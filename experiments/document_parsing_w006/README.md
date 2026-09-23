# W006-T004 financial document parser/OCR bakeoff

This package records the task-local bakeoff and its evidence boundary.

## Reproduce

```bash
python experiments/document_parsing_w006/benchmark.py --out artifacts/document_parsing_w006
```

The harness uses two independent **source groups** derived from first-party public financial sources: Banco Central do Brasil Copom 277 and Petrobras 2T26. For each source group it builds a deterministic table-bearing digital reconstruction and derives scanned, encrypted, and malformed variants. Variants retain distinct SHA-256 hashes but **do not increase source-group N**.

Committed evidence:

- `corpus_manifest.json` — source-group identity, public-source provenance, category coverage, and the source-original-byte limitation;
- `raw_observations.json` — raw per-candidate latency, text/role preservation, hash, route, cost-observation fields, and failures/routes;
- `decision.json` — hard-gate eligibility, uncertainty, Pareto result, deterministic operational policy, and recheck triggers;
- `benchmark.py` — reproducible local harness.

## Evidence boundary

The worker runtime could verify the public source locations but could not obtain source-original PDF bytes for candidate execution. Therefore the committed benchmark runs deterministic **semantic reconstructions** seeded from those public sources; their hashes are not represented as hashes of the original public PDFs. No source-original parser-quality claim is accepted, and no production parser is locked.

This preserves the hard rule from `dr://DR-0014`: text/number presence is not proof of table semantics. In the observed run, pypdf and pdftotext retained digital text but zero structured role pairs; pdfplumber recovered all role pairs on both digital reconstructions; PyMuPDF recovered all Petrobras role pairs and 75% of BCB role pairs; all local non-OCR parsers recovered zero text/roles from scans; Tesseract OCR recovered only partial text and zero structured role pairs from scans. Because no candidate clears the complete hard gate, the eligible/Pareto set is empty.

## Controlled upload/quarantine path

`src/suno_content/ingest/controlled_upload.py` wraps canonical ingest with a fail-closed preflight and deterministic routing:

- invalid signature, size limit, encryption, active/embedded content, malformed tail → `QUARANTINED`;
- no trusted text layer → `OCR_REQUIRED`;
- table-role ambiguity, warnings, or confidence below gate → `REVIEW_REQUIRED`;
- only an extraction that also passes the existing canonical source gate → `SOURCE_READY`.

Every upload/variant carries `sha256:<hash>` provenance and a `source_group_id`. A source-group key can intentionally bind derived variants of one public source without collapsing their immutable byte hashes.

## Cost and latency interpretation

The observed candidates are local, so external service cost is recorded as `0.0 USD` for the run. Compute, license, and operational costs were **not measured** and are not inferred. Latency is a diagnostic observation from one worker host, not an SLO or production comparison. Managed document-AI candidates remain unexecuted and therefore cannot be ranked.
