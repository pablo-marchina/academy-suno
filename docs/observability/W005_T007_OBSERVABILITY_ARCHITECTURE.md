# W005-T007 — Observability, telemetry & safe live evidence architecture

`TASK_ATTEMPT_ID: W005-T007-A01`  
`STATUS: RESEARCH_INPUT_TO_SYNTHESIS`  
`CLAIM_BOUNDARY: NOT_PRODUCTION_READY`  
`DATE: 2026-09-22`

## 1. Purpose

Define an implementation-ready observability contract for the real Academy Suno product and its Live Evidence Cockpit without selecting a production vendor prematurely.

This artifact covers:

- correlation across tenant/request/run/job/branch/provider/eval/repair;
- target spans, structured events, logs and metrics;
- live backend→frontend event semantics;
- safe visibility/redaction boundaries;
- sampling/cardinality/retention posture;
- dashboard/alert inputs;
- quantitative acceptance checks.

It is an input to W005-T010 synthesis. It does not claim production readiness and does not make a canonical technology lock.

## 2. Non-negotiable architectural separation

### 2.1 Durable product events are authoritative for the Cockpit

The Live Evidence Cockpit MUST NOT use a sampled tracing backend as the sole source of truth for run status, the 3×3 matrix, eval/repair state, provenance or audit history.

Reason:

- traces may be sampled intentionally;
- collectors/exporters/backends can be delayed or temporarily unavailable;
- observability pipelines optimize inspection, not business-state durability;
- RISK-0035 explicitly forbids synthetic/stale evidence disconnected from the current run.

Therefore:

```text
real workflow transaction
  ├─ durable run state
  ├─ durable ordered domain/event record (authoritative live evidence)
  └─ correlated telemetry emission (derived observability)
```

The browser consumes authorized snapshots + ordered domain events. Trace/log/metric views are correlated projections attached to the same IDs, not replacements for the run/event record.

### 2.2 OpenTelemetry is the instrumentation/export boundary candidate

Application/service instrumentation should emit vendor-neutral OpenTelemetry traces, metrics and structured logs through OTLP, preferably via an OpenTelemetry Collector boundary before backend export.

This is a candidate for W005-T010 lock, not a worker-level canonical lock. Backend choice remains open.

### 2.3 Content telemetry is opt-in, not the default

Raw source documents, prompts, model inputs, model outputs, repaired content, credentials and arbitrary user text are excluded from default telemetry.

OpenTelemetry's GenAI conventions explicitly warn that model input/output message attributes are likely to contain sensitive/PII data. The default Academy posture is therefore metadata-first.

`CAPTURE_LLM_CONTENT_DEFAULT: false`

## 3. Target topology

```text
Browser Cockpit
  │
  ├── GET authorized snapshot / typed resources
  └── SSE authorized ordered events (per W005-T002 candidate/decision)
          ▲
          │ cursor + replay + snapshot fallback
          │
Live projection/API layer
          ▲
          │
Durable run/event store  <── workflow transaction/outbox
          ▲                         │
          │                         ├── source/anchor
          │                         ├── 9 generation branches
          │                         ├── eval
          │                         ├── repair/re-eval
          │                         └── aggregate/join
          │
          └──────────────── correlation IDs ───────────────┐
                                                           │
App/worker OTel SDKs ──OTLP──> OTel Collector ──OTLP───────┼─> backend candidate(s)
                                     │                     │    - Grafana/Tempo/Loki/Mimir
                                     ├─ redaction/filter   │    - Phoenix
                                     ├─ batch/retry        │    - Langfuse
                                     ├─ sampling           │
                                     └─ exporter health    ┘
```

The event store and telemetry backend may use the same underlying data platform only if later research proves that doing so preserves durability, replay, tenant isolation and operational independence. The logical contracts stay separate.

## 4. Correlation model

### 4.1 Technical distributed-trace IDs

Use W3C Trace Context / OpenTelemetry:

- `trace_id` — end-to-end technical trace identity;
- `span_id` — current operation;
- `parent_span_id` where applicable;
- span links for queued, resumed or fan-in work when a strict synchronous parent/child hierarchy is misleading.

`traceparent`/`tracestate` are for trace correlation only. Do not place PII, tenant names, document text, secrets or business payload in `tracestate`.

### 4.2 Domain correlation IDs

Every relevant persisted event, structured log and trace span SHOULD carry the applicable opaque IDs:

| Field | Meaning | Cardinality | Metric label default? |
|---|---|---:|---|
| `tenant_id` | authorization/isolation boundary | high | **NO** |
| `workspace_id` | workspace scope | high | **NO** |
| `document_id` | controlled source object | high | **NO** |
| `request_id` | API/request identity | very high | **NO** |
| `run_id` | workflow run identity | very high | **NO** |
| `job_id` | durable work item | very high | **NO** |
| `attempt_id` | retry/resume attempt | high | **NO** |
| `branch_id` | stable 3×3 branch identity | bounded within run | only decomposed bounded dimensions |
| `provider_call_id` | provider invocation | very high | **NO** |
| `eval_id` | evaluation instance | very high | **NO** |
| `repair_id` | repair instance | very high | **NO** |
| `experiment_id` | controlled experiment | high | **NO** |
| `trace_id` | technical trace | very high | **NO** |
| `span_id` | technical span | very high | **NO** |

High-cardinality IDs belong in events, traces and structured logs, not metric dimensions.

### 4.3 Baggage rule

Do not use OpenTelemetry Baggage as the default carrier for tenant/user/document identifiers. OTel automatically propagates baggage on many network requests and warns that it can leak to unintended third parties and has no built-in integrity checks.

Carry authorization/business context through the application's typed request/message envelope. Use trace context for technical correlation. If a future implementation uses baggage inside a trusted boundary, it must have an explicit allowlist, propagation boundary and security test.

## 5. Span model: source → 9 → eval → repair → aggregate

Recommended span skeleton:

```text
academy.run
├─ academy.source.ingest
│  ├─ academy.source.parse
│  └─ academy.source.anchor
├─ academy.fanout
│  ├─ academy.branch.generate [audience=BEGINNER, format=...]
│  │  ├─ gen_ai.* provider span
│  │  ├─ academy.eval
│  │  ├─ academy.repair (0..N bounded)
│  │  └─ academy.eval.recheck
│  ├─ ... branch 2
│  └─ ... branch 9
├─ academy.aggregate
└─ academy.run.finalize
```

For asynchronous queues/resume:

- producer span records enqueue/persist action;
- consumer/job execution starts a new span with the same trace where safe and supported, or a new trace with a span link to the originating context;
- durable `run_id`/`job_id` remain the primary domain correlation even when trace continuity is intentionally restarted at trust boundaries.

### 5.1 Required low-cardinality span attributes

Candidate attributes:

- `academy.stage`: `source|generate|eval|repair|aggregate|api|live_delivery`;
- `academy.audience`: one of the 3 canonical audiences;
- `academy.format`: one of the 3 canonical formats;
- `academy.status`: bounded workflow/eval state;
- `academy.eval.type`: bounded evaluator class;
- `academy.repair.reason`: bounded reason code, not free text;
- `gen_ai.operation.name`, provider/model/token attributes when emitted safely under the selected semantic-convention version;
- `error.type` for errors following OTel conventions.

### 5.2 High-cardinality span attributes

Opaque IDs from §4.2 may exist on spans for lookup/correlation if backend privacy/tenant controls permit. They must not silently become metric labels via span-to-metric generation.

When exporting to an external SaaS, pseudonymize tenant/workspace/document identifiers with keyed HMAC where direct identity is not required for operations. Keep the mapping only in the trusted application boundary.

## 6. Live domain-event contract

The event envelope is transport-neutral but designed to satisfy the SSE default selected/recommended by W005-T002 research.

```json
{
  "schema_version": "1.0",
  "event_id": 8129,
  "event_type": "eval.completed",
  "occurred_at": "RFC3339 timestamp",
  "tenant_id": "opaque",
  "workspace_id": "opaque",
  "document_id": "opaque",
  "request_id": "opaque",
  "run_id": "opaque",
  "job_id": "opaque-or-null",
  "attempt_id": "opaque-or-null",
  "branch_id": "opaque-or-null",
  "trace_id": "32-hex-or-null",
  "span_id": "16-hex-or-null",
  "run_revision": 37,
  "stage": "eval",
  "status": "passed",
  "payload": {},
  "visibility": "tenant_private_metadata"
}
```

### 6.1 Event invariants

1. `event_id` is monotonically ordered in the replay scope.
2. `run_revision` allows the client to detect stale/out-of-order projections.
3. Event payload is already authorization-filtered and redacted before serialization.
4. The frontend never receives a privileged superset for client-side hiding.
5. Reconnect resumes from cursor/`Last-Event-ID` where retained.
6. If the cursor is no longer replayable, server returns/forces an authorized fresh snapshot plus a new cursor.
7. The client de-duplicates by `(run_id,event_id)` and rejects regressive revisions except explicit replay handling.
8. Every event exposed as “live evidence” is bound to the same current `run_id` shown in the cockpit.
9. Raw filesystem paths, provider credentials, auth tokens and unrestricted source/model text are forbidden in live event payloads.
10. Live correctness must survive telemetry backend outage because the durable event contract is independent.

### 6.2 Required event families

Minimum candidate families:

- `run.created|started|completed|failed|cancelled`;
- `source.accepted|parsed|anchored|rejected`;
- `branch.queued|started|generated|completed|failed`;
- `provider.started|completed|failed|retried` metadata only;
- `eval.started|completed|failed|review_required`;
- `repair.started|completed|failed`;
- `aggregate.started|completed|failed`;
- `experiment.started|candidate_measured|completed`;
- `reliability.retry|queue_wait|resume|recovered`;
- `telemetry.degraded|restored`;
- `security.authorization_denied` as a safe, non-sensitive user-facing state only where appropriate.

## 7. Safe visibility / redaction policy

### 7.1 Data classes

| Class | Examples | Default telemetry | Cockpit visibility |
|---|---|---|---|
| `PUBLIC_OPERATIONAL` | stage, bounded status, duration, provider/model identifier if non-secret | allowed | allowed |
| `TENANT_OPAQUE_ID` | tenant/workspace/run/job/document IDs | trace/log allowed under controls; metrics no | only authorized tenant/workspace |
| `TENANT_CONTENT` | source text, prompts, model output, repaired copy, citations with surrounding text | **excluded by default** | bounded authorized product view, not generic telemetry dump |
| `PERSONAL_OR_SENSITIVE` | names/emails if present, private financial docs, free-text notes | **excluded by default** | only product feature that requires it, bounded/redacted |
| `SECRET` | API keys, auth tokens, cookies, passwords, signing keys | **never telemetry** | never |
| `INTERNAL_SECURITY` | raw policy internals, stack details that increase attack surface | minimized | admin-only if justified |

### 7.2 Defense in depth

Redaction occurs in this order:

1. **source instrumentation** — do not emit prohibited content;
2. **typed telemetry schema allowlist** — only declared attributes can be produced;
3. **collector filter/redaction** — second line of defense before export;
4. **backend access/tenant controls** — restrict who can query telemetry;
5. **cockpit projection** — server-side authorization and purpose-specific projection;
6. **audit** — sensitive-debug mode and privileged trace access are auditable.

Collector redaction is not the only control; current OTel redaction processor stability differs by signal, so source-level minimization remains mandatory.

### 7.3 Sensitive troubleshooting mode

A future `sensitive_debug_capture` capability is allowed only if all conditions are explicit:

- default OFF;
- tenant/run-scoped, never global by accident;
- authorized privileged actor;
- reason recorded;
- short, explicitly declared retention from owner/security requirements (number not invented here);
- field allowlist + redaction/truncation;
- no credentials/secrets under any mode;
- export destination explicitly approved;
- start/stop events audited;
- UI marks captured sensitive content visibly.

## 8. Metrics model

Metrics stay low-cardinality and workload-relevant.

### 8.1 Candidate metric families

| Metric | Type | Candidate bounded attributes |
|---|---|---|
| `academy.run.duration` | histogram | outcome |
| `academy.branch.duration` | histogram | audience, format, outcome |
| `academy.provider.duration` | histogram | provider, model, operation, outcome |
| `academy.provider.tokens` | counter/histogram | provider, model, direction |
| `academy.provider.cost` | counter | provider, model, pricing_version/currency when trustworthy |
| `academy.eval.duration` | histogram | eval_type, outcome |
| `academy.eval.outcome` | counter | eval_type, outcome, audience, format |
| `academy.repair.count` | counter | reason_code, audience, format, outcome |
| `academy.queue.wait` | histogram | queue_class, stage |
| `academy.queue.depth` | gauge | queue_class |
| `academy.retry.count` | counter | stage, reason_code |
| `academy.live.delivery_lag` | histogram | event_type_class, outcome |
| `academy.live.reconnect` | counter | reason_class |
| `academy.live.replay_events` | counter | outcome |
| `academy.telemetry.export_failures` | counter | signal, exporter_class |
| `academy.telemetry.dropped` | counter | signal, reason_class |
| `academy.telemetry.redacted_fields` | counter | signal, field_class |
| `academy.authz.denied` | counter | action_class, reason_class |
| `academy.workflow.branch_completion` | gauge/counter | audience, format, status |

Do not use `tenant_id`, `workspace_id`, `run_id`, `job_id`, `request_id`, `trace_id`, `span_id`, `document_id`, prompt hashes or source URLs as metric labels by default.

### 8.2 Quantiles

PROD-012 requires p50/p95/p99. Record distributions/histograms and compute quantiles in the telemetry backend. Do not emit hard-coded percentile gauges from every process unless a later backend-specific reason justifies it.

No latency threshold is declared by this task.

## 9. Sampling policy

### 9.1 Never sample away product correctness evidence

- durable domain events: not sampled;
- required audit/provenance records: not sampled;
- security/authz decisions required for evidence: not sampled according to the eventual audit policy;
- metrics: aggregate continuously subject to cardinality controls.

### 9.2 Traces

Candidate policy:

- baseline probabilistic/head sampling for healthy high-volume traces only after representative load evidence;
- retain 100% of traces in controlled acceptance/regression runs;
- tail-sampling candidate for errors, high latency, retries, `FAIL`, `REVIEW_REQUIRED`, repairs and rare failure/recovery paths;
- because OTel tail-sampling processor is stateful and currently beta for traces, production use requires T008 deployment/load evidence and collector topology validation.

No sampling percentage is invented here.

### 9.3 Logs

- structured, schema-controlled logs;
- errors/security/audit categories retained per policy;
- debug verbosity disabled or sampled in production according to measured need;
- raw payload logging prohibited by default.

## 10. Retention classes

This task deliberately does not invent retention days.

| Class | Content | Retention posture |
|---|---|---|
| `AUDIT_PROVENANCE` | required append-only product/audit evidence | owner/legal/security value must be declared and tested |
| `OPERATIONAL_TELEMETRY` | spans/metrics/logs | establish from troubleshooting window, cost and incident needs |
| `SENSITIVE_DEBUG` | exceptional bounded content capture | default off; shortest justified declared retention |
| `PRODUCT_CONTENT` | documents/generated outputs | governed by product/data policy, not observability retention |

Deletion/retention behavior must be tested once owner/legal/product constraints are known.

## 11. Telemetry completeness contract

A production system can sample traces while still proving instrumentation completeness in a controlled acceptance suite.

### 11.1 Acceptance-suite completeness

For a deterministic representative run with telemetry sampling disabled:

- expected required stage spans observed = `100%`;
- each of 9 branch identities represented = `9/9`;
- every required persisted event has `run_id` and applicable correlation IDs = `100%`;
- missing required provenance binding = `0`;
- live replay gap/duplicate in defined reconnect tests = `0`;
- prohibited secret test fixtures exported = `0`;
- cross-tenant live/trace query access successes in negative tests = `0`.

This is a test-evidence gate, not a blanket production promise that every production trace is retained.

### 11.2 Runtime health signals

Monitor:

- collector/exporter queue/backpressure;
- export failures/retries;
- dropped telemetry;
- metric overflow marker where supported;
- sampled vs retained traces;
- live event delivery lag/reconnect/replay;
- projector cursor lag;
- redaction/filter counts;
- trace-event correlation success on sampled traces.

## 12. Alertability

### 12.1 Hard-condition alerts

The following are non-compensatory conditions; alert on any observed occurrence in the defined scope:

- successful unauthorized cross-tenant data access;
- missing required provenance on an accepted run/job artifact;
- critical schema violation promoted as PASS;
- durable live event replay gap that cannot be repaired by snapshot/replay logic;
- secret/credential fixture escaping into telemetry in security tests.

### 12.2 Threshold-based operational alerts

Do not invent alert thresholds here. T008/load/reliability evidence should establish baselines for:

- latency distributions;
- queue depth/wait;
- exporter failure/drop rates;
- reconnect/replay volume;
- provider error/retry rate;
- storage growth;
- collector CPU/memory;
- metric cardinality overflow.

## 13. Backend candidate interface

The application should depend on:

- OpenTelemetry APIs/SDK abstractions;
- OTLP export contract;
- typed domain event contract;
- backend-neutral dashboard/query projection boundary.

It should not depend in core workflow code on a vendor-specific trace object.

Current credible backend classes:

1. **Grafana OTLP stack** — general metrics/logs/traces + dashboards/alerts; self-managed or cloud variants.
2. **Arize Phoenix** — AI/LLM tracing/evals/experiments with OTLP/OpenInference; self-host path.
3. **Langfuse** — LLM observability/evals with OTLP trace ingestion and cloud/self-host options.

`BACKEND_DECISION: NO_OVERALL_PREFERENCE_PENDING_WORKLOAD_AND_OPERATIONS_EVIDENCE`

A hybrid is also plausible: a general OTel backend for infrastructure signals plus an AI-specific UI consuming selected traces. Any duplication must be measured for operational/cost/privacy value before adoption.

## 14. Microbenchmark evidence

Artifacts:

- `experiments/w005_t007_observability_benchmark.py`
- `experiments/results/W005-T007-A01-observability-benchmark.json`

Observed in the local deterministic probe:

- metadata-only compact JSON mean: `364.0447 B/event`;
- same envelope plus synthetic 4 KiB raw content: `4473.0447 B/event`;
- payload multiplier from that synthetic content: `12.2871×`;
- metadata SSE application frame mean: `405.4894 B`, `11.3845%` above compact JSON in this envelope;
- five replay cursor checks over 20,000 deterministic events: gap-free with zero duplicates under the durable-log model;
- illustrative high-cardinality product: `100 tenants × 10 runs × 9 branches × 3 providers × 4 eval types = 108,000` combinations, `54×` the OTel default SDK cardinality limit of 2,000 per metric stream;
- bounded example dimensions `5 stages × 5 statuses × 3 audiences × 3 formats × 3 providers = 675` combinations.

Interpretation limits:

- serialization throughput is synthetic local Python CPU evidence only;
- no network/backend latency or capacity claim;
- SSE result excludes protocol/network stack overhead and compression;
- replay correctness assumes a durable ordered store;
- cardinality scenario is illustrative, not observed Academy production load.

## 15. Phase 9 acceptance tests to implement

1. `test_trace_schema_complete_clean_run`: sampling disabled, required stage spans/correlation 100%.
2. `test_trace_3x3_branch_identity`: exactly all 9 branch identities observable.
3. `test_event_reconnect_replay`: disconnect/reconnect at several cursors; no gap/duplicates.
4. `test_snapshot_fallback_expired_cursor`: old cursor produces authorized fresh snapshot, no stale silent continuation.
5. `test_cross_tenant_live_denied`: tenant A cannot subscribe/query tenant B run.
6. `test_cross_tenant_trace_denied`: cockpit trace projection is server-authorized.
7. `test_secret_canary_redaction`: seeded fake API key/token never exits collector/application telemetry boundary.
8. `test_content_capture_default_off`: prompt/source/output fixtures absent from traces/logs when default configuration is used.
9. `test_metric_label_allowlist`: prohibited high-cardinality ID labels absent.
10. `test_metric_overflow_observable`: controlled cardinality stress surfaces overflow/guard signal rather than silently corrupting dashboards.
11. `test_collector_outage_product_path`: workflow + durable live state continue safely while telemetry backend/collector export is unavailable, with degraded-observability state exposed.
12. `test_provider_eval_repair_trace_links`: provider→eval→repair→re-eval correlation preserved.
13. `test_tail_sampling_failure_paths`: if selected, errors/FAIL/REVIEW/repair traces retained under representative topology.
14. `test_sensitive_debug_audit`: privileged capture requires explicit scope and leaves audit evidence.

## 16. Coordination boundaries

- **W005-T002** owns frontend/API/live transport; its current DR selects SSE by default. This artifact adopts the cursor/replay contract but keeps the event schema transport-neutral.
- **W005-T004** owns identity/tenant/data architecture; T007 requires server-side authz and safe telemetry but does not choose auth/RLS/storage technology.
- **W005-T006** owns AI runtime/provider routing; T007 provides provider/model/eval observability fields without selecting provider/model.
- **W005-T008** owns deployment/reliability/capacity; it must validate collector topology, overhead, failure behavior and actual retention/SLO/capacity values.
- **W005-T009** owns cross-cutting benchmark methodology; future backend bakeoffs should use its accepted method.
- **W005-T010** owns final production architecture synthesis and may lock OTel/backend choices only after the fan-in.

## 17. Decision status

- OpenTelemetry + W3C Trace Context + OTLP/Collector boundary: `CANDIDATE_FOR_T010_LOCK`, confidence **HIGH**.
- durable product event log separate from sampled observability: `CANDIDATE_FOR_T010_LOCK`, confidence **HIGH**.
- metadata-first / GenAI content capture default off: `CANDIDATE_FOR_T010_LOCK`, confidence **HIGH**.
- OTel/OpenInference AI semantic adapter: `CANDIDATE`, confidence **MEDIUM**; exact convention needs version pinning and compatibility test.
- telemetry backend: `NO_OVERALL_PREFERENCE`, confidence **HIGH** in the pending state.
- trace sampling percentages, retention days, alert/SLO thresholds: `PENDING_EVIDENCE`, deliberately unset.

## 18. Reversal conditions

Reopen the OTel boundary recommendation if representative implementation shows a materially superior alternative that preserves all of: traces+metrics+logs, cross-service context, exportability, current ecosystem support, backend portability, safe filtering and comparable operational evidence.

Reopen the separate durable-event-store recommendation only if the selected observability substrate provides transactional product-state/event durability, replay, tenant isolation and failure independence without sampling/loss semantics; this must be proven, not assumed.

Reopen metadata-first capture only if partner/security requirements explicitly require content telemetry and a narrower design cannot satisfy the use case; secret/credential exclusion is not reversible.
