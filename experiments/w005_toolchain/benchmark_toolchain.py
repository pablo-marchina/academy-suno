#!/usr/bin/env python3
"""Reproducible evidence harness for W005-T013.

No third-party Python packages are required by this harness itself.

Examples:
    python experiments/w005_toolchain/benchmark_toolchain.py baseline --repo .
    python experiments/w005_toolchain/benchmark_toolchain.py python-managers --repeats 3

The package-manager probe only runs tools that are already installed on PATH.
It never installs a candidate tool implicitly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from typing import Any


LOCK_NAMES = {
    "uv.lock",
    "poetry.lock",
    "pdm.lock",
    "pylock.toml",
    "requirements.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}

ACTION_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"\buses:\s*([^\s#]+)")
PIP_RE = re.compile(r"(?:python\s+-m\s+pip|\bpip)\s+install\b")

PYPROJECT = """[project]
name = "w005-toolchain-bench"
version = "0.0.0"
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2,<3",
  "httpx>=0.27,<1",
  "pytest>=8,<9",
]
"""

MANAGERS: dict[str, dict[str, Any]] = {
    "uv": {
        "lock": ["uv", "lock"],
        "sync": ["uv", "sync", "--locked"],
        "verify": ["uv", "run", "--locked", "python", "-c", "import pydantic,httpx,pytest"],
        "lockfile": "uv.lock",
    },
    "poetry": {
        "lock": ["poetry", "lock"],
        "sync": ["poetry", "install", "--no-root"],
        "verify": ["poetry", "run", "python", "-c", "import pydantic,httpx,pytest"],
        "lockfile": "poetry.lock",
    },
    "pdm": {
        "lock": ["pdm", "lock"],
        "sync": ["pdm", "sync"],
        "verify": ["pdm", "run", "python", "-c", "import pydantic,httpx,pytest"],
        "lockfile": "pdm.lock",
    },
}


def _files(root: Path, names: set[str]) -> list[str]:
    found: list[str] = []
    for path in root.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.name in names:
            found.append(str(path.relative_to(root)))
    return sorted(found)


def baseline(repo: Path) -> dict[str, Any]:
    workflows_dir = repo / ".github" / "workflows"
    workflows = []
    if workflows_dir.exists():
        workflows = sorted(
            [p for p in workflows_dir.iterdir() if p.is_file() and p.suffix in {".yml", ".yaml"}]
        )

    pip_lines: list[str] = []
    action_refs: list[str] = []
    sha_pinned: list[str] = []
    permissions_declarations = 0

    for wf in workflows:
        for line_no, line in enumerate(wf.read_text(encoding="utf-8").splitlines(), start=1):
            if PIP_RE.search(line):
                pip_lines.append(f"{wf.relative_to(repo)}:{line_no}:{line.strip()}")
            if re.match(r"^\s*permissions\s*:", line):
                permissions_declarations += 1
            match = USES_RE.search(line)
            if not match:
                continue
            ref = match.group(1)
            action_refs.append(ref)
            if "@" in ref:
                _, version = ref.rsplit("@", 1)
                if ACTION_SHA_RE.fullmatch(version):
                    sha_pinned.append(ref)

    return {
        "repo": str(repo.resolve()),
        "workflow_count": len(workflows),
        "workflow_files": [str(p.relative_to(repo)) for p in workflows],
        "pyproject_files": _files(repo, {"pyproject.toml"}),
        "node_package_manifests": _files(repo, {"package.json"}),
        "lockfiles": _files(repo, LOCK_NAMES),
        "inline_pip_install_count": len(pip_lines),
        "inline_pip_install_locations": pip_lines,
        "action_reference_count": len(action_refs),
        "full_sha_pinned_action_reference_count": len(sha_pinned),
        "full_sha_pinned_action_references": sha_pinned,
        "permissions_declaration_count": permissions_declarations,
    }


def _run(command: list[str], cwd: Path, env: dict[str, str]) -> dict[str, Any]:
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
    elapsed = time.perf_counter() - started
    return {
        "command": command,
        "returncode": proc.returncode,
        "wall_seconds": round(elapsed, 4),
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
    }


def _sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def probe_manager(name: str, repeats: int) -> dict[str, Any]:
    spec = MANAGERS[name]
    executable = spec["lock"][0]
    resolved = shutil.which(executable)
    if not resolved:
        return {"manager": name, "available": False, "reason": f"{executable} not found on PATH"}

    runs: list[dict[str, Any]] = []
    for repeat in range(1, repeats + 1):
        with tempfile.TemporaryDirectory(prefix=f"w005-{name}-") as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
            env = os.environ.copy()
            env.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")

            lock_first = _run(spec["lock"], root, env)
            lock_path = root / spec["lockfile"]
            digest_first = _sha256(lock_path)
            sync_first = _run(spec["sync"], root, env) if lock_first["returncode"] == 0 else None
            verify = _run(spec["verify"], root, env) if sync_first and sync_first["returncode"] == 0 else None
            sync_warm = _run(spec["sync"], root, env) if verify and verify["returncode"] == 0 else None
            lock_second = _run(spec["lock"], root, env) if verify and verify["returncode"] == 0 else None
            digest_second = _sha256(lock_path)

            runs.append(
                {
                    "repeat": repeat,
                    "lock_first": lock_first,
                    "sync_first": sync_first,
                    "verify_imports": verify,
                    "sync_warm": sync_warm,
                    "lock_second": lock_second,
                    "lock_sha256_first": digest_first,
                    "lock_sha256_second": digest_second,
                    "repeat_lock_byte_stable": bool(digest_first and digest_first == digest_second),
                }
            )

    return {
        "manager": name,
        "available": True,
        "executable": resolved,
        "repeats": repeats,
        "runs": runs,
    }


def python_managers(repeats: int) -> dict[str, Any]:
    return {
        "scenario": {
            "python": ">=3.11",
            "dependencies": ["pydantic>=2,<3", "httpx>=0.27,<1", "pytest>=8,<9"],
            "note": "First sync uses the machine's existing global package cache if any; compare on the same clean runner image for decision evidence.",
        },
        "results": [probe_manager(name, repeats) for name in MANAGERS],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    base = sub.add_parser("baseline", help="Inventory the repository's current toolchain/CI surface")
    base.add_argument("--repo", type=Path, default=Path("."))

    managers = sub.add_parser("python-managers", help="Probe installed uv/Poetry/PDM candidates")
    managers.add_argument("--repeats", type=int, default=3)

    args = parser.parse_args()
    if args.command == "baseline":
        payload = baseline(args.repo)
    else:
        if args.repeats < 1:
            parser.error("--repeats must be >= 1")
        payload = python_managers(args.repeats)

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
