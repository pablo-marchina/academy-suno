#!/usr/bin/env python3
"""W004-T005-A02: integrate accepted automated blind calibration evidence.

This script performs a post-freeze join between the blind A03 model validation and
frozen generation metadata using content SHA-256. Generation targets are therefore
used only for retrospective calibration analysis; they were not exposed to A03.

The output is MODEL_AUTOMATED_BLIND_CALIBRATION, never human gold.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_A03_SHA256 = "adae7376415cd7052b8b2b84002ce0a7a5890047cb86e98dbe456747c7fe1bb4"
EXPECTED_COUNT = 36
ORDINAL = ("BEGINNER", "INTERMEDIATE", "ADVANCED")
ALL_LABELS = (*ORDINAL, "UNSCORABLE")
CHECKS = (
    "FACTUAL_CRITICAL_PRESERVATION",
    "MATERIAL_CONCEPT_PRESERVATION",
    "FORMAT_NATIVE_CONTRACT",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_jsonl(data: bytes, label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, raw in enumerate(data.decode("utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError(f"{label}:{line_no}: record must be object")
        rows.append(value)
    return rows


def load_frozen_outputs() -> list[dict[str, Any]]:
    manifest = json.loads((ROOT / "data/evals/w004/frozen_outputs_manifest_v001.json").read_text())
    rows: list[dict[str, Any]] = []
    for shard in manifest["shards"]:
        path = ROOT / shard["path"]
        raw = path.read_bytes()
        if sha256(raw) != shard["file_sha256"]:
            raise ValueError(f"frozen shard hash mismatch: {shard['path']}")
        if shard["encoding"] == "utf-8-jsonl":
            decoded = raw
        elif shard["encoding"] == "gzip+base64-utf8-jsonl":
            decoded = gzip.decompress(base64.b64decode(b"".join(raw.split()), validate=True))
            expected = shard.get("decoded_jsonl_sha256")
            if expected and sha256(decoded) != expected:
                raise ValueError(f"decoded shard hash mismatch: {shard['path']}")
        else:
            raise ValueError(f"unsupported encoding: {shard['encoding']}")
        rows.extend(parse_jsonl(decoded, shard["path"]))
    if len(rows) != EXPECTED_COUNT:
        raise ValueError(f"expected 36 frozen outputs, got {len(rows)}")
    return rows


def load_blind_bank() -> tuple[list[dict[str, Any]], str]:
    path = ROOT / "data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64"
    decoded = gzip.decompress(base64.b64decode(b"".join(path.read_bytes().split()), validate=True))
    rows = parse_jsonl(decoded, str(path.relative_to(ROOT)))
    if len(rows) != EXPECTED_COUNT:
        raise ValueError(f"expected 36 blind packets, got {len(rows)}")
    forbidden = {
        "generation_target_level", "human_gold_level", "evaluator_predicted_level",
        "evaluator_scores", "generation_model_id", "generation_method", "prompt_version",
        "expected_label", "other_annotator_labels",
    }
    for row in rows:
        if forbidden.intersection(row):
            raise ValueError("blind bank leaks forbidden top-level target/evaluator fields")
    return rows, sha256(decoded)


def load_a03(path: Path) -> tuple[list[dict[str, Any]], str]:
    raw = path.read_bytes()
    observed = sha256(raw)
    if observed != EXPECTED_A03_SHA256:
        raise ValueError(f"A03 SHA drift: {observed}")
    rows = parse_jsonl(raw, str(path.relative_to(ROOT)))
    if len(rows) != EXPECTED_COUNT:
        raise ValueError(f"A03 must contain 36 rows, got {len(rows)}")
    ids: set[str] = set()
    for row in rows:
        item_id = row.get("item_id")
        if not isinstance(item_id, str) or not item_id or item_id in ids:
            raise ValueError("A03 item IDs must be unique and non-empty")
        ids.add(item_id)
        if row.get("validator_kind") != "MODEL_AUTOMATED":
            raise ValueError(f"A03 row {item_id} lost MODEL_AUTOMATED evidence class")
        if row.get("audience_label") not in ALL_LABELS:
            raise ValueError(f"invalid A03 audience label: {item_id}")
        if "annotation_role" in row or "annotator_id" in row:
            raise ValueError("A03 must not impersonate human annotation fields")
    return rows, observed


def confusion(targets: list[str], predictions: list[str]) -> dict[str, dict[str, int]]:
    matrix = {a: {b: 0 for b in ALL_LABELS} for a in ORDINAL}
    for a, b in zip(targets, predictions):
        matrix[a][b] += 1
    return matrix


def cohen_kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if not n:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    labels = set(a) | set(b)
    expected = sum((ca[x] / n) * (cb[x] / n) for x in labels)
    if abs(1 - expected) < 1e-12:
        return None
    return (observed - expected) / (1 - expected)


def quadratic_weighted_kappa(a: list[str], b: list[str]) -> float | None:
    pairs = [(x, y) for x, y in zip(a, b) if x in ORDINAL and y in ORDINAL]
    if not pairs:
        return None
    n = len(pairs)
    idx = {x: i for i, x in enumerate(ORDINAL)}
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    scale = float((len(ORDINAL) - 1) ** 2)
    observed = sum(((idx[x] - idx[y]) ** 2) / scale for x, y in pairs) / n
    expected = sum(
        (((idx[x] - idx[y]) ** 2) / scale) * (ca[x] / n) * (cb[y] / n)
        for x in ORDINAL for y in ORDINAL
    )
    if abs(expected) < 1e-12:
        return None
    return 1.0 - observed / expected


def build() -> dict[str, Any]:
    frozen = load_frozen_outputs()
    blind, blind_hash = load_blind_bank()
    a03, a03_hash = load_a03(ROOT / "artifacts/evals/w004/model_validation_a03.jsonl")

    frozen_by_hash: dict[str, dict[str, Any]] = {}
    for row in frozen:
        digest = row.get("content_sha256")
        if not isinstance(digest, str) or len(digest) != 64 or digest in frozen_by_hash:
            raise ValueError("frozen content_sha256 must be unique")
        if sha256(row["rendered_text"].encode("utf-8")) != digest:
            raise ValueError(f"rendered_text hash mismatch: {row['item_id']}")
        if row.get("split") != "DEVELOPMENT":
            raise ValueError("held-out/non-development output entered calibration")
        frozen_by_hash[digest] = row

    blind_by_id: dict[str, dict[str, Any]] = {}
    mapping: dict[str, dict[str, Any]] = {}
    for packet in blind:
        blind_id = packet.get("blind_item_id")
        digest = packet.get("output_sha256")
        if not isinstance(blind_id, str) or blind_id in blind_by_id:
            raise ValueError("blind IDs must be unique")
        if digest not in frozen_by_hash:
            raise ValueError(f"blind output hash cannot be joined: {blind_id}")
        if sha256(packet["output_text"].encode("utf-8")) != digest:
            raise ValueError(f"blind packet text hash mismatch: {blind_id}")
        blind_by_id[blind_id] = packet
        mapping[blind_id] = frozen_by_hash[digest]

    if len(mapping) != EXPECTED_COUNT or len({r["item_id"] for r in mapping.values()}) != EXPECTED_COUNT:
        raise ValueError("blind→frozen join must be one-to-one 36/36")

    a03_by_id = {row["item_id"]: row for row in a03}
    if set(a03_by_id) != set(mapping):
        raise ValueError("A03 population does not exactly match blind bank")

    joined: list[dict[str, Any]] = []
    for blind_id in [p["blind_item_id"] for p in blind]:
        frozen_row = mapping[blind_id]
        model_row = a03_by_id[blind_id]
        joined.append({
            "blind_item_id": blind_id,
            "frozen_item_id": frozen_row["item_id"],
            "source_id": frozen_row["source_id"],
            "format": frozen_row["format"],
            "requested_generation_target": frozen_row["generation_target_level"],
            "automated_blind_label": model_row["audience_label"],
            "label_match": frozen_row["generation_target_level"] == model_row["audience_label"],
            "mixed_level_flag": model_row["mixed_level_flag"],
            "confidence": model_row["confidence"],
            "non_compensatory_checks": model_row["non_compensatory_checks"],
            "content_sha256": frozen_row["content_sha256"],
        })

    targets = [r["requested_generation_target"] for r in joined]
    labels = [r["automated_blind_label"] for r in joined]
    scorable_pairs = [(x, y) for x, y in zip(targets, labels) if y in ORDINAL]
    ordinal_index = {x: i for i, x in enumerate(ORDINAL)}
    exact = sum(r["label_match"] for r in joined)
    mae = (
        sum(abs(ordinal_index[x] - ordinal_index[y]) for x, y in scorable_pairs) / len(scorable_pairs)
        if scorable_pairs else None
    )

    by_format: dict[str, dict[str, Any]] = {}
    for fmt in sorted({r["format"] for r in joined}):
        rows = [r for r in joined if r["format"] == fmt]
        by_format[fmt] = {
            "n": len(rows),
            "exact_target_match": sum(r["label_match"] for r in rows) / len(rows),
            "automated_label_counts": dict(sorted(Counter(r["automated_blind_label"] for r in rows).items())),
        }
    by_source: dict[str, dict[str, Any]] = {}
    for source in sorted({r["source_id"] for r in joined}):
        rows = [r for r in joined if r["source_id"] == source]
        by_source[source] = {
            "n": len(rows),
            "exact_target_match": sum(r["label_match"] for r in rows) / len(rows),
            "automated_label_counts": dict(sorted(Counter(r["automated_blind_label"] for r in rows).items())),
        }

    failures = []
    check_counts: dict[str, dict[str, int]] = {}
    for check in CHECKS:
        values = Counter(r["non_compensatory_checks"][check] for r in joined)
        check_counts[check] = dict(sorted(values.items()))
    for row in joined:
        bad = [k for k in CHECKS if row["non_compensatory_checks"][k] in {"FAIL", "REVIEW_REQUIRED"}]
        if bad:
            failures.append({
                "blind_item_id": row["blind_item_id"],
                "frozen_item_id": row["frozen_item_id"],
                "source_id": row["source_id"],
                "format": row["format"],
                "checks_requiring_attention": bad,
            })

    report = {
        "schema_version": "w004-t005-automated-calibration-v001",
        "task_id": "W004-T005",
        "attempt_id": "A02",
        "base_state_version": "0034",
        "base_commit_sha": "9eb8031e14d375738a898561ba5f5a7777c65c82",
        "evidence_policy": "D-0017",
        "evidence_class": "MODEL_AUTOMATED_BLIND_CALIBRATION",
        "human_gold_eligible": False,
        "human_agreement_observed": False,
        "human_preference_observed": False,
        "threshold_disposition": "DIAGNOSTIC_ONLY",
        "held_out_touched": False,
        "join": {
            "method": "post-freeze exact SHA-256 join: blind.output_sha256 == frozen.content_sha256",
            "joined_item_count": len(joined),
            "one_to_one": True,
            "a03_output_sha256": a03_hash,
            "blind_bank_decoded_sha256": blind_hash,
            "target_exposure_during_a03": False,
        },
        "target_to_automated": {
            "n": len(joined),
            "target_counts": dict(sorted(Counter(targets).items())),
            "automated_label_counts": dict(sorted(Counter(labels).items())),
            "exact_match_count": exact,
            "exact_match_rate": exact / len(joined),
            "ordinal_mae_on_scorable_pairs": mae,
            "cohen_kappa_diagnostic": cohen_kappa(targets, labels),
            "quadratic_weighted_kappa_diagnostic": quadratic_weighted_kappa(targets, labels),
            "confusion_matrix_rows_target_cols_automated": confusion(targets, labels),
            "interpretation": (
                "Requested generation target is not gold. These are retrospective target→automated calibration diagnostics, "
                "not human agreement metrics and not evidence for freezing production thresholds."
            ),
        },
        "slices": {"by_format": by_format, "by_source": by_source},
        "non_compensatory_check_counts": check_counts,
        "attention_items": failures,
        "joined_rows": joined,
        "claims_prohibited": [
            "HUMAN_GOLD", "HUMAN_AGREEMENT", "HUMAN_PREFERENCE",
            "HUMAN_VALIDATED_AUDIENCE_THRESHOLDS", "HUMAN_VALIDATED_PRODUCTION_READINESS",
        ],
        "downstream_eligibility": {
            "t006_automated_semantic_ablation": True,
            "t007_automated_provider_model_comparison": True,
            "human_gold_dependent_claims": False,
        },
    }
    return report


def write_outputs(report: dict[str, Any], out_json: Path, out_md: Path, result_path: Path) -> None:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    m = report["target_to_automated"]
    lines = [
        "# W004-T005-A02 — Automated blind calibration integration",
        "",
        "- Evidence class: `MODEL_AUTOMATED_BLIND_CALIBRATION`",
        "- Evidence policy: `D-0017`",
        "- Items joined: **36/36** via exact content SHA-256 after A03 was frozen",
        "- Human gold eligible: **NO**",
        "- Human agreement observed: **NO**",
        "- Held-out touched: **NO**",
        "- Threshold disposition: **DIAGNOSTIC_ONLY**",
        f"- Target→automated exact match: **{m['exact_match_count']}/36 ({m['exact_match_rate']:.3f})**",
        f"- Ordinal MAE (scorable): **{m['ordinal_mae_on_scorable_pairs']:.3f}**",
        f"- Diagnostic Cohen kappa: **{m['cohen_kappa_diagnostic']:.3f}**",
        f"- Diagnostic quadratic weighted kappa: **{m['quadratic_weighted_kappa_diagnostic']:.3f}**",
        f"- Attention items from non-compensatory checks: **{len(report['attention_items'])}**",
        "",
        "## Boundary",
        "",
        "Generation target is not gold. Metrics describe how frozen outputs were classified by the accepted blind automated judge. They must not be represented as human agreement, human preference, or human-validated thresholds.",
    ]
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = [
        "# RESULT W004-T005-A02",
        "",
        "`TASK_ID: W004-T005`",
        "`ATTEMPT_ID: A02`",
        "`BASE_STATE_VERSION: 0034`",
        "`BASE_COMMIT_SHA: 9eb8031e14d375738a898561ba5f5a7777c65c82`",
        "`WORKER_BRANCH: worker/W004-T005-A02`",
        "`STATUS: COMPLETE`",
        "`EVIDENCE_CLASS: MODEL_AUTOMATED_BLIND_CALIBRATION`",
        "`EVIDENCE_POLICY: D-0017`",
        "",
        "## Outcome",
        "",
        "- accepted A03 population linked 36/36 to frozen DEVELOPMENT outputs by exact post-freeze content SHA-256",
        f"- target→automated exact match: `{m['exact_match_count']}/36 ({m['exact_match_rate']:.6f})`",
        f"- ordinal MAE: `{m['ordinal_mae_on_scorable_pairs']:.6f}`",
        f"- diagnostic Cohen kappa: `{m['cohen_kappa_diagnostic']:.6f}`",
        f"- diagnostic quadratic weighted kappa: `{m['quadratic_weighted_kappa_diagnostic']:.6f}`",
        f"- non-compensatory attention items: `{len(report['attention_items'])}`",
        "- held-out touched: `false`",
        "- human gold eligible: `false`",
        "- human agreement observed: `false`",
        "- threshold disposition: `DIAGNOSTIC_ONLY`",
        "- T006 automated semantic ablation eligible: `true`",
        "- T007 automated provider/model comparison eligible: `true`",
        "",
        "## Evidence boundary",
        "",
        "This result satisfies the W004 calibration dependency only under LOCKED waiver D-0017. It does not create or imply PRIMARY_A/PRIMARY_B, human gold, human agreement, human preference, or human-validated production thresholds.",
        "",
        "## Artifacts",
        "",
        f"- `{out_json.as_posix()}`",
        f"- `{out_md.as_posix()}`",
    ]
    result_path.write_text("\n".join(result) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out-json", type=Path, default=ROOT / "experiments/automated_calibration_w004/runs/W004-T005-A02/calibration.json")
    p.add_argument("--out-md", type=Path, default=ROOT / "docs/evals/automated_calibration_w004/W004-T005-A02.md")
    p.add_argument("--result", type=Path, default=ROOT / "SYSTEM/RESULTS/W004-T005-A02.md")
    args = p.parse_args()
    report = build()
    write_outputs(report, args.out_json, args.out_md, args.result)
    print(json.dumps({
        "status": "COMPLETE", "item_count": report["target_to_automated"]["n"],
        "evidence_class": report["evidence_class"],
        "exact_match_rate": report["target_to_automated"]["exact_match_rate"],
        "human_gold_eligible": report["human_gold_eligible"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
