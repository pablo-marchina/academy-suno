#!/usr/bin/env python3
"""Final autonomous W004-T004 provider-family retry for Groq/xAI only.

The secret is classified locally from documented provider-specific key families or
explicit environment-variable wrappers. Unsupported or ambiguous credentials are
never transmitted to any provider.
"""
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
    "groq": {
        "provider": "Groq",
        "protocol": "openai_responses",
        "model": "openai/gpt-oss-20b",
        "model_version": "openai/gpt-oss-20b",
        "endpoint": "https://api.groq.com/openai/v1/responses",
        "pricing_snapshot": "docs/provider_w004/pricing_snapshot.groq-gpt-oss-20b.json",
    },
    "xai": {
        "provider": "xAI",
        "protocol": "openai_responses",
        "model": "grok-4.6",
        "model_version": "grok-4.6",
        "endpoint": "https://api.x.ai/v1/responses",
        "pricing_snapshot": "docs/provider_w004/pricing_snapshot.xai-grok-4.6.json",
    },
}

EXPLICIT_VARIABLES = {
    "GROQ_API_KEY": "groq",
    "XAI_API_KEY": "xai",
    "OPENAI_API_KEY": "known_other_openai",
    "ANTHROPIC_API_KEY": "known_other_anthropic",
    "GEMINI_API_KEY": "known_other_gemini",
    "GOOGLE_API_KEY": "known_other_google",
    "OPENROUTER_API_KEY": "known_other_openrouter",
    "PROVIDER_API_KEY": "generic",
}


def load_harness() -> ModuleType:
    spec = importlib.util.spec_from_file_location("w004_provider_probe", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load provider harness: {HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1].strip()
    return value


def assignment_candidates(raw: str) -> list[tuple[str, str, bool]]:
    names = "|".join(re.escape(name) for name in EXPLICIT_VARIABLES)
    pattern = re.compile(rf"({names})\s*=\s*(.+)")
    found: list[tuple[str, str, bool]] = []
    for line in raw.splitlines():
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        exported = False
        if text.startswith("export "):
            exported = True
            text = text[len("export ") :].strip()
        match = pattern.fullmatch(text)
        if match:
            found.append((match.group(1), strip_quotes(match.group(2)), exported))
    return found


def classify_value(value: str, source: str) -> tuple[str | None, str | None, str]:
    value = strip_quotes(value)
    if value.startswith("Bearer "):
        value = value[len("Bearer ") :].strip()
        source += "_bearer"
    if value.startswith("gsk_"):
        return "groq", value, source + "_groq_gsk"
    if value.startswith("xai-"):
        return "xai", value, source + "_xai_prefix"
    if value.startswith("sk-or-v1-"):
        return None, None, "identified_openrouter_but_a04_does_not_route_it"
    if value.startswith("sk-ant-"):
        return None, None, "identified_anthropic_previous_family"
    if value.startswith("sk-"):
        return None, None, "identified_sk_family_previous_attempt_scope"
    if value.startswith("AIza"):
        return None, None, "identified_google_standard_key_but_gemini_not_proven"
    return None, None, "unsupported_or_ambiguous_credential_format"


def normalize_and_classify(raw: str | None) -> tuple[str | None, str | None, str]:
    if raw is None or not raw.strip():
        return None, None, "missing_PROVIDER_API_KEY"
    stripped = raw.strip()
    candidates = assignment_candidates(stripped)
    if len(candidates) > 1:
        return None, None, "ambiguous_multiple_api_key_assignments"
    if len(candidates) == 1:
        var_name, value, exported = candidates[0]
        if not value:
            return None, None, "empty_recognized_assignment"
        provider_hint = EXPLICIT_VARIABLES[var_name]
        source = ("exported_" if exported else "assignment_") + var_name
        if provider_hint in PROVIDERS:
            return provider_hint, value, source
        if provider_hint != "generic":
            return None, None, f"{source}_identifies_{provider_hint}"
        return classify_value(value, source)

    try:
        payload = json.loads(stripped)
    except Exception:
        payload = None
    if isinstance(payload, dict):
        candidate = payload.get("value")
        if not isinstance(candidate, str):
            api_key = payload.get("api_key")
            candidate = api_key.get("value") if isinstance(api_key, dict) else None
        if isinstance(candidate, str) and candidate.strip():
            return classify_value(candidate.strip(), "json_value")

    return classify_value(stripped, "raw")


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
    print(json.dumps({
        "attempt_id": result.get("attempt_id"),
        "status": result.get("status"),
        "provider": result.get("provider", "N/A"),
        "model": result.get("model", "N/A"),
        "credential_classification": result.get("credential_classification", {}),
    }, ensure_ascii=False))
    if result.get("status") == "OBSERVED_RUN":
        return 0
    if result.get("status") in {"BLOCKED_PROVIDER_CLASSIFICATION", "BLOCKED_NO_CREDENTIAL"}:
        return 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
