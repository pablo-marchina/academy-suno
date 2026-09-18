#!/usr/bin/env python3
"""Validate/import manual provider evidence for downstream W004-T007 mechanics comparison."""
from __future__ import annotations

import argparse
import json

from provider_evidence import load_json, validate_evidence, write_json


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--output")
    p.add_argument(
        "--audit-only",
        action="store_true",
        help="Accept blocker/incomplete artifacts for audit storage while keeping comparable=false.",
    )
    args = p.parse_args()

    evidence = load_json(args.input)
    findings = validate_evidence(evidence)
    imported = {
        "import_schema_version": "provider-t007-import-v1",
        "source_schema_version": evidence.get("schema_version"),
        "run_id": evidence.get("run_id"),
        "status": evidence.get("status"),
        "mechanics_comparable": not findings,
        "full_provider_comparison_eligible": False,
        "findings": findings,
        "evidence": evidence,
    }
    if args.output:
        write_json(args.output, imported)
    print(json.dumps({k: imported[k] for k in imported if k != "evidence"}, ensure_ascii=False))
    if findings and not args.audit_only:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
