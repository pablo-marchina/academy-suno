from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from suno_content.formats import FormatContractError, FormatKind, FormatOutput, parse_format_output


class GenerationContractError(ValueError):
    """Raised when generation input/output violates the provider-neutral contract."""


class AudienceLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


@dataclass(frozen=True, slots=True)
class AudienceContract:
    """Audience intent kept explicitly separate from the media format contract.

    Thresholds and evaluator details are intentionally referenced rather than
    frozen here; later calibration can evolve them without changing format shape.
    """

    level: AudienceLevel
    contract_version: str
    rule_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.contract_version.strip():
            raise GenerationContractError("AudienceContract.contract_version must not be empty")
        if any(not ref.strip() for ref in self.rule_refs):
            raise GenerationContractError("AudienceContract.rule_refs cannot contain empty refs")


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    job_id: str
    audience_contract: AudienceContract
    format: FormatKind
    source_backbone_ref: str
    policy_context_ref: str
    prompt_version: str
    schema_version: str

    def __post_init__(self) -> None:
        for field_name in (
            "job_id",
            "source_backbone_ref",
            "policy_context_ref",
            "prompt_version",
            "schema_version",
        ):
            if not getattr(self, field_name).strip():
                raise GenerationContractError(f"GenerationRequest.{field_name} must not be empty")


@runtime_checkable
class StructuredGenerator(Protocol):
    """Provider/model-neutral structured-generation boundary."""

    def generate(self, request: GenerationRequest) -> Mapping[str, Any]:
        """Return a JSON-like payload conforming to the requested format schema."""
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
    """Strictly decode provider output and enforce request/format agreement."""

    try:
        output = parse_format_output(payload)
    except FormatContractError as exc:
        raise GenerationContractError(str(exc)) from exc
    return validate_output_matches_request(request, output)
