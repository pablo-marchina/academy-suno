from __future__ import annotations

import sys
import unittest
from dataclasses import fields
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.formats import (  # noqa: E402
    CarouselRole,
    FormatContractError,
    FormatKind,
    ShortVideoOutput,
    VideoRole,
    parse_format_output,
)
from suno_content.generation.contracts import (  # noqa: E402
    AudienceContract,
    AudienceLevel,
    GenerationContractError,
    GenerationRequest,
    decode_generation_payload,
)


def source_ref(anchor_id: str) -> dict[str, object]:
    return {
        "source_id": "source-001",
        "anchor_id": anchor_id,
        "span_id": f"span-{anchor_id}",
        "page": 1,
        "claim_id": f"claim-{anchor_id}",
    }


def article_payload() -> dict[str, object]:
    return {
        "format": "ARTICLE",
        "title": "Juros e renda fixa",
        "lead_or_summary": "O movimento da taxa altera o contexto de retorno e risco.",
        "sections": [
            {
                "heading": "O que mudou",
                "paragraphs": [
                    {
                        "text": "A taxa de referência mudou no período analisado.",
                        "source_refs": [source_ref("a-001")],
                    }
                ],
            }
        ],
        "closing_or_takeaways": "A leitura deve preservar o contexto e as ressalvas da fonte.",
        "source_refs": [source_ref("a-001")],
    }


def carousel_payload() -> dict[str, object]:
    return {
        "format": "CAROUSEL",
        "slides": [
            {
                "slide_index": 1,
                "role": "HOOK",
                "headline": "O que mudou nos juros?",
                "body": "Comece pelo fato central.",
                "visual_cue": "Número principal em destaque",
                "source_refs": [source_ref("a-001")],
            },
            {
                "slide_index": 2,
                "role": "BODY",
                "headline": "Por que importa",
                "body": "Explique a implicação sem criar recomendação nova.",
                "visual_cue": None,
                "source_refs": [source_ref("a-002")],
            },
            {
                "slide_index": 3,
                "role": "CONCLUSION",
                "headline": "Leitura final",
                "body": "Feche preservando limites e contexto.",
                "visual_cue": "Resumo visual dos pontos",
                "source_refs": [source_ref("a-003")],
            },
        ],
    }


def short_video_payload() -> dict[str, object]:
    return {
        "format": "SHORT_VIDEO",
        "segments": [
            {
                "start_s": 0,
                "end_s": 4,
                "role": "HOOK",
                "narration": "Os juros mudaram. O que isso significa?",
                "on_screen_text": "Juros: o que mudou?",
                "visual_cue": "Abrir com a taxa em tela",
                "source_refs": [source_ref("a-001")],
            },
            {
                "start_s": 4,
                "end_s": 42,
                "role": "BODY",
                "narration": "Explique o fato e a implicação suportada pela fonte.",
                "on_screen_text": None,
                "visual_cue": "Gráfico simples com período destacado",
                "source_refs": [source_ref("a-002")],
            },
            {
                "start_s": 42,
                "end_s": 55,
                "role": "CONCLUSION",
                "narration": "Feche com a ressalva material da fonte.",
                "on_screen_text": "Contexto importa",
                "visual_cue": "Retomar fonte e ressalva",
                "source_refs": [source_ref("a-003")],
            },
        ],
        "estimated_spoken_duration_s": 51,
    }


class FormatContractTests(unittest.TestCase):
    def test_article_has_unit_level_source_refs(self) -> None:
        output = parse_format_output(article_payload())
        paragraph = output.sections[0].paragraphs[0]
        self.assertEqual(output.format, FormatKind.ARTICLE)
        self.assertEqual(paragraph.source_refs[0].anchor_id, "a-001")
        self.assertEqual(paragraph.source_refs[0].claim_id, "claim-a-001")

    def test_article_rejects_carousel_masquerade(self) -> None:
        payload = article_payload()
        payload["slides"] = carousel_payload()["slides"]
        with self.assertRaisesRegex(FormatContractError, "unexpected keys"):
            parse_format_output(payload)

    def test_article_rejects_video_masquerade(self) -> None:
        payload = article_payload()
        payload["segments"] = short_video_payload()["segments"]
        with self.assertRaisesRegex(FormatContractError, "unexpected keys"):
            parse_format_output(payload)

    def test_carousel_requires_hook_body_conclusion_in_order(self) -> None:
        output = parse_format_output(carousel_payload())
        self.assertEqual(output.slides[0].role, CarouselRole.HOOK)
        self.assertEqual(output.slides[1].role, CarouselRole.BODY)
        self.assertEqual(output.slides[-1].role, CarouselRole.CONCLUSION)

        invalid = carousel_payload()
        invalid["slides"][0]["role"] = "BODY"  # type: ignore[index]
        with self.assertRaisesRegex(FormatContractError, "first slide"):
            parse_format_output(invalid)

    def test_carousel_requires_all_three_structural_roles(self) -> None:
        invalid = carousel_payload()
        invalid["slides"] = invalid["slides"][:2]  # type: ignore[index]
        with self.assertRaisesRegex(FormatContractError, "hook, body, and conclusion"):
            parse_format_output(invalid)

    def test_short_video_requires_timecodes_visual_cues_and_under_60_seconds(self) -> None:
        output = parse_format_output(short_video_payload())
        self.assertIsInstance(output, ShortVideoOutput)
        self.assertEqual(output.segments[0].role, VideoRole.HOOK)
        self.assertLessEqual(output.segments[-1].end_s, 60)
        self.assertLessEqual(output.estimated_spoken_duration_s, 60)

        overlong = short_video_payload()
        overlong["segments"][-1]["end_s"] = 61  # type: ignore[index]
        with self.assertRaisesRegex(FormatContractError, "at or before 60"):
            parse_format_output(overlong)

        missing_visual = short_video_payload()
        del missing_visual["segments"][1]["visual_cue"]  # type: ignore[index]
        with self.assertRaisesRegex(FormatContractError, "missing required keys"):
            parse_format_output(missing_visual)

    def test_short_video_rejects_overlapping_timecodes(self) -> None:
        invalid = short_video_payload()
        invalid["segments"][1]["start_s"] = 3  # type: ignore[index]
        with self.assertRaisesRegex(FormatContractError, "monotonic and non-overlapping"):
            parse_format_output(invalid)


class GenerationContractTests(unittest.TestCase):
    def make_request(self, format_kind: FormatKind) -> GenerationRequest:
        return GenerationRequest(
            job_id="job-001",
            audience_contract=AudienceContract(
                level=AudienceLevel.BEGINNER,
                contract_version="audience-v1",
                rule_refs=("REQ-004",),
            ),
            format=format_kind,
            source_backbone_ref="backbone-001",
            policy_context_ref="policy-001",
            prompt_version="prompt-v1",
            schema_version="format-v1",
        )

    def test_audience_contract_is_separate_from_format_contract(self) -> None:
        audience_fields = {field.name for field in fields(AudienceContract)}
        request_fields = {field.name for field in fields(GenerationRequest)}
        self.assertNotIn("format", audience_fields)
        self.assertIn("audience_contract", request_fields)
        self.assertIn("format", request_fields)

    def test_generation_contract_does_not_select_provider_or_model(self) -> None:
        request_fields = {field.name for field in fields(GenerationRequest)}
        self.assertNotIn("provider", request_fields)
        self.assertNotIn("model", request_fields)

    def test_generation_request_rejects_wrong_native_format(self) -> None:
        request = self.make_request(FormatKind.ARTICLE)
        with self.assertRaisesRegex(GenerationContractError, "requested ARTICLE"):
            decode_generation_payload(request, carousel_payload())

    def test_generation_request_accepts_matching_native_format(self) -> None:
        request = self.make_request(FormatKind.SHORT_VIDEO)
        output = decode_generation_payload(request, short_video_payload())
        self.assertEqual(output.format, FormatKind.SHORT_VIDEO)


if __name__ == "__main__":
    unittest.main()
