from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .models import (
    EvaluationSnapshot,
    EvaluationStatus,
    HardGateAuthority,
    HardGateRun,
    MetricObservation,
)


def _value(value: Any) -> str:
    return str(getattr(value, "value", value))


def snapshot_from_hybrid_decision(
    decision: Any,
    *,
    evaluation_id: str,
    gate_run_ids: Mapping[str, str],
    metrics: Sequence[MetricObservation] = (),
    diagnostics: Mapping[str, Any] | None = None,
) -> EvaluationSnapshot:
    """Adapt the accepted grounding HybridDecision without taking ownership of it.

    The adapter requires SOURCE, DETERMINISTIC_FACTUAL and POLICY runs explicitly,
    so a post-repair snapshot cannot omit any canonical hard gate.
    """

    required = tuple(authority.value for authority in HardGateAuthority)
    missing_ids = [authority for authority in required if authority not in gate_run_ids]
    if missing_ids:
        raise ValueError(f"missing hard-gate run ids: {missing_ids}")

    gates_by_authority: dict[str, Any] = {}
    for gate in decision.gates:
        authority = _value(gate.authority)
        if authority in required:
            gates_by_authority[authority] = gate
    missing_gates = [authority for authority in required if authority not in gates_by_authority]
    if missing_gates:
        raise ValueError(f"HybridDecision missing required hard gates: {missing_gates}")

    hard_gates = tuple(
        HardGateRun(
            authority=HardGateAuthority(authority),
            status=EvaluationStatus(_value(gates_by_authority[authority].status)),
            code=str(gates_by_authority[authority].code),
            run_id=gate_run_ids[authority],
        )
        for authority in required
    )

    failure_codes: list[str] = []
    for gate in decision.gates:
        if _value(gate.status) != EvaluationStatus.PASS.value:
            failure_codes.append(str(gate.code))
    for finding in decision.claim_findings:
        if _value(finding.decision) == EvaluationStatus.PASS.value:
            continue
        if getattr(finding, "failure_code", None):
            failure_codes.append(str(finding.failure_code))
        elif getattr(finding, "unverifiable_reason", None):
            failure_codes.append(_value(finding.unverifiable_reason))
        elif getattr(finding, "deterministic_code", None):
            failure_codes.append(str(finding.deterministic_code))

    return EvaluationSnapshot(
        evaluation_id=evaluation_id,
        evaluator_version=str(decision.evaluator_version),
        status=EvaluationStatus(_value(decision.status)),
        hard_gates=hard_gates,
        failure_codes=tuple(dict.fromkeys(failure_codes)),
        metrics=tuple(metrics),
        diagnostics=dict(diagnostics or {}),
    )
