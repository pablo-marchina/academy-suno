from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from PIL import Image

from scripts.demo_capture_final.run_capture import (
    image_rms_difference,
    image_variance,
    parse_ffprobe_duration,
    parse_fps,
    sha256_file,
    sha256_text,
    validate_pdf,
)


def test_hash_helpers_bind_exact_bytes_and_text(tmp_path: Path) -> None:
    path = tmp_path / "source.pdf"
    raw = b"%PDF-1.7\nfinal-demo-test\n"
    path.write_bytes(raw)
    expected = hashlib.sha256(raw).hexdigest()
    assert sha256_file(path) == expected
    assert validate_pdf(path) == expected
    assert sha256_text("abc") == hashlib.sha256(b"abc").hexdigest()


def test_validate_pdf_rejects_non_pdf(tmp_path: Path) -> None:
    path = tmp_path / "not-a-pdf.bin"
    path.write_bytes(b"not a PDF")
    with pytest.raises(RuntimeError, match="not a PDF"):
        validate_pdf(path)


def test_duration_and_fps_parsers_require_positive_values() -> None:
    assert parse_ffprobe_duration("72.125\n") == pytest.approx(72.125)
    assert parse_fps("25/1") == pytest.approx(25.0)
    assert parse_fps("30000/1001") == pytest.approx(29.970, rel=1e-3)
    with pytest.raises(RuntimeError, match="non-positive"):
        parse_ffprobe_duration("0")
    with pytest.raises(RuntimeError, match="denominator"):
        parse_fps("25/0")


def test_image_validation_distinguishes_frames(tmp_path: Path) -> None:
    first = tmp_path / "first.png"
    second = tmp_path / "second.png"
    Image.new("RGB", (64, 64), (240, 240, 240)).save(first)
    image = Image.new("RGB", (64, 64), (240, 240, 240))
    for x in range(16, 48):
        for y in range(16, 48):
            image.putpixel((x, y), (20, 20, 20))
    image.save(second)
    assert image_rms_difference(first, first) == pytest.approx(0.0)
    assert image_rms_difference(first, second) > 0
    assert image_variance(second) > image_variance(first)
