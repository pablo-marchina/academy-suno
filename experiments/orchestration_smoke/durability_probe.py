from __future__ import annotations

import asyncio
import json
import multiprocessing as mp
import statistics
import tempfile
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
from time import perf_counter
from typing import Any

from suno_content.orchestration import (
    AsyncGraphOrchestrator,
    EvaluationAction,
    JobSpec,
    QualityDecision,
    RunPhase,
)
from suno_content.runstore import SQLiteRunStore


AUDIENCES = ("beginner", "intermediate", "advanced")
FORMATS = ("article", "carousel", "short_video")
QUALITY_REPAIR_JOB = "beginner:carousel"
TRANSPORT_RETRY_JOB = "advanced:short_video"


class WorkloadHarness:
    """Deterministic Academy Suno 3x3 workload with separated retry classes."""

    def __init__(self) -> None:
        self.generate_calls: Counter[str] = Counter()
        self.evaluate_calls: Counter[str] = Counter()
        self.repair_calls: Counter[str] = Counter()

    def planner(self, source: dict[str, Any]) -> tuple[JobSpec, ...]:
        return tuple(
            JobSpec(f"{audience}:{fmt}", {"audience": audience, "format": fmt})
            for audience, fmt in product(AUDIENCES, FORMATS)
        )

    async def generator(self, job: JobSpec, source: dict[str, Any]) -> dict[str, Any]:
        self.generate_calls[job.job_id] += 1
        await asyncio.sleep(0)
        if job.job_id == TRANSPORT_RETRY_JOB and self.generate_calls[job.job_id] == 1:
            raise TimeoutError("synthetic provider timeout")
        return {"job_id": job.job_id, "value": f"draft::{job.job_id}"}

    def evaluator(self, job: JobSpec, output: dict[str, Any]) -> QualityDecision:
        self.evaluate_calls[job.job_id] += 1
        if job.job_id == QUALITY_REPAIR_JOB and str(output["value"]).startswith("draft::"):
            return QualityDecision(EvaluationAction.REPAIR, ("synthetic_quality_gap",))
        return QualityDecision(EvaluationAction.PASS)

    async def repairer(
        self,
        job: JobSpec,
        output: dict[str, Any],
        decision: QualityDecision,
        repair_attempt: int,
    ) -> dict[str, Any]:
        self.repair_calls[job.job_id] += 1
        await asyncio.sleep(0)
        return {"job_id": job.job_id, "value": f"repaired::{job.job_id}"}

    def aggregator(self, outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
        return {"job_ids": sorted(outputs), "count": len(outputs)}


def _engine(path: Path, harness: WorkloadHarness) -> AsyncGraphOrchestrator:
    return AsyncGraphOrchestrator(
        store=SQLiteRunStore(path),
        planner=harness.planner,
        generator=harness.generator,
        evaluator=harness.evaluator,
        repairer=harness.repairer,
        aggregator=harness.aggregator,
        transport_retry_limit=2,
        max_quality_repairs=2,
    )


async def _run_once(path: Path, run_id: str) -> dict[str, Any]:
    harness = WorkloadHarness()
    engine = _engine(path, harness)
    started = perf_counter()
    final = await engine.start(run_id=run_id, source={"source_id": "w005-t003"})
    elapsed_ms = (perf_counter() - started) * 1000.0
    history = engine.store.history(run_id)

    if final.phase is not RunPhase.COMPLETE:
        raise AssertionError(f"run did not complete: {final.phase.value}")
    if len(final.jobs) != 9 or len(final.joined_outputs) != 9:
        raise AssertionError("9/9 fan-out/join invariant failed")
    if final.aggregate is None or int(final.aggregate["count"]) != 9:
        raise AssertionError("aggregate count invariant failed")
    if harness.repair_calls != Counter({QUALITY_REPAIR_JOB: 1}):
        raise AssertionError(f"quality repair locality failed: {harness.repair_calls}")
    if harness.generate_calls[TRANSPORT_RETRY_JOB] != 2:
        raise AssertionError("transport retry was not isolated to the synthetic transport failure")

    return {
        "runtime_ms": round(elapsed_ms, 3),
        "history_snapshots": len(history),
        "joined_outputs": len(final.joined_outputs),
        "quality_repairs": sum(harness.repair_calls.values()),
        "transport_retries": sum(
            branch.transport_retries.get("generate", 0) + branch.transport_retries.get("repair", 0)
            for branch in final.jobs.values()
        ),
    }


async def _repeat_runs(root: Path, repetitions: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(repetitions):
        rows.append(await _run_once(root / f"run-{index}.sqlite3", f"run-{index}"))
    return rows


async def _resume_probe(path: Path) -> dict[str, Any]:
    harness = WorkloadHarness()
    first = _engine(path, harness)
    paused = await first.start(
        run_id="resume-probe",
        source={"source_id": "w005-t003"},
        pause_after="branches",
    )
    generate_before = dict(harness.generate_calls)
    repair_before = dict(harness.repair_calls)
    snapshots_before = len(first.store.history("resume-probe"))

    second = _engine(path, harness)
    final = await second.resume("resume-probe")
    snapshots_after = len(second.store.history("resume-probe"))

    return {
        "paused_phase": paused.phase.value,
        "final_phase": final.phase.value,
        "joined_outputs": len(final.joined_outputs),
        "generate_calls_unchanged": generate_before == dict(harness.generate_calls),
        "repair_calls_unchanged": repair_before == dict(harness.repair_calls),
        "snapshots_before_resume": snapshots_before,
        "snapshots_after_resume": snapshots_after,
        "pass": (
            final.phase is RunPhase.COMPLETE
            and len(final.joined_outputs) == 9
            and generate_before == dict(harness.generate_calls)
            and repair_before == dict(harness.repair_calls)
        ),
    }


def _child_run_to_branches(db_path: str) -> None:
    async def work() -> None:
        harness = WorkloadHarness()
        engine = _engine(Path(db_path), harness)
        paused = await engine.start(
            run_id="process-restart-probe",
            source={"source_id": "w005-t003"},
            pause_after="branches",
        )
        if paused.phase is not RunPhase.BRANCHES_COMPLETE:
            raise AssertionError(paused.phase.value)

    asyncio.run(work())


async def _process_restart_probe(path: Path) -> dict[str, Any]:
    context = mp.get_context("spawn")
    process = context.Process(target=_child_run_to_branches, args=(str(path),))
    process.start()
    process.join(timeout=30)
    if process.is_alive():
        process.kill()
        process.join(timeout=5)
        raise RuntimeError("restart probe child timed out")
    if process.exitcode != 0:
        raise RuntimeError(f"restart probe child exited {process.exitcode}")

    recovery_harness = WorkloadHarness()
    recovery_engine = _engine(path, recovery_harness)
    state_before = recovery_engine.store.load("process-restart-probe")
    final = await recovery_engine.resume("process-restart-probe")
    history = recovery_engine.store.history("process-restart-probe")

    return {
        "child_exitcode": process.exitcode,
        "persisted_phase_before_resume": state_before["phase"],
        "final_phase": final.phase.value,
        "joined_outputs": len(final.joined_outputs),
        "recovery_process_generate_calls": sum(recovery_harness.generate_calls.values()),
        "recovery_process_repair_calls": sum(recovery_harness.repair_calls.values()),
        "history_snapshots": len(history),
        "pass": (
            state_before["phase"] == RunPhase.BRANCHES_COMPLETE.value
            and final.phase is RunPhase.COMPLETE
            and len(final.joined_outputs) == 9
            and sum(recovery_harness.generate_calls.values()) == 0
            and sum(recovery_harness.repair_calls.values()) == 0
        ),
    }


def _distinct_run_concurrency_probe(path: Path, *, workers: int = 8, checkpoints: int = 20) -> dict[str, Any]:
    start = threading.Barrier(workers)

    def writer(index: int) -> tuple[str, int]:
        store = SQLiteRunStore(path)
        run_id = f"concurrent-{index}"
        state: dict[str, Any] = {"run_id": run_id, "writer": index, "step": 0}
        start.wait(timeout=10)
        store.create(state, reason="created")
        for step in range(1, checkpoints + 1):
            state["step"] = step
            store.checkpoint(state, reason=f"step:{step}")
        return run_id, len(store.history(run_id))

    started = perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(writer, range(workers)))
    elapsed_ms = (perf_counter() - started) * 1000.0

    return {
        "workers": workers,
        "checkpoints_per_worker": checkpoints,
        "elapsed_ms": round(elapsed_ms, 3),
        "expected_history_per_run": checkpoints + 1,
        "observed_history_lengths": {run_id: length for run_id, length in results},
        "all_writes_preserved": all(length == checkpoints + 1 for _, length in results),
        "scope": "same-host, same SQLite file, independent run_ids; not a multi-host/shared-filesystem proof",
    }


def _same_run_stale_write_probe(path: Path) -> dict[str, Any]:
    creator = SQLiteRunStore(path)
    creator.create({"run_id": "shared-run", "replica_marks": []}, reason="created")
    both_loaded = threading.Barrier(2)

    def replica(mark: str) -> int:
        store = SQLiteRunStore(path)
        state = store.load("shared-run")
        marks = list(state.get("replica_marks", []))
        marks.append(mark)
        state["replica_marks"] = marks
        both_loaded.wait(timeout=10)
        snapshot = store.checkpoint(state, reason=f"replica:{mark}")
        return snapshot.sequence

    with ThreadPoolExecutor(max_workers=2) as pool:
        sequences = sorted(pool.map(replica, ("A", "B")))

    final_store = SQLiteRunStore(path)
    final = final_store.load("shared-run")
    history = final_store.history("shared-run")
    final_marks = list(final.get("replica_marks", []))

    return {
        "checkpoint_sequences": sequences,
        "history_snapshots": len(history),
        "final_replica_marks": final_marks,
        "both_checkpoint_calls_succeeded": sequences == [2, 3],
        "lost_update_observed": len(final_marks) == 1,
        "interpretation": (
            "SQLite serialization protects sequence allocation, but SQLiteRunStore has no optimistic "
            "version/CAS or per-run lease; two replicas can checkpoint stale whole-run state and the last "
            "writer wins. This is a production multi-replica safety gap, not evidence that SQLite itself "
            "cannot handle concurrent writers."
        ),
    }


def _percentile(values: list[float], quantile: float) -> float:
    if not values:
        raise ValueError("values must not be empty")
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def run_bakeoff(*, repetitions: int = 15) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="w005-t003-") as tmp:
        root = Path(tmp)
        repetitions_rows = asyncio.run(_repeat_runs(root / "repetitions", repetitions))
        latencies = [float(row["runtime_ms"]) for row in repetitions_rows]
        snapshots = [int(row["history_snapshots"]) for row in repetitions_rows]

        resume = asyncio.run(_resume_probe(root / "resume.sqlite3"))
        restart = asyncio.run(_process_restart_probe(root / "restart.sqlite3"))
        independent = _distinct_run_concurrency_probe(root / "concurrent.sqlite3")
        stale_write = _same_run_stale_write_probe(root / "stale-write.sqlite3")

        return {
            "schema": "w005-t003.orchestration-bakeoff.v1",
            "baseline": "AsyncGraphOrchestrator + SQLiteRunStore",
            "repetitions": repetitions,
            "hard_invariants": {
                "fanout_join": "9/9",
                "branch_loss_or_duplication": "none observed",
                "transport_quality_retry_separation": "PASS",
                "hard_gate_relaxation": "none",
            },
            "latency_ms": {
                "min": round(min(latencies), 3),
                "p50": round(statistics.median(latencies), 3),
                "p95": round(_percentile(latencies, 0.95), 3),
                "max": round(max(latencies), 3),
            },
            "state_writes": {
                "history_snapshots_min": min(snapshots),
                "history_snapshots_median": statistics.median(snapshots),
                "history_snapshots_max": max(snapshots),
            },
            "checkpoint_resume": resume,
            "process_restart": restart,
            "shared_file_independent_runs": independent,
            "same_run_stale_write": stale_write,
            "raw_repetition_rows": repetitions_rows,
            "limitations": [
                "Synthetic callbacks isolate orchestration/storage overhead from model/provider latency.",
                "Concurrent-writer probes use one host and one local SQLite file; they do not model network filesystems.",
                "The same-run stale-write probe models two replicas with separate connections but not two hosts.",
                "LangGraph, DBOS and Temporal package runtimes are not installed by the pinned foundation CI; challenger runtime latency is therefore not inferred from this baseline probe.",
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_bakeoff(), ensure_ascii=False, indent=2, sort_keys=True))
