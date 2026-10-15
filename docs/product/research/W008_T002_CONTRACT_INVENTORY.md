# W008-T002 — Existing contract and financial provenance inventory

**Evidence class:** source-code/contract inspection + previously accepted scoped result records. No tests or new production trials were executed by this inventory.
**Observed at task start:** STATE 0065, main `24ece9242c88f9a873c7ee45d84872b1b792e91d`; immutable task base STATE 0064 / `b8e22eca2affc0b9696087bca88603f8285c6940`. 
**Decision state:** `PENDING_EVIDENCE`; no production parser, data-engine, model, frontend, workflow or storage winner.

## 1. Verified current components, not new requirements

| Component | Source evidence | Observed implemented boundary | Limitation |
|---|---|---|---|
| Immutable file provenance | `src/suno_content/domain/models.py:24-42` (`SourceProvenance`), `src/suno_content/ingest/service.py:75-82` | `source_id/source_hash/artifact_ref`, canonical SHA-256 of source bytes | source ID/hash do not convey table row/column semantics |
| Structured domain provenance **already exists** | `src/suno_content/domain/models.py:83-181` | `ProvenanceRef` requires a resolvable span or full table tuple; `SourceSpan`, `TableCellProvenance` and `ParsedDocument` already model page, table ID, row/column, raw value, labels and source lineage | **Do not create redundant models**; bridge the real recipient-ingestion contract and trusted store to these existing types |
| Anchor and variant specification | `src/suno_content/domain/models.py:183-225` | `Anchor` has `source_trust`, materiality and nonempty provenance, `VariantSpec` binds source/prompt/schema and audience/format | no user-facing or durable claim graph relationship established by this inventory |
| Deterministic eval envelope | `src/suno_content/domain/models.py:227-281` | `Failure`, `HardGateResults`, `EvalReport`, `RepairInstruction`, model validator protects noncompensatory PASS | observed system is not yet a cross-variant proof of nine textual claims |
| Source classification | `src/suno_content/domain/enums.py` | source/content/business type categories, three audience levels and three native formats | classification schema is not itself human calibration |
| PDF parser output | `src/suno_content/ingest/adapters.py:22-35` | `PdfExtraction(text, parser_name, parser_version, page_count, confidence, warnings, table_role_ambiguity)` | **Critical transport gap**: no `spans`, `table_cells`, `row/column` or provenance objects at this ingestion boundary |
| Text-layer and fallback parsers | `src/suno_content/ingest/adapters.py:62-185` | Pypdf and pdftotext accept bytes, return flat text with explicit table-role ambiguity warnings | do not promote flat table text as trusted table facts |
| Ingest recipient contract | `src/suno_content/ingest/service.py:29-46, 84-99, 156-181` | `IngestResult` records source hash, parser, confidence, status and flat `extracted_text`; `_source_ready` blocks ambiguous table roles | no structured fragment/cell payload carried in `IngestResult`; `_ready_cells` produces `MECHANICS_ONLY` previews, not real production outputs |
| Controlled upload/quarantine | `src/suno_content/ingest/controlled_upload.py:13-53, 96-241` | size/signature/content preflight, `source_group_id`, SHA-256, quarantine/OCR/review routing and canonical trust promotion | reference/local path; cannot be interpreted as tested cloud object store and production-scale ingestion |
| Generic production contract | `docs/production/contracts/v1/core-contracts.schema.json` | `SourceProvenanceRef`, `ParsedNode`, `ParsedDocument`, tenant/identity, event/replay/CAS/telemetry schema definitions | generic ParsedNode.data lacks normative financial cell/row/column/qualifier role semantics; `ResourceType` has no dedicated `financial_claim` enumerant |
| Authenticated live cockpit | `src/suno_content/cockpit/live.py:51-70, 111-253, 261-345` | `AuthorizedScope`, secure projection/reconnect, two renderer-shell candidates and durable event requirements | not evidence of claim selection and financial line-level source explorer implemented |
| Ingest regression coverage | `tests/ingest/test_controlled_upload.py:27-95` | quarantine, source-group hash, OCR/review role ambiguity, trusted promotion tests | no production adapter test carrying native `TableCellProvenance` through real ingestion |
| Live cockpit security coverage | `tests/cockpit/test_live_cockpit.py:106-260` | equal projection candidates, reconnect, cross-tenant sources/events/traces and stale event tests | no editorial review/approval or claim-level navigation test observed here |

## 2. Evidence from accepted waves

- `SYSTEM/RESULTS/W006-T001-A02.md`: portable identity/source/event/command contracts and DR registry, **not** a production database or vendor decision.
- `SYSTEM/RESULTS/W006-T003-A01.md`: 14/14 reference failure-harness cases and CAS/outbox/replay contract; no multi-replica deployed proof.
- `SYSTEM/RESULTS/W006-T004-A01.md`: controlled upload/quarantine and derived-variant parser bakeoff, explicit NO_PRODUCTION_PARSER_WINNER.
- `SYSTEM/RESULTS/W006-T006-A01.md`: two reference frontend shells, live snapshot/replay/security tests; no concrete frontend winner.
- `SYSTEM/RESULTS/W006-T010-A01.md`: partition/human calibration schema and executable foundation; 0 actual human streams and no held-out human replication.
- `SYSTEM/RESULTS/W007-T004-A01.md`: source-original tests with pypdf, pdftotext, PyMuPDF tables, pdfplumber and Tesseract; PyMuPDF alone passes one bounded Petrobras table-role gate, only DIAGNOSTIC. Data transport into production `PdfExtraction` is a blocker; managed document-AI, pure-image-only original and total costs remain missing.
- `SYSTEM/STATE.md` STATE 0065: W007-T002 (deployed cloud) and T005 (human gold) remain blocked; none of these reference capabilities are FULL PRODUCTION PASS.

## 3. Exact gap and design consequence

**The gap is not an absent table-provenance domain model.** `TableCellProvenance` and `ProvenanceRef` already exist with strict invariants. It is the disconnect between flat `PdfExtraction` / flat `IngestResult` and these structured classes, plus the absence of a durable, tenant-bound financial-claim relation across accepted outputs.

A compatible additive evolution should consider:

1. `PdfExtraction` adding an optional structured `parsed_document`/spans/cells result with explicit `role_provenance_state` (trusted/ambiguous/absent) and parser/version/byte-hash binding. Default missing structured roles must **not** imply trusted table evidence.
2. `IngestResult` carrying validated `ParsedDocument` reference/fragment list through the *same* source trust decision; no direct `SOURCE_READY` promotion for unresolved table roles. Retain flat `extracted_text` only for existing compatible text-only uses.
3. Define additive `FinancialClaim`, `ClaimEvidenceLink`, `ClaimRelation`, and `OutputClaimLink` (naming tentative) with immutable tenant/source-version/provenance identity, claim modality (realized/projected/attributed/conditioned), numeric original surface, unit and period. Do not collapse a financial **assertion** to a single numeric match.
4. Persist graph revisions as authorized resources and append-only review/eval events; preserve accepted CAS/outbox semantics, idempotent attempts, cross-tenant rejection and retention/redaction.
5. Integrate claim-level source/repair findings into the already authorized live cockpit view model; **never** render raw secrets or foreign-tenant source text.

These are candidate contracts only. Before any production schema lock, apply `SYSTEM/DECISION_RESEARCH_GATE.md` to at least: extend current domain models, introduce a narrowly versioned financial claims package, and create a generic facts/relations substrate; compare migration complexity, provenance correctness, cost, isolation and reversibility.

## 4. Minimal additive test vector package (proposed; NOT YET RUN)

| Test | Required observation |
|---|---|
| Table roles / Petrobras 2T26 | row label + column period + value + units/qualifier tied to original source hash, page, table and cell; reject role permutation |
| Note / footnote | amount is not trusted without applicable note and period/denominator |
| Copom modality | statement of expectation must not become confirmed realized fact |
| Source republish | old and new document versions not silently merged |
| OCR ambiguity | ambiguous cell/row roles route REVIEW_REQUIRED; zero accepted trusted ambiguous claims |
| Claim to output | nine distinct outputs share canonical support references; missing/contradictory claims detected |
| Cross tenant | cross-org/workspace claim/cell/source lookup and exports all fail closed |
| Stale edit | concurrent revision CAS rejects stale editor/repair overwrite |
| Retry and idempotency | no duplicate accepted claim/output record on repeated attempts |
| Recovery | outbox replay and backup/restore preserve source-claim-output-evaluation lineage |
| Backwards compatibility | text-only, 9/9, evaluator, repair, export/cockpit and all historical tests keep passing |
| Privacy/cost | no raw private document leak via telemetry, pricing/compute/retrieval costs observed not invented |

## 5. Engineering change locations (proposal only)

- `src/suno_content/ingest/adapters.py`: parser-neutral structured extraction envelope; no parser-specific defaults.
- `src/suno_content/ingest/service.py` and `controlled_upload.py`: preserve source trust while carrying new structured provenance.
- `src/suno_content/domain/models.py`: reuse `ProvenanceRef`, `TableCellProvenance`, `ParsedDocument`; consider versioned claim types rather than redeclaration.
- `docs/production/contracts/v1/`: new schema version or compatible extension with dedicated claim/resource authorization and JSON validation, subject to DRG.
- `src/suno_content/cockpit/live.py`: new *authorized* source/claim/eval projection and review states without untrusted event data.
- `tests/ingest/`, `tests/cockpit/`, `tests/runstore/`: targeted negative/positive and failure-injection regression suites before acceptance.

## 6. Inspection limitations and uncertainty

This inventory read specific files via GitHub connector, not a full cloned repository or exhaustive symbol index. The GitHub code-search connector returned no hits for several known symbols; its lack of results is **not** evidence that a symbol does not exist. An attempted direct fetch of `src/suno_content/generation/contracts.py` returned NOT_FOUND, even though `ingest/service.py` imports the package; therefore the exact physical implementation of `build_3x3_variant_specs` was not independently verified here. The accepted W004/W006 evidence remains the stronger proof for the bounded 3×3 workflow.

No fresh CI, benchmark, human annotation or deployed runtime execution occurred during this research-only inventory. Assertions of production speed/quality/availability remain `NOT_OBSERVED`.

## 7. Next required experiment and decision gates

1. EP-03 freezes representative source groups, metrics and deliberately corrupted financial table/footnote variants.
2. EP-06 evaluates schema alternatives and migration/reversal design through DRG.
3. EP-07 implements adapter spike behind a compatibility flag, using real W007-T004 source-original table-role samples and a distinct image-only source if available.
4. EP-08 implements ledger/tenant-aware API only after EP-07 data passes source trust.
5. EP-10 tests cross-output claims against the same source and validates targeted repair.
6. EP-12 extends editorial UX only through the authorized live product path after W007 authz dependencies qualify.
7. Preserve W007-T002/T005 external blockers; prohibit production claims until deployed and human evidence exists.

**Decision:** `PENDING_EVIDENCE` — adopt *no new production schema or parser default* based on inventory alone.
