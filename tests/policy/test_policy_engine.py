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
    BusinessContext,
    ContentType,
    PolicyContext,
    PolicyDecision,
    PolicyRequest,
    PolicySignals,
    RecommendationProvenance,
    SourceArtifact,
    SourceType,
    evaluate_policy,
)

FIXTURE_PATH = ROOT / "tests" / "fixtures" / "policy" / "adversarial_cases.json"
POLICY_VERSION = "b04.policy-engine.v2"
SOURCE_HASH = "a" * 64


def _context_from_case(case: dict) -> PolicyContext:
    context_data = dict(case.get("context", {}))
    source = SourceArtifact(
        source_id=f"fixture:{case['id']}",
        source_hash=SOURCE_HASH,
        source_type=SourceType(context_data.pop("source_type", "UNKNOWN")),
        content_type=ContentType(context_data.pop("content_type", "UNKNOWN")),
        business_context=BusinessContext(context_data.pop("business_context", "UNKNOWN")),
        public_source_verified=context_data.pop("public_source_verified", True),
        raw_artifact_ref=f"tests/fixtures/policy/{case['id']}.txt",
    )
    return PolicyContext(source=source, policy_version=POLICY_VERSION, **context_data)


def _request_from_case(case: dict) -> PolicyRequest:
    signal_data = dict(case.get("signals", {}))
    if "recommendation_provenance" in signal_data:
        signal_data["recommendation_provenance"] = RecommendationProvenance(
            signal_data["recommendation_provenance"]
        )
    return PolicyRequest(
        source_text=case["source_text"],
        output_text=case["output_text"],
        context=_context_from_case(case),
        signals=PolicySignals(**signal_data),
    )


def _direct_context(
    *,
    source_type: SourceType,
    content_type: ContentType = ContentType.NEWS,
    business_context: BusinessContext = BusinessContext.EDITORIAL,
    public_source_verified: bool = True,
) -> PolicyContext:
    source = SourceArtifact(
        source_id="direct:test",
        source_hash="b" * 64,
        source_type=source_type,
        content_type=content_type,
        business_context=business_context,
        public_source_verified=public_source_verified,
        raw_artifact_ref="memory://direct-test",
    )
    return PolicyContext(source=source, policy_version=POLICY_VERSION)


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
            context=_direct_context(source_type=SourceType.OTHER),
            signals=PolicySignals(external_context_added=True),
        )
        result = evaluate_policy(request)
        self.assertEqual(result.decision, PolicyDecision.REVIEW_REQUIRED)
        self.assertTrue(result.has("HR-06"))

    def test_low_confidence_source_routes_to_review(self) -> None:
        request = PolicyRequest(
            source_text="Trecho extraído com baixa confiança.",
            output_text="Resumo fiel do trecho.",
            context=_direct_context(source_type=SourceType.OTHER),
            signals=PolicySignals(low_confidence_source=True),
        )
        result = evaluate_policy(request)
        self.assertEqual(result.decision, PolicyDecision.REVIEW_REQUIRED)
        self.assertTrue(result.has("HR-04"))

    def test_unverified_public_source_is_hard_fail(self) -> None:
        request = PolicyRequest(
            source_text="Fonte não verificada.",
            output_text="Resumo.",
            context=_direct_context(source_type=SourceType.OTHER, public_source_verified=False),
        )
        result = evaluate_policy(request)
        self.assertEqual(result.decision, PolicyDecision.FAIL)
        self.assertTrue(result.has("HF-06"))

    def test_policy_contract_carries_canonical_source_provenance_and_version(self) -> None:
        case = next(c for c in self.cases if c["id"] == "new-recommendation-from-policy-news")
        request = _request_from_case(case)
        result = evaluate_policy(request)
        self.assertIsInstance(request.context.source.source_type, SourceType)
        self.assertIsInstance(request.context.source.content_type, ContentType)
        self.assertIsInstance(request.context.source.business_context, BusinessContext)
        self.assertEqual(result.policy_version, POLICY_VERSION)
        self.assertEqual(result.provenance, request.context.provenance)
        self.assertEqual(result.source.source_id, f"fixture:{case['id']}")
        self.assertEqual(result.canonical_sha256(), evaluate_policy(request).canonical_sha256())

    def test_hf11_remains_dedicated_non_compensatory_hard_fail(self) -> None:
        case = next(c for c in self.cases if c["id"] == "source-mixing-without-claim-lineage")
        result = evaluate_policy(_request_from_case(case))
        self.assertEqual(result.decision, PolicyDecision.FAIL)
        self.assertEqual(result.codes, ("HF-11",))


if __name__ == "__main__":
    unittest.main()
