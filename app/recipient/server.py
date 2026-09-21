#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import sys
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from suno_content.ingest import (  # noqa: E402
    IngestResult,
    IntegratedEvidence,
    ingest_pdf_bytes,
    ingest_pdf_path,
    ingest_text,
    load_integrated_evidence,
)

DEFAULT_EVIDENCE = ROOT / "docs/release/release_smoke/W004-T012-A01-manifest.json"
MAX_REQUEST_BYTES = 26 * 1024 * 1024


def _e(value: object) -> str:
    return html.escape(str(value), quote=True)


def _page(body: str, *, title: str = "Suno Academy — Recipient App") -> str:
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(title)}</title>
<style>
:root {{ font-family: Inter, system-ui, sans-serif; color: #172033; background: #f5f7fb; }}
body {{ margin: 0; }}
main {{ max-width: 1180px; margin: 0 auto; padding: 28px 18px 56px; }}
h1,h2,h3 {{ margin-top: 0; }}
.card {{ background: white; border: 1px solid #dfe5ef; border-radius: 14px; padding: 18px; margin: 0 0 16px; box-shadow: 0 2px 8px rgba(20,30,50,.04); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); gap: 12px; }}
label {{ display: block; font-weight: 700; margin: 10px 0 6px; }}
textarea,input[type=text],input[type=file] {{ width: 100%; box-sizing: border-box; padding: 10px; border: 1px solid #bfc9d8; border-radius: 8px; background: #fff; }}
textarea {{ min-height: 150px; resize: vertical; }}
button {{ margin-top: 14px; padding: 10px 16px; border: 0; border-radius: 9px; font-weight: 800; cursor: pointer; }}
code,.mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; overflow-wrap: anywhere; }}
.badge {{ display: inline-block; padding: 4px 8px; border: 1px solid #cbd4e1; border-radius: 999px; margin: 2px 4px 2px 0; font-size: .85rem; font-weight: 700; }}
table {{ width: 100%; border-collapse: collapse; }}
th,td {{ border-bottom: 1px solid #e3e8f0; padding: 9px; text-align: left; vertical-align: top; }}
.small {{ font-size: .9rem; color: #526078; }}
.warn {{ border-left: 5px solid currentColor; }}
pre {{ white-space: pre-wrap; word-break: break-word; background:#f7f9fc; padding:12px; border-radius:8px; }}
</style>
</head><body><main>{body}</main></body></html>"""


def render_home(*, error: str | None = None) -> str:
    alert = (
        f'<section class="card warn"><strong>Erro:</strong> {_e(error)}</section>' if error else ""
    )
    body = f"""
<h1>Suno Academy — fluxo recipient-facing</h1>
<p>Entrada real de texto/PDF → hash/proveniência → source-trust gate → planejamento 3×3 → evidência integrada de hard gates/repair.</p>
{alert}
<section class="card">
  <h2>1. Forneça um documento</h2>
  <form method="post" action="/process" enctype="multipart/form-data">
    <label for="text_input">Texto bruto</label>
    <textarea id="text_input" name="text_input" placeholder="Cole aqui o texto de um documento financeiro público..."></textarea>
    <label for="pdf_path">ou caminho local para PDF</label>
    <input id="pdf_path" name="pdf_path" type="text" placeholder="/caminho/para/documento.pdf">
    <label for="pdf_upload">ou upload de PDF</label>
    <input id="pdf_upload" name="pdf_upload" type="file" accept="application/pdf,.pdf">
    <button type="submit">Processar documento</button>
  </form>
  <p class="small">Precedência: upload PDF → caminho PDF → texto. Limite: 25 MiB. Tabelas sem papéis/células resolvíveis falham de forma fechada e não viram SOURCE_READY/PASS.</p>
</section>
<section class="card warn">
  <h2>Escopo de evidência</h2>
  <span class="badge">MECHANICS_ONLY</span>
  <span class="badge">DIAGNOSTIC_ONLY</span>
  <span class="badge">PRODUCTION_UNKNOWN</span>
  <p>O preview 3×3 comprova o fluxo e os contratos mecânicos. Ele não é evidência de qualidade de provider/modelo, calibração humana ou production readiness.</p>
</section>
"""
    return _page(body)


def _evidence_panel(evidence: IntegratedEvidence | None) -> str:
    if evidence is None:
        return "<p>Evidência integrada indisponível nesta cópia; nenhum estado foi promovido.</p>"
    lineage = evidence.repair_lineage
    return f"""
<div class="grid">
  <div><strong>Mechanics E2E</strong><br><span class="badge">{_e(evidence.mechanics_end_to_end)}</span></div>
  <div><strong>Audience thresholds</strong><br><span class="badge">{_e(evidence.audience_thresholds)}</span></div>
  <div><strong>Provider quality/latency/cost</strong><br><span class="badge">{_e(evidence.provider_quality_latency_cost)}</span></div>
  <div><strong>Parser implementation</strong><br><span class="badge">{_e(evidence.parser_implementation)}</span></div>
  <div><strong>Production readiness</strong><br><span class="badge">{_e(evidence.production_release_readiness)}</span></div>
</div>
<h3>Repair lineage observado (T012)</h3>
<table>
<tr><th>Job</th><th>Antes</th><th>Depois</th><th>Fresh gates</th><th>Siblings immutable</th></tr>
<tr><td>{_e(lineage.get('job_id','N/A'))}</td><td>{_e(lineage.get('before_status','N/A'))}</td><td>{_e(lineage.get('after_status','N/A'))}</td><td>{_e(lineage.get('fresh_hard_gate_runs','N/A'))}</td><td>{_e(lineage.get('siblings_immutable','N/A'))}</td></tr>
</table>
<p class="small mono">before={_e(lineage.get('before_output_hash','N/A'))}<br>after={_e(lineage.get('after_output_hash','N/A'))}</p>
"""


def render_result(result: IngestResult, evidence: IntegratedEvidence | None) -> str:
    warnings = "".join(f"<li>{_e(warning)}</li>" for warning in result.warnings) or "<li>nenhum warning</li>"
    rows = "".join(
        "<tr>"
        f"<td>{_e(cell.audience)}</td>"
        f"<td>{_e(cell.output_format)}</td>"
        f"<td class='mono'>{_e(cell.job_id)}</td>"
        f"<td>{_e(cell.status)}</td>"
        f"<td>{_e(cell.evidence_scope)}</td>"
        f"<td>{_e(cell.preview)}</td>"
        "</tr>"
        for cell in result.cells
    )
    body = f"""
<p><a href="/">← novo documento</a></p>
<h1>Resultado recipient-facing</h1>
<section class="card">
<h2>2. Proveniência + source trust</h2>
<div class="grid">
  <div><strong>Input</strong><br>{_e(result.input_kind)}</div>
  <div><strong>Status</strong><br><span class="badge">{_e(result.source_status)}</span></div>
  <div><strong>Hard gate</strong><br><span class="badge">{_e(result.hard_gate_status.value)}</span></div>
  <div><strong>Source trust</strong><br><span class="badge">{_e(result.source_trust.value)}</span></div>
  <div><strong>Parser</strong><br>{_e(result.parser_name)} {_e(result.parser_version)}</div>
  <div><strong>Confidence</strong><br>{result.extraction_confidence:.3f}</div>
  <div><strong>Pages</strong><br>{result.page_count}</div>
  <div><strong>Table-role ambiguity</strong><br>{_e(result.table_role_ambiguity)}</div>
</div>
<p><strong>Artifact ref:</strong> <span class="mono">{_e(result.artifact_label)}</span></p>
<p><strong>SHA-256 do input bruto:</strong> <span class="mono">{_e(result.source_hash)}</span></p>
<p><strong>Source ID:</strong> <span class="mono">{_e(result.source.source_id)}</span></p>
<h3>Warnings</h3><ul>{warnings}</ul>
</section>
<section class="card">
<h2>3. Comparação 3×3</h2>
<p><span class="badge">MECHANICS_ONLY</span> Jobs usam o contrato canônico 3 audiências × 3 formatos quando o source-trust gate permite. O preview é mecânico, não provider-generated.</p>
<table><thead><tr><th>Audiência</th><th>Formato</th><th>Job</th><th>Status</th><th>Escopo</th><th>Preview</th></tr></thead><tbody>{rows}</tbody></table>
</section>
<section class="card">
<h2>4. Evidência integrada / repair</h2>
{_evidence_panel(evidence)}
</section>
<section class="card warn">
<h2>Não-claims</h2>
<p><span class="badge">DIAGNOSTIC_ONLY</span> thresholds de audiência não estão human-calibrated.</p>
<p><span class="badge">PRODUCTION_UNKNOWN</span> qualidade/latência/uso/custo de provider real não foram promovidos.</p>
<p>Esta tela não declara parser winner nem production/release readiness.</p>
</section>
<section class="card"><h2>Texto extraído</h2><pre>{_e(result.extracted_text[:12000])}</pre></section>
"""
    return _page(body, title=f"{result.source_status} — Suno Academy")


def _parse_multipart(content_type: str, body: bytes) -> tuple[dict[str, str], tuple[str, bytes] | None]:
    message = BytesParser(policy=policy.default).parsebytes(
        f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8") + body
    )
    fields: dict[str, str] = {}
    upload: tuple[str, bytes] | None = None
    if not message.is_multipart():
        return fields, upload
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        if not name:
            continue
        payload = part.get_payload(decode=True) or b""
        filename = part.get_filename()
        if name == "pdf_upload" and filename and payload:
            upload = (Path(filename).name, payload)
        elif filename is None:
            charset = part.get_content_charset() or "utf-8"
            fields[name] = payload.decode(charset, errors="replace")
    return fields, upload


def _parse_form(content_type: str, body: bytes) -> tuple[dict[str, str], tuple[str, bytes] | None]:
    if content_type.startswith("multipart/form-data"):
        return _parse_multipart(content_type, body)
    values = parse_qs(body.decode("utf-8", errors="replace"), keep_blank_values=True)
    return {key: vals[-1] for key, vals in values.items() if vals}, None


def process_submission(
    fields: dict[str, str],
    upload: tuple[str, bytes] | None,
    *,
    evidence_path: Path = DEFAULT_EVIDENCE,
) -> tuple[IngestResult, IntegratedEvidence | None]:
    if upload is not None:
        filename, raw_bytes = upload
        result = ingest_pdf_bytes(raw_bytes, artifact_label=f"upload/{filename}")
    elif fields.get("pdf_path", "").strip():
        result = ingest_pdf_path(fields["pdf_path"].strip())
    elif fields.get("text_input", "").strip():
        result = ingest_text(fields["text_input"], artifact_label="recipient-text-input.txt")
    else:
        raise ValueError("forneça texto, caminho PDF ou upload PDF")

    try:
        evidence = load_integrated_evidence(evidence_path)
    except (OSError, ValueError, TypeError):
        evidence = None
    return result, evidence


class RecipientHandler(BaseHTTPRequestHandler):
    server_version = "SunoRecipientApp/1.0"

    def _send_html(self, document: str, status: int = 200) -> None:
        payload = document.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802
        if self.path not in {"/", "/index.html"}:
            self._send_html(_page("<h1>404</h1>"), status=404)
            return
        self._send_html(render_home())

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/process":
            self._send_html(_page("<h1>404</h1>"), status=404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > MAX_REQUEST_BYTES:
                raise ValueError("request vazia ou acima do limite de 26 MiB")
            body = self.rfile.read(size)
            content_type = self.headers.get("Content-Type", "application/x-www-form-urlencoded")
            fields, upload = _parse_form(content_type, body)
            result, evidence = process_submission(fields, upload)
            self._send_html(render_result(result, evidence))
        except Exception as exc:
            self._send_html(render_home(error=f"{type(exc).__name__}: {exc}"), status=400)

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("recipient-app: " + (fmt % args) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Recipient-facing PDF/text → 3x3 evidence application")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), RecipientHandler)
    print(f"Recipient app: http://{args.host}:{args.port}")
    print("Evidence posture: MECHANICS_ONLY / DIAGNOSTIC_ONLY / PRODUCTION_UNKNOWN")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
