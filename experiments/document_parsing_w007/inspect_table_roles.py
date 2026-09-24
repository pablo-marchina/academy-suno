from __future__ import annotations

import io
import json
import urllib.request
from pathlib import Path

URL = "https://api.mziq.com/mzfilemanager/v2/d/25fdf098-34f5-4608-b7fa-17d60b2de47d/857e970b-1bf4-9ea4-093f-b93bfc2bac95?origin=2"
PAGE_INDEX = 4


def fetch() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "academy-suno-w007-t004/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def main() -> None:
    import fitz
    import pdfplumber

    raw = fetch()
    doc = fitz.open(stream=raw, filetype="pdf")
    page = doc[PAGE_INDEX]
    pymupdf = []
    for ti, table in enumerate(page.find_tables().tables):
        pymupdf.append({"table_index": ti, "cells": table.extract()})

    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        plumber = [
            {"table_index": ti, "cells": matrix}
            for ti, matrix in enumerate(pdf.pages[PAGE_INDEX].extract_tables() or [])
        ]

    payload = {
        "source_group_id": "petrobras-2t26",
        "page_number": 5,
        "purpose": "diagnostic_only_separate_parser_structure_from_evaluator_failure",
        "pymupdf": pymupdf,
        "pdfplumber": plumber,
    }
    out = Path("/tmp/w007-t004-evidence/table_diagnostics.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
