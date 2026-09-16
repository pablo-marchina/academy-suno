from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.domain import AudienceLevel, OutputFormat  # noqa: E402
from suno_content.evals.audience import evaluate_audience_features, load_ontology  # noqa: E402


class AntiGamingFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ontology = load_ontology(ROOT / "data" / "ontology" / "finance_ptbr_v001.json")
        payload = json.loads(
            (ROOT / "tests" / "evals" / "audience" / "fixtures" / "anti_gaming_v001.json").read_text(
                encoding="utf-8"
            )
        )
        cls.fixture_version = payload["fixture_version"]
        cls.cases = payload["cases"]

    def test_all_versioned_adversarial_cases_emit_expected_diagnostics(self) -> None:
        self.assertEqual(self.fixture_version, "audience-anti-gaming-v001")
        for case in self.cases:
            with self.subTest(case=case["case_id"]):
                vector = evaluate_audience_features(
                    case["text"],
                    audience=AudienceLevel(case["audience"]),
                    output_format=OutputFormat(case["format"]),
                    ontology=self.ontology,
                    required_concept_ids=tuple(case["required_concepts"]),
                )
                observed = set(vector.anti_gaming.flags)
                self.assertTrue(set(case["expected_flags"]).issubset(observed), observed)


if __name__ == "__main__":
    unittest.main()
