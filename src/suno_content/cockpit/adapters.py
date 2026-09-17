from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .models import (
    CockpitSnapshot,
    EvidenceItem,
    EvidenceState,
    JobEvidence,
    Provenance,
    RepairEvidence,
    TelemetryEvidence,
)

AUDIENCES = ("beginner", "intermediate", "advanced")
FORMATS = ("article", "carousel", "short_video")


def load_json_artifact(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl_artifact(path: str | Path) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"JSONL row {number} must be an object")
        rows.append(value)
    return tuple(rows)


def load_run_state_from_history(path: str | Path) -> tuple[dict[str, Any], str | None]:
    payload = load_json_artifact(path)
    if not isinstance(payload, list) or not payload:
        raise ValueError("RunStore history artifact must be a non-empty list")
    final = payload[-1]
    if not isinstance(final, Mapping) or not isinstance(final.get("state"), Mapping):
        raise ValueError("RunStore history final row must contain an object state")
    return dict(final["state"]), None if final.get("created_at") is None else str(final["created_at"])


def load_run_state_from_sqlite(path: str | Path, run_id: str) -> dict[str, Any]:
    # Keep the canonical RunStore as the only SQLite schema owner.
    from suno_content.runstore import SQLiteRunStore

    return SQLiteRunStore(path).load(run_id)


def _norm(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    return {
        "iniciante": "beginner",
        "intermediario": "intermediate",
        "intermediário": "intermediate",
        "avancado": "advanced",
        "avançado": "advanced",
        "texto": "article",
        "shortvideo": "short_video",
        "video_curto": "short_video",
        "vídeo_curto": "short_video",
    }.get(text, text)


def _source_value(source: Mapping[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = source.get(key)
        if value not in (None, ""):
            return str(value)
    return None


def _prov(
    source: Mapping[str, Any],
    run_id: str | None,
    scope: str | None,
    *,
    job_id: str | None = None,
    attempt: str | int | None = None,
    evidence_ref: str | None = None,
    observed_at: str | None = None,
) -> Provenance:
    return Provenance(
        source_id=_source_value(source, "source_id", "document_id", "id"),
        source_ref=_source_value(source, "source_ref", "uri", "url", "path"),
        source_hash=_source_value(source, "source_hash", "sha256", "content_hash"),
        run_id=run_id,
        job_id=job_id,
        attempt=attempt,
        evidence_ref=evidence_ref,
        observed_at=observed_at,
        evidence_scope=scope,
    )


def _dimensions(job_id: str, branch: Mapping[str, Any]) -> tuple[str | None, str | None]:
    payload = branch.get("payload") if isinstance(branch.get("payload"), Mapping) else {}
    output = branch.get("output") if isinstance(branch.get("output"), Mapping) else {}
    audience = _norm(payload.get("audience") or payload.get("audience_level") or output.get("audience"))
    output_format = _norm(payload.get("format") or payload.get("output_format") or output.get("format"))
    if ":" in job_id:
        left, right = job_id.split(":", 1)
        audience, output_format = audience or _norm(left), output_format or _norm(right)
    return audience, output_format


def _branch_state(branch: Mapping[str, Any]) -> EvidenceState:
    phase = _norm(branch.get("phase"))
    evaluation = branch.get("evaluation") if isinstance(branch.get("evaluation"), Mapping) else {}
    action = _norm(evaluation.get("action"))
    if phase == "failed" or action == "fail":
        return EvidenceState.FAIL
    if phase == "review_required" or action == "review_required":
        return EvidenceState.REVIEW_REQUIRED
    if phase in {"accepted", "repaired"} or action == "pass":
        return EvidenceState.PROVEN
    if phase in {"generated", "needs_repair"} or action == "repair":
        return EvidenceState.REVIEW_REQUIRED
    return EvidenceState.NOT_RUN


def _attempts(events: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for event in events:
        if event.get("job_id") is None or event.get("operation_attempt") is None:
            continue
        try:
            attempt = int(event["operation_attempt"])
        except (TypeError, ValueError):
            continue
        job_id = str(event["job_id"])
        result[job_id] = max(result.get(job_id, 0), attempt)
    return result


def _proof_state(raw: Any) -> EvidenceState | None:
    text = str(raw or "").upper()
    for state in EvidenceState:
        if text.startswith(state.value):
            return state
    return None


def _evidence_items(
    proof: Mapping[str, Any] | None,
    calibration: Mapping[str, Any] | None,
    source: Mapping[str, Any],
    run_id: str | None,
    scope: str | None,
    refs: Mapping[str, str],
) -> tuple[EvidenceItem, ...]:
    items: dict[str, EvidenceItem] = {}

    def add(evidence_id: str, label: str, state: EvidenceState, detail: str, ref_key: str) -> None:
        item = EvidenceItem(
            evidence_id=evidence_id,
            label=label,
            state=state,
            detail=detail,
            provenance=_prov(source, run_id, scope, evidence_ref=refs.get(ref_key)),
        )
        # Proof classifications are downstream/specific and win on duplicate ids.
        if evidence_id not in items or ref_key == "proof_report":
            items[evidence_id] = item

    if proof and isinstance(proof.get("evidence_classification"), Mapping):
        for key, raw in proof["evidence_classification"].items():
            state = _proof_state(raw)
            if state is not None:
                add(str(key), str(key).replace("_", " ").title(), state, str(raw), "proof_report")

    calibration = calibration or {}
    rows, agreement = calibration.get("audience_rows"), calibration.get("independent_agreement")
    if not isinstance(rows, list) or not rows or agreement is None:
        add(
            "audience_human_calibration",
            "Independent human audience calibration",
            EvidenceState.NOT_COMPUTABLE,
            "Independent human labels/agreement are absent; confusion matrices and threshold freeze remain N/A.",
            "calibration",
        )
    else:
        add(
            "audience_human_calibration",
            "Independent human audience calibration",
            EvidenceState.DIAGNOSTIC_ONLY,
            "Human rows exist; no threshold readiness is promoted without an explicit versioned gate.",
            "calibration",
        )

    anti = calibration.get("anti_gaming_cases")
    add(
        "anti_gaming_contract",
        "Anti-gaming contract",
        EvidenceState.PROVEN if isinstance(anti, list) and anti else EvidenceState.NOT_RUN,
        f"{len(anti)} versioned anti-gaming cases are referenced." if isinstance(anti, list) and anti else "No anti-gaming evidence selected.",
        "calibration",
    )

    semantic = calibration.get("semantic_rows")
    if not isinstance(semantic, list) or not semantic:
        add("semantic_ablation", "Semantic backend ablation", EvidenceState.NOT_RUN, "No semantic off/on rows; no backend preference is justified.", "calibration")

    provider_rows = calibration.get("provider_rows")
    comparable = [
        row
        for row in provider_rows or []
        if isinstance(row, Mapping)
        and bool(row.get("quality_observed"))
        and bool(row.get("latency_observed"))
        and str(row.get("pricing_provenance", "")).upper() not in {"", "SYNTHETIC"}
    ] if isinstance(provider_rows, list) else []
    add(
        "provider_comparison",
        "Provider/model comparison",
        EvidenceState.DIAGNOSTIC_ONLY if len(comparable) >= 2 else EvidenceState.NOT_COMPARABLE,
        f"{len(comparable)} comparable real-provider rows." if len(comparable) >= 2 else "Fewer than two comparable real-provider rows; no preference is justified.",
        "calibration",
    )
    if not comparable:
        add(
            "real_provider_quality_cost",
            "Real provider quality / usage / cost",
            EvidenceState.PRODUCTION_UNKNOWN,
            "Real-provider quality and versioned commercial cost remain unknown for production claims.",
            "calibration",
        )
    return tuple(items.values())


def _jobs(
    run_state: Mapping[str, Any],
    telemetry: Mapping[str, Any] | None,
    events: Iterable[Mapping[str, Any]],
    source: Mapping[str, Any],
    run_id: str | None,
    scope: str | None,
    observed_at: str | None,
    refs: Mapping[str, str],
) -> tuple[JobEvidence, ...]:
    branches: dict[str, Mapping[str, Any]] = {}
    if isinstance(run_state.get("jobs"), Mapping):
        branches.update({str(k): v for k, v in run_state["jobs"].items() if isinstance(v, Mapping)})
    terminal = telemetry.get("terminal") if telemetry and isinstance(telemetry.get("terminal"), Mapping) else {}
    telemetry_branches = terminal.get("branch_states") if isinstance(terminal, Mapping) else {}
    if isinstance(telemetry_branches, Mapping):
        for job_id, branch in telemetry_branches.items():
            if isinstance(branch, Mapping):
                branches.setdefault(str(job_id), branch)

    by_dim: dict[tuple[str, str], tuple[str, Mapping[str, Any]]] = {}
    for job_id, branch in branches.items():
        audience, output_format = _dimensions(job_id, branch)
        if audience in AUDIENCES and output_format in FORMATS:
            by_dim[(audience, output_format)] = (job_id, branch)
    event_attempts = _attempts(events)

    result: list[JobEvidence] = []
    for audience in AUDIENCES:
        for output_format in FORMATS:
            match = by_dim.get((audience, output_format))
            if match is None:
                result.append(JobEvidence(audience, output_format, None, EvidenceState.NOT_RUN, None, None, None, None, _prov(source, run_id, scope, evidence_ref=refs.get("runstore"), observed_at=observed_at)))
                continue
            job_id, branch = match
            output = branch.get("output") if isinstance(branch.get("output"), Mapping) else None
            evaluation = branch.get("evaluation") if isinstance(branch.get("evaluation"), Mapping) else None
            attempt: str | int | None = event_attempts.get(job_id)
            if attempt is None and output and output.get("repair_attempt") is not None:
                attempt = output["repair_attempt"]
            result.append(
                JobEvidence(
                    audience,
                    output_format,
                    job_id,
                    _branch_state(branch),
                    None if branch.get("phase") is None else str(branch["phase"]),
                    output,
                    evaluation,
                    None if branch.get("error") is None else str(branch["error"]),
                    _prov(source, run_id, scope, job_id=job_id, attempt=attempt, evidence_ref=refs.get("runstore") or refs.get("telemetry"), observed_at=observed_at),
                )
            )
    return tuple(result)


def _repairs(
    proof: Mapping[str, Any] | None,
    source: Mapping[str, Any],
    run_id: str | None,
    scope: str | None,
    refs: Mapping[str, str],
) -> tuple[RepairEvidence, ...]:
    rows = proof.get("repair_lineage") if proof else None
    if not isinstance(rows, list):
        return ()
    result: list[RepairEvidence] = []
    for row in rows:
        if not isinstance(row, Mapping) or row.get("job_id") is None:
            continue
        try:
            attempt = None if row.get("attempt_number") is None else int(row["attempt_number"])
        except (TypeError, ValueError):
            attempt = None
        job_id = str(row["job_id"])
        result.append(
            RepairEvidence(
                job_id=job_id,
                attempt_number=attempt,
                before_output_hash=None if row.get("before_output_hash") is None else str(row["before_output_hash"]),
                after_output_hash=None if row.get("after_output_hash") is None else str(row["after_output_hash"]),
                before_evaluation=dict(row["before_snapshot_serialized"]) if isinstance(row.get("before_snapshot_serialized"), Mapping) else None,
                after_evaluation=dict(row["after_snapshot"]) if isinstance(row.get("after_snapshot"), Mapping) else None,
                resolved_failure_codes=tuple(str(x) for x in row.get("resolved_failure_codes", ())),
                introduced_failure_codes=tuple(str(x) for x in row.get("introduced_failure_codes", ())),
                fresh_hard_gate_runs=None if row.get("fresh_hard_gate_runs") is None else bool(row["fresh_hard_gate_runs"]),
                siblings_immutable=None if row.get("siblings_immutable") is None else bool(row["siblings_immutable"]),
                provenance=_prov(source, run_id, scope, job_id=job_id, attempt=attempt, evidence_ref=refs.get("proof_report")),
            )
        )
    return tuple(result)


def _synthetic_pricing(calibration: Mapping[str, Any] | None, run_id: str | None) -> bool:
    rows = calibration.get("provider_rows") if calibration else None
    if not isinstance(rows, list):
        return False
    rows = [row for row in rows if isinstance(row, Mapping)]
    matching = [row for row in rows if run_id is not None and str(row.get("candidate_id")) == run_id]
    candidates = matching or rows
    return bool(candidates) and all(str(row.get("pricing_provenance", "")).upper() == "SYNTHETIC" for row in candidates)


def _telemetry(
    summary: Mapping[str, Any] | None,
    calibration: Mapping[str, Any] | None,
    source: Mapping[str, Any],
    run_id: str | None,
    scope: str | None,
    observed_at: str | None,
    refs: Mapping[str, str],
) -> TelemetryEvidence | None:
    if summary is None:
        return None
    telemetry_run_id = run_id or (None if summary.get("run_id") is None else str(summary["run_id"]))
    raw_cost = summary.get("observed_cost")
    synthetic = _synthetic_pricing(calibration, telemetry_run_id)
    cost_state = EvidenceState.PRODUCTION_UNKNOWN if raw_cost is None else (EvidenceState.DIAGNOSTIC_ONLY if synthetic else EvidenceState.PROVEN)
    mapping = lambda key: dict(summary[key]) if isinstance(summary.get(key), Mapping) else {}
    return TelemetryEvidence(
        run_id=telemetry_run_id,
        event_count=None if summary.get("event_count") is None else int(summary["event_count"]),
        stage_latency=mapping("stage_latency"),
        transport_retries=mapping("transport_retries"),
        quality_repairs=mapping("quality_repairs"),
        usage=dict(summary["usage"]) if isinstance(summary.get("usage"), Mapping) else None,
        observed_cost=None if synthetic else raw_cost,
        raw_observed_cost=raw_cost,
        cost_evidence_state=cost_state,
        terminal=mapping("terminal"),
        provenance=_prov(source, telemetry_run_id, scope, evidence_ref=refs.get("telemetry"), observed_at=observed_at),
    )


def build_cockpit_snapshot(
    *,
    run_state: Mapping[str, Any] | None = None,
    telemetry_summary: Mapping[str, Any] | None = None,
    telemetry_events: Iterable[Mapping[str, Any]] = (),
    calibration: Mapping[str, Any] | None = None,
    proof_report: Mapping[str, Any] | None = None,
    task_attempt_id: str | None = None,
    observed_at: str | None = None,
    artifact_refs: Mapping[str, str] | None = None,
) -> CockpitSnapshot:
    """Derive a read-only view; never persist a second evidence truth store."""

    run_state = run_state or {}
    refs = dict(artifact_refs or {})
    source = dict(run_state["source"]) if isinstance(run_state.get("source"), Mapping) else {}
    run_id = None if run_state.get("run_id") is None else str(run_state["run_id"])
    if run_id is None and proof_report and proof_report.get("run_id") is not None:
        run_id = str(proof_report["run_id"])
    if run_id is None and telemetry_summary and telemetry_summary.get("run_id") is not None:
        run_id = str(telemetry_summary["run_id"])
    metadata = run_state.get("metadata") if isinstance(run_state.get("metadata"), Mapping) else {}
    scope_raw = metadata.get("evidence_scope") or source.get("evidence_scope") or (proof_report or {}).get("evidence_scope")
    scope = None if scope_raw is None else str(scope_raw)
    if not source and proof_report and isinstance(proof_report.get("source"), Mapping):
        source = dict(proof_report["source"])
    events = tuple(event for event in telemetry_events if isinstance(event, Mapping))
    return CockpitSnapshot(
        run_id=run_id,
        source=source,
        evidence_scope=scope,
        task_attempt_id=task_attempt_id,
        jobs=_jobs(run_state, telemetry_summary, events, source, run_id, scope, observed_at, refs),
        repairs=_repairs(proof_report, source, run_id, scope, refs),
        telemetry=_telemetry(telemetry_summary, calibration, source, run_id, scope, observed_at, refs),
        evidence_items=_evidence_items(proof_report, calibration, source, run_id, scope, refs),
        artifact_refs=refs,
    )
