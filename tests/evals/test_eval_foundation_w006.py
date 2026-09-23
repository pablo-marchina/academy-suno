from pathlib import Path
import importlib.util
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "experiments/eval_foundation_w006/validate_foundation.py"
SPEC = importlib.util.spec_from_file_location("w006_eval_foundation", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


class EvalFoundationW006Tests(unittest.TestCase):
    def test_model_only_never_human_gold(self):
        self.assertFalse(MOD.model_only_can_be_human_gold(["MODEL_AUTOMATED_BLIND_CALIBRATION", "MODEL_JUDGE_CALIBRATED"]))

    def test_human_reference_classifier(self):
        self.assertTrue(MOD.model_only_can_be_human_gold(["HUMAN_INDEPENDENT_CALIBRATION", "HUMAN_ADJUDICATED_GOLD"]))

    def test_derived_3x3_effective_n(self):
        rows = [{"source_group_id": "one", "audience": a, "format": f} for a in ("BEGINNER", "INTERMEDIATE", "ADVANCED") for f in ("ARTICLE", "CAROUSEL", "SHORT_VIDEO")]
        self.assertEqual(MOD.effective_source_n(rows), 1)

    def test_pairing_requires_exact_membership(self):
        base = [{"source_group_id": "one", "audience": "BEGINNER", "format": "ARTICLE"}]
        cand = list(base)
        self.assertEqual(MOD.validate_pairing(base, cand), (1, 1))
        with self.assertRaises(AssertionError):
            MOD.validate_pairing(base, [])

    def test_repository_contracts(self):
        repo_root = Path(__file__).resolve().parents[2]
        report = MOD.validate_foundation(repo_root)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["observed"]["model_only_human_gold_acceptances"], 0)
        self.assertEqual(report["observed"]["audience_threshold_status"], "DIAGNOSTIC_ONLY")


if __name__ == "__main__":
    unittest.main()
