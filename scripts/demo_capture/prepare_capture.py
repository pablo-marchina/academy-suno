#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TASK_ID = "W004-T016"
ATTEMPT_ID = "A01"
RECIPIENT_APP_BASE_SHA = "0980534866ed84c2f6af28453f6cb20cd1c7efba"
DEFAULT_PDF_URL = "https://www.bcb.gov.br/content/publicacoes/ref/202605/RELESTAB202605-refPub.pdf"
DEFAULT_PDF_LABEL = "Banco Central do Brasil — Relatório de Estabilidade Financeira — maio 2026"
REQUIRED_PATHS = (
    "app/recipient/server.py",
    "scripts/release_smoke/run_release_smoke.py",
    "docs/release/release_smoke/W004-T012-A01-manifest.json",
)


class CapturePreflightError(RuntimeError):
    pass


def _run(command: list[str], *, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and completed.returncode != 0:
        raise CapturePreflightError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stdout}"
        )
    return completed


def _git(repo: Path, *args: str) -> str:
    return _run(["git", *args], cwd=repo).stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_pdf(path: Path) -> None:
    if not path.is_file():
        raise CapturePreflightError(f"PDF missing: {path}")
    with path.open("rb") as handle:
        magic = handle.read(5)
    if magic != b"%PDF-":
        raise CapturePreflightError(f"not a PDF by magic bytes: {path}")


def download_pdf(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "academy-suno-demo-capture/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise CapturePreflightError(f"PDF download failed: {type(exc).__name__}: {exc}") from exc
    require_pdf(destination)


def verify_repo(repo: Path, *, required_base_sha: str) -> dict[str, Any]:
    head = _git(repo, "rev-parse", "HEAD")
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    status = _git(repo, "status", "--porcelain")
    dirty_lines = [line for line in status.splitlines() if line.strip()]
    disallowed_dirty = []
    for line in dirty_lines:
        path_text = line[3:].strip() if len(line) >= 4 else line.strip()
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        if not path_text.startswith("artifacts/demo/"):
            disallowed_dirty.append(line)
    if disallowed_dirty:
        raise CapturePreflightError(
            "working tree contains changes outside artifacts/demo: " + repr(disallowed_dirty)
        )
    ancestor = _run(
        ["git", "merge-base", "--is-ancestor", required_base_sha, head],
        cwd=repo,
        check=False,
    )
    if ancestor.returncode != 0:
        raise CapturePreflightError(
            f"HEAD {head} is not a descendant of recipient-app base {required_base_sha}"
        )
    missing = [relative for relative in REQUIRED_PATHS if not (repo / relative).is_file()]
    if missing:
        raise CapturePreflightError(f"required integrated paths missing: {missing}")
    return {
        "head_sha": head,
        "branch": branch,
        "working_tree_clean": status == "",
        "working_tree_clean_except_capture_artifacts": not disallowed_dirty,
        "working_tree_porcelain": status,
        "recipient_app_base_sha": required_base_sha,
        "recipient_app_base_is_ancestor": True,
    }


def run_release_smoke(repo: Path, runtime_dir: Path) -> dict[str, Any]:
    workdir = runtime_dir / "release-smoke"
    manifest = workdir / "manifest.json"
    command = [
        sys.executable,
        "scripts/release_smoke/run_release_smoke.py",
        "--workdir",
        str(workdir),
        "--output",
        str(manifest),
    ]
    completed = _run(command, cwd=repo, check=False)
    if completed.returncode != 0:
        raise CapturePreflightError(f"release smoke failed\n{completed.stdout}")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    if payload.get("status") != "PASS":
        raise CapturePreflightError(f"release smoke manifest is not PASS: {payload.get('status')}")
    return {
        "command": command,
        "manifest": str(manifest.relative_to(repo) if manifest.is_relative_to(repo) else manifest),
        "status": payload.get("status"),
        "lineage": payload.get("lineage"),
        "evidence_posture": payload.get("evidence_posture"),
    }


def build_preflight(
    *,
    repo: Path,
    pdf_path: Path,
    pdf_url: str | None,
    pdf_label: str,
    run_smoke: bool,
    runtime_dir: Path,
) -> dict[str, Any]:
    repo_info = verify_repo(repo, required_base_sha=RECIPIENT_APP_BASE_SHA)
    require_pdf(pdf_path)
    source = {
        "label": pdf_label,
        "public_source_url": pdf_url,
        "local_path": str(pdf_path.relative_to(repo) if pdf_path.is_relative_to(repo) else pdf_path),
        "sha256": sha256_file(pdf_path),
        "size_bytes": pdf_path.stat().st_size,
        "pdf_magic_verified": True,
    }
    smoke = run_release_smoke(repo, runtime_dir) if run_smoke else {"status": "NOT_RUN_BY_REQUEST"}
    return {
        "schema_version": "academy-suno.demo-capture-preflight.v1",
        "task_id": TASK_ID,
        "attempt_id": ATTEMPT_ID,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": repo_info,
        "source_document": source,
        "release_smoke": smoke,
        "required_visible_evidence_labels": [
            "MECHANICS_ONLY",
            "DIAGNOSTIC_ONLY",
            "PRODUCTION_UNKNOWN",
            "BLOCKED/PENDING",
        ],
        "required_demo_path": [
            "real recipient-facing UI",
            "raw text ingestion",
            "public PDF ingestion",
            "raw input SHA-256/provenance",
            "canonical 3x3 view",
            "persisted FAIL->repair->PASS lineage",
            "explicit evidence/non-claim boundary",
        ],
        "hard_duration_cap_seconds": 300.0,
        "target_duration_seconds": 280.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare exact-provenance inputs for W004-T016 final demo capture")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--pdf-url", default=DEFAULT_PDF_URL)
    parser.add_argument("--pdf-label", default=DEFAULT_PDF_LABEL)
    parser.add_argument("--pdf-path", type=Path, default=None, help="Use an already-downloaded PDF instead of downloading --pdf-url")
    parser.add_argument("--output", type=Path, default=Path("artifacts/demo/capture_preflight.json"))
    parser.add_argument("--runtime-dir", type=Path, default=Path("artifacts/demo/runtime"))
    parser.add_argument("--skip-release-smoke", action="store_true")
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    runtime_dir = args.runtime_dir if args.runtime_dir.is_absolute() else repo / args.runtime_dir
    if args.pdf_path is not None:
        pdf_path = args.pdf_path if args.pdf_path.is_absolute() else repo / args.pdf_path
        pdf_url: str | None = args.pdf_url or None
    else:
        pdf_path = repo / "artifacts/demo/source_document.pdf"
        pdf_url = args.pdf_url
        download_pdf(args.pdf_url, pdf_path)

    try:
        payload = build_preflight(
            repo=repo,
            pdf_path=pdf_path.resolve(),
            pdf_url=pdf_url,
            pdf_label=args.pdf_label,
            run_smoke=not args.skip_release_smoke,
            runtime_dir=runtime_dir.resolve(),
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        print(f"\nPreflight written to {output}")
        print("Next: start `PYTHONPATH=src python app/recipient/server.py --host 127.0.0.1 --port 8765` and follow docs/demo/final/CAPTURE_RUNBOOK.md")
        return 0
    except Exception as exc:
        print(f"PRECHECK_FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
