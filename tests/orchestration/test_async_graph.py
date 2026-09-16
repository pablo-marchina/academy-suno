from __future__ import annotations

import tempfile
import unittest
from collections import Counter
from itertools import product
from pathlib import Path

from suno_content.orchestration import (
    AsyncGraphOrchestrator,
    BranchPhase,
    EvaluationAction,
    JobSpec,
    OrchestrationInvariantError,
    QualityDecision,
    RunPhase,
)
from suno_content.runstore import SQLiteRunStore


AUDIENCES = ("beginner", "intermediate", "advanced")
FORMATS = ("article", "carousel", "short_video")
QUALITY_FAIL_JOB = "beginner:carousel"
TRANSPORT_RETRY_JOB = "advanced:short_video"


class Harness:
    def __init__(self) -> None:
        self.generate_calls: Counter[str] = Counter()
        self.evaluate_calls: Counter[str] = Counter()
        self.repair_calls: Counter[str] = Counter()

    def planner(self, source: dict[str, object]) -> tuple[JobSpec, ...]:
        self.source = source
        return tuple(
            JobSpec(f"{audience}:{fmt}", {"audience": audience, "format": fmt})
            for audience, fmt in product(AUDIENCES, FORMATS)
        )

    async def generator(self, job: JobSpec, source: dict[str, object]) -> dict[str, object]:
        self.generate_calls[job.job_id] += 1
        if job.job_id == TRANSPORT_RETRY_JOB and self.generate_calls[job.job_id] == 1:
            raise TimeoutError("synthetic provider timeout")
        return {"job_id": job.job_id, "value": f"draft::{job.job_id}"}

    def evaluator(self, job: JobSpec, output: dict[str, object]) -> QualityDecision:
        self.evaluate_calls[job.job_id] += 1
        if job.job_id == QUALITY_FAIL_JOB and str(output["value"]).startswith("draft::"):
            return QualityDecision(EvaluationAction.REPAIR, ("synthetic_quality_gap",))
        return QualityDecision(EvaluationAction.PASS)

    async def repairer(
        self,
        job: JobSpec,
        output: dict[str, object],
        decision: QualityDecision,
        repair_attempt: int,
    ) -> dict[str, object]:
        self.repair_calls[job.job_id] += 1
        return {"job_id": job.job_id, "value": f"repaired::{job.job_id}"}

    def aggregator(self, outputs: dict[str, dict[str, object]]) -> dict[str, object]:
        return {"job_ids": sorted(outputs), "count": len(outputs)}


class AsyncGraphOrchestratorTests(unittest.IsolatedAsyncioTestCase):
    def _engine(self, path: Path, harness: Harness) -> AsyncGraphOrchestrator:
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

    async def test_explicit_graph_lossless_9_way_join_and_retry_repair_separation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "runs.sqlite3"
            harness = Harness()
            engine = self._engine(path, harness)

            graph = engine.describe_graph()
            node_ids = {node["node_id"] for node in graph["nodes"]}
            self.assertTrue({"source", "plan", "branch.generate", "branch.evaluate", "branch.repair", "join", "aggregate", "complete"} <= node_ids)
            self.assertIn(
                {"source": "branch.evaluate", "target": "branch.repair", "condition": "evaluation=repair"},
                graph["edges"],
            )

            final = await engine.start(run_id="run-e2e", source={"source_id": "source-1"})

            self.assertEqual(RunPhase.COMPLETE, final.phase)
            self.assertEqual(9, len(final.jobs))
            self.assertEqual(9, len(final.joined_outputs))
            self.assertEqual(9, final.aggregate["count"])
            self.assertTrue(all(branch.phase is BranchPhase.ACCEPTED for branch in final.jobs.values()))
            self.assertEqual(1, harness.repair_calls[QUALITY_FAIL_JOB])
            self.assertEqual({QUALITY_FAIL_JOB}, set(harness.repair_calls))
            self.assertEqual(2, harness.evaluate_calls[QUALITY_FAIL_JOB])
            self.assertTrue(all(harness.generate_calls[job_id] == (2 if job_id == TRANSPORT_RETRY_JOB else 1) for job_id in final.jobs))

            retry_events = final.jobs[TRANSPORT_RETRY_JOB].events
            repair_events = final.jobs[QUALITY_FAIL_JOB].events
            self.assertEqual(1, sum(event["kind"] == "transport_retry" for event in retry_events))
            self.assertEqual(0, sum(event["kind"] == "quality_repair" for event in retry_events))
            self.assertEqual(1, sum(event["kind"] == "quality_repair" for event in repair_events))
            self.assertEqual(0, sum(event["kind"] == "transport_retry" for event in repair_events))

    async def test_persistent_resume_skips_already_accepted_branches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "runs.sqlite3"
            harness = Harness()
            first_engine = self._engine(path, harness)
            paused = await first_engine.start(
                run_id="run-resume",
                source={"source_id": "source-1"},
                pause_after="branches",
            )
            self.assertEqual(RunPhase.BRANCHES_COMPLETE, paused.phase)
            before_generate = harness.generate_calls.copy()
            before_repair = harness.repair_calls.copy()

            second_engine = self._engine(path, harness)
            final = await second_engine.resume("run-resume")

            self.assertEqual(RunPhase.COMPLETE, final.phase)
            self.assertEqual(before_generate, harness.generate_calls)
            self.assertEqual(before_repair, harness.repair_calls)
            history = second_engine.store.history("run-resume")
            self.assertGreater(len(history), 10)
            self.assertEqual("run_complete", history[-1].reason)
            self.assertEqual("complete", history[-1].state["phase"])

    async def test_duplicate_job_ids_fail_before_dict_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness()

            def duplicate_planner(source: dict[str, object]) -> tuple[JobSpec, ...]:
                jobs = list(harness.planner(source))
                jobs[-1] = JobSpec(jobs[0].job_id, {"duplicate": True})
                return tuple(jobs)

            engine = AsyncGraphOrchestrator(
                store=SQLiteRunStore(Path(tmp) / "runs.sqlite3"),
                planner=duplicate_planner,
                generator=harness.generator,
                evaluator=harness.evaluator,
                repairer=harness.repairer,
                aggregator=harness.aggregator,
            )
            with self.assertRaises(OrchestrationInvariantError):
                await engine.start(run_id="run-duplicate", source={"source_id": "source-1"})


if __name__ == "__main__":
    unittest.main()
