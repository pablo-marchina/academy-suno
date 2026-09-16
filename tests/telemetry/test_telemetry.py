from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from suno_content.telemetry import (
    InMemoryTelemetrySink,
    JsonlTelemetrySink,
    OrchestrationTelemetryHooks,
    PricingTable,
    TelemetryEventKind,
    TelemetryRecorder,
    UsageObservation,
    summarize,
)


class FakeClock:
    def __init__(self, values: list[int]) -> None:
        self.values = list(values)

    def __call__(self) -> int:
        if not self.values:
            raise AssertionError("fake clock exhausted")
        return self.values.pop(0)


@dataclass
class Job:
    job_id: str


class TelemetryTests(unittest.TestCase):
    def test_stage_latency_lineage_and_schema_are_reproducible(self) -> None:
        sink = InMemoryTelemetrySink()
        clock = FakeClock([100, 350])
        recorder = TelemetryRecorder(
            run_id="run-1",
            sink=sink,
            monotonic_ns=clock,
            wall_time=lambda: "2026-09-16T16:00:00+00:00",
        )

        result = asyncio.run(
            recorder.invoke(stage="generate", job_id="beginner:article", call=lambda: {"ok": True})
        )
        self.assertEqual({"ok": True}, result)
        self.assertEqual(2, len(sink.events))
        started, completed = sink.events
        self.assertEqual(TelemetryEventKind.STAGE_STARTED, started.kind)
        self.assertEqual(TelemetryEventKind.STAGE_COMPLETED, completed.kind)
        self.assertEqual(started.event_id, completed.parent_event_id)
        self.assertEqual(250, completed.duration_ns)
        self.assertEqual("telemetry.event.v1", completed.schema_version)

        summary = summarize(sink.events)
        self.assertEqual(250, summary["stage_latency"]["generate"]["p50_ns"])
        self.assertEqual(250, summary["stage_latency"]["generate"]["p95_ns"])

    def test_transport_retry_and_quality_repair_are_distinct(self) -> None:
        sink = InMemoryTelemetrySink()
        clock = FakeClock([10, 20, 21, 22, 30, 50, 60, 70, 100])
        recorder = TelemetryRecorder(
            run_id="run-2",
            sink=sink,
            monotonic_ns=clock,
            wall_time=lambda: "2026-09-16T16:00:00+00:00",
        )
        hooks = OrchestrationTelemetryHooks(recorder)
        job = Job("advanced:video")
        calls = {"generate": 0}

        async def generate(_job: Job, _source: dict[str, object]):
            calls["generate"] += 1
            if calls["generate"] == 1:
                raise TimeoutError("provider timeout")
            return {"draft": "ok"}

        wrapped_generate = hooks.generator(generate)
        with self.assertRaises(TimeoutError):
            asyncio.run(wrapped_generate(job, {}))
        self.assertEqual({"draft": "ok"}, asyncio.run(wrapped_generate(job, {})))

        async def repair(_job: Job, output, _decision, repair_attempt: int):
            return {**output, "repair_attempt": repair_attempt}

        wrapped_repair = hooks.repairer(repair)
        repaired = asyncio.run(wrapped_repair(job, {"draft": "bad"}, object(), 1))
        self.assertEqual(1, repaired["repair_attempt"])

        summary = summarize(sink.events)
        self.assertEqual(1, summary["transport_retries"]["total"])
        self.assertEqual(1, summary["quality_repairs"]["total"])
        kinds = [event.kind for event in sink.events]
        self.assertIn(TelemetryEventKind.TRANSPORT_RETRY, kinds)
        self.assertIn(TelemetryEventKind.QUALITY_REPAIR, kinds)

    def test_usage_and_cost_are_na_when_unobserved(self) -> None:
        sink = InMemoryTelemetrySink()
        recorder = TelemetryRecorder(
            run_id="run-3",
            sink=sink,
            monotonic_ns=FakeClock([100, 200]),
            wall_time=lambda: "2026-09-16T16:00:00+00:00",
        )
        asyncio.run(recorder.invoke(stage="aggregate", call=lambda: {"ok": True}))
        summary = summarize(sink.events)
        self.assertIsNone(summary["usage"])
        self.assertIsNone(summary["observed_cost"])
        self.assertIsNone(sink.events[-1].usage)
        self.assertIsNone(sink.events[-1].cost)

    def test_versioned_pricing_only_applies_to_complete_observed_usage(self) -> None:
        pricing = PricingTable(
            version="pricing-2026-09-16.v1",
            currency="USD",
            unit_prices={"input_tokens": "0.000002", "output_tokens": "0.000006"},
        )
        sink = InMemoryTelemetrySink()
        recorder = TelemetryRecorder(
            run_id="run-4",
            sink=sink,
            monotonic_ns=FakeClock([100, 150]),
            wall_time=lambda: "2026-09-16T16:00:00+00:00",
            pricing=pricing,
        )
        hooks = OrchestrationTelemetryHooks(
            recorder,
            usage_extractors={
                "generate": lambda result: UsageObservation(
                    {"input_tokens": result["input_tokens"], "output_tokens": result["output_tokens"]},
                    complete=True,
                    source="adapter-observed",
                )
            },
        )
        result = asyncio.run(
            hooks.generator(lambda _job, _source: {"input_tokens": 100, "output_tokens": 50})(
                Job("intermediate:article"), {}
            )
        )
        self.assertEqual(100, result["input_tokens"])
        completed = sink.events[-1]
        self.assertEqual("pricing-2026-09-16.v1", completed.cost.pricing_version)
        self.assertEqual(Decimal("0.000500"), completed.cost.amount)

        summary = summarize(sink.events)
        self.assertEqual("100", summary["usage"]["quantities"]["input_tokens"])
        self.assertEqual("0.000500", summary["observed_cost"][0]["amount"])

        partial = UsageObservation({"input_tokens": 100}, complete=False)
        self.assertIsNone(pricing.price(partial))
        missing_meter = UsageObservation({"uncatalogued_units": 1}, complete=True)
        self.assertIsNone(pricing.price(missing_meter))

    def test_hard_failures_and_review_states_remain_visible(self) -> None:
        sink = InMemoryTelemetrySink()
        recorder = TelemetryRecorder(
            run_id="run-5",
            sink=sink,
            monotonic_ns=FakeClock([1, 2, 3, 4]),
            wall_time=lambda: "2026-09-16T16:00:00+00:00",
        )
        recorder.observe_run_state(
            {
                "run_id": "run-5",
                "phase": "review_required",
                "jobs": {
                    "a": {
                        "phase": "failed",
                        "error": "quality evaluation hard fail",
                        "quality_repairs": 0,
                        "transport_retries": {},
                    },
                    "b": {
                        "phase": "review_required",
                        "error": None,
                        "quality_repairs": 1,
                        "transport_retries": {"generate": 1},
                    },
                    "c": {
                        "phase": "accepted",
                        "error": None,
                        "quality_repairs": 0,
                        "transport_retries": {},
                    },
                },
            }
        )
        summary = summarize(sink.events)
        self.assertEqual("review_required", summary["terminal"]["run_phase"])
        self.assertEqual(["a"], summary["terminal"]["failed_job_ids"])
        self.assertEqual(["b"], summary["terminal"]["review_required_job_ids"])
        self.assertEqual("quality evaluation hard fail", summary["terminal"]["branch_states"]["a"]["error"])

    def test_jsonl_sink_is_append_only_and_serializable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "telemetry.jsonl"
            sink = JsonlTelemetrySink(path)
            recorder = TelemetryRecorder(
                run_id="run-6",
                sink=sink,
                monotonic_ns=FakeClock([10, 20, 30, 50]),
                wall_time=lambda: "2026-09-16T16:00:00+00:00",
            )
            asyncio.run(recorder.invoke(stage="plan", call=lambda: [1]))
            asyncio.run(recorder.invoke(stage="aggregate", call=lambda: {"ok": True}))

            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(4, len(lines))
            decoded = [json.loads(line) for line in lines]
            self.assertEqual([1, 2, 3, 4], [item["sequence"] for item in decoded])
            self.assertTrue(all(item["schema_version"] == "telemetry.event.v1" for item in decoded))


if __name__ == "__main__":
    unittest.main()
