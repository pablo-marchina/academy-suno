# DR-9001 — Academy Suno Free-tier hosting and PostgreSQL topology research

**Task:** W009-T002-A01 · Issue #258 · research on 2026-10-15  
**Original provenance:** STATE 0065 / 8c903c4fd6022eabb22da1ea0bea9901689f737b  
**Observed starting state:** STATE 0075 / c150d10e1c72eb0652ffd1c55af5695fd8d104b0  
**DRG state:** **PENDING_EVIDENCE / NO_PREFERENCE**  
**Production runtime, database and host LOCK:** **NONE**  
**Confidence:** HIGH for repository/provider documented constraints; MEDIUM for transferability of public plan documentation to account entitlements; LOW for comparative runtime, security, recovery, latency and cost without a matched deployed workload.  
**Decision authority:** this is a Worker research proposal, not a canonical D-002x or a production technology selection.

## 1. Decision question and existing observations

Which zero-subscription hosting/database combinations can *plausibly* host the Academy Suno Python 3.13.15/uv single-product path, including persistent multi-tenant run/job/event state and nine audience × output-format branches, without hidden paid resources, unsupported long-lived workers or invented recovery guarantees? What representative qualification evidence would be needed to select one?

**Actually observed by the Orchestrator (historical provider evidence, not reproduced here):**
- Neon Free project dedicated to Academy Suno, ID **cold-math-95888995**, PostgreSQL 17, region **aws-sa-east-1 (São Paulo)**, database **academy_suno**, branch **main / br-shiny-fog-b6uqjlig**. A read-only SQL connection smoke passed. No application schema, migrated runs, multi-tenant access or recovery was tested. [Record](../../production/NEON_FREE_STAGING_2026-10-15.md).
- Render Free web service **srv-db8gc2ivcj2c73aacg80**, Virginia, deploy **dep-db8gc32vcj2c73aachhg** reported live from source **f42c75e71bee726612208c4e333bf55c5dee0c80**, URL https://academy-suno.onrender.com. It runs only a public, **read-only** 3×3 contract-definition diagnostic; **not** the nine output generator. It does not connect to Neon. External HTTP status probe was NOT observed in the historical record. [Record](../../production/RENDER_FREE_STAGING_RUNBOOK.md) and [Issue #258](https://github.com/pablo-marchina/academy-suno/issues/258).
- Railway private project creation was **rejected**: "Your trial has expired. Please select a plan to continue using Railway." No Railway Academy Suno service was created. Account-specific Free provisioning is **BLOCKED_BY_FREE_PLAN**, even though vendor documentation describes a $0 plan.
- No new cloud resources, migrations, secrets reads, external deployment tests, provider invocations, network benchmarks or restoration were performed by **this** research Worker.

The original W007 GCP/AWS study remains historical and its blocked successors are **unchanged**. D-0021/D-0022 require exclusive free staging, D-0023 defers *new authentication/security implementation* without waiving any hard gate, and D-0024 separates Worker and Orchestrator authority. AI-only evaluation is not human gold.

## 2. Workload and non-negotiable controls

The representative unit is **one immutable original source group → canonical extraction and source/provenance → 3 audiences (beginner/intermediate/advanced) × 3 native formats (article/carousel/short_video) → evaluation/repair/review → lossless nine-branch join**. Freeze exactly one implementation, dataset/source hashes, evaluated gates, provider-effect emulator/configuration, authoritative database event model and runtime versions before topology comparison.

- Python **3.13.15**, uv **0.12.18**, existing pyproject.toml/uv.lock; no edge-runtime rewrite disguised as an implementation-neutral alternative.
- Durable committed state + transition + outbox + CAS/fencing + job ownership, externally stored private source/document versions; survive cold start, crash, retry, redeploy and duplicate delivery across process boundaries.
- Server-authoritative tenant/workspace ownership and row/object/event/trace isolation; no caller-controlled local PDF path or public upload; no client-visible privileged secret; reviewed architecture constraints only, *no new auth implementation* in this attempt.
- Hard gates: factual/source/policy/schema/provenance/tenant non-compensation **0**, accepted nine identities **9/9**, join loss/duplication **0**, stale overwrite **0**, unauthorized cross-tenant success **0**, uncommitted event projection **0**, secret/quarantine leakage **0**, restart/resume and defined backup/restore scenario **100% PASS**. Any failed or untested gate forbids a production winner.
- Observe raw job latency, queue wait, throughput, cold starts, CPU/RAM, connections/locks, recovery/rollback, object storage, trace handling, metered usage, costs and operational steps. No fabricated SLO, RTO/RPO, supported user count or quality gain.

## 3. Predeclared alternatives, not a vendor ranking

| ID / class | Feasibility on stated Free-only boundary | Python/background/durability risks | Eligible status |
|---|---|---|---|
| **B0 local W006 reference** (reference control) | Available in repository; no cloud spend | SQLite/reference process is not a durable multi-replica production authority; no deployed isolate/restore/HA | **DIAGNOSTIC_ONLY**, not production contender |
| **C1 Render Free Web + existing Neon Free PG** (managed sleeping web container + external serverless PG) | **Existing isolated resources observed**, no actual app/database linkage | Render free sleeps after 15m idle, ephemeral disk, **single instance**, no Free background worker/one-off jobs; Python web requests possible but queued work must be resumed by a permitted external execution path. Render Virginia ↔ Neon São Paulo is a geography confounder, not a measured latency penalty. Neon transaction pool cannot carry session ownership across transactions. | **CANDIDATE, PENDING_EVIDENCE**; current diagnostic is **not** product |
| **C2 Koyeb Free Web + existing Neon PG** (alternative sleeping web container) | Public Free instance documented; **no account entitlement/deploy checked**, no additional service authorized | One Free instance per organization, **0.1 vCPU/512 MB/2 GB**, one-hour idle scale-to-zero; Free instance **cannot run Worker Service** or persistent volumes. Foreground long jobs/CPU-intensive PDF processing unqualified. | **HYPOTHETICAL FREE CANDIDATE**, untested |
| **C3 Vercel Hobby Python Functions + Neon PG** (per-invocation serverless function) | Free Hobby exists, but **non-commercial personal use only**; intended partner use may not qualify; no entitlement/deploy checked | Python runtime Beta; finite HTTP function execution; background durable Python worker, app package compatibility, long-run resume and external DB pooling unproven. Distinct scheduling model; do not use on commercial deployment under Hobby. | **RESTRICTED COUNTERFACTUAL**, not assumed eligible |
| **C4 Supabase Free PG/Auth/private Storage + Edge Functions** (managed BaaS/TypeScript-Deno edge) | Free limits are published, but **no dedicated Supabase project authorized/created in addition to Neon**; do not reuse unrelated project | Edge Functions are **TypeScript/Deno, not Python 3.13.15**; 150s wall clock/2s CPU per request on Free (published limits), so replacing the Python graph violates same-workload equivalence. DB/Auth/Storage/RLS are architecture components but not a drop-in worker. Free tier lacks managed PITR and automatic backups. | **CONSTRAINT COUNTERFACTUAL / NOT_EQUIVALENT** |
| **C5 Railway Free App + Railway PG OR Supabase PG/Storage OR existing Neon PG** (container + database variations) | Vendor lists Free $0/mo and $1 monthly credit; **actual connected account project creation rejected**. Trial credit is *not* a recurring production budget. | Worker/container, session pooling, private storage and recovery require separate measured qualification. Supabase DB would be a **new** project, not an implied authorization. | **BLOCKED_BY_FREE_PLAN**, NO paid fallback |
| **C6 Render Free Web + Render Free Postgres** (same-host alternative) | Public plan, but do **not** provision another DB | Free Postgres expires after **30 days**, no managed backups or connection pooling; unacceptable as assumed durable recovery substrate. Render still lacks free worker. | **RULED_OUT for durable production eligibility** on documented feature gap |

**Important:** The presence of several research candidates does not mean they are all concurrently deployable, compatible, or economically legal. Free and $0 advertised rates refer to bounded allowances, *not* verified $0 per completed nine-output run, zero egress charges, or production support. C2/C3/C4/C5/C6 were researched, **not provisioned**.

## 4. Architecture requirements and failure surface matrix

| Capability | Required architecture/test; current status |
|---|---|
| Durable orchestration | Transactional claim with monotonically increasing owner epoch, revision-based CAS, persisted queued/leased/completed jobs, retry with idempotency and independently recorded physical provider attempts; no in-process scheduler as authority. **NOT_RUN on Neon**. |
| PostgreSQL connection pooling | Neon PgBouncer *transaction* pooling forbids persistent session settings, LISTEN/NOTIFY, session advisory locks and SQL PREPARE. Use explicit tenant+resource predicates, transaction-local context only inside an explicit transaction, and a **direct** connection for migrations/pg_dump where needed. Verify driver prepared-statement compatibility; never count a recycled pooled connection as an ownership fence. **NOT_RUN**. |
| Tenant and identity | Separate server principal authorization, least-privilege database roles; WHERE tenant_id/workspace_id plus tested RLS/grants if database is exposed; negative cross-tenant read/write/list/replay attempts. Supabase service role bypasses RLS; privileged access stays server-only. No security implementation in this task. |
| Objects | Explicit private quarantine→validated→accepted lifecycle, opaque keys, content hash, type/size policies and retention, separate object authorization and signed access tests. Existing Render probe accepts **no uploads**. Existing Neon DB alone does not prove safe object handling. |
| Restart and queue | Free web service can sleep/restart. A persistent queue requires a *permitted bounded processing trigger* or durable external worker; merely storing queued jobs in Postgres is **not** evidence of completion/liveness. Long running request/cron and worker feasibility must be tested within actual plan policy. |
| Restore | Neon Free publishes **up to 6 hours or 1 GB changes** of history and one snapshot; project metadata shows **21600s** history. A backup/PITR capability description is not an executed **isolated restore**. Neon branch-root instant restore overwrites data, so never restore the only branch or run destructive P5 against current Neon main. Supabase Free offers no built-in automatic backups/PITR. |
| Migration/rollback | Versioned expand/contract on a disposable authorized branch/DB, clean migration + mixed-version + application rollback; no writes to existing academy_suno main in this attempt. Validate pooled vs direct connection semantics and rollback after in-flight work. |
| Telemetry | OTLP trace/span/run/job/tenant correlation, privacy-redacted logs, missing/drop counts; telemetry not authoritative product state. Render diagnostic logs do not prove per-job traces or production visibility. |
| Region/cost | Report actual endpoint regions (Render Virginia, Neon São Paulo); source geography/configure matched targets for future comparisons. Freeze vendor quote on each test date, egress, monthly instance allowance, storage usage, free-spend enforcement, retry/cold-start compute and deployment limits before trial. |

## 5. Systematic source survey (2026-10-15)

Search classes: official plan/quota/billing/current hosting limitations; Python and worker runtime; PG pooling + backups; row/object isolation; existing Academy Suno source records; only then secondary incident/benchmark data if materially relevant. Queries included "Render free web spin down background worker", "Neon Free CU hours history pooling", "Railway Free trial expired", "Supabase Free Edge Functions Deno RLS backup", "Koyeb free worker limits", "Vercel hobby Python non-commercial". Reviewed **primary** vendor documentation and canonical project evidence; did not turn community anecdotes into measured workload evidence.

| Source (primary unless noted) | Observed claim / relevance | Limitation |
|---|---|---|
| [Render Free](https://render.com/docs/free) (live docs, accessed 2026-10-15) | Sleep 15m, ephemeral disk, one instance, no one-off jobs, **750 free instance hrs per workspace/month**, 30-day free Postgres expiry, no Free PG backups/pooling; usage/bandwidth caution | Published limits, not this project's actual month usage |
| [Render Outbound Bandwidth](https://render.com/docs/outbound-bandwidth) | Public egress and external DB communication can consume included bandwidth; excess may bill if payment method exists | Exact workspace free usage/payment state unobserved |
| [Neon Pricing](https://neon.com/pricing) (accessed 2026-10-15) | **100 CU-hrs / month/project, 1 GB PG / project**, up to 6h or 1GB changes history, Free snapshot allowance; serverless PG | Per-project metadata may have a narrower compute cap; no actual month usage captured |
| [Neon Pooling](https://neon.com/docs/connect/connection-pooling) | PgBouncer transaction mode and session-feature exclusions; direct connection for migrations/dump | Driver/config/workflow behaviour needs testing |
| [Neon Instant Restore](https://neon.com/docs/postgres/backup-restore/branch-restore) | Root restore overwrites and interrupts selected branch; history bounded | Not a completed restore on Academy Suno |
| [Railway Plans](https://docs.railway.com/pricing/plans) and [Trial](https://docs.railway.com/pricing/free-trial) | Free advertises $0 with $1/mo credit; trial expiry/transition described | Account explicitly rejected create_project; cannot infer entitlement |
| [Supabase Billing](https://supabase.com/docs/guides/platform/billing-on-supabase) and [Pricing](https://supabase.com/pricing) | Free ~500 MB DB, 1 GB Storage, 5 GB egress, 500k Edge invocations; Free backup/PITR absent | No dedicated Suno Supabase deployment |
| [Supabase Edge Runtime](https://supabase.com/docs/guides/functions) and [Limits](https://supabase.com/docs/guides/functions/limits) | Deno/TypeScript; Free wall-time/memory/CPU constraints | Not Python runtime; no equivalence claim |
| [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security) | Row policies combined with grants; privileged service role bypasses RLS | Vendor guidance ≠ tenant isolation test |
| [Koyeb Free Instances](https://www.koyeb.com/docs/reference/instances) and [Scale-to-Zero](https://www.koyeb.com/docs/run-and-scale/scale-to-zero) | Free 0.1 vCPU, 512MB; no Worker Service; idle down after 1h | No account eligibility or Python compatibility run |
| [Vercel Hobby](https://vercel.com/docs/plans/hobby), [Python](https://vercel.com/docs/functions/runtimes/python) and [Limits](https://vercel.com/docs/functions/limitations) | Free personal/noncommercial usage, Beta Python functions and duration bounds | Potentially disallowed for partner commercial use; no long-lived worker |
| [W007 accepted DRG](./DR-7001-production-topology-qualification.md) + [qualification protocol](../../production/W007_T001_TOPOLOGY_QUALIFICATION_PROTOCOL.md) | Non-compensatory hard gates and fixed same-workload phases P0–P9 | Research reference, not deployed W009 observation |
| [Neon creation evidence](../../production/NEON_FREE_STAGING_2026-10-15.md) + [Render staging record](../../production/RENDER_FREE_STAGING_RUNBOOK.md) | Provider-linked, isolated bounded smoke and exact IDs | Historical observation; no independent network reconfirmation |

**Source coverage and saturation:** This is sufficient to identify **critical free-tier execution and recovery incompatibilities** and to preregister a same-workload qualification plan. Source research is **not saturated for a production LOCK**: current account billing/eligibility, Free worker viability, real database adapter compatibility, external document storage, geographic end-to-end tests, recoverability and complete metered costs are missing. Reopen immediately if provider changes its terms, eligibility or architecture features.

## 6. Raw evidence and missingness ledger

| Claim/evidence field | Observed provenance | Result / missingness |
|---|---|---|
| Neon PG Free created/ready and isolated read-only SELECT | Prior Orchestrator provider record, 2026-10-15; SQL output in Neon staging document | **HISTORICAL_OBSERVED**; not a run or workload latency sample |
| Render Free staging reported live and startup logged | Prior Orchestrator provider record, 2026-10-15; service/deploy IDs above | **PROVIDER_REPORTED**; public HTTP status **NOT_OBSERVED** |
| Railway project create attempt | Prior Orchestrator provider error | **REJECTED**; C5 **BLOCKED_BY_FREE_PLAN** |
| Matching deployed 9× native generated outputs on any provider | No raw run identities/outputs or dataset result supplied | **NOT_RUN** (not 0%/100%) |
| Two running process/replica ownership and CAS/outbox | Not provisioned; Render Free single instance | **NOT_RUN / FREE_LIMITATION** |
| RLS/tenant/private object abuse negative tests | No public product service; docs only | **NOT_RUN** |
| Restart/replay/sleep/restore/PITR/migration rollback | No destructive authority approved | **NOT_RUN** |
| p50/p95/p99/throughput/DB contention/cold start | No representative run observations | **NULL; sample_count=0; missing_reason=NOT_RUN** |
| Real metered $/nine-output run and spend cap | No monthly usage records, no provider invoice | **NULL / NOT_OBSERVED** |
| Human reader evaluation; model-judge external comparisons | D-0019 AI-only; no evaluation here | **NOT_RUN; HUMAN_GOLD_UNAVAILABLE_BY_CHOICE** |

**Do not impute** costs, precision, uptime, or recovery time from Free plan quotas or successful status probes. Advertised $0 subscription is **not** an observed benchmark cost, and missing production tests **are not passes**.

## 7. Decision and reversal conditions

**DECISION: PENDING_EVIDENCE / NO_PREFERENCE.** C1 is the only currently *authorized and pre-existing* cross-provider web/database staging pair, but it lacks product wiring and an eligible continuous Free worker/backup validation. It is a practical **next research target, not the default**. C2 is another container-class Free hypothesis, C3 a serverless noncommercial-limited hypothesis, C4 a non-Python counterfactual, C5 account-blocked, C6 durability-limited. None qualifies for a production topology lock.

Reopen if a specifically eligible $0 tier supports durable Python workers and appropriate private storage, the operator authorizes a safe disposable restore target, region/plan/allowance changes, representative 3×3 tests pass all hard gates, and measured paired metrics permit a non-dominated set or stable Pareto choice. Production readiness stays **FALSE / NOT_AUTHORIZED**; Orchestrator only may integrate this research and update canonical decisions.

**Traceability:** PROD-001..017 (especially -001..004, -006, -009, -012..016); DR-7001, W005-BENCHMARK-METHODOLOGY-V002, EP-05; D-0019..D-0024; W007 immutable blockers; risks: conditional free availability, per-tenant exposure, worker sleep, recovery window, cross-region egress, unmetered provider costs. See companion [same-workload plan](../../production/railway_supabase_qualification_plan.md).
