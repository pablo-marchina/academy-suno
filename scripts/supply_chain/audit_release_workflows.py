#!/usr/bin/env python3
"""Audit release-path workflows for immutable Actions and least-privilege tokens."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
RELEASE_WORKFLOWS = (
    Path(".github/workflows/release-smoke-w004-t012.yml"),
    Path(".github/workflows/w006-t008-supply-chain.yml"),
)
ACTION_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)
FULL_SHA_RE = re.compile(r"^[^@]+@[0-9a-f]{40}$")


def audit() -> dict[str, object]:
    action_refs: list[dict[str, object]] = []
    movable: list[dict[str, object]] = []
    broad_permissions: list[dict[str, object]] = []

    for relative in RELEASE_WORKFLOWS:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(f"release workflow missing: {relative}")
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            match = ACTION_RE.match(line)
            if match:
                ref = match.group(1)
                record = {"workflow": str(relative), "line": line_number, "ref": ref}
                action_refs.append(record)
                if not ref.startswith("./") and not FULL_SHA_RE.match(ref):
                    movable.append(record)
            stripped = line.strip()
            if stripped in {"permissions: write-all", "permissions: read-all"}:
                broad_permissions.append({
                    "workflow": str(relative),
                    "line": line_number,
                    "value": stripped,
                })

        # Top-level permissions must be exactly contents: read. Additional write
        # scopes are allowed only within the isolated attestation job.
        top_permissions = False
        for line_number, line in enumerate(lines, start=1):
            if line == "permissions:":
                top_permissions = True
                continue
            if top_permissions:
                if line and not line.startswith("  "):
                    top_permissions = False
                    continue
                if line.strip() and line.strip() != "contents: read":
                    broad_permissions.append({
                        "workflow": str(relative),
                        "line": line_number,
                        "value": line.strip(),
                    })

    return {
        "schema_version": "w006-t008-release-workflow-audit.v1",
        "release_workflows": [str(path) for path in RELEASE_WORKFLOWS],
        "action_reference_count": len(action_refs),
        "action_references": action_refs,
        "movable_third_party_release_action_count": len(movable),
        "movable_third_party_release_actions": movable,
        "overly_broad_release_token_permission_count": len(broad_permissions),
        "overly_broad_release_token_permissions": broad_permissions,
        "status": "PASS" if not movable and not broad_permissions else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
