#!/usr/bin/env python3
"""Deterministic stdlib-only microbenchmark for W005-T007-A01.

This measures application-side JSON/SSE framing and replay/cardinality mechanics only.
It does NOT claim network, backend, exporter, or production latency/capacity.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import statistics
import time

N = 20_000
REPEATS = 5


def make_event(i: int, content_bytes: int = 0) -> dict:
    event = {
        "schema_version": "1.0",
        "event_id": i,
        "event_type": "run.node.updated",
        "tenant_id": f"t-{i % 100:03d}",
        "workspace_id": f"w-{i % 250:03d}",
        "request_id": f"req-{i:08d}",
        "run_id": f"run-{i // 20:07d}",
        "job_id": f"job-{i:08d}",
        "branch_id": f"aud{i % 3}-fmt{(i // 3) % 3}",
        "stage": ["source", "generate", "eval", "repair", "aggregate"][i % 5],
        "status": ["queued", "running", "passed", "failed", "review_required"][i % 5],
        "trace_id": hashlib.md5(str(i).encode()).hexdigest(),  # nosec: synthetic ID only
        "span_id": hashlib.sha1(str(i).encode()).hexdigest()[:16],  # nosec: synthetic ID only
        "occurred_at": "2026-09-22T12:00:00Z",
    }
    if content_bytes:
        event["content"] = "x" * content_bytes
    return event


def compact_json_bytes(value: dict) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode()


def measure_serialization(content_bytes: int) -> dict:
    events = [make_event(i, content_bytes) for i in range(1, N + 1)]
    elapsed = []
    total_size = 0
    for _ in range(REPEATS):
        start = time.perf_counter()
        sizes = [len(compact_json_bytes(event)) for event in events]
        elapsed.append(time.perf_counter() - start)
        total_size = sum(sizes)
    median = statistics.median(elapsed)
    return {
        "events": N,
        "content_bytes": content_bytes,
        "mean_json_bytes": total_size / N,
        "total_json_bytes": total_size,
        "serialization_seconds_median": median,
        "serialization_events_per_second_median": N / median,
        "all_seconds": elapsed,
    }


def main() -> None:
    metadata_only = measure_serialization(0)
    with_4k_raw_content = measure_serialization(4096)

    sse_sizes = []
    for i in range(1, N + 1):
        event = make_event(i)
        data = compact_json_bytes(event)
        frame = (
            f"id: {event['event_id']}\n"
            f"event: {event['event_type']}\n"
            f"data: {data.decode()}\n\n"
        ).encode()
        sse_sizes.append((len(frame), len(data)))

    mean_sse = sum(frame for frame, _ in sse_sizes) / N
    mean_json = sum(payload for _, payload in sse_sizes) / N

    replay_checks = []
    for cursor in [1, 17, 5000, 9999, 15000]:
        replay = list(range(cursor + 1, N + 1))
        replay_checks.append(
            {
                "last_event_id": cursor,
                "replayed": len(replay),
                "first": replay[0] if replay else None,
                "last": replay[-1] if replay else None,
                "gap_free": replay == list(range(cursor + 1, N + 1)),
                "duplicate_count": len(replay) - len(set(replay)),
            }
        )

    high_cardinality_scenario = {
        "tenants": 100,
        "runs_per_tenant": 10,
        "branches": 9,
        "providers": 3,
        "eval_types": 4,
    }
    naive_series = math.prod(high_cardinality_scenario.values())
    bounded_dimensions = {
        "stage": 5,
        "status": 5,
        "audience": 3,
        "format": 3,
        "provider": 3,
    }

    result = {
        "benchmark_id": "W005-T007-A01-observability-microbenchmark-v1",
        "date": "2026-09-22",
        "python": platform.python_version(),
        "iterations_per_variant": N,
        "repeats": REPEATS,
        "metadata_only": metadata_only,
        "with_4k_raw_content": with_4k_raw_content,
        "raw_content_payload_multiplier": (
            with_4k_raw_content["mean_json_bytes"] / metadata_only["mean_json_bytes"]
        ),
        "sse_metadata_only": {
            "mean_json_bytes": mean_json,
            "mean_sse_frame_bytes": mean_sse,
            "application_framing_overhead_percent": ((mean_sse - mean_json) / mean_json) * 100,
        },
        "replay_checks": replay_checks,
        "cardinality_scenario": {
            "inputs": high_cardinality_scenario,
            "naive_series_if_high_cardinality_ids_are_metric_labels": naive_series,
            "otel_default_cardinality_limit_per_metric_stream": 2000,
            "ratio_vs_default_limit": naive_series / 2000,
            "bounded_dimension_example": bounded_dimensions,
            "bounded_cartesian_upper_bound": math.prod(bounded_dimensions.values()),
            "note": "Scenario-only combinatorics, not measured Academy production load.",
        },
        "limitations": [
            "CPU serialization timing is local synthetic Python only; not network/export/backend latency.",
            "4 KiB content uses repeated ASCII and does not model compression or real document text.",
            "SSE size excludes HTTP/TLS/TCP framing and proxy buffering.",
            "Replay assumes a durable ordered event store and strict resume after last_event_id.",
            "Cardinality values are scenario combinatorics, not observed production usage.",
        ],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
