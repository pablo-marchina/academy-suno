#!/usr/bin/env python3
"""Groq-specific W004-T004 A05 authenticated preflight and bounded provider probe.

A05 first calls the read-only Groq Models endpoint. Only when authentication succeeds
and `openai/gpt-oss-120b` is present in the active-model response does it issue one
bounded Responses API call. Secret material and response content are never persisted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NA = "N/A"
PROVIDER = "Groq"
PROTOCOL = "openai_responses"
MODEL = "openai/gpt-oss-120b"
MODEL_VERSION = "openai/gpt-oss-120b"
MODELS_ENDPOINT = "https://api.groq.com/openai/v1/models"
RESPONSES_ENDPOINT = "https://api.groq.com/openai/v1/responses"
PRICING = {
    "kind": "official_provider_pricing",
    "source_url": "https://console.groq.com/docs/model/openai/gpt-oss-120b",
    "retrieved_at": "2026-09-21T22:18:00Z",
    "effective_at": "2026-09-21",
    "currency": "USD",
    "prices_per_million_tokens": {"input": 0.15, "output": 0.60},
    "commercial_evidence_eligible": True,
    "status": "OBSERVED_SNAPSHOT",
    "reason": "Official Groq GPT-OSS 120B pricing snapshot declared.",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact(text: str, secret: str) -> str:
    """Remove exact and key-shaped Groq credentials from diagnostic text."""
    safe = text.replace(secret, "[REDACTED_GROQ_KEY]") if secret else text
    return re.sub(r"gsk_[A-Za-z0-9._-]+", "[REDACTED_GROQ_KEY]", safe)


def parse_error(exc: urllib.error.HTTPError, secret: str) -> dict[str, Any]:
    raw = b""
    try:
        raw = exc.read(64 * 1024)
    except Exception:
        raw = b""
    message = str(exc)
    error_type = NA
    code = NA
    if raw:
        try:
            payload = json.loads(raw.decode("utf-8", errors="replace"))
            error = payload.get("error") if isinstance(payload, dict) else None
            if isinstance(error, dict):
                message = str(error.get("message", message))
                error_type = str(error.get("type", NA))
                code = str(error.get("code", NA))
        except Exception:
            pass
    return {
        "http_status": int(exc.code),
        "type": redact(error_type, secret),
        "code": redact(code, secret),
        "message": redact(message, secret)[:1000],
    }


def request_json(request: urllib.request.Request, secret: str, timeout: float) -> tuple[int | None, bytes, dict[str, Any] | None, dict[str, Any] | None, float]:
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            elapsed = round((time.perf_counter() - started) * 1000, 3)
            payload = json.loads(raw.decode("utf-8"))
            return int(response.status), raw, payload, None, elapsed
    except urllib.error.HTTPError as exc:
        elapsed = round((time.perf_counter() - started) * 1000, 3)
        return int(exc.code), b"", None, parse_error(exc, secret), elapsed
    except (urllib.error.URLError, TimeoutError) as exc:
        elapsed = round((time.perf_counter() - started) * 1000, 3)
        return None, b"", None, {
            "http_status": NA,
            "type": type(exc).__name__,
            "code": NA,
            "message": redact(str(exc), secret)[:1000],
        }, elapsed


def pricing_provenance() -> dict[str, Any]:
    return {k: v for k, v in PRICING.items() if k != "prices_per_million_tokens"}


def base_probe(attempt_id: str) -> dict[str, Any]:
    return {
        "schema_version": "provider-probe-v1",
        "task_id": "W004-T004",
        "attempt_id": attempt_id,
        "captured_at": utc_now(),
        "evidence_class": "MECHANICS_ONLY",
        "provider": PROVIDER,
        "provider_protocol": PROTOCOL,
        "model": MODEL,
        "model_version": MODEL_VERSION,
        "endpoint": RESPONSES_ENDPOINT,
        "pricing_provenance": pricing_provenance(),
        "content_quality_evidence": False,
    }


def blocked_probe(attempt_id: str, status: str, preflight: dict[str, Any], error: dict[str, Any] | None = None) -> dict[str, Any]:
    result = {
        **base_probe(attempt_id),
        "status": status,
        "latency_ms": NA,
        "usage": {"input_tokens": NA, "output_tokens": NA, "total_tokens": NA, "observed": False},
        "cost": {"value": NA, "currency": "USD", "observed": False, "derived": False},
        "response": {"sha256": NA, "bytes": NA, "provider_model": NA},
        "preflight": preflight,
    }
    if error:
        result["error"] = error
    return result


def derive_cost(usage: dict[str, Any]) -> dict[str, Any]:
    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    if not isinstance(input_tokens, int) or not isinstance(output_tokens, int):
        return {"value": NA, "currency": "USD", "observed": False, "derived": False}
    prices = PRICING["prices_per_million_tokens"]
    value = (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000
    return {"value": round(value, 10), "currency": "USD", "observed": False, "derived": True}


def execute(attempt_id: str, secret_env: str, prompt_file: str, timeout: float) -> dict[str, Any]:
    secret = os.getenv(secret_env, "").strip()
    if not secret:
        return blocked_probe(attempt_id, "BLOCKED_NO_CREDENTIAL", {"status": "NOT_RUN", "endpoint": MODELS_ENDPOINT})
    if not secret.startswith("gsk_"):
        return blocked_probe(
            attempt_id,
            "BLOCKED_PROVIDER_CLASSIFICATION",
            {"status": "NOT_RUN", "endpoint": MODELS_ENDPOINT},
            {"http_status": NA, "type": "credential_classification", "code": "not_groq_gsk", "message": "Supplied secret is not a Groq gsk_ credential."},
        )

    headers = {"Authorization": f"Bearer {secret}", "Content-Type": "application/json"}
    models_request = urllib.request.Request(MODELS_ENDPOINT, headers=headers, method="GET")
    status, raw, payload, error, preflight_ms = request_json(models_request, secret, timeout)
    preflight: dict[str, Any] = {
        "endpoint": MODELS_ENDPOINT,
        "http_status": status if status is not None else NA,
        "latency_ms": preflight_ms,
        "response_sha256": hashlib.sha256(raw).hexdigest() if raw else NA,
        "response_bytes": len(raw) if raw else NA,
        "active_model_count": 0,
        "target_model_active": False,
        "active_model_ids": [],
    }
    if error:
        preflight["error"] = error
    if status != 200 or not isinstance(payload, dict):
        return blocked_probe(attempt_id, "PREFLIGHT_ERROR", preflight, error)

    data = payload.get("data") or []
    model_ids = sorted({str(item.get("id")) for item in data if isinstance(item, dict) and item.get("id")})
    preflight["active_model_count"] = len(model_ids)
    preflight["active_model_ids"] = model_ids
    preflight["target_model_active"] = MODEL in model_ids
    if MODEL not in model_ids:
        return blocked_probe(
            attempt_id,
            "BLOCKED_MODEL_NOT_ACTIVE",
            preflight,
            {"http_status": 200, "type": "model_availability", "code": "target_model_not_active", "message": f"{MODEL} was not returned by the authenticated Models API."},
        )

    prompt = Path(prompt_file).read_text(encoding="utf-8")
    body = json.dumps({"model": MODEL, "input": prompt, "max_output_tokens": 128}).encode("utf-8")
    response_request = urllib.request.Request(RESPONSES_ENDPOINT, data=body, headers=headers, method="POST")
    response_status, response_raw, response_payload, response_error, response_ms = request_json(response_request, secret, timeout)
    if response_status != 200 or not isinstance(response_payload, dict):
        return blocked_probe(
            attempt_id,
            "TRANSPORT_ERROR",
            preflight,
            response_error or {"http_status": response_status or NA, "type": "unknown", "code": NA, "message": "Provider request failed."},
        ) | {"latency_ms": response_ms}

    raw_usage = response_payload.get("usage") or {}
    input_tokens = raw_usage.get("input_tokens", NA)
    output_tokens = raw_usage.get("output_tokens", NA)
    total_tokens = raw_usage.get("total_tokens", NA)
    usage = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "observed": all(isinstance(value, int) for value in (input_tokens, output_tokens, total_tokens)),
    }
    return {
        **base_probe(attempt_id),
        "status": "OBSERVED_RUN",
        "http_status": response_status,
        "latency_ms": response_ms,
        "usage": usage,
        "cost": derive_cost(usage),
        "response": {
            "sha256": hashlib.sha256(response_raw).hexdigest(),
            "bytes": len(response_raw),
            "provider_model": response_payload.get("model", NA),
        },
        "preflight": preflight,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--secret-env", default="PROVIDER_API_KEY")
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = execute(args.attempt_id, args.secret_env, args.prompt_file, args.timeout)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "attempt_id": result.get("attempt_id"),
        "status": result.get("status"),
        "provider": result.get("provider"),
        "model": result.get("model"),
        "preflight_http_status": (result.get("preflight") or {}).get("http_status", NA),
        "provider_http_status": result.get("http_status", (result.get("error") or {}).get("http_status", NA)),
        "error_type": (result.get("error") or {}).get("type", NA),
        "error_code": (result.get("error") or {}).get("code", NA),
    }, ensure_ascii=False))
    return 0 if result.get("status") == "OBSERVED_RUN" else 3


if __name__ == "__main__":
    raise SystemExit(main())
