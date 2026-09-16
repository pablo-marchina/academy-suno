from __future__ import annotations

from typing import Protocol, runtime_checkable

from .models import AtomicClaim, EvidencePacket, SemanticSignal


@runtime_checkable
class SemanticAdapter(Protocol):
    """Pluggable secondary sensor. It has no authority over hard gates."""

    backend_id: str
    backend_version: str

    def evaluate(self, claim: AtomicClaim, evidence: EvidencePacket) -> SemanticSignal:
        ...
