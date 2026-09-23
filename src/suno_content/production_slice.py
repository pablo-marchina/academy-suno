from __future__ import annotations

import asyncio
import hashlib
import json
import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from suno_content.cockpit import AuthorizedScope, LiveCockpitProjector, reconnect
from suno_content.ingest import PdfParserAdapter, UploadRoute, ingest_controlled_pdf_bytes
from suno_content.orchestration import (
    AsyncGraphOrchestrator,
    EvaluationAction,
    JobSpec,
    QualityDecision,
    RunPhase,
    RunState,
)
from suno_content.runstore import SQLiteDurableStateEventStore, SQLiteRunStore
from suno_content.security import (
    AccessSurface,
    Action,
    BrowserCredentialPolicy,
    BrowserRequestCredential,
    DenyByDefaultAuthorizer,
    Membership,
    PrincipalBinding,
    Role,
    SecurityDirectory,
    TenantResource,
)


REFERENCE_RUNTIME = "plain_async+SQLiteRunStore:REFERENCE_NON_PRODUCTION"
REFERENCE_DATABASE = "SQLiteDurableStateEventStore:REFERENCE_NON_PRODUCTION"
REFERENCE_FRONTEND = "LiveCockpitProjector:FRAMEWORK_NEUTRAL_REFERENCE"
PRODUCTION_RUNTIME_LOCK = "NONE"
PRODUCTION_DATABASE_LOCK = "NONE"
PRODUCTION_PARSER_LOCK = "NONE"
PRODUCTION_FRONTEND_LOCK = "NONE"


class VerticalSliceError(RuntimeError):
    pass


class SourceNotReadyError(VerticalSliceError):
    pass


class ProductionQualificationError(VerticalSliceError):
    pass


@dataclass(frozen=True, slots=True)
class SliceIdentity:
    org_id: str
    workspace_id: str
    user_id: str
    session_id: str
    csrf_token: str


@dataclass(frozen=True, slots=True)
class VerticalSliceEvidence:
    run_id: str
    phase: str
    source_id: str
    source_hash: str
    job_ids: tuple[str, ...]
    accepted_branches: int
    event_count: int
    last_event_revision: int
    aggregate_digest: str
    runtime: str = REFERENCE_RUNTIME
    database: str = REFERENCE_DATABASE
    frontend: str = REFERENCE_FRONTEND
    production_ready_claim: str = "NOT_AUTHORIZED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "phase": self.phase,
            "source_id": self.source_id,
            "source_hash": self.source_hash,
            "job_ids": list(self.job_ids),
            "accepted_branches": self.accepted_branches,
            "event_count": self.event_count,
            "last_event_revision": self.last_event_revision,
            "aggregate_digest": self.aggregate_digest,
            "runtime": self.runtime,
            "database": self.database,
            "frontend": self.frontend,
            "production_ready_claim": self.production_ready_claim,
            "production_locks": {
                "runtime": PRODUCTION_RUNTIME_LOCK,
                "database": PRODUCTION_DATABASE_LOCK,
                "parser": PRODUCTION_PARSER_LOCK,
                "frontend": PRODUCTION_FRONTEND_LOCK,
            },
        }


class ReferenceVerticalSlice:
    """One integrated product path over accepted portable/reference contracts.

    This composes the real security, controlled-ingest, durable orchestration,
    state/event, and live-cockpit implementations already accepted in W006.
    SQLite and the plain-async runtime remain explicitly reference-only; this
    class therefore cannot authorize a production-ready claim.
    """

    RUN_DB = "run-state.sqlite3"
    EVENT_DB = "product-events.sqlite3"

    def __init__(self, root: str | Path, *, parser: PdfParserAdapter):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.parser = parser
        self.run_store = SQLiteRunStore(self.root / self.RUN_DB)
        self.event_store = SQLiteDurableStateEventStore(self.root / self.EVENT_DB)

    @staticmethod
    def assert_production_qualified() -> None:
        raise ProductionQualificationError(
            "production qualification is fail-closed: runtime/database/parser/frontend locks remain NONE"
        )

    def _authorize_upload(self, identity: SliceIdentity, *, provenance_id: str) -> None:
        directory = SecurityDirectory()
        directory.bind_principal(
            PrincipalBinding(
                issuer="reference-idp",
                subject=identity.user_id,
                user_id=identity.user_id,
            )
        )
        directory.put_membership(
            Membership(
                membership_id=f"membership:{identity.user_id}:{identity.workspace_id}",
                user_id=identity.user_id,
                org_id=identity.org_id,
                workspace_id=identity.workspace_id,
                role=Role.EDITOR,
            )
        )
        directory.create_session(
            session_id=identity.session_id,
            user_id=identity.user_id,
            org_id=identity.org_id,
            workspace_id=identity.workspace_id,
            csrf_token=identity.csrf_token,
        )
        context = BrowserCredentialPolicy(directory).authenticate(
            BrowserRequestCredential(
                method="POST",
                session_cookie=identity.session_id,
                same_origin=True,
                csrf_header=identity.csrf_token,
            )
        )
        DenyByDefaultAuthorizer(directory).require(
            context,
            TenantResource(
                surface=AccessSurface.OBJECT,
                org_id=identity.org_id,
                workspace_id=identity.workspace_id,
                resource_id=f"upload:{provenance_id}",
                provenance_id=provenance_id,
            ),
            Action.OBJECT_WRITE,
        )

    @staticmethod
    def _planner_from_cells(cells: list[dict[str, Any]]):
        def planner(_: dict[str, Any]) -> list[JobSpec]:
            return [JobSpec(cell["job_id"], dict(cell)) for cell in cells]

        return planner

    @staticmethod
    def _generator(job: JobSpec, source: dict[str, Any]) -> Mapping[str, Any]:
        return {
            "org_id": source["org_id"],
            "workspace_id": source["workspace_id"],
            "run_id": source["run_id"],
            "cell_id": job.job_id,
            "job_id": job.job_id,
            "attempt_id": f"{job.job_id}:attempt:1",
            "audience": job.payload["audience"],
            "output_format": job.payload["output_format"],
            "state": "PROVEN",
            "detail": job.payload["preview"],
            "source_id": source["source_id"],
            "source_hash": source["source_hash"],
        }

    @staticmethod
    def _evaluator(job: JobSpec, output: Mapping[str, Any]) -> QualityDecision:
        if output.get("job_id") != job.job_id or not output.get("source_hash"):
            return QualityDecision(
                EvaluationAction.FAIL,
                reasons=("identity_or_provenance_mismatch",),
            )
        return QualityDecision(EvaluationAction.PASS)

    @staticmethod
    def _repairer(
        job: JobSpec,
        output: Mapping[str, Any],
        decision: QualityDecision,
        attempt: int,
    ) -> Mapping[str, Any]:
        repaired = dict(output)
        repaired["attempt_id"] = f"{job.job_id}:repair:{attempt}"
        repaired["repair_reasons"] = list(decision.reasons)
        return repaired

    @staticmethod
    def _aggregator(outputs: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
        ordered = {job_id: dict(outputs[job_id]) for job_id in sorted(outputs)}
        payload = json.dumps(ordered, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return {
            "accepted_branch_count": len(ordered),
            "job_ids": list(ordered),
            "outputs": ordered,
            "deterministic_digest": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        }

    def _orchestrator(self, *, cells: list[dict[str, Any]] | None = None) -> AsyncGraphOrchestrator:
        planner = self._planner_from_cells(cells or [])
        return AsyncGraphOrchestrator(
            store=self.run_store,
            planner=planner,
            generator=self._generator,
            evaluator=self._evaluator,
            repairer=self._repairer,
            aggregator=self._aggregator,
        )

    async def start(
        self,
        *,
        run_id: str,
        identity: SliceIdentity,
        raw_pdf: bytes,
        artifact_label: str,
        source_group_key: str,
        pause_after: str | None = None,
    ) -> RunState:
        controlled = ingest_controlled_pdf_bytes(
            raw_pdf,
            artifact_label=artifact_label,
            source_group_key=source_group_key,
            parser=self.parser,
        )
        if controlled.upload.route is not UploadRoute.SOURCE_READY or controlled.ingest is None:
            raise SourceNotReadyError(
                f"controlled source did not clear trust gate: {controlled.upload.route.value}"
            )
        self._authorize_upload(identity, provenance_id=controlled.upload.provenance_ref)
        ingest = controlled.ingest
        cells = [
            {
                "audience": cell.audience,
                "output_format": cell.output_format,
                "job_id": cell.job_id,
                "preview": cell.preview,
            }
            for cell in ingest.cells
        ]
        source = {
            "org_id": identity.org_id,
            "workspace_id": identity.workspace_id,
            "run_id": run_id,
            "source_id": ingest.source.source_id,
            "source_hash": ingest.source_hash,
            "source_group_id": controlled.upload.source_group_id,
            "provenance_ref": controlled.upload.provenance_ref,
            "artifact_label": controlled.upload.artifact_label,
            "parser_name": ingest.parser_name,
            "parser_version": ingest.parser_version,
        }
        return await self._orchestrator(cells=cells).start(
            run_id=run_id,
            source=source,
            metadata={
                "substrate_posture": "REFERENCE_NON_PRODUCTION",
                "production_ready_claim": "NOT_AUTHORIZED",
            },
            pause_after=pause_after,
        )

    async def resume(self, run_id: str, *, pause_after: str | None = None) -> RunState:
        return await self._orchestrator().resume(run_id, pause_after=pause_after)

    def publish_authoritative_events(self, state: RunState) -> tuple[dict[str, Any], ...]:
        if state.phase is not RunPhase.COMPLETE or state.aggregate is None:
            raise VerticalSliceError("authoritative final events require a COMPLETE run")
        source = dict(state.source)
        org_id = str(source["org_id"])
        workspace_id = str(source["workspace_id"])
        run_id = state.run_id
        source_payload = {
            "org_id": org_id,
            "workspace_id": workspace_id,
            "run_id": run_id,
            "source_id": source["source_id"],
            "source_hash": source["source_hash"],
            "source_group_id": source["source_group_id"],
            "provenance_ref": source["provenance_ref"],
        }
        self.event_store.commit(
            org_id=org_id,
            workspace_id=workspace_id,
            run_id=run_id,
            resource_type="document",
            resource_id=str(source["source_id"]),
            expected_revision=0,
            expected_ownership_epoch=0,
            mutation_id=f"t009:{run_id}:source",
            state=source_payload,
            event_type="source.updated",
            payload=source_payload,
        )
        for job_id in sorted(state.joined_outputs):
            cell = dict(state.joined_outputs[job_id])
            self.event_store.commit(
                org_id=org_id,
                workspace_id=workspace_id,
                run_id=run_id,
                resource_type="branch",
                resource_id=job_id,
                expected_revision=0,
                expected_ownership_epoch=0,
                mutation_id=f"t009:{run_id}:cell:{job_id}",
                state=cell,
                event_type="cell.updated",
                payload=cell,
            )
        phase_payload = {
            "org_id": org_id,
            "workspace_id": workspace_id,
            "run_id": run_id,
            "phase": state.phase.value,
        }
        self.event_store.commit(
            org_id=org_id,
            workspace_id=workspace_id,
            run_id=run_id,
            resource_type="run",
            resource_id=run_id,
            expected_revision=0,
            expected_ownership_epoch=0,
            mutation_id=f"t009:{run_id}:complete",
            state={**phase_payload, "aggregate": dict(state.aggregate)},
            event_type="run.phase_changed",
            payload=phase_payload,
        )
        return self.event_store.replay_events(
            org_id=org_id,
            workspace_id=workspace_id,
            run_id=run_id,
        )

    def live_projection(self, state: RunState) -> LiveCockpitProjector:
        events = list(self.publish_authoritative_events(state))
        source = dict(state.source)
        scope = AuthorizedScope(
            org_id=str(source["org_id"]),
            workspace_id=str(source["workspace_id"]),
            run_id=state.run_id,
        )
        snapshot = {
            "contract_version": "1.0.0",
            "org_id": scope.org_id,
            "workspace_id": scope.workspace_id,
            "run_id": scope.run_id,
            "revision": 0,
            "event_revision": 0,
            "phase": "created",
            "source": {
                "org_id": scope.org_id,
                "workspace_id": scope.workspace_id,
                "run_id": scope.run_id,
                "source_id": source["source_id"],
                "source_hash": source["source_hash"],
                "provenance_ref": source["provenance_ref"],
            },
            "cells": [],
            "citations": [],
            "evaluations": [],
            "repairs": [],
            "trace_refs": [],
        }
        return reconnect(scope, snapshot, events)

    def evidence(self, state: RunState) -> VerticalSliceEvidence:
        projector = self.live_projection(state)
        events = self.event_store.replay_events(
            org_id=str(state.source["org_id"]),
            workspace_id=str(state.source["workspace_id"]),
            run_id=state.run_id,
        )
        aggregate = dict(state.aggregate or {})
        return VerticalSliceEvidence(
            run_id=state.run_id,
            phase=state.phase.value,
            source_id=str(state.source["source_id"]),
            source_hash=str(state.source["source_hash"]),
            job_ids=tuple(sorted(state.jobs)),
            accepted_branches=len(state.joined_outputs),
            event_count=len(events),
            last_event_revision=projector.state.last_event_revision,
            aggregate_digest=str(aggregate.get("deterministic_digest", "")),
        )

    @staticmethod
    def _backup_sqlite(source: Path, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        src = sqlite3.connect(str(source))
        dst = sqlite3.connect(str(destination))
        try:
            src.backup(dst)
            row = dst.execute("PRAGMA integrity_check").fetchone()
            if row is None or str(row[0]).lower() != "ok":
                raise VerticalSliceError(f"backup integrity check failed: {destination.name}")
        finally:
            dst.close()
            src.close()

    def backup_to(self, destination: str | Path) -> Path:
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        self._backup_sqlite(self.root / self.RUN_DB, destination / self.RUN_DB)
        self.event_store.backup_to(destination / self.EVENT_DB)
        return destination

    @classmethod
    def restore_from_backup(
        cls,
        backup_root: str | Path,
        destination: str | Path,
        *,
        parser: PdfParserAdapter,
    ) -> "ReferenceVerticalSlice":
        backup_root = Path(backup_root)
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        for name in (cls.RUN_DB, cls.EVENT_DB):
            source = backup_root / name
            if not source.is_file():
                raise VerticalSliceError(f"backup missing {name}")
            shutil.copy2(source, destination / name)
        restored = cls(destination, parser=parser)
        for name in (cls.RUN_DB, cls.EVENT_DB):
            connection = sqlite3.connect(str(destination / name))
            try:
                row = connection.execute("PRAGMA integrity_check").fetchone()
                if row is None or str(row[0]).lower() != "ok":
                    raise VerticalSliceError(f"restore integrity check failed: {name}")
            finally:
                connection.close()
        return restored


def run(coro: Any) -> Any:
    """Tiny synchronous bridge for scripts/evidence capture."""
    return asyncio.run(coro)
