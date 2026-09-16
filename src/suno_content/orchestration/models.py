from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


JsonObject = dict[str, Any]


class RunPhase(str, Enum):
    CREATED = "created"
    PLANNED = "planned"
    BRANCHES_RUNNING = "branches_running"
    BRANCHES_COMPLETE = "branches_complete"
    JOINED = "joined"
    AGGREGATED = "aggregated"
    COMPLETE = "complete"
    REVIEW_REQUIRED = "review_required"
    FAILED = "failed"


class BranchPhase(str, Enum):
    PLANNED = "planned"
    GENERATED = "generated"
    NEEDS_REPAIR = "needs_repair"
    REPAIRED = "repaired"
    ACCEPTED = "accepted"
    REVIEW_REQUIRED = "review_required"
    FAILED = "failed"


class EvaluationAction(str, Enum):
    PASS = "pass"
    REPAIR = "repair"
    REVIEW_REQUIRED = "review_required"
    FAIL = "fail"


@dataclass(frozen=True, slots=True)
class NodeSpec:
    node_id: str
    kind: str
    description: str

    def to_dict(self) -> JsonObject:
        return {
            "node_id": self.node_id,
            "kind": self.kind,
            "description": self.description,
        }


@dataclass(frozen=True, slots=True)
class EdgeSpec:
    source: str
    target: str
    condition: str = "always"

    def to_dict(self) -> JsonObject:
        return {
            "source": self.source,
            "target": self.target,
            "condition": self.condition,
        }


@dataclass(frozen=True, slots=True)
class GraphDefinition:
    graph_id: str
    version: str
    nodes: tuple[NodeSpec, ...]
    edges: tuple[EdgeSpec, ...]

    def to_dict(self) -> JsonObject:
        return {
            "graph_id": self.graph_id,
            "version": self.version,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
        }


DEFAULT_GRAPH = GraphDefinition(
    graph_id="suno_content.source_to_3x3",
    version="graph.v1",
    nodes=(
        NodeSpec("source", "input", "Validate/capture source context"),
        NodeSpec("plan", "planner", "Materialize exactly nine keyed jobs"),
        NodeSpec("branch.generate", "fan_out", "Generate each branch concurrently"),
        NodeSpec("branch.evaluate", "quality_gate", "Evaluate one branch"),
        NodeSpec("branch.repair", "repair", "Repair only the failing branch"),
        NodeSpec("join", "fan_in", "Lossless keyed join by job_id"),
        NodeSpec("aggregate", "aggregate", "Build the run aggregate"),
        NodeSpec("complete", "terminal", "Persist terminal run state"),
    ),
    edges=(
        EdgeSpec("source", "plan"),
        EdgeSpec("plan", "branch.generate", "nine_unique_jobs"),
        EdgeSpec("branch.generate", "branch.evaluate"),
        EdgeSpec("branch.evaluate", "branch.repair", "evaluation=repair"),
        EdgeSpec("branch.repair", "branch.evaluate", "repair_complete"),
        EdgeSpec("branch.evaluate", "join", "evaluation=pass AND all_branches_pass"),
        EdgeSpec("join", "aggregate", "lossless_join"),
        EdgeSpec("aggregate", "complete"),
    ),
)


@dataclass(frozen=True, slots=True)
class JobSpec:
    job_id: str
    payload: JsonObject = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.job_id.strip():
            raise ValueError("job_id must not be empty")


@dataclass(frozen=True, slots=True)
class QualityDecision:
    action: EvaluationAction
    reasons: tuple[str, ...] = ()
    metadata: JsonObject = field(default_factory=dict)

    def to_dict(self) -> JsonObject:
        return {
            "action": self.action.value,
            "reasons": list(self.reasons),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "QualityDecision":
        return cls(
            action=EvaluationAction(str(value["action"])),
            reasons=tuple(str(item) for item in value.get("reasons", ())),
            metadata=dict(value.get("metadata", {})),
        )


@dataclass(slots=True)
class BranchState:
    job_id: str
    payload: JsonObject
    phase: BranchPhase = BranchPhase.PLANNED
    output: JsonObject | None = None
    evaluation: QualityDecision | None = None
    quality_repairs: int = 0
    transport_retries: dict[str, int] = field(default_factory=dict)
    events: list[JsonObject] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> JsonObject:
        return {
            "job_id": self.job_id,
            "payload": dict(self.payload),
            "phase": self.phase.value,
            "output": self.output,
            "evaluation": None if self.evaluation is None else self.evaluation.to_dict(),
            "quality_repairs": self.quality_repairs,
            "transport_retries": dict(self.transport_retries),
            "events": [dict(event) for event in self.events],
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "BranchState":
        evaluation = value.get("evaluation")
        return cls(
            job_id=str(value["job_id"]),
            payload=dict(value.get("payload", {})),
            phase=BranchPhase(str(value.get("phase", BranchPhase.PLANNED.value))),
            output=None if value.get("output") is None else dict(value["output"]),
            evaluation=None if evaluation is None else QualityDecision.from_dict(evaluation),
            quality_repairs=int(value.get("quality_repairs", 0)),
            transport_retries={
                str(key): int(count)
                for key, count in dict(value.get("transport_retries", {})).items()
            },
            events=[dict(event) for event in value.get("events", ())],
            error=None if value.get("error") is None else str(value["error"]),
        )


@dataclass(slots=True)
class RunState:
    run_id: str
    source: JsonObject
    graph_version: str = DEFAULT_GRAPH.version
    phase: RunPhase = RunPhase.CREATED
    jobs: dict[str, BranchState] = field(default_factory=dict)
    joined_outputs: dict[str, JsonObject] = field(default_factory=dict)
    aggregate: JsonObject | None = None
    events: list[JsonObject] = field(default_factory=list)
    metadata: JsonObject = field(default_factory=dict)

    def to_dict(self) -> JsonObject:
        return {
            "run_id": self.run_id,
            "source": dict(self.source),
            "graph_version": self.graph_version,
            "phase": self.phase.value,
            "jobs": {job_id: branch.to_dict() for job_id, branch in self.jobs.items()},
            "joined_outputs": {
                job_id: dict(output) for job_id, output in self.joined_outputs.items()
            },
            "aggregate": None if self.aggregate is None else dict(self.aggregate),
            "events": [dict(event) for event in self.events],
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "RunState":
        return cls(
            run_id=str(value["run_id"]),
            source=dict(value.get("source", {})),
            graph_version=str(value.get("graph_version", DEFAULT_GRAPH.version)),
            phase=RunPhase(str(value.get("phase", RunPhase.CREATED.value))),
            jobs={
                str(job_id): BranchState.from_dict(branch)
                for job_id, branch in dict(value.get("jobs", {})).items()
            },
            joined_outputs={
                str(job_id): dict(output)
                for job_id, output in dict(value.get("joined_outputs", {})).items()
            },
            aggregate=None if value.get("aggregate") is None else dict(value["aggregate"]),
            events=[dict(event) for event in value.get("events", ())],
            metadata=dict(value.get("metadata", {})),
        )
