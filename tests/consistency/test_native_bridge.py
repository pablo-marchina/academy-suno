from __future__ import annotations

import unittest
from dataclasses import replace

from suno_content.consistency import (
    FinancialAssertion,
    FinancialFact,
    NativeEvidenceError,
    NativeVariant,
    evaluate_native_outputs,
)
from suno_content.domain import (
    AudienceLevel,
    GateStatus,
    Materiality,
    OutputFormat,
    ProvenanceRef,
    SourceProvenance,
)
from suno_content.formats import parse_format_output
from suno_content.generation.contracts import build_3x3_variant_specs

HASH = "c" * 64
SOURCE = SourceProvenance(source_id="source-fixture", source_hash=HASH, artifact_ref="synthetic/source.pdf")
REF = ProvenanceRef(source_id=SOURCE.source_id, source_hash=HASH, page_number=2, span_id="span-interest-1")
CLAIM = "copom-rate"
TEXT = "O Copom manteve os juros em 15% ao ano."
GATES = {key: GateStatus.PASS for key in ("source", "factual", "policy", "schema", "provenance")}


def claim_ref(*, claim: str = CLAIM, source_hash: str = HASH, span: str = "span-interest-1") -> dict:
    return {
        "anchor_id": "anchor-rate",
        "claim_id": claim,
        "provenance": {
            "source_id": SOURCE.source_id,
            "source_hash": source_hash,
            "page_number": 2,
            "span_id": span,
        },
    }


def native_payload(fmt: OutputFormat) -> tuple[dict, str]:
    if fmt is OutputFormat.ARTICLE:
        return {
            "format": "ARTICLE", "title": "Juros e contexto",
            "lead_or_summary": "Uma leitura do comunicado.",
            "sections": [{"heading": "Decisao", "paragraphs": [
                {"text": TEXT, "source_refs": [claim_ref()]}
            ]}],
            "closing_or_takeaways": "Contexto e ressalvas importam.",
            "source_refs": [claim_ref()],
        }, TEXT
    if fmt is OutputFormat.CAROUSEL:
        return {
            "format": "CAROUSEL", "slides": [
                {"slide_index": 1, "role": "HOOK", "headline": "O que mudou?", "body": "Juros e politica monetaria",
                 "visual_cue": None, "source_refs": []},
                {"slide_index": 2, "role": "BODY", "headline": "Decisao do Copom", "body": TEXT,
                 "visual_cue": None, "source_refs": [claim_ref()]},
                {"slide_index": 3, "role": "CONCLUSION", "headline": "Contexto", "body": "Leia as ressalvas",
                 "visual_cue": None, "source_refs": []},
            ],
        }, f"Decisao do Copom\n{TEXT}"
    return {
        "format": "SHORT_VIDEO", "segments": [
            {"start_s": 0, "end_s": 5, "role": "HOOK", "narration": "Uma decisao de juros.",
             "on_screen_text": None, "visual_cue": "Grafico", "source_refs": []},
            {"start_s": 5, "end_s": 30, "role": "BODY", "narration": TEXT,
             "on_screen_text": "Taxa: 15%", "visual_cue": "Taxa e fonte", "source_refs": [claim_ref()]},
            {"start_s": 30, "end_s": 40, "role": "CONCLUSION", "narration": "Veja a origem.",
             "on_screen_text": None, "visual_cue": "Fonte", "source_refs": []},
        ], "estimated_spoken_duration_s": 40,
    }, f"{TEXT}\nTaxa: 15%"


def build(*, patch=None):
    fact = FinancialFact(
        fact_id=CLAIM, value="15.0", unit="PERCENT_PER_YEAR", period="2026-10",
        modality="ACTUAL", direction="UNCHANGED", materiality=Materiality.CRITICAL,
        required_for_all=True, provenance=(REF,), source_gate=GateStatus.PASS,
    )
    specs = build_3x3_variant_specs(
        source=SOURCE, source_backbone_ref="backbone-fixture",
        policy_context_ref="policy-fixture", prompt_version="prompt-fixture-v1",
        output_schema_version="native-format-v1",
    )
    variants = []
    for spec in specs:
        payload, rendered_text = native_payload(spec.format)
        assertion_data = {
            "fact_id": CLAIM, "value": "15", "unit": "PERCENT_PER_YEAR", "period": "2026-10",
            "modality": "ACTUAL", "direction": "UNCHANGED",
            "provenance": (REF,), "rendered_text": rendered_text,
        }
        gates = dict(GATES)
        if patch is not None:
            patch(spec, payload, assertion_data, gates)
        assertion = FinancialAssertion.model_validate(assertion_data) if assertion_data else None
        variants.append(NativeVariant(
            spec=spec, output=parse_format_output(payload),
            assertions=() if assertion is None else (assertion,), upstream_gates=gates,
        ))
    return (fact,), tuple(variants)


def run(*, patch=None, change_output=None, facts=None):
    source_facts, entries = build(patch=patch)
    if change_output:
        entries = change_output(entries)
    return evaluate_native_outputs(
        run_id="synthetic-bridge-v1", source=SOURCE,
        source_ledger_version="synthetic-fact-ledger-v1",
        facts=source_facts if facts is None else facts,
        outputs=entries,
    )


class NativeClaimBridgeTests(unittest.TestCase):
    def test_all_nine_native_outputs_bound_and_consistent(self):
        report = run()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["native_binding_status"], "PASS")
        self.assertEqual(report["native_job_count"], 9)
        self.assertEqual(report["observed_native_formats"], ["ARTICLE", "CAROUSEL", "SHORT_VIDEO"])
        self.assertEqual(report["structured_consistency"]["status"], "PASS")
        self.assertEqual(report["native_binding_findings"], [])
        self.assertFalse(report["text_semantic_claim_extraction_observed"])
        self.assertFalse(report["nine_provider_outputs_observed"])

    def test_missing_native_claim_attachment_requires_review(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.BEGINNER and spec.format is OutputFormat.ARTICLE:
                payload["sections"][0]["paragraphs"][0]["source_refs"] = []
        result = run(patch=patch)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertIn("TYPED_ASSERTION_NOT_ANCHORED_IN_NATIVE_UNIT",
                      [f["code"] for f in result["native_binding_findings"]])
        self.assertIn("ARTICLE_METADATA_ONLY_CLAIM",
                      [f["code"] for f in result["native_binding_findings"]])

    def test_native_anchor_without_typed_assertion_reviews(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.ADVANCED and spec.format is OutputFormat.CAROUSEL:
                assertion.clear()
        report = run(patch=patch)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertIn("NATIVE_ANCHOR_WITHOUT_TYPED_ASSERTION",
                      [f["code"] for f in report["native_binding_findings"]])

    def test_wrong_native_span_ref_fails_closed(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.BEGINNER and spec.format is OutputFormat.CAROUSEL:
                payload["slides"][1]["source_refs"][0]["provenance"]["span_id"] = "unverified"
        report = run(patch=patch)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertIn("NATIVE_TYPED_ASSERTION_PROVENANCE_MISMATCH",
                      [f["code"] for f in report["native_binding_findings"]])

    def test_source_hash_tamper_is_rejected(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.BEGINNER and spec.format is OutputFormat.SHORT_VIDEO:
                payload["segments"][1]["source_refs"][0]["provenance"]["source_hash"] = "f" * 64
        with self.assertRaisesRegex(NativeEvidenceError, "lineage mismatch"):
            run(patch=patch)

    def test_native_text_binding_has_exact_text_requirement(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.INTERMEDIATE and spec.format is OutputFormat.SHORT_VIDEO:
                assertion["rendered_text"] = "Taxa: 16%"
        report = run(patch=patch)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertIn("TYPED_ASSERTION_TEXT_NOT_BOUND_TO_NATIVE_UNIT",
                      [f["code"] for f in report["native_binding_findings"]])

    def test_native_multi_unit_same_claim_must_be_reviewed(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.INTERMEDIATE and spec.format is OutputFormat.CAROUSEL:
                payload["slides"][2]["source_refs"] = [claim_ref()]
        report = run(patch=patch)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertIn("MULTIPLE_NATIVE_UNITS_REQUIRE_PER_UNIT_REVIEW",
                      [f["code"] for f in report["native_binding_findings"]])

    def test_unknown_claim_id_is_rejected(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.ADVANCED and spec.format is OutputFormat.ARTICLE:
                payload["sections"][0]["paragraphs"][0]["source_refs"][0]["claim_id"] = "not-in-ledger"
        with self.assertRaisesRegex(NativeEvidenceError, "missing source fact"):
            run(patch=patch)

    def test_financial_mismatch_is_strictly_failed_even_when_native_refs_pass(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.ADVANCED and spec.format is OutputFormat.ARTICLE:
                assertion["value"] = "14"
        report = run(patch=patch)
        self.assertEqual(report["native_binding_status"], "PASS")
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("CLAIM_SOURCE_CONTRADICTION",
                      [x["code"] for x in report["structured_consistency"]["findings"]])
        self.assertEqual(len(report["structured_consistency"]["targeted_repairs"]), 1)

    def test_upstream_policy_fail_dominates_uncertainty(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.BEGINNER and spec.format is OutputFormat.ARTICLE:
                payload["sections"][0]["paragraphs"][0]["source_refs"] = []
                gates["policy"] = GateStatus.FAIL
        report = run(patch=patch)
        self.assertEqual(report["native_binding_status"], "REVIEW_REQUIRED")
        self.assertEqual(report["status"], "FAIL")

    def test_missing_native_branch_review_required(self):
        report = run(change_output=lambda entries: entries[:-1])
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertEqual(report["native_job_count"], 8)
        self.assertEqual(report["structured_consistency"]["observed_branches"], 8)

    def test_duplicate_native_branch_rejected(self):
        with self.assertRaisesRegex(NativeEvidenceError, "duplicate native job_id"):
            run(change_output=lambda entries: entries + (entries[0],))

    def test_wrong_native_format_rejected(self):
        def change(entries):
            other = next(x for x in entries if x.spec.format is OutputFormat.CAROUSEL)
            return (replace(entries[0], output=other.output),) + entries[1:]
        with self.assertRaisesRegex(NativeEvidenceError, "format differs"):
            run(change_output=change)

    def test_native_output_source_must_equal_bundle_source(self):
        def change(entries):
            first = entries[0]
            tampered_spec = first.spec.model_copy(update={"source": SOURCE.model_copy(update={"source_hash": "b" * 64})})
            return (replace(first, spec=tampered_spec),) + entries[1:]
        with self.assertRaisesRegex(NativeEvidenceError, "source identity"):
            run(change_output=change)

    def test_article_metadata_citation_does_not_replace_unit_binding(self):
        def patch(spec, payload, assertion, gates):
            if spec.audience is AudienceLevel.BEGINNER and spec.format is OutputFormat.ARTICLE:
                payload["sections"][0]["paragraphs"][0]["source_refs"] = []
                assertion.clear()
        report = run(patch=patch)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertIn("ARTICLE_METADATA_ONLY_CLAIM",
                      [f["code"] for f in report["native_binding_findings"]])

    def test_deterministic_report_identity_and_synthetic_evidence(self):
        first, second = run(), run()
        self.assertEqual(first, second)
        self.assertFalse(first["production_ready"])
        self.assertFalse(first["source_original_verified_by_bridge"])
        self.assertFalse(first["human_gold_eligible"])


if __name__ == "__main__":
    unittest.main()
