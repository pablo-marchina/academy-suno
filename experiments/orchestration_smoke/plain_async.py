from __future__ import annotations

import asyncio
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from .common import assert_join_invariants, make_jobs, process_job


@dataclass
class MemoryCheckpointStore:
    snapshots: list[dict[str, Any]] = field(default_factory=list)

    def save(self, state: dict[str, Any]) -> None:
        self.snapshots.append(deepcopy(state))

    def latest(self) -> dict[str, Any]:
        if not self.snapshots:
            raise RuntimeError("no checkpoint to resume")
        return deepcopy(self.snapshots[-1])

    def history(self) -> list[dict[str, Any]]:
        return deepcopy(self.snapshots)


async def fan_out(store: MemoryCheckpointStore) -> dict[str, Any]:
    jobs = make_jobs()
    branch_results = await asyncio.gather(*(process_job(job_id) for job_id in jobs))
    outputs = {item["job_id"]: item for item in branch_results}
    state = {"phase": "fanout_complete", "jobs": jobs, "outputs": outputs}
    store.save(state)
    return state


async def resume_from_checkpoint(store: MemoryCheckpointStore) -> dict[str, Any]:
    state = store.latest()
    assert state["phase"] == "fanout_complete"
    assert_join_invariants(state["outputs"])
    state["joined_job_ids"] = sorted(state["outputs"])
    state["phase"] = "complete"
    store.save(state)
    return state


async def run_with_checkpoint_resume() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    store = MemoryCheckpointStore()
    await fan_out(store)  # simulated process stop here
    final_state = await resume_from_checkpoint(store)
    return final_state, store.history()


def run() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    return asyncio.run(run_with_checkpoint_resume())
