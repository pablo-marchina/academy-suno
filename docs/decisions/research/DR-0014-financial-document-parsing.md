# DR-0014 — Financial document parsing / document intelligence

- **Status:** `PENDING_EVIDENCE` — architecture constraints narrowed; **no production parser winner**
- **Task:** `W005-T014-A01`
- **Research date:** 2026-09-22
- **Decision owner:** Orchestrator after fan-in
- **DRG:** `SYSTEM/DECISION_RESEARCH_GATE.md`
- **Production trace:** `PROD-004`, `PROD-005`, `PROD-007`, `PROD-015`
- **Risk trace:** `RISK-0001`, `RISK-0010`, `RISK-0032`, `RISK-0034`

## 1. Decision question

What production ingestion/parsing/extraction stack should Academy Suno use for public financial PDFs and text so that page/section/table roles, rows/columns, units, numbers, dates, entities and provenance anchors remain auditable, while scanned/OCR, complex tables, malformed/large PDFs, security, latency, cost and operational failure modes are handled without silently promoting corrupted evidence?

The W004 baseline (`pypdf` then `pdftotext`) is the baseline, not an incumbent winner. The hard invariant is fail-closed source trust: **text or number presence is never sufficient evidence of table semantics**.

## 2. Workload / constraints

Academy Suno needs a single recipient-facing product path in which document evidence can be traced back to a source hash and page-level/structural anchor. Existing grounding resolves either a text span or `(table_id, row_index, column_index)` and rejects lineage mismatches. Existing ingest marks table-looking flat text as ambiguous and blocks generation rather than guessing table roles.

Relevant workload properties:

- Portuguese financial/economic PDFs, frequently table-heavy and number-dense;
- repeated values across periods, making role swaps possible even with 100% numeric presence;
- digitally born PDFs, image-only scans, OCR-backed scans and mixed pages;
- merged/multi-level headers, footnotes, units and period labels that carry semantic meaning;
- bounded untrusted uploads (current product limit 25 MiB) plus future long/large public documents;
- production need for deterministic source lineage and explicit uncertainty;
- no cloud vendor can be selected without measured quality/latency/cost on the same corpus;
- parser execution on untrusted PDFs must be sandboxed/resource-bounded;
- license and data-residency implications are material production constraints.

## 3. Alternatives

### A. W004 baseline: `pypdf` + Poppler `pdftotext -layout`

Strengths: mature text-layer extraction, local execution, low latency, simple operational fallback. Current code already preserves page labels and deliberately refuses to claim table-cell semantics.

Limitation: PDF itself lacks a semantic layer; pypdf documents that tables are often absolutely positioned text and that it is not OCR. `pdftotext -layout` preserves spacing but does not create canonical cell roles/provenance.

### B. Local geometric/table heuristics: PyMuPDF `find_tables()` / word bboxes

Strengths: local; words/blocks expose bounding boxes and PyMuPDF has table extraction. The diagnostic fixture recovered both role-sensitive tables structurally.

Material constraint: PyMuPDF/MuPDF is dual AGPL/commercial; proprietary deployment requires legal/license resolution. Heuristics still need real-corpus validation and an OCR route.

### C. Local geometric/table heuristics: pdfplumber

Strengths: MIT; exposes characters/lines/rectangles and table extraction; the diagnostic fixture recovered both role-sensitive tables structurally.

Material constraint: its own documentation emphasizes machine-generated PDFs; scanned PDFs need a separate OCR stage. Heuristic tables still need real-corpus validation.

### D. Local ML document intelligence: Docling

Strengths: MIT codebase; `DoclingDocument` represents text, tables, pictures, hierarchy, header/footer disambiguation, bounding boxes and provenance. Its technical report describes dedicated layout and TableFormer table-structure models; full-page OCR is supported by documented conversion options.

Material constraint: heavier model/runtime footprint and model licenses must be checked individually. It was not installed/executed in this worker environment, so quality/latency are unmeasured here.

### E. Managed document AI: Amazon Textract

Strengths: TABLES/LAYOUT features; response blocks include page, geometry, row/column indices/spans and cell entity types including column headers, titles, section titles, footers and summaries. Supports PDF/TIFF/images and managed OCR.

Material constraints: per-page cloud cost, network/service dependency, cloud data handling, regional configuration and vendor lock-in. AWS A2I human-loop integration entered maintenance mode in July 2026 and is unavailable to new customers, so it cannot be assumed as the review path.

### F. Managed document AI: Azure Document Intelligence Layout

Strengths: page/word/paragraph spans and polygons, logical paragraph roles, table rows/columns/cells and Markdown output using HTML tables to retain merged-cell `rowspan`/`colspan`, captions and footnotes.

Material constraints: cloud data handling, service dependency and region-dependent pricing. The public pricing page exposed the 0–500 pages/month free tier to the research crawler but did not expose stable S0 numeric prices; no cost number is inferred.

### G. Managed document AI: Google Document AI Gemini Layout Parser

Strengths: detects figure/paragraph/table/title/heading/header/footer and provides context-aware layout parsing. Managed OCR is available as a separate processor.

Material constraints: online limit is 20 MB / 15 PDF pages; batch raises that to 1 GB / 500 pages. Google explicitly notes that tables spanning multiple pages may be split. Cloud data handling, service dependency and per-page cost apply.

## 4. Evaluation criteria

Hard gates are non-compensatory.

| Criterion | Measurement | Gate posture |
|---|---|---|
| Source lineage | every promoted span/cell resolves to source hash + page + stable structural anchor | hard PASS required |
| Table role preservation | row/column/header/merged-cell topology; GriTS topology/content/location where ground truth exists | hard PASS for table-derived claims |
| Silent corruption detection | repository `earnings_metric_role_swap` and `table_role_drop` plus expanded mutations | zero silent promotion |
| Numeric/unit/date/entity preservation | exact normalized values with semantic role, not bag-of-values presence | hard for critical claims |
| OCR/scanned behavior | OCR recall/error + structure recovery + uncertainty/failure detection | ambiguous => REVIEW_REQUIRED |
| Reading order / sections | section hierarchy, header/footer discrimination, page anchors | measured |
| Robustness | malformed, encrypted, rotated, huge content streams, timeouts, decompression/memory pressure | bounded failure required |
| Security | sandbox, resource limits, no trust in embedded active content/paths, dependency scanning | hard production control |
| Latency | p50/p95 by page count/type under same hardware/network | measured, no invented threshold |
| Cost | infra + license or managed per-page cost at representative volume | measured before lock |
| Operational burden | model downloads, GPU/CPU needs, retries, observability, regional service dependencies | documented |
| Lock-in / portability | ability to normalize outputs into canonical `ParsedDocument` and replay corpus | lower is preferable but not a hard gate |

No aggregate weighted score is used; structural/provenance hard gates cannot be offset by latency or cost.

## 5. Systematic source search

Research date: **2026-09-22**.

Search categories/queries covered:

1. current official parser docs: pypdf extraction/OCR/table limitations; PyMuPDF text positions/tables/licensing; pdfplumber table extraction/licensing;
2. local ML document intelligence: Docling unified document representation, OCR/table/layout capabilities, license and technical report;
3. managed document AI: AWS Textract AnalyzeDocument/tables/pricing; Azure Document Intelligence Layout/Markdown/pricing; Google Document AI Layout Parser/limits/pricing;
4. academic/benchmark evidence: PubTables-1M, GriTS, TableFormer, DocLayNet/Docling technical report, financial table extraction literature;
5. representative first-party public source documents: BCB Copom 277 and Petrobras 2T26 report;
6. repository baseline and adversarial fixtures: W004 ingest adapters/service, grounding provenance resolver, parser silent-corruption fixtures.

**Stopping rule / saturation:** research stopped after each material parser class had primary-source capability evidence; the current baseline plus at least two materially different local approaches and three managed approaches were covered; table-structure benchmark methodology had primary academic sources; pricing/limits were checked where exposed; and the next missing evidence was no longer another source but execution of the same real corpus through untested candidates. Additional search was producing redundant capability descriptions rather than a new architecture class or failure mode.

## 6. Source table

| Source | Type/date | Authority | Claim supported | Limitation |
|---|---|---|---|---|
| https://pypdf.readthedocs.io/en/6.18.1/user/extract-text.html | official docs, current | pypdf | PDFs have no semantic layer; tables are difficult; pypdf is not OCR; large content streams can require high memory | current docs are newer than local benchmark pypdf 5.9.0 |
| https://pymupdf.readthedocs.io/en/latest/app1.html | official docs, current | PyMuPDF | word/block extraction exposes bounding boxes and order metadata | spatial data alone does not prove financial semantics |
| https://pymupdf.readthedocs.io/en/latest/about.html | official docs, current | PyMuPDF | AGPL/commercial dual licensing | license choice still needs project legal decision |
| https://github.com/jsvine/pdfplumber | upstream project, current | pdfplumber | table extraction and visual/geometric primitives; best suited to machine-generated PDFs | no native OCR solution |
| https://docling-project.github.io/docling/concepts/docling_document/ | official docs, current | Docling | unified text/table/picture hierarchy, furniture disambiguation, bounding boxes and provenance | capability evidence, not Academy Suno benchmark |
| https://arxiv.org/abs/2408.09869 | technical report, 2024 | Docling authors | dedicated layout + table-structure models, local execution architecture | paper benchmark/domain differs from Suno corpus |
| https://github.com/docling-project/docling | upstream project, current | Docling | MIT codebase; individual model licenses may differ | runtime not executed in this attempt |
| https://docs.aws.amazon.com/textract/latest/APIReference/API_AnalyzeDocument.html | official API docs, current | AWS | TABLES/LAYOUT, page/geometry/row/column response fields; A2I maintenance-mode note | no Suno-corpus execution |
| https://docs.aws.amazon.com/textract/latest/dg/how-it-works-tables.html | official docs, current | AWS | cell indices, spans, geometry, header/title/footer/summary entity types | no Suno-corpus execution |
| https://aws.amazon.com/textract/pricing/ | official pricing, current | AWS | Tables $0.015/page first 1M and $0.010 thereafter in US West (Oregon); Layout free with Tables in example | region/feature mix changes cost |
| https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0 | official docs, v4.0 | Microsoft | pages, spans/polygons, paragraph roles and table cells | no Suno-corpus execution |
| https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept/markdown-elements?view=doc-intel-4.0.0 | official docs, v4.0 | Microsoft | HTML table output preserves rowspan/colspan, captions and footnotes | Markdown representation still needs canonical normalization |
| https://azure.microsoft.com/pt-br/pricing/details/document-intelligence/ | official pricing, current | Microsoft | free tier 0–500 pages/month; paid price is region/config dependent | crawler did not expose numeric S0 price; do not infer |
| https://docs.cloud.google.com/document-ai/docs/layout-parse-chunk | official docs, current | Google Cloud | PDF structural elements, 15-page online / 500-page batch limits; multi-page tables may split | no Suno-corpus execution |
| https://cloud.google.com/products/document-ai/pricing | official pricing, current | Google Cloud | Layout Parser listed at $10 consumption price and Enterprise OCR at $1.50/1,000 after free band in surfaced table | consumption model/unit details must be rechecked at purchase time |
| https://www.microsoft.com/en-us/research/publication/pubtables-1m/ | peer-reviewed publication, CVPR 2022 | Microsoft Research | large table detection/structure dataset with header/location annotations | scientific-domain distribution, not financial-specific |
| https://www.microsoft.com/en-us/research/?p=835363 | research publication, 2022 | Microsoft Research | GriTS evaluates table topology/location/content in matrix form | metric must be paired with domain-specific semantic checks |
| https://arxiv.org/abs/2203.01017 | research paper, 2022 | IBM Research authors | TableFormer addresses complex row/column headers and cell structure | historical benchmark, not current product version |
| https://arxiv.org/abs/2005.00589 | research paper, 2020 | IBM Research authors | FinTabNet introduced as a real-world financial table structure dataset | older dataset; useful for supplemental benchmark, not production corpus substitute |
| https://www.bcb.gov.br/content/copom/atascopom/Copom277-not20260318277.pdf | first-party public PDF, 2026 | Banco Central do Brasil | real financial/economic table ground truth for IPCA period roles | only one document |
| https://api.mziq.com/mzfilemanager/v2/d/25fdf098-34f5-4608-b7fa-17d60b2de47d/857e970b-1bf4-9ea4-093f-b93bfc2bac95?origin=2 | first-party linked report, 2026 | Petrobras RI | real performance table with 52.445 lucro líquido and 93.843 EBITDA ajustado in 2T26 | only one issuer/report |

## 7. Primary evidence first

The decision uses official product documentation and first-party public financial PDFs for capability/ground-truth claims. Academic papers are used for benchmark methodology and model-class evidence. No blog/community statement is used to promote a parser. The one project-upstream source used for pdfplumber is its maintained repository/documentation.

## 8. Security / reliability / cost / lock-in

### Security

All local parser candidates must run as untrusted-document workloads: isolated process/container, no arbitrary filesystem path from users, CPU/time/memory/file-size limits, decompression/content-stream limits, patched native dependencies, and no promotion after parser exceptions or truncation. The pypdf documentation's example of extreme memory use for large uncompressed content streams reinforces the need for preflight/resource guards.

Managed parsers reduce native parser maintenance but send document content to a vendor boundary. Region, retention, encryption, access control and contractual data-processing settings must be checked before any non-public document is allowed. Public financial documents do not remove the need for production tenant isolation/audit.

### Reliability

The system must distinguish: `TEXT_LAYER_OK`, `STRUCTURE_OK`, `OCR_REQUIRED`, `AMBIGUOUS_STRUCTURE`, `TRUNCATED/LIMIT_EXCEEDED`, and parser failure. A fallback parser cannot silently turn a failed structured parse into a trusted flat-text parse. Fallback can recover content, but trust can only increase when the required structural evidence is present.

### Cost

Local approaches incur compute plus licensing/operations. PyMuPDF has AGPL/commercial implications; pdfplumber and Docling code are MIT. Managed per-page costs must be measured at representative volume and region. AWS provides a clear Tables price example; Google exposes processor prices; Azure's public page requires configuration/region for numeric paid pricing. No cross-vendor cost winner is asserted.

### Lock-in

All candidates must normalize to the existing Academy Suno source/provenance model. Raw provider output must also be persisted for replay/audit. Provider-specific IDs are metadata, never the sole canonical provenance key. This makes candidate replacement possible without changing downstream factual grounding contracts.

## 9. Reproducible benchmark / experiment

Committed experiment package:

- `experiments/document_parsing_w005/benchmark.py`
- `experiments/document_parsing_w005/raw_observations.json`
- `experiments/document_parsing_w005/README.md`

The local diagnostic benchmark generates a digital role-sensitive financial-table fixture and an image-only scanned derivative, then runs pypdf, pdftotext, PyMuPDF table extraction, pdfplumber table extraction and Tesseract OCR under one harness.

### Required production-selection bakeoff

Before a parser default can become `LOCKED`, create a versioned public corpus that includes, at minimum, BCB Copom 277 and Petrobras 2T26 plus enough additional issuers/regulators to cover:

- simple and complex digitally born tables;
- merged/multi-level headers and units/footnotes;
- multi-page tables;
- scanned/image-only and mixed OCR documents;
- rotated pages/tables;
- malformed/truncated/encrypted files;
- large page counts and content streams;
- repeated numeric values and adversarial role swaps.

Use dual-review or deterministic source markup for gold table cells. Persist exact page/table/row/column ground truth. For table structure, report GriTS topology/content/location where applicable plus Academy-specific exact semantic-role checks. Report bootstrap confidence intervals for aggregate quality metrics and distributions (not just means) for latency/memory.

Run every candidate on identical bytes/configuration. Managed candidates must record region, API/model version and request feature set. Local candidates must record package/model versions and hardware. Repeat latency measurements after warm-up; separately report cold/model-load time where material.

## 10. Raw results + uncertainty

Observed local micro-benchmark (`w005-t014-local-0.2`):

| Variant | Candidate | Text anchor recall | Structured role-pair recall | Median latency |
|---|---|---:|---:|---:|
| digital | pypdf | 1.00 | 0.00 | 2.62 ms |
| digital | pdftotext `-layout` | 1.00 | 0.00 | 14.21 ms |
| digital | PyMuPDF `find_tables()` | 1.00 | 1.00 | 32.37 ms |
| digital | pdfplumber tables | 1.00 | 1.00 | 15.70 ms |
| digital | Tesseract text OCR | 0.85 | 0.00 | 739.72 ms |
| scanned | pypdf | 0.00 | 0.00 | 0.44 ms |
| scanned | pdftotext `-layout` | 0.00 | 0.00 | 10.41 ms |
| scanned | PyMuPDF `find_tables()` | 0.00 | 0.00 | 0.66 ms |
| scanned | pdfplumber tables | 0.00 | 0.00 | 1.41 ms |
| scanned | Tesseract text OCR | 0.55 | 0.00 | 676.78 ms |

Interpretation: the baseline reproduces the exact dangerous pattern already encoded by repository adversarial fixtures — all critical strings can survive while structured role evidence is absent. PyMuPDF and pdfplumber demonstrate that local structured extraction is feasible on the generated digital fixture. None of the tested local invocations safely recovers structured table roles from the image-only derivative; OCR text recovers only part of the content and remains structurally ungrounded.

Uncertainty is high for candidate ranking: one synthetic page, simple ruled tables, single host, no managed-service runs, no Docling run, no real-source bytes in the worker execution environment. Therefore these results are **eligibility evidence**, not production comparative evidence.

Separately, the two public source PDFs were visually/textually checked during research to establish target semantics: BCB's table maps IPCA `3,9` to 2026 and `3,3` to 3Q27; Petrobras table 1 maps `52.445` to Lucro líquido - Acionistas Petrobras and `93.843` to EBITDA ajustado for 2T26. They are required real-corpus gold seeds, not claimed parser benchmark results in this attempt.

## 11. Decision

**Decision state: `NO_PRODUCTION_PARSER_WINNER / PENDING_REAL_CORPUS_MANAGED_BAKEOFF`.**

What can be decided now:

1. **The W004 pypdf/pdftotext chain must remain a fast text-layer/fallback mechanism, not the production source-trust authority for table-bearing documents.** Its own contract already correctly blocks table-role ambiguity; preserve that behavior.
2. **Production trust must be parser-agnostic and structure-first.** A parser output is eligible for `SOURCE_READY` only after canonical normalization yields resolvable page/span or table/cell provenance and no role ambiguity.
3. **PyMuPDF and pdfplumber advance as local structured candidates** for real-corpus testing because they demonstrated structural recovery on the diagnostic digital fixture. This is not a winner claim.
4. **Docling advances as the local ML/document-intelligence candidate** based on official/technical capability evidence, pending execution on the same corpus.
5. **Textract, Azure Document Intelligence and Google Document AI advance as managed candidates** pending same-corpus execution, pricing/region normalization and data-handling review.
6. **A scanned/OCR path must be explicit.** Text-only OCR is insufficient for table trust; scanned pages must pass OCR plus structure/provenance validation or remain `REVIEW_REQUIRED`.
7. **Do not implement “first successful parser wins” as a quality policy.** Operational fallback order may exist, but trust is determined by evidence completeness, not parser success/no-exception.

A practical target architecture for the next task is a cost-aware cascade: cheap text-layer preflight -> scan/table/ambiguity classification -> structured local parser and/or managed document AI -> canonical `ParsedDocument` normalization -> invariant source-trust gate. The exact routing thresholds and provider choice remain unlocked until measured.

## 12. Confidence

- **HIGH**: flat-text extraction alone cannot satisfy Academy Suno's table provenance invariant; the current fail-closed behavior is necessary.
- **HIGH**: production parser outputs should normalize to the existing parser-independent provenance contract.
- **MEDIUM**: PyMuPDF/pdfplumber are credible local candidates for digitally born ruled tables; only diagnostic evidence exists here.
- **MEDIUM**: Docling and managed document-AI products expose the required structural primitives according to primary docs.
- **LOW**: any relative quality/cost/latency ranking across Docling/Textract/Azure/Google/PyMuPDF/pdfplumber before the real-corpus bakeoff.

Overall decision confidence: **MEDIUM** for architecture constraints, **LOW / insufficient evidence** for a product/vendor winner.

## 13. Reversal conditions

Reopen or change this decision if:

- a candidate cannot emit/normalize stable cell provenance on real financial tables;
- table-role silent corruption appears in any promoted source;
- Docling/local candidates materially outperform managed candidates at acceptable operational cost, or vice versa, on the same held-out corpus;
- licensing (notably PyMuPDF AGPL/commercial) becomes incompatible with deployment;
- managed-provider region/privacy/retention terms conflict with production requirements;
- pricing/limits change materially;
- multi-page/merged/scanned table failure rates remain unacceptable;
- a new materially different parser demonstrates superior held-out structural accuracy with equivalent auditability.

## 14. Traceability

- `SYSTEM/PRODUCTION_CONTRACT.md`: source trust/factuality/provenance fail-closed; secure document storage; hybrid eval; research-gated architecture.
- `src/suno_content/ingest/adapters.py`: W004 pypdf/pdftotext baseline and explicit table-role ambiguity warnings.
- `src/suno_content/ingest/service.py`: `SOURCE_READY` requires high confidence and no table-role ambiguity.
- `src/suno_content/grounding/provenance.py`: canonical span/table-cell provenance resolution and source-lineage enforcement.
- `tests/fixtures/parser/silent_corruption_cases.json`: `earnings_metric_role_swap` and `table_role_drop` acceptance blockers.
- `experiments/document_parsing_w005/*`: executable diagnostic benchmark and raw observations.
- `SYSTEM/RESULTS/W005-T014-A01.md`: worker result and fan-in handoff.

**Promotion gate:** keep parser/document-intelligence production selection unlocked until the representative real-corpus bakeoff executes all surviving candidate classes under identical gold semantics and the Orchestrator accepts the evidence.
