from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


prepare = load("prepare_capture", "scripts/demo_capture/prepare_capture.py")
finalize = load("finalize_capture", "scripts/demo_capture/finalize_capture.py")


class CaptureToolsTest(unittest.TestCase):
    def test_sha256_and_pdf_magic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.pdf"
            path.write_bytes(b"%PDF-1.7\nexample")
            prepare.require_pdf(path)
            self.assertEqual(
                prepare.sha256_file(path),
                "4c05a9d358d6ae170333b35b69ddf857bde90fe521d98136c23d8cda233fcedd",
            )

    def test_non_pdf_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.pdf"
            path.write_bytes(b"not-pdf")
            with self.assertRaises(prepare.CapturePreflightError):
                prepare.require_pdf(path)

    def test_final_manifest_accepts_sub_five_minutes_and_keeps_visual_review_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            video = Path(tmp) / "demo.mp4"
            video.write_bytes(b"video-bytes")
            preflight = {
                "task_id": "W004-T016",
                "attempt_id": "A01",
                "repository": {"head_sha": "a" * 40},
                "source_document": {"sha256": "b" * 64},
                "required_demo_path": ["real recipient-facing UI"],
                "required_visible_evidence_labels": ["MECHANICS_ONLY"],
            }
            manifest = finalize.build_final_manifest(video=video, preflight=preflight, duration=279.5)
            self.assertTrue(manifest["video"]["within_hard_cap"])
            self.assertEqual(manifest["video"]["duration_seconds"], 279.5)
            self.assertEqual(manifest["content_review"]["status"], "REQUIRES_HUMAN_VISUAL_REVIEW")

    def test_final_manifest_rejects_over_five_minutes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            video = Path(tmp) / "demo.mp4"
            video.write_bytes(b"video-bytes")
            preflight = {
                "repository": {"head_sha": "a" * 40},
                "source_document": {"sha256": "b" * 64},
            }
            with self.assertRaises(finalize.CaptureFinalizeError):
                finalize.build_final_manifest(video=video, preflight=preflight, duration=300.001)


if __name__ == "__main__":
    unittest.main()
