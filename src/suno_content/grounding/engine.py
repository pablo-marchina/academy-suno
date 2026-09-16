from __future__ import annotations

from collections.abc import Mapping, Sequence

from suno_content.domain import EvalStatus, FailureSeverity, GateStatus, Materiality, ProvenanceRef
from suno_content.factual.models import FactualFinding

from .models import (
    AtomicClaim,
    ClaimFinding,
    ClaimSupportStatus,
    DeterministicClaimSignal,
    EvidencePacket,
    GateAuthority,
    GateSignal,
    HybridDecision,
    SemanticSignal,
    UnverifiableReason,
)
from .semantic import SemanticAdapter

GROUNDING_VERSION = "grounding-v001"
EVALUATOR_VERSION = "hybrid-grounding-v001"


def signal_from_factual_finding(
    finding: FactualFinding,
    *,
    claim_id: str,
    evidence_refs: Sequence[ProvenanceRef] = (),
) -> DeterministicClaimSignal:
    severity = None
    if finding.severity in {"CRITICAL", "ERROR", "WARN"}:
        severity = FailureSeverity(finding.severity)
    support = ClaimSupportStatus(
        finding.support_status if finding.support_status != "AMBIGUOUS" else "UNVERIFIABLE"
    )
    return DeterministicClaimSignal(
        claim_id=claim_id,
        status=finding.decision,
        support_status=support,
        code=finding.failure_code,
        severity=severity,
        hard_gate=finding.hard_gate,
        evidence_refs=tuple(evidence_refs),
    )


def _unverifiable(
    claim: AtomicClaim,
    packet: EvidencePacket,
    reason: UnverifiableReason,
    *,
    code: str,
    deterministic_code: str | None = None,
) -> ClaimFinding:
    return ClaimFinding(
        grounding_version=GROUNDING_VERSION,
        claim_id=claim.claim_id,
        materiality=claim.materiality,
        support_status=ClaimSupportStatus.UNVERIFIABLE,
        decision=GateStatus.REVIEW_REQUIRED,
        failure_code=code,
        unverifiable_reason=reason,
        evidence_refs=packet.evidence_refs,
        deterministic_code=deterministic_code,
    )


def evaluate_claim(
    claim: AtomicClaim,
    packet: EvidencePacket,
    *,
    source_status: GateStatus,
    deterministic: DeterministicClaimSignal | None = None,
    semantic_adapter: SemanticAdapter | None = None,
) -> ClaimFinding:
    if packet.claim_id != claim.claim_id:
        raise ValueError("claim/evidence packet id mismatch")
    if deterministic is not None and deterministic.claim_id != claim.claim_id:
        raise ValueError("claim/deterministic signal id mismatch")

    if source_status != GateStatus.PASS:
        return _unverifiable(
            claim,
            packet,
            UnverifiableReason.EXTRACTION_AMBIGUITY,
            code="GROUNDING_SOURCE_EXTRACTION_AMBIGUOUS",
        )

    if deterministic is not None and deterministic.status != GateStatus.PASS:
        if deterministic.status == GateStatus.FAIL:
            return ClaimFinding(
                grounding_version=GROUNDING_VERSION,
                claim_id=claim.claim_id,
                materiality=claim.materiality,
                support_status=deterministic.support_status,
                decision=GateStatus.FAIL,
                failure_code=deterministic.code or "GROUNDING_DETERMINISTIC_FAIL",
                evidence_refs=deterministic.evidence_refs or packet.evidence_refs,
                deterministic_code=deterministic.code,
            )
        reason = (
            UnverifiableReason.RETRIEVAL_MISS
            if deterministic.code and "RETRIEVAL_MISS" in deterministic.code
            else UnverifiableReason.EXTRACTION_AMBIGUITY
        )
        return _unverifiable(
            claim,
            packet,
            reason,
            code=deterministic.code or "GROUNDING_DETERMINISTIC_REVIEW",
            deterministic_code=deterministic.code,
        )

    if packet.retrieval_miss:
        return _unverifiable(
            claim,
            packet,
            UnverifiableReason.RETRIEVAL_MISS,
            code="GROUNDING_RETRIEVAL_MISS",
        )

    if any(item.extraction_status != GateStatus.PASS for item in packet.retrieved):
        return _unverifiable(
            claim,
            packet,
            UnverifiableReason.EXTRACTION_AMBIGUITY,
            code="GROUNDING_EVIDENCE_EXTRACTION_AMBIGUOUS",
        )

    if semantic_adapter is None:
        return _unverifiable(
            claim,
            packet,
            UnverifiableReason.SEMANTIC_NOT_RUN,
            code="GROUNDING_SEMANTIC_NOT_RUN",
        )

    semantic: SemanticSignal = semantic_adapter.evaluate(claim, packet)
    if semantic.claim_id != claim.claim_id:
        raise ValueError("semantic adapter returned the wrong claim_id")
    packet_refs = {ref.canonical_json() for ref in packet.evidence_refs}
    if any(ref.canonical_json() not in packet_refs for ref in semantic.evidence_refs):
        raise ValueError("semantic adapter referenced evidence outside the packet")

    if semantic.support_status == ClaimSupportStatus.SUPPORTED:
        return ClaimFinding(
            grounding_version=GROUNDING_VERSION,
            claim_id=claim.claim_id,
            materiality=claim.materiality,
            support_status=semantic.support_status,
            decision=GateStatus.PASS,
            evidence_refs=semantic.evidence_refs or packet.evidence_refs,
            semantic_signal=semantic,
        )
    if semantic.support_status in {ClaimSupportStatus.CONTRADICTED, ClaimSupportStatus.UNSUPPORTED}:
        decision = (
            GateStatus.FAIL
            if claim.materiality in {Materiality.CRITICAL, Materiality.MATERIAL}
            else GateStatus.REVIEW_REQUIRED
        )
        code = (
            "GROUNDING_CLAIM_CONTRADICTED"
            if semantic.support_status == ClaimSupportStatus.CONTRADICTED
            else "GROUNDING_CLAIM_UNSUPPORTED"
        )
        return ClaimFinding(
            grounding_version=GROUNDING_VERSION,
            claim_id=claim.claim_id,
            materiality=claim.materiality,
            support_status=semantic.support_status,
            decision=decision,
            failure_code=code,
            evidence_refs=semantic.evidence_refs or packet.evidence_refs,
            semantic_signal=semantic,
        )
    return ClaimFinding(
        grounding_version=GROUNDING_VERSION,
        claim_id=claim.claim_id,
        materiality=claim.materiality,
        support_status=ClaimSupportStatus.UNVERIFIABLE,
        decision=GateStatus.REVIEW_REQUIRED,
        failure_code="GROUNDING_SEMANTIC_UNCERTAIN",
        unverifiable_reason=UnverifiableReason.SEMANTIC_UNCERTAINTY,
        evidence_refs=semantic.evidence_refs or packet.evidence_refs,
        semantic_signal=semantic,
    )


def hybrid_decision(
    claims: Sequence[AtomicClaim],
    packets: Mapping[str, EvidencePacket],
    *,
    source_status: GateStatus,
    factual_status: GateStatus,
    policy_status: GateStatus,
    deterministic_signals: Mapping[str, DeterministicClaimSignal] | None = None,
    semantic_adapter: SemanticAdapter | None = None,
    evaluator_version: str = EVALUATOR_VERSION,
) -> HybridDecision:
    deterministic_signals = deterministic_signals or {}
    gates = (
        GateSignal(authority=GateAuthority.SOURCE, code="SOURCE_TRUST", status=source_status),
        GateSignal(
            authority=GateAuthority.DETERMINISTIC_FACTUAL,
            code="DETERMINISTIC_FACTUAL",
            status=factual_status,
        ),
        GateSignal(authority=GateAuthority.POLICY, code="POLICY", status=policy_status),
    )
    hard_fail = any(g.status == GateStatus.FAIL for g in gates)
    findings: list[ClaimFinding] = []
    for claim in claims:
        packet = packets[claim.claim_id]
        deterministic = deterministic_signals.get(claim.claim_id)
        if hard_fail and (deterministic is None or deterministic.status == GateStatus.PASS):
            findings.append(
                _unverifiable(
                    claim,
                    packet,
                    UnverifiableReason.HARD_GATE_BLOCKED,
                    code="GROUNDING_BLOCKED_BY_HARD_GATE",
                )
            )
            continue
        findings.append(
            evaluate_claim(
                claim,
                packet,
                source_status=source_status,
                deterministic=deterministic,
                semantic_adapter=semantic_adapter,
            )
        )

    if hard_fail or any(f.decision == GateStatus.FAIL for f in findings):
        status = EvalStatus.FAIL
    elif any(g.status == GateStatus.REVIEW_REQUIRED for g in gates) or any(
        f.decision == GateStatus.REVIEW_REQUIRED for f in findings
    ):
        status = EvalStatus.REVIEW_REQUIRED
    else:
        status = EvalStatus.PASS

    return HybridDecision(
        evaluator_version=evaluator_version,
        status=status,
        gates=gates,
        claim_findings=tuple(findings),
        semantic_backend_id=getattr(semantic_adapter, "backend_id", None),
        semantic_backend_version=getattr(semantic_adapter, "backend_version", None),
        semantic_enabled=semantic_adapter is not None,
    )
