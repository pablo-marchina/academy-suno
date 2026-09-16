from __future__ import annotations

import json

from suno_content.repair import (
    EvaluationSnapshot,
    EvaluationStatus,
    HardGateAuthority,
    HardGateRun,
    MetricGoal,
    MetricObservation,
    TargetedRepairLoop,
)


def evaluate(output, _job_id, n):
    failing = "R$ 20 bi" in output["text"]
    failure_codes = (
        ("FACTUAL_VALUE_MISMATCH", "REQUIRED_CONCEPT_OMISSION", "UNEXPLAINED_JARGON")
        if failing
        else ()
    )
    factual_status = EvaluationStatus.FAIL if failing else EvaluationStatus.PASS
    return EvaluationSnapshot(
        evaluation_id=f"demo-eval-{n}",
        evaluator_version="controlled-repair-demo-v1",
        status=EvaluationStatus.FAIL if failing else EvaluationStatus.PASS,
        hard_gates=(
            HardGateRun(HardGateAuthority.SOURCE, EvaluationStatus.PASS, "SOURCE_OK", f"source-{n}"),
            HardGateRun(HardGateAuthority.DETERMINISTIC_FACTUAL, factual_status, "FACTUAL_VALUE_MISMATCH" if failing else "FACTUAL_OK", f"factual-{n}"),
            HardGateRun(HardGateAuthority.POLICY, EvaluationStatus.PASS, "POLICY_OK", f"policy-{n}"),
        ),
        failure_codes=failure_codes,
        metrics=(
            MetricObservation("required_concept_recall", 0.5 if failing else 1.0, MetricGoal.MAXIMIZE, 1.0, failing),
            MetricObservation("unexplained_jargon_rate", 1.0 if failing else 0.0, MetricGoal.MINIMIZE, 0.0, failing),
        ),
    )


def repair(output, request):
    output["text"] = (
        "Receita foi R$ 10 bi. EBITDA é o lucro operacional antes de juros, impostos, "
        "depreciação e amortização; na prática, ajuda a comparar a operação."
    )
    output["applied_operations"] = [
        item.operation for item in request.directives if item.repairable
    ]
    return output


def main():
    siblings = {
        "beginner:post": {"text": "accepted sibling"},
        "advanced:video": {"text": "accepted sibling"},
    }
    result = TargetedRepairLoop(max_attempts=2).run(
        job_id="beginner:carousel",
        failed_output={"text": "Receita foi R$ 20 bi. EBITDA."},
        accepted_siblings=siblings,
        evaluator=evaluate,
        repairer=repair,
    )
    attempt = result.attempts[0]
    print(json.dumps({
        "stop_reason": result.stop_reason.value,
        "accepted": result.accepted,
        "attempts": len(result.attempts),
        "before_failures": list(attempt.before_evaluation.failure_codes),
        "directives": [item.operation for item in attempt.request.directives],
        "after_failures": list(attempt.after_evaluation.failure_codes),
        "hard_gate_run_ids_before": [gate.run_id for gate in attempt.before_evaluation.hard_gates],
        "hard_gate_run_ids_after": [gate.run_id for gate in attempt.after_evaluation.hard_gates],
        "siblings_immutable": attempt.sibling_hashes_before == attempt.sibling_hashes_after,
        "metric_deltas": {item.name: item.signed_improvement for item in attempt.metric_deltas},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
