#!/usr/bin/env python3
"""Dependency-light validation for W005 benchmark methodology v002."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "data/evals/w005/benchmark_methodology_v002.json"
SCHEMA = ROOT / "data/evals/w005/benchmark_result_v002.schema.json"
METHODOLOGY = ROOT / "docs/evals/benchmark_methodology_w005.md"
DR = ROOT / "docs/decisions/research/DR-5909-cross-cutting-benchmark-methodology.md"

FAIL_STATES = {"FAIL", "REVIEW_REQUIRED", "NOT_COMPUTABLE"}


def is_eligible(gate_states: Mapping[str, str]) -> bool:
    """Required gates are non-compensatory. NOT_APPLICABLE may pass through."""
    return not any(state in FAIL_STATES for state in gate_states.values())


def dominates(a: Mapping[str, float], b: Mapping[str, float], directions: Mapping[str, str]) -> bool:
    """Return True when a point-dominates b on every declared objective."""
    no_worse = True
    strictly_better = False
    for metric, direction in directions.items():
        av = a[metric]
        bv = b[metric]
        if direction == "maximize":
            if av < bv:
                no_worse = False
                break
            if av > bv:
                strictly_better = True
        elif direction == "minimize":
            if av > bv:
                no_worse = False
                break
            if av < bv:
                strictly_better = True
        else:
            raise ValueError(f"unsupported direction: {direction}")
    return no_worse and strictly_better


def point_pareto_frontier(
    candidate_metrics: Mapping[str, Mapping[str, float]],
    directions: Mapping[str, str],
    eligible: Iterable[str],
) -> List[str]:
    """Compute a deterministic point Pareto frontier for eligible candidates."""
    eligible_ids = sorted(set(eligible))
    frontier: List[str] = []
    for cid in eligible_ids:
        if cid not in candidate_metrics:
            raise KeyError(f"missing metrics for eligible candidate {cid}")
        metrics = candidate_metrics[cid]
        if set(directions) - set(metrics):
            raise KeyError(f"missing objective for eligible candidate {cid}")
        if not any(
            other != cid and dominates(candidate_metrics[other], metrics, directions)
            for other in eligible_ids
        ):
            frontier.append(cid)
    return frontier


def utility_preference_allowed(utility: Mapping[str, object]) -> bool:
    """Only evidence-supported, sensitivity-stable utility may emit preference."""
    if utility.get("status") != "EVIDENCE_SUPPORTED":
        return False
    refs = utility.get("evidence_refs")
    sensitivity = utility.get("sensitivity")
    weights = utility.get("weights")
    if not isinstance(refs, list) or not refs:
        return False
    if not isinstance(weights, dict) or not weights:
        return False
    if abs(sum(float(v) for v in weights.values()) - 1.0) > 1e-9:
        return False
    if not isinstance(sensitivity, dict) or sensitivity.get("preferred_set_stable") is not True:
        return False
    return True


def validate() -> None:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    methodology = METHODOLOGY.read_text(encoding="utf-8")
    dr = DR.read_text(encoding="utf-8")

    assert cfg["methodology_id"] == "W005-BENCHMARK-METHODOLOGY-V002"
    assert cfg["attempt_id"] == "A02"
    decision = cfg["decision_contract"]
    assert decision["hard_gates_non_compensatory"] is True
    assert decision["default_overall_status"] == "NO_PREFERENCE"
    assert decision["business_utility_status"] == "PENDING_EVIDENCE"
    assert decision["default_order"][:4] == [
        "hard_gates", "raw_multidimensional_metrics", "uncertainty", "point_pareto"
    ]

    # The A01 failure mode must be structurally impossible in v002 config.
    utility = cfg["utility"]
    assert utility["status"] == "BUSINESS_UTILITY_PENDING_EVIDENCE"
    assert utility["weights"] is None
    assert utility["anchors"] is None
    assert utility["practical_thresholds"] is None
    assert cfg["statistics"]["practical_materiality"]["fixed_thresholds"] is None
    assert cfg["pareto"]["epsilon_frontier"]["status"] == "PENDING_EVIDENCE"

    pairing = cfg["paired_design"]
    assert pairing["correlation_block"] == "source_group_id"
    assert "never_count_3x3_outputs_from_one_source_as_independent_sources" in pairing["rules"]

    stats = cfg["statistics"]
    assert stats["status"] == "STATISTICAL_METHOD_LOCK"
    assert stats["confidence_interval"]["seed"] == "REQUIRED_IN_RUN_MANIFEST"
    assert stats["confidence_interval"]["resamples"] == "REQUIRED_IN_RUN_MANIFEST"
    assert stats["deterministic_binary_invariants"]["evidence"] == "PASS_FAIL"
    assert stats["multiplicity"]["method"] == "Holm"

    assert cfg["stopping"]["global_numeric_sample_size"] is None
    assert cfg["stopping"]["global_effect_threshold"] is None

    assert schema["properties"]["methodology_id"]["const"] == cfg["methodology_id"]
    required = set(schema["required"])
    assert {"observations", "aggregates", "hard_gates", "pareto", "statistics", "decision", "provenance"} <= required
    practical_enum = schema["$defs"]["stat_result"]["properties"]["practical_materiality"]["enum"]
    assert "PENDING_EVIDENCE" in practical_enum
    assert "BETTER" not in schema["$defs"]["stat_result"]["properties"]["statistical_direction"]["enum"]
    utility_statuses = schema["$defs"]["utility"]["properties"]["status"]["enum"]
    assert "PENDING_EVIDENCE" in utility_statuses and "EVIDENCE_SUPPORTED" in utility_statuses

    # Documentation must state the corrected separation explicitly.
    for token in [
        "STATISTICAL_METHOD_LOCK",
        "BUSINESS_UTILITY_STATUS",
        "NO_PREFERENCE",
        "PENDING_EVIDENCE",
        "source_group_id",
        "Statistical significance does **not** establish business importance",
    ]:
        assert token in methodology
    assert "BUSINESS_UTILITY_PENDING_EVIDENCE" in dr
    # Historical A01 values may be named only as rejected diagnostic policy;
    # v002 prevents them structurally from becoming active utility/threshold config.
    assert "| 40/30/15/15 headline score | **REJECT** |" in methodology

    # Executable decision-surface probes.
    assert is_eligible({"FACTUAL": "PASS", "PAIRING": "PASS"})
    assert not is_eligible({"FACTUAL": "FAIL", "PAIRING": "PASS"})
    assert not is_eligible({"FACTUAL": "REVIEW_REQUIRED"})

    directions = {"quality": "maximize", "latency_ms": "minimize", "cost_usd": "minimize"}
    metrics = {
        "A": {"quality": 90.0, "latency_ms": 120.0, "cost_usd": 0.03},
        "B": {"quality": 88.0, "latency_ms": 100.0, "cost_usd": 0.02},
        "C": {"quality": 80.0, "latency_ms": 150.0, "cost_usd": 0.04},
    }
    assert point_pareto_frontier(metrics, directions, ["A", "B", "C"]) == ["A", "B"]
    assert utility_preference_allowed({"status": "PENDING_EVIDENCE", "weights": None, "evidence_refs": [], "sensitivity": {"preferred_set_stable": False}}) is False
    assert utility_preference_allowed({
        "status": "EVIDENCE_SUPPORTED",
        "weights": {"quality": 0.7, "cost": 0.3},
        "evidence_refs": ["human-priority-study-v1"],
        "sensitivity": {"preferred_set_stable": True},
    }) is True


if __name__ == "__main__":
    validate()
    print("PASS — W005 benchmark methodology v002 invariants validated")
