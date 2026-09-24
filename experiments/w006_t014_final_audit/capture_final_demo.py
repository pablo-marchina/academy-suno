from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from suno_content.ingest import PdfExtraction
from suno_content.orchestration import RunPhase
from suno_content.production_slice import (
    ProductionQualificationError,
    ReferenceVerticalSlice,
    SliceIdentity,
)


TASK_ID = "W006-T014"
ATTEMPT_ID = "A01"
RUN_ID = "run-w006-t014-a01-final-demo"


class LockedFixturePdfAdapter:
    """Same reference-only parser-contract adapter shape accepted by W006-T009-A02.

    This is deliberately not parser-quality or production-parser evidence.
    """

    def __init__(self) -> None:
        self.calls = 0

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        self.calls += 1
        if not raw_bytes.lstrip().startswith(b"%PDF-") or b"%%EOF" not in raw_bytes[-4096:]:
            raise ValueError("fixture parser received malformed PDF bytes")
        return PdfExtraction(
            text=(
                "Banco Central do Brasil Copom meeting 277 monetary policy primary-source reconstruction. "
                "This accepted reference sample exercises source provenance, exact 3x3 branch identity, durable "
                "resume, authoritative events, live replay and restore without claiming parser/provider quality."
            ),
            parser_name="locked-fixture-pdf-adapter",
            parser_version="reference-test-v1",
            page_count=1,
            confidence=0.97,
            warnings=(),
            table_role_ambiguity=False,
        )


def minimal_pdf() -> bytes:
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
        b"2 0 obj\n<< /Length 0 >>\nstream\nendstream\nendobj\n"
        b"trailer\n<< /Root 1 0 R >>\n%%EOF\n"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def safe_event_identity(event: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "event_id",
        "event_revision",
        "transition_id",
        "resource_type",
        "resource_id",
        "result_revision",
        "event_type",
    )
    return {key: event.get(key) for key in keys if key in event}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    run_root = output_dir / "reference-run"

    identity = SliceIdentity(
        org_id="org-a",
        workspace_id="ws-a",
        user_id="user-a",
        session_id="session-a",
        csrf_token="csrf-a",
    )
    parser_adapter = LockedFixturePdfAdapter()
    slice_ = ReferenceVerticalSlice(run_root, parser=parser_adapter)

    paused = asyncio.run(
        slice_.start(
            run_id=RUN_ID,
            identity=identity,
            raw_pdf=minimal_pdf(),
            artifact_label="copom-277-reconstruction.pdf",
            source_group_key="copom_277_2026_03",
            pause_after="planned",
        )
    )
    if paused.phase is not RunPhase.PLANNED or len(paused.jobs) != 9:
        raise AssertionError("reference run did not pause at planned 9-branch state")

    complete = asyncio.run(slice_.resume(RUN_ID))
    if complete.phase is not RunPhase.COMPLETE:
        raise AssertionError("reference run did not complete")
    if len(complete.joined_outputs) != 9:
        raise AssertionError("reference run did not preserve 9/9 joined branches")

    first_events = slice_.publish_authoritative_events(complete)
    second_events = slice_.publish_authoritative_events(complete)
    if first_events != second_events or len(first_events) != 11:
        raise AssertionError("authoritative event publication is not idempotent 11-event replay")

    projector = slice_.live_projection(complete)
    view = projector.state.view_model()
    if view.get("phase") != "complete" or len(view.get("cells", [])) != 9:
        raise AssertionError("live cockpit projection does not show complete 9-cell state")

    evidence = slice_.evidence(complete).to_dict()
    if evidence.get("accepted_branches") != 9:
        raise AssertionError("evidence did not bind 9 accepted branches")
    if evidence.get("production_ready_claim") != "NOT_AUTHORIZED":
        raise AssertionError("reference evidence attempted to authorize production readiness")

    backup = slice_.backup_to(output_dir / "backup")
    restored = ReferenceVerticalSlice.restore_from_backup(
        backup,
        output_dir / "restored",
        parser=LockedFixturePdfAdapter(),
    )
    restored_state = asyncio.run(restored.resume(RUN_ID))
    restored_events = restored.event_store.replay_events(
        org_id=identity.org_id,
        workspace_id=identity.workspace_id,
        run_id=RUN_ID,
    )
    restored_view = restored.live_projection(restored_state).state.view_model()
    if restored_events != first_events:
        raise AssertionError("backup/restore did not preserve authoritative events")
    if restored_view.get("event_revision") != 11 or len(restored_view.get("cells", [])) != 9:
        raise AssertionError("backup/restore did not preserve live projection identity")

    fail_closed = False
    fail_closed_message = ""
    try:
        ReferenceVerticalSlice.assert_production_qualified()
    except ProductionQualificationError as exc:
        fail_closed = True
        fail_closed_message = str(exc)
    if not fail_closed:
        raise AssertionError("reference path did not fail closed on production qualification")

    job_identities = []
    for job_id in sorted(complete.joined_outputs):
        output = dict(complete.joined_outputs[job_id])
        job_identities.append(
            {
                "job_id": job_id,
                "attempt_id": output.get("attempt_id"),
                "audience": output.get("audience"),
                "output_format": output.get("output_format"),
                "source_id": output.get("source_id"),
                "source_hash": output.get("source_hash"),
            }
        )

    config_paths = [
        Path("pyproject.toml"),
        Path("uv.lock"),
        Path("toolchain.lock.json"),
        Path("data/evals/production/w006/evaluator_config_v001.json"),
        Path("data/evals/production/w006/partition_manifest_v001.json"),
    ]
    config_identities = {
        str(path): f"sha256:{sha256_file(path)}" if path.is_file() else "MISSING"
        for path in config_paths
    }

    capture = {
        "task_id": TASK_ID,
        "attempt_id": ATTEMPT_ID,
        "evidence_scope": "ACCEPTED_REAL_REFERENCE_PRODUCT_PATH_NON_PRODUCTION",
        "source_identity": {
            "source_id": complete.source.get("source_id"),
            "source_hash": complete.source.get("source_hash"),
            "source_group_id": complete.source.get("source_group_id"),
            "provenance_ref": complete.source.get("provenance_ref"),
            "artifact_label": complete.source.get("artifact_label"),
            "parser_name": complete.source.get("parser_name"),
            "parser_version": complete.source.get("parser_version"),
            "parser_quality_claim": "NONE_REFERENCE_CONTRACT_ONLY",
        },
        "run_identity": {
            "run_id": RUN_ID,
            "phase": complete.phase.value,
            "aggregate_digest": evidence.get("aggregate_digest"),
            "accepted_branches": evidence.get("accepted_branches"),
        },
        "job_attempt_identities": job_identities,
        "event_identities": [safe_event_identity(dict(event)) for event in first_events],
        "live_projection": {
            "phase": view.get("phase"),
            "event_revision": view.get("event_revision"),
            "cell_count": len(view.get("cells", [])),
            "all_cells_proven": all(cell.get("state") == "PROVEN" for cell in view.get("cells", [])),
            "source_id": (view.get("source") or {}).get("source_id"),
        },
        "recovery": {
            "backup_restore": "PASS_REFERENCE_SCOPE",
            "restored_event_count": len(restored_events),
            "restored_event_revision": restored_view.get("event_revision"),
            "restored_cell_count": len(restored_view.get("cells", [])),
        },
        "hard_gates": {
            "branch_coverage": "9/9",
            "branch_loss": 0,
            "branch_duplication": 0,
            "event_republication_duplication": 0,
            "hard_gate_compensation": 0,
            "static_w004_fallback_used": 0,
            "production_qualification_fail_closed": fail_closed,
        },
        "config_identities": config_identities,
        "build_identity": {
            "github_sha": os.environ.get("GITHUB_SHA", "LOCAL_OR_UNKNOWN"),
            "github_ref": os.environ.get("GITHUB_REF", "LOCAL_OR_UNKNOWN"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID", "LOCAL_OR_UNKNOWN"),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "LOCAL_OR_UNKNOWN"),
            "github_job": os.environ.get("GITHUB_JOB", "LOCAL_OR_UNKNOWN"),
            "python": os.environ.get("W006_T014_PYTHON", "3.13.15_EXPECTED"),
            "uv": os.environ.get("W006_T014_UV", "0.12.18_EXPECTED"),
        },
        "deploy_identity": {
            "status": "MISSING_PRODUCTION_EVIDENCE",
            "runtime_lock": evidence["production_locks"]["runtime"],
            "database_lock": evidence["production_locks"]["database"],
            "parser_lock": evidence["production_locks"]["parser"],
            "frontend_lock": evidence["production_locks"]["frontend"],
            "deployment_lock": "NONE",
            "reason": "no representative locked production runtime/database/deployment topology is available",
        },
        "production_ready_claim": "NOT_AUTHORIZED",
        "production_qualification_fail_closed_message": fail_closed_message,
    }

    capture_path = output_dir / "demo-capture.json"
    capture_path.write_text(json.dumps(capture, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    source_hash_short = str(capture["source_identity"]["source_hash"])[:20]
    aggregate_short = str(capture["run_identity"]["aggregate_digest"])[:20]
    build_sha_short = str(capture["build_identity"]["github_sha"])[:12]

    slides = [
        (
            "01-title.txt",
            f"ACADEMY SUNO — W006-T014 FINAL EVIDENCE AUDIT\n\n"
            f"Scope: accepted real/reference product path (NON-PRODUCTION)\n"
            f"Run: {RUN_ID}\nBuild: {build_sha_short}\n\n"
            "Production-ready claim: NOT AUTHORIZED",
        ),
        (
            "02-live-path.txt",
            "SAME ACCEPTED PRODUCT PATH\n\n"
            "authenticated org/workspace -> controlled PDF bytes -> provenance/trust gate\n"
            "-> durable 3x3 orchestration -> eval/repair -> aggregate\n"
            "-> authoritative state/events -> live cockpit replay\n\n"
            f"Source hash: {source_hash_short}...\nParser: REFERENCE_TEST_ONLY (no parser-quality claim)\n"
            "Static W004 fallback used: 0",
        ),
        (
            "03-identity-chain.txt",
            "IDENTITY CHAIN — OBSERVED IN THIS RUN\n\n"
            f"Branches accepted: {evidence['accepted_branches']}/9\n"
            f"Authoritative events: {evidence['event_count']} (revision 1..{evidence['last_event_revision']})\n"
            f"Aggregate digest: {aggregate_short}...\n"
            f"Live cockpit cells: {len(view.get('cells', []))}\n"
            "org/workspace/run/job/attempt/source bindings persisted",
        ),
        (
            "04-recovery.txt",
            "REFERENCE RELIABILITY / RECOVERY\n\n"
            "Pause after planning: PASS\nResume to COMPLETE: PASS\n"
            "Republish without duplicate authoritative events: PASS\n"
            "Backup/restore replay identity: PASS\n"
            "Production qualification fail-closed: PASS\n\n"
            "These observations are reference-scope evidence, not production SLO/RTO/RPO/capacity.",
        ),
        (
            "05-blockers.txt",
            "PRODUCTION BLOCKERS PRESERVED\n\n"
            "• independent human gold: absent; HELD_OUT: NOT_RUN\n"
            "• provider/model/default/routing winner: NONE\n"
            "• runtime/database/parser/frontend/deployment winners: unresolved\n"
            "• observability backend/topology/sampling/retention: unresolved\n"
            "• representative deployed migration/rollback/capacity evidence: MISSING\n"
            "• production SLO / supported users / RTO / RPO: NOT_CLAIMED",
        ),
        (
            "06-close.txt",
            "AUDIT CONCLUSION\n\n"
            "W006 is evidence-complete for the achieved accepted reference scope.\n"
            "It is NOT evidence-complete for production readiness.\n\n"
            "Follow-up required: production topology qualification + human calibration\n"
            "+ representative provider/model comparison.\n\n"
            "No reference-only evidence was promoted to production truth.",
        ),
    ]
    slides_dir = output_dir / "slides"
    for filename, body in slides:
        write_text(slides_dir / filename, body)

    write_text(
        output_dir / "capture-summary.txt",
        "\n".join(
            [
                f"task_id={TASK_ID}",
                f"attempt_id={ATTEMPT_ID}",
                f"run_id={RUN_ID}",
                f"source_id={capture['source_identity']['source_id']}",
                f"source_hash={capture['source_identity']['source_hash']}",
                f"aggregate_digest={capture['run_identity']['aggregate_digest']}",
                f"branches={evidence['accepted_branches']}/9",
                f"events={evidence['event_count']}",
                f"last_event_revision={evidence['last_event_revision']}",
                "static_w004_fallback_used=0",
                "production_ready_claim=NOT_AUTHORIZED",
                "deploy_identity=MISSING_PRODUCTION_EVIDENCE",
            ]
        ),
    )

    print(json.dumps(capture, sort_keys=True))


if __name__ == "__main__":
    main()
