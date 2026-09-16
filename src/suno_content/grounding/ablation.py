from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Literal

from suno_content.domain import DomainModel, GateStatus

from .engine import hybrid_decision
from .models import AtomicClaim, DeterministicClaimSignal, EvidencePacket, HybridDecision
from .semantic import SemanticAdapter


class AblationResult(DomainModel):
    schema_version: Literal["semantic_ablation_result.v1"] = "semantic_ablation_result.v1"
    backend_id: str
    backend_version: str
    without_semantic: HybridDecision
    with_semantic: HybridDecision
    changed_claim_ids: tuple[str, ...]
    hard_gate_invariant: bool


def run_semantic_ablation(
    claims: Sequence[AtomicClaim],
    packets: Mapping[str, EvidencePacket],
    *,
    source_status: GateStatus,
    factual_status: GateStatus,
    policy_status: GateStatus,
    adapter: SemanticAdapter,
    deterministic_signals: Mapping[str, DeterministicClaimSignal] | None = None,
) -> AblationResult:
    base = hybrid_decision(
        claims,
        packets,
        source_status=source_status,
        factual_status=factual_status,
        policy_status=policy_status,
        deterministic_signals=deterministic_signals,
        semantic_adapter=None,
    )
    enabled = hybrid_decision(
        claims,
        packets,
        source_status=source_status,
        factual_status=factual_status,
        policy_status=policy_status,
        deterministic_signals=deterministic_signals,
        semantic_adapter=adapter,
    )
    base_by_id = {f.claim_id: f for f in base.claim_findings}
    changed = tuple(
        f.claim_id
        for f in enabled.claim_findings
        if base_by_id[f.claim_id].support_status != f.support_status
        or base_by_id[f.claim_id].decision != f.decision
    )
    return AblationResult(
        backend_id=adapter.backend_id,
        backend_version=adapter.backend_version,
        without_semantic=base,
        with_semantic=enabled,
        changed_claim_ids=changed,
        hard_gate_invariant=base.hard_fail_codes == enabled.hard_fail_codes,
    )
