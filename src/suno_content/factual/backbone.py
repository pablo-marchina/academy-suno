from __future__ import annotations

from collections.abc import Iterable

from suno_content.domain import Anchor, GateStatus, Materiality, ParsedDocument, ProvenanceRef, SourceTrust

from .models import FactualBackbone, TableRoleContext


class BackboneValidationError(ValueError):
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


def _document_ref_keys(document: ParsedDocument) -> set[tuple[object, ...]]:
    keys = {_ref_key(span.provenance_ref()) for span in document.spans}
    keys.update(_ref_key(cell.provenance_ref()) for cell in document.table_cells)
    return keys


def _document_table_cells(document: ParsedDocument) -> dict[tuple[object, ...], object]:
    return {_ref_key(cell.provenance_ref()): cell for cell in document.table_cells}


def _status_from_metadata(document: ParsedDocument) -> GateStatus:
    for key in ("source_trust_status", "source_trust", "document_extraction_status"):
        raw = document.coverage_metadata.get(key)
        if isinstance(raw, dict):
            raw = raw.get("status")
        if isinstance(raw, str):
            try:
                return GateStatus(raw)
            except ValueError:
                continue
    return GateStatus.PASS


def _worst_status(*statuses: GateStatus) -> GateStatus:
    if GateStatus.FAIL in statuses:
        return GateStatus.FAIL
    if GateStatus.REVIEW_REQUIRED in statuses:
        return GateStatus.REVIEW_REQUIRED
    return GateStatus.PASS


def build_factual_backbone(
    document: ParsedDocument,
    anchors: Iterable[Anchor],
    *,
    table_roles: Iterable[TableRoleContext] = (),
) -> FactualBackbone:
    """Validate and freeze the source-owned anchor ledger."""
    anchor_tuple = tuple(anchors)
    role_tuple = tuple(table_roles)
    expected_source = (document.source.source_id, document.source.source_hash)
    available_refs = _document_ref_keys(document)
    table_cells = _document_table_cells(document)
    role_by_key = {_ref_key(role.provenance): role for role in role_tuple}
    role_keys = set(role_by_key)
    reasons: list[str] = []
    status = _status_from_metadata(document)

    for anchor in anchor_tuple:
        for ref in anchor.provenance:
            if (ref.source_id, ref.source_hash) != expected_source:
                raise BackboneValidationError(
                    f"anchor {anchor.anchor_id} points to a different source identity/hash"
                )
            key = _ref_key(ref)
            if key not in available_refs:
                raise BackboneValidationError(
                    f"anchor {anchor.anchor_id} provenance is not resolvable in ParsedDocument"
                )
            if ref.table_id is not None and key not in role_keys:
                reasons.append(f"table_role_context_missing:{anchor.anchor_id}")
                status = _worst_status(status, GateStatus.REVIEW_REQUIRED)
            elif ref.table_id is not None:
                role = role_by_key[key]
                cell = table_cells[key]
                row_label = getattr(cell, "row_label", None)
                column_label = getattr(cell, "column_label", None)
                if (row_label and role.row_role != row_label) or (
                    column_label and role.column_role != column_label
                ):
                    reasons.append(f"table_role_context_mismatch:{anchor.anchor_id}")
                    status = _worst_status(status, GateStatus.FAIL)

        if anchor.source_trust == SourceTrust.LOW and anchor.materiality in {
            Materiality.CRITICAL,
            Materiality.MATERIAL,
        }:
            reasons.append(f"low_trust_material_anchor:{anchor.anchor_id}")
            status = _worst_status(status, GateStatus.REVIEW_REQUIRED)

    return FactualBackbone(
        source=document.source,
        anchors=anchor_tuple,
        source_trust_status=status,
        table_roles=role_tuple,
        review_reasons=tuple(dict.fromkeys(reasons)),
    )


def anchor_ledger(backbone: FactualBackbone) -> dict[str, Anchor]:
    return {anchor.anchor_id: anchor for anchor in backbone.anchors}
