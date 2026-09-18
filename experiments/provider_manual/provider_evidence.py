#!/usr/bin/env python3
"""Versioned export/validation contract for manual provider mechanics evidence."""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "provider-observed-evidence-v1"
SOURCE_SCHEMA_VERSION = "provider-probe-v1"
NA = "N/A"
BANNED_SECRET_KEYS = {"api_key", "authorization", "credential", "secret", "access_token", "bearer"}


def _walk_keys(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in BANNED_SECRET_KEYS or lowered.endswith("_api_key") or lowered.endswith("_secret"):
                findings.append(f"{path}.{key}")
            findings.extend(_walk_keys(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_walk_keys(child, f"{path}[{index}]"))
    return findings


def _required_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value != NA


def _observed_usage(usage: dict[str, Any]) -> bool:
    return (
        usage.get("observed") is True
        and isinstance(usage.get("input_tokens"), int)
        and isinstance(usage.get("output_tokens"), int)
        and isinstance(usage.get("total_tokens"), int)
    )


def _eligible_pricing(pricing: dict[str, Any]) -> bool:
    return all(
        [
            pricing.get("commercial_evidence_eligible") is True,
            pricing.get("kind") == "official_provider_pricing",
            _required_text(pricing.get("source_url")),
            _required_text(pricing.get("retrieved_at")),
            _required_text(pricing.get("effective_at")),
            _required_text(pricing.get("currency")),
        ]
    )


def _eligible_cost(cost: dict[str, Any], pricing: dict[str, Any]) -> bool:
    return (
        _eligible_pricing(pricing)
        and cost.get("derived") is True
        and isinstance(cost.get("value"), (int, float))
        and _required_text(cost.get("currency"))
    )


def _mechanics_reasons(probe: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if probe.get("status") != "OBSERVED_RUN":
        reasons.append("run_status_not_observed")
    for field in ("provider", "provider_protocol", "model", "model_version", "endpoint", "captured_at"):
        if not _required_text(probe.get(field)):
            reasons.append(f"missing_{field}")
    latency = probe.get("latency_ms")
    if not isinstance(latency, (int, float)) or latency < 0:
        reasons.append("latency_not_observed")
    usage = probe.get("usage") or {}
    if not _observed_usage(usage):
        reasons.append("provider_usage_not_observed")
    pricing = probe.get("pricing_provenance") or {}
    if not _eligible_pricing(pricing):
        reasons.append("official_pricing_provenance_ineligible")
    cost = probe.get("cost") or {}
    if not _eligible_cost(cost, pricing):
        reasons.append("cost_not_derived_from_observed_usage_and_official_pricing")
    if probe.get("content_quality_evidence") is not False:
        reasons.append("mechanics_artifact_must_not_embed_content_quality")
    response = probe.get("response") or {}
    if not _required_text(response.get("sha256")):
        reasons.append("response_fingerprint_missing")
    return reasons


def export_probe(probe: dict[str, Any]) -> dict[str, Any]:
    """Convert a T004 provider probe into the downstream-stable T007 mechanics contract."""
    reasons = _mechanics_reasons(probe)
    observed = probe.get("status") == "OBSERVED_RUN"
    fingerprint_seed = "|".join(
        str(probe.get(k, NA)) for k in ("provider", "model", "model_version", "captured_at")
    ) + "|" + str((probe.get("response") or {}).get("sha256", NA))
    run_id = "provider-run-" + hashlib.sha256(fingerprint_seed.encode("utf-8")).hexdigest()[:16]
    return {
        "schema_version": SCHEMA_VERSION,
        "source_schema_version": probe.get("schema_version", NA),
        "task_id": "W004-T010",
        "source_task_id": probe.get("task_id", "W004-T004"),
        "run_id": run_id,
        "captured_at": probe.get("captured_at", NA),
        "status": probe.get("status", "UNKNOWN"),
        "evidence_class": "OBSERVED_PROVIDER_MECHANICS" if observed else "BLOCKER_ONLY",
        "observed_run": observed,
        "provenance": {
            "provider": probe.get("provider", NA),
            "provider_protocol": probe.get("provider_protocol", NA),
            "model": probe.get("model", NA),
            "model_version": probe.get("model_version", NA),
            "endpoint": probe.get("endpoint", NA),
        },
        "telemetry": {
            "latency_ms": probe.get("latency_ms", NA),
            "usage": deepcopy(probe.get("usage") or {}),
            "cost": deepcopy(probe.get("cost") or {}),
        },
        "pricing_provenance": deepcopy(probe.get("pricing_provenance") or {}),
        "response_fingerprint": deepcopy(probe.get("response") or {}),
        "content_quality_evidence": {
            "included": False,
            "artifact_ref": None,
            "note": "Quality evidence is intentionally separate and must come from downstream human/source evaluation.",
        },
        "comparison_eligibility": {
            "mechanics_eligible_for_t007": not reasons,
            "full_provider_comparison_eligible": False,
            "reasons": reasons
            or ["content_quality_evidence_is_separate_and_not_satisfied_by_this_artifact"],
        },
    }


def validate_evidence(evidence: dict[str, Any]) -> list[str]:
    """Return validation findings. Empty means eligible provider mechanics for T007 import."""
    findings: list[str] = []
    if evidence.get("schema_version") != SCHEMA_VERSION:
        findings.append("unsupported_schema_version")
    if evidence.get("source_schema_version") != SOURCE_SCHEMA_VERSION:
        findings.append("unsupported_source_schema_version")
    if evidence.get("observed_run") is not True or evidence.get("status") != "OBSERVED_RUN":
        findings.append("not_an_observed_provider_run")
    provenance = evidence.get("provenance") or {}
    for field in ("provider", "provider_protocol", "model", "model_version", "endpoint"):
        if not _required_text(provenance.get(field)):
            findings.append(f"missing_provenance_{field}")
    telemetry = evidence.get("telemetry") or {}
    latency = telemetry.get("latency_ms")
    if not isinstance(latency, (int, float)) or latency < 0:
        findings.append("latency_not_observed")
    usage = telemetry.get("usage") or {}
    if not _observed_usage(usage):
        findings.append("provider_usage_not_observed")
    pricing = evidence.get("pricing_provenance") or {}
    if not _eligible_pricing(pricing):
        findings.append("official_pricing_provenance_ineligible")
    cost = telemetry.get("cost") or {}
    if not _eligible_cost(cost, pricing):
        findings.append("cost_not_eligible")
    response = evidence.get("response_fingerprint") or {}
    if not _required_text(response.get("sha256")):
        findings.append("response_fingerprint_missing")
    quality = evidence.get("content_quality_evidence") or {}
    if quality.get("included") is not False:
        findings.append("embedded_content_quality_not_allowed")
    secret_paths = _walk_keys(evidence)
    if secret_paths:
        findings.append("secret_like_fields_present:" + ",".join(secret_paths))
    return findings


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, value: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
