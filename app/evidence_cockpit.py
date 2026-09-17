#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.cockpit import (  # noqa: E402
    build_cockpit_snapshot,
    load_json_artifact,
    load_run_state_from_history,
    load_run_state_from_sqlite,
    render_html,
)
from suno_content.cockpit.adapters import load_jsonl_artifact  # noqa: E402

DEFAULT_CALIBRATION = ROOT / "experiments" / "calibration" / "current_evidence_v001.json"
DEFAULT_TELEMETRY = ROOT / "experiments" / "telemetry" / "demo_summary_v001.json"


def _existing_default(path: Path) -> Path | None:
    return path if path.exists() else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render the B13 evidence cockpit as a read-only projection over existing "
            "RunStore/proof/telemetry/calibration artifacts."
        )
    )
    run_group = parser.add_mutually_exclusive_group()
    run_group.add_argument("--runstore-history", type=Path, help="Exported RunStore history JSON")
    run_group.add_argument("--runstore-db", type=Path, help="Existing SQLite RunStore database")
    parser.add_argument("--run-id", help="Required with --runstore-db")
    parser.add_argument("--proof-report", type=Path, help="Versioned proof report JSON")
    parser.add_argument(
        "--telemetry-summary",
        type=Path,
        default=None,
        help="Telemetry summary JSON (otherwise proof telemetry is used; repository diagnostic demo is final fallback)",
    )
    parser.add_argument("--telemetry-events", type=Path, help="Telemetry events JSONL for job/attempt lineage")
    parser.add_argument(
        "--calibration",
        type=Path,
        default=_existing_default(DEFAULT_CALIBRATION),
        help="Calibration evidence JSON (defaults to repository current evidence artifact)",
    )
    parser.add_argument("--task-attempt-id", default="W004-T001-A01")
    parser.add_argument("--title", default="Suno Evidence Cockpit")
    parser.add_argument("--output", type=Path, default=ROOT / "app" / "evidence_cockpit.html")
    args = parser.parse_args()

    if args.runstore_db is not None and not args.run_id:
        parser.error("--run-id is required with --runstore-db")

    artifact_refs: dict[str, str] = {}
    run_state = None
    observed_at = None
    if args.runstore_history is not None:
        run_state, observed_at = load_run_state_from_history(args.runstore_history)
        artifact_refs["runstore"] = str(args.runstore_history)
    elif args.runstore_db is not None:
        run_state = load_run_state_from_sqlite(args.runstore_db, args.run_id)
        artifact_refs["runstore"] = f"{args.runstore_db}#run_id={args.run_id}"

    proof_report = None
    if args.proof_report is not None:
        proof_report = load_json_artifact(args.proof_report)
        if not isinstance(proof_report, dict):
            parser.error("--proof-report must contain a JSON object")
        artifact_refs["proof_report"] = str(args.proof_report)

    telemetry_summary = None
    if args.telemetry_summary is not None:
        telemetry_summary = load_json_artifact(args.telemetry_summary)
        if not isinstance(telemetry_summary, dict):
            parser.error("--telemetry-summary must contain a JSON object")
        artifact_refs["telemetry"] = str(args.telemetry_summary)
    elif proof_report and isinstance(proof_report.get("telemetry"), dict):
        telemetry_summary = proof_report["telemetry"]
        artifact_refs["telemetry"] = f"{artifact_refs.get('proof_report', 'proof_report')}#telemetry"
    elif DEFAULT_TELEMETRY.exists():
        telemetry_summary = load_json_artifact(DEFAULT_TELEMETRY)
        if not isinstance(telemetry_summary, dict):
            parser.error("repository telemetry fallback must contain a JSON object")
        artifact_refs["telemetry"] = str(DEFAULT_TELEMETRY)

    telemetry_events = ()
    if args.telemetry_events is not None:
        telemetry_events = load_jsonl_artifact(args.telemetry_events)
        artifact_refs["telemetry_events"] = str(args.telemetry_events)

    calibration = None
    if args.calibration is not None:
        calibration = load_json_artifact(args.calibration)
        if not isinstance(calibration, dict):
            parser.error("--calibration must contain a JSON object")
        artifact_refs["calibration"] = str(args.calibration)

    snapshot = build_cockpit_snapshot(
        run_state=run_state,
        telemetry_summary=telemetry_summary,
        telemetry_events=telemetry_events,
        calibration=calibration,
        proof_report=proof_report,
        task_attempt_id=args.task_attempt_id,
        observed_at=observed_at,
        artifact_refs=artifact_refs,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(snapshot, title=args.title), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
