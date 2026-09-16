from __future__ import annotations

from pathlib import Path

from suno_content.domain import GateStatus, Materiality, ProvenanceRef
from suno_content.factual import evaluate_case
from suno_content.factual.corpus import read_jsonl
from suno_content.grounding import (
    AtomicClaim,
    ClaimSupportStatus,
    EvidenceItem,
    EvidencePacket,
    SemanticSignal,
    hybrid_decision,
    signal_from_factual_finding,
)

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "tests/fixtures/adversarial/factual_v001.jsonl"
HASH = "b" * 64


class AlwaysSupported:
    backend_id = "adversarial-always-supported"
    backend_version = "test-v1"

    def evaluate(self, claim, evidence):
        return SemanticSignal(
            claim_id=claim.claim_id,
            support_status=ClaimSupportStatus.SUPPORTED,
            backend_id=self.backend_id,
            backend_version=self.backend_version,
            evidence_refs=evidence.evidence_refs,
        )


def test_factual_v001_critical_failures_cannot_be_semantically_compensated():
    rows = read_jsonl(CORPUS)
    for row in rows:
        finding = evaluate_case(row)
        if finding.severity != "CRITICAL":
            continue
        assert finding.decision == GateStatus.FAIL
        ref = ProvenanceRef(source_id="SRC", source_hash=HASH, page_number=1, span_id="S1")
        claim = AtomicClaim(
            claim_id=row["id"], text=str(row["adversarial_output"]),
            materiality=Materiality.CRITICAL, expected_evidence_refs=(ref,),
        )
        packet = EvidencePacket(
            claim_id=claim.claim_id, expected_refs=(ref,),
            retrieved=(EvidenceItem(provenance=ref, text="fixture evidence"),),
            retrieval_version="fixture-v1",
        )
        signal = signal_from_factual_finding(finding, claim_id=claim.claim_id, evidence_refs=(ref,))
        result = hybrid_decision(
            (claim,), {claim.claim_id: packet}, source_status=GateStatus.PASS,
            factual_status=finding.decision, policy_status=GateStatus.PASS,
            deterministic_signals={claim.claim_id: signal}, semantic_adapter=AlwaysSupported(),
        )
        assert result.status.value == "FAIL", row["id"]
        assert "DETERMINISTIC_FACTUAL" in result.hard_fail_codes
