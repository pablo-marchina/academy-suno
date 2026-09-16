from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.evals.audience import OntologyMatcher, load_ontology  # noqa: E402


class OntologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ontology = load_ontology(ROOT / "data" / "ontology" / "finance_ptbr_v001.json")
        cls.matcher = OntologyMatcher(cls.ontology)

    def test_aliases_collapse_to_same_concept(self) -> None:
        mentions = self.matcher.match("O EBITDA melhorou. O LAJIDA também foi divulgado.")
        self.assertEqual({m.concept_id for m in mentions}, {"corp:ebitda"})

    def test_longest_match_preserves_adjusted_ebitda_as_distinct_concept(self) -> None:
        mentions = self.matcher.match("O EBITDA ajustado cresceu no trimestre.")
        self.assertEqual([m.concept_id for m in mentions], ["corp:adjusted_ebitda"])

    def test_context_rule_blocks_non_financial_duration_translation(self) -> None:
        no_match = self.matcher.match("A duração financeira do vídeo é de dois minutos.")
        match = self.matcher.match("A duração financeira do título aumenta o risco de juros da carteira.")
        self.assertNotIn("market:duration", {m.concept_id for m in no_match})
        self.assertIn("market:duration", {m.concept_id for m in match})


if __name__ == "__main__":
    unittest.main()
