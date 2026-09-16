from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.domain import OutputFormat  # noqa: E402
from suno_content.evals.audience import READABILITY_VERSION, evaluate_readability  # noqa: E402


class PtBrReadabilityTests(unittest.TestCase):
    def test_versioned_result_and_simple_text_is_easier(self) -> None:
        simple = "Os preços subiram. O crédito ficou caro. A renda perdeu força."
        complex_text = (
            "A persistência inflacionária observada na composição setorial, combinada à transmissão "
            "defasada das condições financeiras, amplia a incerteza sobre a convergência das expectativas."
        )
        simple_result = evaluate_readability(simple, OutputFormat.ARTICLE)
        complex_result = evaluate_readability(complex_text, OutputFormat.ARTICLE)
        self.assertEqual(simple_result.version, READABILITY_VERSION)
        self.assertTrue(simple_result.valid)
        self.assertTrue(complex_result.valid)
        self.assertGreater(simple_result.flesch_raw, complex_result.flesch_raw)

    def test_structural_metadata_does_not_become_words(self) -> None:
        with_labels = "Slide 1: A inflação caiu.\nSlide 2: O crédito desacelerou."
        clean = "A inflação caiu.\nO crédito desacelerou."
        labelled = evaluate_readability(with_labels, OutputFormat.CAROUSEL)
        baseline = evaluate_readability(clean, OutputFormat.CAROUSEL)
        self.assertEqual(labelled.word_count, baseline.word_count)
        self.assertEqual(labelled.flesch_raw, baseline.flesch_raw)

    def test_unknown_acronym_reduces_coverage_instead_of_fake_one_syllable(self) -> None:
        text = "XYZQ orienta a decisão. XYZQ muda o cenário."
        result = evaluate_readability(text, OutputFormat.ARTICLE)
        self.assertIn("XYZQ", result.unsupported_tokens)
        self.assertLess(result.syllable_coverage, 1.0)


if __name__ == "__main__":
    unittest.main()
