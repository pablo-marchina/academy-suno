#!/usr/bin/env python3
"""Validate W004 human-calibration preparation invariants.

The validator deliberately does not inspect or generate held-out outputs. It checks
only frozen development artifacts and the blinded annotation packet.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
W004 = ROOT / "data" / "evals" / "w004"
SOURCE_MANIFEST = W004 / "source_manifest_v001.json"
OUTPUT_MANIFEST = W004 / "frozen_outputs_manifest_v001.json"
BLIND_BANK = W004 / "blind_items" / "blind_bank_v001.jsonl.gz.b64"

AUDIENCES = {"BEGINNER", "INTERMEDIATE", "ADVANCED"}
FORMATS = {"ARTICLE", "CAROUSEL", "SHORT_VIDEO"}
FORBIDDEN_BLIND_KEYS = {
    "generation_target_level",
    "human_gold_level",
    "evaluator_predicted_level",
    "evaluator_scores",
    "generation_model_id",
    "generation_method",
    "prompt_version",
    "expected_label",
    "other_annotator_labels",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_jsonl_bytes(data: bytes, label: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, raw in enumerate(data.decode("utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            fail(f"{label}:{line_no}: JSONL record must be an object")
        records.append(value)
    return records


def load_output_shard(entry: dict[str, Any]) -> list[dict[str, Any]]:
    path = ROOT / entry["path"]
    raw = path.read_bytes()
    if sha256_bytes(raw) != entry["file_sha256"]:
        fail(f"hash mismatch for {entry['path']}")

    encoding = entry["encoding"]
    if encoding == "utf-8-jsonl":
        decoded = raw
    elif encoding == "gzip+base64-utf8-jsonl":
        compressed = base64.b64decode(b"".join(raw.split()))
        decoded = gzip.decompress(compressed)
        expected_decoded_hash = entry.get("decoded_jsonl_sha256")
        if expected_decoded_hash and sha256_bytes(decoded) != expected_decoded_hash:
            fail(f"decoded hash mismatch for {entry['path']}")
    else:
        fail(f"unknown shard encoding {encoding!r}")

    records = parse_jsonl_bytes(decoded, entry["path"])
    if len(records) != entry["item_count"]:
        fail(
            f"{entry['path']}: manifest item_count={entry['item_count']} "
            f"but decoded={len(records)}"
        )
    return records


def nested_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from nested_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from nested_keys(child)


def validate_sources(source_manifest: dict[str, Any]) -> tuple[set[str], set[str]]:
    if source_manifest.get("corpus_version") != "w004-corpus-v001":
        fail("unexpected corpus_version")
    if source_manifest.get("split_unit") != "SOURCE_DOCUMENT":
        fail("split_unit must be SOURCE_DOCUMENT")
    if source_manifest.get("held_out_policy", {}).get("tuning_exposure") != "FORBIDDEN":
        fail("held-out tuning exposure must be FORBIDDEN")
    if source_manifest.get("gold_policy", {}).get("generation_target_is_gold") is not False:
        fail("generation target must not be gold")
    if source_manifest.get("gold_policy", {}).get("threshold_freeze_allowed") is not False:
        fail("threshold freeze must remain disabled")

    sources = source_manifest.get("sources")
    if not isinstance(sources, list) or len(sources) != 6:
        fail("W004 corpus v001 must contain exactly six frozen source identities")

    seen: set[str] = set()
    development: set[str] = set()
    held_out: set[str] = set()
    for source in sources:
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            fail("every source must have a non-empty source_id")
        if source_id in seen:
            fail(f"duplicate source_id {source_id}")
        seen.add(source_id)
        split = source.get("split")
        if split == "DEVELOPMENT":
            development.add(source_id)
        elif split == "HELD_OUT":
            held_out.add(source_id)
        else:
            fail(f"invalid split {split!r} for {source_id}")

    if len(development) != 4 or len(held_out) != 2:
        fail(f"expected 4 development and 2 held-out sources, got {len(development)}/{len(held_out)}")
    if development & held_out:
        fail("source cannot occur in both development and held-out")
    return development, held_out


def validate_outputs(development: set[str], held_out: set[str]) -> list[dict[str, Any]]:
    manifest = load_json(OUTPUT_MANIFEST)
    if manifest.get("corpus_version") != "w004-corpus-v001":
        fail("output manifest corpus_version mismatch")
    if manifest.get("output_version") != "w004-natural-v001":
        fail("unexpected output_version")

    records: list[dict[str, Any]] = []
    for shard in manifest.get("shards", []):
        records.extend(load_output_shard(shard))

    if len(records) != manifest.get("item_count") or len(records) != 36:
        fail(f"expected 36 frozen development outputs, got {len(records)}")

    item_ids: set[str] = set()
    grid: dict[str, set[tuple[str, str]]] = defaultdict(set)
    per_source = Counter()
    for record in records:
        item_id = record.get("item_id")
        if not isinstance(item_id, str) or not item_id:
            fail("frozen output missing item_id")
        if item_id in item_ids:
            fail(f"duplicate output item_id {item_id}")
        item_ids.add(item_id)

        source_id = record.get("source_id")
        if source_id in held_out:
            fail(f"held-out output was generated: {source_id}")
        if source_id not in development:
            fail(f"output references non-development source {source_id}")
        if record.get("split") != "DEVELOPMENT":
            fail(f"output {item_id} is not DEVELOPMENT")
        if record.get("human_gold_level") is not None:
            fail(f"output {item_id} pre-populates human gold")
        if record.get("gold_promotion_status") != "NOT_GOLD":
            fail(f"output {item_id} has invalid gold promotion status")

        audience = record.get("generation_target_level")
        fmt = record.get("format")
        if audience not in AUDIENCES or fmt not in FORMATS:
            fail(f"output {item_id} has invalid audience/format")
        grid[source_id].add((audience, fmt))
        per_source[source_id] += 1

    expected_grid = {(audience, fmt) for audience in AUDIENCES for fmt in FORMATS}
    for source_id in sorted(development):
        if per_source[source_id] != 9:
            fail(f"{source_id} must have exactly 9 outputs, got {per_source[source_id]}")
        if grid[source_id] != expected_grid:
            fail(f"{source_id} does not contain the complete 3x3 audience/format grid")
    return records


def validate_blind_bank(expected_count: int) -> int:
    raw = BLIND_BANK.read_bytes()
    compressed = base64.b64decode(b"".join(raw.split()))
    decoded = gzip.decompress(compressed)
    records = parse_jsonl_bytes(decoded, str(BLIND_BANK.relative_to(ROOT)))
    if len(records) != expected_count:
        fail(f"blind bank expected {expected_count} items, got {len(records)}")

    for index, record in enumerate(records, start=1):
        leaked = sorted(FORBIDDEN_BLIND_KEYS.intersection(set(nested_keys(record))))
        if leaked:
            fail(f"blind item {index} leaks forbidden fields: {leaked}")
    return len(records)


def main() -> None:
    source_manifest = load_json(SOURCE_MANIFEST)
    development, held_out = validate_sources(source_manifest)
    outputs = validate_outputs(development, held_out)
    blind_count = validate_blind_bank(len(outputs))

    summary = {
        "status": "PASS",
        "corpus_version": "w004-corpus-v001",
        "development_source_count": len(development),
        "held_out_source_count": len(held_out),
        "frozen_development_output_count": len(outputs),
        "blind_item_count": blind_count,
        "held_out_generated_output_count": 0,
        "generation_target_is_gold": False,
        "threshold_freeze_allowed": False,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
