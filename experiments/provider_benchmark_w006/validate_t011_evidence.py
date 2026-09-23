#!/usr/bin/env python3
"""Fail-closed validator for W006-T011 provider benchmark evidence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "evals" / "production" / "w006"


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def validate() -> list[str]:
    errors: list[str] = []
    facts = load("provider_current_facts_t011_v001.json")
    manifest = load("provider_benchmark_manifest_t011_v001.json")
    observations = load("provider_benchmark_observations_t011_v001.json")
    pareto = load("provider_pareto_t011_v001.json")

    candidates = facts.get("candidates") or []
    candidate_ids = [c.get("candidate_id") for c in candidates]
    if candidate_ids != manifest.get("candidate_set"):
        errors.append("candidate set must be identical across catalog and frozen manifest")
    if len(candidate_ids) != len(set(candidate_ids)) or not candidate_ids:
        errors.append("candidate IDs must be unique and non-empty")

    for candidate in candidates:
        for field in ("provider", "model_id", "protocol", "endpoint"):
            if not candidate.get(field):
                errors.append(f"{candidate.get('candidate_id')}: missing {field}")
        pricing = candidate.get("pricing") or {}
        if not pricing.get("snapshot_id") or not pricing.get("checked_at_utc"):
            errors.append(f"{candidate.get('candidate_id')}: pricing identity/context missing")
        sources = candidate.get("sources") or []
        if not sources or any(not s.get("url") or not s.get("checked_at_utc") for s in sources):
            errors.append(f"{candidate.get('candidate_id')}: primary-source provenance missing")

    if manifest.get("methodology_id") != "W005-BENCHMARK-METHODOLOGY-V002":
        errors.append("accepted W005 benchmark methodology must be pinned")
    workload = manifest.get("workload") or {}
    if workload.get("derived_3x3_siblings_independent") is not False:
        errors.append("3x3 siblings must not inflate independent sample N")
    if workload.get("representative_benchmark_requirement_satisfied") is not False:
        errors.append("bootstrap workload must not be upgraded to representative production evidence")
    if manifest.get("production_ready_claim") != "NOT_AUTHORIZED":
        errors.append("production-ready claim is not authorized")
    if (manifest.get("routing") or {}).get("default_promotion_allowed") is not False:
        errors.append("default promotion must remain disabled without DRG-valid evidence")

    fresh = observations.get("fresh_execution") or {}
    if fresh.get("status") != "NOT_RUN":
        errors.append("this artifact set must not claim a fresh run that was not executed")
    rows = fresh.get("observations") or []
    if [row.get("candidate_id") for row in rows] != manifest.get("candidate_set"):
        errors.append("fresh observation rows must cover the frozen candidate set")
    for row in rows:
        if row.get("run_status") != "NOT_RUN":
            errors.append("unexecuted candidate cannot be marked observed")
        if any(row.get(k) is not None for k in ("quality", "latency_ms", "cost_usd")):
            errors.append("unexecuted candidate cannot carry fabricated measured objectives")
        if row.get("missingness") != "MISSING_CANDIDATE_OUTPUT":
            errors.append("missing candidate output must remain explicit")

    historical = observations.get("historical_mechanics_control") or {}
    if historical.get("evidence_class") != "OBSERVED_PROVIDER_MECHANICS":
        errors.append("historical control evidence class changed")
    if historical.get("quality") is not None:
        errors.append("historical mechanics control must not acquire synthetic quality")

    if pareto.get("pareto_status") != "PARETO_NOT_COMPUTABLE":
        errors.append("Pareto must remain not computable with required objectives missing")
    if pareto.get("decision_state") != "NO_PREFERENCE":
        errors.append("unresolved evidence must not force a winner")
    if pareto.get("promoted_default") is not None:
        errors.append("material default promotion is forbidden without complete evidence")
    if pareto.get("business_utility_status") != "PENDING_EVIDENCE":
        errors.append("business utility remains pending representative evidence")
    rollback = pareto.get("rollback") or {}
    if rollback.get("status") != "NOT_APPLICABLE_NO_PROMOTION":
        errors.append("rollback evidence must not be presented as PASS when no promotion was attempted")
    if rollback.get("promotion_gate_satisfied") is not False:
        errors.append("promotion gate cannot be satisfied without rollback PASS")
    if pareto.get("production_ready_claim") != "NOT_AUTHORIZED":
        errors.append("production-ready claim is not authorized")

    human = observations.get("human_evidence") or {}
    if human.get("independent_primary_streams") != 0 or human.get("adjudicated_gold_items") != 0:
        errors.append("T011 must not manufacture human evidence")
    if human.get("audience_threshold_status") != "DIAGNOSTIC_ONLY":
        errors.append("audience thresholds must remain diagnostic-only")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("FAIL — W006-T011 provider benchmark evidence")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS — W006-T011 evidence invariants validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
