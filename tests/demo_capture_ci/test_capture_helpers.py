from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from scripts.demo_capture_ci.run_capture import parse_ffprobe_duration, sha256_file, validate_pdf


def test_sha256_file_hashes_exact_bytes(tmp_path: Path) -> None:
    path = tmp_path / "source.pdf"
    raw = b"%PDF-1.7\nreal-bytes-for-test\n"
    path.write_bytes(raw)
    assert sha256_file(path) == hashlib.sha256(raw).hexdigest()
    assert validate_pdf(path) == hashlib.sha256(raw).hexdigest()


def test_validate_pdf_rejects_non_pdf(tmp_path: Path) -> None:
    path = tmp_path / "not-a-pdf.bin"
    path.write_bytes(b"synthetic text, not a PDF")
    with pytest.raises(RuntimeError, match="not a PDF"):
        validate_pdf(path)


def test_parse_ffprobe_duration_requires_positive_value() -> None:
    assert parse_ffprobe_duration("42.125\n") == pytest.approx(42.125)
    with pytest.raises(RuntimeError, match="non-positive"):
        parse_ffprobe_duration("0")
