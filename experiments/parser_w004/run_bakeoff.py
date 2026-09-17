#!/usr/bin/env python3
"""W004 parser/source-trust generalization bakeoff.

This harness is deliberately parser-vendor neutral. It evaluates extraction
behaviour against manually checked, primary-source role contracts. Values
alone never make a table-derived fact source-ready.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
FIXTURES_DIR = HERE / "fixtures"
PROVENANCE_FIELDS = (
    "table_id",
    "row_key",
    "row_role",
    "column_key",
    "column_role",
    "unit",
    "period_role",
)


def load_fixtures(fixtures_dir: Path = FIXTURES_DIR) -> list[dict[str, Any]]:
    fixtures = []
    for path in sorted(fixtures_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_fixture_path"] = str(path.relative_to(HERE))
        fixtures.append(data)
    return fixtures


def gold_extraction(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return copy.deepcopy(fixture["required_anchors"])


def flat_value_only(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for anchor in fixture["required_anchors"]:
        item = {"anchor_id": anchor["anchor_id"], "value": anchor["value"]}
        item.update({field: None for field in PROVENANCE_FIELDS})
        out.append(item)
    return out


def apply_named_mutation(fixture: dict[str, Any], mutation_name: str) -> list[dict[str, Any]]:
    out = gold_extraction(fixture)
    spec = fixture.get("mutations", {}).get(mutation_name)
    if spec is None:
        return out
    by_id = {item["anchor_id"]: item for item in out}
    for patch in spec:
        by_id[patch["anchor_id"]].update(patch["overrides"])
    return out


def score_extraction(fixture: dict[str, Any], extraction: list[dict[str, Any]]) -> dict[str, Any]:
    expected = {a["anchor_id"]: a for a in fixture["required_anchors"]}
    observed = {a["anchor_id"]: a for a in extraction}
    issues: list[dict[str, Any]] = []
    exact_values = 0
    exact_provenance_fields = 0
    total_provenance_fields = len(expected) * len(PROVENANCE_FIELDS)
    hard_fail = False
    review_required = False

    for anchor_id, gold in expected.items():
        item = observed.get(anchor_id)
        if item is None:
            hard_fail = True
            issues.append({"anchor_id": anchor_id, "kind": "missing_anchor"})
            continue

        if item.get("value") == gold["value"]:
            exact_values += 1
        else:
            hard_fail = True
            issues.append({
                "anchor_id": anchor_id,
                "kind": "wrong_value",
                "expected": gold["value"],
                "observed": item.get("value"),
            })

        for field in PROVENANCE_FIELDS:
            expected_value = gold.get(field)
            observed_value = item.get(field)
            if observed_value == expected_value:
                exact_provenance_fields += 1
                continue
            if observed_value is None:
                review_required = True
                issues.append({
                    "anchor_id": anchor_id,
                    "kind": "missing_provenance",
                    "field": field,
                    "expected": expected_value,
                })
            else:
                hard_fail = True
                issues.append({
                    "anchor_id": anchor_id,
                    "kind": "wrong_role_or_provenance",
                    "field": field,
                    "expected": expected_value,
                    "observed": observed_value,
                })

    value_coverage = exact_values / len(expected) if expected else 1.0
    provenance_accuracy = exact_provenance_fields / total_provenance_fields if total_provenance_fields else 1.0
    status = "FAIL" if hard_fail else "REVIEW_REQUIRED" if review_required else "PASS"
    return {
        "status": status,
        "value_coverage": round(value_coverage, 4),
        "provenance_accuracy": round(provenance_accuracy, 4),
        "silent_corruption": value_coverage == 1.0 and status != "PASS",
        "issues": issues,
    }


def candidate_extractions(fixture: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        "provenance_preserving_reference": gold_extraction(fixture),
        "flat_value_only": flat_value_only(fixture),
        "wrong_role_probe": apply_named_mutation(fixture, "wrong_role_probe"),
        "wrong_unit_probe": apply_named_mutation(fixture, "wrong_unit_probe"),
    }


def aggregate_status(statuses: list[str]) -> str:
    if "FAIL" in statuses:
        return "FAIL"
    if "REVIEW_REQUIRED" in statuses:
        return "REVIEW_REQUIRED"
    return "PASS"


def run_bakeoff(fixtures_dir: Path = FIXTURES_DIR) -> dict[str, Any]:
    fixtures = load_fixtures(fixtures_dir)
    if not fixtures:
        raise RuntimeError(f"No fixtures found in {fixtures_dir}")

    candidate_names = tuple(candidate_extractions(fixtures[0]).keys())
    by_fixture: dict[str, Any] = {}
    by_candidate: dict[str, list[dict[str, Any]]] = {name: [] for name in candidate_names}

    for fixture in fixtures:
        fixture_results = {}
        for candidate, extraction in candidate_extractions(fixture).items():
            score = score_extraction(fixture, extraction)
            fixture_results[candidate] = score
            by_candidate[candidate].append({
                "fixture_id": fixture["fixture_id"],
                "source_family": fixture["source_family"],
                **score,
            })
        by_fixture[fixture["fixture_id"]] = {
            "source_family": fixture["source_family"],
            "source_url": fixture["source_url"],
            "raw_bytes_sha256": fixture.get("raw_bytes_sha256"),
            "results": fixture_results,
        }

    aggregate = {}
    for candidate, rows in by_candidate.items():
        aggregate[candidate] = {
            "status": aggregate_status([row["status"] for row in rows]),
            "fixtures": len(rows),
            "value_coverage_min": min(row["value_coverage"] for row in rows),
            "provenance_accuracy_min": min(row["provenance_accuracy"] for row in rows),
            "silent_corruption_detected": any(row["silent_corruption"] for row in rows),
        }

    return {
        "experiment": "W004-T003-A01 parser/source-trust generalization bakeoff",
        "contract_version": "parser-source-trust-w004-v1",
        "fixture_count": len(fixtures),
        "source_families": sorted({f["source_family"] for f in fixtures}),
        "hard_gates": [
            "critical value must be present and exact",
            "table-derived facts require exact table/row/column roles",
            "unit provenance must be exact when specified",
            "period role must be exact",
            "missing provenance cannot be promoted to PASS",
            "wrong non-null provenance is a FAIL even at 100% value coverage",
        ],
        "by_fixture": by_fixture,
        "aggregate_candidates": aggregate,
        "implementation_decision": {
            "status": "UNLOCKED",
            "preferred_implementation": None,
            "reason": (
                "The experiment separates safe vs unsafe extraction behaviours, but does not compare "
                "multiple viable parser libraries on identical raw bytes. Behavioural evidence is not "
                "sufficient to lock implementation identity."
            ),
        },
        "raw_byte_evidence": {
            "status": "UNKNOWN_IN_THIS_ATTEMPT",
            "reason": "The execution environment could inspect official pages/PDF renderings but could not retrieve raw response bytes for hashing.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=FIXTURES_DIR)
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    result = run_bakeoff(args.fixtures)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["aggregate_candidates"], indent=2, ensure_ascii=False))
    print(json.dumps(result["implementation_decision"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
