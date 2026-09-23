#!/usr/bin/env python3
"""W006-T008 reproducible package-manager bakeoff on the repository's declared graph.

The script deliberately installs no manager. CI provisions exact manager versions first.
All candidates receive the same flattened direct dependency set from the root pyproject.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import tomllib
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
IMPORTS = [
    "pydantic",
    "jsonschema",
    "pytest",
    "pypdf",
    "dbos",
    "langgraph",
    "langgraph.checkpoint.sqlite",
]

MANAGERS: dict[str, dict[str, Any]] = {
    "uv": {
        "version": ["uv", "--version"],
        "lock": ["uv", "lock"],
        "sync": ["uv", "sync", "--locked", "--no-install-project"],
        "verify": ["uv", "run", "--no-sync", "python", "-c", "import " + ",".join(IMPORTS)],
        "lockfile": "uv.lock",
    },
    "poetry": {
        "version": ["poetry", "--version"],
        "lock": ["poetry", "lock"],
        "sync": ["poetry", "install", "--no-root"],
        "verify": ["poetry", "run", "python", "-c", "import " + ",".join(IMPORTS)],
        "lockfile": "poetry.lock",
    },
    "pdm": {
        "version": ["pdm", "--version"],
        "lock": ["pdm", "lock"],
        "sync": ["pdm", "sync"],
        "verify": ["pdm", "run", "python", "-c", "import " + ",".join(IMPORTS)],
        "lockfile": "pdm.lock",
    },
}


def declared_dependencies(pyproject: Path) -> list[str]:
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    deps = list(data.get("project", {}).get("dependencies", []))
    for group in data.get("dependency-groups", {}).values():
        for entry in group:
            if not isinstance(entry, str):
                raise ValueError("benchmark only supports direct string dependency-group entries")
            deps.append(entry)
    return sorted(dict.fromkeys(deps))


def candidate_pyproject(deps: list[str]) -> str:
    lines = [
        "[project]",
        'name = "academy-suno-toolchain-benchmark"',
        'version = "0.0.0"',
        'requires-python = ">=3.13,<3.14"',
        "dependencies = [",
    ]
    lines.extend(f'  "{dep}",' for dep in deps)
    lines.extend([
        "]",
        "",
        "[tool.pdm]",
        "distribution = false",
        "",
    ])
    return "\n".join(lines)


def run(command: list[str], cwd: Path, env: dict[str, str]) -> dict[str, Any]:
    started = time.perf_counter()
    proc = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "wall_seconds": round(time.perf_counter() - started, 4),
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
    }


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def median_success(runs: list[dict[str, Any]], field: str) -> float | None:
    values = [
        row[field]["wall_seconds"]
        for row in runs
        if row.get(field) and row[field]["returncode"] == 0
    ]
    return round(statistics.median(values), 4) if values else None


def probe(name: str, deps: list[str], repeats: int, locks_dir: Path | None) -> dict[str, Any]:
    spec = MANAGERS[name]
    if not shutil.which(spec["lock"][0]):
        return {"manager": name, "available": False, "hard_gate_pass": False}

    env = os.environ.copy()
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    env["PYTHONUTF8"] = "1"
    version = run(spec["version"], ROOT, env)
    runs: list[dict[str, Any]] = []

    for repeat in range(1, repeats + 1):
        with tempfile.TemporaryDirectory(prefix=f"w006-t008-{name}-") as tmp:
            project = Path(tmp)
            benchmark_project = candidate_pyproject(deps)
            (project / "pyproject.toml").write_text(benchmark_project, encoding="utf-8")
            first_lock = run(spec["lock"], project, env)
            lock_path = project / spec["lockfile"]
            first_digest = sha256(lock_path)
            if repeat == 1 and first_digest and locks_dir is not None:
                target = locks_dir / name
                target.mkdir(parents=True, exist_ok=True)
                (target / "pyproject.toml").write_text(benchmark_project, encoding="utf-8")
                shutil.copy2(lock_path, target / spec["lockfile"])
            first_sync = run(spec["sync"], project, env) if first_lock["returncode"] == 0 else None
            verify = run(spec["verify"], project, env) if first_sync and first_sync["returncode"] == 0 else None
            warm_sync = run(spec["sync"], project, env) if verify and verify["returncode"] == 0 else None
            second_lock = run(spec["lock"], project, env) if verify and verify["returncode"] == 0 else None
            second_digest = sha256(lock_path)
            runs.append({
                "repeat": repeat,
                "lock_first": first_lock,
                "sync_first": first_sync,
                "verify_imports": verify,
                "sync_warm": warm_sync,
                "lock_second": second_lock,
                "lock_sha256_first": first_digest,
                "lock_sha256_second": second_digest,
                "repeat_lock_byte_stable": bool(first_digest and first_digest == second_digest),
            })

    hard_gate_pass = all(
        row["lock_first"]["returncode"] == 0
        and row["sync_first"] is not None and row["sync_first"]["returncode"] == 0
        and row["verify_imports"] is not None and row["verify_imports"]["returncode"] == 0
        and row["sync_warm"] is not None and row["sync_warm"]["returncode"] == 0
        and row["lock_second"] is not None and row["lock_second"]["returncode"] == 0
        and row["repeat_lock_byte_stable"]
        for row in runs
    )
    return {
        "manager": name,
        "available": True,
        "version_probe": version,
        "repeats": repeats,
        "hard_gate_pass": hard_gate_pass,
        "median_lock_first_seconds": median_success(runs, "lock_first"),
        "median_sync_first_seconds": median_success(runs, "sync_first"),
        "median_sync_warm_seconds": median_success(runs, "sync_warm"),
        "runs": runs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--locks-dir", type=Path)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be >= 1")

    pyproject = ROOT / "pyproject.toml"
    deps = declared_dependencies(pyproject)
    locks_dir = args.locks_dir
    if locks_dir is not None:
        locks_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "w006-t008-toolchain-bakeoff.v1",
        "repository_pyproject_sha256": hashlib.sha256(pyproject.read_bytes()).hexdigest(),
        "python": sys.version,
        "platform": platform.platform(),
        "criteria_order": [
            "all declared dependencies resolve",
            "locked install succeeds",
            "declared imports verify",
            "warm re-sync succeeds",
            "repeated lock is byte-stable",
            "only after all hard gates: operational simplicity and measured same-runner timing may distinguish candidates",
        ],
        "dependencies": deps,
        "results": [probe(name, deps, args.repeats, locks_dir) for name in MANAGERS],
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
