import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "experiments/benchmark_w005/validate_methodology_v002.py"

spec = importlib.util.spec_from_file_location("validate_w005_methodology_v002", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class BenchmarkMethodologyV002ContractTest(unittest.TestCase):
    def test_methodology_invariants(self):
        module.validate()

    def test_artifacts_exist(self):
        for rel in [
            "docs/evals/benchmark_methodology_w005.md",
            "docs/decisions/research/DR-5909-cross-cutting-benchmark-methodology.md",
            "data/evals/w005/benchmark_methodology_v002.json",
            "data/evals/w005/benchmark_result_v002.schema.json",
        ]:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_hard_gate_is_non_compensatory(self):
        self.assertTrue(module.is_eligible({"FACTUAL": "PASS", "PAIRING": "PASS"}))
        self.assertFalse(module.is_eligible({"FACTUAL": "FAIL", "PAIRING": "PASS"}))
        self.assertFalse(module.is_eligible({"FACTUAL": "REVIEW_REQUIRED", "PAIRING": "PASS"}))

    def test_pareto_preserves_tradeoffs(self):
        directions = {"quality": "maximize", "latency": "minimize"}
        metrics = {
            "quality_leader": {"quality": 95.0, "latency": 200.0},
            "latency_leader": {"quality": 85.0, "latency": 100.0},
            "dominated": {"quality": 80.0, "latency": 220.0},
        }
        self.assertEqual(
            module.point_pareto_frontier(metrics, directions, metrics.keys()),
            ["latency_leader", "quality_leader"],
        )

    def test_utility_cannot_select_without_evidence_and_stability(self):
        self.assertFalse(module.utility_preference_allowed({
            "status": "PENDING_EVIDENCE",
            "weights": None,
            "evidence_refs": [],
            "sensitivity": {"preferred_set_stable": False},
        }))
        self.assertFalse(module.utility_preference_allowed({
            "status": "EVIDENCE_SUPPORTED",
            "weights": {"quality": 0.5, "cost": 0.5},
            "evidence_refs": ["study"],
            "sensitivity": {"preferred_set_stable": False},
        }))
        self.assertTrue(module.utility_preference_allowed({
            "status": "EVIDENCE_SUPPORTED",
            "weights": {"quality": 0.5, "cost": 0.5},
            "evidence_refs": ["study"],
            "sensitivity": {"preferred_set_stable": True},
        }))


if __name__ == "__main__":
    unittest.main()
