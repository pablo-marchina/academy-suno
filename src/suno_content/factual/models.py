from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, StringConstraints, model_validator

from suno_content.domain import Anchor, DomainModel, GateStatus, ProvenanceRef, SourceProvenance

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
SupportStatus = Literal["SUPPORTED", "CONTRADICTED", "UNSUPPORTED", "AMBIGUOUS", "UNVERIFIABLE"]
ObservedSeverity = Literal["CRITICAL", "ERROR", "WARN", "INFO"]


class TableRoleContext(DomainModel):
    """Semantic binding layered on top of canonical table-cell provenance.

    The locator itself remains the shared ProvenanceRef contract. This object only
    carries the financial roles that make the located value safe to use as a hard fact.
    """

    schema_version: Literal["table_role_context.v1"] = "table_role_context.v1"
    provenance: ProvenanceRef
    row_role: NonEmptyStr
    column_role: NonEmptyStr
    unit: NonEmptyStr
    period_or_metric: NonEmptyStr

    @model_validator(mode="after")
    def require_table_locator(self) -> "TableRoleContext":
        if self.provenance.table_id is None:
            raise ValueError("table role context requires table-cell provenance")
        return self


class FactualBackbone(DomainModel):
    schema_version: Literal["factual_backbone.v1"] = "factual_backbone.v1"
    source: SourceProvenance
    anchors: tuple[Anchor, ...]
    source_trust_status: GateStatus
    table_roles: tuple[TableRoleContext, ...] = ()
    review_reasons: tuple[NonEmptyStr, ...] = ()

    @model_validator(mode="after")
    def unique_anchor_ids(self) -> "FactualBackbone":
        ids = [a.anchor_id for a in self.anchors]
        if len(ids) != len(set(ids)):
            raise ValueError("anchor_id values must be unique inside a factual backbone")
        return self


class FactualFinding(DomainModel):
    schema_version: Literal["factual_finding.v1"] = "factual_finding.v1"
    fixture_id: NonEmptyStr | None = None
    failure_code: NonEmptyStr | None = None
    severity: ObservedSeverity
    decision: GateStatus
    hard_gate: bool
    support_status: SupportStatus
    evidence_span_ids: tuple[NonEmptyStr, ...] = ()
    details: dict[str, str] = Field(default_factory=dict)

    def oracle_row(self) -> dict[str, object]:
        return {
            "fixture_id": self.fixture_id,
            "failure_code": self.failure_code,
            "severity": self.severity,
            "decision": self.decision.value,
            "hard_gate": self.hard_gate,
            "support_status": self.support_status,
        }
