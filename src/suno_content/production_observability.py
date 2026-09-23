from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from suno_content.ingest import PdfParserAdapter
from suno_content.orchestration import RunState

from .production_slice import ReferenceVerticalSlice


TelemetrySink = Callable[[str, Mapping[str, Any]], None]


class ObservedReferenceVerticalSlice(ReferenceVerticalSlice):
    """Reference vertical slice with best-effort, non-authoritative telemetry.

    Telemetry is deliberately downstream of authoritative mutations. A sink
    outage is recorded for evidence but can neither veto nor alter run state,
    product events, replay, or restore.
    """

    def __init__(
        self,
        root: str | Path,
        *,
        parser: PdfParserAdapter,
        telemetry: TelemetrySink | None = None,
    ) -> None:
        super().__init__(root, parser=parser)
        self.telemetry = telemetry
        self.telemetry_failures: list[str] = []

    def _observe(self, event: str, payload: Mapping[str, Any]) -> None:
        if self.telemetry is None:
            return
        try:
            self.telemetry(event, dict(payload))
        except Exception as exc:  # telemetry is explicitly non-authoritative
            self.telemetry_failures.append(f"{event}:{type(exc).__name__}:{exc}")

    async def start(self, **kwargs: Any) -> RunState:
        state = await super().start(**kwargs)
        self._observe(
            "run.checkpoint",
            {"run_id": state.run_id, "phase": state.phase.value},
        )
        return state

    async def resume(self, run_id: str, *, pause_after: str | None = None) -> RunState:
        state = await super().resume(run_id, pause_after=pause_after)
        self._observe(
            "run.checkpoint",
            {"run_id": state.run_id, "phase": state.phase.value},
        )
        return state

    def publish_authoritative_events(self, state: RunState) -> tuple[dict[str, Any], ...]:
        events = super().publish_authoritative_events(state)
        self._observe(
            "authoritative.events.committed",
            {
                "run_id": state.run_id,
                "event_count": len(events),
                "last_event_revision": events[-1]["event_revision"] if events else 0,
            },
        )
        return events
