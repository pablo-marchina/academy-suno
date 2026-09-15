from __future__ import annotations

from typing import Annotated, Iterable, Literal

from pydantic import Field, StringConstraints

from suno_content.domain.base import DomainModel
from suno_content.domain.enums import (
    BusinessContext,
    ContentType,
    EvalStatus,
    SourceType,
    StrEnum,
)
from suno_content.domain.models import SourceArtifact, SourceProvenance

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
VersionStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]

# Policy decisions intentionally reuse the canonical evaluator status enum so
# review state has one representation across the policy and evaluation layers.
PolicyDecision = EvalStatus


class FindingLevel(StrEnum):
    HARD_FAIL = "HARD_FAIL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class RecommendationProvenance(StrEnum):
    NONE = "NONE"
    ATTRIBUTED_SOURCE = "ATTRIBUTED_SOURCE"
    NEW_GENERIC = "NEW_GENERIC"
    PERSONALIZED = "PERSONALIZED"
    UNKNOWN = "UNKNOWN"


class PolicyContext(DomainModel):
    """Versioned policy overlay around the canonical source contract."""

    schema_version: Literal["policy_context.v2"] = "policy_context.v2"
    source: SourceArtifact
    policy_version: VersionStr
    source_has_recommendation: bool = False
    source_has_forward_looking: bool = False
    source_has_legal_normative_effect: bool = False
    configured_disclaimer_id: NonEmptyStr | None = None

    @property
    def source_type(self) -> SourceType:
        return self.source.source_type

    @property
    def content_type(self) -> ContentType:
        return self.source.content_type

    @property
    def business_context(self) -> BusinessContext:
        return self.source.business_context

    @property
    def provenance(self) -> SourceProvenance:
        return self.source.provenance()


class PolicySignals(DomainModel):
    schema_version: Literal["policy_signals.v2"] = "policy_signals.v2"
    recommendation_provenance: RecommendationProvenance = RecommendationProvenance.NONE
    attribution_preserved: bool | None = None
    material_grounding_mismatch: bool = False
    modality_escalation: bool = False
    fabricated_policy_or_endorsement: bool = False
    normative_distortion: bool = False
    caveat_elision: bool = False
    source_mixing_without_claim_provenance: bool = False
    asset_specific_or_recommendation_like: bool = False
    low_confidence_source: bool = False
    detector_disagreement: bool = False
    external_context_added: bool = False
    sensitive_corporate_event: bool = False
    legal_effect_summary: bool = False


class PolicyRequest(DomainModel):
    schema_version: Literal["policy_request.v2"] = "policy_request.v2"
    source_text: NonEmptyStr
    output_text: NonEmptyStr
    context: PolicyContext
    signals: PolicySignals = Field(default_factory=PolicySignals)


class PolicyFinding(DomainModel):
    schema_version: Literal["policy_finding.v2"] = "policy_finding.v2"
    code: NonEmptyStr
    level: FindingLevel
    reason: NonEmptyStr


class PolicyResult(DomainModel):
    schema_version: Literal["policy_result.v2"] = "policy_result.v2"
    decision: EvalStatus
    findings: tuple[PolicyFinding, ...]
    detected_disclaimer: bool
    recommendation_provenance: RecommendationProvenance
    policy_version: VersionStr
    source: SourceArtifact

    @property
    def codes(self) -> tuple[str, ...]:
        return tuple(finding.code for finding in self.findings)

    def has(self, code: str) -> bool:
        return code in self.codes

    @property
    def provenance(self) -> SourceProvenance:
        return self.source.provenance()


def dedupe_findings(findings: Iterable[PolicyFinding]) -> tuple[PolicyFinding, ...]:
    seen: set[str] = set()
    ordered: list[PolicyFinding] = []
    for finding in findings:
        if finding.code not in seen:
            ordered.append(finding)
            seen.add(finding.code)
    return tuple(ordered)
