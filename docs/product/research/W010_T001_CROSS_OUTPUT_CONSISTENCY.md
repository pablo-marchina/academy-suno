# W010-T001 — Financial claim consistency across nine editorial outputs

**Evidence class:** `STRUCTURED_ASSERTION_DIAGNOSTIC_ONLY`  
**Feature:** M05 reference implementation, no production semantic-comprehension claim  
**Operator scope:** D-0023 prioritizes financial content work; new authentication/security implementation remains deferred, while existing gates stay hard.

## Implemented

`suno_content.consistency` introduces an additive typed contract:

- `FinancialFact`: **caller-supplied** canonical source fact identified by stable `fact_id`, exact Decimal value, unit, period, modality (ACTUAL/FORECAST/CONDITIONAL), conditional phrase, direction, materiality, source trust and resolvable canonical `ProvenanceRef` (span or complete table cell).
- `FinancialAssertion`: what one structured article/carousel/video variant states about that fact; links back to the **same** source hash, period, unit, modality, direction and provenance.
- `VariantAssertions`: canonical `AudienceLevel` and `OutputFormat`, job ID, five mandatory source/factual/policy/schema/provenance gate statuses, zero or more exact fact assertions.
- `ConsistencyBundle`: run and `SourceProvenance` with source ledger version, fact catalog and variants. All source references must carry the same source identity/hash; duplicates/unknown facts are refused.
- `evaluate_consistency`: deterministic report containing PASS/FAIL/REVIEW_REQUIRED, nine-branch presence, source mismatches, per-claim contradictions, targeted repair suggestions, explicit missingness and evidence limits.

**Noncompensatory precedence**: any FAIL among upstream gates or critical source fact/assertion contradictions yields FAIL, any unresolved source/required omission/provenance ambiguity yields at least REVIEW_REQUIRED; no score/LLM can override. Critical/material claim mismatch is a FAIL; nonmaterial discrepancy yields REVIEW. Missing any of the nine branch slots is REVIEW. Missing optional facts in the video/carousel is allowed, because shorter formats legitimately omit detail. Missing **required_for_all** fact yields REVIEW.

**Normalizing semantics**: exact decimal `15.00 == 15` is harmless, while changing numeric magnitude, units, source period, ACTUAL→FORECAST, polarity/direction or named condition flags inconsistency. `rendered_text` is informative; this version cannot read arbitrary text to extract verified claims. Different Portuguese expressions are not considered contradictions solely due to wording differences. Cross-output contradiction is reported when structured fact values differ among observed variants. The targeted repair list names the **affected job**, never modifies or regenerates other siblings; downstream must refresh gates for each repair.

## What is **not** implemented or proved

The fact catalog and per-format assertions are **supplied inputs**; their extraction and attestation from an original trusted Petrobras/BCB/CVM document is **not executed**. A complete all-PASS synthetic bundle is a contract smoke, **not proof of financial factuality** from real source documents. The flat production `PdfExtraction` path still lacks structured table cell transport (W008-T002), and current Render Free service is intentionally **read-only staging**. No public generator/API, unsafe filesystem-path ingestion, Neon database migration, auth bypass, model judge or real run of nine generated outputs.

PROD-008 human thresholds stay `DIAGNOSTIC_ONLY`; `human_gold_eligible=false`, `production_ready=false`. Do not promote M05 to complete production flow without source original + actual nine output claims, full format extraction, provenance cell/row/column, cross-output ground truth, accepted DRG and end-to-end tests.

## Reproduce

```bash
python -m pip install --disable-pip-version-check 'pydantic==2.13.4'
PYTHONPATH=src python -m unittest discover -s tests/consistency -p 'test_*.py' -v
```

Tests cover 9 branches, numeric contradictions and repair targeting, units/time/modality/direction/conditions, optional omission, required omission, missing branch, trust/negative upstream policy, source-ref tampering, duplicate branch/unknown claim, invalid non-finite/float inputs and nonmaterial review. Code uses the existing `ProvenanceRef`, `SourceProvenance`, `AudienceLevel`, `OutputFormat`, `Materiality`, and `GateStatus` without reimplementing them.

## Next implementation

Integrate claim-assertion extraction with native `ArticleOutput`, `CarouselOutput`, `ShortVideoOutput`, backed by original source-verified `AtomicClaim`/provenance ledger; add table-cell transport W008-T002 and actual source-group original benchmark W008-T003. Run seeded nine-output controls where all formats share the same fact ID, and independently measure false contradictions and misses. Preserve D-0023 and all W007 blockers. Never claim audience comprehension or human gold from AI-only evaluations.

**Scope of conclusion:** bounded, synthetic-testable deterministic reference feature; production quality `PENDING_EVIDENCE`.
