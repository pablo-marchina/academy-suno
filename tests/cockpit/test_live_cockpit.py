from __future__ import annotations

import copy
import unittest

from suno_content.cockpit.live import (
    AuthorizationProjectionError,
    AuthorizedScope,
    CANDIDATES,
    ContractProjectionError,
    LiveCockpitProjector,
    reconnect,
    render_candidate,
)


class LiveCockpitBakeoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = AuthorizedScope("org-a", "workspace-a", "run-a")
        cells = []
        for audience in ("beginner", "intermediate", "advanced"):
            for output_format in ("article", "carousel", "short_video"):
                state = "PROVEN"
                if (audience, output_format) == ("beginner", "carousel"):
                    state = "FAIL"
                elif (audience, output_format) == ("advanced", "short_video"):
                    state = "REVIEW_REQUIRED"
                cells.append(
                    {
                        "org_id": "org-a",
                        "workspace_id": "workspace-a",
                        "run_id": "run-a",
                        "cell_id": f"{audience}:{output_format}",
                        "audience": audience,
                        "output_format": output_format,
                        "state": state,
                        "detail": f"durable {state.lower()} state",
                    }
                )
        self.snapshot = {
            "contract_version": "1.0.0",
            "org_id": "org-a",
            "workspace_id": "workspace-a",
            "run_id": "run-a",
            "revision": 7,
            "event_revision": 12,
            "phase": "review_required",
            "source": {
                "org_id": "org-a",
                "workspace_id": "workspace-a",
                "run_id": "run-a",
                "source_id": "source-a",
                "source_hash": "a" * 64,
            },
            "cells": cells,
            "citations": [
                {
                    "org_id": "org-a",
                    "workspace_id": "workspace-a",
                    "run_id": "run-a",
                    "cell_id": "beginner:article",
                    "citation_id": "cite-1",
                    "source_id": "source-a",
                }
            ],
            "evaluations": [
                {
                    "org_id": "org-a",
                    "workspace_id": "workspace-a",
                    "run_id": "run-a",
                    "cell_id": "beginner:carousel",
                    "evaluation_id": "eval-1",
                    "state": "FAIL",
                }
            ],
            "repairs": [],
            "trace_refs": [
                {
                    "org_id": "org-a",
                    "workspace_id": "workspace-a",
                    "run_id": "run-a",
                    "trace_id": "trace-a",
                }
            ],
        }

    def event(self, *, event_id: str, event_revision: int, event_type: str, payload: dict) -> dict:
        return {
            "contract_version": "1.0.0",
            "org_id": "org-a",
            "workspace_id": "workspace-a",
            "run_id": "run-a",
            "event_id": event_id,
            "transition_id": f"transition-{event_id}",
            "mutation_id": f"mutation-{event_id}",
            "resource_id": "run-a",
            "result_revision": 8,
            "event_revision": event_revision,
            "event_type": event_type,
            "payload": payload,
        }

    def test_both_candidates_use_identical_durable_projection_and_accessible_updates(self) -> None:
        projector = LiveCockpitProjector.from_snapshot(self.scope, self.snapshot)
        self.assertEqual(len(projector.state.cells), 9)
        self.assertEqual(projector.state.cells["beginner:carousel"]["state"], "FAIL")
        self.assertEqual(projector.state.cells["advanced:short_video"]["state"], "REVIEW_REQUIRED")

        rendered = {candidate: render_candidate(candidate, projector.state) for candidate in CANDIDATES}
        for html in rendered.values():
            self.assertIn('aria-live="polite"', html)
            self.assertIn('role="status"', html)
            self.assertIn("FAIL", html)
            self.assertIn("REVIEW_REQUIRED", html)
            self.assertIn("revision 7", html)
            self.assertIn("event revision 12", html)
            self.assertNotIn("app/recipient", html)
            self.assertNotIn("W004", html)

    def test_reconnect_rebuilds_snapshot_then_replays_authoritative_events(self) -> None:
        repaired = {
            "org_id": "org-a",
            "workspace_id": "workspace-a",
            "run_id": "run-a",
            "cell_id": "beginner:carousel",
            "audience": "beginner",
            "output_format": "carousel",
            "state": "REVIEW_REQUIRED",
            "detail": "repair applied; fresh evaluation still required",
        }
        event = self.event(
            event_id="event-13",
            event_revision=13,
            event_type="cell.updated",
            payload=repaired,
        )
        projector = reconnect(self.scope, self.snapshot, [event])
        self.assertEqual(projector.state.last_event_revision, 13)
        self.assertEqual(projector.state.revision, 8)
        self.assertEqual(projector.state.cells["beginner:carousel"]["state"], "REVIEW_REQUIRED")
        self.assertFalse(projector.apply_event(event), "at-least-once duplicate must deduplicate by event id")

    def test_cross_tenant_source_event_and_trace_projection_success_is_zero(self) -> None:
        successes = 0

        bad_source = copy.deepcopy(self.snapshot)
        bad_source["source"]["workspace_id"] = "workspace-b"
        try:
            LiveCockpitProjector.from_snapshot(self.scope, bad_source)
            successes += 1
        except AuthorizationProjectionError:
            pass

        bad_trace = copy.deepcopy(self.snapshot)
        bad_trace["trace_refs"][0]["org_id"] = "org-b"
        try:
            LiveCockpitProjector.from_snapshot(self.scope, bad_trace)
            successes += 1
        except AuthorizationProjectionError:
            pass

        projector = LiveCockpitProjector.from_snapshot(self.scope, self.snapshot)
        bad_event = self.event(
            event_id="event-cross-tenant",
            event_revision=13,
            event_type="cell.updated",
            payload=copy.deepcopy(self.snapshot["cells"][0]),
        )
        bad_event["workspace_id"] = "workspace-b"
        try:
            projector.apply_event(bad_event)
            successes += 1
        except AuthorizationProjectionError:
            pass

        self.assertEqual(successes, 0)

    def test_nested_cross_tenant_event_payload_fails_closed(self) -> None:
        projector = LiveCockpitProjector.from_snapshot(self.scope, self.snapshot)
        payload = copy.deepcopy(self.snapshot["cells"][0])
        payload["workspace_id"] = "workspace-b"
        event = self.event(
            event_id="event-13",
            event_revision=13,
            event_type="cell.updated",
            payload=payload,
        )
        with self.assertRaises(AuthorizationProjectionError):
            projector.apply_event(event)
        self.assertEqual(projector.state.last_event_revision, 12)

    def test_static_w004_fallback_is_unavailable(self) -> None:
        missing_source = copy.deepcopy(self.snapshot)
        missing_source["source"] = {}
        with self.assertRaises((AuthorizationProjectionError, ContractProjectionError)):
            LiveCockpitProjector.from_snapshot(self.scope, missing_source)

    def test_cursor_is_not_an_authority_input_and_stale_events_fail_closed(self) -> None:
        projector = LiveCockpitProjector.from_snapshot(self.scope, self.snapshot)
        stale = self.event(
            event_id="event-stale",
            event_revision=11,
            event_type="cell.updated",
            payload=copy.deepcopy(self.snapshot["cells"][0]),
        )
        with self.assertRaises(ContractProjectionError):
            projector.apply_event(stale)
        self.assertNotIn("cursor", projector.state.view_model())


if __name__ == "__main__":
    unittest.main()
