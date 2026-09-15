from __future__ import annotations

import re
from dataclasses import replace

from .models import (
    FindingLevel,
    PolicyContext,
    PolicyDecision,
    PolicyFinding,
    PolicyRequest,
    PolicyResult,
    PolicySignals,
    RecommendationProvenance,
    SourceType,
    dedupe_findings,
)

_RECOMMENDATION_RE = re.compile(
    r"\b(compr(?:e|ar|a)|vend(?:a|er)|manter|aument(?:e|ar)\s+(?:a\s+)?posi[cç][aã]o|"
    r"reduz(?:a|ir)\s+(?:a\s+)?posi[cç][aã]o|entrar|entre\s+(?:em|na|no)|sair|saia\s+(?:de|da|do)|aloc(?:ar|e)|"
    r"rebalance(?:ar|ie)|pre[cç]o[- ]alvo|target price|upside|buy|sell|hold|"
    r"vale a pena|oportunidade|agora [ée] a hora)\b",
    re.IGNORECASE,
)
_PERSONALIZATION_RE = re.compile(
    r"\b(para voc[êe]|se voc[êe]|seu perfil|sua carteira|seu patrim[oô]nio|sua renda|"
    r"seu objetivo|seu horizonte|toler[aâ]ncia a risco|investidor(?:es)?\s+conservador(?:es)?|"
    r"investidor(?:es)?\s+moderado(?:s)?|investidor(?:es)?\s+arrojado(?:s)?)\b",
    re.IGNORECASE,
)
_DISCLAIMER_RE = re.compile(
    r"\b(n[aã]o (?:se trata de|[ée]) (?:uma )?recomenda[cç][aã]o|n[aã]o constitui recomenda[cç][aã]o|"
    r"conte[uú]do (?:meramente )?educacional|opini[aã]o pessoal)\b",
    re.IGNORECASE,
)

_HARD_REASONS = {
    "HF-01": "Unsupported/new recommendation, target, allocation or investment action.",
    "HF-02": "Investment action is personalized to recipient/profile circumstances.",
    "HF-03": "Material grounding signal conflicts with source truth.",
    "HF-04": "Source uncertainty/forecast was escalated into certainty.",
    "HF-05": "Third-party recommendation/opinion lost its attribution.",
    "HF-06": "Public-source scope is violated by an unverified/non-public source.",
    "HF-07": "Unconfigured Suno/internal policy, disclaimer or regulatory endorsement was fabricated.",
    "HF-08": "Risky output has unresolved source type or business context.",
    "HF-09": "Normative obligation, permission, exception, scope or effectiveness was distorted.",
    "HF-10": "A material caveat was removed or displaced to satisfy format constraints.",
    "HF-11": "Claims from multiple sources were mixed without claim-level provenance.",
}

_REVIEW_REASONS = {
    "HR-01": "Source contains recommendation/rating/target/portfolio content.",
    "HR-02": "Sensitive corporate event/guidance requires human review.",
    "HR-03": "Practical legal/regulatory effect is being summarized.",
    "HR-04": "Source extraction/provenance confidence is insufficient for auto-release.",
    "HR-05": "Recommendation detectors/provenance signals disagree or are unresolved.",
    "HR-06": "External context not present in the primary source was added.",
}


def _finding(code: str, level: FindingLevel) -> PolicyFinding:
    reasons = _HARD_REASONS if level is FindingLevel.HARD_FAIL else _REVIEW_REASONS
    return PolicyFinding(code=code, level=level, reason=reasons[code])


def _recommendation_like(text: str) -> bool:
    return bool(_RECOMMENDATION_RE.search(text))


def _personalization_like(text: str) -> bool:
    return bool(_PERSONALIZATION_RE.search(text))


def _disclaimer_like(text: str) -> bool:
    return bool(_DISCLAIMER_RE.search(text))


def derive_text_signals(request: PolicyRequest) -> PolicySignals:
    """Derive only high-precision lexical signals.

    Semantic/provenance-sensitive findings remain explicit inputs. This keeps the
    policy layer deterministic and prevents a keyword match from pretending to
    prove source equivalence.
    """

    output_has_recommendation = _recommendation_like(request.output_text)
    personalized = output_has_recommendation and _personalization_like(request.output_text)
    provenance = request.signals.recommendation_provenance

    if personalized:
        provenance = RecommendationProvenance.PERSONALIZED
    elif output_has_recommendation and provenance is RecommendationProvenance.NONE:
        if request.context.source_has_recommendation:
            if request.signals.attribution_preserved is True:
                provenance = RecommendationProvenance.ATTRIBUTED_SOURCE
            elif request.signals.attribution_preserved is False:
                provenance = RecommendationProvenance.NEW_GENERIC
            else:
                provenance = RecommendationProvenance.UNKNOWN
        else:
            provenance = RecommendationProvenance.NEW_GENERIC

    return replace(
        request.signals,
        recommendation_provenance=provenance,
        asset_specific_or_recommendation_like=(
            request.signals.asset_specific_or_recommendation_like or output_has_recommendation
        ),
    )


def evaluate_policy(request: PolicyRequest) -> PolicyResult:
    signals = derive_text_signals(request)
    context: PolicyContext = request.context
    findings: list[PolicyFinding] = []

    provenance = signals.recommendation_provenance
    if provenance is RecommendationProvenance.PERSONALIZED:
        findings.append(_finding("HF-02", FindingLevel.HARD_FAIL))
    elif provenance is RecommendationProvenance.NEW_GENERIC:
        findings.append(_finding("HF-01", FindingLevel.HARD_FAIL))
        if context.source_has_recommendation and signals.attribution_preserved is False:
            findings.append(_finding("HF-05", FindingLevel.HARD_FAIL))
    elif provenance is RecommendationProvenance.ATTRIBUTED_SOURCE:
        findings.append(_finding("HR-01", FindingLevel.REVIEW_REQUIRED))
    elif provenance is RecommendationProvenance.UNKNOWN:
        findings.append(_finding("HR-05", FindingLevel.REVIEW_REQUIRED))

    if signals.material_grounding_mismatch:
        findings.append(_finding("HF-03", FindingLevel.HARD_FAIL))
    if signals.modality_escalation:
        findings.append(_finding("HF-04", FindingLevel.HARD_FAIL))
    if signals.fabricated_policy_or_endorsement:
        findings.append(_finding("HF-07", FindingLevel.HARD_FAIL))
    if signals.normative_distortion:
        findings.append(_finding("HF-09", FindingLevel.HARD_FAIL))
    if signals.caveat_elision:
        findings.append(_finding("HF-10", FindingLevel.HARD_FAIL))
    if signals.source_mixing_without_claim_provenance:
        findings.append(_finding("HF-11", FindingLevel.HARD_FAIL))

    if not context.public_source_verified:
        findings.append(_finding("HF-06", FindingLevel.HARD_FAIL))

    risky_output = signals.asset_specific_or_recommendation_like
    unresolved_source = context.source_type is SourceType.UNKNOWN_OTHER
    unresolved_business = context.business_context.strip().upper() == "UNKNOWN"
    if risky_output and (unresolved_source or unresolved_business):
        findings.append(_finding("HF-08", FindingLevel.HARD_FAIL))

    if context.source_has_recommendation and provenance is RecommendationProvenance.NONE:
        findings.append(_finding("HR-01", FindingLevel.REVIEW_REQUIRED))
    if signals.sensitive_corporate_event:
        findings.append(_finding("HR-02", FindingLevel.REVIEW_REQUIRED))
    if signals.legal_effect_summary or (
        context.source_has_legal_normative_effect and context.source_type is SourceType.REGULATOR_NORMATIVE
    ):
        findings.append(_finding("HR-03", FindingLevel.REVIEW_REQUIRED))
    if signals.low_confidence_source:
        findings.append(_finding("HR-04", FindingLevel.REVIEW_REQUIRED))
    if signals.detector_disagreement:
        findings.append(_finding("HR-05", FindingLevel.REVIEW_REQUIRED))
    if signals.external_context_added:
        findings.append(_finding("HR-06", FindingLevel.REVIEW_REQUIRED))

    findings_tuple = dedupe_findings(findings)
    if any(f.level is FindingLevel.HARD_FAIL for f in findings_tuple):
        decision = PolicyDecision.FAIL
    elif any(f.level is FindingLevel.REVIEW_REQUIRED for f in findings_tuple):
        decision = PolicyDecision.REVIEW_REQUIRED
    else:
        decision = PolicyDecision.PASS

    # A disclaimer is audit metadata only. It intentionally has no effect on
    # findings or decision, so it can never launder a substantive violation.
    return PolicyResult(
        decision=decision,
        findings=findings_tuple,
        detected_disclaimer=_disclaimer_like(request.output_text),
        recommendation_provenance=provenance,
    )
