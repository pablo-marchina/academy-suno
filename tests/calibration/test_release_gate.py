from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "experiments" / "calibration" / "release_gate.py"
spec = importlib.util.spec_from_file_location("calibration_release_gate", MODULE_PATH)
release_gate = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = release_gate
spec.loader.exec_module(release_gate)


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "benchmark_version": "gold-v001",
            "threshold_policy": {"freeze_allowed": False, "mode": "DIAGNOSTIC_ONLY"},
            "sources": [
                {"source_id": "dev-a", "split": "DEVELOPMENT", "tuning_exposure": "ALLOWED_DEVELOPMENT_ONLY"},
                {"source_id": "dev-b", "split": "DEVELOPMENT", "tuning_exposure": "ALLOWED_DEVELOPMENT_ONLY"},
                {"source_id": "held", "split": "HELD_OUT", "tuning_exposure": "FORBIDDEN"},
            ],
            "gold_labels": [],
        }
        self.anti_gaming = [
            {"case_id": "jargon_stuffing", "observed_flags": ["JARGON_STUFFING", "ACRONYM_HACK"]},
            {"case_id": "sentence_chopping", "observed_flags": ["SENTENCE_CHOPPING"]},
            {"case_id": "acronym_hack", "observed_flags": ["ACRONYM_HACK"]},
            {"case_id": "required_concept_removal", "observed_flags": ["REQUIRED_CONCEPT_OMISSION"]},
        ]

    def test_confusion_matrix_and_macro_metrics_are_reproducible(self):
        truth = ["BEGINNER", "BEGINNER", "INTERMEDIATE", "ADVANCED"]
        predicted = ["BEGINNER", "INTERMEDIATE", "INTERMEDIATE", "BEGINNER"]
        metrics = release_gate.classification_metrics(truth, predicted)
        self.assertEqual(metrics["sample_count"], 4)
        self.assertEqual(metrics["confusion_matrix"]["BEGINNER"]["INTERMEDIATE"], 1)
        self.assertAlmostEqual(metrics["accuracy"], 0.5)
        self.assertIn("f1", metrics["macro"])

    def test_target_to_human_is_separate_from_human_to_evaluator(self):
        rows = [
            {"item_id": "a", "split": "DEVELOPMENT", "generation_target_level": "ADVANCED", "human_gold_level": "INTERMEDIATE", "evaluator_predicted_level": "INTERMEDIATE"},
            {"item_id": "b", "split": "DEVELOPMENT", "generation_target_level": "BEGINNER", "human_gold_level": "BEGINNER", "evaluator_predicted_level": "INTERMEDIATE"},
        ]
        report = release_gate.audience_calibration(rows)
        self.assertEqual(report["status"], "COMPUTED_DIAGNOSTIC")
        self.assertNotEqual(report["target_to_human"]["confusion_matrix"], report["human_to_evaluator"]["confusion_matrix"])

    def test_held_out_row_is_rejected_from_calibration(self):
        rows = [{"item_id": "held::ARTICLE::BEGINNER", "split": "HELD_OUT"}]
        with self.assertRaises(release_gate.CalibrationInputError):
            release_gate.audience_calibration(rows)

    def test_no_human_gold_or_agreement_forces_diagnostic_only(self):
        posture = release_gate.threshold_posture(self.manifest)
        self.assertEqual(posture["mode"], "DIAGNOSTIC_ONLY")
        self.assertFalse(posture["freeze_allowed"])
        self.assertIsNone(posture["numeric_thresholds"])

    def test_anti_gaming_requires_all_mandatory_failure_modes(self):
        gate = release_gate.anti_gaming_gate(self.anti_gaming)
        self.assertEqual(gate["status"], "PASS")
        broken = [case for case in self.anti_gaming if case["case_id"] != "required_concept_removal"]
        self.assertEqual(release_gate.anti_gaming_gate(broken)["status"], "FAIL")

    def test_semantic_ablation_cannot_compensate_hard_gate(self):
        rows = [{
            "item_id": "x",
            "hard_fail_codes_without_semantic": ["SOURCE_FAIL"],
            "hard_fail_codes_with_semantic": ["SOURCE_FAIL"],
            "decision_without_semantic": "FAIL",
            "decision_with_semantic": "PASS",
            "semantic_added_information": True,
        }]
        gate = release_gate.semantic_ablation_gate(rows)
        self.assertEqual(gate["status"], "FAIL")
        self.assertFalse(gate["hard_gate_invariant"])

    def test_synthetic_pricing_never_makes_provider_candidate_comparable(self):
        rows = [
            {"candidate_id": "a", "evidence_kind": "MEASURED", "pricing_provenance": "SYNTHETIC", "quality_observed": True, "latency_observed": True},
            {"candidate_id": "b", "evidence_kind": "MEASURED", "pricing_provenance": "SYNTHETIC", "quality_observed": True, "latency_observed": True},
        ]
        gate = release_gate.provider_comparison_gate(rows)
        self.assertEqual(gate["status"], "NOT_COMPARABLE")
        self.assertEqual(gate["decision"], "NO_PREFERENCE")

    def test_current_evidence_shape_yields_diagnostic_release_gate(self):
        report = release_gate.build_release_gate(
            manifest=self.manifest,
            audience_rows=[],
            anti_gaming_cases=self.anti_gaming,
            semantic_rows=[],
            provider_rows=[
                {"candidate_id": "demo", "evidence_kind": "MEASURED", "pricing_provenance": "SYNTHETIC", "quality_observed": False, "latency_observed": True}
            ],
        )
        self.assertEqual(report["overall_mode"], "DIAGNOSTIC_ONLY")
        self.assertEqual(report["held_out_tuning_exposure"], "FORBIDDEN")
        self.assertEqual(report["anti_gaming"]["status"], "PASS")
        self.assertEqual(report["semantic_ablation"]["decision"], "NO_BACKEND_PREFERENCE")
        self.assertEqual(report["provider_comparison"]["decision"], "NO_PREFERENCE")


if __name__ == "__main__":
    unittest.main()
