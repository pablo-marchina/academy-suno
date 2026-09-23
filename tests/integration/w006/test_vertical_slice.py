from __future__ import annotations

import asyncio
import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from suno_content.ingest import PypdfAdapter
from suno_content.orchestration import RunPhase
from suno_content.production_slice import (
    ProductionQualificationError,
    ReferenceVerticalSlice,
    SliceIdentity,
)


def _minimal_pdf(text: str) -> bytes:
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 12 Tf 72 720 Td ({escaped}) Tj ET\n".encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"endstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    payload = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(payload))
        payload.extend(f"{index} 0 obj\n".encode("ascii"))
        payload.extend(obj)
        payload.extend(b"\nendobj\n")
    xref = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    payload.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(payload)


@unittest.skipUnless(importlib.util.find_spec("pypdf") is not None, "task smoke requires pypdf")
class VerticalSliceIntegrationTests(unittest.TestCase):
    def test_pause_resume_authoritative_replay_and_db_restore(self) -> None:
        corpus_text = (
            "Banco Central do Brasil Copom meeting 277 monetary policy primary-source reconstruction. "
            "This controlled sample exercises source provenance, exact branch identity, durable resume, "
            "authoritative events, reconnect, and database restore without claiming parser quality."
        )
        raw_pdf = _minimal_pdf(corpus_text)
        identity = SliceIdentity(
            org_id="org-a",
            workspace_id="ws-a",
            user_id="user-a",
            session_id="session-a",
            csrf_token="csrf-a",
        )

        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "live"
            parser = PypdfAdapter()
            first = ReferenceVerticalSlice(root, parser=parser)
            paused = asyncio.run(
                first.start(
                    run_id="run-w006-t009-smoke",
                    identity=identity,
                    raw_pdf=raw_pdf,
                    artifact_label="copom-277-reconstruction.pdf",
                    source_group_key="copom_277_2026_03",
                    pause_after="planned",
                )
            )
            self.assertIs(paused.phase, RunPhase.PLANNED)
            self.assertEqual(len(paused.jobs), 9)
            self.assertTrue(paused.source["source_hash"])
            self.assertTrue(paused.source["provenance_ref"].startswith("sha256:"))

            restarted = ReferenceVerticalSlice(root, parser=parser)
            complete = asyncio.run(restarted.resume(paused.run_id))
            self.assertIs(complete.phase, RunPhase.COMPLETE)
            self.assertEqual(len(complete.joined_outputs), 9)
            self.assertEqual(complete.aggregate["accepted_branch_count"], 9)
            self.assertEqual(set(complete.aggregate["job_ids"]), set(complete.jobs))

            first_events = restarted.publish_authoritative_events(complete)
            second_events = restarted.publish_authoritative_events(complete)
            self.assertEqual(len(first_events), 11)
            self.assertEqual(first_events, second_events)
            self.assertEqual([event["event_revision"] for event in first_events], list(range(1, 12)))
            self.assertEqual(restarted.event_store.audit_invariants(), {
                "state_without_latest_transition": 0,
                "transition_without_state": 0,
                "transition_without_outbox": 0,
            })

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
            self.assertTrue(evidence["aggregate_digest"])

            backup = restarted.backup_to(Path(tmp) / "backup")
            restored = ReferenceVerticalSlice.restore_from_backup(
                backup,
                Path(tmp) / "restored",
                parser=parser,
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

    def test_reference_slice_fails_closed_for_production_claim(self) -> None:
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
