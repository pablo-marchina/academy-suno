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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BCB_PDF_URL = "https://www.bcb.gov.br/content/publicacoes/ref/202605/RELESTAB202605-refPub.pdf"
DEFAULT_APP_URL = "http://127.0.0.1:8765"
MAX_DURATION_SECONDS = 300.0
SUCCESS_TEXT = (
    "O Banco Central acompanha estabilidade financeira, crédito, liquidez e capital. "
    "Este texto de demonstração testa o fluxo recipient-facing sem alegar qualidade de provider."
)


@dataclass(frozen=True)
class Milestone:
    slug: str
    label: str
    timestamp_seconds: float
    screenshot_path: Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_pdf(path: Path) -> str:
    raw_prefix = path.read_bytes()[:16].lstrip()
    if not raw_prefix.startswith(b"%PDF-"):
        raise RuntimeError(f"downloaded source is not a PDF by magic bytes: {path}")
    return sha256_file(path)


def download_public_pdf(url: str, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "academy-suno-w004-t019-final-demo/1.0"},
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


def parse_fps(raw: str) -> float:
    value = raw.strip()
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        denominator_value = float(denominator)
        if denominator_value == 0:
            raise RuntimeError(f"invalid fps denominator: {value}")
        fps = float(numerator) / denominator_value
    else:
        fps = float(value)
    if fps <= 0:
        raise RuntimeError(f"invalid non-positive fps: {fps}")
    return fps


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


def ffprobe_video_metadata(path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=index,codec_type,codec_name,width,height,avg_frame_rate:format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(completed.stdout)
    video_streams = [stream for stream in payload.get("streams", []) if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in payload.get("streams", []) if stream.get("codec_type") == "audio"]
    if len(video_streams) != 1:
        raise RuntimeError(f"expected exactly one video stream, got {len(video_streams)}")
    video = video_streams[0]
    return {
        "codec": video.get("codec_name"),
        "width": int(video.get("width", 0)),
        "height": int(video.get("height", 0)),
        "fps": round(parse_fps(str(video.get("avg_frame_rate", "0"))), 3),
        "audio_present": bool(audio_streams),
        "duration_seconds": round(parse_ffprobe_duration(str(payload["format"]["duration"])), 3),
    }


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


def image_rms_difference(first: Path, second: Path) -> float:
    with Image.open(first).convert("RGB") as left, Image.open(second).convert("RGB") as right:
        if left.size != right.size:
            right = right.resize(left.size)
        difference = ImageChops.difference(left, right)
        stats = ImageStat.Stat(difference)
        squared = sum(value * value for value in stats.rms) / max(len(stats.rms), 1)
        return squared**0.5


def image_variance(path: Path) -> float:
    with Image.open(path).convert("L") as image:
        return float(ImageStat.Stat(image).var[0])


def extract_and_validate_video_frames(
    video_path: Path,
    milestones: list[Milestone],
    output_dir: Path,
) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    validations: list[dict[str, Any]] = []
    hashes: set[str] = set()
    for index, milestone in enumerate(milestones, start=1):
        frame = output_dir / f"{index:02d}-{milestone.slug}.png"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-ss",
                f"{milestone.timestamp_seconds:.3f}",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                str(frame),
            ],
            check=True,
        )
        if not frame.is_file() or frame.stat().st_size < 10_000:
            raise RuntimeError(f"representative frame was not decoded correctly: {frame}")
        variance = image_variance(frame)
        if variance < 120.0:
            raise RuntimeError(f"representative frame appears visually degenerate: {frame} variance={variance}")
        rms = image_rms_difference(milestone.screenshot_path, frame)
        if rms > 115.0:
            raise RuntimeError(
                f"decoded video frame diverged too far from the same-state browser screenshot: {frame} rms={rms:.2f}"
            )
        digest = sha256_file(frame)
        hashes.add(digest)
        validations.append(
            {
                "slug": milestone.slug,
                "label": milestone.label,
                "timestamp_seconds": round(milestone.timestamp_seconds, 3),
                "decoded_frame": frame.name,
                "decoded_frame_sha256": digest,
                "reference_screenshot": milestone.screenshot_path.name,
                "reference_screenshot_sha256": sha256_file(milestone.screenshot_path),
                "grayscale_variance": round(variance, 3),
                "rms_vs_reference_screenshot": round(rms, 3),
                "status": "PASS",
            }
        )
    if len(hashes) < max(3, len(milestones) // 2):
        raise RuntimeError("representative video frames are unexpectedly non-distinct")
    return validations


def _inject_caption(page: Any, text: str, tone: str = "info") -> None:
    page.evaluate(
        """([text, tone]) => {
          let box = document.getElementById('academy-demo-caption');
          if (!box) {
            box = document.createElement('div');
            box.id = 'academy-demo-caption';
            Object.assign(box.style, {
              position: 'fixed', top: '18px', right: '18px', zIndex: '2147483647',
              maxWidth: '560px', padding: '14px 18px', borderRadius: '12px',
              fontFamily: 'Inter, system-ui, sans-serif', fontSize: '18px', fontWeight: '800',
              lineHeight: '1.35', boxShadow: '0 8px 28px rgba(0,0,0,.24)',
              border: '2px solid rgba(255,255,255,.85)'
            });
            document.body.appendChild(box);
          }
          const palette = tone === 'warning'
            ? ['#fff3cd', '#5f4500']
            : tone === 'success'
              ? ['#dff6e7', '#124d2b']
              : ['#e8f0ff', '#173f80'];
          box.style.background = palette[0];
          box.style.color = palette[1];
          box.textContent = text;
        }""",
        [text, tone],
    )


def capture_browser_session(
    app_url: str,
    pdf_path: Path,
    pdf_sha256: str,
    output_dir: Path,
) -> dict[str, Any]:
    from playwright.sync_api import sync_playwright

    video_dir = output_dir / "playwright-video"
    screenshot_dir = output_dir / "browser-milestones"
    video_dir.mkdir(parents=True, exist_ok=True)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    assertions: list[str] = []
    milestones: list[Milestone] = []
    success_text_sha256 = sha256_text(SUCCESS_TEXT)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        browser_version = browser.version
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        video = page.video
        if video is None:
            raise RuntimeError("Playwright did not attach a video recorder to the page")
        video_clock_start = time.monotonic()

        def hold(
            slug: str,
            label: str,
            caption: str,
            seconds: float,
            *,
            tone: str = "info",
        ) -> None:
            _inject_caption(page, caption, tone)
            page.wait_for_timeout(500)
            screenshot = screenshot_dir / f"{len(milestones) + 1:02d}-{slug}.png"
            page.screenshot(path=str(screenshot), full_page=False)
            timestamp = time.monotonic() - video_clock_start
            milestones.append(Milestone(slug, label, timestamp, screenshot))
            page.wait_for_timeout(int(seconds * 1000))

        page.goto(app_url, wait_until="networkidle")
        page.get_by_role("heading", name="Suno Academy — fluxo recipient-facing").wait_for()
        for marker in ("MECHANICS_ONLY", "DIAGNOSTIC_ONLY", "PRODUCTION_UNKNOWN"):
            if page.get_by_text(marker, exact=True).count() < 1:
                raise RuntimeError(f"home evidence marker not found: {marker}")
        assertions.append("home rendered MECHANICS_ONLY / DIAGNOSTIC_ONLY / PRODUCTION_UNKNOWN boundaries")
        hold(
            "home",
            "recipient-facing start",
            "Etapa 1/7 — App real: texto/PDF → provenance → source-trust → 3×3 → repair. Claims externos continuam bloqueados.",
            5.0,
        )

        page.locator("#text_input").fill(SUCCESS_TEXT)
        hold(
            "success-input",
            "successful source input",
            "Etapa 2/7 — Caminho positivo primeiro: entrada textual pública/controlável para demonstrar SOURCE_READY/PASS sem fabricar evidência humana/provider.",
            4.0,
            tone="success",
        )
        page.get_by_role("button", name="Processar documento").click()
        page.get_by_role("heading", name="Resultado recipient-facing").wait_for()
        page.get_by_text("SOURCE_READY", exact=True).wait_for()
        page.get_by_text("PASS", exact=True).first.wait_for()
        provenance = page.locator("section.card", has_text="2. Proveniência + source trust")
        provenance.scroll_into_view_if_needed()
        page.get_by_text(success_text_sha256, exact=True).wait_for()
        assertions.append("success text reached SOURCE_READY/PASS and displayed exact UTF-8 input SHA-256")
        hold(
            "success-provenance",
            "SOURCE_READY/PASS provenance",
            "Etapa 3/7 — SOURCE_READY / PASS. O hash visível amarra a entrada real; source trust governa o fan-out.",
            7.0,
            tone="success",
        )

        comparison = page.locator("section.card", has_text="3. Comparação 3×3")
        comparison.scroll_into_view_if_needed()
        if comparison.locator("tbody tr").count() != 9:
            raise RuntimeError("success path did not render exactly nine 3x3 cells")
        if comparison.get_by_text("PLANNED_MECHANICS_ONLY", exact=True).count() != 9:
            raise RuntimeError("success 3x3 cells were not all mechanics-only planned cells")
        assertions.append("success path rendered all 9/9 audience × format cells as PLANNED_MECHANICS_ONLY")
        hold(
            "success-3x3",
            "9/9 mechanics matrix",
            "Etapa 4/7 — Fan-out 3 audiências × 3 formatos: 9/9 células mecânicas visíveis. Isto não é claim de qualidade de provider.",
            8.0,
            tone="success",
        )

        evidence = page.locator("section.card", has_text="4. Evidência integrada / repair")
        evidence.scroll_into_view_if_needed()
        evidence.get_by_text("FAIL", exact=True).wait_for()
        evidence.get_by_text("PASS", exact=True).wait_for()
        evidence_text = evidence.inner_text()
        if "True" not in evidence_text:
            raise RuntimeError("repair panel did not expose fresh-gate/sibling immutability truth values")
        assertions.append("persisted FAIL→repair→PASS lineage exposed fresh-gate and sibling-immutability truth values")
        hold(
            "repair",
            "persisted FAIL→repair→PASS",
            "Etapa 5/7 — Repair auditável: FAIL → repair → PASS, com hard gates reexecutados e siblings aceitos imutáveis.",
            8.0,
            tone="success",
        )

        non_claims = page.locator("section.card.warn", has_text="Não-claims")
        non_claims.scroll_into_view_if_needed()
        for marker in ("DIAGNOSTIC_ONLY", "PRODUCTION_UNKNOWN"):
            non_claims.get_by_text(marker, exact=True).wait_for()
        assertions.append("non-claim panel preserved DIAGNOSTIC_ONLY and PRODUCTION_UNKNOWN evidence boundaries")
        hold(
            "non-claims",
            "evidence boundaries",
            "Limites de evidência — thresholds seguem DIAGNOSTIC_ONLY; provider quality/latency/usage/cost segue PRODUCTION_UNKNOWN/BLOCKED; sem production-readiness claim.",
            6.0,
            tone="warning",
        )

        page.get_by_role("link", name="← novo documento").click()
        page.get_by_role("heading", name="Suno Academy — fluxo recipient-facing").wait_for()
        page.locator("#pdf_upload").set_input_files(str(pdf_path))
        hold(
            "bcb-input",
            "BCB negative-control input",
            "Etapa 6/7 — Negative-control real: PDF público do Banco Central. O objetivo aqui é provar fail-closed quando a provenance de papéis de tabela é ambígua.",
            5.0,
            tone="warning",
        )
        page.get_by_role("button", name="Processar documento").click()
        page.get_by_role("heading", name="Resultado recipient-facing").wait_for(timeout=120_000)
        pdf_provenance = page.locator("section.card", has_text="2. Proveniência + source trust")
        pdf_provenance.scroll_into_view_if_needed()
        page.get_by_text(pdf_sha256, exact=True).wait_for(timeout=30_000)
        page.get_by_text("SOURCE_BLOCKED", exact=True).wait_for()
        page.get_by_text("REVIEW_REQUIRED", exact=True).wait_for()
        page.get_by_text("LOW", exact=True).wait_for()
        if "Table-role ambiguity" not in pdf_provenance.inner_text() or "True" not in pdf_provenance.inner_text():
            raise RuntimeError("BCB negative control did not expose table-role ambiguity")
        page.get_by_text("TABLE_ROLE_AMBIGUITY:TEXT_LAYER_HAS_NO_CELL_ROLE_PROVENANCE", exact=True).wait_for()
        assertions.append("real BCB PDF displayed exact raw-byte SHA and fail-closed SOURCE_BLOCKED/REVIEW_REQUIRED/LOW state")
        hold(
            "bcb-blocked",
            "fail-closed negative control",
            "Etapa 7/7 — Safety negative-control: SOURCE_BLOCKED / REVIEW_REQUIRED / LOW. A ambiguidade de tabela é preservada; nenhum bypass para deixar a demo verde.",
            9.0,
            tone="warning",
        )

        pdf_comparison = page.locator("section.card", has_text="3. Comparação 3×3")
        pdf_comparison.scroll_into_view_if_needed()
        if pdf_comparison.locator("tbody tr").count() != 9:
            raise RuntimeError("BCB negative-control path did not render nine blocked 3x3 cells")
        if pdf_comparison.get_by_text("BLOCKED_SOURCE", exact=True).count() != 9:
            raise RuntimeError("BCB negative-control 3x3 cells were not all BLOCKED_SOURCE")
        assertions.append("BCB negative-control rendered all 9/9 cells as BLOCKED_SOURCE")
        hold(
            "bcb-3x3",
            "blocked 9/9 downstream cells",
            "Negative-control concluído — as 9 células ficam BLOCKED_SOURCE porque source trust falhou fechado. Isso é comportamento de segurança, não falha mascarada.",
            6.0,
            tone="warning",
        )

        context.close()
        recorded_path = Path(video.path())
        browser.close()

    if not recorded_path.is_file() or recorded_path.stat().st_size == 0:
        raise RuntimeError("Playwright recording did not produce a non-empty video")
    return {
        "recorded_path": recorded_path,
        "browser_version": browser_version,
        "assertions": assertions,
        "milestones": milestones,
        "success_text_sha256": success_text_sha256,
    }


def build_manifest(
    *,
    source_url: str,
    source_pdf: Path,
    source_sha256: str,
    success_text_sha256: str,
    raw_video: Path,
    final_video: Path,
    video_metadata: dict[str, Any],
    browser_version: str,
    assertions: list[str],
    frame_validations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "w004-t019-final-demo-capture.v1",
        "task_id": "W004-T019",
        "attempt_id": "A01",
        "base_state_version": "0028",
        "base_commit_sha": "584a23406291a42c29eb795d34bedd2de0357647",
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
            "expected_artifact_name": f"w004-t019-final-demo-{os.environ.get('GITHUB_SHA', git_head())}",
        },
        "sources": {
            "success_text": {
                "artifact_label": "recipient-text-input.txt",
                "encoding": "utf-8",
                "sha256": success_text_sha256,
                "expected_state": "SOURCE_READY/PASS",
            },
            "bcb_negative_control": {
                "publisher": "Banco Central do Brasil",
                "document": "Relatório de Estabilidade Financeira — maio 2026",
                "url": source_url,
                "path": source_pdf.name,
                "magic_validated": True,
                "sha256": source_sha256,
                "size_bytes": source_pdf.stat().st_size,
                "synthetic_fallback_used": False,
                "expected_state": "SOURCE_BLOCKED/REVIEW_REQUIRED/LOW",
                "reason": "TABLE_ROLE_AMBIGUITY:TEXT_LAYER_HAS_NO_CELL_ROLE_PROVENANCE",
            },
        },
        "video": {
            "raw_file": raw_video.name,
            "raw_sha256": sha256_file(raw_video),
            "mp4_file": final_video.name,
            "mp4_sha256": sha256_file(final_video),
            "size_bytes": final_video.stat().st_size,
            "duration_seconds": video_metadata["duration_seconds"],
            "hard_cap_seconds": MAX_DURATION_SECONDS,
            "duration_gate": "PASS" if video_metadata["duration_seconds"] <= MAX_DURATION_SECONDS else "FAIL",
            "codec": video_metadata["codec"],
            "width": video_metadata["width"],
            "height": video_metadata["height"],
            "fps": video_metadata["fps"],
            "audio_present": video_metadata["audio_present"],
            "capture_mechanism": "Playwright Chromium browser-context recording with visible in-page step captions",
            "representative_frame_validation": frame_validations,
        },
        "runtime": {
            "python": platform.python_version(),
            "playwright": importlib.metadata.version("playwright"),
            "pillow": importlib.metadata.version("Pillow"),
            "browser": f"Chromium {browser_version}",
            "ffmpeg": command_version(["ffmpeg", "-version"]),
            "ffprobe": command_version(["ffprobe", "-version"]),
        },
        "dom_content_assertions": assertions,
        "evidence_boundaries": {
            "mechanics": "MECHANICS_ONLY",
            "audience_thresholds": "DIAGNOSTIC_ONLY",
            "provider_quality_latency_usage_cost": "PRODUCTION_UNKNOWN/BLOCKED",
            "human_evidence_claim": False,
            "provider_evidence_claim": False,
            "production_readiness_claim": False,
            "bcb_negative_control_bypass_used": False,
            "visual_claim_basis": "real browser MP4 + exact source hashes + DOM assertions + post-encode representative-frame decoding/comparison",
        },
    }


def main() -> int:
    output_dir = Path(os.environ.get("DEMO_FINAL_OUTPUT_DIR", "/tmp/w004-t019-final-demo"))
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
        capture = capture_browser_session(DEFAULT_APP_URL, source_pdf, source_sha256, output_dir)
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)
        server_log.close()

    raw_source = Path(capture["recorded_path"])
    raw_video = output_dir / "final-demo.webm"
    shutil.copy2(raw_source, raw_video)
    final_video = output_dir / "final-demo.mp4"
    convert_to_mp4(raw_video, final_video)
    video_metadata = ffprobe_video_metadata(final_video)
    if video_metadata["duration_seconds"] > MAX_DURATION_SECONDS:
        raise RuntimeError(
            f"recorded demo duration {video_metadata['duration_seconds']:.3f}s exceeds hard cap {MAX_DURATION_SECONDS:.0f}s"
        )
    if video_metadata["width"] != 1280 or video_metadata["height"] != 720:
        raise RuntimeError(f"unexpected final video dimensions: {video_metadata['width']}x{video_metadata['height']}")

    frame_validations = extract_and_validate_video_frames(
        final_video,
        list(capture["milestones"]),
        output_dir / "decoded-video-frames",
    )
    manifest = build_manifest(
        source_url=source_url,
        source_pdf=source_pdf,
        source_sha256=source_sha256,
        success_text_sha256=str(capture["success_text_sha256"]),
        raw_video=raw_video,
        final_video=final_video,
        video_metadata=video_metadata,
        browser_version=str(capture["browser_version"]),
        assertions=list(capture["assertions"]),
        frame_validations=frame_validations,
    )
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(manifest_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
