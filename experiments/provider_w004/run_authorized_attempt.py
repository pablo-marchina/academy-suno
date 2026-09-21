#!/usr/bin/env python3
"""Run one authorized W004 provider attempt without exposing credential material."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HARNESS_PATH = ROOT / "experiments" / "provider_w004" / "run_provider_probe.py"
NORMALIZED_ENV = "W004_NORMALIZED_PROVIDER_API_KEY"

PROVIDERS = {
    "openai": {
        "provider": "OpenAI",
        "protocol": "openai_responses",
        "model": "gpt-5.6-luna",
        "model_version": "gpt-5.6-luna",
        "endpoint": "https://api.openai.com/v1/responses",
        "pricing_snapshot": "docs/provider_w004/pricing_snapshot.openai-gpt-5.6-luna.json",
    },
    "anthropic": {
        "provider": "Anthropic",
        "protocol": "anthropic_messages",
        "model": "claude-haiku-4-5-20251001",
        "model_version": "claude-haiku-4-5-20251001",
        "endpoint": "https://api.anthropic.com/v1/messages",
        "pricing_snapshot": "docs/provider_w004/pricing_snapshot.anthropic-haiku-4-5.json",
    },
}


def load_harness() -> ModuleType:
    spec = importlib.util.spec_from_file_location("w004_provider_probe", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load provider harness: {HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1].strip()
    return value


def _assignment_candidates(raw: str) -> list[tuple[str, str, bool]]:
    """Return recognized ENV assignments without ever logging their values."""
    candidates: list[tuple[str, str, bool]] = []
    for line in raw.splitlines():
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        exported = False
        if text.startswith("export "):
            exported = True
            text = text[len("export ") :].strip()
        match = re.fullmatch(r"(OPENAI_API_KEY|ANTHROPIC_API_KEY|PROVIDER_API_KEY)\s*=\s*(.+)", text)
        if match:
            candidates.append((match.group(1), _strip_quotes(match.group(2)), exported))
    return candidates


def _json_candidate(raw: str) -> str | None:
    try:
        payload = json.loads(raw)
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    direct = payload.get("value")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    api_key = payload.get("api_key")
    if isinstance(api_key, dict):
        nested = api_key.get("value")
        if isinstance(nested, str) and nested.strip():
            return nested.strip()
    return None


def normalize_and_classify(raw: str | None) -> tuple[str | None, str | None, str]:
    """Return (provider_kind, normalized_secret, safe_reason)."""
    if raw is None or not raw.strip():
        return None, None, "missing_PROVIDER_API_KEY"

    stripped = raw.strip()
    candidates = _assignment_candidates(stripped)
    if len(candidates) == 1:
        var_name, value, exported = candidates[0]
        if not value:
            return None, None, "empty_recognized_assignment"
        source = ("exported_" if exported else "assignment_") + var_name
        if var_name == "OPENAI_API_KEY":
            return "openai", value, source
        if var_name == "ANTHROPIC_API_KEY":
            return "anthropic", value, source
        stripped = value
    elif len(candidates) > 1:
        return None, None, "ambiguous_multiple_api_key_assignments"

    json_value = _json_candidate(stripped)
    if json_value is not None:
        stripped = json_value
        source_prefix = "json_value_"
    else:
        source_prefix = "raw_"
        stripped = _strip_quotes(stripped)

    if stripped.startswith("Bearer "):
        possible = stripped[len("Bearer ") :].strip()
        if possible.startswith("sk-"):
            stripped = possible
            source_prefix += "bearer_"

    if stripped.startswith("sk-ant-"):
        return "anthropic", stripped, source_prefix + "anthropic_prefix"
    if stripped.startswith("sk-"):
        return "openai", stripped, source_prefix + "openai_prefix"
    return None, None, "unsupported_or_ambiguous_credential_format"


def blocked_result(attempt_id: str, reason: str) -> dict[str, Any]:
    return {
        "schema_version": "provider-probe-v1",
        "task_id": "W004-T004",
        "attempt_id": attempt_id,
        "status": "BLOCKED_PROVIDER_CLASSIFICATION",
        "evidence_class": "MECHANICS_ONLY",
        "credential_classification": {"recognized": False, "reason": reason},
        "content_quality_evidence": False,
        "latency_ms": "N/A",
        "usage": {"input_tokens": "N/A", "output_tokens": "N/A", "total_tokens": "N/A", "observed": False},
        "cost": {"value": "N/A", "currency": "N/A", "observed": False, "derived": False},
        "response": {"sha256": "N/A", "bytes": "N/A", "provider_model": "N/A"},
    }


def write_json(path: str | Path, value: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> dict[str, Any]:
    provider_kind, normalized_secret, reason = normalize_and_classify(os.getenv(args.secret_env))
    if provider_kind is None or normalized_secret is None:
        result = blocked_result(args.attempt_id, reason)
        write_json(args.output, result)
        return result

    config = PROVIDERS[provider_kind]
    harness = load_harness()
    os.environ[NORMALIZED_ENV] = normalized_secret
    try:
        harness_args = argparse.Namespace(
            attempt_id=args.attempt_id,
            provider=config["provider"],
            protocol=config["protocol"],
            model=config["model"],
            model_version=config["model_version"],
            endpoint=config["endpoint"],
            api_key_env=NORMALIZED_ENV,
            prompt=None,
            prompt_file=args.prompt_file,
            pricing_snapshot=str(ROOT / config["pricing_snapshot"]),
            timeout=args.timeout,
        )
        result = harness.execute(harness_args)
    finally:
        os.environ.pop(NORMALIZED_ENV, None)

    result["credential_classification"] = {
        "recognized": True,
        "provider_kind": provider_kind,
        "reason": reason,
    }
    write_json(args.output, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--secret-env", default="PROVIDER_API_KEY")
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run(args)
    safe_summary = {
        "attempt_id": result.get("attempt_id"),
        "status": result.get("status"),
        "provider": result.get("provider", "N/A"),
        "model": result.get("model", "N/A"),
        "credential_classification": result.get("credential_classification", {}),
    }
    print(json.dumps(safe_summary, ensure_ascii=False))
    if result.get("status") == "OBSERVED_RUN":
        return 0
    if result.get("status") in {"BLOCKED_PROVIDER_CLASSIFICATION", "BLOCKED_NO_CREDENTIAL"}:
        return 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
