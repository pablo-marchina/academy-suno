from __future__ import annotations

import unittest

from experiments.release_w004 import run_t008_a01 as mod


class T008A01Tests(unittest.TestCase):
    def test_current_evidence_boundaries_are_explicit(self):
        evidence = mod.verify_current_evidence_boundaries()
        self.assertEqual(evidence["protocol_version"], "1.7.0")
        self.assertEqual(evidence["state_version"], "0036")
        self.assertFalse(evidence["calibration"]["human_gold_eligible"])
        self.assertFalse(evidence["calibration"]["human_agreement_observed"])
        self.assertEqual(evidence["calibration"]["thresholds"], "DIAGNOSTIC_ONLY")
        self.assertEqual(evidence["semantic"]["decision"], "NO_BACKEND_PREFERENCE")
        self.assertEqual(evidence["provider_model"]["decision"], "NO_OVERALL_MODEL_PREFERENCE")
        self.assertFalse(evidence["provider_model"]["human_preference_observed"])

    def test_durable_demo_is_exact_accepted_binary(self):
        demo = mod.verify_demo()
        self.assertEqual(demo["sha256"], mod.EXPECTED_DEMO_SHA)
        self.assertEqual(demo["size_bytes"], mod.EXPECTED_DEMO_SIZE)
        self.assertLessEqual(demo["duration_seconds"], 300.0)
        self.assertEqual(demo["video_package_review"], "PASS")
        self.assertTrue(demo["durable_repository_copy"])

    def test_no_blanket_readiness_language_in_decision_contract(self):
        self.assertNotIn("PRODUCTION_PASS", "T008_INTERNAL_RELEASE_PROOF_PASS_READY_FOR_FINAL_RECONCILIATION")


if __name__ == "__main__":
    unittest.main()
