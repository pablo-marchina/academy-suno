# Academy Suno — isolated Neon staging resource / free-only Railway boundary

**Recorded:** 2026-10-15  
**Operator authorization:** create **one new project exclusively for Academy Suno** on Supabase *or* Neon, and use **only the Railway Free plan**; do not enroll in or deploy via a paid Railway plan.  
**Evidence status:** direct authorized provider-tool observations, not a production deployment qualification or a stack DRG LOCK.

## Actually created and checked

| Field | Observation |
|---|---|
| Provider | Neon |
| Plan of owning organization at time of inspection | **free** |
| Project name | `academy-suno` |
| Project ID | `cold-math-95888995` |
| Branch name and ID | `main` / `br-shiny-fog-b6uqjlig` |
| Database | `academy_suno` |
| Region | `aws-sa-east-1` (São Paulo) |
| PostgreSQL | 17; live SQL observed `17.11 (59c914d)` |
| Compute bounds | 0.25–0.25 CU per created project's metadata |
| History retention | 21600 seconds (6 hours) per project metadata |
| Branch readiness | `ready` from provider |
| Connection smoke | Direct read-only SQL `select current_database(), current_setting('server_version'), 1` succeeded; `connection_ok=1` and database `academy_suno` |
| Data imported or application schema migrated by this action | **none** |
| Product deployed / authenticated tenant test / production failover | **NOT_RUN** |

A first Neon create attempt with a custom `suspend_timeout_seconds=300` was rejected by the Free account (`HTTP 412: modifying the suspend interval is not permitted on this account`). A retry without the unsupported option succeeded. The resulting metadata reports `suspend_timeout_seconds=0`, provider-default account behaviour; this must not be interpreted as auto-suspend, unlimited free compute, zero resource consumption or verified RTO.

No database password, connection string, JWT, API secret or privileged token is stored in GitHub. If deployed later, secrets must live in provider-managed encrypted service variables and least-privilege roles, not Git commits/logs. Neon SQL read was executed via a connector that hides database credentials.

**Provider console**: https://console.neon.tech/app/projects/cold-math-95888995

## Railway — explicit free-tier policy and observed block

- The connected account already has two *unrelated* Railway projects, neither was touched.
- An attempt to create a new **private**, **isolated** `academy-suno` staging project on the personal workspace **failed** with: `Your trial has expired. Please select a plan to continue using Railway.`
- No Academy Suno Railway project, deployment, domain, volume or database was created.
- **No paid plan** was selected or purchased; Railway provisioning remains **BLOCKED_BY_PLAN_SELECTION**.
- Railway documentation describes a Free plan after an expired trial and limited free monthly credits, but the available connector exposes **no plan-selection action**; eligibility and availability to this specific account need confirmation in the Railway console, and any cost outside free allowance is **not authorized**.

**User action if they want Railway app hosting:** visit https://railway.com/dashboard (or https://railway.com/account), select a **Free** option for the existing account/workspace if offered; do **not** choose Hobby or Pro. Then rerun the `academy-suno` private project creation and confirm $0-plan eligibility and resource limits before deploying anything. If Railway Free cannot be enabled on this account, pause Railway; assess a free alternative only through a new scoped operator directive.

## DRG decision posture

This was an **environment capability and ownership action**, not an evidence-backed decision that Neon is the production database. Neon is a usable **isolated staging candidate** for the upcoming same-workload bakeoff. Continue W009-T002 research with:
1. accepted local reference baseline;
2. Railway app/worker + Railway PostgreSQL **if Free available**;
3. Railway app/worker + **this** isolated Neon PostgreSQL **if Free available**, with secure least-privilege connectivity;
4. Railway app/worker + new authorized Supabase PostgreSQL as a counterfactual, *without creating a second DB by default*;
5. Supabase-only Edge architecture as a deliberately constrained Python-runtime counterfactual.

Before any production architecture is locked or claimed ready, measure exact 3 audiences × 3 formats/9 outputs, deterministic hard gates, source trust, authorized tenant isolation, storage quarantine, transactional state/event/outbox and CAS, backpressure/restart, security, migration/rollback, backups/recovery, load, raw latency and observed cost; follow `SYSTEM/DECISION_RESEARCH_GATE.md`. Human gold remains unavailable by operator choice and AI-only evidence must remain explicitly marked.

## Follow-ups

- Enforce free-only spend policy; no payment method change, subscription upgrade or paid entitlement requested.
- W009-T002 may use the live Neon project for **scoped, non-destructive** staging SQL/DB capability testing, after preserving credentials and data boundaries. Feature schema changes require versioned migration/DRG and negative tests; do not apply undocumented production migrations.
- Ask for Railway Free activation only if the operator wants a hosted app; if unavailable, keep Railway blocked instead of falling back to a paid plan.
- No unrelated Supabase/Neon/Railway projects modified. No production readiness claim or W007 blocker reclassification.
