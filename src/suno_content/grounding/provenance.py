from __future__ import annotations

from collections.abc import Iterable

from suno_content.domain import GateStatus, ParsedDocument, ProvenanceRef

from .models import AtomicClaim, EvidenceItem, EvidencePacket


class GroundingValidationError(ValueError):
    pass


def _ref_key(ref: ProvenanceRef) -> tuple[object, ...]:
    if ref.span_id is not None:
        return ("span", ref.source_id, ref.source_hash, ref.page_number, ref.span_id)
    return (
        "table",
        ref.source_id,
        ref.source_hash,
        ref.page_number,
        ref.table_id,
        ref.row_index,
        ref.column_index,
    )


def infer_source_status(document: ParsedDocument) -> GateStatus:
    for key in ("source_trust_status", "source_trust", "document_extraction_status"):
        raw = document.coverage_metadata.get(key)
        if isinstance(raw, dict):
            raw = raw.get("status")
        if isinstance(raw, str):
            try:
                return GateStatus(raw)
            except ValueError:
                pass
    return GateStatus.PASS


class ProvenanceResolver:
    """Resolve canonical ProvenanceRef values against one ParsedDocument."""

    def __init__(self, document: ParsedDocument) -> None:
        self.document = document
        self._items: dict[tuple[object, ...], EvidenceItem] = {}
        for span in document.spans:
            ref = span.provenance_ref()
            self._items[_ref_key(ref)] = EvidenceItem(provenance=ref, text=span.text)
        for cell in document.table_cells:
            ref = cell.provenance_ref()
            self._items[_ref_key(ref)] = EvidenceItem(provenance=ref, text=cell.raw_value)

    def resolve(self, ref: ProvenanceRef) -> EvidenceItem:
        expected = (self.document.source.source_id, self.document.source.source_hash)
        if (ref.source_id, ref.source_hash) != expected:
            raise GroundingValidationError("provenance points outside the parsed source lineage")
        try:
            return self._items[_ref_key(ref)]
        except KeyError as exc:
            raise GroundingValidationError("provenance ref is not resolvable in ParsedDocument") from exc

    def packet_for(
        self,
        claim: AtomicClaim,
        retrieved_refs: Iterable[ProvenanceRef],
        *,
        retrieval_version: str,
    ) -> EvidencePacket:
        for ref in claim.expected_evidence_refs:
            self.resolve(ref)
        retrieved = tuple(self.resolve(ref) for ref in retrieved_refs)
        return EvidencePacket(
            claim_id=claim.claim_id,
            expected_refs=claim.expected_evidence_refs,
            retrieved=retrieved,
            retrieval_version=retrieval_version,
        )
