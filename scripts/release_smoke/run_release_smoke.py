#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKDIR = Path(tempfile.gettempdir()) / "academy-suno-release-smoke"

REQUIRED_COCKPIT_STATES = (
    "PROVEN",
    "DIAGNOSTIC_ONLY",
    "PRODUCTION_UNKNOWN",
)


class SmokeFailure(RuntimeError):
    pass


def _run(name: str, command: list[str], *, env: dict[str, str]) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise SmokeFailure(
            f"{name} failed with exit code {completed.returncode}\n"
            f"$ {' '.join(command)}\n{completed.stdout}"
        )
    return {
        "name": name,
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-4000:],
    }


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SmokeFailure(f"{path} must contain a JSON object")
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeFailure(message)


def run_release_smoke(workdir: Path) -> dict[str, Any]:
    workdir.mkdir(parents=True, exist_ok=True)
    proof_dir = workdir / "proof"
    cockpit_path = workdir / "evidence-cockpit.html"
    parser_path = workdir / "parser-w004.json"

    env = os.environ.copy()
    src = str(ROOT / "src")
    env["PYTHONPATH"] = src if not env.get("PYTHONPATH") else os.pathsep.join((src, env["PYTHONPATH"]))

    steps = [
        _run(
            "w003_mechanics_proof",
            [sys.executable, "experiments/w003_e2e/run_proof.py", "--output-dir", str(proof_dir)],
            env=env,
        ),
        _run(
            "evidence_cockpit",
            [
                sys.executable,
                "app/evidence_cockpit.py",
                "--runstore-history",
                str(proof_dir / "runstore_history_v001.json"),
                "--proof-report",
                str(proof_dir / "proof_report_v001.json"),
                "--telemetry-events",
                str(proof_dir / "telemetry_events_v001.jsonl"),
                "--task-attempt-id",
                "W004-T011-A01",
                "--output",
                str(cockpit_path),
            ],
            env=env,
        ),
        _run(
            "parser_source_trust_bakeoff",
            [
                sys.executable,
                "experiments/parser_w004/run_bakeoff.py",
                "--output",
                str(parser_path),
            ],
            env=env,
        ),
    ]

    proof = _json(proof_dir / "proof_report_v001.json")
    _require(proof.get("final_phase") == "complete", "mechanics proof did not reach complete")
    _require(proof.get("job_count") == 9 and proof.get("joined_output_count") == 9, "3x3 join is not 9/9")
    _require(proof.get("evidence_scope") == "MECHANICS_ONLY", "proof scope must remain MECHANICS_ONLY")
    _require(proof.get("provider_mode") == "deterministic_stub", "controlled proof provider marker drifted")
    _require(proof.get("provider_quality_claim") == "NOT_MADE", "provider quality was promoted without evidence")
    _require(proof.get("real_provider_cost_evidence") == "N/A", "real provider cost must remain N/A")

    repairs = proof.get("repair_lineage")
    _require(isinstance(repairs, list) and repairs, "persisted repair lineage is missing")
    repair = repairs[0]
    before = repair.get("before_snapshot_serialized") or {}
    after = repair.get("after_snapshot") or {}
    _require(before.get("status") == "FAIL", "demo lineage must start from a persisted FAIL")
    _require(after.get("status") == "PASS", "demo lineage must end in a persisted PASS after repair")
    _require(repair.get("fresh_hard_gate_runs") is True, "repair must execute fresh hard gates")
    _require(repair.get("siblings_immutable") is True, "repair must preserve accepted siblings")
    _require(repair.get("before_output_hash") != repair.get("after_output_hash"), "repair output hashes must differ")

    classification = proof.get("evidence_classification") or {}
    _require(classification.get("mechanics_end_to_end") == "PROVEN", "mechanics proof classification drifted")
    _require(classification.get("audience_thresholds") == "DIAGNOSTIC_ONLY", "audience thresholds must remain diagnostic")
    _require(classification.get("audience_confusion_matrices") == "NOT_COMPUTABLE", "human matrices must remain unavailable")
    _require(classification.get("provider_quality_latency_cost") == "PRODUCTION_UNKNOWN", "provider production evidence was promoted")
    _require(classification.get("semantic_ablation") == "NOT_RUN", "semantic ablation must not be fabricated")

    calibration = _json(ROOT / "experiments/calibration/current_evidence_v001.json")
    _require(calibration.get("audience_rows") == [], "unexpected human calibration rows require explicit review")
    _require(calibration.get("independent_agreement") is None, "independent agreement must remain absent in this checkpoint")
    provider_rows = calibration.get("provider_rows")
    _require(isinstance(provider_rows, list), "provider_rows must be a list")
    comparable_real_rows = [
        row for row in provider_rows
        if isinstance(row, dict)
        and row.get("quality_observed") is True
        and row.get("latency_observed") is True
        and str(row.get("pricing_provenance", "")).upper() not in {"", "SYNTHETIC"}
    ]
    _require(not comparable_real_rows, "unexpected comparable real-provider evidence requires release review")

    parser = _json(parser_path)
    aggregate = parser.get("aggregate_candidates") or {}
    _require((aggregate.get("provenance_preserving_reference") or {}).get("status") == "PASS", "parser reference must PASS")
    _require((aggregate.get("flat_value_only") or {}).get("status") == "REVIEW_REQUIRED", "flat values must remain REVIEW_REQUIRED")
    _require((aggregate.get("wrong_role_probe") or {}).get("status") == "FAIL", "wrong-role corruption must remain FAIL")
    _require((parser.get("implementation_decision") or {}).get("status") == "UNLOCKED", "parser implementation must remain unlocked")

    html = cockpit_path.read_text(encoding="utf-8")
    for marker in REQUIRED_COCKPIT_STATES:
        _require(marker in html, f"cockpit lost evidence marker {marker}")
    for key in ("before_output_hash", "after_output_hash"):
        value = repair.get(key)
        _require(isinstance(value, str) and value in html, f"cockpit does not expose {key}")
    source_hash = str(proof.get("run_id") or "")
    _require("MECHANICS_ONLY" in html, "cockpit must display mechanics-only scope")
    _require("No aggregate readiness score is computed" in html, "cockpit must preserve non-aggregate posture")

    return {
        "schema_version": "release-smoke.v1",
        "task_attempt_id": "W004-T011-A01",
        "status": "PASS",
        "steps": steps,
        "artifacts": {
            "proof_report": str(proof_dir / "proof_report_v001.json"),
            "runstore_history": str(proof_dir / "runstore_history_v001.json"),
            "telemetry_events": str(proof_dir / "telemetry_events_v001.jsonl"),
            "cockpit_html": str(cockpit_path),
            "parser_bakeoff": str(parser_path),
        },
        "lineage": {
            "job_id": repair.get("job_id"),
            "before_status": before.get("status"),
            "after_status": after.get("status"),
            "before_output_hash": repair.get("before_output_hash"),
            "after_output_hash": repair.get("after_output_hash"),
            "fresh_hard_gate_runs": repair.get("fresh_hard_gate_runs"),
            "siblings_immutable": repair.get("siblings_immutable"),
        },
        "evidence_posture": {
            "mechanics_end_to_end": "PROVEN",
            "audience_thresholds": "DIAGNOSTIC_ONLY",
            "human_confusion_matrices": "BLOCKED/PENDING",
            "real_provider_quality_latency_cost": "PRODUCTION_UNKNOWN/BLOCKED",
            "parser_implementation": "PENDING/UNLOCKED",
            "production_release_readiness": "PENDING_W004_T008",
        },
        "non_claims": [
            "No calibrated audience-threshold claim.",
            "No provider/model quality or preference claim.",
            "No real provider-cost claim.",
            "No production-readiness claim.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproducible release/cockpit smoke for integrated W003/W004 artifacts")
    parser.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or args.workdir / "manifest.json"
    try:
        manifest = run_release_smoke(args.workdir)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "schema_version": "release-smoke.v1",
            "task_attempt_id": "W004-T011-A01",
            "status": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(failure, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, ensure_ascii=False, indent=2, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
