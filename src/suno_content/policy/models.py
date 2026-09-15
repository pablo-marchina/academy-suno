from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class PolicyDecision(str, Enum):
    PASS = "PASS"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    FAIL = "FAIL"


class FindingLevel(str, Enum):
    HARD_FAIL = "HARD_FAIL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class RecommendationProvenance(str, Enum):
    NONE = "NONE"
    ATTRIBUTED_SOURCE = "ATTRIBUTED_SOURCE"
    NEW_GENERIC = "NEW_GENERIC"
    PERSONALIZED = "PERSONALIZED"
    UNKNOWN = "UNKNOWN"


class SourceType(str, Enum):
    REGULATOR_NORMATIVE = "REGULATOR_NORMATIVE"
    REGULATOR_POLICY = "REGULATOR_POLICY"
    ISSUER_MATERIAL_DISCLOSURE = "ISSUER_MATERIAL_DISCLOSURE"
    ISSUER_RESULTS_RELEASE = "ISSUER_RESULTS_RELEASE"
    RESEARCH_WITH_RECOMMENDATION = "RESEARCH_WITH_RECOMMENDATION"
    NEWS_EDITORIAL = "NEWS_EDITORIAL"
    EDUCATIONAL = "EDUCATIONAL"
    UNKNOWN_OTHER = "UNKNOWN_OTHER"


@dataclass(frozen=True)
class PolicyContext:
    source_type: SourceType = SourceType.UNKNOWN_OTHER
    business_context: str = "UNKNOWN"
    public_source_verified: bool = True
    source_has_recommendation: bool = False
    source_has_forward_looking: bool = False
    source_has_legal_normative_effect: bool = False
    configured_disclaimer_id: str | None = None


@dataclass(frozen=True)
class PolicySignals:
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


@dataclass(frozen=True)
class PolicyRequest:
    source_text: str
    output_text: str
    context: PolicyContext = field(default_factory=PolicyContext)
    signals: PolicySignals = field(default_factory=PolicySignals)


@dataclass(frozen=True)
class PolicyFinding:
    code: str
    level: FindingLevel
    reason: str


@dataclass(frozen=True)
class PolicyResult:
    decision: PolicyDecision
    findings: tuple[PolicyFinding, ...]
    detected_disclaimer: bool
    recommendation_provenance: RecommendationProvenance

    @property
    def codes(self) -> tuple[str, ...]:
        return tuple(finding.code for finding in self.findings)

    def has(self, code: str) -> bool:
        return code in self.codes


def dedupe_findings(findings: Iterable[PolicyFinding]) -> tuple[PolicyFinding, ...]:
    seen: set[str] = set()
    ordered: list[PolicyFinding] = []
    for finding in findings:
        if finding.code not in seen:
            ordered.append(finding)
            seen.add(finding.code)
    return tuple(ordered)
