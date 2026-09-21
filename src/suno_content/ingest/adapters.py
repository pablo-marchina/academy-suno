from __future__ import annotations

import io
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Protocol, runtime_checkable


class PdfParserError(RuntimeError):
    """Base error for replaceable PDF parser adapters."""


class PdfParserUnavailable(PdfParserError):
    """Raised when a parser implementation is not installed/available."""


@dataclass(frozen=True, slots=True)
class PdfExtraction:
    text: str
    parser_name: str
    parser_version: str
    page_count: int
    confidence: float
    warnings: tuple[str, ...] = ()
    table_role_ambiguity: bool = False


@runtime_checkable
class PdfParserAdapter(Protocol):
    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        ...


def detect_table_role_ambiguity(text: str) -> bool:
    """Fail-closed heuristic for text that looks tabular but has no role provenance."""

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.count("|") >= 2 or "\t" in line:
            return True
        if sum(ch.isdigit() for ch in line) >= 2 and re.search(r"\S\s{2,}\S\s{2,}\S", line):
            return True
    return False


def _distribution_version(*names: str) -> str:
    for name in names:
        try:
            return metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return "unknown"


class PypdfAdapter:
    """Text-layer PDF adapter. It intentionally does not claim table-role preservation."""

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        try:
            from pypdf import PdfReader  # type: ignore[import-not-found]

            version = _distribution_version("pypdf")
            parser_name = "pypdf"
        except ImportError:
            try:
                from PyPDF2 import PdfReader  # type: ignore[import-not-found,no-redef]

                version = _distribution_version("PyPDF2")
                parser_name = "PyPDF2"
            except ImportError as exc:
                raise PdfParserUnavailable("pypdf/PyPDF2 is not installed") from exc

        try:
            reader = PdfReader(io.BytesIO(raw_bytes))
            pages = list(reader.pages)
        except Exception as exc:
            raise PdfParserError(f"{parser_name} could not open PDF: {exc}") from exc

        page_texts: list[str] = []
        extraction_failures = 0
        for index, page in enumerate(pages, start=1):
            try:
                page_text = (page.extract_text() or "").strip()
            except Exception:
                page_text = ""
                extraction_failures += 1
            if page_text:
                page_texts.append(f"[page {index}]\n{page_text}")

        text = "\n\n".join(page_texts).strip()
        page_count = len(pages)
        extracted_pages = max(0, page_count - extraction_failures)
        coverage = extracted_pages / page_count if page_count else 0.0
        density_ok = len(text) >= 80
        confidence = min(0.98, 0.68 + 0.28 * coverage) if density_ok else 0.45
        warnings: list[str] = []
        if not text:
            warnings.append("NO_TEXT_LAYER_OR_EMPTY_EXTRACTION")
        if extraction_failures:
            warnings.append(f"PAGE_EXTRACTION_FAILURES:{extraction_failures}")
        if page_count == 0:
            warnings.append("NO_PAGES")

        table_ambiguity = detect_table_role_ambiguity(text)
        if table_ambiguity:
            warnings.append("TABLE_ROLE_AMBIGUITY:TEXT_LAYER_HAS_NO_CELL_ROLE_PROVENANCE")

        return PdfExtraction(
            text=text,
            parser_name=parser_name,
            parser_version=version,
            page_count=page_count,
            confidence=confidence,
            warnings=tuple(warnings),
            table_role_ambiguity=table_ambiguity,
        )


class PdftotextAdapter:
    """Poppler fallback. Useful locally, but still role-ambiguous for tables."""

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        executable = shutil.which("pdftotext")
        if not executable:
            raise PdfParserUnavailable("pdftotext executable is not available")

        with tempfile.TemporaryDirectory(prefix="academy-suno-pdf-") as tmp:
            pdf_path = Path(tmp) / "input.pdf"
            pdf_path.write_bytes(raw_bytes)
            completed = subprocess.run(
                [executable, "-layout", str(pdf_path), "-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        if completed.returncode != 0:
            message = completed.stderr.decode("utf-8", errors="replace").strip()
            raise PdfParserError(f"pdftotext failed: {message or completed.returncode}")

        text = completed.stdout.decode("utf-8", errors="replace").strip()
        confidence = 0.90 if len(text) >= 80 else 0.45
        warnings: list[str] = []
        if not text:
            warnings.append("NO_TEXT_LAYER_OR_EMPTY_EXTRACTION")
        table_ambiguity = detect_table_role_ambiguity(text)
        if table_ambiguity:
            warnings.append("TABLE_ROLE_AMBIGUITY:TEXT_LAYOUT_HAS_NO_CELL_ROLE_PROVENANCE")
        return PdfExtraction(
            text=text,
            parser_name="pdftotext",
            parser_version="system",
            page_count=max(1, text.count("\f") + 1) if text else 0,
            confidence=confidence,
            warnings=tuple(warnings),
            table_role_ambiguity=table_ambiguity,
        )


class AutoPdfAdapter:
    """Ordered adapter chain. The first successful parser wins only for this run.

    This is an operational fallback, not a parser-quality winner selection.
    """

    def __init__(self, adapters: tuple[PdfParserAdapter, ...] | None = None) -> None:
        self.adapters = adapters or (PypdfAdapter(), PdftotextAdapter())

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        errors: list[str] = []
        for adapter in self.adapters:
            try:
                return adapter.parse(raw_bytes)
            except (PdfParserUnavailable, PdfParserError) as exc:
                errors.append(f"{type(adapter).__name__}: {exc}")
        raise PdfParserUnavailable("; ".join(errors) or "no PDF parser adapters configured")
