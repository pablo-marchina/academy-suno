from __future__ import annotations

import asyncio
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from suno_content.ingest import PdfExtraction
from suno_content.observability import (
    OtlpHttpJsonExporter,
    TelemetryRecorder,
    TraceContext,
    correlation_ref,
)
from suno_content.orchestration import EvaluationAction, JobSpec, QualityDecision, RunPhase
from suno_content.production_observability import ObservedReferenceVerticalSlice
from suno_content.production_slice import SliceIdentity


class LockedFixturePdfAdapter:
    """Deterministic parser-contract fixture; not parser-quality evidence."""

    def parse(self, raw_bytes: bytes) -> PdfExtraction:
        if not raw_bytes.lstrip().startswith(b"%PDF-") or b"%%EOF" not in raw_bytes[-4096:]:
            raise ValueError("fixture parser received malformed PDF bytes")
        return PdfExtraction(
            text=(
                "Banco Central do Brasil Copom meeting 277 primary-source reconstruction. "
                "This controlled sample exercises observability correlation without exposing raw source content."
            ),
            parser_name="locked-fixture-pdf-adapter",
            parser_version="reference-test-v1",
            page_count=1,
            confidence=0.97,
            warnings=(),
            table_role_ambiguity=False,
        )


def _minimal_pdf(*, extra: bytes = b"") -> bytes:
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
        + extra
        + b"\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n"
    )


def _identity() -> SliceIdentity:
    return SliceIdentity(
        org_id="org-a",
        workspace_id="ws-a",
        user_id="user-a",
        session_id="session-a",
        csrf_token="csrf-a",
    )


class _FailingExporter:
    def export(self, snapshot):
        raise ConnectionError("injected OTLP/backend outage")


class _CaptureOtlpExporter(OtlpHttpJsonExporter):
    def __init__(self) -> None:
        super().__init__("http://collector.invalid")
        self.calls: list[tuple[str, dict]] = []

    def _post(self, path: str, payload):
        self.calls.append((path, dict(payload)))


class ObservabilityLiveOpsTests(unittest.TestCase):
    def test_w3c_3x3_traceability_and_scoped_cockpit_link(self) -> None:
        parent_trace = "0123456789abcdef0123456789abcdef"
        parent_span = "0123456789abcdef"
        headers = {"traceparent": f"00-{parent_trace}-{parent_span}-01"}
        secret_canary = b"SUPER_SECRET_CANARY_T012"

        with TemporaryDirectory() as tmp:
            recorder = TelemetryRecorder()
            slice_ = ObservedReferenceVerticalSlice(
                Path(tmp),
                parser=LockedFixturePdfAdapter(),
                observability=recorder,
            )
            complete = asyncio.run(
                slice_.start(
                    run_id="run-w006-t012-a01",
                    identity=_identity(),
                    raw_pdf=_minimal_pdf(extra=secret_canary),
                    artifact_label="copom-277-observability.pdf",
                    source_group_key="copom_277_2026_03",
                    trace_headers=headers,
                )
            )
            self.assertIs(complete.phase, RunPhase.COMPLETE)
            self.assertEqual(len(complete.joined_outputs), 9)

            events = slice_.publish_authoritative_events(complete)
            self.assertEqual(len(events), 11)
            self.assertNotIn(secret_canary.decode(), json.dumps(events, sort_keys=True))

            snapshot = recorder.snapshot()
            spans = snapshot["spans"]
            provider_spans = [span for span in spans if span["name"] == "provider.generate"]
            eval_spans = [span for span in spans if span["name"] == "eval.evaluate"]
            self.assertEqual(len(provider_spans), 9)
            self.assertEqual(len(eval_spans), 9)
            self.assertTrue(all(span["trace_id"] == parent_trace for span in provider_spans + eval_spans))

            run_span = next(span for span in spans if span["name"] == "run.start")
            self.assertEqual(run_span["trace_id"], parent_trace)
            self.assertEqual(run_span["parent_span_id"], parent_span)

            expected_job_refs = {correlation_ref(job_id) for job_id in complete.jobs}
            observed_job_refs = {span["attributes"]["job_ref"] for span in provider_spans}
            self.assertEqual(observed_job_refs, expected_job_refs)
            self.assertTrue(
                all(
                    raw_job_id not in json.dumps(span["attributes"], sort_keys=True)
                    for raw_job_id in complete.jobs
                    for span in provider_spans + eval_spans
                )
            )

            for metric in snapshot["metrics"]:
                labels = set(metric["attributes"])
                self.assertFalse(
                    labels
                    & {
                        "org_id",
                        "workspace_id",
                        "tenant_id",
                        "run_id",
                        "job_id",
                        "attempt_id",
                        "trace_id",
                        "span_id",
                    }
                )

            telemetry_json = json.dumps(snapshot, sort_keys=True)
            self.assertNotIn(secret_canary.decode(), telemetry_json)
            self.assertNotIn("session-a", telemetry_json)
            self.assertNotIn("csrf-a", telemetry_json)

            trace_ref = slice_.trace_reference(complete.run_id)
            trace_href = slice_.trace_href(complete.run_id)
            self.assertNotIn(parent_trace, trace_href)
            self.assertNotIn(complete.run_id, trace_href)
            self.assertEqual(
                slice_.resolve_trace_reference(
                    trace_ref,
                    org_id="org-a",
                    workspace_id="ws-a",
                    run_id=complete.run_id,
                ),
                parent_trace,
            )
            with self.assertRaises(PermissionError):
                slice_.resolve_trace_reference(
                    trace_ref,
                    org_id="org-b",
                    workspace_id="ws-a",
                    run_id=complete.run_id,
                )

            projector = slice_.live_projection(complete)
            view = projector.state.view_model()
            self.assertEqual(view["phase"], "complete")
            self.assertEqual(len(view["cells"]), 9)
            self.assertEqual(view["event_revision"], 11)
            self.assertEqual(len(view["trace_refs"]), 1)
            self.assertEqual(view["trace_refs"][0]["trace_ref"], trace_ref)
            self.assertEqual(
                view["trace_refs"][0]["evidence_scope"],
                "TELEMETRY_NON_AUTHORITATIVE",
            )

    def test_provider_eval_and_repair_spans_are_correlated_without_raw_branch_ids(self) -> None:
        with TemporaryDirectory() as tmp:
            recorder = TelemetryRecorder()
            slice_ = ObservedReferenceVerticalSlice(
                Path(tmp),
                parser=LockedFixturePdfAdapter(),
                observability=recorder,
            )
            complete = asyncio.run(
                slice_.start(
                    run_id="run-w006-t012-a01-repair-span",
                    identity=_identity(),
                    raw_pdf=_minimal_pdf(),
                    artifact_label="repair-span.pdf",
                    source_group_key="repair_span",
                )
            )
            job_id = sorted(complete.jobs)[0]
            branch = complete.jobs[job_id]
            output = dict(complete.joined_outputs[job_id])
            job = JobSpec(job_id=job_id, payload=dict(branch.payload))
            decision = QualityDecision(
                EvaluationAction.REPAIR,
                reasons=("test_repair_observability",),
            )
            repaired = slice_._repairer(job, output, decision, 1)
            self.assertEqual(repaired["attempt_id"], f"{job_id}:repair:1")

            repair_spans = [
                span
                for span in recorder.snapshot()["spans"]
                if span["name"] == "repair.repair"
            ]
            self.assertEqual(len(repair_spans), 1)
            self.assertEqual(repair_spans[0]["attributes"]["job_ref"], correlation_ref(job_id))
            self.assertNotIn(job_id, json.dumps(repair_spans[0]["attributes"], sort_keys=True))

    def test_otlp_http_json_export_uses_three_standard_signal_paths_and_bounded_payloads(self) -> None:
        exporter = _CaptureOtlpExporter()
        recorder = TelemetryRecorder(exporter=exporter)
        with recorder.span(
            "provider.generate",
            attributes={
                "component": "provider",
                "authorization": "Bearer SUPER_SECRET",
                "prompt": "private source content",
                "run_ref": correlation_ref("run-a"),
            },
        ):
            recorder.log(
                "provider.completed",
                attributes={"content": "private output", "component": "provider"},
            )
            recorder.record_metric(
                "provider.requests",
                1,
                labels={
                    "component": "provider",
                    "outcome": "ok",
                    "run_id": "raw-run-id",
                    "job_id": "raw-job-id",
                },
            )

        self.assertTrue(recorder.export_best_effort())
        self.assertEqual([path for path, _ in exporter.calls], ["/v1/traces", "/v1/metrics", "/v1/logs"])
        payload_json = json.dumps(exporter.calls, sort_keys=True)
        self.assertNotIn("SUPER_SECRET", payload_json)
        self.assertNotIn("private source content", payload_json)
        self.assertNotIn("private output", payload_json)
        self.assertNotIn("raw-run-id", payload_json)
        self.assertNotIn("raw-job-id", payload_json)
        self.assertIn("[REDACTED]", payload_json)

    def test_export_outage_never_blocks_authoritative_product_path(self) -> None:
        with TemporaryDirectory() as tmp:
            recorder = TelemetryRecorder(exporter=_FailingExporter())
            slice_ = ObservedReferenceVerticalSlice(
                Path(tmp),
                parser=LockedFixturePdfAdapter(),
                observability=recorder,
            )
            complete = asyncio.run(
                slice_.start(
                    run_id="run-w006-t012-a01-outage",
                    identity=_identity(),
                    raw_pdf=_minimal_pdf(),
                    artifact_label="telemetry-outage.pdf",
                    source_group_key="telemetry_outage",
                )
            )
            self.assertIs(complete.phase, RunPhase.COMPLETE)
            events = slice_.publish_authoritative_events(complete)
            self.assertEqual(len(events), 11)
            replayed = slice_.event_store.replay_events(
                org_id="org-a",
                workspace_id="ws-a",
                run_id=complete.run_id,
            )
            self.assertEqual(replayed, events)
            self.assertGreaterEqual(len(recorder.export_failures), 2)
            self.assertEqual(len(complete.joined_outputs), 9)

    def test_trace_context_fail_closed_parse_and_injection(self) -> None:
        context = TraceContext.parse(
            "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"
        )
        child = context.child()
        headers: dict[str, str] = {}
        TelemetryRecorder.inject(child, headers)
        extracted = TelemetryRecorder.extract(headers)
        self.assertIsNotNone(extracted)
        assert extracted is not None
        self.assertEqual(extracted.trace_id, context.trace_id)
        self.assertEqual(extracted.span_id, child.span_id)
        self.assertIsNone(TelemetryRecorder.extract({"traceparent": "garbage"}))


if __name__ == "__main__":
    unittest.main()
