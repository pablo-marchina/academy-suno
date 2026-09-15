from __future__ import annotations

import asyncio
from typing import Any

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from .common import make_jobs, process_job


class UnsafeState(TypedDict, total=False):
    jobs: list[str]
    job_id: str
    outputs: dict[str, dict[str, Any]]


async def unsafe_seed(_: UnsafeState) -> UnsafeState:
    return {"jobs": make_jobs()}


def unsafe_fan_out(state: UnsafeState) -> list[Send]:
    return [Send("unsafe_branch", {"job_id": job_id}) for job_id in state["jobs"]]


async def unsafe_branch(state: UnsafeState) -> UnsafeState:
    item = await process_job(state["job_id"])
    return {"outputs": {item["job_id"]: item}}


def build_unsafe_graph():
    builder = StateGraph(UnsafeState)
    builder.add_node("seed", unsafe_seed)
    builder.add_node("unsafe_branch", unsafe_branch)
    builder.add_edge(START, "seed")
    builder.add_conditional_edges("seed", unsafe_fan_out, ["unsafe_branch"])
    builder.add_edge("unsafe_branch", END)
    return builder.compile()


async def probe_missing_reducer_hazard() -> str:
    try:
        await build_unsafe_graph().ainvoke({})
    except Exception as exc:  # package-specific InvalidUpdateError across versions
        return f"{type(exc).__name__}: {exc}"
    raise AssertionError("unsafe parallel state unexpectedly succeeded without reducer")


def run_hazard_probe() -> str:
    return asyncio.run(probe_missing_reducer_hazard())
