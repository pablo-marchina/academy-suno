#!/usr/bin/env python3
"""Manual, credential-safe wrapper around the integrated W004-T004 provider probe."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from types import ModuleType

from provider_evidence import export_probe, write_json

ROOT = Path(__file__).resolve().parents[2]
HARNESS_PATH = ROOT / "experiments" / "provider_w004" / "run_provider_probe.py"


def load_existing_harness() -> ModuleType:
    spec = importlib.util.spec_from_file_location("w004_provider_probe", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load existing provider harness: {HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def execute_manual(args: argparse.Namespace) -> dict:
    harness = load_existing_harness()
    probe = harness.execute(args)
    write_json(args.probe_output, probe)
    evidence = export_probe(probe)
    write_json(args.evidence_output, evidence)
    return evidence


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--provider", required=True)
    p.add_argument("--protocol", required=True, choices=["openai_responses", "anthropic_messages"])
    p.add_argument("--model", required=True)
    p.add_argument("--model-version", required=True)
    p.add_argument("--endpoint", required=True)
    p.add_argument("--api-key-env", default="PROVIDER_API_KEY")
    prompt_group = p.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file")
    p.add_argument("--pricing-snapshot")
    p.add_argument("--timeout", type=float, default=60.0)
    p.add_argument("--probe-output", required=True)
    p.add_argument("--evidence-output", required=True)
    return p


def main() -> int:
    args = build_parser().parse_args()
    evidence = execute_manual(args)
    summary = {
        "schema_version": evidence["schema_version"],
        "run_id": evidence["run_id"],
        "status": evidence["status"],
        "observed_run": evidence["observed_run"],
        "mechanics_eligible_for_t007": evidence["comparison_eligibility"]["mechanics_eligible_for_t007"],
        "probe_output": args.probe_output,
        "evidence_output": args.evidence_output,
    }
    print(json.dumps(summary, ensure_ascii=False))
    # BLOCKED_NO_CREDENTIAL is a valid manual-path outcome. It is not an observed run,
    # and the exported artifact keeps comparison eligibility false.
    return 0 if evidence["status"] in {"OBSERVED_RUN", "BLOCKED_NO_CREDENTIAL"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
