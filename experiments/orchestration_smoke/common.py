from __future__ import annotations

import asyncio
from copy import deepcopy
from itertools import product
from typing import Any

AUDIENCES = ("beginner", "intermediate", "advanced")
FORMATS = ("article", "carousel", "short_video")
JOB_IDS = tuple(f"{audience}:{fmt}" for audience, fmt in product(AUDIENCES, FORMATS))
FAIL_JOB_ID = "beginner:carousel"


def make_jobs() -> list[str]:
    return list(JOB_IDS)


async def process_job(job_id: str) -> dict[str, Any]:
    """Deterministic mock: exactly one branch fails first-pass quality, then repairs locally."""
    await asyncio.sleep(0)
    first_pass_ok = job_id != FAIL_JOB_ID
    repair_count = 0
    value = f"draft::{job_id}"
    events = [f"generated:{job_id}"]

    if not first_pass_ok:
        events.append(f"quality_fail:{job_id}")
        repair_count = 1
        await asyncio.sleep(0)
        value = f"repaired::{job_id}"
        events.append(f"repaired:{job_id}")

    return {
        "job_id": job_id,
        "first_pass_ok": first_pass_ok,
        "repair_count": repair_count,
        "final_status": "PASS",
        "value": value,
        "events": events,
    }


def merge_output_maps(
    left: dict[str, dict[str, Any]] | None,
    right: dict[str, dict[str, Any]] | None,
) -> dict[str, dict[str, Any]]:
    """Reducer used by the LangGraph baseline; duplicate job IDs are a hard error."""
    merged = dict(left or {})
    incoming = right or {}
    overlap = merged.keys() & incoming.keys()
    if overlap:
        raise ValueError(f"duplicate branch outputs: {sorted(overlap)}")
    merged.update(deepcopy(incoming))
    return merged


def assert_join_invariants(outputs: dict[str, dict[str, Any]]) -> None:
    assert set(outputs) == set(JOB_IDS), f"join lost outputs: got={sorted(outputs)}"
    repaired = [job_id for job_id, item in outputs.items() if item["repair_count"]]
    assert repaired == [FAIL_JOB_ID], f"repair leaked across branches: {repaired}"
    assert all(item["final_status"] == "PASS" for item in outputs.values())
