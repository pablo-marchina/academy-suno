# DR-0701 — Observability, telemetry & safe live evidence

`DR_ID: DR-0701`  
`TASK_ATTEMPT_ID: W005-T007-A01`  
`DATE: 2026-09-22`  
`DECISION_RESEARCH_GATE: SATISFIED_FOR_RESEARCH_OUTPUT`  
`PRODUCTION_LOCK_SCOPE: NONE_BY_WORKER`  
`CLAIM_BOUNDARY: RESEARCH_INPUT_TO_W005_T010`

## 1. Decision question

What observability architecture should instrument the real Academy Suno product and safely power inspectable traces/metrics/logs while preserving a live Evidence Cockpit correlated to the actual run, without leaking tenant content/secrets or locking the product to a telemetry vendor prematurely?

Subquestions:

1. What vendor-neutral instrumentation/context/export standard should the runtime use?
2. Should live cockpit correctness depend directly on the observability backend?
3. How should tenant/request/run/job/provider/eval/repair correlation work?
4. What telemetry content may be captured by default?
5. Which LLM/eval observability backends are credible candidates?
6. How should sampling, metric cardinality and retention be constrained before production evidence exists?

## 2. Workload / constraints

Hard/local constraints:

- PROD-011: real Live Evidence Cockpit with run graph/events, 3×3, sources, eval/repair, experiments, traces, cost/latency/tokens/retries, health and audit/provenance;
- PROD-012: correlated traces/metrics/structured logs by request/run/job/tenant, provider/eval spans, p50/p95/p99, error/retry/queue/cost, exportable telemetry;
- PROD-014: no improper document/prompt/secret/credential leakage in logging/telemetry;
- PROD-001 cross-tenant unauthorized access hard gate remains zero;
- RISK-0035: frontend must not visualize synthetic/stale evidence;
- RISK-0037: observability must not leak sensitive content;
- no arbitrary retention/SLO/capacity/latency numbers without representative evidence;
- final framework/provider/storage/deploy/backend locks belong to W005-T010 fan-in, not this worker.

Cross-task constraints:

- W005-T002 owns frontend/API/live transport and its current research selects SSE as the default one-way run feed with cursor/replay semantics;
- W005-T004 owns identity/tenant/storage/security architecture;
- W005-T006 owns provider/model/runtime routing;
- W005-T008 owns deployment/reliability/capacity evidence;
- W005-T009 owns cross-cutting benchmark methodology.

## 3. Alternatives

### A0 — Existing/ad-hoc application logs + static evidence views

Shape:

- continue repository-specific logs/telemetry and static cockpit artifacts;
- add local fields as needed;
- no standardized trace context/export substrate.

Benefits:

- minimum new infrastructure;
- simple for local case mechanics.

Material limitations:

- weak cross-service correlation as product becomes multi-process/multi-replica;
- no standard traces+metrics+logs export boundary;
- poor backend portability;
- does not satisfy the full PROD-011/012 live/inspectable target by itself.

Use as counterfactual baseline only.

### A1 — OpenTelemetry SDKs + W3C Trace Context + OTLP Collector + general observability backend

Representative backend family: Grafana with Tempo/Loki/Mimir, cloud or self-managed.

Shape:

- instrument app/workers with OTel APIs/SDKs;
- W3C Trace Context across service boundaries;
- OTLP to a Collector;
- processors for batching/filtering/redaction/sampling as validated;
- general metrics/logs/traces backend and dashboards/alerts.

Benefits:

- standardized traces, metrics, logs and context propagation;
- backend-neutral application boundary;
- general SRE observability depth;
- Collector provides an operational choke point for export/filter/retry.

Risks/trade-offs:

- AI-specific trace/eval UX may need custom dashboards or a second specialist backend;
- self-managed general stack has operational burden;
- Collector components have mixed stability and must be evaluated individually.

### A2 — OpenTelemetry/OpenInference + Arize Phoenix

Shape:

- OTel transport/instrumentation with OpenInference AI semantics where useful;
- Phoenix accepts OTLP traces and provides AI tracing/evals/datasets/experiments;
- available self-hosted as well as managed paths.

Benefits:

- AI/LLM-oriented trace/eval workflow;
- OTLP/OpenInference compatibility;
- self-host option with application data kept in the chosen infrastructure according to current Phoenix documentation.

Risks/trade-offs:

- does not replace a complete production metrics/logs/SRE stack by evidence shown here;
- OpenInference adds an additional convention layer to govern/version;
- production tenancy/access/scaling/retention still require workload-specific validation.

### A3 — OpenTelemetry + Langfuse

Shape:

- Langfuse accepts OTLP/HTTP trace ingestion;
- LLM-specific generations/evals/trace analysis in Langfuse;
- managed and self-host paths exist in product documentation.

Benefits:

- native LLM-observability product model;
- OTLP trace compatibility reduces application instrumentation lock-in;
- current documentation explicitly supports direct OTLP ingestion.

Risks/trade-offs:

- OTLP trace ingestion is not, by itself, a general metrics/logs backend;
- Langfuse-specific observation metadata may be needed for richest UX;
- exact data-location, retention, auth, scaling and operational footprint require later environment-specific evidence.

### A4 — LangSmith-centered observability

Shape:

- ecosystem-specific tracing/evals around LangChain/LangGraph deployments;
- cloud/hybrid/self-host deployment variants.

Benefits:

- strong integrated agent/eval workflow if LangChain/LangGraph becomes a production runtime choice.

Risks/trade-offs:

- current official data-plane documentation couples tracing behavior materially to LangSmith deployment mode;
- choosing it before workflow/runtime decisions could create unnecessary coupling;
- less evidence in this task for a backend-neutral traces+metrics+logs substrate than A1.

Retained as a counterfactual, not eliminated globally.

## 4. Evaluation criteria

No synthetic weighted score is used. Security/evidence correctness are hard, non-compensatory requirements.

| Criterion | Why material |
|---|---|
| cross-service correlation | request/run/job/provider/eval must join reliably |
| traces + metrics + logs | PROD-012 asks for all three signal classes |
| AI/eval semantics | generation/eval/repair must be inspectable |
| backend portability | avoid vendor lock before W005 fan-in |
| live-evidence correctness | sampled telemetry cannot fabricate Cockpit state |
| privacy/redaction | RISK-0037 / PROD-014 |
| tenant isolation | cross-tenant leakage is critical hard gate |
| cardinality control | per-run IDs can explode metric series |
| sampling control | production volume/cost without losing critical evidence |
| self-host / data control | relevant while partner data constraints are unknown |
| operational burden | collector/backend topology must be supportable |
| export/query interoperability | final evidence should remain inspectable/exportable |
| maturity/stability | unstable collector/convention features require explicit risk |
| cost | must be measured on representative usage, not guessed |

## 5. Systematic source search

Research buckets:

1. W3C distributed trace context standard;
2. OpenTelemetry signal/context/metrics/semantic-convention documentation;
3. Collector architecture/security and processor stability;
4. current GenAI semantic-convention privacy characteristics;
5. browser live-event contract coordination from W005-T002;
6. official OTLP/self-host documentation for Grafana, Phoenix and Langfuse;
7. credible ecosystem-specific counterfactual (LangSmith);
8. reproducible task-local microbenchmark for event payload/replay/cardinality mechanics.

Search date: `2026-09-22`.

Primary/official sources were preferred. Secondary opinion/community evidence was not needed to discriminate the architectural contract at this stage.

### Stopping rule

Stop when:

- every hard criterion has primary/official evidence or is explicitly pending workload evidence;
- at least three materially different backend/architecture alternatives are covered;
- the search yields no new instrumentation architecture class or security constraint in two successive passes;
- measurable payload/replay/cardinality mechanics have a reproducible local probe;
- remaining differentiators are environment-specific deployment/load/cost/retention questions owned by later W005 fan-in tasks.

Saturation was reached: later searches added product details but did not alter the central separation of durable live events from sampled telemetry, the OTel/OTLP portability candidate, or the metadata-first privacy posture.

## 6. Source table

All web sources accessed 2026-09-22 unless otherwise noted.

| ID | Source | Type | Evidence used | Limitation |
|---|---|---|---|---|
| S01 | `SYSTEM/PRODUCTION_CONTRACT.md` | primary/local | PROD-011/012/014 and no invented targets | project contract, not external validation |
| S02 | `SYSTEM/ASSUMPTION_RISK_REGISTER.md` | primary/local | RISK-0035/0037, A-0016 | project risk register |
| S03 | `SYSTEM/DECISION_RESEARCH_GATE.md` | primary/local | research/promotion method | process rule |
| S04 | https://www.w3.org/TR/trace-context/ | standard | traceparent/tracestate interoperability; no PII in trace context | HTTP-oriented trace context standard |
| S05 | https://opentelemetry.io/docs/concepts/context-propagation/ | primary/project docs | sanitize/ignore untrusted context; do not propagate sensitive baggage | general guidance, implementation varies |
| S06 | https://opentelemetry.io/docs/concepts/signals/baggage/ | primary/project docs | baggage auto-propagation/leak and no integrity checks | does not prohibit all IDs; Academy adopts stricter default |
| S07 | https://opentelemetry.io/docs/concepts/signals/metrics/ | primary/project docs | cardinality behavior, default 2000, overflow point | SDK/backend configurations can differ |
| S08 | https://opentelemetry.io/docs/specs/otel/metrics/sdk/ | specification | default cardinality limit SHOULD be 2000 absent overrides | implementation-specific support still tested later |
| S09 | https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ | specification | GenAI input/output messages likely sensitive/PII; filter/truncate allowed | GenAI conventions evolve and must be version-pinned |
| S10 | https://opentelemetry.io/docs/specs/semconv/how-to-write-conventions/ | specification/guidance | sensitive/expensive/verbose attributes should be opt-in; head-sampling attrs low-cardinality | convention-author guidance applied conservatively |
| S11 | https://opentelemetry.io/docs/collector/ | primary/project docs | Collector recommended for retries/batching/encryption/sensitive filtering | deployment topology still workload-specific |
| S12 | https://opentelemetry.io/docs/collector/components/processor/ | primary/project docs | processor stability differs by signal; tail sampling beta traces; redaction beta traces/alpha metrics/logs | status can change; pin/recheck before implementation |
| S13 | https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md | primary/project repo | allowlist/masking; privacy use; redaction is one line of defense | component stability varies by signal |
| S14 | https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/tailsamplingprocessor/README.md | primary/project repo | stateful trace grouping; all spans same collector; policy types/scaling caveat | beta component; production topology must be tested |
| S15 | https://opentelemetry.io/docs/security/config-best-practices/ | primary/project docs | secure collector config and scrub sensitive data | generic guidance |
| S16 | https://grafana.com/docs/opentelemetry/ingest/ | primary/vendor | OTLP metrics/logs/traces into cloud or self-managed Mimir/Loki/Tempo | vendor docs; operational fit unmeasured here |
| S17 | https://grafana.com/docs/tempo/latest/ | primary/vendor | Tempo OTel/open protocol tracing and correlation with metrics/logs | trace-focused component only |
| S18 | https://arize.com/docs/phoenix/ | primary/vendor | Phoenix AI tracing/evals; accepts OTLP | product docs; workload fit unmeasured |
| S19 | https://arize.com/docs/phoenix/self-hosting | primary/vendor | self-host path, privacy/data control claims | vendor statement; deployment evidence still required |
| S20 | https://arize-ai.github.io/openinference/ | primary/project docs | OpenInference complements OTel and works with OTel-compatible backends | separate convention governance required |
| S21 | https://langfuse.com/integrations/native/opentelemetry | primary/vendor | Langfuse OTLP trace endpoint; OTel compatibility | traces focus; richest features may use Langfuse attrs |
| S22 | https://langfuse.com/docs/api-and-data-platform/features/public-api | primary/vendor | OTLP is current supported trace ingestion path; legacy ingestion deprecation | mutating product detail; recheck on implementation |
| S23 | https://docs.langchain.com/langsmith/data-plane | primary/vendor | LangSmith cloud/hybrid/self-host tracing/data-plane coupling | not a full LangSmith bakeoff |
| S24 | W005-T002 `DR-0001-evidence-cockpit-frontend-api-live-events.md` | peer primary/research | SSE default, durable cursor/replay, server-side redaction | pending orchestrator acceptance/integration |
| S25 | task-local benchmark | experiment | payload multiplier, SSE framing, replay model, cardinality scenario | synthetic; not network/backend capacity evidence |

## 7. Reproducible benchmark / raw evidence

Artifacts:

- `experiments/w005_t007_observability_benchmark.py`
- `experiments/results/W005-T007-A01-observability-benchmark.json`

Protocol:

- stdlib Python only;
- 20,000 deterministic events per variant;
- 5 serialization repetitions;
- metadata-only envelope versus same envelope plus synthetic 4 KiB content;
- exact application-level SSE `id/event/data` framing;
- deterministic cursor-replay checks;
- explicit illustrative cardinality combinatorics.

Raw observations:

| Probe | Result |
|---|---:|
| metadata compact JSON | 364.0447 B/event mean |
| + synthetic 4 KiB content | 4473.0447 B/event mean |
| content payload multiplier | 12.2871× |
| metadata SSE application frame | 405.4894 B/event mean |
| SSE application framing overhead vs compact JSON | 11.3845% |
| replay checks | 5/5 gap-free, 0 duplicates under durable-log model |
| naive cardinality scenario | 108,000 combinations |
| ratio to OTel default 2,000 cardinality limit | 54× |
| bounded example Cartesian upper bound | 675 combinations |

Uncertainty/limits:

- local CPU serialization is not production latency;
- no network, TLS, proxy, exporter or backend timing;
- synthetic repeated content does not model compression;
- durable replay correctness is assumed by the model and must be tested against selected persistence;
- cardinality counts illustrate design pressure, not expected production traffic.

## 8. Findings

### F1 — Standardize instrumentation before selecting a backend

W3C Trace Context + OpenTelemetry provide interoperable technical context and a single application-facing model for traces/metrics/logs. OTLP gives multiple backend options. This directly reduces avoidable vendor lock compared with vendor-specific instrumentation in core workflow code.

### F2 — The Collector is a useful control plane, not a privacy guarantee

Official OTel guidance recommends a Collector for batching/retries/encryption/sensitive filtering. However, processor maturity differs: current redaction support is beta for traces and alpha for metrics/logs; tail sampling is beta for traces and stateful. Therefore privacy must start at instrumentation/schema allowlists, with collector redaction as defense in depth.

### F3 — Live Evidence Cockpit correctness must not depend on sampled telemetry

Tracing intentionally permits sampling and exporter delay/failure. The current product requirement needs live current-run truth. A durable ordered run/domain-event record provides cursor/replay/audit semantics independently; telemetry is correlated to it. This is the strongest control for RISK-0035.

### F4 — Content capture creates disproportionate privacy/cost surface

OTel GenAI docs explicitly warn input/output message fields may contain PII. The local synthetic 4 KiB content field increased event payload 12.29×. Raw content also creates retention, vendor-export and access-control obligations. Metadata-first default is therefore both a security and operational control.

### F5 — High-cardinality business IDs belong outside metric labels

OTel SDKs have cardinality controls; the current documented default is 2,000 combinations per metric stream. The illustrative Academy-like Cartesian product reaches 108,000 before request/job/document IDs are even added. Run/tenant/request/job/trace IDs should remain trace/log/event lookup fields, not default metric dimensions.

### F6 — Baggage is too permissive for default tenant/user propagation

Official OTel docs warn baggage is automatically propagated across many network requests, can reach unintended third parties and lacks integrity checks. Academy should propagate authorization/business identifiers through typed application messages and use W3C trace context only for technical trace correlation.

### F7 — No single backend wins on current evidence

- Grafana-family stack has broad general SRE signal coverage and OTLP ingestion.
- Phoenix has strong AI/LLM tracing/evals/experiments and self-host evidence.
- Langfuse has LLM-specific observability and current OTLP trace ingestion.
- LangSmith is credible if its ecosystem/runtime becomes foundational, but that dependency is not yet selected.

No representative Academy production deployment/load/cost/operator benchmark exists yet. Declaring a winner would violate DRG.

### F8 — OpenInference is a useful adapter candidate, not a required canonical schema yet

OpenInference complements OTel for AI traces and is supported by Phoenix/OTel-compatible backends. OpenTelemetry itself also has evolving GenAI conventions. Until T010/implementation compatibility evidence exists, the durable Academy domain event schema should remain its own versioned product contract; AI trace conventions can be adapters over it.

### F9 — Retention and sampling numbers remain evidence-gated

No partner/legal troubleshooting window, target traffic, SLO, data residency or telemetry budget is known. Retention days, trace sampling percentages and operational alert thresholds remain `PENDING_EVIDENCE` rather than arbitrary values.

## 9. Decisions / recommendation state

Workers do not create canonical locks. These are recommendations to W005-T010.

### D1 — Instrumentation/export boundary

`OUTCOME: CANDIDATE_FOR_T010_LOCK`

Use OpenTelemetry SDK/API semantics, W3C Trace Context and OTLP with a Collector boundary as the default production instrumentation/export contract.

Confidence: **HIGH**.

Why evidence is sufficient for candidate status:

- standards-based technical correlation;
- all three required signal classes;
- multiple credible OTLP backends;
- collector control surface for filtering/retry/batching;
- no requirement to commit core workflow to a vendor trace model.

Reversal conditions:

- representative bakeoff proves an alternative materially improves reliability/security/operability while preserving traces+metrics+logs, context interoperability, exportability and backend portability;
- a mandatory production environment lacks viable OTel support.

### D2 — Cockpit source-of-truth separation

`OUTCOME: CANDIDATE_FOR_T010_LOCK`

Use a durable ordered product event/run-state source for live Cockpit correctness; treat telemetry as a correlated derived signal.

Confidence: **HIGH**.

Reversal condition:

- selected observability substrate is proven under the Academy workload to provide transactional product-event durability, replay, authorization/isolation and failure independence without loss/sampling semantics. No current evidence proves that.

### D3 — Default telemetry content posture

`OUTCOME: CANDIDATE_FOR_T010_LOCK`

Metadata-first; raw documents/prompts/model inputs/model outputs/repair text disabled by default. Secrets/credentials never allowed. Exceptional sensitive capture must be explicit, scoped, audited, redacted and policy-retained.

Confidence: **HIGH**.

Reversal conditions:

- partner/security requirement demonstrates content capture is necessary and approved;
- a narrower derived/hashed/fragment approach cannot meet the need.

Secret/credential exclusion is non-reversible within compatible production security requirements.

### D4 — Metric dimension policy

`OUTCOME: CANDIDATE_FOR_T010_LOCK`

Use a metric-attribute allowlist of bounded dimensions. Exclude tenant/workspace/request/run/job/document/trace/span IDs from default metric labels.

Confidence: **HIGH**.

Reversal condition:

- a specific backend/metric design demonstrates safe bounded cardinality for a particular ID dimension with measurable operational value. The default remains deny.

### D5 — LLM/eval observability backend

`OUTCOME: NO_OVERALL_PREFERENCE`

Keep Grafana-family general OTel backend, Phoenix and Langfuse as credible candidates; retain LangSmith as a runtime-coupled counterfactual. A hybrid general + AI-specific topology is also viable but must justify duplicated telemetry/cost/privacy surface.

Confidence in pending state: **HIGH**.

Required deciding evidence:

- identical Academy clean-run trace/eval slice;
- traces/metrics/logs coverage actually needed by operators;
- tenant isolation/auth/access controls;
- self-host/cloud deployment fit and data residency;
- ingestion/query latency under representative volume;
- retention/storage growth;
- collector/exporter failure/recovery behavior;
- maintenance/upgrade burden;
- current pricing under observed usage;
- exportability and migration/reversal cost.

### D6 — AI semantic convention

`OUTCOME: PENDING_EVIDENCE`

Pin a specific OpenTelemetry GenAI semantic-convention version and/or OpenInference adapter only after the selected provider/runtime/backend slice proves compatibility. Durable Academy domain event names remain independent.

Confidence: **MEDIUM**.

### D7 — Sampling and retention values

`OUTCOME: PENDING_EVIDENCE`

- no production trace sampling percentage selected;
- no retention-day values selected;
- no numeric alert/SLO thresholds selected.

Controlled acceptance runs should use 100% required instrumentation to prove completeness; later production sampling must never sample away authoritative product/audit evidence.

Confidence: **HIGH** that deferral is required.

## 10. Security/reliability/cost/lock-in analysis

### Security

- source-level telemetry allowlist is mandatory;
- collector redaction is second-line defense;
- no secrets or raw credentials;
- browser receives only server-authorized projections;
- external SaaS export should use pseudonymous/HMAC tenant/workspace/document identifiers where direct identity is unnecessary;
- untrusted incoming trace context may be sanitized/ignored at trust boundaries;
- tenant/run IDs are authorization context, not authorization proof.

### Reliability

- telemetry outage must not corrupt/block product state unless a later explicit fail-closed safety requirement says otherwise;
- collector exporter health/drop/backpressure must be observable;
- tail sampling needs topology evidence because it is stateful and requires a trace's spans to reach the same decision point;
- durable event replay and snapshot fallback are separate from telemetry export.

### Cost

No backend cost winner is claimed. Main controllable drivers identified:

- event/span/log volume;
- content payload size;
- trace retention;
- metric cardinality;
- duplicated export to multiple backends;
- tail-sampling collector resources;
- query/ingest pricing for managed services.

The local content-payload probe establishes direction but not production cost.

### Lock-in

Lowest application-level lock-in comes from keeping core workflow instrumentation on OTel/OTLP and keeping durable product event schemas vendor-neutral. Vendor-specific attributes/exporters may exist at adapters/collector/backend layers.

## 11. Telemetry/event schema output

Detailed implementation contract:

- `docs/observability/W005_T007_OBSERVABILITY_ARCHITECTURE.md`

Includes:

- correlation fields;
- span skeleton source→9→eval→repair→aggregate;
- ordered event envelope;
- redaction/visibility classes;
- metric allowlist approach;
- sampling/retention posture;
- dashboard/alert inputs;
- Phase 9 acceptance tests.

## 12. Traceability

Primary refs:

- `PROD-011` — live evidence cockpit;
- `PROD-012` — observability;
- `PROD-014` — security/privacy;
- `RISK-0035` — synthetic/stale frontend evidence;
- `RISK-0037` — sensitive telemetry leakage;
- `A-0016` — maximum safe frontend visibility.

Secondary affected risks:

- `RISK-0031` cross-tenant leakage;
- `RISK-0038` invented/untested capacity;
- `RISK-0040` research without decision value.

Downstream tasks:

- T004: bind telemetry query/event authorization to selected tenancy model;
- T008: benchmark collector/backend overhead, failure, capacity, recovery and establish operational thresholds;
- T009: align future backend bakeoff with cross-cutting statistical method;
- T010: decide/lock architecture from accepted fan-in;
- Phase 9: implement/test schema and security canaries.

## 13. Research limitations

- no real production Academy traffic exists yet;
- no Suno partner retention/data-residency policy is known;
- no real multi-user deployment was benchmarked;
- no real collector/backend ingestion latency or CPU/memory overhead was measured;
- no current managed-service cost was calculated because usage and deployment region are undecided;
- T002 peer research may still be rejected/revised by the Orchestrator; T007's event envelope remains transport-neutral if that occurs.

These limits prohibit a backend winner and any `PRODUCTION_READY` claim.
