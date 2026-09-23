from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from typing import Any, Mapping

CONTRACT_VERSION = "1.0.0"
EXPLICIT_CELL_STATES = {
    "PROVEN",
    "DIAGNOSTIC_ONLY",
    "NOT_COMPUTABLE",
    "NOT_RUN",
    "NOT_COMPARABLE",
    "PRODUCTION_UNKNOWN",
    "FAIL",
    "REVIEW_REQUIRED",
}
RESOURCE_TYPES = {
    "organization",
    "workspace",
    "user",
    "document",
    "run",
    "job",
    "branch",
    "attempt",
    "evaluation",
    "repair",
    "experiment",
    "artifact",
    "event",
    "index",
    "publish_attempt",
}
CANDIDATES = ("server_hypermedia_shell", "client_event_shell")


class LiveCockpitError(ValueError):
    """Base error for fail-closed live cockpit projection."""


class AuthorizationProjectionError(LiveCockpitError):
    """Protected data attempted to cross its server-authorized tenant scope."""


class ContractProjectionError(LiveCockpitError):
    """Production contract/revision semantics are invalid or unsupported."""


@dataclass(frozen=True, slots=True)
class AuthorizedScope:
    org_id: str
    workspace_id: str
    run_id: str

    def assert_matches(self, value: Mapping[str, Any], *, label: str) -> None:
        observed = (
            str(value.get("org_id", "")),
            str(value.get("workspace_id", "")),
            str(value.get("run_id", "")),
        )
        expected = (self.org_id, self.workspace_id, self.run_id)
        if observed != expected:
            raise AuthorizationProjectionError(
                f"{label} scope does not match server-authorized stream"
            )

    def authorized_stream(self) -> dict[str, Any]:
        """Canonical AuthorizedStream shape from production contracts v1."""
        return {
            "contract_version": CONTRACT_VERSION,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "run_id": self.run_id,
        }


@dataclass(slots=True)
class LiveCockpitState:
    scope: AuthorizedScope
    revision: int
    last_event_revision: int
    source: dict[str, Any]
    phase: str
    cells: dict[str, dict[str, Any]] = field(default_factory=dict)
    citations: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    evaluations: dict[str, dict[str, Any]] = field(default_factory=dict)
    repairs: list[dict[str, Any]] = field(default_factory=list)
    trace_refs: list[dict[str, Any]] = field(default_factory=list)
    resource_revisions: dict[str, int] = field(default_factory=dict)
    seen_event_ids: set[str] = field(default_factory=set)

    def view_model(self) -> dict[str, Any]:
        ordered_cells = [self.cells[key] for key in sorted(self.cells)]
        return {
            "org_id": self.scope.org_id,
            "workspace_id": self.scope.workspace_id,
            "run_id": self.scope.run_id,
            "revision": self.revision,
            "event_revision": self.last_event_revision,
            "phase": self.phase,
            "source": dict(self.source),
            "cells": [dict(cell) for cell in ordered_cells],
            "citations": {key: list(value) for key, value in sorted(self.citations.items())},
            "evaluations": {key: dict(value) for key, value in sorted(self.evaluations.items())},
            "repairs": list(self.repairs),
            "trace_refs": list(self.trace_refs),
        }


class LiveCockpitProjector:
    """Project durable snapshot + canonical EventEnvelope values into live state.

    Authorization is supplied by the server as ``AuthorizedScope``. Replay cursor
    values are deliberately absent from authorization checks: a cursor is a
    position, never authority. Unknown contracts, stale stream revisions, scope
    mismatches and protected nested records fail closed.
    """

    def __init__(self, state: LiveCockpitState):
        self.state = state

    @classmethod
    def from_snapshot(
        cls,
        authorized_scope: AuthorizedScope,
        snapshot: Mapping[str, Any],
    ) -> "LiveCockpitProjector":
        _require_contract(snapshot)
        authorized_scope.assert_matches(snapshot, label="snapshot")
        revision = _non_negative_int(snapshot.get("revision"), "snapshot.revision")
        event_revision = _non_negative_int(
            snapshot.get("event_revision"), "snapshot.event_revision"
        )
        source = _protected_copy(snapshot.get("source"), authorized_scope, "source")
        if not source:
            raise ContractProjectionError(
                "authoritative source is required; static W004 fallback is disabled"
            )

        cells: dict[str, dict[str, Any]] = {}
        for raw_cell in _objects(snapshot.get("cells", []), "snapshot.cells"):
            cell = _protected_copy(raw_cell, authorized_scope, "cell")
            cell_id = _cell_id(cell)
            _assert_explicit_state(cell)
            cells[cell_id] = cell

        citations: dict[str, list[dict[str, Any]]] = {}
        for raw in _objects(snapshot.get("citations", []), "snapshot.citations"):
            citation = _protected_copy(raw, authorized_scope, "citation")
            citations.setdefault(_required_text(citation, "cell_id"), []).append(citation)

        evaluations: dict[str, dict[str, Any]] = {}
        for raw in _objects(snapshot.get("evaluations", []), "snapshot.evaluations"):
            evaluation = _protected_copy(raw, authorized_scope, "evaluation")
            evaluations[_required_text(evaluation, "cell_id")] = evaluation

        repairs = [
            _protected_copy(raw, authorized_scope, "repair")
            for raw in _objects(snapshot.get("repairs", []), "snapshot.repairs")
        ]
        traces = [
            _protected_copy(raw, authorized_scope, "trace")
            for raw in _objects(snapshot.get("trace_refs", []), "snapshot.trace_refs")
        ]
        resource_revisions = {f"run:{authorized_scope.run_id}": revision}
        raw_revisions = snapshot.get("resource_revisions", {})
        if raw_revisions is not None:
            if not isinstance(raw_revisions, Mapping):
                raise ContractProjectionError("snapshot.resource_revisions must be an object")
            for key, value in raw_revisions.items():
                resource_revisions[str(key)] = _non_negative_int(
                    value, f"snapshot.resource_revisions.{key}"
                )

        state = LiveCockpitState(
            scope=authorized_scope,
            revision=revision,
            last_event_revision=event_revision,
            source=source,
            phase=str(snapshot.get("phase", "unknown")),
            cells=cells,
            citations=citations,
            evaluations=evaluations,
            repairs=repairs,
            trace_refs=traces,
            resource_revisions=resource_revisions,
        )
        return cls(state)

    def apply_event(self, event: Mapping[str, Any]) -> bool:
        """Apply one canonical production ``EventEnvelope`` projection."""
        _require_contract(event)
        self.state.scope.assert_matches(event, label="event")
        event_id = _required_text(event, "event_id")
        if event_id in self.state.seen_event_ids:
            return False
        _required_text(event, "transition_id")
        _required_text(event, "occurred_at")
        event_schema_version = _non_negative_int(
            event.get("event_schema_version"), "event.event_schema_version"
        )
        if event_schema_version < 1:
            raise ContractProjectionError("event.event_schema_version must be >= 1")
        resource_type = _required_text(event, "resource_type")
        if resource_type not in RESOURCE_TYPES:
            raise ContractProjectionError(f"unknown canonical resource_type: {resource_type}")
        resource_id = _required_text(event, "resource_id")

        event_revision = _non_negative_int(event.get("event_revision"), "event.event_revision")
        result_revision = _non_negative_int(event.get("result_revision"), "event.result_revision")
        if event_revision <= self.state.last_event_revision:
            raise ContractProjectionError("stale/out-of-order event revision")
        revision_key = f"{resource_type}:{resource_id}"
        known_resource_revision = self.state.resource_revisions.get(revision_key)
        if known_resource_revision is not None and result_revision < known_resource_revision:
            raise ContractProjectionError("event regresses authoritative resource revision")

        event_type = _required_text(event, "event_type")
        payload = event.get("payload")
        if not isinstance(payload, Mapping):
            raise ContractProjectionError("event.payload must be an object")

        if event_type == "source.updated":
            self.state.source = _protected_copy(payload, self.state.scope, "event.source")
        elif event_type == "cell.updated":
            cell = _protected_copy(payload, self.state.scope, "event.cell")
            _assert_explicit_state(cell)
            self.state.cells[_cell_id(cell)] = cell
        elif event_type == "citation.attached":
            citation = _protected_copy(payload, self.state.scope, "event.citation")
            self.state.citations.setdefault(_required_text(citation, "cell_id"), []).append(citation)
        elif event_type == "evaluation.recorded":
            evaluation = _protected_copy(payload, self.state.scope, "event.evaluation")
            self.state.evaluations[_required_text(evaluation, "cell_id")] = evaluation
        elif event_type == "repair.recorded":
            self.state.repairs.append(_protected_copy(payload, self.state.scope, "event.repair"))
        elif event_type == "trace.linked":
            self.state.trace_refs.append(_protected_copy(payload, self.state.scope, "event.trace"))
        elif event_type == "run.phase_changed":
            self.state.scope.assert_matches(payload, label="event.phase")
            self.state.phase = _required_text(payload, "phase")
        else:
            raise ContractProjectionError(f"unsupported authoritative event type: {event_type}")

        self.state.resource_revisions[revision_key] = result_revision
        if resource_type == "run" and resource_id == self.state.scope.run_id:
            self.state.revision = result_revision
        self.state.last_event_revision = event_revision
        self.state.seen_event_ids.add(event_id)
        return True

    def replay(self, events: list[Mapping[str, Any]]) -> int:
        applied = 0
        for event in events:
            if self.apply_event(event):
                applied += 1
        return applied


def build_command(
    scope: AuthorizedScope,
    *,
    command_id: str,
    command_type: str,
    resource_type: str,
    resource_id: str,
    provenance: Mapping[str, Any],
    expected_revision: int,
    idempotency_key: str,
    issued_at: str,
    payload: Mapping[str, Any] | None = None,
    user_id: str | None = None,
) -> dict[str, Any]:
    """Build the exact canonical ``CommandEnvelope`` shape for a UI mutation."""
    if resource_type not in RESOURCE_TYPES:
        raise ContractProjectionError(f"unknown canonical resource_type: {resource_type}")
    if resource_type == "run" and resource_id != scope.run_id:
        raise AuthorizationProjectionError("run command is outside authorized run")
    if provenance.get("contract_version") != CONTRACT_VERSION:
        raise ContractProjectionError("command provenance must use contract version 1.0.0")
    command = {
        "contract_version": CONTRACT_VERSION,
        "command_id": _required_text({"command_id": command_id}, "command_id"),
        "command_type": _required_text({"command_type": command_type}, "command_type"),
        "org_id": scope.org_id,
        "workspace_id": scope.workspace_id,
        "resource_type": resource_type,
        "resource_id": _required_text({"resource_id": resource_id}, "resource_id"),
        "provenance": dict(provenance),
        "expected_revision": _non_negative_int(expected_revision, "command.expected_revision"),
        "idempotency_key": _required_text({"idempotency_key": idempotency_key}, "idempotency_key"),
        "issued_at": _required_text({"issued_at": issued_at}, "issued_at"),
    }
    if user_id is not None:
        command["user_id"] = _required_text({"user_id": user_id}, "user_id")
    if payload is not None:
        command["payload"] = dict(payload)
    return command


def render_candidate(candidate: str, state: LiveCockpitState) -> str:
    """Render either bakeoff shell from the exact same durable view model."""
    if candidate not in CANDIDATES:
        raise ValueError(f"unknown candidate: {candidate}")
    vm = state.view_model()
    cells = "".join(_render_cell(cell) for cell in vm["cells"])
    source_id = escape(str(vm["source"].get("source_id", "source")))
    phase = escape(str(vm["phase"]))
    workspace = escape(str(vm["workspace_id"]))
    shell_class = "hypermedia" if candidate == CANDIDATES[0] else "event-client"
    return (
        '<main data-contract="1.0.0" data-shell="' + shell_class + '">'
        '<h1>Live content cockpit</h1>'
        f'<nav aria-label="Workspace">Workspace: {workspace}</nav>'
        '<section aria-labelledby="source-heading"><h2 id="source-heading">Upload / source</h2>'
        '<label for="source-upload">Add source document</label>'
        '<input id="source-upload" type="file" data-command-type="source.upload" '
        'aria-describedby="source-help">'
        '<p id="source-help">Upload is submitted as the canonical production CommandEnvelope.</p>'
        f'<p>Current durable source: {source_id}</p></section>'
        '<section aria-labelledby="run-heading"><h2 id="run-heading">Live run</h2>'
        f'<p role="status" aria-live="polite">Run status: {phase}; revision {vm["revision"]}; '
        f'event revision {vm["event_revision"]}</p></section>'
        '<section aria-labelledby="grid-heading"><h2 id="grid-heading">3×3 outputs</h2>'
        '<div role="list" aria-label="Audience by format cells">' + cells + '</div></section>'
        '<p class="contract-note">State is projected only from the authorized durable snapshot and events.</p>'
        '</main>'
    )


def reconnect(
    authorized_scope: AuthorizedScope,
    snapshot: Mapping[str, Any],
    replay_events: list[Mapping[str, Any]],
) -> LiveCockpitProjector:
    """Rebuild from a server-authorized snapshot, then replay durable events.

    The server can use a canonical opaque ReplayCursor to choose the event range;
    the client projector never derives tenant/resource authority from that cursor.
    """
    projector = LiveCockpitProjector.from_snapshot(authorized_scope, snapshot)
    projector.replay(replay_events)
    return projector


def _render_cell(cell: Mapping[str, Any]) -> str:
    state = escape(str(cell.get("state", "NOT_RUN")))
    audience = escape(str(cell.get("audience", "unknown")))
    output_format = escape(str(cell.get("output_format", "unknown")))
    cell_id = escape(_cell_id(cell))
    detail = escape(str(cell.get("detail", "")))
    return (
        f'<article role="listitem" aria-labelledby="{cell_id}-title">'
        f'<h3 id="{cell_id}-title">{audience} · {output_format}</h3>'
        f'<p><strong>Status:</strong> {state}</p><p>{detail}</p></article>'
    )


def _require_contract(value: Mapping[str, Any]) -> None:
    if value.get("contract_version") != CONTRACT_VERSION:
        raise ContractProjectionError("unsupported production contract version")


def _objects(value: Any, label: str) -> list[Mapping[str, Any]]:
    if not isinstance(value, list):
        raise ContractProjectionError(f"{label} must be an array")
    if not all(isinstance(item, Mapping) for item in value):
        raise ContractProjectionError(f"{label} must contain objects")
    return list(value)


def _protected_copy(value: Any, scope: AuthorizedScope, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractProjectionError(f"{label} must be an object")
    scope.assert_matches(value, label=label)
    return dict(value)


def _required_text(value: Mapping[str, Any], key: str) -> str:
    text = str(value.get(key, "")).strip()
    if not text:
        raise ContractProjectionError(f"{key} is required")
    return text


def _non_negative_int(value: Any, label: str) -> int:
    if isinstance(value, bool):
        raise ContractProjectionError(f"{label} must be a non-negative integer")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ContractProjectionError(f"{label} must be a non-negative integer") from exc
    if number < 0:
        raise ContractProjectionError(f"{label} must be a non-negative integer")
    return number


def _cell_id(cell: Mapping[str, Any]) -> str:
    explicit = str(cell.get("cell_id", "")).strip()
    if explicit:
        return explicit
    audience = _required_text(cell, "audience")
    output_format = _required_text(cell, "output_format")
    return f"{audience}:{output_format}"


def _assert_explicit_state(cell: Mapping[str, Any]) -> None:
    state = _required_text(cell, "state")
    if state not in EXPLICIT_CELL_STATES:
        raise ContractProjectionError(f"cell state is not explicit/recognized: {state}")
