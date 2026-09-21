from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from suno_content.domain import AudienceLevel, GateStatus, OutputFormat, SourceProvenance, SourceTrust
from suno_content.generation.contracts import build_3x3_variant_specs

from .adapters import AutoPdfAdapter, PdfExtraction, PdfParserAdapter, detect_table_role_ambiguity

MIN_READY_CONFIDENCE = 0.90
MAX_SOURCE_BYTES = 25 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class ThreeByThreeCell:
    audience: str
    output_format: str
    job_id: str
    status: str
    evidence_scope: str
    preview: str


@dataclass(frozen=True, slots=True)
class IngestResult:
    input_kind: str
    source: SourceProvenance
    artifact_label: str
    parser_name: str
    parser_version: str
    page_count: int
    extraction_confidence: float
    source_trust: SourceTrust
    source_status: str
    hard_gate_status: GateStatus
    warnings: tuple[str, ...]
    table_role_ambiguity: bool
    extracted_text: str
    cells: tuple[ThreeByThreeCell, ...]

    @property
    def source_hash(self) -> str:
        return self.source.source_hash


@dataclass(frozen=True, slots=True)
class IntegratedEvidence:
    mechanics_end_to_end: str
    audience_thresholds: str
    provider_quality_latency_cost: str
    parser_implementation: str
    production_release_readiness: str
    repair_lineage: dict[str, Any]


def _sha256(raw_bytes: bytes) -> str:
    return hashlib.sha256(raw_bytes).hexdigest()


def _source_id(source_hash: str) -> str:
    return f"source-{source_hash[:16]}"


def _clean_artifact_label(label: str) -> str:
    label = label.strip().replace("\\", "/")
    label = re.sub(r"\s+", " ", label)
    return label or "recipient-input"


def _source_provenance(raw_bytes: bytes, artifact_label: str) -> SourceProvenance:
    source_hash = _sha256(raw_bytes)
    return SourceProvenance(
        source_id=_source_id(source_hash),
        source_hash=source_hash,
        artifact_ref=_clean_artifact_label(artifact_label),
    )


def _assess_trust(extraction: PdfExtraction) -> SourceTrust:
    if extraction.table_role_ambiguity or extraction.confidence < 0.75 or not extraction.text.strip():
        return SourceTrust.LOW
    if extraction.confidence < MIN_READY_CONFIDENCE or extraction.warnings:
        return SourceTrust.MEDIUM
    return SourceTrust.HIGH


def _source_ready(extraction: PdfExtraction, trust: SourceTrust) -> bool:
    return (
        bool(extraction.text.strip())
        and extraction.confidence >= MIN_READY_CONFIDENCE
        and not extraction.table_role_ambiguity
        and trust is SourceTrust.HIGH
    )


def _preview(text: str, audience: AudienceLevel, output_format: OutputFormat) -> str:
    normalized = " ".join(text.split())
    excerpt = normalized[:520] + ("…" if len(normalized) > 520 else "")
    audience_hint = {
        AudienceLevel.BEGINNER: "explicação guiada, termos definidos",
        AudienceLevel.INTERMEDIATE: "contexto + relações entre métricas",
        AudienceLevel.ADVANCED: "densidade técnica + premissas explícitas",
    }[audience]
    format_hint = {
        OutputFormat.ARTICLE: "artigo",
        OutputFormat.CAROUSEL: "carrossel",
        OutputFormat.SHORT_VIDEO: "vídeo curto",
    }[output_format]
    return (
        f"[MECHANICS_ONLY] Plano {audience.value} × {output_format.value} "
        f"({format_hint}; {audience_hint}). Fonte: {excerpt}"
    )


def _blocked_cells() -> tuple[ThreeByThreeCell, ...]:
    return tuple(
        ThreeByThreeCell(
            audience=audience.value,
            output_format=output_format.value,
            job_id="BLOCKED_SOURCE",
            status="BLOCKED_SOURCE",
            evidence_scope="MECHANICS_ONLY",
            preview="Source trust gate is not PASS; generation/evaluation must not proceed.",
        )
        for audience in AudienceLevel
        for output_format in OutputFormat
    )


def _ready_cells(source: SourceProvenance, text: str) -> tuple[ThreeByThreeCell, ...]:
    specs = build_3x3_variant_specs(
        source=source,
        source_backbone_ref=f"recipient-ingest/{source.source_id}/extracted-text",
        policy_context_ref="recipient-app/policy-context/pending-runtime-evaluation",
        prompt_version="recipient-mechanics-v1",
        output_schema_version="format-native-v1",
    )
    return tuple(
        ThreeByThreeCell(
            audience=spec.audience.value,
            output_format=spec.format.value,
            job_id=spec.job_id,
            status="PLANNED_MECHANICS_ONLY",
            evidence_scope="MECHANICS_ONLY",
            preview=_preview(text, spec.audience, spec.format),
        )
        for spec in specs
    )


def _result(
    *,
    input_kind: str,
    raw_bytes: bytes,
    artifact_label: str,
    extraction: PdfExtraction,
) -> IngestResult:
    source = _source_provenance(raw_bytes, artifact_label)
    trust = _assess_trust(extraction)
    ready = _source_ready(extraction, trust)
    return IngestResult(
        input_kind=input_kind,
        source=source,
        artifact_label=_clean_artifact_label(artifact_label),
        parser_name=extraction.parser_name,
        parser_version=extraction.parser_version,
        page_count=extraction.page_count,
        extraction_confidence=extraction.confidence,
        source_trust=trust,
        source_status="SOURCE_READY" if ready else "SOURCE_BLOCKED",
        hard_gate_status=GateStatus.PASS if ready else GateStatus.REVIEW_REQUIRED,
        warnings=extraction.warnings,
        table_role_ambiguity=extraction.table_role_ambiguity,
        extracted_text=extraction.text,
        cells=_ready_cells(source, extraction.text) if ready else _blocked_cells(),
    )


def ingest_text(text: str, *, artifact_label: str = "recipient-text-input.txt") -> IngestResult:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text input must not be empty")
    raw_bytes = text.encode("utf-8")
    if len(raw_bytes) > MAX_SOURCE_BYTES:
        raise ValueError("text input exceeds 25 MiB source limit")
    table_ambiguity = detect_table_role_ambiguity(text)
    warnings = (
        ("TABLE_ROLE_AMBIGUITY:PLAIN_TEXT_HAS_NO_CELL_ROLE_PROVENANCE",)
        if table_ambiguity
        else ()
    )
    extraction = PdfExtraction(
        text=text.strip(),
        parser_name="plain-text",
        parser_version="utf-8-v1",
        page_count=1,
        confidence=1.0,
        warnings=warnings,
        table_role_ambiguity=table_ambiguity,
    )
    return _result(
        input_kind="TEXT",
        raw_bytes=raw_bytes,
        artifact_label=artifact_label,
        extraction=extraction,
    )


def ingest_pdf_bytes(
    raw_bytes: bytes,
    *,
    artifact_label: str = "recipient-upload.pdf",
    parser: PdfParserAdapter | None = None,
) -> IngestResult:
    if not raw_bytes:
        raise ValueError("PDF input must not be empty")
    if len(raw_bytes) > MAX_SOURCE_BYTES:
        raise ValueError("PDF input exceeds 25 MiB source limit")
    if not raw_bytes.lstrip().startswith(b"%PDF-"):
        raise ValueError("input does not have a PDF signature")
    adapter = parser or AutoPdfAdapter()
    extraction = adapter.parse(raw_bytes)
    return _result(
        input_kind="PDF",
        raw_bytes=raw_bytes,
        artifact_label=artifact_label,
        extraction=extraction,
    )


def ingest_pdf_path(
    path: str | Path,
    *,
    parser: PdfParserAdapter | None = None,
) -> IngestResult:
    pdf_path = Path(path).expanduser()
    if not pdf_path.is_file():
        raise ValueError(f"PDF path does not exist or is not a file: {pdf_path}")
    raw_bytes = pdf_path.read_bytes()
    return ingest_pdf_bytes(
        raw_bytes,
        artifact_label=f"local-pdf/{pdf_path.name}",
        parser=parser,
    )


def load_integrated_evidence(path: str | Path) -> IntegratedEvidence:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    posture = payload.get("evidence_posture") or {}
    return IntegratedEvidence(
        mechanics_end_to_end=str(posture.get("mechanics_end_to_end", "UNKNOWN")),
        audience_thresholds=str(posture.get("audience_thresholds", "DIAGNOSTIC_ONLY")),
        provider_quality_latency_cost=str(
            posture.get("real_provider_quality_latency_cost", "PRODUCTION_UNKNOWN/BLOCKED")
        ),
        parser_implementation=str(posture.get("parser_implementation", "PENDING/UNLOCKED")),
        production_release_readiness=str(
            posture.get("production_release_readiness", "PENDING_W004_T008")
        ),
        repair_lineage=dict(payload.get("repair_lineage") or {}),
    )
