from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, JsonValue, StringConstraints, field_validator, model_validator

from .base import DomainModel
from .enums import (
    AnchorKind,
    AttemptKind,
    AudienceLevel,
    BusinessContext,
    ContentType,
    EvalStatus,
    FailureCategory,
    FailureSeverity,
    GateStatus,
    Materiality,
    OutputFormat,
    RunStatus,
    SourceTrust,
    SourceType,
)

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Sha256Hex = Annotated[str, StringConstraints(pattern=r"^[0-9a-fA-F]{64}$")]
VersionStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]


class SourceProvenance(DomainModel):
    schema_version: Literal["source_provenance.v1"] = "source_provenance.v1"
    source_id: NonEmptyStr
    source_hash: Sha256Hex
    artifact_ref: NonEmptyStr

    @field_validator("source_hash")
    @classmethod
    def normalize_source_hash(cls, value: str) -> str:
        return value.lower()


class SourceArtifact(DomainModel):
    schema_version: Literal["source_artifact.v1"] = "source_artifact.v1"
    source_id: NonEmptyStr
    source_uri: NonEmptyStr | None = None
    source_hash: Sha256Hex
    source_title: NonEmptyStr | None = None
    source_publisher: NonEmptyStr | None = None
    source_publication_datetime: NonEmptyStr | None = None
    source_type: SourceType = SourceType.UNKNOWN
    content_type: ContentType = ContentType.UNKNOWN
    business_context: BusinessContext = BusinessContext.UNKNOWN
    public_source_verified: bool
    raw_artifact_ref: NonEmptyStr

    @field_validator("source_hash")
    @classmethod
    def normalize_source_hash(cls, value: str) -> str:
        return value.lower()

    def provenance(self) -> SourceProvenance:
        return SourceProvenance(
            source_id=self.source_id,
            source_hash=self.source_hash,
            artifact_ref=self.raw_artifact_ref,
        )


class BoundingBox(DomainModel):
    schema_version: Literal["bounding_box.v1"] = "bounding_box.v1"
    x0: float
    y0: float
    x1: float
    y1: float

    @model_validator(mode="after")
    def validate_order(self) -> "BoundingBox":
        if self.x1 < self.x0 or self.y1 < self.y0:
            raise ValueError("bounding box max coordinates must be >= min coordinates")
        return self


class ProvenanceRef(DomainModel):
    """A resolvable pointer to a source span or a table cell."""

    schema_version: Literal["provenance_ref.v1"] = "provenance_ref.v1"
    source_id: NonEmptyStr
    source_hash: Sha256Hex
    page_number: Annotated[int, Field(ge=1)]
    span_id: NonEmptyStr | None = None
    table_id: NonEmptyStr | None = None
    row_index: Annotated[int, Field(ge=0)] | None = None
    column_index: Annotated[int, Field(ge=0)] | None = None

    @field_validator("source_hash")
    @classmethod
    def normalize_source_hash(cls, value: str) -> str:
        return value.lower()

    @model_validator(mode="after")
    def require_resolvable_locator(self) -> "ProvenanceRef":
        has_span = self.span_id is not None
        table_parts = (self.table_id, self.row_index, self.column_index)
        has_any_table = any(part is not None for part in table_parts)
        has_complete_table = all(part is not None for part in table_parts)
        if not has_span and not has_complete_table:
            raise ValueError("provenance must identify a span or complete table cell")
        if has_any_table and not has_complete_table:
            raise ValueError("table provenance requires table_id, row_index and column_index")
        return self


class SourceSpan(DomainModel):
    schema_version: Literal["source_span.v1"] = "source_span.v1"
    span_id: NonEmptyStr
    source: SourceProvenance
    text: NonEmptyStr
    page_number: Annotated[int, Field(ge=1)]
    section: NonEmptyStr | None = None
    bbox: BoundingBox | None = None
    table_ref: NonEmptyStr | None = None

    def provenance_ref(self) -> ProvenanceRef:
        return ProvenanceRef(
            source_id=self.source.source_id,
            source_hash=self.source.source_hash,
            page_number=self.page_number,
            span_id=self.span_id,
        )


class TableCellProvenance(DomainModel):
    schema_version: Literal["table_cell_provenance.v1"] = "table_cell_provenance.v1"
    source: SourceProvenance
    table_id: NonEmptyStr
    row_index: Annotated[int, Field(ge=0)]
    column_index: Annotated[int, Field(ge=0)]
    page_number: Annotated[int, Field(ge=1)]
    raw_value: NonEmptyStr
    normalized_value: JsonValue | None = None
    row_label: NonEmptyStr | None = None
    column_label: NonEmptyStr | None = None
    bbox: BoundingBox | None = None

    def provenance_ref(self) -> ProvenanceRef:
        return ProvenanceRef(
            source_id=self.source.source_id,
            source_hash=self.source.source_hash,
            page_number=self.page_number,
            table_id=self.table_id,
            row_index=self.row_index,
            column_index=self.column_index,
        )


class ExtractionWarning(DomainModel):
    schema_version: Literal["extraction_warning.v1"] = "extraction_warning.v1"
    warning_code: NonEmptyStr
    message: NonEmptyStr
    source_ref: ProvenanceRef | None = None


class ParsedDocument(DomainModel):
    schema_version: Literal["parsed_document.v1"] = "parsed_document.v1"
    document_id: NonEmptyStr
    source: SourceProvenance
    parser_version: VersionStr
    spans: Annotated[tuple[SourceSpan, ...], Field(min_length=1)]
    table_cells: tuple[TableCellProvenance, ...] = ()
    warnings: tuple[ExtractionWarning, ...] = ()
    coverage_metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_source_lineage(self) -> "ParsedDocument":
        expected = (self.source.source_id, self.source.source_hash)
        for item in (*self.spans, *self.table_cells):
            observed = (item.source.source_id, item.source.source_hash)
            if observed != expected:
                raise ValueError("parsed document children must share document source provenance")
        return self


class Anchor(DomainModel):
    schema_version: Literal["anchor.v1"] = "anchor.v1"
    anchor_id: NonEmptyStr
    kind: AnchorKind
    normalized_value: JsonValue
    surface_value: NonEmptyStr
    semantic_role: NonEmptyStr | None = None
    provenance: Annotated[tuple[ProvenanceRef, ...], Field(min_length=1)]
    source_trust: SourceTrust
    materiality: Materiality


class VariantSpec(DomainModel):
    schema_version: Literal["variant_spec.v1"] = "variant_spec.v1"
    job_id: NonEmptyStr
    audience: AudienceLevel
    format: OutputFormat
    prompt_version: VersionStr
    output_schema_version: VersionStr
    source: SourceProvenance
    source_backbone_ref: NonEmptyStr
    policy_context_ref: NonEmptyStr


class Failure(DomainModel):
    schema_version: Literal["failure.v1"] = "failure.v1"
    failure_code: NonEmptyStr
    severity: FailureSeverity
    category: FailureCategory
    evidence_refs: Annotated[tuple[NonEmptyStr, ...], Field(min_length=1)]
    observed: JsonValue | None = None
    target_or_config: JsonValue | None = None
    repairable: bool
    repair_hint: NonEmptyStr | None = None


class CheckResult(DomainModel):
    schema_version: Literal["check_result.v1"] = "check_result.v1"
    check_code: NonEmptyStr
    status: GateStatus
    evidence_refs: tuple[NonEmptyStr, ...] = ()
    details: dict[str, JsonValue] = Field(default_factory=dict)


class RepairInstruction(DomainModel):
    schema_version: Literal["repair_instruction.v1"] = "repair_instruction.v1"
    instruction_code: NonEmptyStr
    failure_codes: Annotated[tuple[NonEmptyStr, ...], Field(min_length=1)]
    instruction: NonEmptyStr


class HardGateResults(DomainModel):
    schema_version: Literal["hard_gate_results.v1"] = "hard_gate_results.v1"
    source_trust: GateStatus
    factuality: GateStatus
    required_concepts: GateStatus
    policy: GateStatus
    format_contract: GateStatus
    audience_contract: GateStatus


class EvalReport(DomainModel):
    schema_version: Literal["eval_report.v1"] = "eval_report.v1"
    output_id: NonEmptyStr
    evaluator_version: VersionStr
    status: EvalStatus
    hard_gates: HardGateResults
    predicted_audience: AudienceLevel | None = None
    features: dict[str, JsonValue] = Field(default_factory=dict)
    checks: tuple[CheckResult, ...] = ()
    failures: tuple[Failure, ...] = ()
    repair_plan: tuple[RepairInstruction, ...] = ()
    source_refs: Annotated[tuple[ProvenanceRef, ...], Field(min_length=1)]
    calibration_version: VersionStr | None = None

    @model_validator(mode="after")
    def protect_non_compensatory_pass(self) -> "EvalReport":
        if self.status == EvalStatus.PASS:
            bad_gate = any(
                status != GateStatus.PASS
                for status in (
                    self.hard_gates.source_trust,
                    self.hard_gates.factuality,
                    self.hard_gates.required_concepts,
                    self.hard_gates.policy,
                    self.hard_gates.format_contract,
                    self.hard_gates.audience_contract,
                )
            )
            blocking_failure = any(
                failure.severity in {FailureSeverity.CRITICAL, FailureSeverity.ERROR}
                for failure in self.failures
            )
            if bad_gate or blocking_failure:
                raise ValueError("PASS cannot coexist with unresolved hard-gate or blocking failures")
        return self


class ComponentVersions(DomainModel):
    """Version spine. Nullable fields are explicit when a component has not run yet."""

    schema_version: Literal["component_versions.v1"] = "component_versions.v1"
    contract_version: VersionStr
    parser_version: VersionStr | None = None
    prompt_version: VersionStr | None = None
    output_schema_version: VersionStr | None = None
    evaluator_version: VersionStr | None = None
    ontology_version: VersionStr | None = None
    policy_version: VersionStr | None = None
    model_version: VersionStr | None = None
    semantic_backend_version: VersionStr | None = None
    pricing_version: VersionStr | None = None


class RunManifest(DomainModel):
    schema_version: Literal["run_manifest.v1"] = "run_manifest.v1"
    run_id: NonEmptyStr
    attempt_id: NonEmptyStr
    attempt_kind: AttemptKind
    source: SourceProvenance
    versions: ComponentVersions
    status: RunStatus
    variant_job_ids: tuple[NonEmptyStr, ...] = ()
    output_refs: dict[str, NonEmptyStr] = Field(default_factory=dict)
    evaluation_refs: dict[str, NonEmptyStr] = Field(default_factory=dict)
    telemetry_refs: tuple[NonEmptyStr, ...] = ()
    failure_codes: tuple[NonEmptyStr, ...] = ()
    metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_job_ref_integrity(self) -> "RunManifest":
        if len(self.variant_job_ids) != len(set(self.variant_job_ids)):
            raise ValueError("variant_job_ids must be unique")
        known = set(self.variant_job_ids)
        referenced = set(self.output_refs) | set(self.evaluation_refs)
        if referenced and not known:
            raise ValueError("output/evaluation refs require declared variant_job_ids")
        unknown = referenced - known
        if unknown:
            raise ValueError(f"refs point to undeclared variant jobs: {sorted(unknown)}")
        return self
