from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Callable, Mapping
from typing import Any

from .models import (
    EvaluationSnapshot,
    EvaluationStatus,
    HardGateAuthority,
    MetricDelta,
    MetricGoal,
    RepairAttemptLineage,
    RepairLoopResult,
    RepairRequest,
    StopReason,
)
from .planner import build_repair_request

JsonObject = dict[str, Any]
Evaluator = Callable[[Mapping[str, Any], str, int], EvaluationSnapshot]
Repairer = Callable[[Mapping[str, Any], RepairRequest], Mapping[str, Any]]


class RepairInvariantError(RuntimeError):
    pass


def stable_hash(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sibling_hashes(siblings: Mapping[str, Mapping[str, Any]]) -> dict[str, str]:
    return {job_id: stable_hash(output) for job_id, output in sorted(siblings.items())}


def _assert_hard_gates_reexecuted(before: EvaluationSnapshot, after: EvaluationSnapshot) -> None:
    before_by_authority = {gate.authority: gate for gate in before.hard_gates}
    after_by_authority = {gate.authority: gate for gate in after.hard_gates}
    for authority in HardGateAuthority:
        if before_by_authority[authority].run_id == after_by_authority[authority].run_id:
            raise RepairInvariantError(f"hard gate {authority.value} was not re-executed after repair")


def _metric_deltas(before: EvaluationSnapshot, after: EvaluationSnapshot) -> tuple[MetricDelta, ...]:
    before_metrics = before.metric_map()
    after_metrics = after.metric_map()
    deltas: list[MetricDelta] = []
    for name in sorted(before_metrics.keys() & after_metrics.keys()):
        left = before_metrics[name]
        right = after_metrics[name]
        if left.goal != right.goal:
            raise RepairInvariantError(f"metric goal changed across repair: {name}")
        raw_delta = right.value - left.value
        signed = raw_delta if left.goal == MetricGoal.MAXIMIZE else -raw_delta
        deltas.append(
            MetricDelta(
                name=name,
                before=left.value,
                after=right.value,
                signed_improvement=round(signed, 12),
            )
        )
    return tuple(deltas)


def _hard_gate_regressions(before: EvaluationSnapshot, after: EvaluationSnapshot) -> tuple[str, ...]:
    before_map = {gate.authority: gate for gate in before.hard_gates}
    regressions: list[str] = []
    for gate in after.hard_gates:
        old = before_map[gate.authority]
        if old.status == EvaluationStatus.PASS and gate.status != EvaluationStatus.PASS:
            regressions.append(f"{gate.authority.value}:{gate.code}")
        elif old.status == EvaluationStatus.REVIEW_REQUIRED and gate.status == EvaluationStatus.FAIL:
            regressions.append(f"{gate.authority.value}:{gate.code}")
    return tuple(regressions)


class TargetedRepairLoop:
    def __init__(self, *, max_attempts: int = 2, stop_on_no_improvement: bool = True) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        self.max_attempts = max_attempts
        self.stop_on_no_improvement = stop_on_no_improvement

    def run(
        self,
        *,
        job_id: str,
        failed_output: Mapping[str, Any],
        accepted_siblings: Mapping[str, Mapping[str, Any]],
        evaluator: Evaluator,
        repairer: Repairer,
    ) -> RepairLoopResult:
        sibling_hashes = _sibling_hashes(accepted_siblings)
        current_output: JsonObject = copy.deepcopy(dict(failed_output))
        current_eval = evaluator(current_output, job_id, 0)

        if current_eval.status == EvaluationStatus.PASS:
            return RepairLoopResult(
                job_id=job_id,
                final_output=current_output,
                final_evaluation=current_eval,
                attempts=(),
                stop_reason=StopReason.ALREADY_ACCEPTED,
                accepted_sibling_hashes=sibling_hashes,
            )

        attempts: list[RepairAttemptLineage] = []
        for attempt_number in range(1, self.max_attempts + 1):
            request = build_repair_request(
                job_id=job_id,
                attempt_number=attempt_number,
                snapshot=current_eval,
            )
            if not request.actionable:
                return RepairLoopResult(
                    job_id=job_id,
                    final_output=current_output,
                    final_evaluation=current_eval,
                    attempts=tuple(attempts),
                    stop_reason=StopReason.NO_LOCAL_REPAIR_AVAILABLE,
                    accepted_sibling_hashes=sibling_hashes,
                )

            before_hash = stable_hash(current_output)
            before_eval = current_eval
            repaired = copy.deepcopy(dict(repairer(copy.deepcopy(current_output), request)))

            sibling_hashes_after = _sibling_hashes(accepted_siblings)
            if sibling_hashes_after != sibling_hashes:
                raise RepairInvariantError("accepted sibling output mutated during branch-local repair")

            after_eval = evaluator(repaired, job_id, attempt_number)
            _assert_hard_gates_reexecuted(before_eval, after_eval)

            before_codes = set(before_eval.failure_codes)
            after_codes = set(after_eval.failure_codes)
            lineage = RepairAttemptLineage(
                attempt_number=attempt_number,
                job_id=job_id,
                request=request,
                before_evaluation=before_eval,
                after_evaluation=after_eval,
                before_output_hash=before_hash,
                after_output_hash=stable_hash(repaired),
                sibling_hashes_before=dict(sibling_hashes),
                sibling_hashes_after=dict(sibling_hashes_after),
                metric_deltas=_metric_deltas(before_eval, after_eval),
                resolved_failure_codes=tuple(sorted(before_codes - after_codes)),
                introduced_failure_codes=tuple(sorted(after_codes - before_codes)),
                hard_gate_regressions=_hard_gate_regressions(before_eval, after_eval),
            )
            attempts.append(lineage)
            current_output = repaired
            current_eval = after_eval

            if lineage.hard_gate_regressions:
                return RepairLoopResult(
                    job_id=job_id,
                    final_output=current_output,
                    final_evaluation=current_eval,
                    attempts=tuple(attempts),
                    stop_reason=StopReason.HARD_GATE_REGRESSION,
                    accepted_sibling_hashes=sibling_hashes,
                )

            if current_eval.status == EvaluationStatus.PASS:
                return RepairLoopResult(
                    job_id=job_id,
                    final_output=current_output,
                    final_evaluation=current_eval,
                    attempts=tuple(attempts),
                    stop_reason=StopReason.ACCEPTED_AFTER_REEVALUATION,
                    accepted_sibling_hashes=sibling_hashes,
                )

            if self.stop_on_no_improvement and not lineage.measurable_improvement:
                return RepairLoopResult(
                    job_id=job_id,
                    final_output=current_output,
                    final_evaluation=current_eval,
                    attempts=tuple(attempts),
                    stop_reason=StopReason.NO_MEASURABLE_IMPROVEMENT,
                    accepted_sibling_hashes=sibling_hashes,
                )

        return RepairLoopResult(
            job_id=job_id,
            final_output=current_output,
            final_evaluation=current_eval,
            attempts=tuple(attempts),
            stop_reason=StopReason.MAX_ATTEMPTS_REACHED,
            accepted_sibling_hashes=sibling_hashes,
        )
