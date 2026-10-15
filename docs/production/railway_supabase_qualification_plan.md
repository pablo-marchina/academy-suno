# W009-T002 — Same-workload Free-tier infrastructure qualification plan

**Worker attempt:** W009-T002-A01 · [Issue #258](https://github.com/pablo-marchina/academy-suno/issues/258)  
**Date/preregistration:** 2026-10-15  
**Decision input:** [DR-9001](../decisions/research/DR-9001-railway-supabase-topology.md)  
**Status:** **SPECIFICATION_ONLY / NOT_RUN**; eligible provider-funded execution not approved.  
**Current safe resource boundary:** the existing Neon Free **cold-math-95888995**, DB **academy_suno**, São Paulo, is NOT migrated or restored; the existing Render Free **srv-db8gc2ivcj2c73aacg80**, Virginia, remains **read-only diagnostic** without Neon credentials. No changes to unrelated cloud projects, no paid resources, no new authentication implementation.

This is a **replicable trial recipe**, not a claim that deployment or benchmarks were performed. It deliberately separates zero-cost offline preflight, permissible read-only environment evidence, and **future experiments gated by separate authorization**. The earlier canonical W007 P0–P9 protocol remains the rigorous production target; no blocked predecessor is silently reclassified.

## A. Frozen comparison contract

### A1. Identity required for every attempted run

Record a signed/hashed manifest **before** candidate outputs are inspected:

| Field | Value to freeze before a trial |
|---|---|
| Task lineage | task_id W009-T002, attempt_id A01 for this study, *new attempt/task* for future live execution |
| Repository | exact source SHA + dirty state = false, immutable container digest (if applicable), dependency lock SHA256, Python **3.13.15**, **uv 0.12.18** |
| Dataset | original PDF bytes SHA256, source group ID, source license/data policy, extraction/parser version, required paragraph/table provenance, DEV/CALIBRATION/HELD_OUT group assignment from W008-T003 |
| Variant set | exact nine Cartesian product: beginner, intermediate, advanced × article, carousel, short_video; stable run_id, job_id, branch_id with canonical output schema |
| Provider effects | same recorded deterministic simulator/fixture for substrate-only trial; separately freeze real model/provider config for future end-to-end product run; never compare a live model with a stub and call it the same workload |
| Acceptance | gate config/version, committed transition/outbox schema, CAS/owner epochs, idempotency key policy, logical vs physical attempt records, raw audit snapshot |
| Networking | API region, worker region, DB region, object region, DNS path, private/public connection class, TLS mode, pool mode and minimum resources |
| Service envelope | allowed concurrency, instances, plan, quota remaining, stated spend ceiling **$0 subscription and $0 overage**, operator-approved time window, safely bounded maximum attempts |
| Timing | UTC start/end and instrumentation clock sync approach, provider request IDs, elapsed raw units, service warm/cold status |
| Reversibility | throwaway environment resource IDs, backup/restore target, before/after tenant-independent integrity hash, kill switch, owner approval reference |

For the existing staging pair record **Render region=virginia** and **Neon region=aws-sa-east-1**. Never silently compare its latency with a same-region architecture and label the difference as vendor compute superiority. If a matching region is unavailable on an authorized free tier, **stratify as confounded**, do not adjust away the unknown.

### A2. Candidate and admission registry

| Candidate | Pre-trial gate | Eligibility |
|---|---|---|
| B0 local reference | Existing W006 semantics, no real hosting; run same frozen data locally as diagnostic | Reference only; cannot achieve production eligibility |
| C1 Render Free + Neon Free | Current plan ownership verified; separate scoped approval for adding private DB configuration, queue, controlled worker and synthetic fixture data; **do not expose recipient demo server** | Candidate **only** if Free Python trigger and restart/resume can be proven |
| C2 Koyeb Free + Neon Free | Confirm exact account/region/Free grant; separate approval required for new app; Free Worker Service is unavailable | Candidate counterfactual; no continuous worker assumption |
| C3 Vercel Hobby Python + Neon Free | Confirm project is entirely **personal, non-commercial**; get permission before new project; max function duration and Python compatibility tested | Not eligible for a commercial partner product via Hobby |
| C4 Supabase Free + Edge | Dedicated legal project approval; TypeScript-Deno edge **cannot** execute current Python graph without a separate research-gated rewrite | Constraint comparator only, **not same-workload result** |
| C5 Railway Free + its PG / Neon / Supabase PG | Account must actually permit $0 Free project creation. Current create error blocks all variations | **BLOCKED_BY_FREE_PLAN**; do not select paid plan |
| C6 Render Free + its Free PG | 30-day expiry/no backups disallows required durable restore | Negative feasibility control, not deployed |

A pair is not admitted to an apples-to-apples performance chart when its worker scheduling model cannot produce the same authoritative outputs, unless explicitly labeled **NON_EQUIVALENT_COUNTERFACTUAL**.

### A3. Workload fixture

One case consists of **one independent source-group original**, permission-safe with immutable SHA256, nine variants, identical factual/financial numeric anchors and table evidence where available, deterministic provider-effect stub for substrate comparison, plus a canonical run/job/event transition log. Do not feed unrelated private/customer documents into Free plans. Preserve three slices: text PDF, table-rich PDF, scanned/image-only PDF, with **MISSING_SOURCE_OR_RIGHTS** rather than fabricated content when not acquired. Reuse W008-T003's preregistered group partition, never substitute synthetic generated text for source-original benchmark evidence.

Nine branch keys must be exactly:

| Audience | Article | Carousel | Short video |
|---|---|---|---|
| beginner | beginner:article | beginner:carousel | beginner:short_video |
| intermediate | intermediate:article | intermediate:carousel | intermediate:short_video |
| advanced | advanced:article | advanced:carousel | advanced:short_video |

For N input source groups, attempt **N complete runs per predeclared candidate/repetition**, storing every aborted/failed attempt separately. Independent source groups—not nine correlated branches—are the statistical unit for comparisons. No counts, denominators, source hashes, timing samples or outcomes have been observed by this attempt.

## B. Evidence capture format (machine-readable contract for future execution)

Persist UTF-8 JSONL (or parquet with equivalent fields), immutable per test window. Null requires **missing_reason**; never coerce NOT_RUN to zero. This schema is a **specification**, not a file of fake runs:

| Record type | Mandatory fields |
|---|---|
| **manifest.json** | schema_version, preregistration_commit, candidate_id, architecture_class, eligibility_class, read_only/authorized flags, subscription_cost_policy, image_digest, source_sha, lock_sha256, fixture_manifest_sha256, config_revision, runtime_version, plan/region/size, provider_docs_snapshot URLs+retrieval time |
| **attempt.jsonl** | trial_id, run_id, source_group, branch_key, job_id, tenant_id *opaque*, attempt_no, physical_attempt_id, candidate_id, trace_id, start/end_utc, latency_ms, cpu_ms, db_wait_ms, cold_start, error_code, outcome, missing_reason |
| **transition.jsonl** | tenant/workspace/run/job IDs, transition_id, mutation_id, expected_revision, result_revision, owner_epoch, committed_at, outbox_id, event_id, event_revision, duplicate_delivery, accepted_output_hash, provenance_hash |
| **negative_tests.jsonl** | candidate_id, gate_id, test_case_id, expected_deny, actual_result, secret_canary_leaked, cross_tenant_success, null_if_not_run, evidence_ref |
| **recovery.jsonl** | interruption_id, scenario, before/after immutable manifest hashes, failure_start_utc, recovery_utc, recovery_elapsed_ms, lost/duplicate branches, restore_target, timeline/LSN, observed_data_loss, missing_reason |
| **usage.jsonl** | candidate_id, provider, plan, resource ID, usage period, instance-hours, CU-hours, storage_GB-month, network_egress_GB, build minutes, request count, price snapshot, currency, actual charge (nullable), quota remaining, source invoice/export ref |
| **readout.json** | stage and hard-gate verdict per candidate, exact numerator/denominator, sample_counts, p50/p95/p99 if observed, source-group paired interval method, missingness vector, Pareto set, decision state, uncertainty, all raw refs |

Do **not** commit connection strings, provider tokens, whole financial source text from restricted documents, email addresses, user IDs, insecure raw traces or private object links. Use stable opaque identifiers and hashes, with separately controlled secure evidence storage if a future authorized test involves secrets.

## C. Step-by-step execution phases

**P-1: Offline/read-only preflight — permitted now**

1. Freeze docs/source contract, validate JSON schemas and nine valid branch keys **without cloud calls**; check deterministic synthetic regression and source-group split membership on the existing test suite.
2. Inspect existing historical Render/Neon provider records in versioned docs and GitHub Issue. Optionally refresh metadata/SELECT **read-only only** from the two already-authorized resources when tooling/access permits; state exact observation time and command. No schema writes or credentials retrieval.
3. Check free plan/quotas, alert/spend behaviour and workload legality with official provider docs. **STOP if unknown account payment/billing setting could incur overage.** Existing Render service must remain only the read-only HTTP probe.
4. Produce a missingness matrix and feasibility verdict. **This research attempt stops here**; all P0–P9 rows below remain NOT_RUN.

**P0: Consent/build/deployment identity — future gated action**

Prerequisites: separate Orchestrator-approved task, explicit authorization for the exact new/modified Free resource, zero-overage safeguard, disposable test isolation, loss limits, and no new public upload surface. Build **one** image or equivalent reproducible Python application version; pin source/lock/migration SHA/digest, region, worker/API resources. Check clean deploy and startup, provider-reported state *and* real network probes. Use no unrelated projects.

**P1: Shared state, worker liveness, cold start and ownership**

Require **two independently restarted processes or equivalent concurrency**, not necessarily two paid replicas. In a disposable authorized DB, create same-tenant and cross-tenant run/job IDs with stable branch set. Exercise CAS race, stale owner fencing, duplicate delivery, retry after physical provider effect but before commit, kill-before-commit, kill-after-commit/outbox-before-publish, fresh-process resume, queue starvation during web sleep, and crash recovery. Distinguish **accepted output** vs **physical attempt**. If an architecture can only run while an HTTP request is open and has no supported durable trigger, declare **HARD_GATE_UNSUPPORTED**; never claim a background worker exists.

**P2: All 9 outputs, source/factual/tenant/object negative tests**

For each original source group run exact 9 branch identities to terminal and verify lossless join, idempotency and provenance. Include unknown/missing source, wrong tenant, forged principal, revocation/org-switch, replay cursor scope, inaccessible private document object, quarantine bypass, oversize/invalid upload and storage-denial scenarios **only on a private test service after security implementation is separately authorized**. This task does *not* implement auth/security. Any omitted critical security gate means product **NOT_ELIGIBLE**.

**P3: Load, queue and bounded backpressure**

Start trial at concurrency **1**, then **2, 4, 8, ...** and stop at first **observed** saturation, provider quota/guardrail, or preregistered **$0** cost/budget ceiling. Record all raw samples, queue depth, CPU/RAM, DB locks/waits, pool saturation and completed 3×3 runs. Repeat balanced source-group windows; order candidates rotationally to reduce time-of-day drift. Censor, do not extrapolate a tier never executed. Any attempt that risks paid egress/overage is stopped before admission.

**P4: Controlled failure, sleeping and restart**

Inject web sleep, process kill/redeploy, delayed duplicate delivery, DB connection loss, object denial and OTLP exporter loss separately in the disposable workload. Record time between outage and each restored invariant, stale writer rejection and resulting authoritative state. Do not claim failover/HA or a numerical RTO from a healthy startup probe.

**P5: Restore/backup/PITR**

Requires **a second authorized isolated recovery target**, disposable data, explicit destruction consent and provider-supported copy/snapshot. Hash known committed events, add later mutations, restore *only the isolated target*, attach a fresh application and verify tenant binding, 9/9, event replay and hashes. Neon instant restore overwrites the chosen root branch; **never point restore at the only live academy_suno branch**. Note Free Neon history **up to 6h or 1 GB of changes** and per-project settings, and Free Supabase backup/PITR absence. If the authorized Free plan cannot demonstrate isolated restore with required objective, mark **NOT_ELIGIBLE**, not PASS or ZERO_LOSS.

**P6: Schema migration and rollback**

On a disposable database run migration N → additive N+1, mixed-version read/write, backfill/reconcile, app rollback to N (schema remains forward compatible), and resume queued runs; measure locks/migration and rollback durations. Destructive migration rollback requires the already verified restore route.

**P7: Observability and data-leak probes**

Structured redacted logs, W3C trace IDs and OTLP spans across API→worker→DB→eval/repair; verify export receipt, drop ratio, queryability, cardinality and provider cost. Inject synthetic credential/source markers and assert no leak; collector failure must never alter committed state. Existing Render startup log is **not** proof of product traces.

**P8: Operational burden and full lifecycle**

Fresh deploy after clean environment initialization; readiness, rollout, app rollback, fresh restart, quota exhaustion and recovery. Capture real operator commands, billable steps, wall-clock times, intervention count, alerting and upgrade pressure (an operational cost). Free sleeping services are not equivalent to always-on multi-replica services.

**P9: Multiobjective cost and verdict**

For every **eligible** candidate, report pricing snapshot and actual metered usage by compute, DB, network, build, storage/object, backups, secrets, observability, extra geographic transfer and model calls; calculate cost per successful 3×3 run **only** when numerator/denominator observed. Do not round missing to $0. Use hard gates → raw metrics → uncertainty/missingness → point Pareto. If multiple eligible nondominated remain, **NO_PREFERENCE**; missing representative evidence means **PENDING_EVIDENCE**.

## D. Pass/fail, preregistered targets, and stopping

### D1. Non-compensatory hard gates

| Gate | Required result | Missing or failing result |
|---|---|---|
| Critical source/factual/policy/schema/provenance override | **0** | INVALID/REVIEW, never optimized away |
| Unauthorized cross-tenant access and private-object/quarantine bypass | **0** | INELIGIBLE / NOT_TESTED |
| Exact branch coverage / accepted join | **9/9**, zero loss/duplicate | INELIGIBLE / NOT_TESTED |
| Same-run stale owner or duplicate accepted output | **0** | INELIGIBLE |
| Uncommitted event treated as authoritative | **0** | INELIGIBLE |
| Credential/raw document canary leak | **0** | INELIGIBLE / NOT_TESTED |
| Defined restart/resume and restore scenarios | **100% PASS in tested scenarios** | NOT_ELIGIBLE_FOR_PRODUCTION if absent |
| Billing overrun or paid resource requirement without authorization | **0** | HARD STOP; no compensating technical result |
| Respect for fixed Python 3.13.15 graph | **YES** for like-for-like trials | NON_EQUIVALENT_COUNTERFACTUAL otherwise |

No unattested threshold for p95 latency, dollars/run, throughput, reader audience comprehension, SLO or RPO is specified; those are empirical **discovery metrics**. Predetermined benchmarks for user utility would require relevant domain evidence, not guesswork.

### D2. Statistical/uncertainty plan

Treat **source group** as the independent cluster and 9 format/audience branches as correlated observations. Store per-group paired vectors, sample counts and missingness. When enough independent groups have completed paired windows, present median plus p50/p95/p99 raw distributions and cluster bootstrap intervals or a justified paired procedure; report CI method, repetitions, censoring, cold-vs-warm slices, CPU/region mix, retry side effects. Do not pretend n=9 independent samples from one source. When n is inadequate for inference, report **DESCRIPTIVE_ONLY**.

### D3. Stopping rules

Research-only stopping: source survey stopped when official docs settled material free-tier/Python/worker/recovery constraints and additional categories would not remove observed missingness without deployment. **Does not mean production evidence saturation**.

Future execution: stop a candidate immediately on safety/security/billing violation; permit hard-gate-failed candidate to skip costly later phases **after preserving raw evidence**. For a candidate without a permitted equivalent worker or recovery, stop with explicit **UNSUPPORTED_ON_FREE**. Stop load at measured saturation or **$0**-plan quota risk, not at a fabricated target. Never terminate other eligible candidates merely because one looks faster; finish equivalent predeclared windows before a decision.

## E. Permission boundaries and staged next actions

**Safe deliverable from W009-T002 now:** these two versioned research documents and the Worker RESULT with GitHub lifecycle/CI evidence. The worker must not perform P0–P9 live product tests, alter Render service config or Neon schemas, add a second DB, touch unrelated resources, use hidden creds, expose uploads, implement login, or purchase subscriptions.

**For an eventual separate authorized qualification:**
1. Orchestrator records explicit choice of **disposable Free-only target**, consent for DB mutations/backup restore, region, provider quota and $0-overage/stop guarantees; if impossible, remain research-only.
2. An independent engineering task builds private typed API, least-privilege identities, safe quarantine and transactional PG job/outbox adapters; keep D-0023 deferral until explicitly reopened; *do not* expose the legacy recipient demo server.
3. A separate workload task runs identical frozen source originals and 3×3 graph on all materially equivalent, eligible environments and records immutable raw P0–P9 evidence, CI and recovery proof.
4. Orchestrator audits paired hard gates, raw metrics, missingness, provider conditions and point Pareto before modifying any production decision. W007 blocked original attempts remain separate.

**Current verdict:** **PENDING_EVIDENCE / NO_PREFERENCE / PRODUCTION_READY=FALSE**. An available Neon SQL smoke plus Render public diagnostic is valuable staging infrastructure, not a working durable Academy Suno product.

## F. Reproducible inspection commands (read-only; not execution evidence)

The future operator may confirm **repository-local** invariants without any cloud access:

- **Source version:** git rev-parse HEAD; git status --porcelain; sha256sum uv.lock
- **Runtime/dependency version:** python --version; uv --version; uv sync --frozen --group test (local installation only)
- **Local regression:** uv run --frozen python -m pytest -q tests (after dependencies are installed; scope/test selection must be recorded)
- **Canonical gate:** python scripts/validate_system.py --base-ref MAIN_SHA (requires correct GitHub base ref)
- **Staging behavior expectations in local tests:** no POST public uploads; definitions yield three audiences × three formats; readyz intentionally 503. Record actual assertions before classifying any PASS.

Do not copy any command's hypothetical output into evidence. Real HTTP curl, SQL SELECT, provider cost usage export or deployment credentials were **not invoked** for this Worker.

## G. Reference authority

- [Canonical W007 qualification protocol](W007_T001_TOPOLOGY_QUALIFICATION_PROTOCOL.md) and [accepted topology DRG](../decisions/research/DR-7001-production-topology-qualification.md).
- [W006 durable state/event reference](W006_T003_DURABLE_STATE_EVENT_SUBSTRATE.md); [W005 target architecture](W005_TARGET_PRODUCTION_ARCHITECTURE.md); [Production Contract](../../SYSTEM/PRODUCTION_CONTRACT.md).
- [Neon Free staging observation](NEON_FREE_STAGING_2026-10-15.md); [Render read-only staging](RENDER_FREE_STAGING_RUNBOOK.md); [W008-T003 corpus/metric registry](../product/research/W008_T003_CORPUS_AND_METRIC_REGISTRY.md).
- [Render Free limits](https://render.com/docs/free); [Neon plan](https://neon.com/pricing) and [transaction pool](https://neon.com/docs/connect/connection-pooling); [Railway plans](https://docs.railway.com/pricing/plans); [Supabase Edge limits](https://supabase.com/docs/guides/functions/limits); [Koyeb Free instance](https://www.koyeb.com/docs/reference/instances); [Vercel Hobby](https://vercel.com/docs/plans/hobby). Prices/limits accessed **2026-10-15** and must be refreshed at actual execution.
