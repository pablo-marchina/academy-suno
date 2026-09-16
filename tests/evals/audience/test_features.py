from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.domain import AudienceLevel, OutputFormat  # noqa: E402
from suno_content.evals.audience import (  # noqa: E402
    THRESHOLD_MODE,
    AudienceComplexityVector,
    evaluate_audience_features,
    load_ontology,
)


class AudienceFeatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ontology = load_ontology(ROOT / "data" / "ontology" / "finance_ptbr_v001.json")

    def evaluate(self, text: str, required=()):
        return evaluate_audience_features(
            text,
            audience=AudienceLevel.BEGINNER,
            output_format=OutputFormat.ARTICLE,
            ontology=self.ontology,
            required_concept_ids=required,
        )

    def test_vector_has_no_unvalidated_scalar_score(self) -> None:
        fields = set(AudienceComplexityVector.model_fields)
        self.assertNotIn("score", fields)
        self.assertNotIn("overall_score", fields)
        vector = self.evaluate("O IPCA é o índice que acompanha preços ao consumidor.")
        self.assertEqual(vector.threshold_mode, THRESHOLD_MODE)

    def test_contextualization_reduces_unexplained_jargon(self) -> None:
        unexplained = self.evaluate("O EBITDA subiu no trimestre.")
        explained = self.evaluate(
            "O EBITDA é uma medida do resultado operacional antes de juros, impostos, depreciação e amortização. "
            "Na prática, ele ajuda a observar a operação antes desses efeitos."
        )
        self.assertEqual(unexplained.terminology.unexplained_jargon_rate, 1.0)
        self.assertEqual(explained.terminology.unexplained_jargon_rate, 0.0)
        self.assertGreater(explained.terminology.contextualization_rate, 0.0)

    def test_jargon_repetition_inflates_raw_but_not_unique_weighted_density(self) -> None:
        clean = self.evaluate("O EBITDA cresceu, mas precisa ser interpretado com cautela.")
        stuffed = self.evaluate("EBITDA EBITDA EBITDA EBITDA EBITDA cresceu.")
        self.assertGreater(
            stuffed.terminology.raw_term_density_per_100_words,
            clean.terminology.raw_term_density_per_100_words,
        )
        self.assertTrue(stuffed.anti_gaming.jargon_stuffing)
        self.assertGreater(stuffed.anti_gaming.repetition_ratio, 0.5)
        self.assertLess(
            stuffed.terminology.difficulty_weighted_density_per_100_words,
            stuffed.terminology.raw_term_density_per_100_words,
        )

    def test_alias_stuffing_is_visible(self) -> None:
        vector = self.evaluate("EBITDA, LAJIDA, EBITDA e LAJIDA aparecem na mesma lista.")
        self.assertTrue(vector.anti_gaming.alias_stuffing)
        self.assertEqual(vector.terminology.detected_concepts, ("corp:ebitda",))

    def test_required_concept_recall_blocks_readability_gaming_diagnostic(self) -> None:
        complete = self.evaluate(
            "O hiato do produto compara a atividade atual com uma estimativa de potencial. "
            "Pense como a folga de uma fábrica: capacidade ociosa sugere espaço antes de nova pressão.",
            required=("macro:output_gap",),
        )
        removed = self.evaluate(
            "A economia está mais calma. Há espaço para crescer. Os preços podem reagir depois.",
            required=("macro:output_gap",),
        )
        self.assertEqual(complete.terminology.required_concept_recall, 1.0)
        self.assertEqual(removed.terminology.required_concept_recall, 0.0)
        self.assertTrue(removed.anti_gaming.required_concept_omission)
        self.assertIn("REQUIRED_CONCEPT_OMISSION", removed.anti_gaming.flags)
        self.assertGreater(removed.readability.flesch_raw, complete.readability.flesch_raw)

    def test_sentence_chopping_does_not_hide_as_readability_gain(self) -> None:
        vector = self.evaluate("Juros. Caem. Preços. Sobem. Crédito. Muda.")
        self.assertTrue(vector.anti_gaming.sentence_chopping)
        self.assertIn("SENTENCE_CHOPPING", vector.anti_gaming.flags)

    def test_acronym_hack_is_diagnostic(self) -> None:
        vector = self.evaluate("IPCA, EBITDA, CAPEX, EBITDA.")
        self.assertTrue(vector.anti_gaming.acronym_hack)
        self.assertIn("ACRONYM_HACK", vector.anti_gaming.flags)


if __name__ == "__main__":
    unittest.main()
