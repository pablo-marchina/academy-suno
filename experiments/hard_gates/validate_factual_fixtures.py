#!/usr/bin/env python3
"""EXP-C factual fixture/oracle validator. Standard library only; no semantic judge."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "tests/fixtures/adversarial/factual_v001.jsonl"
SPEC = ROOT / "experiments/hard_gates/factual_hard_gate_spec_v001.json"
FIELDS = ("failure_code", "severity", "decision", "support_status")

def jsonl(path: Path):
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"{path}:{n}: {e}") from e
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{n}: object required")
        rows.append(row)
    return rows

def check(spec, fixtures):
    errors, ids, muts, sevs, decs, targets = [], set(), set(), set(), set(), set()
    registry = spec.get("failure_codes", {})
    if spec.get("independence", {}).get("semantic_judge_required") is not False:
        errors.append("semantic_judge_required must be false")
    for i, f in enumerate(fixtures, 1):
        fid, exp = f.get("id"), f.get("expected")
        p = f"fixture[{i}] {fid!r}"
        if not fid or fid in ids: errors.append(f"{p}: missing/duplicate id")
        ids.add(fid)
        if not isinstance(exp, dict): errors.append(f"{p}: missing expected"); continue
        muts.add(f.get("mutation_type")); sevs.add(exp.get("severity")); decs.add(exp.get("decision"))
        targets.update(exp.get("backlog_targets", []))
        for key in ("severity","decision","hard_gate","auto_pass_blocker","support_status",
                    "required_action","evidence_span_ids","backlog_targets"):
            if key not in exp: errors.append(f"{p}: expected.{key} missing")
        code = exp.get("failure_code")
        if code is not None:
            if code not in registry: errors.append(f"{p}: unregistered failure_code={code}")
            elif registry[code].get("severity") != exp.get("severity"):
                errors.append(f"{p}: severity disagrees with registry")
        if exp.get("severity") == "CRITICAL":
            if exp.get("decision") != "FAIL" or exp.get("hard_gate") is not True:
                errors.append(f"{p}: CRITICAL must be hard FAIL")
        if exp.get("decision") != "PASS" and exp.get("auto_pass_blocker") is not True:
            errors.append(f"{p}: non-PASS must block auto-PASS")
        span_ids = {s.get("span_id") for s in f.get("source", {}).get("spans", [])}
        for sid in exp.get("evidence_span_ids", []):
            if sid not in span_ids: errors.append(f"{p}: evidence span {sid!r} missing from source")
    need_m = set(spec.get("required_mutation_coverage", []))
    need_s = set(spec.get("required_expected_classes", {}).get("severity", []))
    need_d = set(spec.get("required_expected_classes", {}).get("decision", []))
    if not need_m <= muts: errors.append(f"missing mutations={sorted(need_m-muts)}")
    if not need_s <= sevs: errors.append(f"missing severities={sorted(need_s-sevs)}")
    if not need_d <= decs: errors.append(f"missing decisions={sorted(need_d-decs)}")
    if not {"B03","B08"} <= targets: errors.append("B03/B08 direct mapping incomplete")
    return errors

def compare(spec, fixtures, observed):
    errors, by_id = [], {}
    for row in observed:
        fid = row.get("fixture_id")
        if fid in by_id: errors.append(f"duplicate observed fixture_id={fid}")
        by_id[fid] = row
    expected = {f["id"]: f["expected"] for f in fixtures}
    missing = sorted(set(expected)-set(by_id))
    unknown = sorted(set(by_id)-set(expected))
    if spec.get("acceptance", {}).get("all_fixture_ids_required") and missing:
        errors.append(f"missing observed fixture ids={missing}")
    if unknown: errors.append(f"unknown observed fixture ids={unknown}")
    for fid, exp in expected.items():
        obs = by_id.get(fid)
        if not obs: continue
        for key in FIELDS:
            if obs.get(key) != exp.get(key):
                errors.append(f"{fid}: {key} expected={exp.get(key)!r} observed={obs.get(key)!r}")
        if exp.get("severity") == "CRITICAL" and obs.get("hard_gate") is not True:
            errors.append(f"{fid}: CRITICAL must set hard_gate=true")
        if exp.get("auto_pass_blocker") and obs.get("decision") == "PASS":
            errors.append(f"{fid}: auto-PASS blocker observed PASS")
    return errors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", type=Path, default=CORPUS)
    ap.add_argument("--spec", type=Path, default=SPEC)
    ap.add_argument("--observed", type=Path)
    a = ap.parse_args()
    try:
        spec = json.loads(a.spec.read_text(encoding="utf-8"))
        fixtures = jsonl(a.corpus)
        errors = check(spec, fixtures)
        if a.observed: errors += compare(spec, fixtures, jsonl(a.observed))
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr); return 2
    if errors:
        for e in errors: print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(f"PASS fixture-contract: {len(fixtures)} fixtures, {len(spec['failure_codes'])} failure codes")
    if a.observed: print("PASS observed-results oracle comparison")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
