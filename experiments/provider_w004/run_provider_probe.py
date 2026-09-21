#!/usr/bin/env python3
"""Provider/model mechanics probe for W004-T004.

This harness records observed transport latency and provider-reported usage while
keeping unobserved fields explicitly N/A. It does not score content quality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NA = "N/A"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def pricing_provenance(snapshot: dict[str, Any] | None) -> dict[str, Any]:
    if snapshot is None:
        return {
            "status": "UNOBSERVED",
            "source_url": NA,
            "retrieved_at": NA,
            "effective_at": NA,
            "currency": NA,
            "commercial_evidence_eligible": False,
            "reason": "No pricing snapshot supplied; cost must remain N/A.",
        }
    kind = snapshot.get("kind", "unknown")
    eligible = kind == "official_provider_pricing"
    return {
        "status": "OBSERVED_SNAPSHOT" if eligible else "NON_COMMERCIAL_OR_UNKNOWN",
        "kind": kind,
        "source_url": snapshot.get("source_url", NA),
        "retrieved_at": snapshot.get("retrieved_at", NA),
        "effective_at": snapshot.get("effective_at", NA),
        "currency": snapshot.get("currency", NA),
        "commercial_evidence_eligible": eligible,
        "reason": (
            "Official provider pricing snapshot declared."
            if eligible
            else "Synthetic/unknown pricing is ineligible as commercial evidence."
        ),
    }


def extract_usage(protocol: str, payload: dict[str, Any]) -> dict[str, Any]:
    usage = payload.get("usage") or {}
    if protocol == "openai_responses":
        input_tokens = usage.get("input_tokens", NA)
        output_tokens = usage.get("output_tokens", NA)
        total_tokens = usage.get("total_tokens", NA)
    elif protocol == "anthropic_messages":
        input_tokens = usage.get("input_tokens", NA)
        output_tokens = usage.get("output_tokens", NA)
        total_tokens = (
            input_tokens + output_tokens
            if isinstance(input_tokens, int) and isinstance(output_tokens, int)
            else NA
        )
    else:
        input_tokens = output_tokens = total_tokens = NA
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "observed": any(isinstance(v, int) for v in (input_tokens, output_tokens, total_tokens)),
    }


def compute_cost(usage: dict[str, Any], snapshot: dict[str, Any] | None) -> dict[str, Any]:
    prov = pricing_provenance(snapshot)
    if not usage.get("observed") or not prov["commercial_evidence_eligible"]:
        return {"value": NA, "currency": prov.get("currency", NA), "observed": False, "derived": False}
    prices = snapshot.get("prices_per_million_tokens") or {}
    in_price = prices.get("input")
    out_price = prices.get("output")
    if not all(isinstance(x, (int, float)) for x in (in_price, out_price)):
        return {"value": NA, "currency": prov.get("currency", NA), "observed": False, "derived": False}
    in_tokens = usage.get("input_tokens")
    out_tokens = usage.get("output_tokens")
    if not isinstance(in_tokens, int) or not isinstance(out_tokens, int):
        return {"value": NA, "currency": prov.get("currency", NA), "observed": False, "derived": False}
    value = (in_tokens * in_price + out_tokens * out_price) / 1_000_000
    return {"value": round(value, 10), "currency": prov["currency"], "observed": False, "derived": True}


def build_request(protocol: str, endpoint: str, api_key: str, model: str, prompt: str) -> urllib.request.Request:
    if protocol == "openai_responses":
        body = {"model": model, "input": prompt, "max_output_tokens": 128}
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    elif protocol == "anthropic_messages":
        body = {"model": model, "max_tokens": 128, "messages": [{"role": "user", "content": prompt}]}
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
    else:
        raise ValueError(f"Unsupported protocol: {protocol}")
    return urllib.request.Request(endpoint, data=json.dumps(body).encode(), headers=headers, method="POST")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    prompt = Path(args.prompt_file).read_text(encoding="utf-8") if args.prompt_file else args.prompt
    api_key = os.getenv(args.api_key_env)
    snapshot = load_json(args.pricing_snapshot)
    base = {
        "schema_version": "provider-probe-v1",
        "task_id": "W004-T004",
        "attempt_id": getattr(args, "attempt_id", "A01"),
        "captured_at": utc_now(),
        "evidence_class": "MECHANICS_ONLY",
        "provider": args.provider,
        "provider_protocol": args.protocol,
        "model": args.model,
        "model_version": args.model_version or NA,
        "endpoint": args.endpoint,
        "pricing_provenance": pricing_provenance(snapshot),
        "content_quality_evidence": False,
    }
    if not api_key:
        return {
            **base,
            "status": "BLOCKED_NO_CREDENTIAL",
            "latency_ms": NA,
            "usage": {"input_tokens": NA, "output_tokens": NA, "total_tokens": NA, "observed": False},
            "cost": {"value": NA, "currency": NA, "observed": False, "derived": False},
            "response": {"sha256": NA, "bytes": NA, "provider_model": NA},
            "blocker": f"Environment variable {args.api_key_env} is not set.",
        }

    request = build_request(args.protocol, args.endpoint, api_key, args.model, prompt)
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            raw = response.read()
            http_status = response.status
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        elapsed = round((time.perf_counter() - started) * 1000, 3)
        return {
            **base,
            "status": "TRANSPORT_ERROR",
            "latency_ms": elapsed,
            "usage": {"input_tokens": NA, "output_tokens": NA, "total_tokens": NA, "observed": False},
            "cost": {"value": NA, "currency": NA, "observed": False, "derived": False},
            "response": {"sha256": NA, "bytes": NA, "provider_model": NA},
            "error": f"{type(exc).__name__}: {exc}",
        }
    elapsed = round((time.perf_counter() - started) * 1000, 3)
    payload = json.loads(raw.decode("utf-8"))
    usage = extract_usage(args.protocol, payload)
    return {
        **base,
        "status": "OBSERVED_RUN",
        "http_status": http_status,
        "latency_ms": elapsed,
        "usage": usage,
        "cost": compute_cost(usage, snapshot),
        "response": {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "provider_model": payload.get("model", NA),
        },
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--attempt-id", default="A01")
    p.add_argument("--provider", required=True)
    p.add_argument("--protocol", required=True, choices=["openai_responses", "anthropic_messages"])
    p.add_argument("--model", required=True)
    p.add_argument("--model-version")
    p.add_argument("--endpoint", required=True)
    p.add_argument("--api-key-env", required=True)
    prompt_group = p.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file")
    p.add_argument("--pricing-snapshot")
    p.add_argument("--timeout", type=float, default=60.0)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    result = execute(args)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] in {"OBSERVED_RUN", "BLOCKED_NO_CREDENTIAL"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
