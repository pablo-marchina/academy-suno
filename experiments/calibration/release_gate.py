from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

AUDIENCE_LABELS = ("BEGINNER", "INTERMEDIATE", "ADVANCED")
MANDATORY_ANTI_GAMING_CASES = {
    "jargon_stuffing": {"JARGON_STUFFING"},
    "sentence_chopping": {"SENTENCE_CHOPPING"},
    "acronym_hack": {"ACRONYM_HACK"},
    "required_concept_removal": {"REQUIRED_CONCEPT_OMISSION"},
}


class CalibrationInputError(ValueError):
    """Raised when calibration inputs violate split/provenance invariants."""


@dataclass(frozen=True)
class MetricRow:
    label: str
    precision: float
    recall: float
    f1: float
    support: int


def _safe_div(num: int, den: int) -> float:
    return num / den if den else 0.0


def confusion_matrix(
    truth: Sequence[str],
    predicted: Sequence[str],
    *,
    labels: Sequence[str] = AUDIENCE_LABELS,
) -> dict[str, dict[str, int]]:
    """Return a deterministic truth-row/prediction-column confusion matrix."""
    if len(truth) != len(predicted):
        raise CalibrationInputError("truth/predicted length mismatch")
    allowed = tuple(labels)
    unknown = sorted((set(truth) | set(predicted)) - set(allowed))
    if unknown:
        raise CalibrationInputError(f"unknown labels: {unknown}")
    matrix = {actual: {guess: 0 for guess in allowed} for actual in allowed}
    for actual, guess in zip(truth, predicted):
        matrix[actual][guess] += 1
    return matrix


def classification_metrics(
    truth: Sequence[str],
    predicted: Sequence[str],
    *,
    labels: Sequence[str] = AUDIENCE_LABELS,
) -> dict[str, object]:
    """Compute reproducible per-level and macro metrics from independent labels."""
    matrix = confusion_matrix(truth, predicted, labels=labels)
    label_order = tuple(labels)
    rows: list[MetricRow] = []
    correct = 0
    for label in label_order:
        tp = matrix[label][label]
        fp = sum(matrix[actual][label] for actual in label_order if actual != label)
        fn = sum(matrix[label][guess] for guess in label_order if guess != label)
        support = sum(matrix[label].values())
        precision = _safe_div(tp, tp + fp)
        recall = _safe_div(tp, tp + fn)
        f1 = _safe_div(2 * precision * recall, precision + recall)
        rows.append(MetricRow(label, precision, recall, f1, support))
        correct += tp
    total = len(truth)
    macro = {
        "precision": sum(row.precision for row in rows) / len(rows) if rows else 0.0,
        "recall": sum(row.recall for row in rows) / len(rows) if rows else 0.0,
        "f1": sum(row.f1 for row in rows) / len(rows) if rows else 0.0,
    }
    return {
        "sample_count": total,
        "labels": list(label_order),
        "confusion_matrix": matrix,
        "accuracy": _safe_div(correct, total),
        "macro": macro,
        "per_level": {
            row.label: {
                "precision": row.precision,
                "recall": row.recall,
                "f1": row.f1,
                "support": row.support,
            }
            for row in rows
        },
    }


def development_only(rows: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    """Reject any tuning/calibration row that is not explicitly DEVELOPMENT."""
    accepted: list[Mapping[str, object]] = []
    for row in rows:
        split = row.get("split")
        if split != "DEVELOPMENT":
            raise CalibrationInputError(
                f"calibration row {row.get('item_id', '<unknown>')} has forbidden split={split!r}"
            )
        accepted.append(row)
    return accepted


def audience_calibration(rows: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Separate requested-target→human behavior from human→evaluator performance."""
    dev_rows = development_only(rows)
    if not dev_rows:
        return {
            "status": "NOT_COMPUTABLE",
            "reason": "no development rows with independent human gold and evaluator predictions",
            "target_to_human": None,
            "human_to_evaluator": None,
        }
    required = {"generation_target_level", "human_gold_level", "evaluator_predicted_level"}
    for row in dev_rows:
        missing = sorted(key for key in required if not row.get(key))
        if missing:
            raise CalibrationInputError(
                f"row {row.get('item_id', '<unknown>')} missing fields: {missing}"
            )
    target = [str(row["generation_target_level"]) for row in dev_rows]
    human = [str(row["human_gold_level"]) for row in dev_rows]
    evaluator = [str(row["evaluator_predicted_level"]) for row in dev_rows]
    return {
        "status": "COMPUTED_DIAGNOSTIC",
        "target_to_human": classification_metrics(target, human),
        "human_to_evaluator": classification_metrics(human, evaluator),
        "note": "generation target is treatment/intent, never promoted to gold",
    }


def threshold_posture(
    manifest: Mapping[str, object],
    *,
    independent_agreement: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Never invent floors; freeze only when the manifest explicitly authorizes it."""
    policy = manifest.get("threshold_policy") or {}
    if not isinstance(policy, Mapping):
        raise CalibrationInputError("manifest.threshold_policy must be an object")
    gold_labels = manifest.get("gold_labels") or []
    blockers: list[str] = []
    if not gold_labels:
        blockers.append("NO_INDEPENDENT_HUMAN_GOLD_LABELS")
    if not independent_agreement:
        blockers.append("NO_INDEPENDENT_HUMAN_AGREEMENT")
    elif independent_agreement.get("status") != "SUFFICIENT":
        blockers.append("AGREEMENT_NOT_MARKED_SUFFICIENT")
    if policy.get("freeze_allowed") is not True:
        blockers.append("MANIFEST_FREEZE_NOT_AUTHORIZED")
    if blockers:
        return {
            "mode": "DIAGNOSTIC_ONLY",
            "freeze_allowed": False,
            "blockers": blockers,
            "numeric_thresholds": None,
        }
    return {
        "mode": "ELIGIBLE_FOR_EXTERNAL_FREEZE_REVIEW",
        "freeze_allowed": True,
        "blockers": [],
        "numeric_thresholds": None,
        "note": "this harness never manufactures thresholds; reviewed values must be supplied as versioned evidence",
    }


def anti_gaming_gate(cases: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Require mandatory readability/terminology/format anti-gaming cases to stay detected."""
    by_id = {str(case.get("case_id")): case for case in cases}
    missing = sorted(set(MANDATORY_ANTI_GAMING_CASES) - set(by_id))
    failures: dict[str, list[str]] = {}
    for case_id, required_flags in MANDATORY_ANTI_GAMING_CASES.items():
        case = by_id.get(case_id)
        if case is None:
            continue
        observed = {str(flag) for flag in case.get("observed_flags", [])}
        absent = sorted(required_flags - observed)
        if absent:
            failures[case_id] = absent
    return {
        "status": "PASS" if not missing and not failures else "FAIL",
        "mandatory_case_ids": sorted(MANDATORY_ANTI_GAMING_CASES),
        "missing_cases": missing,
        "missing_required_flags": failures,
        "case_count": len(by_id),
    }


def semantic_ablation_gate(rows: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Measure incremental semantic value without allowing hard-gate compensation."""
    records = list(rows)
    if not records:
        return {
            "status": "NOT_RUN",
            "decision": "NO_BACKEND_PREFERENCE",
            "reason": "no measured development-gold semantic ablation rows",
        }
    invariant_failures: list[str] = []
    changed = 0
    informative = 0
    for row in records:
        row_id = str(row.get("item_id", "<unknown>"))
        before_codes = tuple(sorted(str(x) for x in row.get("hard_fail_codes_without_semantic", [])))
        after_codes = tuple(sorted(str(x) for x in row.get("hard_fail_codes_with_semantic", [])))
        if before_codes != after_codes:
            invariant_failures.append(row_id)
        before = row.get("decision_without_semantic")
        after = row.get("decision_with_semantic")
        if before != after:
            changed += 1
        if row.get("semantic_added_information") is True:
            informative += 1
        if before_codes and after == "PASS":
            invariant_failures.append(row_id)
    return {
        "status": "FAIL" if invariant_failures else "PASS_DIAGNOSTIC",
        "sample_count": len(records),
        "decision_changed_count": changed,
        "semantic_added_information_count": informative,
        "hard_gate_invariant": not invariant_failures,
        "invariant_failure_item_ids": sorted(set(invariant_failures)),
        "decision": "NO_BACKEND_PREFERENCE",
    }


def provider_comparison_gate(rows: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Allow provider/model/backend comparison only from complete measured evidence."""
    records = list(rows)
    eligible = []
    excluded = defaultdict(list)
    for row in records:
        row_id = str(row.get("candidate_id", "<unknown>"))
        if row.get("evidence_kind") != "MEASURED":
            excluded[row_id].append("NOT_MEASURED")
        if row.get("pricing_provenance") == "SYNTHETIC":
            excluded[row_id].append("SYNTHETIC_PRICING")
        if row.get("quality_observed") is not True:
            excluded[row_id].append("QUALITY_NOT_OBSERVED")
        if row.get("latency_observed") is not True:
            excluded[row_id].append("LATENCY_NOT_OBSERVED")
        if not excluded[row_id]:
            eligible.append(row_id)
    comparable = len(eligible) >= 2
    return {
        "status": "COMPARABLE" if comparable else "NOT_COMPARABLE",
        "eligible_candidates": sorted(eligible),
        "excluded_candidates": {key: value for key, value in sorted(excluded.items()) if value},
        "decision": "NO_PREFERENCE" if not comparable else "EXTERNAL_REVIEW_REQUIRED",
        "note": "synthetic demo pricing never counts as provider-cost evidence",
    }


def build_release_gate(
    *,
    manifest: Mapping[str, object],
    audience_rows: Iterable[Mapping[str, object]] = (),
    anti_gaming_cases: Iterable[Mapping[str, object]] = (),
    semantic_rows: Iterable[Mapping[str, object]] = (),
    provider_rows: Iterable[Mapping[str, object]] = (),
    independent_agreement: Mapping[str, object] | None = None,
) -> dict[str, object]:
    sources = manifest.get("sources") or []
    if not isinstance(sources, list):
        raise CalibrationInputError("manifest.sources must be a list")
    development_sources = [s for s in sources if isinstance(s, Mapping) and s.get("split") == "DEVELOPMENT"]
    held_out_sources = [s for s in sources if isinstance(s, Mapping) and s.get("split") == "HELD_OUT"]
    for source in held_out_sources:
        if source.get("tuning_exposure") != "FORBIDDEN":
            raise CalibrationInputError("held-out source must keep tuning_exposure=FORBIDDEN")

    threshold = threshold_posture(manifest, independent_agreement=independent_agreement)
    audience = audience_calibration(audience_rows)
    anti_gaming = anti_gaming_gate(anti_gaming_cases)
    semantic = semantic_ablation_gate(semantic_rows)
    provider = provider_comparison_gate(provider_rows)

    blockers = list(threshold["blockers"])
    if audience["status"] == "NOT_COMPUTABLE":
        blockers.append("AUDIENCE_CONFUSION_METRICS_NOT_COMPUTABLE")
    if anti_gaming["status"] != "PASS":
        blockers.append("ANTI_GAMING_GATE_FAILED")
    if semantic["status"] == "FAIL":
        blockers.append("SEMANTIC_HARD_GATE_INVARIANT_FAILED")

    return {
        "schema_version": "calibration-release-gate.v1",
        "benchmark_version": manifest.get("benchmark_version"),
        "development_source_ids": [s.get("source_id") for s in development_sources],
        "held_out_source_ids": [s.get("source_id") for s in held_out_sources],
        "held_out_tuning_exposure": "FORBIDDEN",
        "audience_calibration": audience,
        "threshold_posture": threshold,
        "anti_gaming": anti_gaming,
        "semantic_ablation": semantic,
        "provider_comparison": provider,
        "overall_mode": "DIAGNOSTIC_ONLY" if blockers else "ELIGIBLE_FOR_EXTERNAL_RELEASE_REVIEW",
        "release_blockers": sorted(set(blockers)),
        "kill_criteria": [
            "HELD_OUT_TOUCHED_BY_TUNING",
            "TARGET_PROMOTED_TO_GOLD",
            "UNVERSIONED_OR_UNPROVENANCED_GOLD",
            "HARD_GATE_COMPENSATED_BY_SOFT_OR_SEMANTIC_SIGNAL",
            "ANTI_GAMING_MANDATORY_CASE_MISSED",
            "SYNTHETIC_PRICING_PRESENTED_AS_PROVIDER_COST",
        ],
    }


def _load(path: str | None, default: object) -> object:
    if path is None:
        return default
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Development-only calibration/ablation release gate")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--audience-rows")
    parser.add_argument("--anti-gaming-cases")
    parser.add_argument("--semantic-rows")
    parser.add_argument("--provider-rows")
    parser.add_argument("--agreement")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_release_gate(
        manifest=_load(args.manifest, {}),
        audience_rows=_load(args.audience_rows, []),
        anti_gaming_cases=_load(args.anti_gaming_cases, []),
        semantic_rows=_load(args.semantic_rows, []),
        provider_rows=_load(args.provider_rows, []),
        independent_agreement=_load(args.agreement, None),
    )
    Path(args.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
