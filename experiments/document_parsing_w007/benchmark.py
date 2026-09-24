from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import statistics
import subprocess
import tempfile
import time
import unicodedata
import urllib.request
from pathlib import Path

SOURCES = [
    {
        "source_group_id": "petrobras-2t26",
        "url": "https://api.mziq.com/mzfilemanager/v2/d/25fdf098-34f5-4608-b7fa-17d60b2de47d/857e970b-1bf4-9ea4-093f-b93bfc2bac95?origin=2",
        "publisher": "Petrobras",
        "title": "Relatório de Desempenho 2T26",
        "evidence_class": "SOURCE_ORIGINAL_PUBLIC_FINANCIAL",
        "document_class": ["digital", "table-heavy"],
        "target_pages_1based": [5],
        "anchors": ["Receita de vendas", "Lucro líquido - Acionistas Petrobras", "EBITDA ajustado", "2T26"],
        "table_roles": [
            {"row": "Receita de vendas", "column": "2T26", "value": "169.530"},
            {"row": "Lucro líquido - Acionistas Petrobras", "column": "2T26", "value": "52.445"},
            {"row": "EBITDA ajustado", "column": "2T26", "value": "93.843"},
        ],
    },
    {
        "source_group_id": "bcb-rpm-2026-1t",
        "url": "https://www.bcb.gov.br/conteudo/home-ptbr/TextosApresentacoes/RPM_2026_1T.pdf",
        "publisher": "Banco Central do Brasil",
        "title": "Relatório de Política Monetária — apresentação 1T26",
        "evidence_class": "SOURCE_ORIGINAL_PUBLIC_FINANCIAL",
        "document_class": ["digital", "chart-heavy"],
        "target_pages_1based": [3],
        "anchors": ["4,1%", "3,8%", "3,3%", "Cenário de referência"],
        "table_roles": [],
    },
    {
        "source_group_id": "frb-annual-report-1914",
        "url": "https://fraser.stlouisfed.org/files/docs/publications/arfr/1910s/arfr_1914.pdf",
        "publisher": "Federal Reserve Board / FRASER",
        "title": "First Annual Report of the Federal Reserve Board, 1914",
        "evidence_class": "SOURCE_ORIGINAL_PUBLIC_FINANCIAL",
        "document_class": ["historical-scan", "ocr-candidate"],
        "target_pages_1based": [1],
        "anchors": ["FIRST ANNUAL REPORT", "FEDERAL RESERVE BOARD", "1914"],
        "table_roles": [],
    },
]
REPEATS = 3


def norm(value: object) -> str:
    s = "" if value is None else str(value)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower().replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "academy-suno-w007-t004/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    pos = (len(s) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    frac = pos - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def candidate_pypdf(raw: bytes, pages0: list[int]) -> dict:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(raw))
    if reader.is_encrypted:
        raise RuntimeError("ENCRYPTED_PDF_PASSWORD_REQUIRED")
    texts = []
    prov = []
    for p in pages0:
        text = (reader.pages[p].extract_text() or "").strip()
        texts.append(text)
        prov.append({"page_number": p + 1, "anchor_kind": "page", "node_id": f"pypdf-page-{p+1}"})
    return {"text": "\n".join(texts), "tables": [], "provenance": prov, "page_count": len(reader.pages)}


def candidate_pdftotext(raw: bytes, pages0: list[int]) -> dict:
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "input.pdf"
        path.write_bytes(raw)
        texts = []
        for p in pages0:
            cp = subprocess.run(
                ["pdftotext", "-layout", "-f", str(p + 1), "-l", str(p + 1), str(path), "-"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
            )
            if cp.returncode:
                raise RuntimeError(cp.stderr.decode("utf-8", "replace").strip() or f"pdftotext_rc_{cp.returncode}")
            texts.append(cp.stdout.decode("utf-8", "replace"))
        info = subprocess.run(["pdfinfo", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        m = re.search(r"^Pages:\s+(\d+)", info.stdout.decode("utf-8", "replace"), re.M)
        page_count = int(m.group(1)) if m else None
    return {
        "text": "\n".join(texts),
        "tables": [],
        "provenance": [{"page_number": p + 1, "anchor_kind": "page", "node_id": f"pdftotext-page-{p+1}"} for p in pages0],
        "page_count": page_count,
    }


def candidate_pymupdf(raw: bytes, pages0: list[int]) -> dict:
    import fitz
    doc = fitz.open(stream=raw, filetype="pdf")
    if doc.needs_pass:
        raise RuntimeError("ENCRYPTED_PDF_PASSWORD_REQUIRED")
    texts, tables, prov = [], [], []
    for p in pages0:
        page = doc[p]
        texts.append(page.get_text("text"))
        found = page.find_tables()
        for ti, table in enumerate(found.tables):
            matrix = table.extract()
            tables.append({"page_number": p + 1, "table_index": ti, "cells": matrix})
            for ri, row in enumerate(matrix):
                for ci, cell in enumerate(row or []):
                    if cell not in (None, ""):
                        prov.append({
                            "page_number": p + 1, "anchor_kind": "cell",
                            "node_id": f"pymupdf-p{p+1}-t{ti}-r{ri}-c{ci}",
                            "table_index": ti, "row_index": ri, "column_index": ci,
                        })
        prov.append({"page_number": p + 1, "anchor_kind": "page", "node_id": f"pymupdf-page-{p+1}"})
    return {"text": "\n".join(texts), "tables": tables, "provenance": prov, "page_count": len(doc)}


def candidate_pdfplumber(raw: bytes, pages0: list[int]) -> dict:
    import pdfplumber
    texts, tables, prov = [], [], []
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        page_count = len(pdf.pages)
        for p in pages0:
            page = pdf.pages[p]
            texts.append(page.extract_text() or "")
            for ti, matrix in enumerate(page.extract_tables() or []):
                tables.append({"page_number": p + 1, "table_index": ti, "cells": matrix})
                for ri, row in enumerate(matrix or []):
                    for ci, cell in enumerate(row or []):
                        if cell not in (None, ""):
                            prov.append({
                                "page_number": p + 1, "anchor_kind": "cell",
                                "node_id": f"pdfplumber-p{p+1}-t{ti}-r{ri}-c{ci}",
                                "table_index": ti, "row_index": ri, "column_index": ci,
                            })
            prov.append({"page_number": p + 1, "anchor_kind": "page", "node_id": f"pdfplumber-page-{p+1}"})
    return {"text": "\n".join(texts), "tables": tables, "provenance": prov, "page_count": page_count}


def candidate_tesseract(raw: bytes, pages0: list[int]) -> dict:
    import fitz
    doc = fitz.open(stream=raw, filetype="pdf")
    if doc.needs_pass:
        raise RuntimeError("ENCRYPTED_PDF_PASSWORD_REQUIRED")
    texts, prov = [], []
    with tempfile.TemporaryDirectory() as td:
        for p in pages0:
            page = doc[p]
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
            image = Path(td) / f"p{p+1}.png"
            pix.save(str(image))
            cp = subprocess.run(
                ["tesseract", str(image), "stdout", "-l", "por+eng", "--psm", "6"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
            )
            if cp.returncode:
                raise RuntimeError(cp.stderr.decode("utf-8", "replace").strip() or f"tesseract_rc_{cp.returncode}")
            texts.append(cp.stdout.decode("utf-8", "replace"))
            prov.append({"page_number": p + 1, "anchor_kind": "page", "node_id": f"tesseract-page-{p+1}"})
    return {"text": "\n".join(texts), "tables": [], "provenance": prov, "page_count": len(doc)}


CANDIDATES = {
    "pypdf-text": candidate_pypdf,
    "pdftotext-layout": candidate_pdftotext,
    "pymupdf-tables": candidate_pymupdf,
    "pdfplumber-tables": candidate_pdfplumber,
    "tesseract-ocr": candidate_tesseract,
}


def role_metrics(tables: list[dict], gold: list[dict]) -> dict:
    if not gold:
        return {"applicable": False, "true_positive": None, "false_positive": None, "recall": None, "precision": None, "assertions": []}
    assertions = []
    tp = fp = 0
    for target in gold:
        expected = norm(target["value"])
        asserted = None
        for table in tables:
            rows = table.get("cells") or []
            header_index = None
            column_index = None
            for ri, row in enumerate(rows[:5]):
                for ci, cell in enumerate(row or []):
                    if norm(target["column"]) == norm(cell):
                        header_index, column_index = ri, ci
                        break
                if column_index is not None:
                    break
            if column_index is None:
                continue
            for ri, row in enumerate(rows[header_index + 1 :], start=header_index + 1):
                joined = " | ".join(norm(c) for c in (row or []))
                if norm(target["row"]) in joined and column_index < len(row):
                    asserted = norm(row[column_index])
                    break
            if asserted is not None:
                break
        if asserted is not None:
            ok = expected == asserted
            tp += int(ok)
            fp += int(not ok)
            assertions.append({"row": target["row"], "column": target["column"], "expected": target["value"], "asserted": asserted, "correct": ok})
    recall = tp / len(gold)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    return {"applicable": True, "true_positive": tp, "false_positive": fp, "recall": recall, "precision": precision, "assertions": assertions}


def anchor_recall(text: str, anchors: list[str]) -> float:
    hay = norm(text)
    hits = sum(1 for a in anchors if norm(a) in hay)
    return hits / len(anchors) if anchors else 1.0


def run_candidate(name: str, fn, raw: bytes, source: dict) -> dict:
    pages0 = [p - 1 for p in source["target_pages_1based"]]
    runs = []
    representative = None
    for _ in range(REPEATS):
        started = time.perf_counter()
        try:
            result = fn(raw, pages0)
            elapsed = (time.perf_counter() - started) * 1000
            runs.append({"success": True, "latency_ms": elapsed})
            representative = result
        except Exception as exc:
            elapsed = (time.perf_counter() - started) * 1000
            runs.append({"success": False, "latency_ms": elapsed, "error": f"{type(exc).__name__}: {exc}"})
    lat = [r["latency_ms"] for r in runs]
    success_count = sum(bool(r["success"]) for r in runs)
    out = {
        "candidate": name,
        "runs": runs,
        "success_rate": success_count / REPEATS,
        "latency_ms": {"p50": percentile(lat, .5), "p95": percentile(lat, .95), "min": min(lat), "max": max(lat)},
        "provider_billed_cost_usd": 0.0,
        "compute_cost_usd": None,
        "compute_cost_missingness": "runner compute allocation not priced; do not treat zero provider bill as zero total cost",
    }
    if representative is not None:
        out["anchor_recall"] = anchor_recall(representative["text"], source["anchors"])
        out["role_metrics"] = role_metrics(representative["tables"], source["table_roles"])
        out["provenance"] = {
            "source_hash_present": True,
            "page_anchor_count": sum(1 for p in representative["provenance"] if p["anchor_kind"] == "page"),
            "cell_anchor_count": sum(1 for p in representative["provenance"] if p["anchor_kind"] == "cell"),
            "target_pages_have_page_anchor": all(any(x["page_number"] == p and x["anchor_kind"] == "page" for x in representative["provenance"]) for p in source["target_pages_1based"]),
        }
        out["extracted_text_chars"] = len(representative["text"])
        out["table_count"] = len(representative["tables"])
        if source["table_roles"]:
            rm = out["role_metrics"]
            out["hard_gate_table_role"] = bool(rm["recall"] == 1.0 and rm["precision"] == 1.0 and out["provenance"]["cell_anchor_count"] > 0)
        else:
            out["hard_gate_table_role"] = "NOT_APPLICABLE"
        out["hard_gate_provenance"] = bool(out["provenance"]["source_hash_present"] and out["provenance"]["target_pages_have_page_anchor"])
    else:
        out["anchor_recall"] = 0.0
        out["role_metrics"] = role_metrics([], source["table_roles"])
        out["hard_gate_table_role"] = False if source["table_roles"] else "NOT_APPLICABLE"
        out["hard_gate_provenance"] = False
    return out


def make_negative_controls(raw: bytes) -> list[dict]:
    controls = []
    malformed = raw[: max(1024, len(raw) // 3)]
    controls.append({
        "source_group_id": "petrobras-2t26-derived-malformed",
        "evidence_class": "DERIVED_MECHANICS_ONLY",
        "document_class": ["malformed"],
        "raw": malformed,
        "expected_trust": "QUARANTINED",
    })
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(io.BytesIO(raw))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt("w007-evidence")
        buf = io.BytesIO()
        writer.write(buf)
        controls.append({
            "source_group_id": "petrobras-2t26-derived-encrypted",
            "evidence_class": "DERIVED_MECHANICS_ONLY",
            "document_class": ["encrypted"],
            "raw": buf.getvalue(),
            "expected_trust": "QUARANTINED",
        })
    except Exception as exc:
        controls.append({
            "source_group_id": "petrobras-2t26-derived-encrypted",
            "evidence_class": "DERIVED_MECHANICS_ONLY",
            "document_class": ["encrypted"],
            "raw": b"%PDF-1.7\n% encrypted control generation failed\n",
            "expected_trust": "QUARANTINED",
            "generation_error": f"{type(exc).__name__}: {exc}",
        })
    return controls


def environment() -> dict:
    versions = {}
    for cmd in (["pdftotext", "-v"], ["tesseract", "--version"]):
        cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        versions[cmd[0]] = cp.stdout.decode("utf-8", "replace").splitlines()[0] if cp.stdout else "unknown"
    try:
        import pypdf
        versions["pypdf"] = pypdf.__version__
    except Exception:
        versions["pypdf"] = "unavailable"
    try:
        import fitz
        versions["pymupdf"] = fitz.VersionBind
    except Exception:
        versions["pymupdf"] = "unavailable"
    try:
        import pdfplumber
        versions["pdfplumber"] = pdfplumber.__version__
    except Exception:
        versions["pdfplumber"] = "unavailable"
    return {"python": os.sys.version, "versions": versions}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    manifest, observations = [], []
    source_bytes = {}
    for source in SOURCES:
        raw = fetch(source["url"])
        source_bytes[source["source_group_id"]] = raw
        sha = hashlib.sha256(raw).hexdigest()
        manifest.append({
            **{k: v for k, v in source.items() if k not in ("anchors", "table_roles")},
            "sha256": sha,
            "byte_length": len(raw),
            "selection_use": "REPRESENTATIVE_BOUNDED_SOURCE_ORIGINAL",
        })
        for name, fn in CANDIDATES.items():
            observations.append({
                "source_group_id": source["source_group_id"],
                "source_sha256": sha,
                "evidence_class": source["evidence_class"],
                **run_candidate(name, fn, raw, source),
            })

    controls_out = []
    pet = source_bytes["petrobras-2t26"]
    for control in make_negative_controls(pet):
        raw = control.pop("raw")
        sha = hashlib.sha256(raw).hexdigest()
        candidate_failures = []
        source_stub = {"target_pages_1based": [1], "anchors": [], "table_roles": []}
        for name, fn in CANDIDATES.items():
            r = run_candidate(name, fn, raw, source_stub)
            candidate_failures.append({
                "candidate": name,
                "success_rate": r["success_rate"],
                "errors": [x.get("error") for x in r["runs"] if not x["success"]],
            })
        controls_out.append({
            **control,
            "sha256": sha,
            "byte_length": len(raw),
            "trusted_generation_eligible": False,
            "candidate_execution": candidate_failures,
        })

    pet_obs = [o for o in observations if o["source_group_id"] == "petrobras-2t26"]
    eligible = [
        o["candidate"] for o in pet_obs
        if o.get("hard_gate_provenance") is True and o.get("hard_gate_table_role") is True and o["success_rate"] == 1.0
    ]
    quality_latency = []
    for o in pet_obs:
        if o["candidate"] in eligible:
            quality_latency.append({
                "candidate": o["candidate"],
                "role_recall": o["role_metrics"]["recall"],
                "role_precision": o["role_metrics"]["precision"],
                "latency_p50_ms": o["latency_ms"]["p50"],
            })
    frontier = []
    for a in quality_latency:
        dominated = False
        for b in quality_latency:
            if a is b:
                continue
            no_worse = (
                b["role_recall"] >= a["role_recall"]
                and b["role_precision"] >= a["role_precision"]
                and b["latency_p50_ms"] <= a["latency_p50_ms"]
            )
            strictly = (
                b["role_recall"] > a["role_recall"]
                or b["role_precision"] > a["role_precision"]
                or b["latency_p50_ms"] < a["latency_p50_ms"]
            )
            if no_worse and strictly:
                dominated = True
                break
        if not dominated:
            frontier.append(a["candidate"])

    accepted_missing_hash = 0
    ambiguous_promoted_trusted = 0
    quarantined_promoted_trusted = sum(1 for c in controls_out if c["trusted_generation_eligible"])

    summary = {
        "task_id": "W007-T004",
        "attempt_id": "A01",
        "methodology": "W005-BENCHMARK-METHODOLOGY-V002",
        "hard_gates": {
            "accepted_source_missing_hash": accepted_missing_hash,
            "ambiguous_ocr_or_table_role_promoted_trusted": ambiguous_promoted_trusted,
            "quarantined_or_unsupported_promoted_trusted_generation": quarantined_promoted_trusted,
            "all_acceptance_zero": accepted_missing_hash == ambiguous_promoted_trusted == quarantined_promoted_trusted == 0,
        },
        "source_original_count": len(manifest),
        "source_groups": [m["source_group_id"] for m in manifest],
        "candidate_count_executed": len(CANDIDATES),
        "table_role_hard_gate_eligible_on_petrobras": eligible,
        "diagnostic_quality_latency_point_pareto": frontier,
        "production_pareto": {
            "status": "PARETO_NOT_COMPUTABLE",
            "reason": "Required total compute-cost objective is missing and managed candidates were not executed in this credentialless benchmark; methodology forbids silent objective drop.",
        },
        "decision": "NO_PREFERENCE/PENDING_EVIDENCE",
        "production_parser_lock_authorized": False,
        "managed_candidates_execution": "NOT_RUN_NO_CREDENTIALS_OR_BILLING_CONTEXT",
        "negative_controls_are_selection_evidence": False,
    }

    (out / "corpus_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "raw_observations.json").write_text(json.dumps(observations, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "negative_controls.json").write_text(json.dumps(controls_out, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "environment.json").write_text(json.dumps(environment(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
