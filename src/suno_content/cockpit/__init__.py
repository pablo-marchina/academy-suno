"""Evidence cockpit over existing versioned run/eval artifacts."""

from .adapters import (
    build_cockpit_snapshot,
    load_json_artifact,
    load_run_state_from_history,
    load_run_state_from_sqlite,
)
from .live import (
    AuthorizationProjectionError,
    AuthorizedScope,
    CANDIDATES,
    ContractProjectionError,
    LiveCockpitProjector,
    LiveCockpitState,
    reconnect,
    render_candidate,
)
from .models import (
    CockpitSnapshot,
    EvidenceItem,
    EvidenceState,
    JobEvidence,
    Provenance,
    RepairEvidence,
    TelemetryEvidence,
)
from .render import render_html

__all__ = [
    "AuthorizationProjectionError",
    "AuthorizedScope",
    "CANDIDATES",
    "CockpitSnapshot",
    "ContractProjectionError",
    "EvidenceItem",
    "EvidenceState",
    "JobEvidence",
    "LiveCockpitProjector",
    "LiveCockpitState",
    "Provenance",
    "RepairEvidence",
    "TelemetryEvidence",
    "build_cockpit_snapshot",
    "load_json_artifact",
    "load_run_state_from_history",
    "load_run_state_from_sqlite",
    "reconnect",
    "render_candidate",
    "render_html",
]
