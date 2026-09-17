#!/usr/bin/env python3
"""Compute pre-adjudication agreement for W004 independent human annotations.

Uses only the Python standard library so the report can be reproduced in a clean
checkout. The script is intentionally strict: PRIMARY_A and PRIMARY_B must cover
exactly the same item IDs and duplicate records are rejected.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

LABELS = ("BEGINNER", "INTERMEDIATE", "ADVANCED", "UNSCORABLE")
ORDINAL = ("BEGINNER", "INTERMEDIATE", "ADVANCED")
CHECK_KEYS = (
    "FACTUAL_CRITICAL_PRESERVATION",
    "MATERIAL_CONCEPT_PRESERVATION",
    "FORMAT_NATIVE_CONTRACT",
)


def load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            record = json.loads(line)
            item_id = record.get("item_id")
            if not isinstance(item_id, str) or not item_id:
                raise ValueError(f"{path}:{line_no}: missing non-empty item_id")
            if item_id in records:
                raise ValueError(f"{path}:{line_no}: duplicate item_id {item_id}")
            label = record.get("audience_label")
            if label not in LABELS:
                raise ValueError(f"{path}:{line_no}: invalid audience_label {label!r}")
            checks = record.get("non_compensatory_checks")
            if not isinstance(checks, dict):
                raise ValueError(f"{path}:{line_no}: missing non_compensatory_checks")
            missing_checks = [key for key in CHECK_KEYS if key not in checks]
            if missing_checks:
                raise ValueError(
                    f"{path}:{line_no}: missing non-compensatory checks {missing_checks}"
                )
            records[item_id] = record
    if not records:
        raise ValueError(f"{path}: no annotation records")
    return records


def cohen_kappa(a_labels: list[str], b_labels: list[str]) -> float | None:
    n = len(a_labels)
    if n == 0:
        return None
    observed = sum(a == b for a, b in zip(a_labels, b_labels)) / n
    ca = Counter(a_labels)
    cb = Counter(b_labels)
    expected = sum((ca[label] / n) * (cb[label] / n) for label in LABELS)
    denom = 1.0 - expected
    if abs(denom) < 1e-12:
        return None
    return (observed - expected) / denom


def quadratic_weighted_kappa(a_labels: list[str], b_labels: list[str]) -> float | None:
    pairs = [(a, b) for a, b in zip(a_labels, b_labels) if a in ORDINAL and b in ORDINAL]
    if not pairs:
        return None

    n = len(pairs)
    index = {label: i for i, label in enumerate(ORDINAL)}
    denom_scale = float((len(ORDINAL) - 1) ** 2)
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)

    observed_disagreement = 0.0
    for a, b in pairs:
        observed_disagreement += ((index[a] - index[b]) ** 2) / denom_scale
    observed_disagreement /= n

    expected_disagreement = 0.0
    for a in ORDINAL:
        for b in ORDINAL:
            weight = ((index[a] - index[b]) ** 2) / denom_scale
            expected_disagreement += weight * (ca[a] / n) * (cb[b] / n)

    if abs(expected_disagreement) < 1e-12:
        return None
    return 1.0 - observed_disagreement / expected_disagreement


def confusion_matrix(a_labels: list[str], b_labels: list[str]) -> dict[str, dict[str, int]]:
    matrix = {a: {b: 0 for b in LABELS} for a in LABELS}
    for a, b in zip(a_labels, b_labels):
        matrix[a][b] += 1
    return matrix


def adjudication_reasons(a: dict[str, Any], b: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if a["audience_label"] != b["audience_label"]:
        reasons.append("AUDIENCE_LABEL_DISAGREEMENT")
    if a["audience_label"] == "UNSCORABLE" or b["audience_label"] == "UNSCORABLE":
        reasons.append("UNSCORABLE_PRESENT")

    checks_a = a["non_compensatory_checks"]
    checks_b = b["non_compensatory_checks"]
    for key in CHECK_KEYS:
        if checks_a[key] != checks_b[key]:
            reasons.append(f"CHECK_DISAGREEMENT:{key}")
        if checks_a[key] in {"FAIL", "REVIEW_REQUIRED"} or checks_b[key] in {
            "FAIL",
            "REVIEW_REQUIRED",
        }:
            reasons.append(f"CHECK_REVIEW:{key}")
    return sorted(set(reasons))


def build_report(a_records: dict[str, dict[str, Any]], b_records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    a_ids = set(a_records)
    b_ids = set(b_records)
    if a_ids != b_ids:
        raise ValueError(
            "PRIMARY_A and PRIMARY_B item sets differ: "
            f"only_a={sorted(a_ids - b_ids)}, only_b={sorted(b_ids - a_ids)}"
        )

    item_ids = sorted(a_ids)
    a_labels = [a_records[item_id]["audience_label"] for item_id in item_ids]
    b_labels = [b_records[item_id]["audience_label"] for item_id in item_ids]
    n = len(item_ids)
    agree_count = sum(a == b for a, b in zip(a_labels, b_labels))

    queue = []
    for item_id in item_ids:
        reasons = adjudication_reasons(a_records[item_id], b_records[item_id])
        if reasons:
            queue.append({"item_id": item_id, "reasons": reasons})

    return {
        "report_version": "w004-agreement-report-v001",
        "paired_item_count": n,
        "raw_agreement": agree_count / n,
        "disagreement_rate": (n - agree_count) / n,
        "cohen_kappa": cohen_kappa(a_labels, b_labels),
        "quadratic_weighted_kappa_on_scorable_pairs": quadratic_weighted_kappa(
            a_labels, b_labels
        ),
        "unscorable_rate_a": sum(label == "UNSCORABLE" for label in a_labels) / n,
        "unscorable_rate_b": sum(label == "UNSCORABLE" for label in b_labels) / n,
        "label_counts_a": dict(Counter(a_labels)),
        "label_counts_b": dict(Counter(b_labels)),
        "primary_a_to_primary_b_confusion": confusion_matrix(a_labels, b_labels),
        "adjudication_queue_count": len(queue),
        "adjudication_queue": queue,
        "threshold_freeze_allowed": False,
        "interpretation_note": (
            "Agreement metrics are diagnostic evidence. They do not authorize threshold "
            "freeze and must be interpreted with sample counts and source clustering in view."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", required=True, type=Path, help="PRIMARY_A JSONL")
    parser.add_argument("--b", required=True, type=Path, help="PRIMARY_B JSONL")
    parser.add_argument("--out", required=True, type=Path, help="Output report JSON")
    args = parser.parse_args()

    report = build_report(load_jsonl(args.a), load_jsonl(args.b))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
