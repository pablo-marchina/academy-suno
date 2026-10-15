from __future__ import annotations

import unittest
from copy import deepcopy
from decimal import Decimal

from pydantic import ValidationError

from suno_content.consistency import ConsistencyBundle, evaluate_consistency
from suno_content.domain import AudienceLevel, OutputFormat


HASH = "a" * 64


def make_fixture(*, required: bool = True) -> dict:
    source = {"source_id": "fixture-copom", "source_hash": HASH, "artifact_ref": "fixture/copom.pdf"}
    provenance = [{
        "source_id": source["source_id"], "source_hash": HASH, "page_number": 1, "span_id": "policy-rate"
    }]
    fact = {
        "fact_id": "selic-2026-10", "value": "15.00", "unit": "PERCENT_PER_YEAR",
        "period": "2026-10", "modality": "ACTUAL", "direction": "UNCHANGED",
        "materiality": "CRITICAL", "required_for_all": required,
        "provenance": deepcopy(provenance), "source_gate": "PASS"
    }
    variants = []
    for audience in AudienceLevel:
        for output_format in OutputFormat:
            variants.append({
                "job_id": f"job-{audience.value.lower()}-{output_format.value.lower()}",
                "audience": audience.value, "output_format": output_format.value,
                "upstream_gates": {
                    "source": "PASS", "factual": "PASS", "policy": "PASS",
                    "schema": "PASS", "provenance": "PASS"
                },
                "assertions": [{
                    "fact_id": "selic-2026-10",
                    "value": "15", "unit": "PERCENT_PER_YEAR", "period": "2026-10",
                    "modality": "ACTUAL", "direction": "UNCHANGED", "provenance": deepcopy(provenance),
                    "rendered_text": (
                        "A taxa Selic ficou em 15% ao ano."
                        if audience is AudienceLevel.BEGINNER
                        else "O Copom manteve a taxa Selic em 15% ao ano."
                    ),
                }],
            })
    return {
        "run_id": "synthetic-fixture-only",
        "source": source,
        "source_ledger_version": "synthetic-ledger-v1",
        "facts": [fact],
        "variants": variants,
    }


def evaluate(value: dict) -> dict:
    return evaluate_consistency(ConsistencyBundle.model_validate(value))


class CrossOutputConsistencyTests(unittest.TestCase):
    def test_complete_nine_with_legitimate_wording_differences(self) -> None:
        report = evaluate(make_fixture())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["observed_branches"], 9)
        self.assertEqual(report["expected_branches"], 9)
        self.assertEqual(report["findings"], [])
        self.assertFalse(report["human_gold_eligible"])
        self.assertFalse(report["production_ready"])
        self.assertFalse(report["source_original_claim_extraction_observed"])

    def test_numeric_contradiction_targets_only_bad_branch(self) -> None:
        fixture = make_fixture()
        fixture["variants"][0]["assertions"][0]["value"] = "14.5"
        report = evaluate(fixture)
        self.assertEqual(report["status"], "FAIL")
        codes = [f["code"] for f in report["findings"]]
        self.assertIn("CLAIM_SOURCE_CONTRADICTION", codes)
        self.assertIn("CROSS_OUTPUT_CONTRADICTION", codes)
        self.assertEqual(len(report["targeted_repairs"]), 1)
        self.assertEqual(report["targeted_repairs"][0]["job_id"], fixture["variants"][0]["job_id"])
        self.assertNotIn("output", report["targeted_repairs"][0])

    def test_period_and_unit_mismatch_fail_financial_meaning(self) -> None:
        for field, value in [("period", "2025-10"), ("unit", "BASIS_POINTS")]:
            with self.subTest(field=field):
                fixture = make_fixture()
                fixture["variants"][3]["assertions"][0][field] = value
                report = evaluate(fixture)
                self.assertEqual(report["status"], "FAIL")
                bad = next(x for x in report["findings"] if x["code"] == "CLAIM_SOURCE_CONTRADICTION")
                self.assertEqual(bad["mismatched_fields"], [field])

    def test_modality_forecast_promotion_detected(self) -> None:
        fixture = make_fixture()
        fixture["variants"][1]["assertions"][0]["modality"] = "FORECAST"
        report = evaluate(fixture)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("modality", next(
            x["mismatched_fields"] for x in report["findings"]
            if x["code"] == "CLAIM_SOURCE_CONTRADICTION"
        ))

    def test_opposite_direction_detected(self) -> None:
        fixture = make_fixture()
        fixture["variants"][2]["assertions"][0]["direction"] = "UP"
        report = evaluate(fixture)
        self.assertEqual(report["status"], "FAIL")

    def test_optional_claim_omission_is_not_false_contradiction(self) -> None:
        fixture = make_fixture(required=False)
        fixture["variants"][1]["assertions"] = []
        report = evaluate(fixture)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["findings"], [])

    def test_required_claim_omission_reviews_not_passes(self) -> None:
        fixture = make_fixture()
        fixture["variants"][1]["assertions"] = []
        report = evaluate(fixture)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertIn("REQUIRED_FACT_OMITTED", [f["code"] for f in report["findings"]])

    def test_missing_nine_branch_reviews(self) -> None:
        fixture = make_fixture()
        fixture["variants"].pop()
        report = evaluate(fixture)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertEqual(len(report["missing_branches"]), 1)

    def test_source_review_and_policy_fail_preserved(self) -> None:
        fixture = make_fixture()
        fixture["facts"][0]["source_gate"] = "REVIEW_REQUIRED"
        self.assertEqual(evaluate(fixture)["status"], "REVIEW_REQUIRED")
        fixture["variants"][0]["upstream_gates"]["policy"] = "FAIL"
        self.assertEqual(evaluate(fixture)["status"], "FAIL")

    def test_wrong_or_missing_provenance_fails_closed(self) -> None:
        fixture = make_fixture()
        fixture["variants"][0]["assertions"][0]["provenance"][0]["span_id"] = "wrong-span"
        report = evaluate(fixture)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertIn("ASSERTION_SOURCE_REF_MISMATCH", [f["code"] for f in report["findings"]])
        fixture = make_fixture()
        fixture["variants"][0]["assertions"][0]["provenance"][0]["source_hash"] = "b" * 64
        with self.assertRaisesRegex(ValidationError, "outside run source"):
            evaluate(fixture)
        fixture = make_fixture()
        fixture["variants"][0]["assertions"][0]["provenance"] = []
        with self.assertRaises(ValidationError):
            evaluate(fixture)

    def test_duplicate_branch_or_unknown_claim_blocked(self) -> None:
        fixture = make_fixture()
        fixture["variants"].append(deepcopy(fixture["variants"][0]))
        with self.assertRaisesRegex(ValidationError, "duplicate 3x3 branch"):
            evaluate(fixture)
        fixture = make_fixture()
        fixture["variants"][0]["assertions"][0]["fact_id"] = "fabricated-claim"
        with self.assertRaisesRegex(ValidationError, "unknown assertion fact_id"):
            evaluate(fixture)

    def test_nonfinite_or_float_value_rejected_without_rounding(self) -> None:
        for value in [15.0, float("nan"), "Infinity", "NaN"]:
            with self.subTest(value=str(value)):
                fixture = make_fixture()
                fixture["variants"][0]["assertions"][0]["value"] = value
                with self.assertRaises(ValidationError):
                    evaluate(fixture)

    def test_conditional_source_qualifier_retained(self) -> None:
        fixture = make_fixture()
        fact = fixture["facts"][0]
        fact["modality"] = "CONDITIONAL"
        fact["condition"] = "sujeito a aprovacao"
        for variant in fixture["variants"]:
            variant["assertions"][0]["modality"] = "CONDITIONAL"
            variant["assertions"][0]["condition"] = "sujeito a aprovacao"
        self.assertEqual(evaluate(fixture)["status"], "PASS")
        fixture["variants"][0]["assertions"][0]["condition"] = "caso contrario"
        report = evaluate(fixture)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("condition", next(x for x in report["findings"]
                                        if x["code"] == "CLAIM_SOURCE_CONTRADICTION")["mismatched_fields"])

    def test_unobserved_source_fact_review_even_when_no_output_mentions_it(self) -> None:
        fixture = make_fixture(required=False)
        for variant in fixture["variants"]:
            variant["assertions"] = []
        fixture["facts"][0]["source_gate"] = "REVIEW_REQUIRED"
        report = evaluate(fixture)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertEqual(report["findings"][0]["code"], "UNVERIFIED_SOURCE_FACT")

    def test_nonmaterial_discrepancy_reviews_instead_of_critical_fail(self) -> None:
        fixture = make_fixture()
        fixture["facts"][0]["materiality"] = "OTHER"
        fixture["variants"][0]["assertions"][0]["value"] = "16.0"
        self.assertEqual(evaluate(fixture)["status"], "REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
