"""W009 AI-only evaluation harness: reproducible blind rows and fail-closed gates.

Reference/diagnostic implementation. Does not execute a model provider or
certify human comprehension, production safety, source authenticity or trust.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from suno_content.domain import AudienceLevel, GateStatus, OutputFormat
from suno_content.factual.checks import evaluate_case

HARNESS_VERSION = "ai-only-w009.v1"
GATES = ("source", "factual", "policy", "schema", "provenance")
AUDIENCES = frozenset(item.value for item in AudienceLevel)
FORMATS = frozenset(item.value for item in OutputFormat)
BRANCHES = frozenset((audience, fmt) for audience in AUDIENCES for fmt in FORMATS)
SPLIT_BOUNDARIES = (60, 80)  # Preregistered assignment policy, not a quality threshold.


class EvidenceError(ValueError):
    """Reject missing, ambiguous or inconsistent input rather than filling gaps."""


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source_group_split(source_group_id: str, *, split_salt: str) -> str:
    """Stable by *source group*, never by content variant to avoid split leakage."""
    if not source_group_id.strip() or not split_salt.strip():
        raise EvidenceError("source group and split salt are required")
    bucket = int(digest(f"{split_salt}|{source_group_id}")[:12], 16) % 100
    if bucket < SPLIT_BOUNDARIES[0]:
        return "DEV"
    if bucket < SPLIT_BOUNDARIES[1]:
        return "CALIBRATION"
    return "HELD_OUT"


def _identity(raw: Any, field: str) -> tuple[str, str, str]:
    if not isinstance(raw, dict):
        raise EvidenceError(f"{field} identity must be an object")
    value = tuple(raw.get(key) for key in ("provider", "model", "version"))
    if any(not isinstance(x, str) or not x.strip() for x in value):
        raise EvidenceError(f"{field} identity requires provider/model/version")
    return value  # type: ignore[return-value]


def _gate(value: Any, *, label: str) -> GateStatus:
    if not isinstance(value, str):
        raise EvidenceError(f"{label} requires an explicit gate status")
    try:
        return GateStatus(value)
    except ValueError as exc:
        raise EvidenceError(f"{label} invalid gate status") from exc


def _combine(statuses: list[GateStatus]) -> GateStatus:
    if GateStatus.FAIL in statuses:
        return GateStatus.FAIL
    if GateStatus.REVIEW_REQUIRED in statuses:
        return GateStatus.REVIEW_REQUIRED
    return GateStatus.PASS


def _required_str(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{key} must be a non-empty string")
    return value


def evaluate_run(raw: Mapping[str, Any], *, split_salt: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Evaluate explicit branch evidence; never consume labels or predicted scores.

    Any missing branch, missing hard gate, duplicate or missing source evidence
    prevents an all-PASS result. Deterministic factual checks are sourced from
    the existing financial check engine; no semantic/human gold is synthesized.
    """
    if raw.get("schema_version") != "ai_only_w009.input.v1":
        raise EvidenceError("unsupported input schema version")
    run_id = _required_str(raw, "run_id")
    source_group_id = _required_str(raw, "source_group_id")
    evidence_class = _required_str(raw, "evidence_class")
    if evidence_class not in {"SYNTHETIC_FIXTURE", "SOURCE_GROUNDED_DIAGNOSTIC", "PROVIDER_OBSERVED"}:
        raise EvidenceError("unknown evidence class")
    generator = _identity(raw.get("generator"), "generator")
    judge = raw.get("judge")
    if judge is not None and _identity(judge, "judge") == generator:
        raise EvidenceError("same provider/model/version cannot be its own independent judge")
    if raw.get("human_annotations") is not None or raw.get("human_gold") is not None:
        raise EvidenceError("AI-only harness never accepts human-gold claim fields")
    source = raw.get("source")
    if not isinstance(source, dict):
        raise EvidenceError("source must be an evidence object")
    spans = source.get("spans")
    if not isinstance(spans, list) or not spans or any(
        not isinstance(span, dict)
        or not isinstance(span.get("span_id"), str)
        or not span["span_id"].strip()
        or not isinstance(span.get("text"), str)
        or not span["text"].strip()
        for span in spans
    ):
        raise EvidenceError("source must contain nonempty evidence spans with identifiers")
    span_ids = [span["span_id"] for span in spans]
    if len(span_ids) != len(set(span_ids)):
        raise EvidenceError("duplicate source span identifiers")
    if not isinstance(raw.get("variants"), list):
        raise EvidenceError("variants must be an array")
    variants = raw["variants"]
    seen: set[tuple[str, str]] = set()
    statuses: list[GateStatus] = []
    findings: list[dict[str, Any]] = []
    blind_items: list[dict[str, Any]] = []
    source_status = _gate(source.get("status"), label="source.status")

    for variant in variants:
        if not isinstance(variant, dict):
            raise EvidenceError("each variant must be an object")
        audience, fmt = _required_str(variant, "audience"), _required_str(variant, "format")
        pair = (audience, fmt)
        if pair not in BRANCHES:
            raise EvidenceError("unknown 3x3 audience/format")
        if pair in seen:
            raise EvidenceError("duplicate 3x3 branch")
        seen.add(pair)
        output = _required_str(variant, "output")
        hard_gates = variant.get("hard_gates")
        if not isinstance(hard_gates, dict) or set(hard_gates) != set(GATES):
            raise EvidenceError("all five non-compensatory hard gates required, no extras")
        gate_values = {key: _gate(hard_gates[key], label=f"hard_gates.{key}") for key in GATES}
        gate_values["source"] = _combine([source_status, gate_values["source"]])
        # No access to oracle outcomes. Existing factual deterministic checks
        # apply to the same supplied evidence across all nine branches.
        case = {
            "id": digest(f"{run_id}|{audience}|{fmt}")[:20],
            "source": source,
            "adversarial_output": output,
        }
        factual = evaluate_case(case)
        gate_values["factual"] = _combine([gate_values["factual"], factual.decision])
        decision = _combine(list(gate_values.values()))
        statuses.append(decision)
        blinded_id = digest(f"{split_salt}|{run_id}|{audience}|{fmt}")[:24]
        findings.append(
            {
                "blind_id": blinded_id,
                "audience": audience,
                "format": fmt,
                "status": decision.value,
                "hard_gates": {name: status.value for name, status in gate_values.items()},
                "factual_failure_code": factual.failure_code,
                "factual_support_status": factual.support_status,
                "evidence_span_ids": list(factual.evidence_span_ids),
                "judge_status": "NOT_RUN",
            }
        )
        blind_items.append(
            {
                "blind_id": blinded_id,
                "target_audience": audience,
                "target_format": fmt,
                "evidence_spans": [{"span_id": s["span_id"], "text": s["text"]} for s in spans],
                "candidate_text": output,
                "rubric_version": "machine_judge_secondary_v1_NOT_EXECUTED",
            }
        )

    missing = sorted(BRANCHES - seen)
    if missing:
        # Partial evidence is reportable, never silently accepted as a complete run.
        statuses.append(GateStatus.REVIEW_REQUIRED)
    overall = _combine(statuses) if statuses else GateStatus.REVIEW_REQUIRED
    result = {
        "schema_version": "ai_only_w009.report.v1",
        "harness_version": HARNESS_VERSION,
        "run_id": run_id,
        "source_group_digest": digest(f"{split_salt}|{source_group_id}"),
        "split": source_group_split(source_group_id, split_salt=split_salt),
        "evidence_class": evidence_class,
        "generator": {"provider": generator[0], "model": generator[1], "version": generator[2]},
        "configured_judge": None if judge is None else {
            "provider": _identity(judge, "judge")[0],
            "model": _identity(judge, "judge")[1],
            "version": _identity(judge, "judge")[2],
        },
        "judge_status": "NOT_RUN",
        "human_gold_eligible": False,
        "audience_thresholds": "DIAGNOSTIC_ONLY",
        "production_ready": False,
        "branch_count_observed": len(seen),
        "branch_count_expected": len(BRANCHES),
        "missing_branches": [{"audience": a, "format": f} for a, f in missing],
        "overall_status": overall.value,
        "counts": dict(Counter(status.value for status in statuses[:len(seen)])),
        "raw_findings": sorted(findings, key=lambda x: (x["audience"], x["format"])),
        "uncertainty": "No human data or external judge; deterministic heuristics are not comprehensive source verification.",
        "not_run": [
            "external_blinded_model_judge",
            "source_original_financial_benchmark",
            "cross_output_semantic_contradiction_judge",
            "human_comprehension_calibration",
            "production_quality_threshold_calibration",
        ],
    }
    return result, sorted(blind_items, key=lambda x: digest(x["blind_id"]))


def evaluate_corpus(runs: list[Mapping[str, Any]], *, split_salt: str) -> dict[str, Any]:
    if not runs:
        raise EvidenceError("corpus must contain at least one run")
    reports = []
    seen_runs: set[str] = set()
    group_partitions: dict[str, str] = {}
    for run in runs:
        report, _ = evaluate_run(run, split_salt=split_salt)
        if report["run_id"] in seen_runs:
            raise EvidenceError("duplicate run_id in corpus")
        seen_runs.add(report["run_id"])
        digest_key, partition = report["source_group_digest"], report["split"]
        if digest_key in group_partitions and group_partitions[digest_key] != partition:
            raise EvidenceError("source group split leakage")
        group_partitions[digest_key] = partition
        reports.append(report)
    return {
        "schema_version": "ai_only_w009.corpus_report.v1",
        "harness_version": HARNESS_VERSION,
        "run_count": len(reports),
        "source_group_count": len(group_partitions),
        "source_group_splits": dict(Counter(group_partitions.values())),
        "run_statuses": dict(Counter(report["overall_status"] for report in reports)),
        "human_gold_eligible": False,
        "model_judge_status": "NOT_RUN",
        "production_ready": False,
        "reports": reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline AI-only pre-judge deterministic diagnostic")
    parser.add_argument("--input", type=Path, required=True, help="JSON input corpus list")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--blind-output", type=Path, required=True)
    parser.add_argument("--split-salt", required=True, help="fixed preregistered group-split salt")
    args = parser.parse_args()
    raw = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        parser.error("--input must be a JSON array")
    report = evaluate_corpus(raw, split_salt=args.split_salt)
    blind_rows: list[dict[str, Any]] = []
    for item in raw:
        _, rows = evaluate_run(item, split_salt=args.split_salt)
        blind_rows.extend(rows)
    # Both files contain content and might be sensitive; never target a public
    # web service directory, Github logs or automatically committed artifacts.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.blind_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.blind_output.write_text(
        json.dumps(blind_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
