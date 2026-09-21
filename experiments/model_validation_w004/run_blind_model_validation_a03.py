#!/usr/bin/env python3
"""A03: blind automated validation with explicit throttling.

A01 failed cleanly on provider HTTP 429. A02 failed before network use because
its wrapper import path was invalid. A03 fixes that import locally and performs
no HTTP retries; it spaces successful independent batches so the observed Groq
TPM window can drain between requests.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from openai import OpenAI as RealOpenAI

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_blind_model_validation as base  # noqa: E402

THROTTLE_SECONDS = 70.0


class _ResponsesProxy:
    def __init__(self, inner):
        self._inner = inner
        self._calls = 0

    def create(self, *args, **kwargs):
        if self._calls:
            time.sleep(THROTTLE_SECONDS)
        self._calls += 1
        return self._inner.create(*args, **kwargs)


class _ClientProxy:
    def __init__(self, *args, **kwargs):
        self._client = RealOpenAI(*args, **kwargs)
        self.models = self._client.models
        self.responses = _ResponsesProxy(self._client.responses)


def main() -> int:
    args = base.build_parser().parse_args()
    if args.batch_size < 1 or args.batch_size > 6:
        raise SystemExit("batch-size must be 1..6")

    base.OpenAI = _ClientProxy
    provenance = base.run(args)

    prov_path = Path(args.output).with_suffix(Path(args.output).suffix + ".provenance.json")
    persisted = json.loads(prov_path.read_text(encoding="utf-8"))
    persisted["rate_limit_posture"] = {
        "attempt_a01": "FAILED_CLEANLY_HTTP_429_NO_ACCEPTED_ARTIFACT",
        "attempt_a02": "FAILED_BEFORE_NETWORK_IMPORT_ERROR_NO_ACCEPTED_ARTIFACT",
        "observed_tpm_limit": 8000,
        "inter_batch_throttle_seconds": THROTTLE_SECONDS,
        "http_retry_count": 0,
    }
    prov_path.write_text(json.dumps(persisted, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary_path = Path(args.summary)
    summary = summary_path.read_text(encoding="utf-8")
    summary = summary.replace(
        "# W004 automated blind model validation — A01",
        f"# W004 automated blind model validation — {args.attempt_id}",
        1,
    )
    summary += (
        "\n## Attempt / rate-limit posture\n\n"
        "- A01: failed cleanly on provider HTTP 429; no accepted artifact.\n"
        "- A02: failed before network use on wrapper import; no accepted artifact.\n"
        f"- {args.attempt_id}: {THROTTLE_SECONDS:g}s inter-batch throttle; HTTP retries: 0.\n"
    )
    summary_path.write_text(summary, encoding="utf-8")

    print(json.dumps({
        "status": "COMPLETE",
        "attempt_id": provenance["attempt_id"],
        "item_count": provenance["item_count"],
        "model": provenance["model"],
        "output_jsonl_sha256": provenance["output_jsonl_sha256"],
        "human_gold_eligible": False,
        "inter_batch_throttle_seconds": THROTTLE_SECONDS,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
