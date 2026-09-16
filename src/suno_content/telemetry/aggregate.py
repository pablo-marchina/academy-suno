from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal
from math import ceil
from typing import Any, Iterable

from .models import SUMMARY_SCHEMA_VERSION, TelemetryEvent, TelemetryEventKind


def _percentile_nearest_rank(values: list[int], percentile: float) -> int:
    if not values:
        raise ValueError("percentile requires at least one value")
    ordered = sorted(values)
    rank = max(1, ceil(percentile * len(ordered)))
    return ordered[rank - 1]


def summarize(events: Iterable[TelemetryEvent]) -> dict[str, Any]:
    ordered = sorted(events, key=lambda event: event.sequence)
    if not ordered:
        raise ValueError("at least one telemetry event is required")
    run_ids = {event.run_id for event in ordered}
    if len(run_ids) != 1:
        raise ValueError("summary cannot mix multiple run_ids")

    stage_durations: dict[str, list[int]] = defaultdict(list)
    retry_counts: Counter[tuple[str, str | None]] = Counter()
    repair_counts: Counter[str | None] = Counter()
    usage_totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    usage_events = 0
    cost_totals: dict[tuple[str, str], Decimal] = defaultdict(lambda: Decimal("0"))
    terminal_run_phase: str | None = None
    branch_states: dict[str, dict[str, Any]] = {}

    for event in ordered:
        if event.kind in {TelemetryEventKind.STAGE_COMPLETED, TelemetryEventKind.STAGE_FAILED}:
            if event.stage is not None and event.duration_ns is not None:
                stage_durations[event.stage].append(event.duration_ns)
        if event.kind is TelemetryEventKind.TRANSPORT_RETRY:
            retry_counts[(event.stage or "unknown", event.job_id)] += 1
        if event.kind is TelemetryEventKind.QUALITY_REPAIR:
            repair_counts[event.job_id] += 1
        if event.usage is not None:
            usage_events += 1
            for meter_id, quantity in event.usage.quantities.items():
                usage_totals[meter_id] += quantity
        if event.cost is not None:
            key = (event.cost.currency, event.cost.pricing_version)
            cost_totals[key] += event.cost.amount
        if event.kind is TelemetryEventKind.RUN_STATE_OBSERVED:
            terminal_run_phase = None if event.details.get("phase") is None else str(event.details["phase"])
        if event.kind is TelemetryEventKind.BRANCH_STATE_OBSERVED and event.job_id is not None:
            branch_states[event.job_id] = dict(event.details)

    latency = {
        stage: {
            "count": len(values),
            "min_ns": min(values),
            "max_ns": max(values),
            "mean_ns": sum(values) // len(values),
            "p50_ns": _percentile_nearest_rank(values, 0.50),
            "p95_ns": _percentile_nearest_rank(values, 0.95),
        }
        for stage, values in sorted(stage_durations.items())
    }

    retry_detail = [
        {"stage": stage, "job_id": job_id, "count": count}
        for (stage, job_id), count in sorted(
            retry_counts.items(), key=lambda item: (item[0][0], item[0][1] or "")
        )
    ]
    repair_detail = [
        {"job_id": job_id, "count": count}
        for job_id, count in sorted(repair_counts.items(), key=lambda item: item[0] or "")
    ]

    failures = sorted(
        job_id for job_id, state in branch_states.items() if state.get("phase") == "failed"
    )
    review_required = sorted(
        job_id
        for job_id, state in branch_states.items()
        if state.get("phase") == "review_required"
    )

    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "run_id": ordered[0].run_id,
        "event_count": len(ordered),
        "stage_latency": latency,
        "transport_retries": {
            "total": sum(retry_counts.values()),
            "by_stage_job": retry_detail,
        },
        "quality_repairs": {
            "total": sum(repair_counts.values()),
            "by_job": repair_detail,
        },
        "usage": (
            None
            if usage_events == 0
            else {
                "observed_event_count": usage_events,
                "quantities": {key: str(value) for key, value in sorted(usage_totals.items())},
            }
        ),
        "observed_cost": (
            None
            if not cost_totals
            else [
                {
                    "currency": currency,
                    "pricing_version": pricing_version,
                    "amount": str(amount),
                }
                for (currency, pricing_version), amount in sorted(cost_totals.items())
            ]
        ),
        "terminal": {
            "run_phase": terminal_run_phase,
            "branch_states": branch_states,
            "failed_job_ids": failures,
            "review_required_job_ids": review_required,
        },
    }
