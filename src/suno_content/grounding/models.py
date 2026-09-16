from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from pydantic import Field, StringConstraints, model_validator

from suno_content.domain import (
    DomainModel,
    EvalStatus,
    FailureSeverity,
    GateStatus,
    Materiality,
    ProvenanceRef,
)

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
VersionStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]


class ClaimSupportStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNVERIFIABLE = "UNVERIFIABLE"


class UnverifiableReason(str, Enum):
    RETRIEVAL_MISS = "RETRIEVAL_MISS"
    EXTRACTION_AMBIGUITY = "EXTRACTION_AMBIGUITY"
    SEMANTIC_NOT_RUN = "SEMANTIC_NOT_RUN"
    SEMANTIC_UNCERTAINTY = "SEMANTIC_UNCERTAINTY"
    HARD_GATE_BLOCKED = "HARD_GATE_BLOCKED"


class GateAuthority(str, Enum):
    SOURCE = "SOURCE"
    DETERMINISTIC_FACTUAL = "DETERMINISTIC_FACTUAL"
    POLICY = "POLICY"
    CLAIM_GROUNDING = "CLAIM_GROUNDING"


class AtomicClaim(DomainModel):
    schema_version: Literal["atomic_claim.v1"] = "atomic_claim.v1"
    claim_id: NonEmptyStr
    text: NonEmptyStr
    materiality: Materiality
    expected_evidence_refs: Annotated[tuple[ProvenanceRef, ...], Field(min_length=1)]
    anchor_ids: tuple[NonEmptyStr, ...] = ()

    @model_validator(mode="after")
    def single_source_lineage(self) -> "AtomicClaim":
        lineage = {(ref.source_id, ref.source_hash) for ref in self.expected_evidence_refs}
        if len(lineage) != 1:
            raise ValueError("an atomic claim must resolve to one source identity/hash")
        return self


class EvidenceItem(DomainModel):
    schema_version: Literal["claim_evidence_item.v1"] = "claim_evidence_item.v1"
    provenance: ProvenanceRef
    text: NonEmptyStr
    extraction_status: GateStatus = GateStatus.PASS


class EvidencePacket(DomainModel):
    schema_version: Literal["claim_evidence_packet.v1"] = "claim_evidence_packet.v1"
    claim_id: NonEmptyStr
    expected_refs: Annotated[tuple[ProvenanceRef, ...], Field(min_length=1)]
    retrieved: tuple[EvidenceItem, ...] = ()
    retrieval_version: VersionStr

    @model_validator(mode="after")
    def validate_lineage(self) -> "EvidencePacket":
        expected_lineage = {(ref.source_id, ref.source_hash) for ref in self.expected_refs}
        if len(expected_lineage) != 1:
            raise ValueError("expected evidence refs must share one source lineage")
        for item in self.retrieved:
            if (item.provenance.source_id, item.provenance.source_hash) not in expected_lineage:
                raise ValueError("retrieved evidence must share the claim source lineage")
        keys = [item.provenance.canonical_json() for item in self.retrieved]
        if len(keys) != len(set(keys)):
            raise ValueError("retrieved evidence refs must be unique")
        return self

    @property
    def retrieval_miss(self) -> bool:
        return not self.retrieved

    @property
    def evidence_refs(self) -> tuple[ProvenanceRef, ...]:
        return tuple(item.provenance for item in self.retrieved)


class DeterministicClaimSignal(DomainModel):
    schema_version: Literal["deterministic_claim_signal.v1"] = "deterministic_claim_signal.v1"
    claim_id: NonEmptyStr
    status: GateStatus
    support_status: ClaimSupportStatus
    code: NonEmptyStr | None = None
    severity: FailureSeverity | None = None
    hard_gate: bool = False
    evidence_refs: tuple[ProvenanceRef, ...] = ()


class SemanticSignal(DomainModel):
    schema_version: Literal["semantic_signal.v1"] = "semantic_signal.v1"
    claim_id: NonEmptyStr
    support_status: ClaimSupportStatus
    backend_id: NonEmptyStr
    backend_version: VersionStr
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] | None = None
    evidence_refs: tuple[ProvenanceRef, ...] = ()
    diagnostic_codes: tuple[NonEmptyStr, ...] = ()


class ClaimFinding(DomainModel):
    schema_version: Literal["claim_finding.v1"] = "claim_finding.v1"
    grounding_version: VersionStr
    claim_id: NonEmptyStr
    materiality: Materiality
    support_status: ClaimSupportStatus
    decision: GateStatus
    failure_code: NonEmptyStr | None = None
    unverifiable_reason: UnverifiableReason | None = None
    evidence_refs: tuple[ProvenanceRef, ...] = ()
    deterministic_code: NonEmptyStr | None = None
    semantic_signal: SemanticSignal | None = None

    @model_validator(mode="after")
    def coherent_support_state(self) -> "ClaimFinding":
        if self.support_status == ClaimSupportStatus.SUPPORTED and self.decision != GateStatus.PASS:
            raise ValueError("SUPPORTED claim must have PASS claim decision")
        if self.support_status == ClaimSupportStatus.UNVERIFIABLE:
            if self.decision == GateStatus.PASS or self.unverifiable_reason is None:
                raise ValueError("UNVERIFIABLE claim requires reason and cannot PASS")
        elif self.unverifiable_reason is not None:
            raise ValueError("unverifiable_reason is only valid for UNVERIFIABLE claims")
        return self


class GateSignal(DomainModel):
    schema_version: Literal["hybrid_gate_signal.v1"] = "hybrid_gate_signal.v1"
    authority: GateAuthority
    code: NonEmptyStr
    status: GateStatus
    hard_gate: bool = True


class HybridDecision(DomainModel):
    schema_version: Literal["hybrid_decision.v1"] = "hybrid_decision.v1"
    evaluator_version: VersionStr
    status: EvalStatus
    gates: tuple[GateSignal, ...]
    claim_findings: tuple[ClaimFinding, ...]
    semantic_backend_id: NonEmptyStr | None = None
    semantic_backend_version: VersionStr | None = None
    semantic_enabled: bool = False

    @model_validator(mode="after")
    def protect_hard_gate_precedence(self) -> "HybridDecision":
        hard_fail = any(g.hard_gate and g.status == GateStatus.FAIL for g in self.gates)
        hard_review = any(g.hard_gate and g.status == GateStatus.REVIEW_REQUIRED for g in self.gates)
        claim_fail = any(f.decision == GateStatus.FAIL for f in self.claim_findings)
        claim_review = any(f.decision == GateStatus.REVIEW_REQUIRED for f in self.claim_findings)
        if hard_fail and self.status != EvalStatus.FAIL:
            raise ValueError("hard FAIL must dominate HybridDecision")
        if claim_fail and self.status != EvalStatus.FAIL:
            raise ValueError("claim FAIL must dominate HybridDecision")
        if self.status == EvalStatus.PASS and (hard_review or claim_review):
            raise ValueError("PASS cannot compensate REVIEW_REQUIRED evidence")
        if self.semantic_enabled != (self.semantic_backend_id is not None):
            raise ValueError("semantic_enabled and semantic backend audit fields must agree")
        if (self.semantic_backend_id is None) != (self.semantic_backend_version is None):
            raise ValueError("semantic backend id/version must be persisted together")
        return self

    @property
    def hard_fail_codes(self) -> tuple[str, ...]:
        return tuple(g.code for g in self.gates if g.hard_gate and g.status == GateStatus.FAIL)
