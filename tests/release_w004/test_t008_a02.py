from __future__ import annotations
import unittest
from experiments.release_w004 import run_t008_a02 as mod

class T008A02Tests(unittest.TestCase):
    def test_canonical_dependency_is_attempt_valid_a05(self):
        e=mod.canonical_evidence()
        self.assertEqual(e['provider_model']['accepted_attempt'],'A05')
        self.assertEqual(e['provider_model']['observed_calls'],8)
        self.assertEqual(e['provider_model']['decision'],'NO_OVERALL_MODEL_PREFERENCE')
        self.assertFalse(e['provider_model']['human_gold'])
        self.assertFalse(e['provider_model']['human_preference'])
        self.assertEqual(e['semantic']['decision'],'NO_BACKEND_PREFERENCE')
        self.assertEqual(e['calibration']['thresholds'],'DIAGNOSTIC_ONLY')

    def test_durable_demo_identity(self):
        d=mod.demo_evidence()
        self.assertEqual(d['sha256'],mod.EXPECTED_DEMO_SHA)
        self.assertEqual(d['size_bytes'],mod.EXPECTED_DEMO_SIZE)
        self.assertLessEqual(d['duration_seconds'],300.0)
        self.assertTrue(d['durable_copy'])

if __name__=='__main__': unittest.main()
