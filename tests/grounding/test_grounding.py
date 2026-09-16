from __future__ import annotations

import pytest

from suno_content.domain import (
    GateStatus,
    Materiality,
    ParsedDocument,
    SourceProvenance,
    SourceSpan,
)
from suno_content.grounding import (
    AtomicClaim,
    ClaimSupportStatus,
    EvidenceItem,
    EvidencePacket,
    GroundingValidationError,
    ProvenanceResolver,
    SemanticSignal,
    UnverifiableReason,
    hybrid_decision,
    run_semantic_ablation,
)

HASH = "a" * 64


class StubSemanticAdapter:
    backend_id = "stub-semantic"
    backend_version = "test-v1"

    def __init__(self, support: ClaimSupportStatus) -> None:
        self.support = support
        self.calls = 0

    def evaluate(self, claim: AtomicClaim, evidence: EvidencePacket) -> SemanticSignal:
        self.calls += 1
        return SemanticSignal(
            claim_id=claim.claim_id,
            support_status=self.support,
            backend_id=self.backend_id,
            backend_version=self.backend_version,
            confidence=0.9,
            evidence_refs=evidence.evidence_refs,
        )


def _doc() -> ParsedDocument:
    source = SourceProvenance(source_id="SRC", source_hash=HASH, artifact_ref="raw/source.pdf")
    return ParsedDocument(
        document_id="DOC",
        source=source,
        parser_version="parser-test",
        spans=(SourceSpan(span_id="S1", source=source, text="Receita cresceu 10%.", page_number=1),),
    )


def _claim_and_packet():
    doc = _doc()
    ref = doc.spans[0].provenance_ref()
    claim = AtomicClaim(
        claim_id="C1",
        text="A receita cresceu 10%.",
        materiality=Materiality.MATERIAL,
        expected_evidence_refs=(ref,),
    )
    packet = ProvenanceResolver(doc).packet_for(claim, (ref,), retrieval_version="retrieval-test")
    return claim, packet, ref


def test_atomic_claim_provenance_is_resolvable_and_auditable():
    claim, packet, ref = _claim_and_packet()
    assert packet.evidence_refs == (ref,)
    assert claim.canonical_sha256() == claim.canonical_sha256()
    bad = ref.model_copy(update={"span_id": "missing"})
    with pytest.raises(GroundingValidationError):
        ProvenanceResolver(_doc()).resolve(bad)


def test_retrieval_miss_and_extraction_ambiguity_stay_unverifiable_but_distinct():
    claim, packet, ref = _claim_and_packet()
    miss = packet.model_copy(update={"retrieved": ()})
    miss_decision = hybrid_decision(
        (claim,), {claim.claim_id: miss}, source_status=GateStatus.PASS,
        factual_status=GateStatus.PASS, policy_status=GateStatus.PASS,
    )
    assert miss_decision.claim_findings[0].support_status == ClaimSupportStatus.UNVERIFIABLE
    assert miss_decision.claim_findings[0].unverifiable_reason == UnverifiableReason.RETRIEVAL_MISS

    ambiguous = packet.model_copy(
        update={"retrieved": (EvidenceItem(provenance=ref, text="Receita cresceu 10%.", extraction_status=GateStatus.REVIEW_REQUIRED),)}
    )
    ambiguous_decision = hybrid_decision(
        (claim,), {claim.claim_id: ambiguous}, source_status=GateStatus.PASS,
        factual_status=GateStatus.PASS, policy_status=GateStatus.PASS,
    )
    assert ambiguous_decision.claim_findings[0].support_status == ClaimSupportStatus.UNVERIFIABLE
    assert ambiguous_decision.claim_findings[0].unverifiable_reason == UnverifiableReason.EXTRACTION_AMBIGUITY


@pytest.mark.parametrize(
    ("support", "decision"),
    [
        (ClaimSupportStatus.SUPPORTED, "PASS"),
        (ClaimSupportStatus.CONTRADICTED, "FAIL"),
        (ClaimSupportStatus.UNSUPPORTED, "FAIL"),
        (ClaimSupportStatus.UNVERIFIABLE, "REVIEW_REQUIRED"),
    ],
)
def test_claim_support_states_are_distinct(support, decision):
    claim, packet, _ = _claim_and_packet()
    adapter = StubSemanticAdapter(support)
    result = hybrid_decision(
        (claim,), {claim.claim_id: packet}, source_status=GateStatus.PASS,
        factual_status=GateStatus.PASS, policy_status=GateStatus.PASS,
        semantic_adapter=adapter,
    )
    assert result.claim_findings[0].support_status == support
    assert result.status.value == decision


def test_source_and_policy_hard_fails_short_circuit_semantic_sensor():
    claim, packet, _ = _claim_and_packet()
    for kwargs in (
        dict(source_status=GateStatus.FAIL, factual_status=GateStatus.PASS, policy_status=GateStatus.PASS),
        dict(source_status=GateStatus.PASS, factual_status=GateStatus.FAIL, policy_status=GateStatus.PASS),
        dict(source_status=GateStatus.PASS, factual_status=GateStatus.PASS, policy_status=GateStatus.FAIL),
    ):
        adapter = StubSemanticAdapter(ClaimSupportStatus.SUPPORTED)
        result = hybrid_decision((claim,), {claim.claim_id: packet}, semantic_adapter=adapter, **kwargs)
        assert result.status.value == "FAIL"
        assert adapter.calls == 0


def test_ablation_reports_incremental_semantic_effect_without_changing_hard_gate():
    claim, packet, _ = _claim_and_packet()
    adapter = StubSemanticAdapter(ClaimSupportStatus.SUPPORTED)
    result = run_semantic_ablation(
        (claim,), {claim.claim_id: packet}, source_status=GateStatus.PASS,
        factual_status=GateStatus.PASS, policy_status=GateStatus.PASS, adapter=adapter,
    )
    assert result.without_semantic.status.value == "REVIEW_REQUIRED"
    assert result.with_semantic.status.value == "PASS"
    assert result.changed_claim_ids == ("C1",)
    assert result.hard_gate_invariant is True
