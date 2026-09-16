from __future__ import annotations

import copy
import unittest
from types import SimpleNamespace

from suno_content.repair import (
    EvaluationSnapshot,
    EvaluationStatus,
    HardGateAuthority,
    HardGateRun,
    MetricGoal,
    MetricObservation,
    RepairInvariantError,
    StopReason,
    TargetedRepairLoop,
    snapshot_from_hybrid_decision,
)


def snapshot(
    evaluation_number: int,
    *,
    factual: EvaluationStatus = EvaluationStatus.PASS,
    policy: EvaluationStatus = EvaluationStatus.PASS,
    source: EvaluationStatus = EvaluationStatus.PASS,
    failures: tuple[str, ...] = (),
    recall: float = 1.0,
    jargon: float = 0.0,
) -> EvaluationSnapshot:
    status = (
        EvaluationStatus.PASS
        if source == factual == policy == EvaluationStatus.PASS and not failures
        else EvaluationStatus.FAIL
    )
    return EvaluationSnapshot(
        evaluation_id=f"eval-{evaluation_number}",
        evaluator_version="controlled-v1",
        status=status,
        hard_gates=(
            HardGateRun(HardGateAuthority.SOURCE, source, "SOURCE_OK" if source == EvaluationStatus.PASS else "SOURCE_MISMATCH", f"source-{evaluation_number}"),
            HardGateRun(HardGateAuthority.DETERMINISTIC_FACTUAL, factual, "FACTUAL_OK" if factual == EvaluationStatus.PASS else "FACTUAL_VALUE_MISMATCH", f"factual-{evaluation_number}"),
            HardGateRun(HardGateAuthority.POLICY, policy, "POLICY_OK" if policy == EvaluationStatus.PASS else "POLICY_NEW_RECOMMENDATION", f"policy-{evaluation_number}"),
        ),
        failure_codes=failures,
        metrics=(
            MetricObservation("required_concept_recall", recall, MetricGoal.MAXIMIZE, target=1.0, violated=recall < 1.0),
            MetricObservation("unexplained_jargon_rate", jargon, MetricGoal.MINIMIZE, target=0.0, violated=jargon > 0.0),
        ),
    )


class TargetedRepairTests(unittest.TestCase):
    def test_fail_feedback_repair_reeval_preserves_siblings(self) -> None:
        evaluations: list[int] = []
        siblings = {
            "beginner:post": {"text": "accepted beginner post"},
            "advanced:video": {"text": "accepted advanced video"},
        }

        def evaluator(output, job_id, evaluation_number):
            self.assertEqual(job_id, "beginner:carousel")
            evaluations.append(evaluation_number)
            if output["text"] == "Receita foi R$ 20 bi. EBITDA.":
                return snapshot(
                    evaluation_number,
                    factual=EvaluationStatus.FAIL,
                    failures=("FACTUAL_VALUE_MISMATCH", "REQUIRED_CONCEPT_OMISSION", "UNEXPLAINED_JARGON"),
                    recall=0.5,
                    jargon=1.0,
                )
            return snapshot(evaluation_number, recall=1.0, jargon=0.0)

        def repairer(output, request):
            operations = {directive.operation for directive in request.directives if directive.repairable}
            self.assertIn("CORRECT_FACTUAL_CLAIM_FROM_SOURCE", operations)
            self.assertIn("RESTORE_REQUIRED_CONCEPTS", operations)
            self.assertIn("EXPLAIN_FIRST_USE", operations)
            self.assertEqual(request.failure_codes[0], "FACTUAL_VALUE_MISMATCH")
            output["text"] = (
                "Receita foi R$ 10 bi. EBITDA é o lucro operacional antes de juros, impostos, "
                "depreciação e amortização; aqui ele ajuda a comparar a operação."
            )
            return output

        before_siblings = copy.deepcopy(siblings)
        result = TargetedRepairLoop(max_attempts=2).run(
            job_id="beginner:carousel",
            failed_output={"text": "Receita foi R$ 20 bi. EBITDA."},
            accepted_siblings=siblings,
            evaluator=evaluator,
            repairer=repairer,
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.stop_reason, StopReason.ACCEPTED_AFTER_REEVALUATION)
        self.assertEqual(evaluations, [0, 1])
        self.assertEqual(siblings, before_siblings)
        self.assertEqual(len(result.attempts), 1)
        lineage = result.attempts[0]
        self.assertEqual(lineage.sibling_hashes_before, lineage.sibling_hashes_after)
        self.assertIn("FACTUAL_VALUE_MISMATCH", lineage.resolved_failure_codes)
        deltas = {delta.name: delta.signed_improvement for delta in lineage.metric_deltas}
        self.assertGreater(deltas["required_concept_recall"], 0)
        self.assertGreater(deltas["unexplained_jargon_rate"], 0)

    def test_policy_hard_fail_cannot_be_compensated_by_soft_metrics(self) -> None:
        def evaluator(output, _job_id, evaluation_number):
            if evaluation_number == 0:
                return snapshot(
                    evaluation_number,
                    policy=EvaluationStatus.FAIL,
                    failures=("POLICY_NEW_RECOMMENDATION", "UNEXPLAINED_JARGON"),
                    jargon=1.0,
                )
            return snapshot(
                evaluation_number,
                policy=EvaluationStatus.FAIL,
                failures=("POLICY_NEW_RECOMMENDATION",),
                jargon=0.0,
            )

        def repairer(output, _request):
            output["text"] = "Cleaner text that still adds a new recommendation."
            return output

        result = TargetedRepairLoop(max_attempts=1).run(
            job_id="intermediate:post",
            failed_output={"text": "bad"},
            accepted_siblings={},
            evaluator=evaluator,
            repairer=repairer,
        )
        self.assertFalse(result.accepted)
        self.assertEqual(result.stop_reason, StopReason.MAX_ATTEMPTS_REACHED)
        self.assertEqual(result.final_evaluation.hard_fail_codes, ("POLICY_NEW_RECOMMENDATION",))
        self.assertTrue(result.attempts[0].measurable_improvement)

    def test_unrepairable_retrieval_miss_stops_without_rewrite(self) -> None:
        calls = 0

        def evaluator(_output, _job_id, evaluation_number):
            return snapshot(evaluation_number, failures=("RETRIEVAL_MISS",))

        def repairer(output, _request):
            nonlocal calls
            calls += 1
            return output

        result = TargetedRepairLoop().run(
            job_id="advanced:video",
            failed_output={"text": "claim"},
            accepted_siblings={},
            evaluator=evaluator,
            repairer=repairer,
        )
        self.assertEqual(calls, 0)
        self.assertEqual(result.stop_reason, StopReason.NO_LOCAL_REPAIR_AVAILABLE)

    def test_detects_accepted_sibling_mutation(self) -> None:
        siblings = {"accepted:1": {"text": "keep me"}}

        def evaluator(_output, _job_id, evaluation_number):
            return snapshot(evaluation_number, failures=("REQUIRED_CONCEPT_OMISSION",), recall=0.0)

        def repairer(output, _request):
            siblings["accepted:1"]["text"] = "mutated"
            output["text"] = "repair"
            return output

        with self.assertRaisesRegex(RepairInvariantError, "accepted sibling output mutated"):
            TargetedRepairLoop(max_attempts=1).run(
                job_id="failed:1",
                failed_output={"text": "bad"},
                accepted_siblings=siblings,
                evaluator=evaluator,
                repairer=repairer,
            )

    def test_requires_new_hard_gate_run_ids_after_repair(self) -> None:
        def evaluator(_output, _job_id, evaluation_number):
            base = snapshot(evaluation_number, failures=("REQUIRED_CONCEPT_OMISSION",), recall=0.0)
            if evaluation_number == 0:
                return base
            return EvaluationSnapshot(
                evaluation_id="eval-1",
                evaluator_version=base.evaluator_version,
                status=EvaluationStatus.FAIL,
                hard_gates=tuple(
                    HardGateRun(gate.authority, gate.status, gate.code, gate.run_id.replace("-1", "-0"))
                    for gate in base.hard_gates
                ),
                failure_codes=base.failure_codes,
                metrics=base.metrics,
            )

        with self.assertRaisesRegex(RepairInvariantError, "was not re-executed"):
            TargetedRepairLoop(max_attempts=1).run(
                job_id="failed:1",
                failed_output={"text": "bad"},
                accepted_siblings={},
                evaluator=evaluator,
                repairer=lambda output, _request: output,
            )

    def test_records_metric_regression_and_new_failure_code(self) -> None:
        def evaluator(_output, _job_id, evaluation_number):
            if evaluation_number == 0:
                return snapshot(evaluation_number, failures=("REQUIRED_CONCEPT_OMISSION",), recall=0.0, jargon=0.0)
            return snapshot(evaluation_number, failures=("UNEXPLAINED_JARGON",), recall=1.0, jargon=1.0)

        result = TargetedRepairLoop(max_attempts=1).run(
            job_id="beginner:post",
            failed_output={"text": "bad"},
            accepted_siblings={},
            evaluator=evaluator,
            repairer=lambda output, _request: {"text": output["text"] + " repaired"},
        )
        lineage = result.attempts[0]
        self.assertIn("REQUIRED_CONCEPT_OMISSION", lineage.resolved_failure_codes)
        self.assertIn("UNEXPLAINED_JARGON", lineage.introduced_failure_codes)
        self.assertTrue(lineage.has_regression)
        jargon_delta = next(delta for delta in lineage.metric_deltas if delta.name == "unexplained_jargon_rate")
        self.assertLess(jargon_delta.signed_improvement, 0)

    def test_hybrid_adapter_requires_and_preserves_three_canonical_hard_gates(self) -> None:
        decision = SimpleNamespace(
            evaluator_version="hybrid-v1",
            status=SimpleNamespace(value="FAIL"),
            gates=(
                SimpleNamespace(authority=SimpleNamespace(value="SOURCE"), status=SimpleNamespace(value="PASS"), code="SOURCE_OK"),
                SimpleNamespace(authority=SimpleNamespace(value="DETERMINISTIC_FACTUAL"), status=SimpleNamespace(value="FAIL"), code="FACTUAL_VALUE_MISMATCH"),
                SimpleNamespace(authority=SimpleNamespace(value="POLICY"), status=SimpleNamespace(value="PASS"), code="POLICY_OK"),
            ),
            claim_findings=(),
        )
        adapted = snapshot_from_hybrid_decision(
            decision,
            evaluation_id="hybrid-eval-1",
            gate_run_ids={
                "SOURCE": "source-run-1",
                "DETERMINISTIC_FACTUAL": "factual-run-1",
                "POLICY": "policy-run-1",
            },
        )
        self.assertEqual(adapted.hard_fail_codes, ("FACTUAL_VALUE_MISMATCH",))
        self.assertIn("FACTUAL_VALUE_MISMATCH", adapted.failure_codes)

        with self.assertRaisesRegex(ValueError, "missing hard-gate run ids"):
            snapshot_from_hybrid_decision(
                decision,
                evaluation_id="hybrid-eval-2",
                gate_run_ids={"SOURCE": "s", "DETERMINISTIC_FACTUAL": "f"},
            )


if __name__ == "__main__":
    unittest.main()
