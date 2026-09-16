#!/usr/bin/env python3
"""Validate gold-v001 benchmark invariants using only the standard library."""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

LEVELS = {"BEGINNER", "INTERMEDIATE", "ADVANCED"}
FORMATS = {"ARTICLE", "CAROUSEL", "SHORT_VIDEO"}
FORBIDDEN = {
    "generation_target_level",
    "evaluator_predicted_level",
    "evaluator_scores",
    "generation_model_id",
    "prompt_version",
    "other_annotator_labels",
    "expected_label",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def property_names(node: Any) -> set[str]:
    out: set[str] = set()
    if isinstance(node, dict):
        props = node.get("properties")
        if isinstance(props, dict):
            out |= set(props)
        for value in node.values():
            out |= property_names(value)
    elif isinstance(node, list):
        for value in node:
            out |= property_names(value)
    return out


def validate(root: Path, manifest: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if manifest.get("split_unit") != "SOURCE_DOCUMENT":
        errors.append("split_unit must be SOURCE_DOCUMENT")

    grid = manifest.get("variant_grid", {})
    levels = set(grid.get("audience_levels", []))
    formats = set(grid.get("formats", []))
    if levels != LEVELS or formats != FORMATS or grid.get("variants_per_source") != 9:
        errors.append("variant_grid must be the canonical 3 audiences x 3 formats")

    sources = manifest.get("sources", [])
    ids = [s.get("source_id") for s in sources]
    if len(ids) != len(set(ids)):
        errors.append("source_id values must be unique")
    if not any(s.get("split") == "DEVELOPMENT" for s in sources):
        errors.append("at least one development source is required")
    if not any(s.get("split") == "HELD_OUT" for s in sources):
        errors.append("at least one held-out source is required")

    for source in sources:
        sid = source["source_id"]
        expected = hashlib.sha256(
            f"{manifest['benchmark_version']}{sid}".encode("utf-8")
        ).hexdigest()
        if source.get("split_key") != expected:
            errors.append(f"{sid}: split_key mismatch")
        if source.get("split") == "HELD_OUT" and source.get("tuning_exposure") != "FORBIDDEN":
            errors.append(f"{sid}: held-out tuning exposure must be FORBIDDEN")

        fixture = root / source["fixture_ref"]
        if not fixture.exists():
            errors.append(f"{sid}: missing fixture {source['fixture_ref']}")
            continue
        data = load(fixture)
        prov = data.get("provenance", {})
        if data.get("fixture_id") != sid:
            errors.append(f"{sid}: fixture_id mismatch")
        if data.get("source", {}).get("primary_source") is not True:
            errors.append(f"{sid}: fixture is not marked primary_source=true")
        if prov.get("source_identity_sha256") != source.get("source_identity_sha256"):
            errors.append(f"{sid}: source_identity_sha256 mismatch")
        if prov.get("golden_checks_sha256") != source.get("golden_checks_sha256"):
            errors.append(f"{sid}: golden_checks_sha256 mismatch")

    for gold in manifest.get("gold_labels", []):
        if gold.get("human_gold_level") not in LEVELS | {"UNSCORABLE"}:
            errors.append("gold label has invalid human_gold_level")
        if gold.get("gold_label_source") != "BLIND_HUMAN_ADJUDICATION":
            errors.append("gold label lacks BLIND_HUMAN_ADJUDICATION provenance")
        if len(gold.get("annotation_ids", [])) < 2:
            errors.append("gold label requires at least two independent annotation refs")

    threshold = manifest.get("threshold_policy", {})
    if manifest.get("status") == "DIAGNOSTIC_ONLY" and threshold.get("freeze_allowed") is not False:
        errors.append("DIAGNOSTIC_ONLY requires freeze_allowed=false")
    if threshold.get("freeze_allowed") is True and not manifest.get("gold_labels"):
        errors.append("cannot freeze thresholds with no human gold")

    leaked = FORBIDDEN & property_names(schema)
    if leaked:
        errors.append(f"forbidden annotator fields leaked into schema: {sorted(leaked)}")
    declared = set(schema.get("x_blinding", {}).get("forbidden_input_fields", []))
    if FORBIDDEN - declared:
        errors.append("schema x_blinding does not declare all forbidden inputs")
    if schema.get("additionalProperties") is not False:
        errors.append("annotation schema must set additionalProperties=false")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()
    root = args.repo_root.resolve()

    manifest = load(root / "data/evals/gold/benchmark_manifest_v001.json")
    schema = load(root / "data/evals/gold/annotation_schema_v001.json")
    errors = validate(root, manifest, schema)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print(
        f"benchmark={manifest['benchmark_version']} sources={len(manifest['sources'])} "
        f"expected_items={manifest['variant_grid']['expected_item_count']} "
        f"status={manifest['status']} threshold_mode={manifest['threshold_policy']['mode']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
