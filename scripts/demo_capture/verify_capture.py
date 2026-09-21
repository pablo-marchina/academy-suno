#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


class VerifyError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify persisted hashes/cap for W004-T016 capture artifacts")
    parser.add_argument("--manifest", type=Path, default=Path("artifacts/demo/final_capture_manifest.json"))
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, default=Path("artifacts/demo/source_document.pdf"))
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        video = data.get("video") or {}
        source = data.get("source_document") or {}
        if video.get("duration_seconds", 999999) > video.get("hard_cap_seconds", 300):
            raise VerifyError("manifest duration exceeds hard cap")
        if sha256_file(args.video) != video.get("sha256"):
            raise VerifyError("video SHA-256 mismatch")
        if sha256_file(args.pdf) != source.get("sha256"):
            raise VerifyError("source PDF SHA-256 mismatch")
        if data.get("content_review", {}).get("status") != "REQUIRES_HUMAN_VISUAL_REVIEW":
            raise VerifyError("content-review boundary drifted")
        print("VERIFY_PASS")
        print(f"repo_sha={data.get('repository', {}).get('head_sha')}")
        print(f"video_sha256={video.get('sha256')}")
        print(f"duration_seconds={video.get('duration_seconds')}")
        print(f"source_pdf_sha256={source.get('sha256')}")
        return 0
    except Exception as exc:
        print(f"VERIFY_FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
