from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.domain import AudienceLevel  # noqa: E402
from suno_content.evals.audience import ONTOLOGY_SCHEMA_VERSION, load_ontology  # noqa: E402


class OntologyValidationTests(unittest.TestCase):
    def test_seed_ontology_is_versioned_and_complete_per_audience(self) -> None:
        ontology = load_ontology(ROOT / "data" / "ontology" / "finance_ptbr_v001.json")
        self.assertEqual(ontology.schema_version, ONTOLOGY_SCHEMA_VERSION)
        self.assertGreaterEqual(len(ontology.concepts), 15)
        for concept in ontology.concepts:
            self.assertEqual(set(concept.audience_policy), set(AudienceLevel))
            self.assertTrue(concept.source_refs)


if __name__ == "__main__":
    unittest.main()
