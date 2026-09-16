from __future__ import annotations

import inspect
import time
from collections.abc import Awaitable, Callable, Mapping
from datetime import datetime, timezone
from typing import Any, TypeVar

from .models import CostObservation, PricingTable, TelemetryEvent, TelemetryEventKind, UsageObservation
from .sinks import TelemetrySink


T = TypeVar("T")
MaybeAwaitable = T | Awaitable[T]
UsageExtractor = Callable[[Any], UsageObservation | None]


async def _resolve(value: MaybeAwaitable[T]) -> T:
    if inspect.isawaitable(value):
        return await value
    return value


class TelemetryRecorder:
    """Versioned event recorder with injectable clocks for deterministic tests."""

    def __init__(
        self,
        *,
        run_id: str,
        sink: TelemetrySink,
        monotonic_ns: Callable[[], int] = time.perf_counter_ns,
        wall_time: Callable[[], str] | None = None,
        pricing: PricingTable | None = None,
        transport_exceptions: tuple[type[BaseException], ...] = (TimeoutError, ConnectionError),
    ) -> None:
        if not run_id.strip():
            raise ValueError("run_id must not be empty")
        self.run_id = run_id
        self.sink = sink
        self.monotonic_ns = monotonic_ns
        self.wall_time = wall_time or (lambda: datetime.now(timezone.utc).isoformat())
        self.pricing = pricing
        self.transport_exceptions = transport_exceptions
        self._sequence = 0
        self._attempts: dict[tuple[str, str | None, int | None], int] = {}
        self._transport_failures: dict[tuple[str, str | None, int | None], str] = {}

    def _emit(
        self,
        kind: TelemetryEventKind,
        *,
        monotonic_ns: int,
        stage: str | None = None,
        job_id: str | None = None,
        operation_attempt: int | None = None,
        parent_event_id: str | None = None,
        duration_ns: int | None = None,
        usage: UsageObservation | None = None,
        cost: CostObservation | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> TelemetryEvent:
        self._sequence += 1
        event = TelemetryEvent(
            event_id=f"{self.run_id}:{self._sequence:06d}",
            sequence=self._sequence,
            run_id=self.run_id,
            kind=kind,
            observed_at=self.wall_time(),
            monotonic_ns=monotonic_ns,
            stage=stage,
            job_id=job_id,
            operation_attempt=operation_attempt,
            parent_event_id=parent_event_id,
            duration_ns=duration_ns,
            usage=usage,
            cost=cost,
            details=dict(details or {}),
        )
        self.sink.emit(event)
        return event

    async def invoke(
        self,
        *,
        stage: str,
        call: Callable[[], MaybeAwaitable[T]],
        job_id: str | None = None,
        quality_repair_attempt: int | None = None,
        usage_extractor: UsageExtractor | None = None,
    ) -> T:
        key = (stage, job_id, quality_repair_attempt)
        operation_attempt = self._attempts.get(key, 0) + 1
        self._attempts[key] = operation_attempt

        retry_parent = self._transport_failures.pop(key, None)
        if retry_parent is not None:
            retry_time = self.monotonic_ns()
            self._emit(
                TelemetryEventKind.TRANSPORT_RETRY,
                monotonic_ns=retry_time,
                stage=stage,
                job_id=job_id,
                operation_attempt=operation_attempt,
                parent_event_id=retry_parent,
                details={"retry_number": operation_attempt - 1},
            )

        if quality_repair_attempt is not None and operation_attempt == 1:
            repair_time = self.monotonic_ns()
            self._emit(
                TelemetryEventKind.QUALITY_REPAIR,
                monotonic_ns=repair_time,
                stage=stage,
                job_id=job_id,
                operation_attempt=operation_attempt,
                details={"quality_repair_attempt": quality_repair_attempt},
            )

        started_ns = self.monotonic_ns()
        started = self._emit(
            TelemetryEventKind.STAGE_STARTED,
            monotonic_ns=started_ns,
            stage=stage,
            job_id=job_id,
            operation_attempt=operation_attempt,
            details=(
                {"quality_repair_attempt": quality_repair_attempt}
                if quality_repair_attempt is not None
                else None
            ),
        )
        try:
            result = await _resolve(call())
        except Exception as exc:
            ended_ns = self.monotonic_ns()
            failed = self._emit(
                TelemetryEventKind.STAGE_FAILED,
                monotonic_ns=ended_ns,
                stage=stage,
                job_id=job_id,
                operation_attempt=operation_attempt,
                parent_event_id=started.event_id,
                duration_ns=ended_ns - started_ns,
                details={
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "transport_failure": isinstance(exc, self.transport_exceptions),
                    **(
                        {"quality_repair_attempt": quality_repair_attempt}
                        if quality_repair_attempt is not None
                        else {}
                    ),
                },
            )
            if isinstance(exc, self.transport_exceptions):
                self._transport_failures[key] = failed.event_id
            raise

        ended_ns = self.monotonic_ns()
        usage = None if usage_extractor is None else usage_extractor(result)
        cost = None if self.pricing is None else self.pricing.price(usage)
        self._emit(
            TelemetryEventKind.STAGE_COMPLETED,
            monotonic_ns=ended_ns,
            stage=stage,
            job_id=job_id,
            operation_attempt=operation_attempt,
            parent_event_id=started.event_id,
            duration_ns=ended_ns - started_ns,
            usage=usage,
            cost=cost,
            details=(
                {"quality_repair_attempt": quality_repair_attempt}
                if quality_repair_attempt is not None
                else None
            ),
        )
        return result

    def observe_run_state(self, state: Mapping[str, Any] | Any) -> None:
        payload = state.to_dict() if hasattr(state, "to_dict") else dict(state)
        run_id = str(payload.get("run_id", ""))
        if run_id != self.run_id:
            raise ValueError(f"run state id mismatch: expected={self.run_id} observed={run_id}")
        observed_ns = self.monotonic_ns()
        self._emit(
            TelemetryEventKind.RUN_STATE_OBSERVED,
            monotonic_ns=observed_ns,
            details={"phase": payload.get("phase")},
        )
        jobs = dict(payload.get("jobs", {}))
        for job_id in sorted(jobs):
            branch = dict(jobs[job_id])
            branch_ns = self.monotonic_ns()
            self._emit(
                TelemetryEventKind.BRANCH_STATE_OBSERVED,
                monotonic_ns=branch_ns,
                job_id=str(job_id),
                details={
                    "phase": branch.get("phase"),
                    "error": branch.get("error"),
                    "quality_repairs": int(branch.get("quality_repairs", 0)),
                    "transport_retries": dict(branch.get("transport_retries", {})),
                },
            )


class OrchestrationTelemetryHooks:
    """Provider-neutral adapters for the current orchestration callback contract."""

    def __init__(
        self,
        recorder: TelemetryRecorder,
        *,
        usage_extractors: Mapping[str, UsageExtractor] | None = None,
    ) -> None:
        self.recorder = recorder
        self.usage_extractors = dict(usage_extractors or {})

    def _usage_extractor(self, stage: str) -> UsageExtractor | None:
        return self.usage_extractors.get(stage)

    def planner(self, callback: Callable[[dict[str, Any]], MaybeAwaitable[T]]):
        async def wrapped(source: dict[str, Any]) -> T:
            return await self.recorder.invoke(
                stage="plan",
                call=lambda: callback(source),
                usage_extractor=self._usage_extractor("plan"),
            )

        return wrapped

    def generator(self, callback: Callable[[Any, dict[str, Any]], MaybeAwaitable[T]]):
        async def wrapped(job: Any, source: dict[str, Any]) -> T:
            return await self.recorder.invoke(
                stage="generate",
                job_id=str(job.job_id),
                call=lambda: callback(job, source),
                usage_extractor=self._usage_extractor("generate"),
            )

        return wrapped

    def evaluator(self, callback: Callable[[Any, Mapping[str, Any]], MaybeAwaitable[T]]):
        async def wrapped(job: Any, output: Mapping[str, Any]) -> T:
            return await self.recorder.invoke(
                stage="evaluate",
                job_id=str(job.job_id),
                call=lambda: callback(job, output),
                usage_extractor=self._usage_extractor("evaluate"),
            )

        return wrapped

    def repairer(
        self,
        callback: Callable[[Any, Mapping[str, Any], Any, int], MaybeAwaitable[T]],
    ):
        async def wrapped(job: Any, output: Mapping[str, Any], decision: Any, repair_attempt: int) -> T:
            return await self.recorder.invoke(
                stage="repair",
                job_id=str(job.job_id),
                quality_repair_attempt=repair_attempt,
                call=lambda: callback(job, output, decision, repair_attempt),
                usage_extractor=self._usage_extractor("repair"),
            )

        return wrapped

    def aggregator(self, callback: Callable[[Mapping[str, Mapping[str, Any]]], MaybeAwaitable[T]]):
        async def wrapped(outputs: Mapping[str, Mapping[str, Any]]) -> T:
            return await self.recorder.invoke(
                stage="aggregate",
                call=lambda: callback(outputs),
                usage_extractor=self._usage_extractor("aggregate"),
            )

        return wrapped

    def observe_state(self, state: Mapping[str, Any] | Any) -> None:
        self.recorder.observe_run_state(state)
