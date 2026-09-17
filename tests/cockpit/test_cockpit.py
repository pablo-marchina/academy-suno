from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from suno_content.cockpit import EvidenceState, build_cockpit_snapshot, load_run_state_from_history, render_html


class EvidenceCockpitTests(unittest.TestCase):
    def _run_state(self) -> dict:
        jobs = {}
        for audience in ("beginner", "intermediate", "advanced"):
            for output_format in ("article", "carousel", "short_video"):
                job_id = f"{audience}:{output_format}"
                phase = "accepted"
                evaluation = {"action": "pass", "reasons": [], "metadata": {}}
                error = None
                if job_id == "beginner:carousel":
                    phase = "failed"
                    evaluation = {"action": "fail", "reasons": ["FACTUAL_VALUE_MISMATCH"], "metadata": {}}
                    error = "hard factual gate failed"
                elif job_id == "advanced:short_video":
                    phase = "review_required"
                    evaluation = {"action": "review_required", "reasons": ["MANUAL_REVIEW"], "metadata": {}}
                jobs[job_id] = {
                    "job_id": job_id,
                    "payload": {"audience": audience, "format": output_format},
                    "phase": phase,
                    "output": {
                        "job_id": job_id,
                        "source_id": "source-001",
                        "source_hash": "a" * 64,
                        "text": f"output for {job_id}",
                        "provider_mode": "deterministic_stub",
                        "evidence_scope": "MECHANICS_ONLY",
                    },
                    "evaluation": evaluation,
                    "quality_repairs": 0,
                    "transport_retries": {},
                    "events": [],
                    "error": error,
                }
        return {
            "run_id": "run-001",
            "source": {
                "source_id": "source-001",
                "source_ref": "fixture://source-001",
                "source_hash": "a" * 64,
                "evidence_scope": "MECHANICS_ONLY",
            },
            "phase": "review_required",
            "jobs": jobs,
            "metadata": {"evidence_scope": "MECHANICS_ONLY"},
        }

    def _proof_report(self) -> dict:
        return {
            "run_id": "run-001",
            "evidence_scope": "MECHANICS_ONLY",
            "repair_lineage": [
                {
                    "job_id": "beginner:carousel",
                    "attempt_number": 1,
                    "before_output_hash": "before-hash",
                    "after_output_hash": "after-hash",
                    "before_snapshot_serialized": {"status": "FAIL", "failure_codes": ["FACTUAL_VALUE_MISMATCH"]},
                    "after_snapshot": {"status": "PASS", "failure_codes": []},
                    "resolved_failure_codes": ["FACTUAL_VALUE_MISMATCH"],
                    "introduced_failure_codes": [],
                    "fresh_hard_gate_runs": True,
                    "siblings_immutable": True,
                }
            ],
            "evidence_classification": {
                "mechanics_end_to_end": "PROVEN",
                "audience_thresholds": "DIAGNOSTIC_ONLY",
                "audience_confusion_matrices": "NOT_COMPUTABLE",
                "semantic_ablation": "NOT_RUN",
                "provider_comparison": "NOT_COMPARABLE",
                "provider_quality_latency_cost": "PRODUCTION_UNKNOWN",
            },
        }

    def _telemetry(self) -> dict:
        return {
            "run_id": "run-001",
            "event_count": 12,
            "stage_latency": {"generate": {"count": 9, "mean_ns": 100, "p50_ns": 90, "p95_ns": 150}},
            "transport_retries": {"total": 1, "by_stage_job": []},
            "quality_repairs": {"total": 1, "by_job": []},
            "usage": {"observed_event_count": 1, "quantities": {"input_tokens": "10"}},
            "observed_cost": [{"amount": "0.01", "currency": "USD", "pricing_version": "synthetic.v1"}],
            "terminal": {
                "run_phase": "review_required",
                "branch_states": {},
                "failed_job_ids": ["beginner:carousel"],
                "review_required_job_ids": ["advanced:short_video"],
            },
        }

    def _calibration(self) -> dict:
        return {
            "audience_rows": [],
            "independent_agreement": None,
            "anti_gaming_cases": [{"case_id": "jargon_stuffing"}],
            "semantic_rows": [],
            "provider_rows": [
                {
                    "candidate_id": "run-001",
                    "pricing_provenance": "SYNTHETIC",
                    "quality_observed": False,
                    "latency_observed": True,
                }
            ],
        }

    def test_required_states_are_explicit(self) -> None:
        self.assertEqual(
            {state.value for state in EvidenceState},
            {
                "PROVEN",
                "DIAGNOSTIC_ONLY",
                "NOT_COMPUTABLE",
                "NOT_RUN",
                "NOT_COMPARABLE",
                "PRODUCTION_UNKNOWN",
                "FAIL",
                "REVIEW_REQUIRED",
            },
        )

    def test_snapshot_preserves_grid_failures_unknowns_and_provenance(self) -> None:
        events = (
            {"job_id": "advanced:short_video", "operation_attempt": 1},
            {"job_id": "advanced:short_video", "operation_attempt": 2},
        )
        snapshot = build_cockpit_snapshot(
            run_state=self._run_state(),
            telemetry_summary=self._telemetry(),
            telemetry_events=events,
            calibration=self._calibration(),
            proof_report=self._proof_report(),
            task_attempt_id="W004-T001-A01",
            artifact_refs={
                "runstore": "runstore_history_v001.json",
                "proof_report": "proof_report_v001.json",
                "telemetry": "telemetry_summary.json",
                "calibration": "current_evidence_v001.json",
            },
        )
        self.assertEqual(len(snapshot.jobs), 9)
        by_id = {job.job_id: job for job in snapshot.jobs if job.job_id is not None}
        self.assertIs(by_id["beginner:carousel"].state, EvidenceState.FAIL)
        self.assertIs(by_id["advanced:short_video"].state, EvidenceState.REVIEW_REQUIRED)
        self.assertEqual(by_id["advanced:short_video"].provenance.attempt, 2)
        self.assertEqual(by_id["beginner:article"].provenance.source_id, "source-001")
        self.assertEqual(by_id["beginner:article"].provenance.run_id, "run-001")
        self.assertEqual(by_id["beginner:article"].provenance.job_id, "beginner:article")
        self.assertEqual(by_id["beginner:article"].provenance.evidence_scope, "MECHANICS_ONLY")
        self.assertTrue(snapshot.has_failures)
        self.assertTrue(snapshot.needs_review)

        states = {item.state for item in snapshot.evidence_items}
        self.assertTrue(
            {
                EvidenceState.PROVEN,
                EvidenceState.DIAGNOSTIC_ONLY,
                EvidenceState.NOT_COMPUTABLE,
                EvidenceState.NOT_RUN,
                EvidenceState.NOT_COMPARABLE,
                EvidenceState.PRODUCTION_UNKNOWN,
            }.issubset(states)
        )

    def test_synthetic_cost_is_visible_but_not_promoted_to_provider_cost_evidence(self) -> None:
        snapshot = build_cockpit_snapshot(
            run_state=self._run_state(),
            telemetry_summary=self._telemetry(),
            calibration=self._calibration(),
        )
        self.assertIsNotNone(snapshot.telemetry)
        assert snapshot.telemetry is not None
        self.assertIsNone(snapshot.telemetry.observed_cost)
        self.assertIsNotNone(snapshot.telemetry.raw_observed_cost)
        self.assertIs(snapshot.telemetry.cost_evidence_state, EvidenceState.DIAGNOSTIC_ONLY)

    def test_repair_lineage_and_html_keep_before_after_and_no_green_aggregate(self) -> None:
        snapshot = build_cockpit_snapshot(
            run_state=self._run_state(),
            telemetry_summary=self._telemetry(),
            calibration=self._calibration(),
            proof_report=self._proof_report(),
            task_attempt_id="W004-T001-A01",
        )
        self.assertEqual(len(snapshot.repairs), 1)
        repair = snapshot.repairs[0]
        self.assertEqual(repair.before_output_hash, "before-hash")
        self.assertEqual(repair.after_output_hash, "after-hash")
        self.assertEqual(repair.resolved_failure_codes, ("FACTUAL_VALUE_MISMATCH",))
        self.assertTrue(repair.fresh_hard_gate_runs)
        self.assertTrue(repair.siblings_immutable)

        rendered = render_html(snapshot)
        for state in EvidenceState:
            self.assertIn(state.value, rendered)
        self.assertIn("No aggregate readiness score is computed", rendered)
        self.assertIn("Hard failure remains visible", rendered)
        self.assertIn("before-hash", rendered)
        self.assertIn("after-hash", rendered)
        self.assertIn("source-001", rendered)
        self.assertIn("synthetic/diagnostic", rendered)

    def test_runstore_history_adapter_uses_final_state_without_creating_a_store(self) -> None:
        state = self._run_state()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "history.json"
            path.write_text(
                json.dumps(
                    [
                        {"sequence": 1, "created_at": "2026-09-17T10:00:00+00:00", "state": {"run_id": "older"}},
                        {"sequence": 2, "created_at": "2026-09-17T10:01:00+00:00", "state": state},
                    ]
                ),
                encoding="utf-8",
            )
            loaded, observed_at = load_run_state_from_history(path)
        self.assertEqual(loaded["run_id"], "run-001")
        self.assertEqual(observed_at, "2026-09-17T10:01:00+00:00")


if __name__ == "__main__":
    unittest.main()
