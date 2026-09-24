from __future__ import annotations

import argparse
import asyncio
import inspect
import json
import math
import resource
import statistics
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from suno_content.ingest import PdfExtraction, UploadRoute, preflight_pdf_upload
from suno_content.production_slice import ReferenceVerticalSlice, SliceIdentity
from suno_content.security import (
    AccessSurface,
    Action,
    DenyByDefaultAuthorizer,
    Membership,
    Role,
    SecurityDirectory,
    TenantIsolationError,
    TenantResource,
    sanitize_event_payload,
    sanitize_telemetry_attributes,
)


VALID_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    b"2 0 obj\n<< /Length 0 >>\nstream\nendstream\nendobj\n"
    b"trailer\n<< /Root 1 0 R >>\n%%EOF\n"
)


@dataclass
class LockedFixturePdfAdapter:
    calls: int = 0

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        self.calls += 1
        if not raw_bytes.lstrip().startswith(b"%PDF-") or b"%%EOF" not in raw_bytes[-4096:]:
            raise ValueError("fixture parser received malformed PDF bytes")
        return PdfExtraction(
            text=(
                "Banco Central do Brasil Copom meeting 277 monetary policy primary-source reconstruction. "
                "This controlled sample exercises source provenance, exact branch identity, durable resume, "
                "authoritative events, reconnect, retry isolation, and database restore without claiming parser quality."
            ),
            parser_name="locked-fixture-pdf-adapter",
            parser_version="reference-test-v1",
            page_count=1,
            confidence=0.97,
            warnings=(),
            table_role_ambiguity=False,
        )


def percentile(values: Iterable[float], q: float) -> float | None:
    data = sorted(float(value) for value in values)
    if not data:
        return None
    if len(data) == 1:
        return data[0]
    rank = (len(data) - 1) * q
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return data[low]
    weight = rank - low
    return data[low] * (1.0 - weight) + data[high] * weight


def distribution(values: Iterable[float]) -> dict[str, float | int | None]:
    data = list(float(value) for value in values)
    return {
        "count": len(data),
        "min": min(data) if data else None,
        "p50": percentile(data, 0.50),
        "p95": percentile(data, 0.95),
        "p99": percentile(data, 0.99),
        "max": max(data) if data else None,
        "mean": statistics.fmean(data) if data else None,
    }


def security_qualification() -> dict[str, Any]:
    directory = SecurityDirectory()
    directory.put_membership(
        Membership(
            membership_id="m-a",
            user_id="user-a",
            org_id="org-a",
            workspace_id="ws-a",
            role=Role.EDITOR,
        )
    )
    directory.create_session(
        session_id="sess-a",
        user_id="user-a",
        org_id="org-a",
        workspace_id="ws-a",
        csrf_token="csrf-a",
    )
    context = directory.resolve_context("sess-a")
    authorizer = DenyByDefaultAuthorizer(directory)

    unauthorized_successes = 0
    for surface, action in (
        (AccessSurface.API, Action.API_READ),
        (AccessSurface.DATA, Action.DATA_READ),
        (AccessSurface.OBJECT, Action.OBJECT_READ),
        (AccessSurface.EVENT, Action.EVENT_CONNECT),
        (AccessSurface.TRACE, Action.TRACE_READ),
    ):
        try:
            authorizer.require(
                context,
                TenantResource(
                    surface=surface,
                    org_id="org-b",
                    workspace_id="ws-b",
                    resource_id=f"foreign-{surface.value}",
                    provenance_id="sha256:foreign",
                ),
                action,
            )
        except TenantIsolationError:
            continue
        unauthorized_successes += 1

    quarantine_cases = {
        "invalid_signature": b"not a pdf",
        "encrypted": b"%PDF-1.7\n/Encrypt true\n%%EOF\n",
        "active_content": b"%PDF-1.7\n/JavaScript\n%%EOF\n",
        "embedded_file": b"%PDF-1.7\n/EmbeddedFile\n%%EOF\n",
        "malformed": b"%PDF-1.7\ntruncated",
    }
    quarantine_bypasses = 0
    quarantine_routes: dict[str, str] = {}
    for name, payload in quarantine_cases.items():
        record = preflight_pdf_upload(payload)
        quarantine_routes[name] = record.route.value
        if record.route is not UploadRoute.QUARANTINED:
            quarantine_bypasses += 1

    canary = "SECRET_CANARY_W006_T013_A01"
    event = sanitize_event_payload(
        {
            "status": "running",
            "authorization": f"Bearer {canary}",
            "nested": {"cookie": f"session={canary}", "safe": f"prefix-{canary}"},
        },
        secret_values=(canary,),
    )
    telemetry = sanitize_telemetry_attributes(
        {
            "trace_id": "trace-t013",
            "status": f"error:{canary}",
            "authorization": f"Bearer {canary}",
            "unexpected_raw_payload": {"secret": canary},
        },
        secret_values=(canary,),
    )
    serialized = json.dumps({"event": event, "telemetry": telemetry}, sort_keys=True)
    secret_leaks = int(
        canary in serialized
        or "authorization" in serialized.lower()
        or "cookie" in serialized.lower()
    )

    start_params = inspect.signature(ReferenceVerticalSlice.start).parameters
    filesystem_path_inputs = sum(name in start_params for name in ("path", "file_path", "filesystem_path"))

    metrics = {
        "cross_tenant_unauthorized_success": unauthorized_successes,
        "secret_credential_canary_leakage": secret_leaks,
        "private_quarantine_bypass": quarantine_bypasses,
        "arbitrary_untrusted_server_filesystem_path_input": filesystem_path_inputs,
        "quarantine_routes": quarantine_routes,
    }
    passed = all(
        metrics[key] == 0
        for key in (
            "cross_tenant_unauthorized_success",
            "secret_credential_canary_leakage",
            "private_quarantine_bypass",
            "arbitrary_untrusted_server_filesystem_path_input",
        )
    )
    return {"status": "PASS" if passed else "FAIL", "metrics": metrics}


def identity(index: int) -> SliceIdentity:
    return SliceIdentity(
        org_id=f"org-load-{index}",
        workspace_id=f"ws-load-{index}",
        user_id=f"user-load-{index}",
        session_id=f"session-load-{index}",
        csrf_token=f"csrf-load-{index}",
    )


async def reference_restart_and_restore(root: Path) -> dict[str, Any]:
    parser = LockedFixturePdfAdapter()
    live_root = root / "restart-live"
    first = ReferenceVerticalSlice(live_root, parser=parser)
    paused = await first.start(
        run_id="run-t013-restart",
        identity=identity(10001),
        raw_pdf=VALID_PDF,
        artifact_label="t013-reference.pdf",
        source_group_key="t013-reference",
        pause_after="planned",
    )
    restarted = ReferenceVerticalSlice(live_root, parser=LockedFixturePdfAdapter())
    complete = await restarted.resume(paused.run_id)
    first_events = restarted.publish_authoritative_events(complete)
    second_events = restarted.publish_authoritative_events(complete)

    backup_root = restarted.backup_to(root / "restart-backup")
    restored = ReferenceVerticalSlice.restore_from_backup(
        backup_root,
        root / "restart-restored",
        parser=LockedFixturePdfAdapter(),
    )
    restored_state = await restored.resume(complete.run_id)
    restored_events = restored.event_store.replay_events(
        org_id=str(complete.source["org_id"]),
        workspace_id=str(complete.source["workspace_id"]),
        run_id=complete.run_id,
    )

    job_ids = list(complete.jobs)
    accepted_ids = list(complete.joined_outputs)
    metrics = {
        "planned_branch_count": len(job_ids),
        "accepted_branch_count": len(accepted_ids),
        "unique_planned_branch_count": len(set(job_ids)),
        "unique_accepted_branch_count": len(set(accepted_ids)),
        "accepted_branch_loss": len(set(job_ids) - set(accepted_ids)),
        "accepted_branch_duplication": len(accepted_ids) - len(set(accepted_ids)),
        "required_provenance_missing": sum(
            not output.get("source_hash") or not output.get("source_id") or not output.get("attempt_id")
            for output in complete.joined_outputs.values()
        ),
        "authoritative_event_count": len(first_events),
        "duplicate_authoritative_event_on_republish": int(first_events != second_events),
        "restart_resume_pass": int(complete.phase.value == "complete" and len(accepted_ids) == 9),
        "backup_restore_pass": int(
            restored_state.phase.value == "complete"
            and restored_events == first_events
            and sum(restored.event_store.audit_invariants().values()) == 0
        ),
    }
    passed = (
        metrics["planned_branch_count"] == 9
        and metrics["accepted_branch_count"] == 9
        and metrics["unique_planned_branch_count"] == 9
        and metrics["unique_accepted_branch_count"] == 9
        and metrics["accepted_branch_loss"] == 0
        and metrics["accepted_branch_duplication"] == 0
        and metrics["required_provenance_missing"] == 0
        and metrics["duplicate_authoritative_event_on_republish"] == 0
        and metrics["restart_resume_pass"] == 1
        and metrics["backup_restore_pass"] == 1
    )
    return {"status": "PASS" if passed else "FAIL", "metrics": metrics}


async def run_one_reference(root: Path, index: int, semaphore: asyncio.Semaphore, queued_at: float) -> dict[str, Any]:
    async with semaphore:
        started = time.perf_counter()
        queue_seconds = started - queued_at
        parser = LockedFixturePdfAdapter()
        slice_ = ReferenceVerticalSlice(root / f"run-{index}", parser=parser)
        try:
            state = await slice_.start(
                run_id=f"run-load-{index}",
                identity=identity(index),
                raw_pdf=VALID_PDF,
                artifact_label="t013-load.pdf",
                source_group_key="t013-load",
            )
            events = slice_.publish_authoritative_events(state)
            accepted = len(state.joined_outputs)
            event_count = len(events)
            invariant_violations = sum(slice_.event_store.audit_invariants().values())
            error = None
        except Exception as exc:  # pragma: no cover - evidence path
            accepted = 0
            event_count = 0
            invariant_violations = -1
            error = f"{type(exc).__name__}: {exc}"
        ended = time.perf_counter()
        return {
            "index": index,
            "queue_seconds": queue_seconds,
            "service_seconds": ended - started,
            "total_seconds": ended - queued_at,
            "accepted_branches": accepted,
            "authoritative_events": event_count,
            "invariant_violations": invariant_violations,
            "error": error,
        }


def directory_bytes(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


async def load_phase(
    root: Path,
    *,
    phase: str,
    requests: int,
    concurrency: int,
    inter_arrival_seconds: float = 0.0,
    index_offset: int = 0,
) -> dict[str, Any]:
    phase_root = root / phase
    phase_root.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(concurrency)
    usage_before = resource.getrusage(resource.RUSAGE_SELF)
    wall_start = time.perf_counter()
    tasks: list[asyncio.Task[dict[str, Any]]] = []
    for local_index in range(requests):
        queued_at = time.perf_counter()
        tasks.append(
            asyncio.create_task(
                run_one_reference(
                    phase_root,
                    index_offset + local_index,
                    semaphore,
                    queued_at,
                )
            )
        )
        if inter_arrival_seconds > 0 and local_index + 1 < requests:
            await asyncio.sleep(inter_arrival_seconds)
    rows = await asyncio.gather(*tasks)
    wall_seconds = time.perf_counter() - wall_start
    usage_after = resource.getrusage(resource.RUSAGE_SELF)
    errors = [row for row in rows if row["error"]]
    accepted_failures = [
        row
        for row in rows
        if not row["error"]
        and (
            row["accepted_branches"] != 9
            or row["authoritative_events"] != 11
            or row["invariant_violations"] != 0
        )
    ]
    completed = requests - len(errors) - len(accepted_failures)
    return {
        "phase": phase,
        "scope": "REFERENCE_LOCAL_GITHUB_RUNNER_NON_PRODUCTION",
        "requests": requests,
        "concurrency": concurrency,
        "inter_arrival_seconds": inter_arrival_seconds,
        "wall_seconds": wall_seconds,
        "throughput_runs_per_second": completed / wall_seconds if wall_seconds else None,
        "error_count": len(errors),
        "qualification_failure_count": len(accepted_failures),
        "error_rate": (len(errors) + len(accepted_failures)) / requests if requests else 0.0,
        "latency_seconds": distribution(row["total_seconds"] for row in rows),
        "service_seconds": distribution(row["service_seconds"] for row in rows),
        "queue_seconds": distribution(row["queue_seconds"] for row in rows),
        "resource": {
            "process_user_cpu_seconds_delta": usage_after.ru_utime - usage_before.ru_utime,
            "process_system_cpu_seconds_delta": usage_after.ru_stime - usage_before.ru_stime,
            "process_max_rss_kib_observed": usage_after.ru_maxrss,
            "phase_artifact_bytes": directory_bytes(phase_root),
        },
        "cost": {
            "status": "NOT_EXPOSED_BY_REFERENCE_PATH",
            "value": None,
            "unit": None,
        },
        "rows": rows,
    }


def saturation_observation(ladder: list[dict[str, Any]]) -> dict[str, Any]:
    if not ladder:
        return {"status": "NOT_RUN", "interval": None}
    prior = ladder[0]
    for current in ladder[1:]:
        prior_tp = float(prior["throughput_runs_per_second"] or 0.0)
        current_tp = float(current["throughput_runs_per_second"] or 0.0)
        prior_p95 = float(prior["latency_seconds"]["p95"] or 0.0)
        current_p95 = float(current["latency_seconds"]["p95"] or 0.0)
        throughput_regressed = prior_tp > 0 and current_tp < prior_tp * 0.95
        latency_inflated = prior_p95 > 0 and current_p95 > prior_p95 * 1.25
        if current["error_rate"] > 0 or (throughput_regressed and latency_inflated):
            return {
                "status": "DIAGNOSTIC_SIGNAL_OBSERVED",
                "interval_concurrent_runs": [prior["concurrency"], current["concurrency"]],
                "criterion": "error_rate>0 OR (throughput regression >5% AND p95 latency inflation >25% versus prior rung)",
                "production_capacity_claim": "NOT_AUTHORIZED",
            }
        prior = current
    return {
        "status": "NOT_OBSERVED_WITHIN_TESTED_INTERVAL",
        "interval_concurrent_runs": [ladder[0]["concurrency"], ladder[-1]["concurrency"]],
        "criterion": "error_rate>0 OR (throughput regression >5% AND p95 latency inflation >25% versus prior rung)",
        "production_capacity_claim": "NOT_AUTHORIZED",
    }


async def capacity_qualification(root: Path) -> dict[str, Any]:
    ladder: list[dict[str, Any]] = []
    offset = 20000
    for concurrency in (1, 2, 4, 8, 16):
        requests = max(8, concurrency * 2)
        ladder.append(
            await load_phase(
                root,
                phase=f"concurrency-{concurrency}",
                requests=requests,
                concurrency=concurrency,
                index_offset=offset,
            )
        )
        offset += requests

    arrival: list[dict[str, Any]] = []
    for step, inter_arrival in enumerate((0.050, 0.020, 0.005, 0.0), start=1):
        arrival.append(
            await load_phase(
                root,
                phase=f"arrival-step-{step}",
                requests=8,
                concurrency=8,
                inter_arrival_seconds=inter_arrival,
                index_offset=offset,
            )
        )
        offset += 8

    burst = await load_phase(
        root,
        phase="burst-16",
        requests=16,
        concurrency=16,
        index_offset=offset,
    )
    offset += 16
    soak = await load_phase(
        root,
        phase="short-soak-32-at-4",
        requests=32,
        concurrency=4,
        index_offset=offset,
    )

    all_phases = ladder + arrival + [burst, soak]
    zero_tolerance_failures = sum(
        phase["error_count"] + phase["qualification_failure_count"] for phase in all_phases
    )
    return {
        "status": "PASS" if zero_tolerance_failures == 0 else "FAIL",
        "scope": "REFERENCE_LOCAL_GITHUB_RUNNER_NON_PRODUCTION",
        "concurrency_ladder": ladder,
        "arrival_staircase": arrival,
        "burst": burst,
        "short_soak": soak,
        "saturation": saturation_observation(ladder),
        "zero_tolerance_reference_run_failures": zero_tolerance_failures,
        "supported_user_count": "NOT_CLAIMED",
        "production_slo": "NOT_CLAIMED",
        "production_rto": "NOT_CLAIMED",
        "production_rpo": "NOT_CLAIMED",
        "production_topology_capacity_evidence": "MISSING",
    }


async def main_async(output: Path) -> int:
    with tempfile.TemporaryDirectory(prefix="w006-t013-") as tmp:
        root = Path(tmp)
        security = security_qualification()
        restart_restore = await reference_restart_and_restore(root / "recovery")
        capacity = await capacity_qualification(root / "capacity")
        hard_failures = sum(
            item["status"] != "PASS" for item in (security, restart_restore, capacity)
        )
        payload = {
            "artifact": "W006-T013-A01 security reliability capacity recovery qualification",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task_id": "W006-T013",
            "attempt_id": "A01",
            "scope": "accepted same-product reference path; not a representative deployed production topology",
            "security": security,
            "restart_resume_backup_restore": restart_restore,
            "capacity": capacity,
            "deployment_migration_rollback": {
                "status": "MISSING_PRODUCTION_EVIDENCE",
                "reason": "production runtime/database/deployment topology remain evidence-gated and unlocked; no representative deployed migration target exists in this task environment",
                "fake_pass": False,
            },
            "production_claims": {
                "production_ready": "NOT_AUTHORIZED",
                "supported_user_count": "NOT_CLAIMED",
                "slo": "NOT_CLAIMED",
                "rto": "NOT_CLAIMED",
                "rpo": "NOT_CLAIMED",
            },
            "overall_status": "PASS_REFERENCE_SCOPE" if hard_failures == 0 else "FAIL",
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if hard_failures == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return asyncio.run(main_async(args.output))


if __name__ == "__main__":
    raise SystemExit(main())
