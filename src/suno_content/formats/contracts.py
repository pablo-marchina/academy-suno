from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Any, ClassVar, Mapping, TypeAlias


class FormatContractError(ValueError):
    """Raised when a structured output violates its native format contract."""


class FormatKind(str, Enum):
    ARTICLE = "ARTICLE"
    CAROUSEL = "CAROUSEL"
    SHORT_VIDEO = "SHORT_VIDEO"


class CarouselRole(str, Enum):
    HOOK = "HOOK"
    BODY = "BODY"
    CONCLUSION = "CONCLUSION"


class VideoRole(str, Enum):
    HOOK = "HOOK"
    BODY = "BODY"
    CONCLUSION = "CONCLUSION"


def _require_text(value: object, *, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FormatContractError(f"{path} must be a non-empty string")
    return value.strip()


def _require_keys(
    payload: Mapping[str, Any],
    *,
    path: str,
    required: set[str],
    optional: set[str] | None = None,
) -> None:
    optional = optional or set()
    missing = required - payload.keys()
    unexpected = payload.keys() - required - optional
    if missing:
        raise FormatContractError(f"{path} is missing required keys: {sorted(missing)}")
    if unexpected:
        raise FormatContractError(f"{path} has unexpected keys: {sorted(unexpected)}")


@dataclass(frozen=True, slots=True)
class SourceRef:
    """Opaque provenance hook resolved by the factual/source domain layer.

    This slice deliberately owns only the reference shape used by format units.
    `source_id` and `anchor_id` are stable integration hooks; richer provenance can
    be added by the domain layer without coupling format validation to a parser.
    """

    source_id: str
    anchor_id: str
    span_id: str | None = None
    page: int | None = None
    claim_id: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.source_id, path="SourceRef.source_id")
        _require_text(self.anchor_id, path="SourceRef.anchor_id")
        if self.span_id is not None:
            _require_text(self.span_id, path="SourceRef.span_id")
        if self.claim_id is not None:
            _require_text(self.claim_id, path="SourceRef.claim_id")
        if self.page is not None and self.page < 1:
            raise FormatContractError("SourceRef.page must be >= 1 when provided")


@dataclass(frozen=True, slots=True)
class ArticleParagraph:
    text: str
    source_refs: tuple[SourceRef, ...]

    def __post_init__(self) -> None:
        _require_text(self.text, path="ArticleParagraph.text")


@dataclass(frozen=True, slots=True)
class ArticleSection:
    heading: str
    paragraphs: tuple[ArticleParagraph, ...]

    def __post_init__(self) -> None:
        _require_text(self.heading, path="ArticleSection.heading")
        if not self.paragraphs:
            raise FormatContractError("ArticleSection.paragraphs must not be empty")


@dataclass(frozen=True, slots=True)
class ArticleOutput:
    title: str
    lead_or_summary: str
    sections: tuple[ArticleSection, ...]
    closing_or_takeaways: str
    source_refs: tuple[SourceRef, ...] = ()

    format: ClassVar[FormatKind] = FormatKind.ARTICLE

    def __post_init__(self) -> None:
        _require_text(self.title, path="ArticleOutput.title")
        _require_text(self.lead_or_summary, path="ArticleOutput.lead_or_summary")
        _require_text(self.closing_or_takeaways, path="ArticleOutput.closing_or_takeaways")
        if not self.sections:
            raise FormatContractError("ArticleOutput.sections must not be empty")


@dataclass(frozen=True, slots=True)
class CarouselSlide:
    slide_index: int
    role: CarouselRole
    headline: str
    body: str
    visual_cue: str | None
    source_refs: tuple[SourceRef, ...]

    def __post_init__(self) -> None:
        if self.slide_index < 1:
            raise FormatContractError("CarouselSlide.slide_index must be >= 1")
        _require_text(self.headline, path="CarouselSlide.headline")
        _require_text(self.body, path="CarouselSlide.body")
        if self.visual_cue is not None:
            _require_text(self.visual_cue, path="CarouselSlide.visual_cue")


@dataclass(frozen=True, slots=True)
class CarouselOutput:
    slides: tuple[CarouselSlide, ...]

    format: ClassVar[FormatKind] = FormatKind.CAROUSEL

    def __post_init__(self) -> None:
        if len(self.slides) < 3:
            raise FormatContractError("CarouselOutput requires hook, body, and conclusion slides")
        expected_indexes = tuple(range(1, len(self.slides) + 1))
        observed_indexes = tuple(slide.slide_index for slide in self.slides)
        if observed_indexes != expected_indexes:
            raise FormatContractError("CarouselOutput slide_index values must be contiguous and start at 1")
        if self.slides[0].role is not CarouselRole.HOOK:
            raise FormatContractError("CarouselOutput first slide must have role HOOK")
        if self.slides[-1].role is not CarouselRole.CONCLUSION:
            raise FormatContractError("CarouselOutput last slide must have role CONCLUSION")
        if any(slide.role is not CarouselRole.BODY for slide in self.slides[1:-1]):
            raise FormatContractError("CarouselOutput middle slides must have role BODY")


@dataclass(frozen=True, slots=True)
class ShortVideoSegment:
    start_s: float
    end_s: float
    role: VideoRole
    narration: str
    on_screen_text: str | None
    visual_cue: str
    source_refs: tuple[SourceRef, ...]

    def __post_init__(self) -> None:
        if not isfinite(self.start_s) or not isfinite(self.end_s):
            raise FormatContractError("ShortVideoSegment timecodes must be finite")
        if self.start_s < 0 or self.end_s <= self.start_s:
            raise FormatContractError("ShortVideoSegment requires 0 <= start_s < end_s")
        _require_text(self.narration, path="ShortVideoSegment.narration")
        _require_text(self.visual_cue, path="ShortVideoSegment.visual_cue")
        if self.on_screen_text is not None:
            _require_text(self.on_screen_text, path="ShortVideoSegment.on_screen_text")


@dataclass(frozen=True, slots=True)
class ShortVideoOutput:
    segments: tuple[ShortVideoSegment, ...]
    estimated_spoken_duration_s: float

    format: ClassVar[FormatKind] = FormatKind.SHORT_VIDEO
    max_duration_s: ClassVar[float] = 60.0

    def __post_init__(self) -> None:
        if not self.segments:
            raise FormatContractError("ShortVideoOutput.segments must not be empty")
        if self.segments[0].role is not VideoRole.HOOK:
            raise FormatContractError("ShortVideoOutput first segment must have role HOOK")
        if not isfinite(self.estimated_spoken_duration_s) or self.estimated_spoken_duration_s <= 0:
            raise FormatContractError("ShortVideoOutput.estimated_spoken_duration_s must be > 0")
        if self.estimated_spoken_duration_s > self.max_duration_s:
            raise FormatContractError("ShortVideoOutput spoken duration must be <= 60 seconds")

        previous_end = -1.0
        for segment in self.segments:
            if segment.start_s < previous_end:
                raise FormatContractError("ShortVideoOutput timecodes must be monotonic and non-overlapping")
            previous_end = segment.end_s
        if self.segments[-1].end_s > self.max_duration_s:
            raise FormatContractError("ShortVideoOutput timeline must end at or before 60 seconds")


FormatOutput: TypeAlias = ArticleOutput | CarouselOutput | ShortVideoOutput


def _parse_source_ref(payload: object, *, path: str) -> SourceRef:
    if not isinstance(payload, Mapping):
        raise FormatContractError(f"{path} must be an object")
    _require_keys(
        payload,
        path=path,
        required={"source_id", "anchor_id"},
        optional={"span_id", "page", "claim_id"},
    )
    page = payload.get("page")
    if page is not None and (not isinstance(page, int) or isinstance(page, bool)):
        raise FormatContractError(f"{path}.page must be an integer when provided")
    return SourceRef(
        source_id=_require_text(payload["source_id"], path=f"{path}.source_id"),
        anchor_id=_require_text(payload["anchor_id"], path=f"{path}.anchor_id"),
        span_id=payload.get("span_id"),
        page=page,
        claim_id=payload.get("claim_id"),
    )


def _parse_source_refs(payload: object, *, path: str) -> tuple[SourceRef, ...]:
    if not isinstance(payload, (list, tuple)):
        raise FormatContractError(f"{path} must be an array")
    return tuple(_parse_source_ref(item, path=f"{path}[{index}]") for index, item in enumerate(payload))


def _parse_article(payload: Mapping[str, Any]) -> ArticleOutput:
    _require_keys(
        payload,
        path="ArticleOutput",
        required={"format", "title", "lead_or_summary", "sections", "closing_or_takeaways"},
        optional={"source_refs"},
    )
    raw_sections = payload["sections"]
    if not isinstance(raw_sections, (list, tuple)):
        raise FormatContractError("ArticleOutput.sections must be an array")
    sections: list[ArticleSection] = []
    for section_index, raw_section in enumerate(raw_sections):
        path = f"ArticleOutput.sections[{section_index}]"
        if not isinstance(raw_section, Mapping):
            raise FormatContractError(f"{path} must be an object")
        _require_keys(raw_section, path=path, required={"heading", "paragraphs"})
        raw_paragraphs = raw_section["paragraphs"]
        if not isinstance(raw_paragraphs, (list, tuple)):
            raise FormatContractError(f"{path}.paragraphs must be an array")
        paragraphs: list[ArticleParagraph] = []
        for paragraph_index, raw_paragraph in enumerate(raw_paragraphs):
            paragraph_path = f"{path}.paragraphs[{paragraph_index}]"
            if not isinstance(raw_paragraph, Mapping):
                raise FormatContractError(f"{paragraph_path} must be an object")
            _require_keys(raw_paragraph, path=paragraph_path, required={"text", "source_refs"})
            paragraphs.append(
                ArticleParagraph(
                    text=_require_text(raw_paragraph["text"], path=f"{paragraph_path}.text"),
                    source_refs=_parse_source_refs(
                        raw_paragraph["source_refs"], path=f"{paragraph_path}.source_refs"
                    ),
                )
            )
        sections.append(
            ArticleSection(
                heading=_require_text(raw_section["heading"], path=f"{path}.heading"),
                paragraphs=tuple(paragraphs),
            )
        )
    return ArticleOutput(
        title=_require_text(payload["title"], path="ArticleOutput.title"),
        lead_or_summary=_require_text(payload["lead_or_summary"], path="ArticleOutput.lead_or_summary"),
        sections=tuple(sections),
        closing_or_takeaways=_require_text(
            payload["closing_or_takeaways"], path="ArticleOutput.closing_or_takeaways"
        ),
        source_refs=_parse_source_refs(payload.get("source_refs", []), path="ArticleOutput.source_refs"),
    )


def _parse_carousel(payload: Mapping[str, Any]) -> CarouselOutput:
    _require_keys(payload, path="CarouselOutput", required={"format", "slides"})
    raw_slides = payload["slides"]
    if not isinstance(raw_slides, (list, tuple)):
        raise FormatContractError("CarouselOutput.slides must be an array")
    slides: list[CarouselSlide] = []
    for index, raw_slide in enumerate(raw_slides):
        path = f"CarouselOutput.slides[{index}]"
        if not isinstance(raw_slide, Mapping):
            raise FormatContractError(f"{path} must be an object")
        _require_keys(
            raw_slide,
            path=path,
            required={"slide_index", "role", "headline", "body", "visual_cue", "source_refs"},
        )
        slide_index = raw_slide["slide_index"]
        if not isinstance(slide_index, int) or isinstance(slide_index, bool):
            raise FormatContractError(f"{path}.slide_index must be an integer")
        try:
            role = CarouselRole(raw_slide["role"])
        except (TypeError, ValueError) as exc:
            raise FormatContractError(f"{path}.role is invalid") from exc
        visual_cue = raw_slide["visual_cue"]
        if visual_cue is not None and not isinstance(visual_cue, str):
            raise FormatContractError(f"{path}.visual_cue must be a string or null")
        slides.append(
            CarouselSlide(
                slide_index=slide_index,
                role=role,
                headline=_require_text(raw_slide["headline"], path=f"{path}.headline"),
                body=_require_text(raw_slide["body"], path=f"{path}.body"),
                visual_cue=visual_cue,
                source_refs=_parse_source_refs(raw_slide["source_refs"], path=f"{path}.source_refs"),
            )
        )
    return CarouselOutput(slides=tuple(slides))


def _parse_short_video(payload: Mapping[str, Any]) -> ShortVideoOutput:
    _require_keys(
        payload,
        path="ShortVideoOutput",
        required={"format", "segments", "estimated_spoken_duration_s"},
    )
    raw_segments = payload["segments"]
    if not isinstance(raw_segments, (list, tuple)):
        raise FormatContractError("ShortVideoOutput.segments must be an array")
    segments: list[ShortVideoSegment] = []
    for index, raw_segment in enumerate(raw_segments):
        path = f"ShortVideoOutput.segments[{index}]"
        if not isinstance(raw_segment, Mapping):
            raise FormatContractError(f"{path} must be an object")
        _require_keys(
            raw_segment,
            path=path,
            required={
                "start_s",
                "end_s",
                "role",
                "narration",
                "on_screen_text",
                "visual_cue",
                "source_refs",
            },
        )
        try:
            start_s = float(raw_segment["start_s"])
            end_s = float(raw_segment["end_s"])
        except (TypeError, ValueError) as exc:
            raise FormatContractError(f"{path} timecodes must be numeric") from exc
        try:
            role = VideoRole(raw_segment["role"])
        except (TypeError, ValueError) as exc:
            raise FormatContractError(f"{path}.role is invalid") from exc
        on_screen_text = raw_segment["on_screen_text"]
        if on_screen_text is not None and not isinstance(on_screen_text, str):
            raise FormatContractError(f"{path}.on_screen_text must be a string or null")
        segments.append(
            ShortVideoSegment(
                start_s=start_s,
                end_s=end_s,
                role=role,
                narration=_require_text(raw_segment["narration"], path=f"{path}.narration"),
                on_screen_text=on_screen_text,
                visual_cue=_require_text(raw_segment["visual_cue"], path=f"{path}.visual_cue"),
                source_refs=_parse_source_refs(raw_segment["source_refs"], path=f"{path}.source_refs"),
            )
        )
    try:
        estimated_duration = float(payload["estimated_spoken_duration_s"])
    except (TypeError, ValueError) as exc:
        raise FormatContractError("ShortVideoOutput.estimated_spoken_duration_s must be numeric") from exc
    return ShortVideoOutput(
        segments=tuple(segments),
        estimated_spoken_duration_s=estimated_duration,
    )


def parse_format_output(payload: Mapping[str, Any]) -> FormatOutput:
    """Parse a strict, discriminated structured-generation payload.

    Strict top-level and nested keys are intentional: an ARTICLE payload carrying
    `slides` or `segments` is rejected rather than silently accepted as another
    format. This is the anti-masquerading boundary for structured generation.
    """

    if not isinstance(payload, Mapping):
        raise FormatContractError("format output must be an object")
    raw_format = payload.get("format")
    try:
        format_kind = FormatKind(raw_format)
    except (TypeError, ValueError) as exc:
        raise FormatContractError("format output requires a valid format discriminator") from exc

    if format_kind is FormatKind.ARTICLE:
        return _parse_article(payload)
    if format_kind is FormatKind.CAROUSEL:
        return _parse_carousel(payload)
    return _parse_short_video(payload)
