from __future__ import annotations
import unittest
from experiments.semantic_ablation_w004 import run_t006_a01 as mod


class T006A01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = mod.build()

    def test_population_and_evidence_boundary(self):
        self.assertEqual(self.report['sample_count'], 36)
        self.assertEqual(self.report['reference_evidence_class'], 'MODEL_AUTOMATED_BLIND_CALIBRATION')
        self.assertFalse(self.report['human_gold_eligible'])
        self.assertFalse(self.report['human_preference_observed'])
        self.assertEqual(self.report['threshold_disposition'], 'DIAGNOSTIC_ONLY')

    def test_hard_gates_are_invariant_and_never_compensated(self):
        self.assertTrue(self.report['hard_gate_invariant_all'])
        self.assertEqual(self.report['hard_fail_compensation_count'], 0)
        for row in self.report['rows']:
            self.assertTrue(row['hard_gate_invariant'])
            self.assertEqual(row['hard_fail_codes_without_semantic'], row['hard_fail_codes_with_semantic'])
            if row['hard_fail_codes_without_semantic']:
                self.assertNotEqual(row['with_semantic'], 'PASS')

    def test_experimental_proxy_cannot_lock_backend(self):
        self.assertFalse(self.report['candidate_backend']['production_lock_eligible'])
        self.assertEqual(self.report['backend_decision'], 'NO_BACKEND_PREFERENCE')

    def test_ablation_is_paired(self):
        self.assertEqual(len(self.report['rows']), 36)
        self.assertEqual(len(self.report['semantic_rows_for_release_gate']), 36)


if __name__ == '__main__':
    unittest.main()
