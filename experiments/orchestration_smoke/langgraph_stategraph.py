from __future__ import annotations

import asyncio
from typing import Annotated, Any

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from .common import assert_join_invariants, make_jobs, merge_output_maps, process_job


class GraphState(TypedDict, total=False):
    jobs: list[str]
    job_id: str
    outputs: Annotated[dict[str, dict[str, Any]], merge_output_maps]
    joined_job_ids: list[str]
    phase: str


async def seed(_: GraphState) -> GraphState:
    return {"jobs": make_jobs(), "phase": "seeded"}


def fan_out(state: GraphState) -> list[Send]:
    return [Send("process_branch", {"job_id": job_id}) for job_id in state["jobs"]]


async def process_branch(state: GraphState) -> GraphState:
    item = await process_job(state["job_id"])
    return {"outputs": {item["job_id"]: item}}


def join(state: GraphState) -> GraphState:
    assert_join_invariants(state["outputs"])
    return {"joined_job_ids": sorted(state["outputs"]), "phase": "complete"}


def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("seed", seed)
    builder.add_node("process_branch", process_branch)
    builder.add_node("join", join)
    builder.add_edge(START, "seed")
    builder.add_conditional_edges("seed", fan_out, ["process_branch"])
    builder.add_edge("process_branch", "join")
    builder.add_edge("join", END)
    return builder.compile(checkpointer=InMemorySaver(), interrupt_after=["process_branch"])


async def run_with_checkpoint_resume() -> tuple[dict[str, Any], list[Any]]:
    graph = build_graph()
    config = {"configurable": {"thread_id": "exp-b-langgraph"}}
    paused = await graph.ainvoke({}, config=config)
    assert_join_invariants(paused["outputs"])

    snapshot = await graph.aget_state(config)
    assert snapshot.next == ("join",), f"unexpected resume target: {snapshot.next}"

    final_state = await graph.ainvoke(None, config=config)
    history = [item async for item in graph.aget_state_history(config)]
    assert final_state["phase"] == "complete"
    assert_join_invariants(final_state["outputs"])
    return final_state, history


def run() -> tuple[dict[str, Any], list[Any]]:
    return asyncio.run(run_with_checkpoint_resume())
