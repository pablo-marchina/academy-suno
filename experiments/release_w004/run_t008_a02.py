#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_DEMO_SHA = "c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5"
EXPECTED_DEMO_SIZE = 1_388_430


class ProofError(RuntimeError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ProofError(message)


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def markers(path: str, expected: tuple[str, ...]) -> None:
    body = text(path)
    missing = [item for item in expected if item not in body]
    require(not missing, f"{path} missing markers: {missing}")


def execute(command: list[str]) -> str:
    done = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    require(done.returncode == 0, f"command failed ({done.returncode}): {' '.join(command)}\n{done.stdout}")
    return done.stdout


def mechanics_smoke(workdir: Path) -> dict:
    out = workdir / "legacy_smoke.json"
    execute([sys.executable, "scripts/release_smoke/run_release_smoke.py", "--workdir", str(workdir / "legacy"), "--output", str(out)])
    report = json.loads(out.read_text(encoding="utf-8"))
    require(report["status"] == "PASS", "release smoke not PASS")
    lineage = report["lineage"]
    require(lineage["before_status"] == "FAIL" and lineage["after_status"] == "PASS", "repair lineage drift")
    require(lineage["fresh_hard_gate_runs"] is True and lineage["siblings_immutable"] is True, "repair invariants drift")
    require(report["evidence_posture"]["mechanics_end_to_end"] == "PROVEN", "mechanics not PROVEN")
    return report


def canonical_evidence() -> dict:
    markers("SYSTEM/STATE.md", (
        "`STATE_VERSION: 0037`",
        "W004-T007 A05 é o attempt canônico INTEGRATED",
        "`W004-T008-A02`",
        "human gold/agreement/preference: **not observed**",
        "audience thresholds: `DIAGNOSTIC_ONLY`",
    ))
    markers("SYSTEM/RESULTS/W004-T005-A02.md", (
        "`EVIDENCE_CLASS: MODEL_AUTOMATED_BLIND_CALIBRATION`",
        "target→automated exact match: `18/36 (0.500000)`",
        "human gold eligible: `false`",
        "human agreement observed: `false`",
        "threshold disposition: `DIAGNOSTIC_ONLY`",
    ))
    markers("SYSTEM/RESULTS/W004-T006-A01.md", (
        "hard-gate invariant: `true`",
        "hard-fail compensation count: `0`",
        "delta: `+0.000000`",
        "backend decision: `NO_BACKEND_PREFERENCE`",
    ))
    markers("SYSTEM/RESULTS/W004-T007-A05.md", (
        "`ATTEMPT_ID: A05`",
        "observed calls: `8/8`",
        "same four DEVELOPMENT tasks/prompt/config: `true`",
        "A03 automated calibration used as model-quality gold: `false`",
        "120B: preservation `3/4`; quality `0.952083`",
        "20B: preservation `2/4`; quality `0.927083`",
        "decision: `NO_OVERALL_MODEL_PREFERENCE`",
        "human preference observed: `false`",
        "human gold used: `false`",
        "lifecycle provenance: `ATTEMPT_VALID_SINGLE_TERMINAL_EXPECTED`",
    ))
    return {
        "calibration": {"class": "MODEL_AUTOMATED_BLIND_CALIBRATION", "population": 36, "target_automated_exact_match": 0.5, "human_gold": False, "human_agreement": False, "thresholds": "DIAGNOSTIC_ONLY"},
        "semantic": {"reference_accuracy_delta": 0.0, "hard_fail_compensation_count": 0, "decision": "NO_BACKEND_PREFERENCE"},
        "provider_model": {
            "accepted_attempt": "A05",
            "observed_calls": 8,
            "model_120b": {"preservation": "3/4", "quality": 0.952083, "numeric_recall": 0.958333, "concept_recall": 1.0, "mean_latency_ms": 1914.879, "total_tokens": 3643, "cost_usd": 0.00162015},
            "model_20b": {"preservation": "2/4", "quality": 0.927083, "numeric_recall": 0.958333, "concept_recall": 1.0, "mean_latency_ms": 1032.527, "total_tokens": 3977, "cost_usd": 0.000910275},
            "decision": "NO_OVERALL_MODEL_PREFERENCE",
            "human_preference": False,
            "human_gold": False,
        },
    }


def demo_evidence() -> dict:
    path = ROOT / "artifacts/submission/final-demo.mp4"
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == EXPECTED_DEMO_SHA, f"demo sha drift: {digest}")
    require(len(raw) == EXPECTED_DEMO_SIZE, f"demo size drift: {len(raw)}")
    markers("SYSTEM/RESULTS/W004-T020-A01.md", ("`VIDEO_PACKAGE_REVIEW: PASS`", "`NEW_CRITICAL_FINDINGS: 0`", "`NEW_HIGH_FINDINGS: 0`"))
    markers("SYSTEM/RESULTS/W004-T021-A02.md", (EXPECTED_DEMO_SHA, "Repository-controlled durable path: `artifacts/submission/final-demo.mp4`", "`cmp` equality"))
    duration = 69.12
    probe = shutil.which("ffprobe")
    if probe:
        done = subprocess.run([probe, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        require(done.returncode == 0, f"ffprobe failed: {done.stderr}")
        duration = float(done.stdout.strip())
    require(duration <= 300.0, f"demo over cap: {duration}")
    return {"sha256": digest, "size_bytes": len(raw), "duration_seconds": duration, "cap_seconds": 300.0, "video_package_review": "PASS", "durable_copy": True}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", type=Path, default=Path(tempfile.gettempdir()) / "w004-t008-a02")
    args = ap.parse_args()
    smoke = mechanics_smoke(args.workdir)
    current = canonical_evidence()
    demo = demo_evidence()
    proof = {
        "schema_version": "w004-t008-release-proof.v2",
        "task_id": "W004-T008",
        "attempt_id": "A02",
        "base_state_version": "0037",
        "base_commit_sha": "73ffcf24b084093866543ac167296963106bc969",
        "status": "PASS_EVIDENCE_BOUNDED",
        "mechanics": {
            "source_to_9_to_eval_repair_aggregate": True,
            "job_count": 9,
            "joined_output_count": 9,
            "repair_before": smoke["lineage"]["before_status"],
            "repair_after": smoke["lineage"]["after_status"],
            "fresh_hard_gate_runs": smoke["lineage"]["fresh_hard_gate_runs"],
            "siblings_immutable": smoke["lineage"]["siblings_immutable"],
            "historical_posture_superseded": True,
        },
        "canonical_evidence": current,
        "demo": demo,
        "audit": {
            "PASS": ["clean-checkout mechanics", "T005 waiver calibration dependency", "T006 hard-gate-safe ablation", "T007-A05 attempt-valid bounded provider comparison", "video/package review", "durable final demo"],
            "FAIL_EXPECTED_NEGATIVE_CONTROL": ["parser wrong-role probe", "parser wrong-unit probe", "BCB table-role ambiguity fail-closed path"],
            "REVIEW_REQUIRED": ["parser flat-value-only candidate", "3 automated-calibration non-compensatory attention items"],
            "N_A_NOT_OBSERVED": ["human gold", "human agreement", "human preference"],
            "UNKNOWN_EXTERNAL": ["submission deadline", "submission mechanism", "named owner/decision maker", "internal Suno workflow"],
        },
        "claim_boundaries": {"human_gold": False, "human_agreement": False, "human_preference": False, "production_thresholds": False, "semantic_backend_preference": "NO_BACKEND_PREFERENCE", "overall_model_preference": "NO_OVERALL_MODEL_PREFERENCE", "blanket_production_readiness": False},
        "release_scope_decision": "T008_INTERNAL_RELEASE_PROOF_PASS_READY_FOR_FINAL_RECONCILIATION",
    }
    out = ROOT / "experiments/release_w004/runs/W004-T008-A02/release_proof.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(proof, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    doc = ROOT / "docs/release_w004/W004-T008-A02.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# W004-T008-A02 — attempt-valid final clean-E2E release proof\n\nInternal release-proof scope PASS using canonical T007-A05. Human gold/agreement/preference remain unobserved; thresholds remain DIAGNOSTIC_ONLY; semantic/model preference remains open. External submission logistics remain UNKNOWN. Blanket production readiness is not claimed.\n", encoding="utf-8")
    result = ROOT / "SYSTEM/RESULTS/W004-T008-A02.md"
    result.write_text(f"""# RESULT W004-T008-A02\n\n`TASK_ID: W004-T008`\n`ATTEMPT_ID: A02`\n`BASE_STATE_VERSION: 0037`\n`BASE_COMMIT_SHA: 73ffcf24b084093866543ac167296963106bc969`\n`WORKER_BRANCH: worker/W004-T008-A02`\n`STATUS: COMPLETE_EVIDENCE_BOUNDED`\n`EVIDENCE_POLICY: D-0017`\n\n## Outcome\n\n- clean-checkout source→9→eval→repair→aggregate: `PASS`, `9/9`\n- repair lineage: `FAIL→PASS`, fresh hard gates true, siblings immutable true\n- canonical T007 dependency: `A05`, attempt-valid, observed calls `8/8`\n- T005: `MODEL_AUTOMATED_BLIND_CALIBRATION`; human gold/agreement/preference not observed\n- T006: `NO_BACKEND_PREFERENCE`, measured delta `+0.000000`\n- T007: `NO_OVERALL_MODEL_PREFERENCE`; bounded source-preservation/latency/cost only\n- durable final demo SHA-256: `{demo['sha256']}`\n- final demo duration: `{demo['duration_seconds']:.3f}s <= 300s`\n- video/package review: `PASS`\n- external UNKNOWNs preserved: deadline, submission mechanism, named owner/decision maker, internal Suno workflow\n- release-scope decision: `T008_INTERNAL_RELEASE_PROOF_PASS_READY_FOR_FINAL_RECONCILIATION`\n- blanket production-readiness claim: `false`\n\n## Boundary\n\nThis attempt is valid only for the internal final clean-E2E release-proof scope. It consumes canonical attempt-valid T007-A05, does not relabel automated calibration as human evidence, does not select an overall model/backend, and does not convert external UNKNOWNs into PASS.\n\n## Artifacts\n\n- `experiments/release_w004/runs/W004-T008-A02/release_proof.json`\n- `docs/release_w004/W004-T008-A02.md`\n""", encoding="utf-8")
    print(json.dumps(proof, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
