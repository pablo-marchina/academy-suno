from __future__ import annotations

import pytest

from suno_content.domain import (
    Anchor,
    AnchorKind,
    GateStatus,
    Materiality,
    ParsedDocument,
    SourceProvenance,
    SourceSpan,
    SourceTrust,
    TableCellProvenance,
)
from suno_content.factual import BackboneValidationError, TableRoleContext, build_factual_backbone

HASH = "a" * 64


def source() -> SourceProvenance:
    return SourceProvenance(source_id="src-1", source_hash=HASH, artifact_ref="raw/src-1.pdf")


def document(*, metadata=None) -> ParsedDocument:
    prov = source()
    span = SourceSpan(span_id="S1", source=prov, text="Resultados", page_number=1)
    cell = TableCellProvenance(
        source=prov,
        table_id="T1",
        row_index=1,
        column_index=2,
        page_number=1,
        raw_value="10,0",
        normalized_value=10.0,
        row_label="Receita líquida",
        column_label="2T26",
    )
    return ParsedDocument(
        document_id="doc-1",
        source=prov,
        parser_version="parser-test",
        spans=(span,),
        table_cells=(cell,),
        coverage_metadata=metadata or {},
    )


def table_anchor(*, trust=SourceTrust.HIGH) -> Anchor:
    cell = document().table_cells[0]
    return Anchor(
        anchor_id="a-table",
        kind=AnchorKind.CURRENCY,
        normalized_value=10.0,
        surface_value="R$ 10,0 bilhões",
        semantic_role="receita_liquida",
        provenance=(cell.provenance_ref(),),
        source_trust=trust,
        materiality=Materiality.CRITICAL,
    )


def complete_role(doc: ParsedDocument, *, row_role="Receita líquida") -> TableRoleContext:
    return TableRoleContext(
        provenance=doc.table_cells[0].provenance_ref(),
        row_role=row_role,
        column_role="2T26",
        unit="R$ bilhões",
        period_or_metric="2T26",
    )


def test_table_anchor_without_semantic_role_context_cannot_be_source_ready():
    backbone = build_factual_backbone(document(), (table_anchor(),))
    assert backbone.source_trust_status == GateStatus.REVIEW_REQUIRED
    assert backbone.review_reasons == ("table_role_context_missing:a-table",)


def test_complete_table_role_context_allows_source_ready():
    doc = document()
    backbone = build_factual_backbone(doc, (table_anchor(),), table_roles=(complete_role(doc),))
    assert backbone.source_trust_status == GateStatus.PASS


def test_t002_review_required_metadata_is_preserved():
    doc = document(metadata={"source_trust_status": "REVIEW_REQUIRED"})
    backbone = build_factual_backbone(doc, (table_anchor(),), table_roles=(complete_role(doc),))
    assert backbone.source_trust_status == GateStatus.REVIEW_REQUIRED


def test_low_trust_material_anchor_cannot_auto_pass():
    doc = document()
    backbone = build_factual_backbone(
        doc,
        (table_anchor(trust=SourceTrust.LOW),),
        table_roles=(complete_role(doc),),
    )
    assert backbone.source_trust_status == GateStatus.REVIEW_REQUIRED
    assert "low_trust_material_anchor:a-table" in backbone.review_reasons


def test_anchor_provenance_must_resolve_against_parsed_document():
    anchor = table_anchor().model_copy(
        update={"provenance": (table_anchor().provenance[0].model_copy(update={"row_index": 99}),)}
    )
    with pytest.raises(BackboneValidationError, match="not resolvable"):
        build_factual_backbone(document(), (anchor,))


def test_wrong_table_role_context_is_fail_not_review():
    doc = document()
    backbone = build_factual_backbone(
        doc,
        (table_anchor(),),
        table_roles=(complete_role(doc, row_role="EBITDA ajustado"),),
    )
    assert backbone.source_trust_status == GateStatus.FAIL
    assert "table_role_context_mismatch:a-table" in backbone.review_reasons


def test_t002_fail_metadata_is_preserved():
    doc = document(metadata={"source_trust": {"status": "FAIL"}})
    backbone = build_factual_backbone(doc, (table_anchor(),), table_roles=(complete_role(doc),))
    assert backbone.source_trust_status == GateStatus.FAIL
