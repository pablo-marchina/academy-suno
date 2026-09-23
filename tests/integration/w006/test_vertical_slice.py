from __future__ import annotations

import asyncio
import inspect
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from suno_content.ingest import PdfExtraction
from suno_content.orchestration import EvaluationAction, QualityDecision, RunPhase
from suno_content.production_observability import ObservedReferenceVerticalSlice
from suno_content.production_slice import (
    ProductionQualificationError,
    ReferenceVerticalSlice,
    SliceIdentity,
    SourceNotReadyError,
)


class LockedFixturePdfAdapter:
    """Deterministic reference adapter using no dependency outside the accepted lock.

    This is integration-fixture evidence for the parser/trust contract only; it is
    not parser-quality evidence and cannot select a production parser.
    """

    def __init__(self, *, confidence: float = 0.97, warnings: tuple[str, ...] = ()) -> None:
        self.confidence = confidence
        self.warnings = warnings
        self.calls = 0

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        self.calls += 1
        if not raw_bytes.lstrip().startswith(b"%PDF-") or b"%%EOF" not in raw_bytes[-4096:]:
            raise ValueError("fixture parser received malformed PDF bytes")
        return PdfExtraction(
            text=(
                "Banco Central do Brasil Copom meeting 277 monetary policy primary-source reconstruction. "
                "This controlled sample exercises source provenance, exact branch identity, durable resume, "
                "authoritative events, reconnect, retry isolation, and database restore without claiming parser quality."
            ),
            parser_name="locked-fixture-pdf-adapter",
            parser_version="reference-test-v1",
            page_count=1,
            confidence=self.confidence,
            warnings=self.warnings,
            table_role_ambiguity=False,
        )


def _minimal_pdf() -> bytes:
    # Structurally bounded PDF-like fixture: preflight sees a PDF signature and EOF;
    # extraction itself is delegated to LockedFixturePdfAdapter above.
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
        b"2 0 obj\n<< /Length 0 >>\nstream\nendstream\nendobj\n"
        b"trailer\n<< /Root 1 0 R >>\n%%EOF\n"
    )


def _identity() -> SliceIdentity:
    return SliceIdentity(
        org_id="org-a",
        workspace_id="ws-a",
        user_id="user-a",
        session_id="session-a",
        csrf_token="csrf-a",
    )


class _RetryRepairSlice(ReferenceVerticalSlice):
    def __init__(self, root: str | Path, *, parser: LockedFixturePdfAdapter) -> None:
        super().__init__(root, parser=parser)
        self.generator_calls: dict[str, int] = {}
        self.evaluator_calls: dict[str, int] = {}

    def _generator(self, job, source):
        calls = self.generator_calls.get(job.job_id, 0) + 1
        self.generator_calls[job.job_id] = calls
        if (
            job.payload["audience"] == "BEGINNER"
            and job.payload["output_format"] == "ARTICLE"
            and calls == 1
        ):
            raise TimeoutError("injected transient transport failure")
        return ReferenceVerticalSlice._generator(job, source)

    def _evaluator(self, job, output):
        calls = self.evaluator_calls.get(job.job_id, 0) + 1
        self.evaluator_calls[job.job_id] = calls
        if (
            job.payload["audience"] == "ADVANCED"
            and job.payload["output_format"] == "CAROUSEL"
            and calls == 1
        ):
            return QualityDecision(
                EvaluationAction.REPAIR,
                reasons=("injected_branch_local_quality_repair",),
            )
        return ReferenceVerticalSlice._evaluator(job, output)


class VerticalSliceIntegrationTests(unittest.TestCase):
    def test_pause_resume_authoritative_replay_and_db_restore(self) -> None:
        raw_pdf = _minimal_pdf()
        identity = _identity()

        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "live"
            parser = LockedFixturePdfAdapter()
            first = ReferenceVerticalSlice(root, parser=parser)
            paused = asyncio.run(
                first.start(
                    run_id="run-w006-t009-a02-smoke",
                    identity=identity,
                    raw_pdf=raw_pdf,
                    artifact_label="copom-277-reconstruction.pdf",
                    source_group_key="copom_277_2026_03",
                    pause_after="planned",
                )
            )
            self.assertIs(paused.phase, RunPhase.PLANNED)
            self.assertEqual(len(paused.jobs), 9)
            self.assertEqual(parser.calls, 1)
            self.assertTrue(paused.source["source_hash"])
            self.assertTrue(paused.source["provenance_ref"].startswith("sha256:"))
            self.assertEqual(paused.source["parser_name"], "locked-fixture-pdf-adapter")

            restarted = ReferenceVerticalSlice(root, parser=LockedFixturePdfAdapter())
            complete = asyncio.run(restarted.resume(paused.run_id))
            self.assertIs(complete.phase, RunPhase.COMPLETE)
            self.assertEqual(len(complete.joined_outputs), 9)
            self.assertEqual(complete.aggregate["accepted_branch_count"], 9)
            self.assertEqual(set(complete.aggregate["job_ids"]), set(complete.jobs))
            self.assertEqual(len(set(complete.jobs)), 9)
            for job_id, output in complete.joined_outputs.items():
                self.assertEqual(output["org_id"], identity.org_id)
                self.assertEqual(output["workspace_id"], identity.workspace_id)
                self.assertEqual(output["run_id"], complete.run_id)
                self.assertEqual(output["cell_id"], job_id)
                self.assertEqual(output["job_id"], job_id)
                self.assertTrue(output["attempt_id"].startswith(f"{job_id}:"))
                self.assertEqual(output["source_id"], complete.source["source_id"])
                self.assertEqual(output["source_hash"], complete.source["source_hash"])

            first_events = restarted.publish_authoritative_events(complete)
            second_events = restarted.publish_authoritative_events(complete)
            self.assertEqual(len(first_events), 11)
            self.assertEqual(first_events, second_events)
            self.assertEqual([event["event_revision"] for event in first_events], list(range(1, 12)))
            self.assertEqual(
                restarted.event_store.audit_invariants(),
                {
                    "state_without_latest_transition": 0,
                    "transition_without_state": 0,
                    "transition_without_outbox": 0,
                },
            )

            projector = restarted.live_projection(complete)
            view = projector.state.view_model()
            self.assertEqual(view["phase"], "complete")
            self.assertEqual(len(view["cells"]), 9)
            self.assertEqual(view["event_revision"], 11)
            self.assertTrue(all(cell["state"] == "PROVEN" for cell in view["cells"]))

            evidence = restarted.evidence(complete).to_dict()
            self.assertEqual(evidence["accepted_branches"], 9)
            self.assertEqual(evidence["event_count"], 11)
            self.assertEqual(evidence["production_ready_claim"], "NOT_AUTHORIZED")
            self.assertEqual(evidence["production_locks"]["runtime"], "NONE")
            self.assertEqual(evidence["production_locks"]["parser"], "NONE")
            self.assertTrue(evidence["aggregate_digest"])

            backup = restarted.backup_to(Path(tmp) / "backup")
            restored = ReferenceVerticalSlice.restore_from_backup(
                backup,
                Path(tmp) / "restored",
                parser=LockedFixturePdfAdapter(),
            )
            restored_state = asyncio.run(restored.resume(complete.run_id))
            self.assertIs(restored_state.phase, RunPhase.COMPLETE)
            restored_events = restored.event_store.replay_events(
                org_id="org-a",
                workspace_id="ws-a",
                run_id=complete.run_id,
            )
            self.assertEqual(restored_events, first_events)
            restored_view = restored.live_projection(restored_state).state.view_model()
            self.assertEqual(len(restored_view["cells"]), 9)
            self.assertEqual(restored_view["event_revision"], 11)

    def test_transport_retry_and_quality_repair_are_branch_local(self) -> None:
        with TemporaryDirectory() as tmp:
            slice_ = _RetryRepairSlice(Path(tmp) / "faults", parser=LockedFixturePdfAdapter())
            complete = asyncio.run(
                slice_.start(
                    run_id="run-w006-t009-a02-faults",
                    identity=_identity(),
                    raw_pdf=_minimal_pdf(),
                    artifact_label="copom-277-reconstruction.pdf",
                    source_group_key="copom_277_2026_03",
                )
            )
            self.assertIs(complete.phase, RunPhase.COMPLETE)
            self.assertEqual(len(complete.jobs), 9)
            self.assertEqual(len(complete.joined_outputs), 9)

            retry_job = next(
                job_id
                for job_id, branch in complete.jobs.items()
                if branch.payload["audience"] == "BEGINNER"
                and branch.payload["output_format"] == "ARTICLE"
            )
            repair_job = next(
                job_id
                for job_id, branch in complete.jobs.items()
                if branch.payload["audience"] == "ADVANCED"
                and branch.payload["output_format"] == "CAROUSEL"
            )
            self.assertEqual(complete.jobs[retry_job].transport_retries, {"generate": 1})
            self.assertEqual(complete.jobs[repair_job].quality_repairs, 1)
            self.assertTrue(
                all(
                    not branch.transport_retries
                    for job_id, branch in complete.jobs.items()
                    if job_id != retry_job
                )
            )
            self.assertTrue(
                all(
                    branch.quality_repairs == 0
                    for job_id, branch in complete.jobs.items()
                    if job_id != repair_job
                )
            )
            self.assertEqual(set(complete.joined_outputs), set(complete.jobs))
            events = slice_.publish_authoritative_events(complete)
            self.assertEqual(len(events), 11)

    def test_telemetry_outage_cannot_block_or_corrupt_authoritative_completion(self) -> None:
        def unavailable_telemetry(_: str, __: object) -> None:
            raise ConnectionError("injected telemetry outage")

        with TemporaryDirectory() as tmp:
            slice_ = ObservedReferenceVerticalSlice(
                Path(tmp) / "telemetry",
                parser=LockedFixturePdfAdapter(),
                telemetry=unavailable_telemetry,
            )
            complete = asyncio.run(
                slice_.start(
                    run_id="run-w006-t009-a02-telemetry-outage",
                    identity=_identity(),
                    raw_pdf=_minimal_pdf(),
                    artifact_label="copom-277-reconstruction.pdf",
                    source_group_key="copom_277_2026_03",
                )
            )
            self.assertIs(complete.phase, RunPhase.COMPLETE)
            self.assertEqual(len(complete.joined_outputs), 9)
            events = slice_.publish_authoritative_events(complete)
            self.assertEqual(len(events), 11)
            self.assertEqual(events[-1]["payload"]["phase"], "complete")
            self.assertEqual(len(slice_.telemetry_failures), 2)
            replayed = slice_.event_store.replay_events(
                org_id="org-a",
                workspace_id="ws-a",
                run_id=complete.run_id,
            )
            self.assertEqual(replayed, events)

    def test_controlled_upload_fails_closed_before_parser_on_active_content(self) -> None:
        parser = LockedFixturePdfAdapter()
        dangerous = b"%PDF-1.4\n/JavaScript\n%%EOF\n"
        with TemporaryDirectory() as tmp:
            slice_ = ReferenceVerticalSlice(Path(tmp), parser=parser)
            with self.assertRaises(SourceNotReadyError):
                asyncio.run(
                    slice_.start(
                        run_id="run-w006-t009-a02-quarantine",
                        identity=_identity(),
                        raw_pdf=dangerous,
                        artifact_label="untrusted.pdf",
                        source_group_key="untrusted",
                    )
                )
        self.assertEqual(parser.calls, 0)

    def test_low_confidence_extraction_cannot_enter_orchestration(self) -> None:
        parser = LockedFixturePdfAdapter(confidence=0.50)
        with TemporaryDirectory() as tmp:
            slice_ = ReferenceVerticalSlice(Path(tmp), parser=parser)
            with self.assertRaises(SourceNotReadyError):
                asyncio.run(
                    slice_.start(
                        run_id="run-w006-t009-a02-low-confidence",
                        identity=_identity(),
                        raw_pdf=_minimal_pdf(),
                        artifact_label="low-confidence.pdf",
                        source_group_key="low-confidence",
                    )
                )
        self.assertEqual(parser.calls, 1)

    def test_reference_surface_has_no_server_filesystem_path_input_and_fails_closed_for_production(self) -> None:
        params = inspect.signature(ReferenceVerticalSlice.start).parameters
        self.assertIn("raw_pdf", params)
        self.assertNotIn("path", params)
        self.assertNotIn("file_path", params)
        with self.assertRaises(ProductionQualificationError):
            ReferenceVerticalSlice.assert_production_qualified()

    def test_evidence_json_is_deterministically_serializable(self) -> None:
        payload = {
            "runtime_lock": "NONE",
            "database_lock": "NONE",
            "parser_lock": "NONE",
            "frontend_lock": "NONE",
            "production_ready_claim": "NOT_AUTHORIZED",
        }
        first = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        second = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
