#!/usr/bin/env python3
"""Validate W006-T010 eval/human-calibration foundation contracts.

Standard-library only. The validator intentionally fail-closes on split leakage,
model-only "human gold", hard-gate compensation, and 3x3/source-variant sample
inflation. It validates contracts and protocol fixtures; it does not fabricate
human annotations or production thresholds.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ALLOWED_SPLITS = {"DEV", "CALIBRATION", "HELD_OUT"}
MODEL_ONLY_EVIDENCE = {"MODEL_AUTOMATED_BLIND_CALIBRATION", "MODEL_JUDGE_CALIBRATED", "MACHINE_DETERMINISTIC"}
HUMAN_REFERENCE_EVIDENCE = {"HUMAN_INDEPENDENT_CALIBRATION", "HUMAN_ADJUDICATED_GOLD"}
LEGACY_HELD_OUT = {"petrobras_capex_fato_relevante_2024_08_08", "vale_2t26_production_sales"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_true(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def effective_source_n(rows: list[dict[str, Any]]) -> int:
    return len({row["source_group_id"] for row in rows})


def model_only_can_be_human_gold(evidence_classes: list[str]) -> bool:
    return bool(evidence_classes) and all(evidence in HUMAN_REFERENCE_EVIDENCE for evidence in evidence_classes)


def validate_pairing(baseline: list[dict[str, Any]], candidate: list[dict[str, Any]]) -> tuple[int, int]:
    key = lambda row: (row["source_group_id"], row["audience"], row["format"])
    baseline_keys = {key(row) for row in baseline}
    candidate_keys = {key(row) for row in candidate}
    if baseline_keys != candidate_keys:
        missing_candidate = sorted(baseline_keys - candidate_keys)
        missing_baseline = sorted(candidate_keys - baseline_keys)
        raise AssertionError(f"paired arms differ: missing_candidate={missing_candidate}, missing_baseline={missing_baseline}")
    return len(baseline_keys), len({k[0] for k in baseline_keys})


def validate_foundation(repo_root: Path) -> dict[str, Any]:
    w006_dir = repo_root / "data/evals/production/w006"
    exp_dir = repo_root / "experiments/eval_foundation_w006"
    partition = load_json(w006_dir / "partition_manifest_v001.json")
    human_schema = load_json(w006_dir / "human_annotation_record_schema_v001.json")
    judge = load_json(w006_dir / "judge_calibration_contract_v001.json")
    paired = load_json(w006_dir / "paired_experiment_contract_v001.json")
    evaluator = load_json(w006_dir / "evaluator_config_v001.json")
    status = load_json(exp_dir / "foundation_status_v001.json")
    checks: list[dict[str, str]] = []

    def check(condition: bool, check_id: str, detail: str) -> None:
        assert_true(condition, f"{check_id}: {detail}")
        checks.append({"check_id": check_id, "status": "PASS", "detail": detail})

    groups = partition["source_groups"]
    ids = [group["source_group_id"] for group in groups]
    check(len(ids) == len(set(ids)), "PARTITION_UNIQUE_SOURCE_GROUPS", "source_group_id unique")
    splits = [group["partition"] for group in groups]
    check(set(splits) <= ALLOWED_SPLITS, "PARTITION_ENUM", "only DEV/CALIBRATION/HELD_OUT")
    computed_counts = {split: splits.count(split) for split in sorted(ALLOWED_SPLITS)}
    check(computed_counts == partition["partition_counts"], "PARTITION_COUNTS", f"declared counts match computed {computed_counts}")
    held_out_ids = {g["source_group_id"] for g in groups if g["partition"] == "HELD_OUT"}
    check(held_out_ids == LEGACY_HELD_OUT, "LEGACY_HELD_OUT_PRESERVED", "historical W004 held-out source groups unchanged")
    check(partition["sample_accounting"]["derived_3x3_siblings_count_as_independent_draws"] is False, "NO_3X3_SAMPLE_INFLATION", "derived audience/format siblings never increase independent source N")
    check(partition["sample_accounting"]["parser_variants_count_as_independent_draws"] is False, "NO_PARSER_VARIANT_SAMPLE_INFLATION", "parser/OCR variants never increase independent source N")

    alias_owner: dict[str, str] = {}
    for group in groups:
        for alias in group.get("derived_group_aliases", []):
            assert_true(alias not in alias_owner, f"duplicate derived alias {alias}")
            alias_owner[alias] = group["source_group_id"]
    check(alias_owner.get("bcb-copom-277") == "copom_277_2026_03" and alias_owner.get("petrobras-2t26") == "petrobras_2t26_results", "T004_SOURCE_GROUP_ALIAS_BINDING", "T004 reconstructed groups map to one W004 source group each")

    upstream_path = repo_root / "data/evals/w004/source_manifest_v001.json"
    if upstream_path.exists():
        upstream = load_json(upstream_path)
        upstream_by_id = {source["source_id"]: source for source in upstream["sources"]}
        check(set(ids) == set(upstream_by_id), "UPSTREAM_SOURCE_MEMBERSHIP", "W006 bootstrap partitions cover exactly the six W004 source groups")
        for group in groups:
            legacy = upstream_by_id[group["source_id"]]["split"]
            check(legacy == group["legacy_w004_split"], f"LEGACY_SPLIT_{group['source_group_id']}", f"legacy split preserved as lineage ({legacy})")

    parser_manifest_path = repo_root / "experiments/document_parsing_w006/corpus_manifest.json"
    if parser_manifest_path.exists():
        parser_manifest = load_json(parser_manifest_path)
        parser_ids = {g["source_group_id"] for g in parser_manifest["source_groups"]}
        check(parser_ids == {"bcb-copom-277", "petrobras-2t26"}, "T004_PARSER_GROUPS_OBSERVED", "expected two T004 source groups present")
        check(parser_manifest["sample_accounting"]["source_group_count"] == 2 and parser_manifest["sample_accounting"]["variant_count"] == 8, "T004_VARIANTS_NOT_DRAWS", "2 source groups / 8 variants boundary preserved")

    evidence_enum = set(human_schema["properties"]["evidence_class"]["enum"])
    check(evidence_enum == HUMAN_REFERENCE_EVIDENCE, "HUMAN_SCHEMA_NO_MODEL_GOLD", "human annotation evidence class excludes model-only evidence")
    forbidden = set(human_schema["x_blinding"]["forbidden_primary_visible_fields"])
    check({"generation_target_audience", "evaluator_prediction", "peer_primary_annotation", "baseline_candidate_identity"} <= forbidden, "PRIMARY_BLINDING_FIELDS", "target/evaluator/peer/arm identity hidden from primaries")
    check(human_schema["x_blinding"]["same_person_both_primary_streams_for_item_allowed"] is False, "PRIMARY_INDEPENDENCE", "same person cannot provide both primary streams for an item")
    check(human_schema["x_gold_promotion"]["model_only_label_can_be_human_gold"] is False, "MODEL_ONLY_GOLD_FORBIDDEN", "schema explicitly forbids model-only human gold")

    allowed_refs = set(judge["reference_evidence_classes_allowed"])
    forbidden_refs = set(judge["reference_evidence_classes_forbidden"])
    check(allowed_refs == HUMAN_REFERENCE_EVIDENCE and MODEL_ONLY_EVIDENCE <= forbidden_refs, "JUDGE_REQUIRES_HUMAN_REFERENCE", "judge calibration requires human reference and rejects model-only reference")
    check(judge["hard_gate_override_allowed"] is False, "JUDGE_CANNOT_OVERRIDE_HARD_GATES", "secondary judge cannot override critical hard gates")

    check(paired["pairing"]["required_same_dataset_version"] is True and paired["pairing"]["cluster_key"] == "source_group_id" and paired["pairing"]["derived_3x3_siblings_are_independent_units"] is False, "PAIRED_SOURCE_CLUSTERING", "paired arms share dataset and cluster by source group")
    check(paired["decision"]["critical_hard_gate_regression_tolerance"] == 0 and paired["decision"]["hard_gates_non_compensatory"] is True and paired["decision"]["scalar_utility_can_compensate_hard_gate_failure"] is False, "NON_COMPENSATORY_EXPERIMENT_GATE", "hard-gate regressions have zero tolerance and cannot be compensated")
    check(paired["splits"]["held_out_may_drive_tuning"] is False, "HELD_OUT_NO_TUNING", "HELD_OUT is release replication only after freeze")

    check(evaluator["audience_thresholds"]["status"] == "DIAGNOSTIC_ONLY" and evaluator["audience_thresholds"]["freeze_allowed"] is False, "AUDIENCE_THRESHOLDS_DIAGNOSTIC_ONLY", "audience thresholds remain diagnostic until human calibration + held-out replication")
    check(evaluator["model_judge"]["enabled_for_release_evidence"] is False, "JUDGE_RELEASE_DISABLED", "model judge is not release evidence before calibration")
    check(evaluator["hard_gate_compensation_allowed"] is False, "EVALUATOR_HARD_GATE_COMPENSATION_ZERO", "hybrid evaluator cannot compensate hard-gate failure")

    human_status = status["human_evidence"]
    check(human_status["independent_primary_streams_observed"] == 0 and human_status["adjudicated_gold_items_observed"] == 0 and human_status["external_evidence_dependency"] is True, "NO_FAKE_HUMAN_EVIDENCE", "no human evidence is claimed; external collection remains explicit")
    check(status["thresholds"]["audience_threshold_status"] == "DIAGNOSTIC_ONLY" and status["thresholds"]["production_freeze_allowed"] is False and status["thresholds"]["held_out_replication_status"] == "NOT_RUN", "NO_THRESHOLD_PROMOTION", "no production audience threshold or held-out replication is claimed")
    check(status["parser_selection"]["w006_t004_decision_preserved"] == "NO_PRODUCTION_PARSER_WINNER", "PARSER_DECISION_BOUNDARY", "T004 no-winner boundary preserved")

    check(model_only_can_be_human_gold(["MODEL_AUTOMATED_BLIND_CALIBRATION", "MODEL_JUDGE_CALIBRATED"]) is False, "FIXTURE_MODEL_ONLY_REJECTED", "model/model-judge fixture rejected as human reference")
    check(model_only_can_be_human_gold(["HUMAN_INDEPENDENT_CALIBRATION", "HUMAN_ADJUDICATED_GOLD"]) is True, "FIXTURE_HUMAN_REFERENCE_ACCEPTED", "human-only reference classes accepted by the evidence classifier")

    sibling_rows = [{"source_group_id": "sg-one", "audience": audience, "format": fmt} for audience in ("BEGINNER", "INTERMEDIATE", "ADVANCED") for fmt in ("ARTICLE", "CAROUSEL", "SHORT_VIDEO")]
    check(effective_source_n(sibling_rows) == 1, "FIXTURE_3X3_EFFECTIVE_N_ONE", "nine derived siblings from one source group have effective independent N=1")
    baseline = sibling_rows + [{"source_group_id": "sg-two", "audience": "BEGINNER", "format": "ARTICLE"}]
    candidate = list(reversed(baseline))
    pair_count, source_count = validate_pairing(baseline, candidate)
    check(pair_count == 10 and source_count == 2, "FIXTURE_PAIRED_MATCH", "paired contract matches exact branch keys and source-group clusters")
    mismatch_rejected = False
    try:
        validate_pairing(baseline, candidate[:-1])
    except AssertionError:
        mismatch_rejected = True
    check(mismatch_rejected, "FIXTURE_UNPAIRED_REJECTED", "candidate/baseline branch mismatch fails closed")

    return {
        "report_version": "w006-t010-foundation-validation-v001",
        "task_id": "W006-T010",
        "attempt_id": "A01",
        "status": "PASS",
        "check_count": len(checks),
        "failed_check_count": 0,
        "checks": checks,
        "observed": {
            "source_group_count": len(groups),
            "partition_counts": computed_counts,
            "human_primary_streams_observed": 0,
            "human_adjudicated_gold_items_observed": 0,
            "model_only_human_gold_acceptances": 0,
            "hard_gate_compensation_paths": 0,
            "audience_threshold_status": "DIAGNOSTIC_ONLY",
            "held_out_replication_status": "NOT_RUN"
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2], help="Repository root; defaults from this script location.")
    parser.add_argument("--out", type=Path, default=None, help="Optional report path; defaults to experiments/eval_foundation_w006/validation_report.json")
    args = parser.parse_args()
    report = validate_foundation(args.repo_root)
    out = args.out or args.repo_root / "experiments/eval_foundation_w006/validation_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
