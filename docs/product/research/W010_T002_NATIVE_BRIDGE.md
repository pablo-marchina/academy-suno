# W010-T002 — Native article/carousel/video claim-reference bridge

**Task:** W010-T002-A01  
**Evidence:** CODE_AND_SYNTHETIC_NATIVE_FORMAT_TESTS  
**Implementation:** `src/suno_content/consistency/native_bridge.py`  
**Governed scope:** D-0023, new security/auth development deferred; existing financial/source/tenant critical gates preserved.

## Actual functionality

M05 T001 already checks a provided structured financial fact catalog against nine `FinancialAssertion` records, with source hashes and non-compensatory gates. This increment introduces `NativeVariant` and `evaluate_native_outputs`: a typed, offline bridge from **actual native format output models** and the canonical 3×3 `VariantSpec` to the existing engine. The bridge reads:

- `ArticleOutput.sections[].paragraphs[].text/source_refs`; article top-level `source_refs` are **metadata only**, not an assertion anchored in a particular text unit.
- `CarouselOutput.slides[].headline/body/source_refs` (canonical bound text `headline + "\n" + body`).
- `ShortVideoOutput.segments[].narration/on_screen_text/source_refs` (canonical bound text `narration + "\n" + on_screen_text` when present).

Each native content unit may carry `SourceRef.claim_id` and `SourceRef.provenance`. The bridge only matches it to a **separately supplied** typed `FinancialAssertion` for that claim ID, whose exact `rendered_text` must be identical to the native unit representation and whose reference set must match the native source references. `VariantSpec` source identity/hash, format, audience and job ID remain authoritative. `FinancialFact` and `FinancialAssertion` are not inferred or certified by the bridge.

The engine itself still checks structured values, units, periods, direction, modality (ACTUAL/FORECAST/CONDITIONAL) and conditional qualifiers, and respects every upstream factual/policy/source/schema/provenance gate. The bridge merges native uncertainty conservatively: `FAIL` dominates `REVIEW_REQUIRED`, which dominates `PASS`.

## Fail-closed handling

- A native unit `claim_id` not found in the provided source fact catalog, duplicate job ID, duplicated audience/format pair, wrong native output format or source hash mismatch **rejects** the entire input.
- An article root-only citation with `claim_id` does **not** count as evidence attached to a paragraph, so it triggers `ARTICLE_METADATA_ONLY_CLAIM`/REVIEW.
- An actual unit source ref with claim ID but no supplied typed financial assertion -> `NATIVE_ANCHOR_WITHOUT_TYPED_ASSERTION`/REVIEW.
- A supplied typed claim with no matching paragraph/slide/segment ref -> `TYPED_ASSERTION_NOT_ANCHORED_IN_NATIVE_UNIT`/REVIEW.
- A different span/table locator between the native ref and typed assertion -> `NATIVE_TYPED_ASSERTION_PROVENANCE_MISMATCH`/REVIEW.
- A typed assertion with `rendered_text` not identical to any bound unit text -> `TYPED_ASSERTION_TEXT_NOT_BOUND_TO_NATIVE_UNIT`/REVIEW.
- The same claim ID repeated in multiple distinct text units is `MULTIPLE_NATIVE_UNITS_REQUIRE_PER_UNIT_REVIEW`: this bounded bridge cannot attest that the entire repeated prose has been checked.
- Missing a native 3×3 branch is still `REVIEW_REQUIRED`, via T001; a critical inconsistent structured number remains `FAIL`, regardless of a bridge PASS.
- Generic references with no `claim_id` are not falsely classified as financial claim anchors. This DOES NOT mean the uncited/untagged prose has been checked; source coverage of all native text is **NOT PROVEN**.

Source original bytes and canonical `ProvenanceRef` locators remain caller-supplied, not provider-attested. Matching a native `claim_id` to a synthetic structured fact is **not** proof that the PDF actually supports it. Printed percent values embedded in natural-language output are not independently parsed; a malicious or incomplete `FinancialAssertion` could still omit an incorrect figure. Accordingly, **a PASS is only a bounded consistency contract check**, not a real source-grounded semantic 9/9 pass.

## Tests and execution

```bash
python -m pip install 'pydantic==2.13.4'
PYTHONPATH=src python -m unittest discover -s tests/consistency -p 'test_*.py' -v
```

Sixteen new native-bridge synthetic test methods exercise all nine canonical `VariantSpec` identities, real `parse_format_output` native Pydantic/dataclass contracts, source attestation identity, per-unit binding, missing annotations, metadata-only citations, claim ID mismatch, wrong span/source hash, typed text mismatch, multi-unit claim repetition, native format mismatch, incomplete branches, structured numeric contradictions and upstream gate precedence. The previously integrated fifteen M05 tests remain in the same CI group. The GitHub `W010 Cross-output Consistency` workflow runs all native and structured tests; no provider model or billed infrastructure used.

## Next governed steps

1. Build explicit **source-original claim ledger** from controlled financial PDF and typed table-cell preservation (W008-T002 gap), then populate facts from verified original bytes and independently audited associations.
2. Implement bounded extraction/annotation for claim-bearing text units (including lead/closing and visual/audio overlays) and compare typed figures against actual prose with false-positive/negative measurements. Unit-bound evidence is a prerequisite, not a complete NLP verifier.
3. Run the preregistered W008-T003 four-method benchmark on real source-grouped nine outputs with verifiable raw observations, variance and missingness before promoting M05.
4. Keep Render Free read-only staging and isolated Neon Free database unchanged; no public anonymous document uploads, no security bypass and no paid plans under D-0023.

**Promotion decision:** `PENDING_EVIDENCE`, `human_gold_eligible=false`, `production_ready=false`. No source-original actual nine generated outputs and no model judge were executed.
