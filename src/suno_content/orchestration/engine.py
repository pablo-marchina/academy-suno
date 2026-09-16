from __future__ import annotations

import asyncio
import inspect
from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import Any, TypeVar

from suno_content.runstore import SQLiteRunStore

from .models import (
    DEFAULT_GRAPH,
    BranchPhase,
    BranchState,
    EvaluationAction,
    GraphDefinition,
    JobSpec,
    QualityDecision,
    RunPhase,
    RunState,
)


T = TypeVar("T")
MaybeAwaitable = T | Awaitable[T]
Planner = Callable[[dict[str, Any]], MaybeAwaitable[Sequence[JobSpec]]]
Generator = Callable[[JobSpec, dict[str, Any]], MaybeAwaitable[Mapping[str, Any]]]
Evaluator = Callable[[JobSpec, Mapping[str, Any]], MaybeAwaitable[QualityDecision]]
Repairer = Callable[
    [JobSpec, Mapping[str, Any], QualityDecision, int],
    MaybeAwaitable[Mapping[str, Any]],
]
Aggregator = Callable[[Mapping[str, Mapping[str, Any]]], MaybeAwaitable[Mapping[str, Any]]]


class OrchestrationInvariantError(RuntimeError):
    pass


class TransportExhaustedError(RuntimeError):
    pass


async def _resolve(value: MaybeAwaitable[T]) -> T:
    if inspect.isawaitable(value):
        return await value
    return value


class AsyncGraphOrchestrator:
    """Plain-async runtime driven by an explicit graph and durable state machine."""

    def __init__(
        self,
        *,
        store: SQLiteRunStore,
        planner: Planner,
        generator: Generator,
        evaluator: Evaluator,
        repairer: Repairer,
        aggregator: Aggregator,
        graph: GraphDefinition = DEFAULT_GRAPH,
        transport_retry_limit: int = 2,
        max_quality_repairs: int = 2,
        transport_exceptions: tuple[type[BaseException], ...] = (TimeoutError, ConnectionError),
    ) -> None:
        if transport_retry_limit < 0:
            raise ValueError("transport_retry_limit must be >= 0")
        if max_quality_repairs < 0:
            raise ValueError("max_quality_repairs must be >= 0")
        self.store = store
        self.planner = planner
        self.generator = generator
        self.evaluator = evaluator
        self.repairer = repairer
        self.aggregator = aggregator
        self.graph = graph
        self.transport_retry_limit = transport_retry_limit
        self.max_quality_repairs = max_quality_repairs
        self.transport_exceptions = transport_exceptions

    def describe_graph(self) -> dict[str, Any]:
        return self.graph.to_dict()

    async def start(
        self,
        *,
        run_id: str,
        source: Mapping[str, Any],
        metadata: Mapping[str, Any] | None = None,
        pause_after: str | None = None,
    ) -> RunState:
        state = RunState(
            run_id=run_id,
            source=dict(source),
            graph_version=self.graph.version,
            metadata=dict(metadata or {}),
        )
        self.store.create(state.to_dict(), reason="source_captured")
        return await self._advance(state, pause_after=pause_after)

    async def resume(self, run_id: str, *, pause_after: str | None = None) -> RunState:
        state = RunState.from_dict(self.store.load(run_id))
        if state.graph_version != self.graph.version:
            raise OrchestrationInvariantError(
                f"graph version mismatch: stored={state.graph_version} runtime={self.graph.version}"
            )
        return await self._advance(state, pause_after=pause_after)

    async def _advance(self, state: RunState, *, pause_after: str | None) -> RunState:
        if state.phase in {RunPhase.COMPLETE, RunPhase.REVIEW_REQUIRED, RunPhase.FAILED}:
            return state

        if state.phase is RunPhase.CREATED:
            jobs = await _resolve(self.planner(dict(state.source)))
            self._install_jobs(state, jobs)
            state.phase = RunPhase.PLANNED
            self._event(state, "planned", job_count=len(state.jobs))
            self._checkpoint(state, "planned_3x3")
            if pause_after == "planned":
                return state

        if state.phase in {RunPhase.PLANNED, RunPhase.BRANCHES_RUNNING}:
            state.phase = RunPhase.BRANCHES_RUNNING
            self._checkpoint(state, "fanout_started")
            await asyncio.gather(
                *(self._advance_branch(state, branch) for branch in state.jobs.values())
            )
            failed = [branch.job_id for branch in state.jobs.values() if branch.phase is BranchPhase.FAILED]
            review = [
                branch.job_id
                for branch in state.jobs.values()
                if branch.phase is BranchPhase.REVIEW_REQUIRED
            ]
            if failed:
                state.phase = RunPhase.FAILED
                self._event(state, "run_failed", job_ids=failed)
                self._checkpoint(state, "branch_failure")
                return state
            if review:
                state.phase = RunPhase.REVIEW_REQUIRED
                self._event(state, "review_required", job_ids=review)
                self._checkpoint(state, "review_required")
                return state
            if not all(
                branch.phase is BranchPhase.ACCEPTED for branch in state.jobs.values()
            ):
                raise OrchestrationInvariantError("fan-out returned with non-terminal branches")
            state.phase = RunPhase.BRANCHES_COMPLETE
            self._event(state, "branches_complete", job_count=len(state.jobs))
            self._checkpoint(state, "branches_complete")
            if pause_after in {"branches", "fanout"}:
                return state

        if state.phase is RunPhase.BRANCHES_COMPLETE:
            state.joined_outputs = self._lossless_join(state)
            state.phase = RunPhase.JOINED
            self._event(state, "joined", job_count=len(state.joined_outputs))
            self._checkpoint(state, "lossless_join")
            if pause_after == "join":
                return state

        if state.phase is RunPhase.JOINED:
            aggregate = await _resolve(self.aggregator(dict(state.joined_outputs)))
            state.aggregate = dict(aggregate)
            state.phase = RunPhase.AGGREGATED
            self._event(state, "aggregated")
            self._checkpoint(state, "aggregate_complete")
            if pause_after == "aggregate":
                return state

        if state.phase is RunPhase.AGGREGATED:
            state.phase = RunPhase.COMPLETE
            self._event(state, "run_complete")
            self._checkpoint(state, "run_complete")

        return state

    def _install_jobs(self, state: RunState, jobs: Sequence[JobSpec]) -> None:
        if len(jobs) != 9:
            raise OrchestrationInvariantError(
                f"planner must return exactly nine jobs, got {len(jobs)}"
            )
        installed: dict[str, BranchState] = {}
        for job in jobs:
            if job.job_id in installed:
                raise OrchestrationInvariantError(
                    f"duplicate job_id would overwrite branch state: {job.job_id}"
                )
            installed[job.job_id] = BranchState(job_id=job.job_id, payload=dict(job.payload))
        state.jobs = installed

    async def _advance_branch(self, state: RunState, branch: BranchState) -> None:
        if branch.phase in {
            BranchPhase.ACCEPTED,
            BranchPhase.REVIEW_REQUIRED,
            BranchPhase.FAILED,
        }:
            return
        job = JobSpec(branch.job_id, dict(branch.payload))
        try:
            while branch.phase not in {
                BranchPhase.ACCEPTED,
                BranchPhase.REVIEW_REQUIRED,
                BranchPhase.FAILED,
            }:
                if branch.phase is BranchPhase.PLANNED:
                    branch.output = dict(
                        await self._transport_call(
                            state,
                            branch,
                            "generate",
                            lambda: self.generator(job, dict(state.source)),
                        )
                    )
                    branch.phase = BranchPhase.GENERATED
                    branch.evaluation = None
                    self._branch_event(branch, "generated")
                    self._checkpoint(state, f"generated:{branch.job_id}")
                    continue

                if branch.phase in {BranchPhase.GENERATED, BranchPhase.REPAIRED}:
                    if branch.output is None:
                        raise OrchestrationInvariantError(
                            f"{branch.job_id} cannot evaluate without output"
                        )
                    decision = await _resolve(self.evaluator(job, dict(branch.output)))
                    if not isinstance(decision, QualityDecision):
                        raise OrchestrationInvariantError(
                            "evaluator must return QualityDecision"
                        )
                    branch.evaluation = decision
                    if decision.action is EvaluationAction.PASS:
                        branch.phase = BranchPhase.ACCEPTED
                        self._branch_event(branch, "quality_pass")
                    elif decision.action is EvaluationAction.REPAIR:
                        if branch.quality_repairs >= self.max_quality_repairs:
                            branch.phase = BranchPhase.FAILED
                            branch.error = "quality repair limit exhausted"
                            self._branch_event(branch, "quality_repair_exhausted")
                        else:
                            branch.phase = BranchPhase.NEEDS_REPAIR
                            self._branch_event(branch, "quality_repair_requested")
                    elif decision.action is EvaluationAction.REVIEW_REQUIRED:
                        branch.phase = BranchPhase.REVIEW_REQUIRED
                        self._branch_event(branch, "review_required")
                    else:
                        branch.phase = BranchPhase.FAILED
                        branch.error = "quality evaluation hard fail"
                        self._branch_event(branch, "quality_fail")
                    self._checkpoint(state, f"evaluated:{branch.job_id}")
                    continue

                if branch.phase is BranchPhase.NEEDS_REPAIR:
                    if branch.output is None or branch.evaluation is None:
                        raise OrchestrationInvariantError(
                            f"{branch.job_id} cannot repair without output/evaluation"
                        )
                    next_repair = branch.quality_repairs + 1
                    repaired = await self._transport_call(
                        state,
                        branch,
                        "repair",
                        lambda: self.repairer(
                            job,
                            dict(branch.output or {}),
                            branch.evaluation,
                            next_repair,
                        ),
                    )
                    branch.output = dict(repaired)
                    branch.quality_repairs = next_repair
                    branch.phase = BranchPhase.REPAIRED
                    self._branch_event(
                        branch,
                        "quality_repair",
                        repair_attempt=next_repair,
                    )
                    self._checkpoint(state, f"repaired:{branch.job_id}")
                    continue

                raise OrchestrationInvariantError(
                    f"unsupported branch phase: {branch.phase.value}"
                )
        except TransportExhaustedError as exc:
            branch.phase = BranchPhase.FAILED
            branch.error = str(exc)
            self._branch_event(branch, "transport_exhausted", error=str(exc))
            self._checkpoint(state, f"transport_exhausted:{branch.job_id}")
        except Exception as exc:  # persist unexpected branch-local failure for recovery/audit
            branch.phase = BranchPhase.FAILED
            branch.error = f"{type(exc).__name__}: {exc}"
            self._branch_event(branch, "branch_exception", error=branch.error)
            self._checkpoint(state, f"branch_exception:{branch.job_id}")

    async def _transport_call(
        self,
        state: RunState,
        branch: BranchState,
        stage: str,
        call: Callable[[], MaybeAwaitable[Mapping[str, Any]]],
    ) -> Mapping[str, Any]:
        retries = 0
        while True:
            try:
                return await _resolve(call())
            except self.transport_exceptions as exc:
                if retries >= self.transport_retry_limit:
                    raise TransportExhaustedError(
                        f"transport retry limit exhausted at {stage} for {branch.job_id}: "
                        f"{type(exc).__name__}: {exc}"
                    ) from exc
                retries += 1
                branch.transport_retries[stage] = branch.transport_retries.get(stage, 0) + 1
                self._branch_event(
                    branch,
                    "transport_retry",
                    stage=stage,
                    retry=retries,
                    error_type=type(exc).__name__,
                )
                self._checkpoint(state, f"transport_retry:{stage}:{branch.job_id}:{retries}")
                await asyncio.sleep(0)

    def _lossless_join(self, state: RunState) -> dict[str, dict[str, Any]]:
        if len(state.jobs) != 9:
            raise OrchestrationInvariantError("join requires exactly nine branches")
        joined: dict[str, dict[str, Any]] = {}
        for job_id, branch in state.jobs.items():
            if branch.phase is not BranchPhase.ACCEPTED or branch.output is None:
                raise OrchestrationInvariantError(
                    f"join received non-accepted branch: {job_id}:{branch.phase.value}"
                )
            if job_id in joined:
                raise OrchestrationInvariantError(f"duplicate join key: {job_id}")
            joined[job_id] = dict(branch.output)
        if set(joined) != set(state.jobs) or len(joined) != 9:
            raise OrchestrationInvariantError("join lost or invented branch outputs")
        return joined

    def _checkpoint(self, state: RunState, reason: str) -> None:
        self.store.checkpoint(state.to_dict(), reason=reason)

    @staticmethod
    def _event(state: RunState, kind: str, **details: Any) -> None:
        state.events.append({"kind": kind, **details})

    @staticmethod
    def _branch_event(branch: BranchState, kind: str, **details: Any) -> None:
        branch.events.append({"kind": kind, **details})
