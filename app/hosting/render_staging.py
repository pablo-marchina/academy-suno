#!/usr/bin/env python3
"""Public, read-only infrastructure staging endpoint. NOT the recipient-facing product.

This explicitly does not expose the historical unauthenticated recipient upload
server or any GitHub artifacts/source tree to the internet.
"""
from __future__ import annotations

import json
import os
import runpy
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
ENUM_SOURCE = ROOT / "src" / "suno_content" / "domain" / "enums.py"

HTML = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Academy Suno — staging técnico</title>
<style>body{font-family:system-ui,sans-serif;max-width:750px;margin:8vh auto;
padding:0 20px;color:#18243a;line-height:1.6}main{border:1px solid #ced5df;
border-radius:14px;padding:25px}code{background:#f2f4f7;padding:2px 5px}
strong{color:#8b2820}a{color:#1d4e8f}</style></head>
<body><main><h1>Academy Suno</h1>
<p><strong>Ambiente técnico de staging — não é o produto pronto para uso.</strong></p>
<p>Este serviço gratuito comprova apenas inicialização HTTP e verificação
do contrato canônico 3 audiências × 3 formatos. Ele não executa
geração de conteúdo, não oferece upload de documentos, não recebe dados
de clientes e não está conectado ao banco Neon.</p>
<p>Produção: <code>NOT_AUTHORIZED</code>. Avaliação de público:
<code>AI_ONLY / DIAGNOSTIC_ONLY</code>.</p>
<p>Diagnóstico técnico: <a href="/healthz">/healthz</a>.
A indisponibilidade do fluxo real pode ser confirmada em
<a href="/readyz">/readyz</a> (503).</p>
<p>A implantação do produto completo depende de autenticação, isolamento
por tenant, persistência durável, evidência de falhas e gates de segurança.</p>
</main></body></html>"""


def _contract_status() -> dict[str, object]:
    """Read the *real committed* audience/format enums, not hardcoded counts."""
    try:
        domain = runpy.run_path(str(ENUM_SOURCE))
        audiences = sorted(member.value for member in domain["AudienceLevel"])
        formats = sorted(member.value for member in domain["OutputFormat"])
        valid = audiences == ["ADVANCED", "BEGINNER", "INTERMEDIATE"] and formats == [
            "ARTICLE", "CAROUSEL", "SHORT_VIDEO"
        ]
        return {
            "status": "ok" if valid else "contract_violation",
            "canonical_audiences": audiences,
            "canonical_formats": formats,
            "branches_defined": len(audiences) * len(formats),
            "contract_valid": valid,
            "production_ready": False,
            "product_api_enabled": False,
            "neon_database_connected": False,
            "evidence_class": "CODE_CONTRACT_SMOKE_ONLY",
        }
    except (OSError, KeyError, ValueError, SyntaxError) as exc:
        return {
            "status": "contract_unavailable",
            "error_class": type(exc).__name__,
            "contract_valid": False,
            "production_ready": False,
            "product_api_enabled": False,
            "neon_database_connected": False,
            "evidence_class": "CODE_CONTRACT_SMOKE_ONLY",
        }


class StagingHandler(BaseHTTPRequestHandler):
    server_version = "AcademySunoStaging"
    sys_version = ""

    def _reply(self, status: HTTPStatus, content_type: str, body: bytes, *, send_body: bool = True,
               allow: str | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; style-src 'unsafe-inline'; "
                         "base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        if allow is not None:
            self.send_header("Allow", allow)
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def _read_only(self, *, head: bool = False) -> None:
        # Do not serve paths, files, uploaded data, query-driven HTML or debugging internals.
        path = urlsplit(self.path).path
        if path == "/":
            self._reply(HTTPStatus.OK, "text/html; charset=utf-8",
                        HTML.encode("utf-8"), send_body=not head)
        elif path in {"/healthz", "/readyz"}:
            obj = _contract_status()
            if path == "/readyz":
                obj = {
                    "status": "product_not_ready",
                    "production_ready": False,
                    "reason": "AUTH_AND_DURABLE_MULTITENANT_WORKFLOW_NOT_DEPLOYED",
                }
                code = HTTPStatus.SERVICE_UNAVAILABLE
            else:
                code = HTTPStatus.OK if obj["contract_valid"] else HTTPStatus.SERVICE_UNAVAILABLE
            self._reply(code, "application/json; charset=utf-8",
                        json.dumps(obj, sort_keys=True).encode("utf-8"), send_body=not head)
        else:
            self._reply(HTTPStatus.NOT_FOUND, "text/plain; charset=utf-8",
                        b"Not Found\n", send_body=not head)

    def do_GET(self) -> None:  # noqa: N802
        self._read_only()

    def do_HEAD(self) -> None:  # noqa: N802
        self._read_only(head=True)

    def do_POST(self) -> None:  # noqa: N802
        self._reply(HTTPStatus.METHOD_NOT_ALLOWED, "text/plain; charset=utf-8",
                    b"Staging endpoint is read-only\n", allow="GET, HEAD")

    do_PUT = do_POST
    do_PATCH = do_POST
    do_DELETE = do_POST

    def log_message(self, _fmt: str, *_args: object) -> None:
        # Never copy attacker-controlled paths/query strings, cookies, uploads or secrets to logs.
        pass


def main() -> None:
    # Render injects PORT; binding must be public on the container, not loopback.
    port = int(os.environ.get("PORT", "10000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), StagingHandler)
    print(f"Academy Suno staging-only HTTP listener started on port {port}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
