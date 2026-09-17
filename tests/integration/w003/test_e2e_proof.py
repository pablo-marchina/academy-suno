from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.w003_e2e.run_proof import execute_proof  # noqa: E402


class W003EndToEndProofTests(unittest.TestCase):
    def test_source_to_nine_jobs_repair_resume_and_telemetry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="w003-proof-test-") as temp_dir:
            report = execute_proof(Path(temp_dir))
        self.assertEqual(report["final_phase"], "complete")
        self.assertEqual(report["job_count"], 9)
        self.assertEqual(report["joined_output_count"], 9)
        self.assertEqual(report["telemetry"]["transport_retries"]["total"], 1)
        self.assertEqual(report["telemetry"]["quality_repairs"]["total"], 1)
        self.assertIsNone(report["telemetry"]["usage"])
        self.assertIsNone(report["telemetry"]["observed_cost"])
        self.assertTrue(report["repair_lineage"][0]["fresh_hard_gate_runs"])
        self.assertTrue(report["repair_lineage"][0]["siblings_immutable"])
        self.assertFalse(report["non_compensation_probe"]["soft_signal_masked_hard_fail"])
        self.assertEqual(report["evidence_classification"]["audience_thresholds"], "DIAGNOSTIC_ONLY")
        self.assertEqual(report["evidence_classification"]["semantic_ablation"], "NOT_RUN")
        self.assertEqual(report["evidence_classification"]["provider_quality_latency_cost"], "PRODUCTION_UNKNOWN")


if __name__ == "__main__":
    unittest.main()
