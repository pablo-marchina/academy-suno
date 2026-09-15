from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Mapping, Protocol, runtime_checkable

from suno_content.domain import AudienceLevel, OutputFormat, SourceProvenance, VariantSpec
from suno_content.formats import FormatContractError, FormatOutput, parse_format_output


class GenerationContractError(ValueError):
    """Raised when generation input/output violates the provider-neutral contract."""


@dataclass(frozen=True, slots=True)
class AudienceContract:
    """Audience intent kept separate from the media-format contract."""

    level: AudienceLevel
    contract_version: str
    rule_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.level, AudienceLevel):
            raise GenerationContractError("AudienceContract.level must be a canonical AudienceLevel")
        if not self.contract_version.strip():
            raise GenerationContractError("AudienceContract.contract_version must not be empty")
        if any(not ref.strip() for ref in self.rule_refs):
            raise GenerationContractError("AudienceContract.rule_refs cannot contain empty refs")


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    """Execution request around the canonical VariantSpec.

    Provider/model identity is intentionally absent; adapters/config own that choice.
    """

    variant: VariantSpec
    audience_contract: AudienceContract

    def __post_init__(self) -> None:
        if self.variant.audience != self.audience_contract.level:
            raise GenerationContractError(
                "GenerationRequest audience contract must match VariantSpec.audience"
            )

    @property
    def job_id(self) -> str:
        return self.variant.job_id

    @property
    def format(self) -> OutputFormat:
        return self.variant.format

    @property
    def source_backbone_ref(self) -> str:
        return self.variant.source_backbone_ref

    @property
    def policy_context_ref(self) -> str:
        return self.variant.policy_context_ref

    @property
    def prompt_version(self) -> str:
        return self.variant.prompt_version

    @property
    def schema_version(self) -> str:
        return self.variant.output_schema_version


_AUDIENCE_ORDER = (
    AudienceLevel.BEGINNER,
    AudienceLevel.INTERMEDIATE,
    AudienceLevel.ADVANCED,
)
_FORMAT_ORDER = (
    OutputFormat.ARTICLE,
    OutputFormat.CAROUSEL,
    OutputFormat.SHORT_VIDEO,
)


def _require_non_empty(value: str, *, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GenerationContractError(f"{name} must not be empty")
    return value.strip()


def _job_id(
    *,
    source: SourceProvenance,
    audience: AudienceLevel,
    output_format: OutputFormat,
    prompt_version: str,
    output_schema_version: str,
    source_backbone_ref: str,
    policy_context_ref: str,
) -> str:
    seed = "\x1f".join(
        (
            "variant_spec.v1",
            source.source_id,
            source.source_hash,
            audience.value,
            output_format.value,
            prompt_version,
            output_schema_version,
            source_backbone_ref,
            policy_context_ref,
        )
    )
    digest = sha256(seed.encode("utf-8")).hexdigest()[:20]
    format_slug = output_format.value.lower().replace("_", "-")
    return f"job-{audience.value.lower()}-{format_slug}-{digest}"


def build_3x3_variant_specs(
    *,
    source: SourceProvenance,
    source_backbone_ref: str,
    policy_context_ref: str,
    prompt_version: str,
    output_schema_version: str,
) -> tuple[VariantSpec, ...]:
    """Create exactly nine deterministic canonical jobs for 3 audiences × 3 formats."""

    source_backbone_ref = _require_non_empty(source_backbone_ref, name="source_backbone_ref")
    policy_context_ref = _require_non_empty(policy_context_ref, name="policy_context_ref")
    prompt_version = _require_non_empty(prompt_version, name="prompt_version")
    output_schema_version = _require_non_empty(
        output_schema_version, name="output_schema_version"
    )

    specs = tuple(
        VariantSpec(
            job_id=_job_id(
                source=source,
                audience=audience,
                output_format=output_format,
                prompt_version=prompt_version,
                output_schema_version=output_schema_version,
                source_backbone_ref=source_backbone_ref,
                policy_context_ref=policy_context_ref,
            ),
            audience=audience,
            format=output_format,
            prompt_version=prompt_version,
            output_schema_version=output_schema_version,
            source=source,
            source_backbone_ref=source_backbone_ref,
            policy_context_ref=policy_context_ref,
        )
        for audience in _AUDIENCE_ORDER
        for output_format in _FORMAT_ORDER
    )
    if len(specs) != 9 or len({spec.job_id for spec in specs}) != 9:
        raise GenerationContractError("3x3 planning must produce exactly nine unique jobs")
    return specs


@runtime_checkable
class StructuredGenerator(Protocol):
    """Provider/model-neutral structured-generation boundary."""

    def generate(self, request: GenerationRequest) -> Mapping[str, Any]:
        ...


def validate_output_matches_request(
    request: GenerationRequest,
    output: FormatOutput,
) -> FormatOutput:
    if output.format is not request.format:
        raise GenerationContractError(
            f"requested {request.format.value} but received {output.format.value}"
        )
    return output


def decode_generation_payload(
    request: GenerationRequest,
    payload: Mapping[str, Any],
) -> FormatOutput:
    try:
        output = parse_format_output(payload)
    except FormatContractError as exc:
        raise GenerationContractError(str(exc)) from exc
    return validate_output_matches_request(request, output)
