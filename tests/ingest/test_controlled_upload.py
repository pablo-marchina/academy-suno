from __future__ import annotations

from dataclasses import dataclass

from suno_content.ingest import (
    PdfExtraction,
    QuarantineReason,
    UploadRoute,
    ingest_controlled_pdf_bytes,
    preflight_pdf_upload,
    route_extraction,
)


VALID_PDF = b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n"


@dataclass
class StubParser:
    extraction: PdfExtraction

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        assert raw_bytes.startswith(b"%PDF-")
        return self.extraction


def test_preflight_quarantines_invalid_encrypted_and_malformed() -> None:
    invalid = preflight_pdf_upload(b"not a pdf")
    encrypted = preflight_pdf_upload(b"%PDF-1.7\n/Encrypt true\n%%EOF\n")
    malformed = preflight_pdf_upload(b"%PDF-1.7\ntruncated")

    assert invalid.route is UploadRoute.QUARANTINED
    assert invalid.quarantine_reason is QuarantineReason.INVALID_PDF_SIGNATURE
    assert encrypted.quarantine_reason is QuarantineReason.ENCRYPTED
    assert malformed.quarantine_reason is QuarantineReason.MALFORMED


def test_source_group_is_stable_across_byte_variants_without_losing_hash_identity() -> None:
    first = preflight_pdf_upload(VALID_PDF, source_group_key="BCB Copom 277")
    second = preflight_pdf_upload(VALID_PDF + b" ", source_group_key="BCB Copom 277")

    assert first.source_group_id == second.source_group_id
    assert first.source_hash != second.source_hash
    assert first.provenance_ref == f"sha256:{first.source_hash}"
    assert second.provenance_ref == f"sha256:{second.source_hash}"


def test_route_extraction_sends_scan_to_ocr_and_ambiguous_table_to_review() -> None:
    upload = preflight_pdf_upload(VALID_PDF)
    scan = route_extraction(
        upload,
        extracted_text="",
        extraction_confidence=0.45,
        warnings=("NO_TEXT_LAYER_OR_EMPTY_EXTRACTION",),
    )
    table = route_extraction(
        upload,
        extracted_text="Metric | 2026 | 2027",
        extraction_confidence=0.98,
        table_role_ambiguity=True,
    )

    assert scan.route is UploadRoute.OCR_REQUIRED
    assert table.route is UploadRoute.REVIEW_REQUIRED
    assert not scan.accepted_as_trusted_evidence
    assert not table.accepted_as_trusted_evidence


def test_controlled_ingest_preserves_hash_and_only_promotes_canonical_ready_source() -> None:
    parser = StubParser(
        PdfExtraction(
            text="Narrative evidence without tabular role ambiguity. " * 4,
            parser_name="stub",
            parser_version="1",
            page_count=1,
            confidence=0.98,
        )
    )
    result = ingest_controlled_pdf_bytes(
        VALID_PDF,
        artifact_label="public/bcb.pdf",
        source_group_key="BCB Copom 277",
        parser=parser,
    )

    assert result.ingest is not None
    assert result.upload.source_hash == result.ingest.source_hash
    assert result.ingest.source_status == "SOURCE_READY"
    assert result.upload.route is UploadRoute.SOURCE_READY


def test_controlled_ingest_never_promotes_ambiguous_table() -> None:
    parser = StubParser(
        PdfExtraction(
            text="Metric | 2026 | 2027\nIPCA | 3,9 | 3,3",
            parser_name="stub",
            parser_version="1",
            page_count=1,
            confidence=0.98,
            warnings=("TABLE_ROLE_AMBIGUITY:TEXT_LAYER_HAS_NO_CELL_ROLE_PROVENANCE",),
            table_role_ambiguity=True,
        )
    )
    result = ingest_controlled_pdf_bytes(VALID_PDF, parser=parser)

    assert result.ingest is not None
    assert result.ingest.source_status == "SOURCE_BLOCKED"
    assert result.upload.route is UploadRoute.REVIEW_REQUIRED
    assert not result.upload.accepted_as_trusted_evidence
