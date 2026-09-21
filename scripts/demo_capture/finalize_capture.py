#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HARD_CAP_SECONDS = 300.0
TARGET_SECONDS = 280.0


class CaptureFinalizeError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe_duration_seconds(video: Path, *, ffprobe: str = "ffprobe") -> float:
    if shutil.which(ffprobe) is None:
        raise CaptureFinalizeError("ffprobe not found in PATH")
    completed = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise CaptureFinalizeError(f"ffprobe failed ({completed.returncode}): {completed.stdout}")
    try:
        value = float(completed.stdout.strip())
    except ValueError as exc:
        raise CaptureFinalizeError(f"invalid ffprobe duration: {completed.stdout!r}") from exc
    if value <= 0:
        raise CaptureFinalizeError(f"video duration must be positive, got {value}")
    return value


def build_final_manifest(*, video: Path, preflight: dict[str, Any], duration: float) -> dict[str, Any]:
    if duration > HARD_CAP_SECONDS:
        raise CaptureFinalizeError(f"duration {duration:.3f}s exceeds hard cap {HARD_CAP_SECONDS:.3f}s")
    repository = preflight.get("repository") or {}
    source_document = preflight.get("source_document") or {}
    if not repository.get("head_sha"):
        raise CaptureFinalizeError("preflight repository.head_sha missing")
    if not source_document.get("sha256"):
        raise CaptureFinalizeError("preflight source_document.sha256 missing")
    return {
        "schema_version": "academy-suno.demo-final-capture.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "task_id": preflight.get("task_id"),
        "attempt_id": preflight.get("attempt_id"),
        "repository": repository,
        "source_document": source_document,
        "video": {
            "path": str(video),
            "sha256": sha256_file(video),
            "size_bytes": video.stat().st_size,
            "duration_seconds": round(duration, 3),
            "hard_cap_seconds": HARD_CAP_SECONDS,
            "within_hard_cap": True,
            "target_seconds": TARGET_SECONDS,
            "target_delta_seconds": round(duration - TARGET_SECONDS, 3),
        },
        "content_review": {
            "status": "REQUIRES_HUMAN_VISUAL_REVIEW",
            "required_items": preflight.get("required_demo_path", []),
            "required_visible_evidence_labels": preflight.get("required_visible_evidence_labels", []),
            "note": "Duration/hash are measured mechanically. This manifest does not fabricate visual-review evidence.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure/hash a W004-T016 demo recording without overstating visual evidence")
    parser.add_argument("video", type=Path)
    parser.add_argument("--preflight", type=Path, default=Path("artifacts/demo/capture_preflight.json"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/demo/final_capture_manifest.json"))
    parser.add_argument("--ffprobe", default="ffprobe")
    args = parser.parse_args()
    try:
        if not args.video.is_file():
            raise CaptureFinalizeError(f"video not found: {args.video}")
        preflight = json.loads(args.preflight.read_text(encoding="utf-8"))
        duration = probe_duration_seconds(args.video, ffprobe=args.ffprobe)
        manifest = build_final_manifest(video=args.video, preflight=preflight, duration=duration)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(f"FINALIZE_FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
