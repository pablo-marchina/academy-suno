#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BCB_PDF_URL = "https://www.bcb.gov.br/content/publicacoes/ref/202605/RELESTAB202605-refPub.pdf"
DEFAULT_APP_URL = "http://127.0.0.1:8765"
MAX_DURATION_SECONDS = 300.0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_pdf(path: Path) -> str:
    raw_prefix = path.read_bytes()[:16].lstrip()
    if not raw_prefix.startswith(b"%PDF-"):
        raise RuntimeError(f"downloaded source is not a PDF by magic bytes: {path}")
    return sha256_file(path)


def download_public_pdf(url: str, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "academy-suno-w004-t017-ci/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            status = getattr(response, "status", 200)
            if status != 200:
                raise RuntimeError(f"BCB download returned HTTP {status}")
            with destination.open("wb") as output:
                shutil.copyfileobj(response, output)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    return validate_pdf(destination)


def parse_ffprobe_duration(raw: str) -> float:
    value = float(raw.strip())
    if value <= 0:
        raise RuntimeError(f"invalid non-positive video duration: {value}")
    return value


def command_version(command: list[str]) -> str:
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    return (completed.stdout or completed.stderr).splitlines()[0].strip()


def ffprobe_duration(path: Path) -> float:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return parse_ffprobe_duration(completed.stdout)


def wait_for_port(host: str, port: int, timeout_seconds: float = 30.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return
        except OSError:
            time.sleep(0.25)
    raise RuntimeError(f"recipient app did not listen on {host}:{port} within {timeout_seconds}s")


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def convert_to_mp4(webm: Path, mp4: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(webm),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-an",
            str(mp4),
        ],
        check=True,
    )
    if not mp4.is_file() or mp4.stat().st_size == 0:
        raise RuntimeError("ffmpeg did not create a non-empty MP4")


def capture_browser_session(app_url: str, pdf_path: Path, pdf_sha256: str, video_dir: Path) -> dict[str, Any]:
    from playwright.sync_api import sync_playwright

    video_dir.mkdir(parents=True, exist_ok=True)
    assertions: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        browser_version = browser.version
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        video = page.video
        if video is None:
            raise RuntimeError("Playwright did not attach a video recorder to the page")

        page.goto(app_url, wait_until="networkidle")
        page.get_by_role("heading", name="Suno Academy — fluxo recipient-facing").wait_for()
        for marker in ("MECHANICS_ONLY", "DIAGNOSTIC_ONLY", "PRODUCTION_UNKNOWN"):
            if page.get_by_text(marker, exact=True).count() < 1:
                raise RuntimeError(f"home evidence marker not found: {marker}")
        assertions.append("home rendered evidence boundaries")

        text_input = (
            "O Banco Central acompanha estabilidade financeira, crédito, liquidez e capital. "
            "Este texto de demonstração testa o fluxo recipient-facing sem alegar qualidade de provider."
        )
        page.locator("#text_input").fill(text_input)
        page.get_by_role("button", name="Processar documento").click()
        page.get_by_role("heading", name="Resultado recipient-facing").wait_for()
        page.get_by_text("SOURCE_READY", exact=True).wait_for()
        page.get_by_text("PASS", exact=True).first.wait_for()
        comparison = page.locator("section.card", has_text="3. Comparação 3×3")
        comparison.scroll_into_view_if_needed()
        if comparison.locator("tbody tr").count() != 9:
            raise RuntimeError("text ingestion did not render exactly nine 3x3 cells")
        if comparison.get_by_text("PLANNED_MECHANICS_ONLY", exact=True).count() != 9:
            raise RuntimeError("text ingestion 3x3 cells were not all mechanics-only planned cells")
        assertions.append("text ingestion reached SOURCE_READY/PASS and rendered 9 mechanics-only cells")

        evidence = page.locator("section.card", has_text="4. Evidência integrada / repair")
        evidence.scroll_into_view_if_needed()
        evidence.get_by_text("FAIL", exact=True).wait_for()
        evidence.get_by_text("PASS", exact=True).wait_for()
        if "True" not in evidence.inner_text():
            raise RuntimeError("repair panel did not expose fresh-gate/sibling immutability truth values")
        non_claims = page.locator("section.card.warn", has_text="Não-claims")
        non_claims.scroll_into_view_if_needed()
        for marker in ("DIAGNOSTIC_ONLY", "PRODUCTION_UNKNOWN"):
            non_claims.get_by_text(marker, exact=True).wait_for()
        assertions.append("persisted FAIL→repair→PASS evidence panel and non-claim labels were visited")

        page.get_by_role("link", name="← novo documento").click()
        page.get_by_role("heading", name="Suno Academy — fluxo recipient-facing").wait_for()
        page.locator("#pdf_upload").set_input_files(str(pdf_path))
        page.get_by_role("button", name="Processar documento").click()
        page.get_by_role("heading", name="Resultado recipient-facing").wait_for(timeout=120_000)
        provenance = page.locator("section.card", has_text="2. Proveniência + source trust")
        provenance.scroll_into_view_if_needed()
        if "PDF" not in provenance.inner_text():
            raise RuntimeError("PDF ingestion did not render input kind PDF")
        page.get_by_text(pdf_sha256, exact=True).wait_for(timeout=30_000)
        assertions.append("real BCB PDF upload rendered exact raw-byte SHA-256 in recipient UI")

        pdf_comparison = page.locator("section.card", has_text="3. Comparação 3×3")
        pdf_comparison.scroll_into_view_if_needed()
        if pdf_comparison.locator("tbody tr").count() != 9:
            raise RuntimeError("PDF ingestion did not render exactly nine 3x3 cells")
        pdf_evidence = page.locator("section.card", has_text="4. Evidência integrada / repair")
        pdf_evidence.scroll_into_view_if_needed()
        pdf_evidence.get_by_text("FAIL", exact=True).wait_for()
        pdf_evidence.get_by_text("PASS", exact=True).wait_for()
        page.locator("section.card.warn", has_text="Não-claims").scroll_into_view_if_needed()
        page.wait_for_timeout(1500)
        assertions.append("PDF path visited 3x3, repair evidence and evidence-state labels")

        context.close()
        recorded_path = Path(video.path())
        browser.close()

    if not recorded_path.is_file() or recorded_path.stat().st_size == 0:
        raise RuntimeError("Playwright recording did not produce a non-empty video")
    return {
        "recorded_path": recorded_path,
        "browser_version": browser_version,
        "assertions": assertions,
    }


def build_manifest(
    *,
    source_url: str,
    source_pdf: Path,
    source_sha256: str,
    raw_video: Path,
    final_video: Path,
    duration_seconds: float,
    browser_version: str,
    assertions: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "w004-t017-demo-capture-ci.v1",
        "task_id": "W004-T017",
        "attempt_id": "A01",
        "base_state_version": "0026",
        "base_commit_sha": "6269c4b8466ff794d1f448507f2e4e3ed15d48dd",
        "task_commit_sha": git_head(),
        "status": "PASS_TASK_SCOPE",
        "ci": {
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "job": os.environ.get("GITHUB_JOB"),
            "sha": os.environ.get("GITHUB_SHA"),
            "ref": os.environ.get("GITHUB_REF"),
            "actor": os.environ.get("GITHUB_ACTOR"),
            "server_url": os.environ.get("GITHUB_SERVER_URL"),
            "expected_artifact_name": f"w004-t017-demo-{os.environ.get('GITHUB_SHA', git_head())}",
        },
        "source": {
            "publisher": "Banco Central do Brasil",
            "document": "Relatório de Estabilidade Financeira — maio 2026",
            "url": source_url,
            "path": source_pdf.name,
            "magic_validated": True,
            "sha256": source_sha256,
            "size_bytes": source_pdf.stat().st_size,
            "synthetic_fallback_used": False,
        },
        "video": {
            "raw_file": raw_video.name,
            "raw_sha256": sha256_file(raw_video),
            "mp4_file": final_video.name,
            "mp4_sha256": sha256_file(final_video),
            "size_bytes": final_video.stat().st_size,
            "duration_seconds": round(duration_seconds, 3),
            "hard_cap_seconds": MAX_DURATION_SECONDS,
            "duration_gate": "PASS" if duration_seconds <= MAX_DURATION_SECONDS else "FAIL",
            "capture_mechanism": "Playwright Chromium browser context video recording",
        },
        "runtime": {
            "python": platform.python_version(),
            "playwright": importlib.metadata.version("playwright"),
            "browser": f"Chromium {browser_version}",
            "ffmpeg": command_version(["ffmpeg", "-version"]),
            "ffprobe": command_version(["ffprobe", "-version"]),
        },
        "dom_content_assertions": assertions,
        "evidence_boundaries": {
            "mechanics": "MECHANICS_ONLY",
            "audience_thresholds": "DIAGNOSTIC_ONLY",
            "provider_quality_latency_cost": "PRODUCTION_UNKNOWN/BLOCKED",
            "human_evidence_claim": False,
            "provider_evidence_claim": False,
            "production_readiness_claim": False,
            "visual_claim_basis": "real browser recording plus DOM/content assertions; no storyboard/screenshot substitution",
        },
    }


def main() -> int:
    output_dir = Path(os.environ.get("DEMO_CI_OUTPUT_DIR", "/tmp/w004-t017-demo-ci"))
    output_dir.mkdir(parents=True, exist_ok=True)
    source_url = os.environ.get("BCB_PDF_URL", DEFAULT_BCB_PDF_URL)
    source_pdf = output_dir / "bcb-financial-source.pdf"
    source_sha256 = download_public_pdf(source_url, source_pdf)

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    server_log = (output_dir / "recipient-app.log").open("w", encoding="utf-8")
    server = subprocess.Popen(
        [sys.executable, "app/recipient/server.py", "--host", "127.0.0.1", "--port", "8765"],
        cwd=ROOT,
        env=env,
        stdout=server_log,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_port("127.0.0.1", 8765)
        capture = capture_browser_session(DEFAULT_APP_URL, source_pdf, source_sha256, output_dir / "playwright-video")
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)
        server_log.close()

    raw_source = Path(capture["recorded_path"])
    raw_video = output_dir / "browser-demo.webm"
    shutil.copy2(raw_source, raw_video)
    final_video = output_dir / "browser-demo.mp4"
    convert_to_mp4(raw_video, final_video)
    duration_seconds = ffprobe_duration(final_video)
    if duration_seconds > MAX_DURATION_SECONDS:
        raise RuntimeError(
            f"recorded demo duration {duration_seconds:.3f}s exceeds hard cap {MAX_DURATION_SECONDS:.0f}s"
        )

    manifest = build_manifest(
        source_url=source_url,
        source_pdf=source_pdf,
        source_sha256=source_sha256,
        raw_video=raw_video,
        final_video=final_video,
        duration_seconds=duration_seconds,
        browser_version=str(capture["browser_version"]),
        assertions=list(capture["assertions"]),
    )
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(manifest_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
