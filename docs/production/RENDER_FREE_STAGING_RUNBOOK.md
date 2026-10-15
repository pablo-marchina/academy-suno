# Academy Suno — Render Free safe staging runbook

**Date:** 2026-10-15
**Owner workspace:** `Pablo's workspace` / ID `tea-db8g1d6q1p3s73d8k10g` (explicit operator confirmation)
**Scope:** a single Render **Free** Web Service named `academy-suno`; no paid plan or add-on.
**Database:** existing isolated Neon Free project `cold-math-95888995`; **not connected to public staging probe**, deliberately no `DATABASE_URL` until real auth/storage security gates pass.
**Production/quality decision:** `PENDING_EVIDENCE`, not a winner/LOCK.

## Security and exact deployment boundary

The existing `app/recipient/server.py` is a reference/demo receiver with an untrusted caller-supplied `pdf_path` and no real production identity/tenant boundary. **DO NOT deploy or expose it publicly.** This would expose arbitrary local filesystem inputs. The existing Cockpit is diagnostic/reference evidence, not a substitute for live authenticated multiuser product.

Render Free staging instead runs `app/hosting/render_staging.py`, a tiny **read-only infrastructure probe**:
- `GET /`: truthful status page, no claims of generated content/product readiness.
- `GET /healthz`: checks `AudienceLevel` and `OutputFormat` from committed real source to confirm the **defined 3 × 3 = 9 contracts**. This does NOT prove 9 generated outputs or provider execution.
- `GET /readyz`: always 503 until authenticated multiuser product and durability gates are separately implemented/evidenced.
- `GET /src/...`: 404; no static file source or private artifacts accessible.
- `POST,PUT,PATCH,DELETE`: 405; no upload, arbitrary path, data mutation or PDF parsing exposed.
- CSP, no-store, nosniff, no-referrer, frame-deny headers; query data not logged.

## Render Free service parameters

- Owner workspace: explicit ID above. Preserve all preexisting unrelated resources.
- Name: `academy-suno`.
- Repository: `https://github.com/pablo-marchina/academy-suno`.
- Branch: `main`, auto deploy `yes`, runtime `python`, plan **`free`**, region `virginia` (not Brazil).
- Env: `PYTHON_VERSION=3.13.15` (repository locked Python version), **NO application secrets**.
- Build command: `python -m pip install --disable-pip-version-check --no-cache-dir -e .`
- Start command: `python app/hosting/render_staging.py`.
- The process uses the Render-injected `PORT` and binds `0.0.0.0`.
- Validate successful build and running deploy, `/healthz` 200 & `branches_defined=9`, `/readyz` 503, denied `POST /process`; gather live logs, not assumed observations.
- A Render Free service may sleep after inactivity, has constrained resources and does not provide an always-on background worker. **No continual generation or live production support is expected**.

## Governance and acceptance

1. No deployment before the source PR passes `System Integrity` and `Render Free Staging Safety`.
2. No chargeable resource. If Render rejects `plan=free`, STOP; do not fallback to Starter.
3. No Neon owner credentials, DSNs or API keys in GitHub or publicly exposed probe; staging is intentionally not Neon-backed at this point.
4. Verify actual Render deploy status/logs and record exact service ID, URL and commit. Do not assert a product that does not exist.
5. Future actual recipient-facing production development requires versioned Auth/RBAC/tenant, safe controlled bytes upload + private quarantine, typed API, durable Neon schema/queue, source-grounded 3×3 output and live event projections. Do this under new tasks/DRG rather than relaxing gates.
6. This is a **bounded infrastructure smoke for an operator-authorized Free tier**, not a production hosting vendor lock, failure recovery qualification, cost benchmark or completed W007 deployment.

**References:** `SYSTEM/DECISION_RESEARCH_GATE.md`, `SYSTEM/PRODUCTION_CONTRACT.md`, `docs/production/NEON_FREE_STAGING_2026-10-15.md`.
