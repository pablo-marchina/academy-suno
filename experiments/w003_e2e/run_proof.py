#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.domain import AudienceLevel, GateStatus, OutputFormat  # noqa: E402
from suno_content.evals.audience import evaluate_audience_features, load_ontology  # noqa: E402
from suno_content.grounding import hybrid_decision  # noqa: E402
from suno_content.orchestration import (  # noqa: E402
    AsyncGraphOrchestrator,
    EvaluationAction,
    JobSpec,
    QualityDecision,
    RunPhase,
)
from suno_content.repair import (  # noqa: E402
    EvaluationSnapshot,
    EvaluationStatus,
    HardGateAuthority,
    HardGateRun,
    MetricGoal,
    MetricObservation,
    build_repair_request,
    stable_hash,
)
from suno_content.runstore import SQLiteRunStore  # noqa: E402
from suno_content.telemetry import (  # noqa: E402
    InMemoryTelemetrySink,
    OrchestrationTelemetryHooks,
    TelemetryRecorder,
    summarize,
)

RUN_ID = "w003-t009-e2e-v001"
SOURCE_HASH = "9" * 64
SOURCE_VALUE_BRL_BILLION = 18.7
REPAIR_JOB_ID = "beginner:carousel"
RETRY_JOB_ID = "advanced:short_video"
REQUIRED_CONCEPTS = ("corp:ebitda", "corp:capex")
GOOD_TEXT = (
    "A companhia reportou receita de R$ 18,7 bi. "
    "EBITDA é uma medida do resultado operacional antes de juros, impostos, depreciação e amortização; "
    "na prática, ajuda a observar a operação. "
    "CAPEX significa investimentos em ativos e projetos de longo prazo."
)
BAD_TEXT = "Receita foi R$ 20 bi. EBITDA."


def _snapshot_dict(snapshot: EvaluationSnapshot) -> dict[str, Any]:
    return {
        "evaluation_id": snapshot.evaluation_id,
        "evaluator_version": snapshot.evaluator_version,
        "status": snapshot.status.value,
        "failure_codes": list(snapshot.failure_codes),
        "hard_gates": [
            {
                "authority": gate.authority.value,
                "status": gate.status.value,
                "code": gate.code,
                "run_id": gate.run_id,
            }
            for gate in snapshot.hard_gates
        ],
        "metrics": [
            {
                "name": metric.name,
                "value": metric.value,
                "goal": metric.goal.value,
                "target": metric.target,
                "violated": metric.violated,
            }
            for metric in snapshot.metrics
        ],
        "diagnostics": snapshot.diagnostics,
    }


def _request_dict(request: Any) -> dict[str, Any]:
    return {
        "job_id": request.job_id,
        "attempt_number": request.attempt_number,
        "before_evaluation_id": request.before_evaluation_id,
        "failure_codes": list(request.failure_codes),
        "metric_triggers": list(request.metric_triggers),
        "directives": [asdict(item) for item in request.directives],
        "actionable": request.actionable,
    }


class ProofRuntime:
    """Deterministic mechanics provider composed with the integrated W003 runtime."""

    def __init__(self) -> None:
        self.ontology = load_ontology(ROOT / "data" / "ontology" / "finance_ptbr_v001.json")
        self.generation_calls: dict[str, int] = {}
        self.evaluation_calls: dict[str, int] = {}
        self.snapshots: dict[str, list[EvaluationSnapshot]] = {}
        self.accepted_outputs: dict[str, dict[str, Any]] = {}
        self.pending_repairs: dict[str, dict[str, Any]] = {}
        self.repair_lineage: dict[str, list[dict[str, Any]]] = {}

    @staticmethod
    def planner(source: dict[str, Any]) -> tuple[JobSpec, ...]:
        del source
        audiences = (
            ("beginner", AudienceLevel.BEGINNER),
            ("intermediate", AudienceLevel.INTERMEDIATE),
            ("advanced", AudienceLevel.ADVANCED),
        )
        formats = (
            ("article", OutputFormat.ARTICLE),
            ("carousel", OutputFormat.CAROUSEL),
            ("short_video", OutputFormat.SHORT_VIDEO),
        )
        return tuple(
            JobSpec(
                job_id=f"{audience_slug}:{format_slug}",
                payload={"audience": audience.value, "format": output_format.value},
            )
            for audience_slug, audience in audiences
            for format_slug, output_format in formats
        )

    def generator(self, job: JobSpec, source: dict[str, Any]) -> dict[str, Any]:
        call = self.generation_calls.get(job.job_id, 0) + 1
        self.generation_calls[job.job_id] = call
        if job.job_id == RETRY_JOB_ID and call == 1:
            raise TimeoutError("controlled transport timeout for retry lineage proof")

        bad = job.job_id == REPAIR_JOB_ID
        return {
            "job_id": job.job_id,
            "audience": job.payload["audience"],
            "format": job.payload["format"],
            "source_id": source["source_id"],
            "source_hash": source["source_hash"],
            "claimed_value_brl_billion": 20.0 if bad else SOURCE_VALUE_BRL_BILLION,
            "text": BAD_TEXT if bad else GOOD_TEXT,
            "provider_mode": "deterministic_stub",
            "evidence_scope": "MECHANICS_ONLY",
        }

    def _make_snapshot(self, job: JobSpec, output: Mapping[str, Any], *, call: int) -> EvaluationSnapshot:
        audience = AudienceLevel(str(job.payload["audience"]))
        output_format = OutputFormat(str(job.payload["format"]))
        vector = evaluate_audience_features(
            str(output["text"]),
            audience=audience,
            output_format=output_format,
            ontology=self.ontology,
            required_concept_ids=REQUIRED_CONCEPTS,
        )

        source_status = GateStatus.PASS if output.get("source_hash") == SOURCE_HASH else GateStatus.FAIL
        factual_status = (
            GateStatus.PASS
            if float(output.get("claimed_value_brl_billion", -1.0)) == SOURCE_VALUE_BRL_BILLION
            else GateStatus.FAIL
        )
        policy_status = GateStatus.FAIL if bool(output.get("prohibited_recommendation")) else GateStatus.PASS
        decision = hybrid_decision(
            (),
            {},
            source_status=source_status,
            factual_status=factual_status,
            policy_status=policy_status,
            semantic_adapter=None,
        )

        hard_gate_codes = {
            HardGateAuthority.SOURCE: "SOURCE_LINEAGE_MISMATCH",
            HardGateAuthority.DETERMINISTIC_FACTUAL: "FACTUAL_VALUE_MISMATCH",
            HardGateAuthority.POLICY: "POLICY_UNSUPPORTED_RECOMMENDATION",
        }
        decision_gates = {
            str(gate.authority.value): EvaluationStatus(str(gate.status.value))
            for gate in decision.gates
        }
        hard_gates = tuple(
            HardGateRun(
                authority=authority,
                status=decision_gates[authority.value],
                code=hard_gate_codes[authority],
                run_id=f"{authority.value.lower()}:{job.job_id}:{call}",
            )
            for authority in HardGateAuthority
        )

        failure_codes: list[str] = [
            gate.code for gate in hard_gates if gate.status != EvaluationStatus.PASS
        ]
        failure_codes.extend(vector.anti_gaming.flags)
        jargon_rate = vector.terminology.unexplained_jargon_rate
        if jargon_rate is not None and jargon_rate > 0.0:
            failure_codes.append("UNEXPLAINED_JARGON")
        failure_codes = list(dict.fromkeys(failure_codes))

        metrics: list[MetricObservation] = []
        recall = vector.terminology.required_concept_recall
        if recall is not None:
            metrics.append(
                MetricObservation(
                    name="required_concept_recall",
                    value=float(recall),
                    goal=MetricGoal.MAXIMIZE,
                    target=1.0,
                    violated=recall < 1.0,
                )
            )
        if jargon_rate is not None:
            metrics.append(
                MetricObservation(
                    name="unexplained_jargon_rate",
                    value=float(jargon_rate),
                    goal=MetricGoal.MINIMIZE,
                    target=0.0,
                    violated=jargon_rate > 0.0,
                )
            )

        if any(gate.status == EvaluationStatus.FAIL for gate in hard_gates):
            status = EvaluationStatus.FAIL
        elif any(gate.status == EvaluationStatus.REVIEW_REQUIRED for gate in hard_gates):
            status = EvaluationStatus.REVIEW_REQUIRED
        elif failure_codes:
            status = EvaluationStatus.FAIL
        else:
            status = EvaluationStatus.PASS

        return EvaluationSnapshot(
            evaluation_id=f"eval:{job.job_id}:{call}",
            evaluator_version=str(decision.evaluator_version),
            status=status,
            hard_gates=hard_gates,
            failure_codes=tuple(failure_codes),
            metrics=tuple(metrics),
            diagnostics={
                "grounding_status": str(decision.status.value),
                "semantic_enabled": bool(decision.semantic_enabled),
                "audience_threshold_mode": vector.threshold_mode,
                "audience_vector": vector.model_dump(mode="json"),
            },
        )

    def evaluator(self, job: JobSpec, output: Mapping[str, Any]) -> QualityDecision:
        call = self.evaluation_calls.get(job.job_id, 0) + 1
        self.evaluation_calls[job.job_id] = call
        snapshot = self._make_snapshot(job, output, call=call)
        self.snapshots.setdefault(job.job_id, []).append(snapshot)

        pending = self.pending_repairs.pop(job.job_id, None)
        if pending is not None:
            before = pending["before_snapshot"]
            before_codes = set(before.failure_codes)
            after_codes = set(snapshot.failure_codes)
            before_gate_ids = {gate.authority.value: gate.run_id for gate in before.hard_gates}
            after_gate_ids = {gate.authority.value: gate.run_id for gate in snapshot.hard_gates}
            pending.pop("before_snapshot", None)
            pending.update(
                {
                    "after_snapshot": _snapshot_dict(snapshot),
                    "after_output_hash": stable_hash(dict(output)),
                    "resolved_failure_codes": sorted(before_codes - after_codes),
                    "introduced_failure_codes": sorted(after_codes - before_codes),
                    "hard_gate_run_ids_before": before_gate_ids,
                    "hard_gate_run_ids_after": after_gate_ids,
                    "fresh_hard_gate_runs": all(
                        before_gate_ids[key] != after_gate_ids[key] for key in before_gate_ids
                    ),
                }
            )
            self.repair_lineage.setdefault(job.job_id, []).append(pending)

        if snapshot.status == EvaluationStatus.PASS:
            self.accepted_outputs[job.job_id] = dict(output)
            return QualityDecision(EvaluationAction.PASS, metadata={"evaluation": _snapshot_dict(snapshot)})

        request = build_repair_request(job_id=job.job_id, attempt_number=call, snapshot=snapshot)
        action = EvaluationAction.REPAIR if request.actionable else EvaluationAction.FAIL
        return QualityDecision(
            action,
            reasons=snapshot.failure_codes,
            metadata={"evaluation": _snapshot_dict(snapshot), "repair_actionable": request.actionable},
        )

    def repairer(
        self,
        job: JobSpec,
        output: Mapping[str, Any],
        decision: QualityDecision,
        repair_attempt: int,
    ) -> dict[str, Any]:
        del decision
        before_snapshot = self.snapshots[job.job_id][-1]
        request = build_repair_request(
            job_id=job.job_id,
            attempt_number=repair_attempt,
            snapshot=before_snapshot,
        )
        if not request.actionable:
            raise RuntimeError("controlled repair unexpectedly has no actionable directives")

        sibling_hashes_before = {
            sibling_id: stable_hash(sibling)
            for sibling_id, sibling in sorted(self.accepted_outputs.items())
            if sibling_id != job.job_id
        }
        repaired = dict(output)
        repaired.update(
            {
                "claimed_value_brl_billion": SOURCE_VALUE_BRL_BILLION,
                "text": GOOD_TEXT,
                "repair_attempt": repair_attempt,
                "repair_operations": [item.operation for item in request.directives if item.repairable],
            }
        )
        sibling_hashes_after = {
            sibling_id: stable_hash(sibling)
            for sibling_id, sibling in sorted(self.accepted_outputs.items())
            if sibling_id != job.job_id
        }
        if sibling_hashes_before != sibling_hashes_after:
            raise RuntimeError("accepted sibling mutated during controlled branch-local repair")

        self.pending_repairs[job.job_id] = {
            "attempt_number": repair_attempt,
            "job_id": job.job_id,
            "request": _request_dict(request),
            "before_snapshot": before_snapshot,
            "before_snapshot_serialized": _snapshot_dict(before_snapshot),
            "before_output_hash": stable_hash(dict(output)),
            "accepted_sibling_hashes_before": sibling_hashes_before,
            "accepted_sibling_hashes_after": sibling_hashes_after,
            "siblings_immutable": sibling_hashes_before == sibling_hashes_after,
        }
        return repaired

    @staticmethod
    def aggregator(outputs: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
        return {
            "job_count": len(outputs),
            "job_ids": sorted(outputs),
            "provider_mode": "deterministic_stub",
            "evidence_scope": "MECHANICS_ONLY",
        }

    def non_compensation_probe(self) -> dict[str, Any]:
        job = JobSpec(
            "probe:hard-gate",
            {"audience": AudienceLevel.BEGINNER.value, "format": OutputFormat.ARTICLE.value},
        )
        output = {"text": GOOD_TEXT, "source_hash": SOURCE_HASH, "claimed_value_brl_billion": 20.0}
        snapshot = self._make_snapshot(job, output, call=1)
        audience = snapshot.diagnostics["audience_vector"]["terminology"]
        return {
            "status": snapshot.status.value,
            "failure_codes": list(snapshot.failure_codes),
            "factual_hard_gate": next(
                gate.status.value
                for gate in snapshot.hard_gates
                if gate.authority == HardGateAuthority.DETERMINISTIC_FACTUAL
            ),
            "required_concept_recall": audience["required_concept_recall"],
            "unexplained_jargon_rate": audience["unexplained_jargon_rate"],
            "soft_signal_masked_hard_fail": snapshot.status == EvaluationStatus.PASS,
        }


def _history_payload(store: SQLiteRunStore, run_id: str) -> list[dict[str, Any]]:
    return [
        {"sequence": item.sequence, "reason": item.reason, "created_at": item.created_at, "state": item.state}
        for item in store.history(run_id)
    ]


def execute_proof(output_dir: Path | None = None) -> dict[str, Any]:
    runtime = ProofRuntime()
    sink = InMemoryTelemetrySink()
    recorder = TelemetryRecorder(run_id=RUN_ID, sink=sink)
    hooks = OrchestrationTelemetryHooks(recorder)
    callbacks = {
        "planner": hooks.planner(runtime.planner),
        "generator": hooks.generator(runtime.generator),
        "evaluator": hooks.evaluator(runtime.evaluator),
        "repairer": hooks.repairer(runtime.repairer),
        "aggregator": hooks.aggregator(runtime.aggregator),
    }

    source = {
        "source_id": "w003-e2e-controlled-source-v001",
        "source_hash": SOURCE_HASH,
        "canonical_value_brl_billion": SOURCE_VALUE_BRL_BILLION,
        "evidence_scope": "MECHANICS_ONLY",
    }

    with tempfile.TemporaryDirectory(prefix="w003-t009-") as temp_dir:
        db_path = Path(temp_dir) / "runstore.sqlite3"
        store = SQLiteRunStore(db_path)
        orchestrator = AsyncGraphOrchestrator(
            store=store,
            transport_retry_limit=1,
            max_quality_repairs=1,
            **callbacks,
        )
        paused = asyncio.run(
            orchestrator.start(
                run_id=RUN_ID,
                source=source,
                metadata={"provider_mode": "deterministic_stub", "evidence_scope": "MECHANICS_ONLY"},
                pause_after="branches",
            )
        )
        hooks.observe_state(paused)
        calls_before_resume = dict(runtime.generation_calls)
        history_before_resume = _history_payload(store, RUN_ID)

        reopened = SQLiteRunStore(db_path)
        resumed_orchestrator = AsyncGraphOrchestrator(
            store=reopened,
            transport_retry_limit=1,
            max_quality_repairs=1,
            **callbacks,
        )
        final = asyncio.run(resumed_orchestrator.resume(RUN_ID))
        hooks.observe_state(final)
        history = _history_payload(reopened, RUN_ID)

    telemetry_summary = summarize(sink.events)
    probe = runtime.non_compensation_probe()
    repair_entries = runtime.repair_lineage.get(REPAIR_JOB_ID, [])

    assert paused.phase == RunPhase.BRANCHES_COMPLETE
    assert final.phase == RunPhase.COMPLETE
    assert len(final.jobs) == 9
    assert len(final.joined_outputs) == 9
    assert len(repair_entries) == 1
    assert repair_entries[0]["fresh_hard_gate_runs"] is True
    assert repair_entries[0]["siblings_immutable"] is True
    assert runtime.generation_calls == calls_before_resume
    assert runtime.generation_calls[RETRY_JOB_ID] == 2
    assert runtime.generation_calls[REPAIR_JOB_ID] == 1
    assert final.jobs[REPAIR_JOB_ID].quality_repairs == 1
    assert telemetry_summary["transport_retries"]["total"] == 1
    assert telemetry_summary["quality_repairs"]["total"] == 1
    assert telemetry_summary["usage"] is None
    assert telemetry_summary["observed_cost"] is None
    assert probe["soft_signal_masked_hard_fail"] is False
    assert "FACTUAL_VALUE_MISMATCH" in probe["failure_codes"]

    report = {
        "schema_version": "w003.e2e.proof.v1",
        "task_id": "W003-T009",
        "attempt_id": "A01",
        "run_id": RUN_ID,
        "evidence_scope": "MECHANICS_ONLY",
        "provider_mode": "deterministic_stub",
        "provider_quality_claim": "NOT_MADE",
        "real_provider_cost_evidence": "N/A",
        "paused_phase": paused.phase.value,
        "final_phase": final.phase.value,
        "job_count": len(final.jobs),
        "joined_output_count": len(final.joined_outputs),
        "job_ids": sorted(final.jobs),
        "repair_job_id": REPAIR_JOB_ID,
        "transport_retry_job_id": RETRY_JOB_ID,
        "generation_calls": dict(sorted(runtime.generation_calls.items())),
        "evaluation_calls": dict(sorted(runtime.evaluation_calls.items())),
        "repair_lineage": repair_entries,
        "non_compensation_probe": probe,
        "runstore": {
            "history_count_before_resume": len(history_before_resume),
            "history_count_final": len(history),
            "checkpoint_reasons": [item["reason"] for item in history],
            "reopened_before_resume": True,
            "accepted_branches_regenerated_after_resume": False,
        },
        "telemetry": telemetry_summary,
        "evidence_classification": {
            "mechanics_end_to_end": "PROVEN",
            "anti_gaming_contract": "PROVEN_BY_INTEGRATED_T004_T008_EVIDENCE",
            "audience_thresholds": "DIAGNOSTIC_ONLY",
            "audience_confusion_matrices": "NOT_COMPUTABLE",
            "semantic_ablation": "NOT_RUN",
            "semantic_backend_preference": "NO_BACKEND_PREFERENCE",
            "provider_comparison": "NOT_COMPARABLE",
            "provider_preference": "NO_PREFERENCE",
            "provider_quality_latency_cost": "PRODUCTION_UNKNOWN",
            "langgraph_challenger": "PENDING_RUNTIME_RECHECK",
        },
    }

    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "proof_report_v001.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (output_dir / "runstore_history_v001.json").write_text(
            json.dumps(history, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        with (output_dir / "telemetry_events_v001.jsonl").open("w", encoding="utf-8") as handle:
            for event in sink.events:
                handle.write(json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=True))
                handle.write("\n")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute the W003 end-to-end mechanics proof")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "experiments" / "w003_e2e" / "evidence",
    )
    args = parser.parse_args()
    report = execute_proof(args.output_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
