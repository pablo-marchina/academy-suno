"""W005-T014 reproducible role-sensitive PDF parser micro-benchmark.

This deliberately tests the difference between text/number presence and provable
row/column semantics. It generates a digital PDF and an image-only derivative,
then runs locally available parser classes under the same fixture.

It is a diagnostic bakeoff, not a production-parser selection benchmark.
"""
from __future__ import annotations

import argparse
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
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

GOLD = {
    "copom277_table": {
        "columns": ["Indice de precos", "2026", "3o tri 2027"],
        "rows": [
            ["IPCA", "3,9", "3,3"],
            ["IPCA livres", "3,7", "3,3"],
            ["IPCA administrados", "4,3", "3,2"],
        ],
    },
    "petrobras_2t26_table": {
        "columns": ["R$ milhoes", "2T26", "1T26", "2T25", "1S26", "1S25"],
        "rows": [
            ["Lucro liquido - Acionistas Petrobras", "52.445", "32.663", "26.652", "85.108", "61.861"],
            ["EBITDA ajustado", "93.843", "59.643", "52.257", "153.486", "113.341"],
        ],
    },
}

ANCHORS = [
    "IPCA", "3,9", "3,3", "IPCA livres", "3,7", "IPCA administrados", "4,3", "3,2",
    "Lucro liquido - Acionistas Petrobras", "52.445", "32.663", "26.652", "85.108", "61.861",
    "EBITDA ajustado", "93.843", "59.643", "52.257", "153.486", "113.341",
]
ROLE_PAIRS = [
    ("IPCA", "3,9"), ("IPCA", "3,3"), ("IPCA livres", "3,7"),
    ("IPCA administrados", "4,3"),
    ("Lucro liquido - Acionistas Petrobras", "52.445"),
    ("EBITDA ajustado", "93.843"),
]


def normalize(text: str) -> str:
    for before, after in {
        "Í": "I", "í": "i", "ç": "c", "Ç": "C", "õ": "o", "ã": "a",
        "º": "o", "á": "a", "é": "e", "ú": "u", "ô": "o",
    }.items():
        text = text.replace(before, after)
    return " ".join(text.split()).lower()


def generate_digital_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, height - 20 * mm, "Representative financial parsing fixture")
    c.setFont("Helvetica", 8)
    c.drawString(20 * mm, height - 28 * mm, "Synthetic reconstruction of role-sensitive public financial tables; not source evidence.")

    bcb = [GOLD["copom277_table"]["columns"]] + GOLD["copom277_table"]["rows"]
    table = Table(bcb, colWidths=[65 * mm, 35 * mm, 35 * mm], rowHeights=8 * mm)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 20 * mm, height - 75 * mm)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, height - 83 * mm, "Petrobras-like table")
    petro = [GOLD["petrobras_2t26_table"]["columns"]] + GOLD["petrobras_2t26_table"]["rows"]
    table = Table(petro, colWidths=[65 * mm] + [22 * mm] * 5, rowHeights=8 * mm)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 20 * mm, height - 115 * mm)
    c.save()


def generate_scanned_pdf(source: Path, target: Path) -> None:
    document = fitz.open(source)
    pixmap = document[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
    image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    image.save(target, "PDF", resolution=120.0)


def timed(function: Callable[[], Any], repetitions: int = 3) -> tuple[float, Any]:
    timings, result = [], None
    for _ in range(repetitions):
        start = time.perf_counter()
        result = function()
        timings.append((time.perf_counter() - start) * 1000)
    return median(timings), result


def text_anchor_recall(text: str) -> tuple[float, list[str]]:
    normalized = normalize(text)
    hits = [anchor for anchor in ANCHORS if normalize(anchor) in normalized]
    return len(hits) / len(ANCHORS), hits


def structured_role_recall(tables: list[list[list[Any]]]) -> tuple[float, list[list[str]], list[str]]:
    rows = []
    for table in tables:
        for row in table or []:
            rows.append(" | ".join("" if cell is None else str(cell) for cell in row))
    hits = [[label, value] for label, value in ROLE_PAIRS if any(
        normalize(label) in normalize(row) and normalize(value) in normalize(row) for row in rows
    )]
    return len(hits) / len(ROLE_PAIRS), hits, rows[:20]


def pypdf_text(path: Path):
    def run():
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    latency, text = timed(run)
    return text, [], latency, {"page_count": len(PdfReader(str(path)).pages), "has_cell_coordinates": False}


def pdftotext_layout(path: Path):
    executable = shutil.which("pdftotext")
    if not executable:
        raise RuntimeError("pdftotext executable unavailable")
    def run():
        process = subprocess.run([executable, "-layout", str(path), "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if process.returncode:
            raise RuntimeError(process.stderr.decode("utf-8", "replace"))
        return process.stdout.decode("utf-8", "replace")
    latency, text = timed(run)
    return text, [], latency, {"page_count": max(1, text.count("\f")), "has_cell_coordinates": False}


def pymupdf_tables(path: Path):
    def run():
        document, texts, tables = fitz.open(path), [], []
        for page in document:
            texts.append(page.get_text("text", sort=True))
            tables.extend(table.extract() for table in page.find_tables().tables)
        return "\n".join(texts), tables
    latency, (text, tables) = timed(run)
    return text, tables, latency, {"page_count": fitz.open(path).page_count, "structured_tables": len(tables), "has_cell_coordinates": bool(tables)}


def pdfplumber_tables(path: Path):
    def run():
        texts, tables = [], []
        with pdfplumber.open(path) as document:
            page_count = len(document.pages)
            for page in document.pages:
                texts.append(page.extract_text() or "")
                tables.extend(page.extract_tables() or [])
        return "\n".join(texts), tables, page_count
    latency, (text, tables, page_count) = timed(run)
    return text, tables, latency, {"page_count": page_count, "structured_tables": len(tables), "has_cell_coordinates": bool(tables)}


def tesseract_text(path: Path):
    if not shutil.which("tesseract"):
        raise RuntimeError("tesseract executable unavailable")
    def run():
        document, texts = fitz.open(path), []
        for page in document:
            pixmap = page.get_pixmap(matrix=fitz.Matrix(4, 4), alpha=False)
            image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            texts.append(pytesseract.image_to_string(image, config="--psm 4"))
        return "\n".join(texts)
    latency, text = timed(run, repetitions=1)
    return text, [], latency, {"page_count": fitz.open(path).page_count, "has_cell_coordinates": False, "ocr": True}


PARSERS = {
    "pypdf_text": pypdf_text,
    "pdftotext_layout": pdftotext_layout,
    "pymupdf_find_tables": pymupdf_tables,
    "pdfplumber_tables": pdfplumber_tables,
    "tesseract_ocr_text": tesseract_text,
}


def version(name: str) -> str:
    try:
        return md.version(name)
    except md.PackageNotFoundError:
        return "unavailable"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("artifacts/document_parsing_w005"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    digital, scanned = args.out / "digital.pdf", args.out / "scanned.pdf"
    generate_digital_pdf(digital)
    generate_scanned_pdf(digital, scanned)

    results = []
    for variant, path in (("digital", digital), ("scanned", scanned)):
        for name, function in PARSERS.items():
            try:
                text, tables, latency, metadata = function(path)
                anchor_recall, anchor_hits = text_anchor_recall(text)
                role_recall, role_hits, sample_rows = structured_role_recall(tables)
                results.append({
                    "variant": variant,
                    "parser": name,
                    "latency_ms_median": round(latency, 2),
                    "anchor_recall": round(anchor_recall, 4),
                    "role_pair_recall_structured": round(role_recall, 4),
                    "text_chars": len(text),
                    "table_count": len(tables),
                    "anchor_hits": anchor_hits,
                    "role_pair_hits": role_hits,
                    "sample_rows": sample_rows,
                    "meta": metadata,
                })
            except Exception as exc:
                results.append({"variant": variant, "parser": name, "error": f"{type(exc).__name__}: {exc}"})

    observations = {
        "benchmark_version": "w005-t014-local-0.2",
        "scope": "synthetic role-sensitive micro-benchmark; diagnostic only; not a production parser winner benchmark",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "pypdf": version("pypdf"),
            "pymupdf": version("PyMuPDF"),
            "pdfplumber": version("pdfplumber"),
            "pytesseract": version("pytesseract"),
            "reportlab": version("reportlab"),
            "pillow": version("Pillow"),
        },
        "gold": GOLD,
        "results": results,
    }
    output = args.out / "raw_observations.json"
    output.write_text(json.dumps(observations, indent=2, ensure_ascii=False), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
