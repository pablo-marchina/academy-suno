from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.ingest import PdfExtraction, ingest_pdf_path, ingest_text  # noqa: E402


class StubPdfParser:
    def __init__(self, extraction: PdfExtraction) -> None:
        self.extraction = extraction

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        self.seen = raw_bytes
        return self.extraction


class RecipientIngestTests(unittest.TestCase):
    def test_text_input_reaches_source_ready_and_exact_3x3_plan(self) -> None:
        text = (
            "A companhia divulgou receita de R$ 10 bilhões no trimestre e explicou "
            "as principais premissas operacionais sem estrutura tabular ambígua."
        )
        result = ingest_text(text)
        self.assertEqual(result.source_status, "SOURCE_READY")
        self.assertEqual(result.hard_gate_status.value, "PASS")
        self.assertEqual(result.source_hash, hashlib.sha256(text.encode("utf-8")).hexdigest())
        self.assertEqual(len(result.cells), 9)
        self.assertEqual(len({cell.job_id for cell in result.cells}), 9)
        self.assertTrue(all(cell.evidence_scope == "MECHANICS_ONLY" for cell in result.cells))

    def test_plain_text_table_ambiguity_cannot_become_pass(self) -> None:
        result = ingest_text("Métrica | 1T26 | 2T26\nReceita | 10 | 12")
        self.assertEqual(result.source_status, "SOURCE_BLOCKED")
        self.assertNotEqual(result.hard_gate_status.value, "PASS")
        self.assertTrue(result.table_role_ambiguity)
        self.assertTrue(all(cell.status == "BLOCKED_SOURCE" for cell in result.cells))

    def test_real_pdf_path_boundary_hashes_raw_bytes_and_uses_replaceable_adapter(self) -> None:
        raw = b"%PDF-1.4\n% recipient-app focused fixture\n%%EOF\n"
        extraction = PdfExtraction(
            text=("Texto extraído com conteúdo suficiente para demonstrar o caminho PDF. " * 3).strip(),
            parser_name="focused-test-adapter",
            parser_version="v1",
            page_count=1,
            confidence=0.97,
        )
        parser = StubPdfParser(extraction)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "documento.pdf"
            path.write_bytes(raw)
            result = ingest_pdf_path(path, parser=parser)
        self.assertEqual(result.input_kind, "PDF")
        self.assertEqual(result.source_hash, hashlib.sha256(raw).hexdigest())
        self.assertEqual(result.parser_name, "focused-test-adapter")
        self.assertEqual(result.source_status, "SOURCE_READY")
        self.assertEqual(len(result.cells), 9)
        self.assertEqual(parser.seen, raw)

    def test_low_confidence_pdf_cannot_become_source_ready(self) -> None:
        raw = b"%PDF-1.4\nfixture\n%%EOF\n"
        parser = StubPdfParser(
            PdfExtraction(
                text="texto parcial",
                parser_name="low-confidence",
                parser_version="v1",
                page_count=1,
                confidence=0.60,
                warnings=("LOW_COVERAGE",),
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "low.pdf"
            path.write_bytes(raw)
            result = ingest_pdf_path(path, parser=parser)
        self.assertEqual(result.source_status, "SOURCE_BLOCKED")
        self.assertNotEqual(result.hard_gate_status.value, "PASS")

    def test_table_role_ambiguity_pdf_cannot_become_source_ready(self) -> None:
        raw = b"%PDF-1.4\nfixture\n%%EOF\n"
        parser = StubPdfParser(
            PdfExtraction(
                text="Receita  10  12",
                parser_name="role-ambiguous",
                parser_version="v1",
                page_count=1,
                confidence=0.99,
                warnings=("TABLE_ROLE_AMBIGUITY",),
                table_role_ambiguity=True,
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "table.pdf"
            path.write_bytes(raw)
            result = ingest_pdf_path(path, parser=parser)
        self.assertEqual(result.source_status, "SOURCE_BLOCKED")
        self.assertNotEqual(result.hard_gate_status.value, "PASS")
        self.assertTrue(result.table_role_ambiguity)


if __name__ == "__main__":
    unittest.main()
