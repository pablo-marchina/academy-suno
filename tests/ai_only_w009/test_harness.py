from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "experiments" / "ai_only_w009" / "harness.py"
spec = importlib.util.spec_from_file_location("w009_harness", SCRIPT)
assert spec is not None and spec.loader is not None
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


def sample(*, wrong_branch: tuple[str, str] | None = None) -> dict:
    variants = []
    for audience, fmt in sorted(harness.BRANCHES):
        output = "O Copom manteve a taxa Selic em 15% ao ano."
        if (audience, fmt) == wrong_branch:
            output = "O Copom manteve a taxa Selic em 14% ao ano."
        variants.append(
            {
                "audience": audience,
                "format": fmt,
                "output": output,
                "hard_gates": {gate: "PASS" for gate in harness.GATES},
            }
        )
    return {
        "schema_version": "ai_only_w009.input.v1",
        "run_id": "synthetic-test-run-01",
        "source_group_id": "SYNTHETIC_COPOM_01",
        "evidence_class": "SYNTHETIC_FIXTURE",
        "generator": {"provider": "synthetic_fixture", "model": "test-input", "version": "v1"},
        "source": {
            "status": "PASS",
            "spans": [{"span_id": "fixture-s1", "text": "O Copom manteve a taxa Selic em 15% ao ano."}],
        },
        "variants": variants,
    }


class TestAiOnlyHarness(unittest.TestCase):
    SALT = "w009-preregistered-split-policy-v1"

    def test_nine_variants_deterministic_and_honest_limits(self) -> None:
        fixture = sample()
        report, blind = harness.evaluate_run(fixture, split_salt=self.SALT)
        again, blind2 = harness.evaluate_run(fixture, split_salt=self.SALT)
        self.assertEqual(report, again)
        self.assertEqual(blind, blind2)
        self.assertEqual(report["branch_count_observed"], 9)
        self.assertEqual(report["branch_count_expected"], 9)
        self.assertEqual(report["missing_branches"], [])
        self.assertEqual(report["overall_status"], "PASS")
        self.assertEqual(report["evidence_class"], "SYNTHETIC_FIXTURE")
        self.assertFalse(report["human_gold_eligible"])
        self.assertFalse(report["production_ready"])
        self.assertEqual(report["judge_status"], "NOT_RUN")
        self.assertEqual(len(blind), 9)
        for item in blind:
            self.assertNotIn("generator", item)
            self.assertNotIn("run_id", item)
            self.assertNotIn("source_group_id", item)
            self.assertNotIn("fixture_id", item)
            self.assertEqual(item["rubric_version"], "machine_judge_secondary_v1_NOT_EXECUTED")

    def test_one_critical_numeric_mismatch_blocks_all_pass(self) -> None:
        report, _ = harness.evaluate_run(
            sample(wrong_branch=("BEGINNER", "ARTICLE")), split_salt=self.SALT
        )
        self.assertEqual(report["overall_status"], "FAIL")
        finding = next(x for x in report["raw_findings"] if x["audience"] == "BEGINNER"
                       and x["format"] == "ARTICLE")
        self.assertEqual(finding["hard_gates"]["factual"], "FAIL")
        self.assertEqual(finding["factual_failure_code"], "FACT_NUMERIC_MAGNITUDE_MISMATCH")
        self.assertEqual(report["counts"]["FAIL"], 1)
        self.assertEqual(report["counts"]["PASS"], 8)

    def test_missing_branch_never_becomes_complete_pass(self) -> None:
        fixture = sample()
        fixture["variants"].pop()
        report, _ = harness.evaluate_run(fixture, split_salt=self.SALT)
        self.assertEqual(report["branch_count_observed"], 8)
        self.assertEqual(report["overall_status"], "REVIEW_REQUIRED")
        self.assertEqual(len(report["missing_branches"]), 1)

    def test_source_review_and_policy_fail_are_noncompensatory(self) -> None:
        fixture = sample()
        fixture["source"]["status"] = "REVIEW_REQUIRED"
        review, _ = harness.evaluate_run(fixture, split_salt=self.SALT)
        self.assertEqual(review["overall_status"], "REVIEW_REQUIRED")
        fixture["variants"][0]["hard_gates"]["policy"] = "FAIL"
        failed, _ = harness.evaluate_run(fixture, split_salt=self.SALT)
        self.assertEqual(failed["overall_status"], "FAIL")

    def test_reject_duplicate_or_unknown_branches_and_missing_gates(self) -> None:
        fixture = sample()
        fixture["variants"].append(dict(fixture["variants"][0]))
        with self.assertRaisesRegex(harness.EvidenceError, "duplicate"):
            harness.evaluate_run(fixture, split_salt=self.SALT)
        fixture = sample()
        fixture["variants"][0]["format"] = "PODCAST"
        with self.assertRaisesRegex(harness.EvidenceError, "unknown"):
            harness.evaluate_run(fixture, split_salt=self.SALT)
        fixture = sample()
        del fixture["variants"][0]["hard_gates"]["provenance"]
        with self.assertRaisesRegex(harness.EvidenceError, "five"):
            harness.evaluate_run(fixture, split_salt=self.SALT)

    def test_identical_generator_and_judge_blocked(self) -> None:
        fixture = sample()
        fixture["judge"] = dict(fixture["generator"])
        with self.assertRaisesRegex(harness.EvidenceError, "independent judge"):
            harness.evaluate_run(fixture, split_salt=self.SALT)

    def test_falsely_passing_human_gold_is_rejected(self) -> None:
        fixture = sample()
        fixture["human_gold"] = []
        with self.assertRaisesRegex(harness.EvidenceError, "never accepts"):
            harness.evaluate_run(fixture, split_salt=self.SALT)

    def test_source_group_partition_stable_and_no_corrupt_spans(self) -> None:
        a = sample()
        b = sample()
        b["run_id"] = "synthetic-test-run-02"
        corpus = harness.evaluate_corpus([a, b], split_salt=self.SALT)
        self.assertEqual(corpus["source_group_count"], 1)
        self.assertEqual(corpus["reports"][0]["split"], corpus["reports"][1]["split"])
        self.assertEqual(corpus["model_judge_status"], "NOT_RUN")
        a["source"]["spans"] = []
        with self.assertRaisesRegex(harness.EvidenceError, "nonempty evidence spans"):
            harness.evaluate_run(a, split_salt=self.SALT)

    def test_fail_closed_on_bad_corpus(self) -> None:
        with self.assertRaisesRegex(harness.EvidenceError, "at least one"):
            harness.evaluate_corpus([], split_salt=self.SALT)
        a = sample()
        with self.assertRaisesRegex(harness.EvidenceError, "duplicate run"):
            harness.evaluate_corpus([a, a], split_salt=self.SALT)

    def test_json_round_trip_and_blind_order(self) -> None:
        a = sample()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input.json"
            path.write_text(json.dumps([a]), encoding="utf-8")
            data = json.loads(path.read_text(encoding="utf-8"))
            report = harness.evaluate_corpus(data, split_salt=self.SALT)
            _, rows = harness.evaluate_run(data[0], split_salt=self.SALT)
        self.assertEqual(report["run_count"], 1)
        self.assertEqual(len(rows), 9)
        self.assertEqual(len(set(x["blind_id"] for x in rows)), 9)


if __name__ == "__main__":
    unittest.main()
