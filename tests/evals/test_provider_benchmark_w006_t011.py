from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "experiments" / "provider_benchmark_w006" / "validate_t011_evidence.py"
spec = importlib.util.spec_from_file_location("validate_t011_evidence", VALIDATOR)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class ProviderBenchmarkT011Tests(unittest.TestCase):
    def test_evidence_invariants_pass(self) -> None:
        self.assertEqual(module.validate(), [])

    def test_no_fresh_measurements_are_fabricated(self) -> None:
        data = json.loads((ROOT / "data/evals/production/w006/provider_benchmark_observations_t011_v001.json").read_text())
        self.assertEqual(data["fresh_execution"]["status"], "NOT_RUN")
        for row in data["fresh_execution"]["observations"]:
            self.assertIsNone(row["quality"])
            self.assertIsNone(row["latency_ms"])
            self.assertIsNone(row["cost_usd"])

    def test_no_winner_or_default_is_forced(self) -> None:
        data = json.loads((ROOT / "data/evals/production/w006/provider_pareto_t011_v001.json").read_text())
        self.assertEqual(data["pareto_status"], "PARETO_NOT_COMPUTABLE")
        self.assertEqual(data["decision_state"], "NO_PREFERENCE")
        self.assertIsNone(data["promoted_default"])

    def test_human_boundary_is_preserved(self) -> None:
        data = json.loads((ROOT / "data/evals/production/w006/provider_benchmark_observations_t011_v001.json").read_text())
        human = data["human_evidence"]
        self.assertEqual(human["independent_primary_streams"], 0)
        self.assertEqual(human["adjudicated_gold_items"], 0)
        self.assertEqual(human["audience_threshold_status"], "DIAGNOSTIC_ONLY")

    def test_historical_groq_evidence_is_mechanics_only(self) -> None:
        data = json.loads((ROOT / "data/evals/production/w006/provider_benchmark_observations_t011_v001.json").read_text())
        control = data["historical_mechanics_control"]
        self.assertEqual(control["evidence_class"], "OBSERVED_PROVIDER_MECHANICS")
        self.assertIsNone(control["quality"])
        self.assertIn("MECHANICS_ONLY", control["comparison_eligibility"])


if __name__ == "__main__":
    unittest.main()
