from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass

from suno_content.telemetry import (
    InMemoryTelemetrySink,
    OrchestrationTelemetryHooks,
    PricingTable,
    TelemetryRecorder,
    UsageObservation,
    summarize,
)


class DemoClock:
    def __init__(self) -> None:
        self.value = 0

    def __call__(self) -> int:
        self.value += 1_000_000
        return self.value


@dataclass
class Job:
    job_id: str


async def main() -> None:
    sink = InMemoryTelemetrySink()
    pricing = PricingTable(
        version="demo-pricing.v1",
        currency="USD",
        unit_prices={"input_tokens": "0.000002", "output_tokens": "0.000006"},
    )
    recorder = TelemetryRecorder(
        run_id="telemetry-demo",
        sink=sink,
        monotonic_ns=DemoClock(),
        wall_time=lambda: "2026-09-16T16:00:00+00:00",
        pricing=pricing,
    )
    hooks = OrchestrationTelemetryHooks(
        recorder,
        usage_extractors={
            "generate": lambda result: UsageObservation(
                {
                    "input_tokens": result["usage"]["input_tokens"],
                    "output_tokens": result["usage"]["output_tokens"],
                },
                complete=True,
                source="demo-adapter",
            )
        },
    )

    job = Job("advanced:short_video")
    calls = 0

    async def generate(_job: Job, _source: dict[str, object]):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise TimeoutError("simulated transport timeout")
        return {"text": "draft", "usage": {"input_tokens": 120, "output_tokens": 80}}

    wrapped_generate = hooks.generator(generate)
    try:
        await wrapped_generate(job, {})
    except TimeoutError:
        pass
    await wrapped_generate(job, {})

    wrapped_repair = hooks.repairer(
        lambda _job, output, _decision, attempt: {**output, "repaired": attempt}
    )
    await wrapped_repair(job, {"text": "draft"}, object(), 1)

    hooks.observe_state(
        {
            "run_id": "telemetry-demo",
            "phase": "review_required",
            "jobs": {
                "advanced:short_video": {
                    "phase": "review_required",
                    "error": None,
                    "quality_repairs": 1,
                    "transport_retries": {"generate": 1},
                },
                "beginner:carousel": {
                    "phase": "failed",
                    "error": "quality evaluation hard fail",
                    "quality_repairs": 0,
                    "transport_retries": {},
                },
            },
        }
    )

    print(json.dumps(summarize(sink.events), indent=2, sort_keys=True))


if __name__ == "__main__":
    asyncio.run(main())
