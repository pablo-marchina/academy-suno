from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

JsonObject = dict[str, Any]


class EvaluationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class HardGateAuthority(str, Enum):
    SOURCE = "SOURCE"
    DETERMINISTIC_FACTUAL = "DETERMINISTIC_FACTUAL"
    POLICY = "POLICY"


class MetricGoal(str, Enum):
    MAXIMIZE = "MAXIMIZE"
    MINIMIZE = "MINIMIZE"


class StopReason(str, Enum):
    ACCEPTED_AFTER_REEVALUATION = "ACCEPTED_AFTER_REEVALUATION"
    ALREADY_ACCEPTED = "ALREADY_ACCEPTED"
    NO_LOCAL_REPAIR_AVAILABLE = "NO_LOCAL_REPAIR_AVAILABLE"
    NO_MEASURABLE_IMPROVEMENT = "NO_MEASURABLE_IMPROVEMENT"
    HARD_GATE_REGRESSION = "HARD_GATE_REGRESSION"
    MAX_ATTEMPTS_REACHED = "MAX_ATTEMPTS_REACHED"


@dataclass(frozen=True, slots=True)
class HardGateRun:
    authority: HardGateAuthority
    status: EvaluationStatus
    code: str
    run_id: str

    def __post_init__(self) -> None:
        if not self.code.strip() or not self.run_id.strip():
            raise ValueError("hard gate code/run_id must not be empty")


@dataclass(frozen=True, slots=True)
class MetricObservation:
    name: str
    value: float
    goal: MetricGoal
    target: float | None = None
    violated: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("metric name must not be empty")


@dataclass(frozen=True, slots=True)
class EvaluationSnapshot:
    evaluation_id: str
    evaluator_version: str
    status: EvaluationStatus
    hard_gates: tuple[HardGateRun, ...]
    failure_codes: tuple[str, ...] = ()
    metrics: tuple[MetricObservation, ...] = ()
    diagnostics: JsonObject = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.evaluation_id.strip() or not self.evaluator_version.strip():
            raise ValueError("evaluation identity/version must not be empty")
        authorities = [gate.authority for gate in self.hard_gates]
        expected = set(HardGateAuthority)
        if set(authorities) != expected or len(authorities) != len(expected):
            raise ValueError("snapshot must contain exactly one SOURCE, DETERMINISTIC_FACTUAL and POLICY hard gate")
        blocking = [gate for gate in self.hard_gates if gate.status != EvaluationStatus.PASS]
        if self.status == EvaluationStatus.PASS and blocking:
            raise ValueError("PASS cannot compensate a hard-gate FAIL/REVIEW_REQUIRED")
        if self.status == EvaluationStatus.PASS and self.failure_codes:
            raise ValueError("PASS snapshot cannot carry failure codes")

    @property
    def hard_fail_codes(self) -> tuple[str, ...]:
        return tuple(gate.code for gate in self.hard_gates if gate.status == EvaluationStatus.FAIL)

    @property
    def hard_block_count(self) -> int:
        return sum(gate.status != EvaluationStatus.PASS for gate in self.hard_gates)

    def metric_map(self) -> dict[str, MetricObservation]:
        return {metric.name: metric for metric in self.metrics}


@dataclass(frozen=True, slots=True)
class RepairDirective:
    source_code: str
    operation: str
    reason: str
    repairable: bool = True


@dataclass(frozen=True, slots=True)
class RepairRequest:
    job_id: str
    attempt_number: int
    before_evaluation_id: str
    failure_codes: tuple[str, ...]
    metric_triggers: tuple[str, ...]
    directives: tuple[RepairDirective, ...]

    @property
    def actionable(self) -> bool:
        return any(directive.repairable for directive in self.directives)


@dataclass(frozen=True, slots=True)
class MetricDelta:
    name: str
    before: float
    after: float
    signed_improvement: float


@dataclass(frozen=True, slots=True)
class RepairAttemptLineage:
    attempt_number: int
    job_id: str
    request: RepairRequest
    before_evaluation: EvaluationSnapshot
    after_evaluation: EvaluationSnapshot
    before_output_hash: str
    after_output_hash: str
    sibling_hashes_before: Mapping[str, str]
    sibling_hashes_after: Mapping[str, str]
    metric_deltas: tuple[MetricDelta, ...]
    resolved_failure_codes: tuple[str, ...]
    introduced_failure_codes: tuple[str, ...]
    hard_gate_regressions: tuple[str, ...]

    @property
    def measurable_improvement(self) -> bool:
        if self.after_evaluation.hard_block_count < self.before_evaluation.hard_block_count:
            return True
        if self.resolved_failure_codes:
            return True
        return any(delta.signed_improvement > 0 for delta in self.metric_deltas)

    @property
    def has_regression(self) -> bool:
        return bool(
            self.introduced_failure_codes
            or self.hard_gate_regressions
            or any(delta.signed_improvement < 0 for delta in self.metric_deltas)
        )


@dataclass(frozen=True, slots=True)
class RepairLoopResult:
    job_id: str
    final_output: JsonObject
    final_evaluation: EvaluationSnapshot
    attempts: tuple[RepairAttemptLineage, ...]
    stop_reason: StopReason
    accepted_sibling_hashes: Mapping[str, str]

    @property
    def accepted(self) -> bool:
        return self.final_evaluation.status == EvaluationStatus.PASS
