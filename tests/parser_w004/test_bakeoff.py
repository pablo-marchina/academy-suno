import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "experiments" / "parser_w004" / "run_bakeoff.py"
SPEC = importlib.util.spec_from_file_location("parser_w004_bakeoff", RUNNER)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class ParserW004BakeoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = mod.run_bakeoff()

    def test_representative_source_families_present(self):
        self.assertEqual(
            set(self.result["source_families"]),
            {"copom", "cvm_itr", "earnings_results"},
        )
        self.assertGreaterEqual(self.result["fixture_count"], 3)

    def test_reference_preserves_provenance_and_passes(self):
        aggregate = self.result["aggregate_candidates"]["provenance_preserving_reference"]
        self.assertEqual(aggregate["status"], "PASS")
        self.assertEqual(aggregate["provenance_accuracy_min"], 1.0)
        self.assertEqual(aggregate["value_coverage_min"], 1.0)

    def test_flat_values_never_become_source_ready(self):
        aggregate = self.result["aggregate_candidates"]["flat_value_only"]
        self.assertEqual(aggregate["status"], "REVIEW_REQUIRED")
        self.assertEqual(aggregate["value_coverage_min"], 1.0)
        self.assertEqual(aggregate["provenance_accuracy_min"], 0.0)
        self.assertTrue(aggregate["silent_corruption_detected"])

    def test_wrong_role_fails_despite_full_value_coverage(self):
        aggregate = self.result["aggregate_candidates"]["wrong_role_probe"]
        self.assertEqual(aggregate["status"], "FAIL")
        self.assertEqual(aggregate["value_coverage_min"], 1.0)
        self.assertTrue(aggregate["silent_corruption_detected"])
        for fixture in self.result["by_fixture"].values():
            score = fixture["results"]["wrong_role_probe"]
            self.assertEqual(score["value_coverage"], 1.0)
            self.assertEqual(score["status"], "FAIL")

    def test_wrong_unit_cross_table_fails_where_applicable(self):
        score = self.result["by_fixture"]["petrobras_1t26_results"]["results"]["wrong_unit_probe"]
        self.assertEqual(score["status"], "FAIL")
        self.assertEqual(score["value_coverage"], 1.0)
        fields = {issue.get("field") for issue in score["issues"]}
        self.assertIn("unit", fields)
        self.assertIn("table_id", fields)

    def test_parser_identity_remains_unlocked(self):
        decision = self.result["implementation_decision"]
        self.assertEqual(decision["status"], "UNLOCKED")
        self.assertIsNone(decision["preferred_implementation"])

    def test_hard_gate_contract_is_explicit(self):
        gates = "\n".join(self.result["hard_gates"])
        self.assertIn("missing provenance cannot be promoted to PASS", gates)
        self.assertIn("wrong non-null provenance is a FAIL", gates)

    def test_results_are_json_serializable(self):
        json.dumps(self.result, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
