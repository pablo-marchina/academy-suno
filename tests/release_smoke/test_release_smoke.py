from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.release_smoke.run_release_smoke import run_release_smoke  # noqa: E402


class ReleaseSmokeTests(unittest.TestCase):
    def test_integrated_release_smoke_preserves_lineage_and_unknowns(self) -> None:
        with tempfile.TemporaryDirectory(prefix="w004-release-smoke-") as temp_dir:
            manifest = run_release_smoke(Path(temp_dir))

        self.assertEqual(manifest["status"], "PASS")
        self.assertEqual(manifest["lineage"]["before_status"], "FAIL")
        self.assertEqual(manifest["lineage"]["after_status"], "PASS")
        self.assertTrue(manifest["lineage"]["fresh_hard_gate_runs"])
        self.assertTrue(manifest["lineage"]["siblings_immutable"])
        self.assertEqual(manifest["evidence_posture"]["mechanics_end_to_end"], "PROVEN")
        self.assertEqual(manifest["evidence_posture"]["audience_thresholds"], "DIAGNOSTIC_ONLY")
        self.assertIn("PRODUCTION_UNKNOWN", manifest["evidence_posture"]["real_provider_quality_latency_cost"])
        self.assertEqual(manifest["evidence_posture"]["production_release_readiness"], "PENDING_W004_T008")
        self.assertEqual(len(manifest["non_claims"]), 4)


if __name__ == "__main__":
    unittest.main()
