from __future__ import annotations

import asyncio
import json
import tempfile
from collections import Counter
from itertools import product
from pathlib import Path

from suno_content.orchestration import (
    AsyncGraphOrchestrator,
    EvaluationAction,
    JobSpec,
    QualityDecision,
)
from suno_content.runstore import SQLiteRunStore


AUDIENCES = ("beginner", "intermediate", "advanced")
FORMATS = ("article", "carousel", "short_video")
QUALITY_FAIL_JOB = "beginner:carousel"
TRANSPORT_RETRY_JOB = "advanced:short_video"


async def main() -> None:
    calls: Counter[str] = Counter()

    def planner(source: dict[str, object]) -> tuple[JobSpec, ...]:
        return tuple(
            JobSpec(f"{audience}:{fmt}", {"audience": audience, "format": fmt})
            for audience, fmt in product(AUDIENCES, FORMATS)
        )

    async def generator(job: JobSpec, source: dict[str, object]) -> dict[str, object]:
        calls[f"generate:{job.job_id}"] += 1
        if job.job_id == TRANSPORT_RETRY_JOB and calls[f"generate:{job.job_id}"] == 1:
            raise TimeoutError("synthetic transport failure")
        return {"job_id": job.job_id, "value": f"draft::{job.job_id}"}

    def evaluator(job: JobSpec, output: dict[str, object]) -> QualityDecision:
        if job.job_id == QUALITY_FAIL_JOB and str(output["value"]).startswith("draft::"):
            return QualityDecision(EvaluationAction.REPAIR, ("synthetic_quality_gap",))
        return QualityDecision(EvaluationAction.PASS)

    async def repairer(
        job: JobSpec,
        output: dict[str, object],
        decision: QualityDecision,
        repair_attempt: int,
    ) -> dict[str, object]:
        calls[f"repair:{job.job_id}"] += 1
        return {"job_id": job.job_id, "value": f"repaired::{job.job_id}"}

    def aggregator(outputs: dict[str, dict[str, object]]) -> dict[str, object]:
        return {"count": len(outputs), "job_ids": sorted(outputs)}

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "runtime.sqlite3"
        first = AsyncGraphOrchestrator(
            store=SQLiteRunStore(db_path),
            planner=planner,
            generator=generator,
            evaluator=evaluator,
            repairer=repairer,
            aggregator=aggregator,
        )
        paused = await first.start(
            run_id="runtime-proof",
            source={"source_id": "synthetic-source"},
            pause_after="branches",
        )
        second = AsyncGraphOrchestrator(
            store=SQLiteRunStore(db_path),
            planner=planner,
            generator=generator,
            evaluator=evaluator,
            repairer=repairer,
            aggregator=aggregator,
        )
        final = await second.resume("runtime-proof")
        history = second.store.history("runtime-proof")
        print(
            json.dumps(
                {
                    "paused_phase": paused.phase.value,
                    "final_phase": final.phase.value,
                    "joined_outputs": len(final.joined_outputs),
                    "quality_repairs": {
                        job_id: branch.quality_repairs
                        for job_id, branch in final.jobs.items()
                        if branch.quality_repairs
                    },
                    "transport_retries": {
                        job_id: branch.transport_retries
                        for job_id, branch in final.jobs.items()
                        if branch.transport_retries
                    },
                    "history_snapshots": len(history),
                    "graph": second.describe_graph(),
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
