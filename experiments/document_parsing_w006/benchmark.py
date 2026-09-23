"""W006-T004 source-group-aware financial document parser/OCR bakeoff.

The harness reconstructs role-sensitive semantic seeds from two first-party public
financial sources into deterministic test PDFs, derives scan/encrypted/malformed
variants, and records immutable hashes per variant while aggregating sample size by
source group. The reconstruction is diagnostic and is not the original public bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as md
import json
import platform
import shutil
import subprocess
import time
from pathlib import Path
from statistics import median
from typing import Any, Callable

import fitz
import pdfplumber
import pytesseract
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

SOURCES: dict[str, dict[str, Any]] = {
    "bcb-copom-277": {
        "public_url": "https://www.bcb.gov.br/content/copom/atascopom/Copom277-not20260318277.pdf",
        "title": "BCB Copom 277",
        "columns": ["Indice de precos", "2026", "3o tri 2027"],
        "rows": [
            ["IPCA", "3,9", "3,3"],
            ["IPCA livres", "3,7", "3,3"],
            ["IPCA administrados", "4,3", "3,2"],
        ],
        "anchors": ["IPCA", "3,9", "3,3", "IPCA livres", "3,7", "IPCA administrados", "4,3", "3,2"],
        "role_pairs": [["IPCA", "3,9"], ["IPCA", "3,3"], ["IPCA livres", "3,7"], ["IPCA administrados", "4,3"]],
    },
    "petrobras-2t26": {
        "public_url": "https://api.mziq.com/mzfilemanager/v2/d/25fdf098-34f5-4608-b7fa-17d60b2de47d/857e970b-1bf4-9ea4-093f-b93bfc2bac95?origin=2",
        "title": "Petrobras 2T26",
        "columns": ["R$ milhoes", "2T26", "1T26", "2T25", "1S26", "1S25"],
        "rows": [
            ["Lucro liquido - Acionistas Petrobras", "52.445", "32.663", "26.652", "85.108", "61.861"],
            ["EBITDA ajustado", "93.843", "59.643", "52.257", "153.486", "113.341"],
        ],
        "anchors": [
            "Lucro liquido - Acionistas Petrobras", "52.445", "32.663", "26.652", "85.108", "61.861",
            "EBITDA ajustado", "93.843", "59.643", "52.257", "153.486", "113.341",
        ],
        "role_pairs": [["Lucro liquido - Acionistas Petrobras", "52.445"], ["EBITDA ajustado", "93.843"]],
    },
}


def _version(name: str) -> str:
    try:
        return md.version(name)
    except md.PackageNotFoundError:
        return "unavailable"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalize(text: str) -> str:
    for before, after in {
        "Í": "I", "í": "i", "ç": "c", "Ç": "C", "õ": "o", "ã": "a",
        "º": "o", "á": "a", "é": "e", "ú": "u", "ô": "o",
    }.items():
        text = text.replace(before, after)
    return " ".join(text.split()).lower()


def generate_digital(spec: dict[str, Any], path: Path) -> None:
    pdf = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(20 * mm, height - 20 * mm, f"{spec['title']} - benchmark reconstruction")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(20 * mm, height - 28 * mm, "Synthetic reconstruction from public-source semantic seeds; NOT original source bytes.")
    data = [spec["columns"]] + spec["rows"]
    remaining = len(spec["columns"]) - 1
    widths = [65 * mm] + [130 * mm / remaining] * remaining
    table = Table(data, colWidths=widths, rowHeights=8 * mm)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 20 * mm, height - 80 * mm)
    pdf.save()


def generate_scan(source: Path, target: Path) -> None:
    document = fitz.open(source)
    pixmap = document[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
    image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    image.save(target, "PDF", resolution=120.0)


def generate_encrypted(source: Path, target: Path) -> None:
    reader = PdfReader(str(source))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt("academy-suno-benchmark")
    with target.open("wb") as stream:
        writer.write(stream)


def _timed(function: Callable[[], Any], repetitions: int = 3) -> tuple[float, Any]:
    timings: list[float] = []
    result: Any = None
    for _ in range(repetitions):
        start = time.perf_counter()
        result = function()
        timings.append((time.perf_counter() - start) * 1000)
    return median(timings), result


def pypdf_text(path: Path) -> tuple[str, list[Any], float]:
    def run() -> tuple[str, list[Any]]:
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages), []
    latency, result = _timed(run)
    text, tables = result
    return text, tables, latency


def pdftotext_layout(path: Path) -> tuple[str, list[Any], float]:
    executable = shutil.which("pdftotext")
    if not executable:
        raise RuntimeError("pdftotext unavailable")
    def run() -> tuple[str, list[Any]]:
        process = subprocess.run([executable, "-layout", str(path), "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if process.returncode:
            raise RuntimeError(process.stderr.decode("utf-8", "replace"))
        return process.stdout.decode("utf-8", "replace"), []
    latency, result = _timed(run)
    text, tables = result
    return text, tables, latency


def pymupdf_tables(path: Path) -> tuple[str, list[Any], float]:
    def run() -> tuple[str, list[Any]]:
        document = fitz.open(path)
        texts: list[str] = []
        tables: list[Any] = []
        for page in document:
            texts.append(page.get_text("text", sort=True))
            tables.extend(table.extract() for table in page.find_tables().tables)
        return "\n".join(texts), tables
    latency, result = _timed(run)
    text, tables = result
    return text, tables, latency


def pdfplumber_tables(path: Path) -> tuple[str, list[Any], float]:
    def run() -> tuple[str, list[Any]]:
        texts: list[str] = []
        tables: list[Any] = []
        with pdfplumber.open(path) as document:
            for page in document.pages:
                texts.append(page.extract_text() or "")
                tables.extend(page.extract_tables() or [])
        return "\n".join(texts), tables
    latency, result = _timed(run)
    text, tables = result
    return text, tables, latency


def tesseract_text(path: Path) -> tuple[str, list[Any], float]:
    if not shutil.which("tesseract"):
        raise RuntimeError("tesseract unavailable")
    def run() -> tuple[str, list[Any]]:
        document = fitz.open(path)
        texts: list[str] = []
        for page in document:
            pixmap = page.get_pixmap(matrix=fitz.Matrix(4, 4), alpha=False)
            image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            texts.append(pytesseract.image_to_string(image, config="--psm 4"))
        return "\n".join(texts), []
    latency, result = _timed(run, repetitions=1)
    text, tables = result
    return text, tables, latency


PARSERS = {
    "pypdf_text": pypdf_text,
    "pdftotext_layout": pdftotext_layout,
    "pymupdf_find_tables": pymupdf_tables,
    "pdfplumber_tables": pdfplumber_tables,
    "tesseract_ocr_text": tesseract_text,
}


def _metrics(spec: dict[str, Any], text: str, tables: list[Any]) -> tuple[float, float, list[str], list[list[str]]]:
    normalized = _normalize(text)
    anchor_hits = [anchor for anchor in spec["anchors"] if _normalize(anchor) in normalized]
    rows = [" | ".join("" if cell is None else str(cell) for cell in row) for table in tables for row in (table or [])]
    role_hits = [pair for pair in spec["role_pairs"] if any(_normalize(pair[0]) in _normalize(row) and _normalize(pair[1]) in _normalize(row) for row in rows)]
    return (
        round(len(anchor_hits) / len(spec["anchors"]), 4),
        round(len(role_hits) / len(spec["role_pairs"]), 4),
        anchor_hits,
        role_hits,
    )


def _preflight(path: Path) -> tuple[str, str | None]:
    raw = path.read_bytes()
    if b"/Encrypt" in raw:
        return "QUARANTINED", "ENCRYPTED"
    if b"%%EOF" not in raw[-4096:]:
        return "QUARANTINED", "MALFORMED"
    return "PARSER_READY", None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("artifacts/document_parsing_w006"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []

    for source_group_id, spec in SOURCES.items():
        digital = args.out / f"{source_group_id}-digital.pdf"
        scanned = args.out / f"{source_group_id}-scanned.pdf"
        encrypted = args.out / f"{source_group_id}-encrypted.pdf"
        malformed = args.out / f"{source_group_id}-malformed.pdf"
        generate_digital(spec, digital)
        generate_scan(digital, scanned)
        generate_encrypted(digital, encrypted)
        malformed.write_bytes(digital.read_bytes()[:-64])

        for variant, path in (("digital", digital), ("scanned", scanned), ("encrypted", encrypted), ("malformed", malformed)):
            route, reason = _preflight(path)
            variants.append({
                "source_group_id": source_group_id,
                "variant": variant,
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
                "preflight_route": route,
                "quarantine_reason": reason,
            })

        for variant, path in (("digital", digital), ("scanned", scanned)):
            for name, function in PARSERS.items():
                row: dict[str, Any] = {
                    "source_group_id": source_group_id,
                    "variant": variant,
                    "sha256": _sha256(path),
                    "parser": name,
                    "external_service_cost_usd_observed": 0.0,
                    "compute_cost_measured": False,
                }
                try:
                    text, tables, latency = function(path)
                    anchor_recall, role_recall, anchor_hits, role_hits = _metrics(spec, text, tables)
                    row.update({
                        "status": "OK",
                        "latency_ms_median": round(latency, 2),
                        "text_anchor_recall": anchor_recall,
                        "structured_role_pair_recall": role_recall,
                        "text_chars": len(text),
                        "table_count": len(tables),
                        "anchor_hits": anchor_hits,
                        "role_pair_hits": role_hits,
                    })
                except Exception as exc:
                    row.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
                results.append(row)

    pdftotext_version = "unavailable"
    if shutil.which("pdftotext"):
        version_run = subprocess.run(["pdftotext", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        version_lines = (version_run.stderr or version_run.stdout).splitlines()
        pdftotext_version = version_lines[0] if version_lines else "system"
    tesseract_version = "unavailable"
    if shutil.which("tesseract"):
        version_run = subprocess.run(["tesseract", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        version_lines = version_run.stdout.splitlines()
        tesseract_version = version_lines[0] if version_lines else "system"

    observations = {
        "benchmark_version": "w006-t004-local-0.1",
        "executed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scope": "public-source-semantic reconstruction bakeoff; source-original bytes unavailable in worker runtime; no production winner claim",
        "source_group_count": len(SOURCES),
        "variant_count": len(variants),
        "source_groups": SOURCES,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "pypdf": _version("pypdf"),
            "pymupdf": _version("PyMuPDF"),
            "pdfplumber": _version("pdfplumber"),
            "pytesseract": _version("pytesseract"),
            "reportlab": _version("reportlab"),
            "pillow": _version("Pillow"),
            "pdftotext": pdftotext_version,
            "tesseract": tesseract_version,
        },
        "variants": variants,
        "results": results,
    }
    output = args.out / "raw_observations.json"
    output.write_text(json.dumps(observations, indent=2, ensure_ascii=False), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
