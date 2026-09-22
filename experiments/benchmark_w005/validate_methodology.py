#!/usr/bin/env python3
"""Validate W005 quantitative benchmark methodology invariants using stdlib only."""

from __future__ import annotations
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "data/evals/w005/benchmark_methodology_v001.json"
SCHEMA = ROOT / "data/evals/w005/benchmark_result_v001.schema.json"

def validate() -> None:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert cfg["methodology_id"] == "W005-BENCHMARK-METHODOLOGY-V001"
    assert cfg["evidence_posture"]["current"] == "DIAGNOSTIC_ONLY"

    axes = cfg["score"]["axes"]
    assert set(axes) == {"factuality", "end_user_value", "latency", "cost"}
    assert math.isclose(sum(axis["weight"] for axis in axes.values()), 1.0, abs_tol=1e-12)
    assert cfg["score"]["range"] == {"min": 0.0, "max": 100.0}
    assert axes["factuality"]["weight"] == 0.40
    assert axes["end_user_value"]["weight"] == 0.30
    assert axes["latency"]["weight"] == 0.15
    assert axes["cost"]["weight"] == 0.15

    gates = cfg["hard_gates"]
    assert gates["semantics"] == "ANY_FAIL_OR_UNRESOLVED_REVIEW_DISQUALIFIES"
    assert all(g["non_compensatory"] for g in gates["gates"])
    gate_ids = {g["id"] for g in gates["gates"]}
    assert {"FACTUAL_CRITICAL_PRESERVATION", "MATERIAL_CONCEPT_PRESERVATION",
            "FINANCIAL_RELEVANCE_CRITICAL", "PAIRING_AND_COVERAGE"} <= gate_ids

    pairing = cfg["paired_design"]
    assert pairing["experimental_unit"] == "evidence_item_id x audience x format"
    assert pairing["pair_key"] == ["evidence_item_id", "audience", "format", "stratum_id"]

    stats = cfg["statistics"]
    assert stats["confidence_level"] == 0.95
    assert stats["alpha"] == 0.05
    assert stats["confidence_interval"]["method"] == "paired_BCa_bootstrap"
    assert stats["confidence_interval"]["resamples"] >= 9999
    assert stats["hypothesis_test"]["method"] == "paired_randomization_sign_flip"
    assert stats["multiplicity"]["method"] == "Holm"

    pareto = cfg["pareto"]
    directions = {o["id"]: o["direction"] for o in pareto["objectives"]}
    assert directions == {
        "factuality": "maximize",
        "end_user_value": "maximize",
        "latency": "minimize",
        "cost": "minimize",
    }
    assert pareto["eligibility"] == "hard_gate_eligible_only"

    required_sources = {
        "SYSTEM/RESULTS/W003-T009-A01.md",
        "SYSTEM/RESULTS/W004-T005-A02.md",
        "SYSTEM/RESULTS/W004-T006-A01.md",
        "SYSTEM/RESULTS/W004-T007-A05.md",
        "SYSTEM/RESULTS/W004-T008-A02.md",
        "SYSTEM/PRODUCTION_CONTRACT.md",
        "SYSTEM/ASSUMPTION_RISK_REGISTER.md",
    }
    assert required_sources <= set(cfg["evidence_sources"])

    assert schema["$schema"].endswith("draft/2020-12/schema")
    assert schema["properties"]["methodology_id"]["const"] == cfg["methodology_id"]
    required = set(schema["required"])
    assert {"pairs", "aggregates", "hard_gates", "pareto", "statistics", "provenance"} <= required

if __name__ == "__main__":
    validate()
    print("PASS — W005 benchmark methodology v001 invariants validated")
