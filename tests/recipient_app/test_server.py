from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from app.recipient.server import render_home, render_result  # noqa: E402
from suno_content.ingest import IntegratedEvidence, ingest_text  # noqa: E402


class RecipientServerRenderingTests(unittest.TestCase):
    def test_home_exposes_text_pdf_path_and_pdf_upload(self) -> None:
        page = render_home()
        self.assertIn('name="text_input"', page)
        self.assertIn('name="pdf_path"', page)
        self.assertIn('name="pdf_upload"', page)
        self.assertIn("MECHANICS_ONLY", page)
        self.assertIn("PRODUCTION_UNKNOWN", page)

    def test_result_surfaces_provenance_3x3_and_repair_lineage(self) -> None:
        result = ingest_text(
            "Documento financeiro com contexto suficiente para o planejamento recipient-facing."
        )
        evidence = IntegratedEvidence(
            mechanics_end_to_end="PROVEN",
            audience_thresholds="DIAGNOSTIC_ONLY",
            provider_quality_latency_cost="PRODUCTION_UNKNOWN/BLOCKED",
            parser_implementation="PENDING/UNLOCKED",
            production_release_readiness="PENDING_W004_T008",
            repair_lineage={
                "job_id": "beginner:carousel",
                "before_status": "FAIL",
                "after_status": "PASS",
                "before_output_hash": "before-hash",
                "after_output_hash": "after-hash",
                "fresh_hard_gate_runs": True,
                "siblings_immutable": True,
            },
        )
        page = render_result(result, evidence)
        self.assertIn(result.source_hash, page)
        self.assertIn("SOURCE_READY", page)
        self.assertGreaterEqual(page.count("PLANNED_MECHANICS_ONLY"), 9)
        self.assertIn("DIAGNOSTIC_ONLY", page)
        self.assertIn("PRODUCTION_UNKNOWN/BLOCKED", page)
        self.assertIn("before-hash", page)
        self.assertIn("after-hash", page)


if __name__ == "__main__":
    unittest.main()
