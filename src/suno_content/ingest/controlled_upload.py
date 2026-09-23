from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from enum import Enum
from typing import Any

MAX_UPLOAD_BYTES = 25 * 1024 * 1024
MIN_READY_CONFIDENCE = 0.90


class UploadRoute(str, Enum):
    QUARANTINED = "QUARANTINED"
    PARSER_READY = "PARSER_READY"
    OCR_REQUIRED = "OCR_REQUIRED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    SOURCE_READY = "SOURCE_READY"


class QuarantineReason(str, Enum):
    EMPTY = "EMPTY"
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    INVALID_PDF_SIGNATURE = "INVALID_PDF_SIGNATURE"
    ENCRYPTED = "ENCRYPTED"
    MALFORMED = "MALFORMED"
    ACTIVE_CONTENT = "ACTIVE_CONTENT"
    PARSER_FAILURE = "PARSER_FAILURE"


@dataclass(frozen=True, slots=True)
class ControlledUploadRecord:
    artifact_label: str
    media_type: str
    byte_count: int
    source_hash: str
    source_group_id: str
    provenance_ref: str
    route: UploadRoute
    quarantine_reason: QuarantineReason | None = None
    detail: str | None = None

    @property
    def accepted_for_parsing(self) -> bool:
        return self.route is UploadRoute.PARSER_READY

    @property
    def accepted_as_trusted_evidence(self) -> bool:
        return self.route is UploadRoute.SOURCE_READY


@dataclass(frozen=True, slots=True)
class ControlledIngestResult:
    upload: ControlledUploadRecord
    ingest: Any | None


def _sha256(raw_bytes: bytes) -> str:
    return hashlib.sha256(raw_bytes).hexdigest()


def _clean_label(label: str) -> str:
    cleaned = re.sub(r"\s+", " ", str(label).strip().replace("\\", "/"))
    return cleaned or "recipient-upload.pdf"


def _group_id(source_group_key: str | None, source_hash: str) -> str:
    if source_group_key is None or not str(source_group_key).strip():
        return f"sg-{source_hash[:16]}"
    normalized = " ".join(str(source_group_key).strip().lower().split())
    return f"sg-{hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:16]}"


def _quarantine(
    *,
    raw_bytes: bytes,
    artifact_label: str,
    source_group_key: str | None,
    reason: QuarantineReason,
    detail: str,
) -> ControlledUploadRecord:
    source_hash = _sha256(raw_bytes)
    return ControlledUploadRecord(
        artifact_label=_clean_label(artifact_label),
        media_type="application/pdf",
        byte_count=len(raw_bytes),
        source_hash=source_hash,
        source_group_id=_group_id(source_group_key, source_hash),
        provenance_ref=f"sha256:{source_hash}",
        route=UploadRoute.QUARANTINED,
        quarantine_reason=reason,
        detail=detail,
    )


def preflight_pdf_upload(
    raw_bytes: bytes,
    *,
    artifact_label: str = "recipient-upload.pdf",
    source_group_key: str | None = None,
    max_bytes: int = MAX_UPLOAD_BYTES,
) -> ControlledUploadRecord:
    """Fail closed before an untrusted PDF reaches a parser.

    ``source_group_key`` groups byte variants derived from the same public source so
    benchmark/reliability accounting cannot inflate N with mutations of one document.
    The immutable byte hash remains the provenance identity for every variant.
    """

    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise TypeError("PDF upload must be bytes")
    raw_bytes = bytes(raw_bytes)
    if not raw_bytes:
        return _quarantine(
            raw_bytes=raw_bytes,
            artifact_label=artifact_label,
            source_group_key=source_group_key,
            reason=QuarantineReason.EMPTY,
            detail="zero-byte upload",
        )
    if len(raw_bytes) > max_bytes:
        return _quarantine(
            raw_bytes=raw_bytes,
            artifact_label=artifact_label,
            source_group_key=source_group_key,
            reason=QuarantineReason.LIMIT_EXCEEDED,
            detail=f"upload exceeds {max_bytes} bytes",
        )
    head = raw_bytes[:1024].lstrip()
    if not head.startswith(b"%PDF-"):
        return _quarantine(
            raw_bytes=raw_bytes,
            artifact_label=artifact_label,
            source_group_key=source_group_key,
            reason=QuarantineReason.INVALID_PDF_SIGNATURE,
            detail="missing PDF signature in first 1024 bytes",
        )

    # Conservative preflight: the parser still validates full PDF syntax.
    if b"/Encrypt" in raw_bytes:
        return _quarantine(
            raw_bytes=raw_bytes,
            artifact_label=artifact_label,
            source_group_key=source_group_key,
            reason=QuarantineReason.ENCRYPTED,
            detail="encrypted PDFs require an explicit decrypt/review workflow",
        )
    active_tokens = (b"/JavaScript", b"/JS ", b"/Launch", b"/EmbeddedFile")
    if any(token in raw_bytes for token in active_tokens):
        return _quarantine(
            raw_bytes=raw_bytes,
            artifact_label=artifact_label,
            source_group_key=source_group_key,
            reason=QuarantineReason.ACTIVE_CONTENT,
            detail="active/embedded content token detected",
        )
    if b"%%EOF" not in raw_bytes[-4096:]:
        return _quarantine(
            raw_bytes=raw_bytes,
            artifact_label=artifact_label,
            source_group_key=source_group_key,
            reason=QuarantineReason.MALFORMED,
            detail="PDF EOF marker missing from bounded tail scan",
        )

    source_hash = _sha256(raw_bytes)
    return ControlledUploadRecord(
        artifact_label=_clean_label(artifact_label),
        media_type="application/pdf",
        byte_count=len(raw_bytes),
        source_hash=source_hash,
        source_group_id=_group_id(source_group_key, source_hash),
        provenance_ref=f"sha256:{source_hash}",
        route=UploadRoute.PARSER_READY,
    )


def route_extraction(
    upload: ControlledUploadRecord,
    *,
    extracted_text: str,
    extraction_confidence: float,
    warnings: tuple[str, ...] = (),
    table_role_ambiguity: bool = False,
) -> ControlledUploadRecord:
    """Promote only provenance-bound, unambiguous extraction; otherwise route deterministically."""

    if upload.route is not UploadRoute.PARSER_READY:
        return upload
    if not extracted_text.strip() or "NO_TEXT_LAYER_OR_EMPTY_EXTRACTION" in warnings:
        return replace(upload, route=UploadRoute.OCR_REQUIRED, detail="no trusted text layer")
    if table_role_ambiguity or any("TABLE_ROLE_AMBIGUITY" in item for item in warnings):
        return replace(upload, route=UploadRoute.REVIEW_REQUIRED, detail="table/OCR roles are ambiguous")
    if extraction_confidence < MIN_READY_CONFIDENCE or warnings:
        return replace(upload, route=UploadRoute.REVIEW_REQUIRED, detail="extraction did not clear trust gate")
    return replace(upload, route=UploadRoute.SOURCE_READY, detail="source trust gate passed")


def ingest_controlled_pdf_bytes(
    raw_bytes: bytes,
    *,
    artifact_label: str = "recipient-upload.pdf",
    source_group_key: str | None = None,
    parser: Any | None = None,
) -> ControlledIngestResult:
    """Controlled recipient upload path wrapping the existing canonical ingest service."""

    upload = preflight_pdf_upload(
        raw_bytes,
        artifact_label=artifact_label,
        source_group_key=source_group_key,
    )
    if not upload.accepted_for_parsing:
        return ControlledIngestResult(upload=upload, ingest=None)

    from .adapters import PdfParserError, PdfParserUnavailable
    from .service import ingest_pdf_bytes

    try:
        ingest = ingest_pdf_bytes(raw_bytes, artifact_label=artifact_label, parser=parser)
    except (PdfParserError, PdfParserUnavailable, ValueError) as exc:
        failed = replace(
            upload,
            route=UploadRoute.QUARANTINED,
            quarantine_reason=QuarantineReason.PARSER_FAILURE,
            detail=f"{type(exc).__name__}: {exc}",
        )
        return ControlledIngestResult(upload=failed, ingest=None)

    if ingest.source_hash != upload.source_hash:
        raise RuntimeError("source hash mismatch between upload preflight and canonical ingest")
    routed = route_extraction(
        upload,
        extracted_text=ingest.extracted_text,
        extraction_confidence=ingest.extraction_confidence,
        warnings=ingest.warnings,
        table_role_ambiguity=ingest.table_role_ambiguity,
    )
    # Canonical source gate is authoritative; never let the wrapper over-promote.
    if routed.route is UploadRoute.SOURCE_READY and ingest.source_status != "SOURCE_READY":
        routed = replace(routed, route=UploadRoute.REVIEW_REQUIRED, detail="canonical source gate did not pass")
    return ControlledIngestResult(upload=routed, ingest=ingest)
