from __future__ import annotations
import json
import unittest
from experiments.automated_calibration_w004 import run_t005_a02 as mod


class AutomatedCalibrationT005A02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = mod.build()

    def test_population_and_join_are_exact(self):
        self.assertEqual(self.report["target_to_automated"]["n"], 36)
        self.assertEqual(self.report["join"]["joined_item_count"], 36)
        self.assertTrue(self.report["join"]["one_to_one"])
        self.assertFalse(self.report["join"]["target_exposure_during_a03"])
        self.assertFalse(self.report["held_out_touched"])

    def test_evidence_class_cannot_impersonate_human_gold(self):
        self.assertEqual(self.report["evidence_class"], "MODEL_AUTOMATED_BLIND_CALIBRATION")
        self.assertFalse(self.report["human_gold_eligible"])
        self.assertFalse(self.report["human_agreement_observed"])
        self.assertFalse(self.report["human_preference_observed"])
        self.assertEqual(self.report["threshold_disposition"], "DIAGNOSTIC_ONLY")
        self.assertFalse(self.report["downstream_eligibility"]["human_gold_dependent_claims"])
        for row in self.report["joined_rows"]:
            self.assertNotIn("annotation_role", row)
            self.assertNotIn("annotator_id", row)

    def test_requested_targets_remain_balanced_frozen_grid(self):
        self.assertEqual(
            self.report["target_to_automated"]["target_counts"],
            {"ADVANCED": 12, "BEGINNER": 12, "INTERMEDIATE": 12},
        )

    def test_a03_fingerprint_is_accepted_one(self):
        self.assertEqual(self.report["join"]["a03_output_sha256"], mod.EXPECTED_A03_SHA256)

    def test_serialized_report_has_no_primary_role_claims(self):
        text = json.dumps(self.report, sort_keys=True)
        self.assertNotIn('"annotation_role":', text)
        self.assertNotIn('"human_gold_eligible": true', text.lower())
        self.assertNotIn('"human_agreement_observed": true', text.lower())


if __name__ == "__main__":
    unittest.main()
