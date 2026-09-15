from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from suno_content.policy import (  # noqa: E402
    PolicyContext,
    PolicyDecision,
    PolicyRequest,
    PolicySignals,
    RecommendationProvenance,
    SourceType,
    evaluate_policy,
)

FIXTURE_PATH = ROOT / "tests" / "fixtures" / "policy" / "adversarial_cases.json"


def _request_from_case(case: dict) -> PolicyRequest:
    context_data = dict(case.get("context", {}))
    context_data["source_type"] = SourceType(context_data.get("source_type", "UNKNOWN_OTHER"))
    signal_data = dict(case.get("signals", {}))
    if "recommendation_provenance" in signal_data:
        signal_data["recommendation_provenance"] = RecommendationProvenance(
            signal_data["recommendation_provenance"]
        )
    return PolicyRequest(
        source_text=case["source_text"],
        output_text=case["output_text"],
        context=PolicyContext(**context_data),
        signals=PolicySignals(**signal_data),
    )


class PolicyAdversarialFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_all_adversarial_cases(self) -> None:
        for case in self.cases:
            with self.subTest(case=case["id"]):
                result = evaluate_policy(_request_from_case(case))
                self.assertEqual(result.decision.value, case["expected_decision"])
                self.assertEqual(set(result.codes), set(case["expected_codes"]))

    def test_disclaimer_never_overrides_personalized_fail(self) -> None:
        case = next(c for c in self.cases if c["id"] == "personalized-advice-with-disclaimer")
        result = evaluate_policy(_request_from_case(case))
        self.assertTrue(result.detected_disclaimer)
        self.assertEqual(result.decision, PolicyDecision.FAIL)
        self.assertTrue(result.has("HF-02"))

    def test_review_is_first_class_but_never_compensates_hard_fail(self) -> None:
        case = next(c for c in self.cases if c["id"] == "review-plus-fail-remains-fail")
        result = evaluate_policy(_request_from_case(case))
        self.assertEqual(result.decision, PolicyDecision.FAIL)
        self.assertTrue(result.has("HR-01"))
        self.assertTrue(result.has("HF-10"))

    def test_unknown_internal_policy_is_not_invented_for_safe_content(self) -> None:
        case = next(c for c in self.cases if c["id"] == "safe-educational-unknown-internal-policy")
        result = evaluate_policy(_request_from_case(case))
        self.assertEqual(result.decision, PolicyDecision.PASS)
        self.assertEqual(result.codes, ())

    def test_external_context_routes_to_review(self) -> None:
        request = PolicyRequest(
            source_text="A fonte descreve o evento.",
            output_text="O evento é descrito, com contexto externo adicional.",
            context=PolicyContext(source_type=SourceType.NEWS_EDITORIAL, business_context="EDITORIAL"),
            signals=PolicySignals(external_context_added=True),
        )
        result = evaluate_policy(request)
        self.assertEqual(result.decision, PolicyDecision.REVIEW_REQUIRED)
        self.assertTrue(result.has("HR-06"))

    def test_low_confidence_source_routes_to_review(self) -> None:
        request = PolicyRequest(
            source_text="Trecho extraído com baixa confiança.",
            output_text="Resumo fiel do trecho.",
            context=PolicyContext(source_type=SourceType.NEWS_EDITORIAL, business_context="EDITORIAL"),
            signals=PolicySignals(low_confidence_source=True),
        )
        result = evaluate_policy(request)
        self.assertEqual(result.decision, PolicyDecision.REVIEW_REQUIRED)
        self.assertTrue(result.has("HR-04"))

    def test_unverified_public_source_is_hard_fail(self) -> None:
        request = PolicyRequest(
            source_text="Fonte não verificada.",
            output_text="Resumo.",
            context=PolicyContext(
                source_type=SourceType.NEWS_EDITORIAL,
                business_context="EDITORIAL",
                public_source_verified=False,
            ),
        )
        result = evaluate_policy(request)
        self.assertEqual(result.decision, PolicyDecision.FAIL)
        self.assertTrue(result.has("HF-06"))


if __name__ == "__main__":
    unittest.main()
