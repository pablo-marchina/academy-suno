#!/usr/bin/env python3
"""Reproducible validator for W006-T001-A02 Phase 9 contracts."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError as exc:
    raise SystemExit("jsonschema with Draft 2020-12 support is required") from exc

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "core-contracts.schema.json"
REG_SCHEMA_PATH = HERE / "decision-research-registry.schema.json"
REGISTRY_PATH = ROOT / "docs/decisions/DECISION_RESEARCH_REGISTRY.v1.json"

DENY = {
    "SYSTEM/CONSTITUTION.md", "SYSTEM/DECISION_RESEARCH_GATE.md",
    "SYSTEM/TASK_SIGNALS.md", "SYSTEM/AUTOPILOT.md", "SYSTEM/STATE.md",
    "SYSTEM/TASK_LEDGER.md", "scripts/validate_system.py",
    ".github/workflows/system-integrity.yml",
}
DENY_PREFIXES = ("SYSTEM/WAVES/", "SYSTEM/CHECKPOINT", "SYSTEM/checkpoint")

class UnknownDecisionRef(ValueError): pass
class AmbiguousDecisionRef(ValueError): pass

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def schema_for_def(core: dict, name: str) -> dict:
    return {"$schema": core["$schema"], "$defs": core["$defs"], "$ref": f"#/$defs/{name}"}

def validate_def(core: dict, name: str, instance: dict) -> None:
    Draft202012Validator(schema_for_def(core, name)).validate(instance)

def reject(core: dict, name: str, instance: dict, label: str) -> None:
    try:
        validate_def(core, name, instance)
    except ValidationError:
        return
    raise AssertionError(f"negative case unexpectedly passed: {label}")

def resolve_decision_ref(registry: dict, ref: str, source_path: str | None = None) -> str:
    canonical = {r["canonical_ref"]: r for r in registry["records"]}
    if ref in canonical:
        return ref
    aliases = {a["alias"]: a for a in registry["aliases"]}
    entry = aliases.get(ref)
    if entry is None:
        raise UnknownDecisionRef(ref)
    targets = entry["targets"]
    if entry["resolution"] == "UNIQUE":
        if len(targets) != 1:
            raise AssertionError(f"UNIQUE alias has {len(targets)} targets: {ref}")
        return targets[0]["canonical_ref"]
    if source_path is None:
        raise AmbiguousDecisionRef(ref)
    selected = [t for t in targets if t["source_path"] == source_path]
    if len(selected) != 1:
        raise AmbiguousDecisionRef(f"{ref} @ {source_path}")
    return selected[0]["canonical_ref"]

def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()

def changed_file_review(base_ref: str) -> list[str]:
    proc = subprocess.run(["git", "diff", "--name-only", f"{base_ref}...HEAD"], cwd=ROOT, check=True, capture_output=True, text=True)
    changed = [p.strip() for p in proc.stdout.splitlines() if p.strip()]
    violations = [p for p in changed if p in DENY or any(p.startswith(prefix) for prefix in DENY_PREFIXES)]
    if violations:
        raise AssertionError(f"protocol/canonical files changed: {violations}")
    return changed

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", help="git base ref for changed-file review")
    parser.add_argument("--skip-source-files", action="store_true")
    args = parser.parse_args()

    core, reg_schema, registry = load(CORE_PATH), load(REG_SCHEMA_PATH), load(REGISTRY_PATH)
    assert core["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert reg_schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    Draft202012Validator.check_schema(core)
    Draft202012Validator.check_schema(reg_schema)
    Draft202012Validator(reg_schema).validate(registry)

    ids = [r["canonical_id"] for r in registry["records"]]
    refs = [r["canonical_ref"] for r in registry["records"]]
    assert len(ids) == len(set(ids)), "duplicate canonical Decision Research ID"
    assert len(refs) == len(set(refs)), "duplicate canonical Decision Research reference"
    for record in registry["records"]:
        assert record["canonical_ref"] == f'dr://{record["canonical_id"]}'
        if not args.skip_source_files:
            source = ROOT / record["source_path"]
            assert source.is_file(), f"missing Decision Research source: {record['source_path']}"
            assert git_blob_sha(source) == record["source_blob_sha"], f"source blob drift: {record['source_path']}"

    alias_names = [a["alias"] for a in registry["aliases"]]
    assert len(alias_names) == len(set(alias_names)), "duplicate alias entry"
    known_refs = set(refs)
    for alias in registry["aliases"]:
        target_refs = [t["canonical_ref"] for t in alias["targets"]]
        assert all(ref in known_refs for ref in target_refs)
        if alias["resolution"] == "UNIQUE":
            assert len(target_refs) == 1
        else:
            assert len(set(target_refs)) > 1

    try:
        resolve_decision_ref(registry, "DR-0001")
    except AmbiguousDecisionRef:
        pass
    else:
        raise AssertionError("bare colliding DR-0001 did not fail closed")
    assert resolve_decision_ref(registry, "DR-0001", "docs/decisions/research/DR-0001-evidence-cockpit-frontend-api-live-events.md") == "dr://DR-0001"
    assert resolve_decision_ref(registry, "DR-0001", "docs/decisions/research/DR-0001-orchestration-durability-runtime.md") == "dr://DR-5910"
    try:
        resolve_decision_ref(registry, "DR-DOES-NOT-EXIST")
    except UnknownDecisionRef:
        pass
    else:
        raise AssertionError("unknown Decision Research reference did not fail closed")

    artifact = {"contract_version":"1.0.0","artifact_id":"artifact-1","content":{"contract_version":"1.0.0","algorithm":"sha256","digest":"a"*64}}
    provenance = {"contract_version":"1.0.0","provenance_id":"prov-1","origin_kind":"user_upload","source_ref":artifact}
    protected = {"contract_version":"1.0.0","org_id":"org-1","workspace_id":"workspace-1","resource_type":"document","resource_id":"document-1","provenance":provenance}
    validate_def(core, "ProtectedResourceIdentity", protected)
    reject(core, "ProtectedResourceIdentity", {k:v for k,v in protected.items() if k != "provenance"}, "protected resource missing provenance")
    reject(core, "ProtectedResourceIdentity", {k:v for k,v in protected.items() if k != "org_id"}, "protected resource missing tenant identity")

    cursor = {"contract_version":"1.0.0","cursor_token":"opaque:event:3","last_event_revision":3}
    validate_def(core, "ReplayCursor", cursor)
    reject(core, "ReplayCursor", {**cursor,"org_id":"attacker-selected-org"}, "cursor attempts tenant selection")

    event = {"contract_version":"1.0.0","org_id":"org-1","workspace_id":"workspace-1","run_id":"run-1","event_id":"event-1","event_type":"run.transitioned","event_schema_version":1,"transition_id":"transition-1","resource_type":"run","resource_id":"run-1","result_revision":2,"event_revision":3,"occurred_at":"2026-09-22T17:30:00Z"}
    validate_def(core, "EventEnvelope", event)
    reject(core, "EventEnvelope", {k:v for k,v in event.items() if k != "transition_id"}, "event missing transition identity")
    reject(core, "EventEnvelope", {**event,"result_revision":"2"}, "malformed event revision")

    changed = changed_file_review(args.base_ref) if args.base_ref else None
    print("PASS schema_draft_2020_12")
    print("PASS schema_structural_validity")
    print("PASS registry_instance_validation")
    print(f"PASS canonical_uniqueness records={len(registry['records'])}")
    print("PASS alias_resolution collision=fail_closed unknown=fail_closed source_qualified=unique")
    print("PASS negative_contract_cases")
    if changed is not None:
        print(f"PASS changed_file_review files={len(changed)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
