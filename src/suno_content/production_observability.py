from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping
from pathlib import Path
from typing import Any

from suno_content.ingest import PdfParserAdapter
from suno_content.orchestration import RunState

from .observability import (
    OpaqueTraceLinkRegistry,
    TelemetryRecorder,
    TraceContext,
    TraceScope,
    correlation_ref,
)
from .production_slice import ReferenceVerticalSlice, SliceIdentity


TelemetrySink = Callable[[str, Mapping[str, Any]], None]


class ObservedReferenceVerticalSlice(ReferenceVerticalSlice):
    """Reference vertical slice with best-effort, non-authoritative telemetry.

    Durable product/run state and durable ordered product events remain the two
    authoritative planes. Correlated telemetry is deliberately a third,
    sampled/best-effort plane: exporter failure can neither veto nor alter
    product state, replay, reconnect, or restore.
    """

    def __init__(
        self,
        root: str | Path,
        *,
        parser: PdfParserAdapter,
        telemetry: TelemetrySink | None = None,
        observability: TelemetryRecorder | None = None,
        trace_links: OpaqueTraceLinkRegistry | None = None,
    ) -> None:
        super().__init__(root, parser=parser)
        self.telemetry = telemetry
        self.telemetry_failures: list[str] = []
        self.observability = observability or TelemetryRecorder()
        self.trace_links = trace_links or OpaqueTraceLinkRegistry()
        self._trace_refs_by_run: dict[str, str] = {}
        self._trace_contexts_by_run: dict[str, TraceContext] = {}

    def _observe(self, event: str, payload: Mapping[str, Any]) -> None:
        """Legacy evidence callback retained for the accepted T009 contract."""

        if self.telemetry is None:
            return
        try:
            self.telemetry(event, dict(payload))
        except Exception as exc:  # telemetry is explicitly non-authoritative
            self.telemetry_failures.append(f"{event}:{type(exc).__name__}:{exc}")

    @staticmethod
    def _scope_from_state(state: RunState) -> TraceScope:
        return TraceScope(
            org_id=str(state.source["org_id"]),
            workspace_id=str(state.source["workspace_id"]),
            run_id=state.run_id,
        )

    @staticmethod
    def _run_attributes(run_id: str, identity: SliceIdentity | None = None) -> dict[str, str]:
        attributes = {
            "component": "workflow",
            "run_ref": correlation_ref(run_id),
        }
        if identity is not None:
            attributes.update(
                {
                    "org_ref": correlation_ref(identity.org_id),
                    "workspace_ref": correlation_ref(identity.workspace_id),
                }
            )
        return attributes

    @staticmethod
    def _branch_attributes(job: Any, source: Mapping[str, Any], *, attempt_id: str) -> dict[str, Any]:
        return {
            "component": "ai-runtime",
            "org_ref": correlation_ref(str(source["org_id"])),
            "workspace_ref": correlation_ref(str(source["workspace_id"])),
            "run_ref": correlation_ref(str(source["run_id"])),
            "source_ref": correlation_ref(str(source["source_id"])),
            "source_hash": str(source["source_hash"]),
            "job_ref": correlation_ref(str(job.job_id)),
            "attempt_ref": correlation_ref(attempt_id),
            "audience": str(job.payload["audience"]),
            "output_format": str(job.payload["output_format"]),
        }

    def _generator(self, job: Any, source: Mapping[str, Any]) -> Mapping[str, Any]:
        attempt_id = f"{job.job_id}:attempt:1"
        attributes = self._branch_attributes(job, source, attempt_id=attempt_id)
        attributes["component"] = "provider"
        with self.observability.span("provider.generate", attributes=attributes):
            return ReferenceVerticalSlice._generator(job, source)

    def _evaluator(self, job: Any, output: Mapping[str, Any]):
        source = {
            "org_id": output["org_id"],
            "workspace_id": output["workspace_id"],
            "run_id": output["run_id"],
            "source_id": output["source_id"],
            "source_hash": output["source_hash"],
        }
        attributes = self._branch_attributes(
            job,
            source,
            attempt_id=str(output.get("attempt_id", f"{job.job_id}:attempt:unknown")),
        )
        attributes["component"] = "evaluation"
        with self.observability.span("eval.evaluate", attributes=attributes) as span:
            decision = ReferenceVerticalSlice._evaluator(job, output)
            span.set_attribute("evaluation_action", decision.action.value)
            return decision

    def _repairer(
        self,
        job: Any,
        output: Mapping[str, Any],
        decision: Any,
        attempt: int,
    ) -> Mapping[str, Any]:
        source = {
            "org_id": output["org_id"],
            "workspace_id": output["workspace_id"],
            "run_id": output["run_id"],
            "source_id": output["source_id"],
            "source_hash": output["source_hash"],
        }
        attempt_id = f"{job.job_id}:repair:{attempt}"
        attributes = self._branch_attributes(job, source, attempt_id=attempt_id)
        attributes["component"] = "repair"
        attributes["repair_attempt"] = attempt
        with self.observability.span("repair.repair", attributes=attributes):
            return ReferenceVerticalSlice._repairer(job, output, decision, attempt)

    async def start(self, **kwargs: Any) -> RunState:
        trace_headers = kwargs.pop("trace_headers", None)
        run_id = str(kwargs.get("run_id", "unknown-run"))
        identity = kwargs.get("identity")
        parent = self.observability.extract(trace_headers)
        with self.observability.span(
            "run.start",
            attributes=self._run_attributes(run_id, identity if isinstance(identity, SliceIdentity) else None),
            parent=parent,
        ) as span:
            state = await super().start(**kwargs)
            scope = self._scope_from_state(state)
            reference = self.trace_links.issue(scope, span.context.trace_id)
            self._trace_refs_by_run[state.run_id] = reference
            self._trace_contexts_by_run[state.run_id] = span.context
        self._observe(
            "run.checkpoint",
            {"run_id": state.run_id, "phase": state.phase.value},
        )
        self.observability.export_best_effort()
        return state

    async def resume(self, run_id: str, *, pause_after: str | None = None) -> RunState:
        with self.observability.span(
            "run.resume",
            attributes=self._run_attributes(run_id),
        ) as span:
            state = await super().resume(run_id, pause_after=pause_after)
            scope = self._scope_from_state(state)
            reference = self.trace_links.issue(scope, span.context.trace_id)
            self._trace_refs_by_run[state.run_id] = reference
            self._trace_contexts_by_run[state.run_id] = span.context
        self._observe(
            "run.checkpoint",
            {"run_id": state.run_id, "phase": state.phase.value},
        )
        self.observability.export_best_effort()
        return state

    def publish_authoritative_events(self, state: RunState) -> tuple[dict[str, Any], ...]:
        run_id = state.run_id
        with self.observability.span(
            "product.events.commit",
            attributes={
                "component": "product-events",
                "run_ref": correlation_ref(run_id),
                "source_ref": correlation_ref(str(state.source["source_id"])),
            },
        ) as span:
            events = super().publish_authoritative_events(state)
            span.set_attribute("event_count", len(events))
            span.set_attribute("last_event_revision", events[-1]["event_revision"] if events else 0)
            for event in events:
                payload = event.get("payload", {})
                self.observability.log(
                    "product.event.committed",
                    attributes={
                        "component": "product-events",
                        "run_ref": correlation_ref(run_id),
                        "event_type": str(event.get("event_type", "unknown")),
                        "event_revision": int(event.get("event_revision", 0)),
                        "job_ref": correlation_ref(str(payload["job_id"])) if payload.get("job_id") else "none",
                    },
                )
        self._observe(
            "authoritative.events.committed",
            {
                "run_id": state.run_id,
                "event_count": len(events),
                "last_event_revision": events[-1]["event_revision"] if events else 0,
            },
        )
        self.observability.export_best_effort()
        return events

    def live_projection(self, state: RunState):
        projector = super().live_projection(state)
        reference = self._trace_refs_by_run.get(state.run_id)
        if reference is not None:
            scope = self._scope_from_state(state)
            projector.state.trace_refs = [
                {
                    "org_id": scope.org_id,
                    "workspace_id": scope.workspace_id,
                    "run_id": scope.run_id,
                    "trace_ref": reference,
                    "href": self.trace_links.href(reference),
                    "evidence_scope": "TELEMETRY_NON_AUTHORITATIVE",
                }
            ]
        return projector

    def trace_reference(self, run_id: str) -> str:
        try:
            return self._trace_refs_by_run[run_id]
        except KeyError as exc:
            raise LookupError(f"no trace reference is registered for run {run_id}") from exc

    def trace_href(self, run_id: str) -> str:
        return self.trace_links.href(self.trace_reference(run_id))

    def resolve_trace_reference(
        self,
        reference: str,
        *,
        org_id: str,
        workspace_id: str,
        run_id: str,
    ) -> str:
        return self.trace_links.resolve(
            reference,
            TraceScope(org_id=org_id, workspace_id=workspace_id, run_id=run_id),
        )

    def inject_trace_headers(self, run_id: str, headers: MutableMapping[str, str]) -> None:
        context = self._trace_contexts_by_run.get(run_id)
        if context is None:
            raise LookupError(f"no trace context is registered for run {run_id}")
        self.observability.inject(context.child(), headers)
