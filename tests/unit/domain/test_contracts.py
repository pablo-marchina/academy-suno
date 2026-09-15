from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from suno_content.domain import (
    Anchor,
    AnchorKind,
    AttemptKind,
    AudienceLevel,
    ComponentVersions,
    EvalReport,
    EvalStatus,
    Failure,
    FailureCategory,
    FailureSeverity,
    GateStatus,
    HardGateResults,
    Materiality,
    OutputFormat,
    ProvenanceRef,
    RunManifest,
    RunStatus,
    SourceArtifact,
    SourceProvenance,
    SourceSpan,
    SourceTrust,
    TableCellProvenance,
    VariantSpec,
)

SOURCE_HASH = "A" * 64


def source() -> SourceProvenance:
    return SourceProvenance(
        source_id="copom-001",
        source_hash=SOURCE_HASH,
        artifact_ref="artifacts/copom-001.pdf",
    )


def span_ref() -> ProvenanceRef:
    return ProvenanceRef(
        source_id="copom-001",
        source_hash=SOURCE_HASH,
        page_number=2,
        span_id="span-17",
    )


def all_pass_gates() -> HardGateResults:
    return HardGateResults(
        source_trust=GateStatus.PASS,
        factuality=GateStatus.PASS,
        required_concepts=GateStatus.PASS,
        policy=GateStatus.PASS,
        format_contract=GateStatus.PASS,
        audience_contract=GateStatus.PASS,
    )


def test_source_artifact_has_explicit_lineage_and_normalizes_hash() -> None:
    artifact = SourceArtifact(
        source_id="copom-001",
        source_hash=SOURCE_HASH,
        public_source_verified=True,
        raw_artifact_ref="artifacts/copom-001.pdf",
    )

    assert artifact.source_hash == SOURCE_HASH.lower()
    assert artifact.provenance().source_hash == SOURCE_HASH.lower()
    assert artifact.schema_version == "source_artifact.v1"


@pytest.mark.parametrize("missing", ["source_hash", "raw_artifact_ref"])
def test_source_artifact_rejects_missing_required_provenance(missing: str) -> None:
    payload = {
        "source_id": "copom-001",
        "source_hash": SOURCE_HASH,
        "public_source_verified": True,
        "raw_artifact_ref": "artifacts/copom-001.pdf",
    }
    payload.pop(missing)

    with pytest.raises(ValidationError):
        SourceArtifact(**payload)


def test_span_and_table_cell_expose_resolvable_provenance_refs() -> None:
    span = SourceSpan(
        span_id="span-17",
        source=source(),
        text="A taxa Selic foi mantida em 10,50%.",
        page_number=2,
    )
    cell = TableCellProvenance(
        source=source(),
        table_id="table-3",
        row_index=1,
        column_index=2,
        page_number=4,
        raw_value="10,50%",
        normalized_value=10.5,
    )

    assert span.provenance_ref().span_id == "span-17"
    assert cell.provenance_ref().table_id == "table-3"
    assert cell.provenance_ref().row_index == 1


def test_provenance_ref_requires_complete_locator() -> None:
    with pytest.raises(ValidationError):
        ProvenanceRef(
            source_id="copom-001",
            source_hash=SOURCE_HASH,
            page_number=1,
        )

    with pytest.raises(ValidationError):
        ProvenanceRef(
            source_id="copom-001",
            source_hash=SOURCE_HASH,
            page_number=1,
            table_id="table-1",
            row_index=0,
        )


def test_anchor_requires_source_provenance() -> None:
    valid = {
        "anchor_id": "a-1",
        "kind": AnchorKind.PERCENT,
        "normalized_value": 10.5,
        "surface_value": "10,50%",
        "source_trust": SourceTrust.HIGH,
        "materiality": Materiality.CRITICAL,
    }

    with pytest.raises(ValidationError):
        Anchor(**valid, provenance=())

    anchor = Anchor(**valid, provenance=(span_ref(),))
    assert anchor.provenance[0].source_hash == SOURCE_HASH.lower()


def test_variant_spec_keeps_audience_and_format_separate_and_versioned() -> None:
    spec = VariantSpec(
        job_id="job-beginner-article",
        audience=AudienceLevel.BEGINNER,
        format=OutputFormat.ARTICLE,
        prompt_version="prompt.v1",
        output_schema_version="article.v1",
        source=source(),
        source_backbone_ref="backbone/copom-001/v1",
        policy_context_ref="policy/copom-001/v1",
    )

    assert spec.audience is AudienceLevel.BEGINNER
    assert spec.format is OutputFormat.ARTICLE
    assert spec.prompt_version == "prompt.v1"


def test_eval_report_rejects_pass_with_failing_hard_gate() -> None:
    gates = all_pass_gates().model_copy(update={"factuality": GateStatus.FAIL})

    with pytest.raises(ValidationError):
        EvalReport(
            output_id="output-1",
            evaluator_version="eval.v1",
            status=EvalStatus.PASS,
            hard_gates=gates,
            source_refs=(span_ref(),),
        )


def test_failure_and_eval_report_require_evidence_provenance() -> None:
    with pytest.raises(ValidationError):
        Failure(
            failure_code="HF-01",
            severity=FailureSeverity.CRITICAL,
            category=FailureCategory.FACTUAL,
            evidence_refs=(),
            repairable=True,
        )

    with pytest.raises(ValidationError):
        EvalReport(
            output_id="output-1",
            evaluator_version="eval.v1",
            status=EvalStatus.FAIL,
            hard_gates=all_pass_gates(),
            source_refs=(),
        )


def test_canonical_serialization_is_stable_across_mapping_insertion_order() -> None:
    common = dict(
        run_id="run-1",
        attempt_id="attempt-1",
        attempt_kind=AttemptKind.INITIAL,
        source=source(),
        versions=ComponentVersions(contract_version="domain.v1"),
        status=RunStatus.CREATED,
        variant_job_ids=("job-1",),
    )
    first = RunManifest(**common, metadata={"z": 1, "a": {"y": 2, "b": 3}})
    second = RunManifest(**common, metadata={"a": {"b": 3, "y": 2}, "z": 1})

    assert first.canonical_json() == second.canonical_json()
    assert first.canonical_sha256() == second.canonical_sha256()
    assert first.canonical_json() == first.canonical_json()


def test_run_manifest_serializes_unknown_component_versions_explicitly() -> None:
    manifest = RunManifest(
        run_id="run-1",
        attempt_id="attempt-1",
        attempt_kind=AttemptKind.INITIAL,
        source=source(),
        versions=ComponentVersions(contract_version="domain.v1"),
        status=RunStatus.CREATED,
    )

    data = json.loads(manifest.canonical_json())
    versions = data["versions"]
    assert versions["contract_version"] == "domain.v1"
    assert "parser_version" in versions and versions["parser_version"] is None
    assert "model_version" in versions and versions["model_version"] is None
    assert "semantic_backend_version" in versions and versions["semantic_backend_version"] is None


def test_run_manifest_rejects_refs_to_undeclared_jobs() -> None:
    with pytest.raises(ValidationError):
        RunManifest(
            run_id="run-1",
            attempt_id="attempt-1",
            attempt_kind=AttemptKind.INITIAL,
            source=source(),
            versions=ComponentVersions(contract_version="domain.v1"),
            status=RunStatus.EVALUATING,
            variant_job_ids=("job-1",),
            output_refs={"job-2": "outputs/job-2.json"},
        )
