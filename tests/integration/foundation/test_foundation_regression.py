from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.domain import (  # noqa: E402
    Anchor,
    AnchorKind,
    AudienceLevel,
    BusinessContext,
    ContentType,
    EvalStatus,
    GateStatus,
    Materiality,
    OutputFormat,
    ParsedDocument,
    SourceArtifact,
    SourceSpan,
    SourceTrust,
    SourceType,
)
from suno_content.factual import build_factual_backbone  # noqa: E402
from suno_content.formats import (  # noqa: E402
    ArticleOutput,
    ArticleParagraph,
    ArticleSection,
    SourceRef,
)
from suno_content.generation.contracts import (  # noqa: E402
    AudienceContract,
    GenerationRequest,
    build_3x3_variant_specs,
    validate_output_matches_request,
)
from suno_content.policy import (  # noqa: E402
    PolicyContext,
    PolicyRequest,
    evaluate_policy,
)


class FoundationCrossPackageRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = SourceArtifact(
            source_id="foundation-source-001",
            source_uri="https://example.invalid/foundation-source",
            source_hash="a" * 64,
            source_title="Foundation clean-checkout fixture",
            source_publisher="Academy Suno regression",
            source_type=SourceType.OTHER,
            content_type=ContentType.EDUCATIONAL,
            business_context=BusinessContext.EDUCATION,
            public_source_verified=True,
            raw_artifact_ref="raw/foundation-source.txt",
        )
        self.provenance = self.source.provenance()
        self.span = SourceSpan(
            span_id="span-revenue",
            source=self.provenance,
            text="A companhia informou receita de R$ 10 bilhões no período.",
            page_number=1,
            section="resultado",
        )
        self.document = ParsedDocument(
            document_id="doc-foundation-001",
            source=self.provenance,
            parser_version="foundation-fixture-v1",
            spans=(self.span,),
            coverage_metadata={"source_trust_status": "PASS"},
        )
        self.anchor = Anchor(
            anchor_id="anchor-revenue",
            kind=AnchorKind.NUMBER,
            normalized_value=10,
            surface_value="10",
            semantic_role="receita_bilhoes_brl",
            provenance=(self.span.provenance_ref(),),
            source_trust=SourceTrust.HIGH,
            materiality=Materiality.MATERIAL,
        )

    def test_one_canonical_source_composes_across_foundation_packages(self) -> None:
        backbone = build_factual_backbone(self.document, (self.anchor,))
        self.assertEqual(backbone.source_trust_status, GateStatus.PASS)
        self.assertEqual(backbone.source, self.provenance)
        self.assertEqual(backbone.anchors, (self.anchor,))

        policy_context = PolicyContext(
            source=self.source,
            policy_version="policy-foundation-v1",
        )
        policy_result = evaluate_policy(
            PolicyRequest(
                source_text=self.span.text,
                output_text="A companhia informou receita de R$ 10 bilhões no período.",
                context=policy_context,
            )
        )
        self.assertEqual(policy_result.decision, EvalStatus.PASS)
        self.assertEqual(policy_result.provenance, self.provenance)

        variants = build_3x3_variant_specs(
            source=self.provenance,
            source_backbone_ref="backbone/foundation-source-001/v1",
            policy_context_ref="policy/foundation-source-001/v1",
            prompt_version="prompt-foundation-v1",
            output_schema_version="format-native-v1",
        )
        self.assertEqual(len(variants), 9)
        self.assertEqual(len({variant.job_id for variant in variants}), 9)
        self.assertEqual(
            {(variant.audience, variant.format) for variant in variants},
            {(audience, fmt) for audience in AudienceLevel for fmt in OutputFormat},
        )
        self.assertTrue(all(variant.source == self.provenance for variant in variants))

        article_variant = next(
            variant
            for variant in variants
            if variant.audience is AudienceLevel.BEGINNER
            and variant.format is OutputFormat.ARTICLE
        )
        request = GenerationRequest(
            variant=article_variant,
            audience_contract=AudienceContract(
                level=AudienceLevel.BEGINNER,
                contract_version="audience-foundation-v1",
                rule_refs=("foundation-regression",),
            ),
        )
        source_ref = SourceRef(
            anchor_id=self.anchor.anchor_id,
            provenance=self.anchor.provenance[0],
        )
        article = ArticleOutput(
            title="Receita no período",
            lead_or_summary="Resumo estritamente derivado da fonte.",
            sections=(
                ArticleSection(
                    heading="Dado principal",
                    paragraphs=(
                        ArticleParagraph(
                            text="A companhia informou receita de R$ 10 bilhões.",
                            source_refs=(source_ref,),
                        ),
                    ),
                ),
            ),
            closing_or_takeaways="O valor permanece ligado ao mesmo trecho de origem.",
        )
        validated = validate_output_matches_request(request, article)
        self.assertIs(validated, article)
        self.assertEqual(
            article.sections[0].paragraphs[0].source_refs[0].provenance,
            self.span.provenance_ref(),
        )

    def test_policy_hard_fail_remains_non_compensatory_in_combined_checkout(self) -> None:
        result = evaluate_policy(
            PolicyRequest(
                source_text=self.span.text,
                output_text=(
                    "Isto não é recomendação. Se você é investidor conservador, compre X."
                ),
                context=PolicyContext(
                    source=self.source,
                    policy_version="policy-foundation-v1",
                ),
            )
        )
        self.assertEqual(result.decision, EvalStatus.FAIL)
        self.assertTrue(result.detected_disclaimer)
        self.assertIn("HF-02", result.codes)


if __name__ == "__main__":
    unittest.main()
