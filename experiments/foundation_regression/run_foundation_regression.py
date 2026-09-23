#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARTIFACT_DIR = Path(tempfile.gettempdir()) / "academy-suno-foundation-regression"
ARTIFACT_DIR = Path(os.environ.get("FOUNDATION_ARTIFACT_DIR", DEFAULT_ARTIFACT_DIR))


class RegressionFailure(RuntimeError):
    pass


def _dependency_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def _command_text(command: list[str]) -> str:
    return " ".join(command)


def run_step(name: str, command: list[str], *, env: dict[str, str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    log_path = ARTIFACT_DIR / f"{name}.log"
    log_path.write_text(completed.stdout, encoding="utf-8")
    print(f"\n== {name} ==")
    print(f"$ {_command_text(command)}")
    print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    result = {
        "name": name,
        "command": command,
        "returncode": completed.returncode,
        "log": str(log_path),
    }
    if completed.returncode != 0:
        raise RegressionFailure(f"step {name} failed with exit code {completed.returncode}")
    return result


def verify_parser_contract(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    candidates = payload.get("candidates", {})
    structured = candidates.get("structured_reference", [])
    flat = candidates.get("flat_text_baseline", [])
    wrong_role = candidates.get("wrong_role_corruption", [])

    if not structured or not all(row.get("decision") == "PASS" for row in structured):
        raise RegressionFailure("parser contract drift: structured_reference must PASS all fixtures")
    if not any(row.get("decision") == "REVIEW_REQUIRED" for row in flat):
        raise RegressionFailure(
            "parser contract drift: flat-text table loss must remain REVIEW_REQUIRED"
        )
    if not any(
        row.get("decision") == "FAIL" and row.get("silent_corruption") is True
        for row in wrong_role
    ):
        raise RegressionFailure(
            "parser contract drift: wrong-role silent corruption must remain a hard FAIL"
        )

    return {
        "structured_reference_all_pass": True,
        "flat_text_review_required_observed": True,
        "wrong_role_silent_corruption_fail_observed": True,
    }


def verify_state_event_harness(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    metrics = payload.get("metrics", {})
    required_zero = (
        "silent_stale_overwrite_accepted",
        "permanent_logical_event_gap_after_reconciliation",
        "event_without_authoritative_committed_transition",
        "duplicate_logical_projection",
        "cross_tenant_replay_success",
    )
    if payload.get("overall_status") != "PASS":
        raise RegressionFailure("state/event failure harness must PASS")
    if any(metrics.get(name) != 0 for name in required_zero):
        raise RegressionFailure("state/event hard-gate metric drift")
    if metrics.get("restart_replay_repair_pass_rate") != 1.0:
        raise RegressionFailure("restart/replay/repair pass rate must remain 100%")
    if metrics.get("backup_restore_pass_rate") != 1.0:
        raise RegressionFailure("backup/restore pass rate must remain 100%")
    return {
        "overall_status": "PASS",
        "hard_gate_zero_metrics": list(required_zero),
        "restart_replay_repair_pass_rate": 1.0,
        "backup_restore_pass_rate": 1.0,
    }


def main() -> int:
    if ARTIFACT_DIR.exists():
        shutil.rmtree(ARTIFACT_DIR)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    src_path = str(ROOT / "src")
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        src_path if not existing_pythonpath else os.pathsep.join((src_path, existing_pythonpath))
    )

    manifest: dict[str, object] = {
        "runner": "foundation_regression.v1",
        "python": sys.version,
        "dependencies": {
            "pydantic": _dependency_version("pydantic"),
            "pytest": _dependency_version("pytest"),
            "langgraph": _dependency_version("langgraph"),
        },
        "steps": [],
        "notes": [
            "LangGraph remains a W002 challenger pending runtime recheck; it is not installed by this foundation gate.",
            "The parser bakeoff is executed in deterministic offline observed-behavior mode; no network fetch is required.",
            "W006-T003 SQLite state/event substrate is a reference evidence candidate, not a production backend winner.",
        ],
        "status": "RUNNING",
    }
    manifest_path = ARTIFACT_DIR / "manifest.json"

    try:
        steps = manifest["steps"]
        assert isinstance(steps, list)

        steps.append(
            run_step(
                "compileall",
                [sys.executable, "-m", "compileall", "-q", "src", "tests", "experiments"],
                env=env,
            )
        )
        steps.append(
            run_step(
                "critical_foundation_suites",
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                    "tests/unit/domain",
                    "tests/factual",
                    "tests/policy",
                    "tests/formats",
                    "tests/generation",
                    "tests/runstore",
                    "tests/experiments/orchestration",
                    "tests/integration/foundation",
                ],
                env=env,
            )
        )
        steps.append(
            run_step(
                "factual_oracle",
                [
                    sys.executable,
                    "experiments/hard_gates/validate_factual_fixtures.py",
                    "--observed",
                    "tests/factual/observed_factual_v001.jsonl",
                ],
                env=env,
            )
        )

        parser_result = ARTIFACT_DIR / "parser_bakeoff_results.json"
        steps.append(
            run_step(
                "parser_bakeoff",
                [
                    sys.executable,
                    "experiments/parser_bakeoff/run_bakeoff.py",
                    "--output",
                    str(parser_result),
                ],
                env=env,
            )
        )
        manifest["parser_contract_assertions"] = verify_parser_contract(parser_result)

        state_event_result = ARTIFACT_DIR / "state_event_failure_harness.json"
        state_event_step = run_step(
            "state_event_failure_harness",
            [sys.executable, "tests/runstore/failure_harness_w006_t003.py"],
            env=env,
        )
        steps.append(state_event_step)
        state_event_log = Path(str(state_event_step["log"]))
        state_event_result.write_text(state_event_log.read_text(encoding="utf-8"), encoding="utf-8")
        manifest["state_event_contract_assertions"] = verify_state_event_harness(state_event_result)

        benchmark_path = ARTIFACT_DIR / "orchestration_benchmark.json"
        benchmark_step = run_step(
            "orchestration_benchmark",
            [sys.executable, "-m", "experiments.orchestration_smoke.benchmark"],
            env=env,
        )
        steps.append(benchmark_step)
        benchmark_log = Path(str(benchmark_step["log"]))
        benchmark_path.write_text(benchmark_log.read_text(encoding="utf-8"), encoding="utf-8")

        manifest["status"] = "PASS"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"\nPASS foundation-regression: manifest={manifest_path}")
        return 0
    except Exception as exc:
        manifest["status"] = "FAIL"
        manifest["failure"] = f"{type(exc).__name__}: {exc}"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"\nFAIL foundation-regression: {exc}", file=sys.stderr)
        print(f"manifest={manifest_path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
