from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


JsonObject = dict[str, Any]


class EvidenceState(str, Enum):
    """Evidence posture exposed by the cockpit.

    The enum deliberately has no PASS/green aggregate. A caller must preserve
    every individual state so FAIL/REVIEW_REQUIRED/unknown evidence cannot be
    compensated by unrelated positive evidence.
    """

    PROVEN = "PROVEN"
    DIAGNOSTIC_ONLY = "DIAGNOSTIC_ONLY"
    NOT_COMPUTABLE = "NOT_COMPUTABLE"
    NOT_RUN = "NOT_RUN"
    NOT_COMPARABLE = "NOT_COMPARABLE"
    PRODUCTION_UNKNOWN = "PRODUCTION_UNKNOWN"
    FAIL = "FAIL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


@dataclass(frozen=True, slots=True)
class Provenance:
    source_id: str | None = None
    source_ref: str | None = None
    source_hash: str | None = None
    run_id: str | None = None
    job_id: str | None = None
    attempt: str | int | None = None
    evidence_ref: str | None = None
    observed_at: str | None = None
    evidence_scope: str | None = None

    def to_dict(self) -> JsonObject:
        return {
            "source_id": self.source_id,
            "source_ref": self.source_ref,
            "source_hash": self.source_hash,
            "run_id": self.run_id,
            "job_id": self.job_id,
            "attempt": self.attempt,
            "evidence_ref": self.evidence_ref,
            "observed_at": self.observed_at,
            "evidence_scope": self.evidence_scope,
        }


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    evidence_id: str
    label: str
    state: EvidenceState
    detail: str
    provenance: Provenance = field(default_factory=Provenance)
    metrics: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class JobEvidence:
    audience: str
    output_format: str
    job_id: str | None
    state: EvidenceState
    phase: str | None
    output: Mapping[str, Any] | None
    evaluation: Mapping[str, Any] | None
    error: str | None
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class RepairEvidence:
    job_id: str
    attempt_number: int | None
    before_output_hash: str | None
    after_output_hash: str | None
    before_evaluation: Mapping[str, Any] | None
    after_evaluation: Mapping[str, Any] | None
    resolved_failure_codes: tuple[str, ...]
    introduced_failure_codes: tuple[str, ...]
    fresh_hard_gate_runs: bool | None
    siblings_immutable: bool | None
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class TelemetryEvidence:
    run_id: str | None
    event_count: int | None
    stage_latency: Mapping[str, Any]
    transport_retries: Mapping[str, Any]
    quality_repairs: Mapping[str, Any]
    usage: Mapping[str, Any] | None
    observed_cost: Any
    raw_observed_cost: Any
    cost_evidence_state: EvidenceState
    terminal: Mapping[str, Any]
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class CockpitSnapshot:
    run_id: str | None
    source: Mapping[str, Any]
    evidence_scope: str | None
    task_attempt_id: str | None
    jobs: tuple[JobEvidence, ...]
    repairs: tuple[RepairEvidence, ...]
    telemetry: TelemetryEvidence | None
    evidence_items: tuple[EvidenceItem, ...]
    artifact_refs: Mapping[str, str]

    @property
    def has_failures(self) -> bool:
        return any(item.state is EvidenceState.FAIL for item in self.jobs + self.evidence_items)

    @property
    def needs_review(self) -> bool:
        return any(
            item.state is EvidenceState.REVIEW_REQUIRED
            for item in self.jobs + self.evidence_items
        )
