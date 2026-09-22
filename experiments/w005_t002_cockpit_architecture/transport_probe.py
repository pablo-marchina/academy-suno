#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from typing import Any


def ws_server_header_bytes(payload_len: int) -> int:
    # RFC 6455 server-to-client frames are not masked.
    if payload_len <= 125:
        return 2
    if payload_len <= 65535:
        return 4
    return 10


def make_event(index: int, target_bytes: int) -> dict[str, Any]:
    event = {
        "schema_version": "run-event.v1",
        "id": f"run-probe:evt-{index:06d}",
        "type": "job.phase.changed",
        "occurred_at": "2026-09-22T12:00:00Z",
        "workspace_id": "workspace-probe",
        "run_id": "run-probe",
        "job_id": f"job-{index % 9}",
        "cursor": index,
        "visibility": "workspace",
        "payload": {
            "phase": "evaluating" if index % 2 else "generating",
            "evidence_state": "DIAGNOSTIC_ONLY",
            "trace_ref": f"trace-{index:06d}",
        },
        "redactions": ["provider.request.body", "document.raw_text"],
    }
    # Pad deterministically so compact JSON is at least target_bytes.
    # We report the final exact compact-JSON byte length, not the requested target.
    raw = json.dumps(event, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(raw) < target_bytes:
        event["payload"]["pad"] = "x" * (target_bytes - len(raw))
    return event


def compact(event: dict[str, Any]) -> bytes:
    return json.dumps(event, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def sse_frame(event: dict[str, Any], raw: bytes) -> bytes:
    return (
        f"id: {event['id']}\n"
        f"event: {event['type']}\n"
        "data: "
    ).encode("utf-8") + raw + b"\n\n"


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    idx = min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))
    return ordered[idx]


def run(events_count: int, target_payload_bytes: int, poll_ms: int, poll_batch: int) -> dict[str, Any]:
    events = [make_event(i, target_payload_bytes) for i in range(1, events_count + 1)]
    raw = [compact(e) for e in events]

    json_bytes = sum(len(x) for x in raw)
    sse_bytes = sum(len(sse_frame(e, r)) for e, r in zip(events, raw))
    ws_bytes = sum(len(r) + ws_server_header_bytes(len(r)) for r in raw)

    polling_bytes = 0
    polls = 0
    for start in range(0, len(events), poll_batch):
        batch = events[start:start + poll_batch]
        body = json.dumps(
            {"events": batch, "next_cursor": batch[-1]["cursor"]},
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        polling_bytes += len(body)
        polls += 1

    # If event arrival is uniform relative to a polling timer, added delivery
    # delay is uniform in [0, poll_ms]. This is a model, not a network measurement.
    modeled_delays = [((i + 0.5) / 10000.0) * poll_ms for i in range(10000)]

    replay_cursor = events_count // 2
    replayed = [e for e in events if e["cursor"] > replay_cursor]
    expected = list(range(replay_cursor + 1, events_count + 1))
    observed = [e["cursor"] for e in replayed]

    mean_event = json_bytes / events_count
    return {
        "probe_version": "w005-t002-transport-probe.v1",
        "scope": {
            "events": events_count,
            "requested_min_json_event_bytes": target_payload_bytes,
            "mean_actual_json_event_bytes": round(mean_event, 2),
            "poll_interval_ms": poll_ms,
            "poll_batch_events": poll_batch,
            "excludes": [
                "HTTP/TLS handshake bytes",
                "TCP/IP framing",
                "compression",
                "proxy buffering",
                "real network latency",
                "client/server CPU",
            ],
        },
        "application_framing": {
            "raw_json": {"total_bytes": json_bytes, "overhead_vs_json_pct": 0.0},
            "sse": {
                "total_bytes": sse_bytes,
                "overhead_vs_json_pct": round((sse_bytes / json_bytes - 1.0) * 100, 3),
                "resume_primitive": "id + Last-Event-ID",
            },
            "websocket_server_text_frames": {
                "total_bytes": ws_bytes,
                "overhead_vs_json_pct": round((ws_bytes / json_bytes - 1.0) * 100, 3),
                "resume_primitive": "application-defined cursor required",
            },
            "polling_json_batches": {
                "total_bytes": polling_bytes,
                "overhead_vs_json_pct": round((polling_bytes / json_bytes - 1.0) * 100, 3),
                "poll_responses": polls,
                "resume_primitive": "cursor query/response",
            },
        },
        "polling_delivery_delay_model_ms": {
            "assumption": "event arrival uniform relative to polling timer",
            "mean": round(sum(modeled_delays) / len(modeled_delays), 3),
            "p50": round(percentile(modeled_delays, 0.50), 3),
            "p95": round(percentile(modeled_delays, 0.95), 3),
            "p99": round(percentile(modeled_delays, 0.99), 3),
            "max_lt": poll_ms,
        },
        "resume_replay_check": {
            "cursor": replay_cursor,
            "replayed_events": len(replayed),
            "first_cursor": observed[0] if observed else None,
            "last_cursor": observed[-1] if observed else None,
            "gap_free": observed == expected,
            "duplicates": len(observed) - len(set(observed)),
            "note": "Durable ordered storage is assumed; transport alone cannot guarantee replay.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=int, default=10000)
    parser.add_argument("--payload-bytes", type=int, default=768)
    parser.add_argument("--poll-ms", type=int, default=1000)
    parser.add_argument("--poll-batch", type=int, default=25)
    args = parser.parse_args()
    if min(args.events, args.payload_bytes, args.poll_ms, args.poll_batch) <= 0:
        parser.error("all numeric arguments must be > 0")
    print(json.dumps(run(args.events, args.payload_bytes, args.poll_ms, args.poll_batch), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
