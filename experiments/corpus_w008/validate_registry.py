"""Validate frozen W008 source-group/metric preregistration; no model execution.

Only inventory coverage and invariant status are computed. Missing benchmarks
remain null, never manufactured zeros or a vendor/model recommendation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = Path(__file__).with_name("registry.v1.json")
FACTUAL_ORACLE = ROOT / "tests" / "factual" / "observed_factual_v001.jsonl"
REQUIRED_FAMILIES = frozenset({"PETROBRAS", "BCB", "CVM", "FRASER"})
REQUIRED_METHODS = frozenset({"DIRECT", "ANCHORED", "EVAL_REPAIR", "FULL_3X3"})
REQUIRED_METRICS = frozenset({
    "critical_false_accept_count", "false_support_rate",
    "numeric_period_unit_preservation", "cross_output_claim_contradictions",
    "provenance_traceability", "audience_diagnostic", "latency_p95",
    "cost_total", "recovery_integrity",
})
SUPPORTED_STATES = frozenset({"HISTORICAL_REPOSITORY_ACCEPTED", "PLANNED_NOT_ACQUIRED"})
SHA = re.compile(r"^[0-9a-f]{64}$")


class RegistryError(ValueError):
    pass


def group_split(group_id: str, *, salt: str) -> str:
    """Byte-for-byte equivalent to W009-T001 source_group_split policy."""
    if not isinstance(group_id, str) or not group_id.strip():
        raise RegistryError("source group must be a nonempty string")
    if not isinstance(salt, str) or not salt.strip():
        raise RegistryError("salt must be a nonempty string")
    digest = hashlib.sha256(f"{salt}|{group_id}".encode("utf-8")).hexdigest()
    bucket = int(digest[:12], 16) % 100
    return "DEV" if bucket < 60 else "CALIBRATION" if bucket < 80 else "HELD_OUT"


def _ids(rows: list[dict[str, Any]], field: str) -> set[str]:
    values = [row.get(field) for row in rows]
    if any(not isinstance(v, str) or not v.strip() for v in values):
        raise RegistryError(f"{field} empty/missing")
    if len(values) != len(set(values)):
        raise RegistryError(f"duplicate {field}")
    return set(values)


def _oracle(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RegistryError("existing factual oracle reference unavailable")
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            fixture = row["fixture_id"]
            if fixture in result:
                raise RegistryError("duplicate factual oracle id")
            result[fixture] = row["failure_code"]
    return result


def validate_registry(registry: dict[str, Any], *, oracle_path: Path = FACTUAL_ORACLE) -> dict[str, Any]:
    if registry.get("schema_version") != "w008_t003_corpus_registry.v1":
        raise RegistryError("unknown corpus schema")
    if registry.get("protocol_status") != "PREREGISTERED_DESIGN_NO_NEW_CORPUS_RUN":
        raise RegistryError("benchmark status must remain not run before observations")
    partition = registry.get("partition", {})
    if (
        partition.get("algorithm") != "sha256_prefix12_mod100"
        or partition.get("salt") != "w009-preregistered-split-policy-v1"
        or partition.get("unit") != "source_group_id_primary_document_or_event"
        or partition.get("buckets") != {"DEV": "0..59", "CALIBRATION": "60..79", "HELD_OUT": "80..99"}
    ):
        raise RegistryError("split contract mismatches accepted W009 group policy")
    methods = registry.get("candidate_methods")
    if not isinstance(methods, list) or _ids(methods, "id") != REQUIRED_METHODS:
        raise RegistryError("must preregister exactly four comparable alternatives")
    groups = registry.get("source_groups")
    if not isinstance(groups, list) or not groups:
        raise RegistryError("source group registry required")
    ids = _ids(groups, "group_id")
    families = [g.get("family") for g in groups]
    if set(families) != REQUIRED_FAMILIES or len(families) != len(REQUIRED_FAMILIES):
        raise RegistryError("BCB/Petrobras/CVM/FRASER families required and unique")
    if any(g.get("record_status") not in SUPPORTED_STATES for g in groups):
        raise RegistryError("unknown source record evidence class")
    hashes: set[str] = set()
    observed: list[dict[str, Any]] = []
    planned: list[dict[str, Any]] = []
    for g in groups:
        status = g["record_status"]
        if status == "HISTORICAL_REPOSITORY_ACCEPTED":
            sha = g.get("source_sha256")
            url, ref = g.get("source_url"), g.get("ref")
            if not isinstance(sha, str) or not SHA.fullmatch(sha):
                raise RegistryError("historical original missing valid 64-char source hash")
            if sha in hashes:
                raise RegistryError("duplicate original bytes across source groups; manual group review required")
            hashes.add(sha)
            if not isinstance(url, str) or not url.startswith("https://"):
                raise RegistryError("historical original missing source URL")
            if ref != "SYSTEM/RESULTS/W007-T004-A01.md":
                raise RegistryError("historical source acceptance must link to actual W007 result")
            observed.append(g)
        else:
            if any(g.get(k) is not None for k in ("source_sha256", "source_url", "ref")):
                raise RegistryError("unacquired source cannot have invented hash/url/evidence ref")
            if not isinstance(g.get("missing_reason"), str) or not g["missing_reason"].strip():
                raise RegistryError("unacquired source must disclose missingness")
            planned.append(g)
    if {g["family"] for g in planned} != {"CVM"}:
        raise RegistryError("only CVM can be marked not acquired in this evidence snapshot")
    controls = registry.get("adversarial_controls")
    if not isinstance(controls, list):
        raise RegistryError("adversarial controls absent")
    _ids(controls, "id")
    oracle = _oracle(oracle_path)
    if set(c["id"] for c in controls) != set(oracle):
        raise RegistryError("controls must cover exactly existing synthetic oracle ids")
    for control in controls:
        if control.get("kind") != "SYNTHETIC_EXISTING_FIXTURE":
            raise RegistryError("synthetic controls cannot be promoted to human/source-original")
        if control.get("failure_code") != oracle[control["id"]]:
            raise RegistryError("control failure code disagrees with accepted oracle row")
        if control.get("group_id") not in ids:
            raise RegistryError("synthetic control missing parent source-group partition")
        if "NOT source-original claim" not in str(control.get("data_authority")):
            raise RegistryError("synthetic control lacks explicit provenance limitation")
    defs = registry.get("metric_definitions")
    if not isinstance(defs, list) or _ids(defs, "metric_id") != REQUIRED_METRICS:
        raise RegistryError("raw metric registry does not match the nine predeclared dimensions")
    for metric in defs:
        if (
            metric.get("direction") not in {"lower", "higher"}
            or metric.get("hard_gate") not in {True, False}
            or not all(isinstance(metric.get(k), str) and metric[k].strip()
                       for k in ("unit", "level", "observation", "evidence_required"))
        ):
            raise RegistryError("metric missing unit/direction/evidence or authority")
    if registry.get("current_observations") != {
        "status": "NO_NEW_BENCHMARK_RUN",
        "samples": [],
        "raw_measurements": [],
        "summary_statistics": None,
        "confidence_intervals": None,
        "point_pareto": None,
        "decision": "PENDING_EVIDENCE",
    }:
        raise RegistryError("no executed benchmark metrics or preference can be asserted")
    missing = registry.get("study_missingness")
    if not isinstance(missing, dict) or missing.get("human_gold") != "UNAVAILABLE_BY_OPERATOR_CHOICE" or missing.get("external_model_judge") != "NOT_RUN" or missing.get("production_ready") != "FALSE":
        raise RegistryError("missingness and human-evidence waiver must remain explicit")
    split_by_id = {g["group_id"]: group_split(g["group_id"], salt=partition["salt"]) for g in groups}
    if any(split_by_id[c["group_id"]] != group_split(c["group_id"], salt=partition["salt"])
           for c in controls):
        raise RegistryError("adversarial control escaped parent group partition")
    return {
        "schema_version": "w008_t003_validation.v1",
        "validation": "PASS_PREREGISTRATION_ONLY",
        "evidence_class": "HISTORICAL_REPO_SOURCE_INVENTORY_PLUS_SYNTHETIC_CONTROLS",
        "observed_original_groups_from_prior_work": len(observed),
        "new_original_downloads": 0,
        "new_executed_source_generation_benchmarks": 0,
        "required_family_coverage": sorted(REQUIRED_FAMILIES),
        "historical_family_coverage": sorted(g["family"] for g in observed),
        "not_acquired_families": sorted(g["family"] for g in planned),
        "source_group_assignments": split_by_id,
        "observed_group_split_counts": dict(sorted(Counter(split_by_id[g["group_id"]] for g in observed).items())),
        "synthetic_control_count": len(controls),
        "predeclared_candidate_count": len(methods),
        "predeclared_metric_count": len(defs),
        "measured_metric_count": 0,
        "model_judge_status": "NOT_RUN",
        "human_gold_eligible": False,
        "business_utility_status": "PENDING_EVIDENCE",
        "candidate_preference": "PENDING_EVIDENCE",
        "production_ready": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--output", type=Path, default=None, help="Optional report file, no raw source text")
    args = parser.parse_args()
    data = json.loads(args.registry.read_text(encoding="utf-8"))
    result = validate_registry(data)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
