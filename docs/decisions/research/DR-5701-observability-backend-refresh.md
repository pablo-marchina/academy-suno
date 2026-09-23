# DR-5701 — W006 observability backend/topology refresh

`DR_ID: DR-5701`  
`TASK_ATTEMPT_ID: W006-T012-A01`  
`DATE: 2026-09-23`  
`DECISION_RESEARCH_GATE: SATISFIED_FOR_IMPLEMENTATION_BOUNDARY`  
`PRODUCTION_LOCK_SCOPE: NONE`  
`DECISION: NO_OVERALL_PREFERENCE / PENDING_REPRESENTATIVE_BACKEND_BAKEOFF`

## 1. Decision question

Which observability backend/collector topology, if any, should be promoted while W006-T012 integrates W3C trace propagation, OpenTelemetry-compatible instrumentation, OTLP export, provider/eval/repair spans, bounded metrics and authorized cockpit trace links on the accepted real/reference 3×3 path?

This refresh does **not** reopen the already accepted architecture boundary from DR-0701: W3C Trace Context + OpenTelemetry signal semantics + OTLP/Collector remain the portable boundary. The open question is whether current evidence is sufficient to promote a concrete backend or collector topology.

## 2. Workload / constraints

Hard requirements from the current product/dispatch boundary:

- real/reference path is document → trusted source/provenance → exactly 3×3 branches → eval/repair → aggregate → durable product events → live cockpit;
- durable product/run state and durable ordered product/domain events remain authoritative; sampled telemetry cannot become cockpit state authority;
- provider/eval/repair spans must correlate to source/run/job/attempt without exposing raw tenant/run/job identifiers in default metrics;
- raw credentials/secrets in telemetry = `0`;
- raw private content emitted by default = `0`;
- high-cardinality tenant/run/job identifiers as default metric labels = `0`;
- unauthorized cockpit trace-link access = `0` in defined tests;
- telemetry export/backend outage corrupting or blocking the authoritative product path = `0`;
- no production SLO, retention, capacity, cost or backend winner may be invented from local/reference evidence.

The accepted single-project Python toolchain remains Python `3.13.15` + `uv@0.12.18` with the committed lock. This task therefore keeps application instrumentation dependency-neutral and exercises W3C/OTLP protocol contracts without adding a backend-specific SDK/package lock.

## 3. Alternatives

### A0 — Direct application OTLP to a backend, no Collector

Benefits:

- minimum topology;
- fewer moving pieces for a small deployment.

Material limitations:

- pushes retry/filter/redaction/routing responsibility toward application processes or vendor endpoint behavior;
- weaker operational isolation when backend behavior changes;
- makes multi-backend routing and centralized export policy harder.

Retained as a deployment counterfactual only. Not promoted.

### A1 — OpenTelemetry Collector gateway + Grafana-family backend

Representative shape: application OTLP → Collector gateway → Tempo for traces plus metrics/logs backends such as Mimir/Loki or equivalent managed ingestion.

Documented strengths:

- OTLP-native ingestion path;
- Tempo supports multi-tenant trace isolation using tenant-scoped headers when multitenancy is enabled;
- general SRE signal coverage is available across the Grafana stack rather than trace-only UX.

Open evidence gaps:

- Academy-specific query latency, ingestion/resource cost, tenant configuration, retention and operational burden are unmeasured;
- the exact metrics/logs backend combination is itself a topology choice;
- no production load/capacity curve exists yet.

### A2 — OpenTelemetry Collector / Data Prepper + OpenSearch observability

Representative shape: application OTLP → Collector and/or Data Prepper unified OTLP source → OpenSearch trace/log/observability surfaces.

Documented strengths:

- Data Prepper exposes unified OTLP ingestion for telemetry pipelines;
- OpenSearch provides trace analytics and a broader searchable operational-data platform.

Open evidence gaps:

- direct protocol details differ by Data Prepper source; the current unified OTLP HTTP path is documented with protobuf, while this task's dependency-neutral reference exporter exercises OTLP/HTTP JSON;
- Academy-specific resource cost, multi-tenant isolation model, schema/index operations and retention are unmeasured;
- operational footprint may be materially larger than a trace-specialized backend.

### A3 — OpenTelemetry Collector + Jaeger for traces + separate metrics/logs backend

Documented strengths:

- Jaeger 2.x accepts OTLP over gRPC and HTTP and is a mature trace-focused backend;
- simple trace exploration can be operationally attractive when traces are the primary need.

Material limitation for this product:

- Jaeger is trace-focused; PROD-012 also requires metrics and structured logs, so a complete topology needs additional signal backends and correlation conventions.

Open evidence gaps:

- combined operational burden and cross-signal UX versus A1/A2 are unmeasured on the Academy workload.

## 4. Predeclared evaluation criteria

No scalar score or weighted utility is used. Hard gates are non-compensatory.

| Criterion | Type | Required evidence |
|---|---|---|
| W3C/OTLP interoperability | hard | protocol-compatible application boundary |
| traces + metrics + logs | hard product coverage | all three signal classes exportable/inspectable |
| product-path outage isolation | hard | exporter/backend failure cannot block/corrupt product state/events |
| privacy / secret exposure | hard | raw credentials/secrets/private content default = 0 |
| metric cardinality control | hard | raw tenant/run/job IDs absent from default metric labels |
| tenant-safe trace access | hard | server-side scoped opaque trace references |
| 3×3 correlation completeness | hard | all controlled branches traceable by safe correlation refs |
| query/ingest latency | quantitative | representative deployed benchmark |
| resource/cost footprint | quantitative | representative deployed benchmark + current pricing where applicable |
| retention/operations | quantitative/operational | environment-specific deployment evidence |
| lock-in/reversibility | qualitative + protocol evidence | application remains OTLP/W3C portable |

## 5. Systematic source refresh

Search date: `2026-09-23`.

Primary/official sources were prioritized. Search stopped when the refresh confirmed the accepted portable boundary, exposed the current protocol/topology distinctions among three materially different backend families, and remaining discriminators required a deployed representative benchmark rather than more documentation.

| ID | Source | Evidence used | Limitation |
|---|---|---|---|
| S01 | https://www.w3.org/TR/trace-context/ | interoperable `traceparent`/`tracestate` boundary | context standard, not backend selection |
| S02 | https://opentelemetry.io/docs/specs/otlp/ | current OTLP specification; traces/metrics/logs; OTLP/HTTP protobuf or JSON; standard `/v1/traces`, `/v1/metrics`, `/v1/logs` paths | protocol spec, not operational benchmark |
| S03 | https://opentelemetry.io/docs/collector/deployment/ | Collector deployment patterns including agent/gateway | topology guidance; workload fit unmeasured |
| S04 | https://opentelemetry.io/docs/collector/deployment/gateway/ | centralized policy/filtering/sampling benefits and added failure/latency/resource trade-offs | no Academy-specific measurement |
| S05 | https://grafana.com/docs/tempo/latest/operations/manage-advanced-systems/multitenancy/ | tenant-scoped Tempo reads/writes when multitenancy enabled | trace component only |
| S06 | https://grafana.com/docs/tempo/latest/configuration/network/tls/ | Tempo/OTLP operational transport configuration context | deployment-specific |
| S07 | https://www.jaegertracing.io/docs/2.21/apis/ | Jaeger 2.21 OTLP gRPC/HTTP ingestion; trace-focused API surface | not a metrics/logs backend |
| S08 | https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/unified-otlp-source/ | unified OTLP source for logs/metrics/traces; protocol constraints | operational fit unmeasured |
| S09 | https://docs.opensearch.org/latest/observing-your-data/trace/ta-dashboards/ | OpenSearch trace analytics surfaces | broader stack still needs deployed evidence |
| S10 | `docs/decisions/research/DR-0701-observability-telemetry-safe-live-evidence.md` | prior systematic observability architecture research | dated one day earlier; refreshed here for W006 implementation |

## 6. Representative workload evidence in this attempt

The W006-T012 implementation and tests exercise the accepted real/reference 3×3 path, not a synthetic dashboard-only path:

- inbound W3C parent context is propagated into the run trace;
- exactly nine provider spans and nine eval spans are generated for the controlled 3×3 run;
- repair instrumentation is explicitly exercised;
- eleven durable authoritative product events remain replayable independently from telemetry;
- raw source canary content is absent from product telemetry in the defined test;
- tenant/run/job identifiers use one-way correlation references in telemetry and are excluded from default metric labels;
- an opaque cockpit trace reference is authorized server-side against exact organization/workspace/run scope;
- OTLP/HTTP JSON payload generation exercises traces, metrics and logs on the standard paths;
- injected exporter/backend failure is best-effort only and leaves completion + event replay healthy.

This is **application/protocol integration evidence**, not a deployed backend performance bakeoff. No network/backend latency, capacity, cost, retention or SLO claim is made.

## 7. Raw comparison / Pareto status

| Candidate | 3 signals in complete topology | OTLP boundary | Tenant controls documented | Additional topology burden | Representative Academy backend benchmark |
|---|---|---|---|---|---|
| A0 direct backend | backend-dependent | yes | backend-dependent | low topology / higher app-policy coupling | `NOT_RUN` |
| A1 Collector + Grafana family | yes | yes | Tempo tenant controls documented | multiple signal stores/components | `NOT_RUN` |
| A2 Collector/Data Prepper + OpenSearch | yes | yes, protocol details differ by source | deployment-specific | unified/search platform operations | `NOT_RUN` |
| A3 Collector + Jaeger + separate metrics/logs | yes only with extra backends | yes | deployment-specific | multi-backend correlation burden | `NOT_RUN` |

No candidate dominates across deployment burden, three-signal completeness, tenancy, query behavior, cost and operational fit without representative deployed evidence. There is therefore no justified production winner.

## 8. Decision

### Application boundary

**IMPLEMENT / PRESERVE**:

- W3C Trace Context propagation;
- OpenTelemetry-compatible span/metric/log semantics;
- OTLP-compatible export boundary;
- metadata-first, allowlisted telemetry attributes;
- bounded metric dimensions;
- opaque, server-authorized trace references;
- durable product events independent from sampled telemetry.

The task-local Python implementation is a dependency-neutral **reference implementation of these contracts**, not a claim that a custom telemetry SDK should become the production default. A production OTel SDK/package selection remains reversible inside the accepted W3C/OTLP architecture boundary.

### Backend / Collector topology

`NO_OVERALL_PREFERENCE / PENDING_REPRESENTATIVE_BACKEND_BAKEOFF`.

No Grafana, OpenSearch, Jaeger, managed vendor, sampling policy, retention value, SLO/capacity target or collector deployment topology is promoted by this worker.

## 9. Confidence

- **HIGH** that W3C + OTel signal semantics + OTLP is the correct portable application boundary under current project constraints; this is consistent with the accepted prior DR and refreshed primary sources.
- **HIGH** that telemetry must remain non-authoritative for live cockpit state.
- **LOW** for any concrete production backend/topology winner because deployed workload evidence is absent.

## 10. Reversal / promotion conditions

A backend/topology may be promoted only after a representative environment exists and a DRG-compliant bakeoff measures, on the same Academy workload:

- ingest/query p50/p95/p99;
- dropped/rejected telemetry and retry/queue behavior;
- product-path isolation under exporter/backend outage;
- resource utilization and current cost/pricing evidence;
- tenant access controls/adversarial checks;
- retention/storage behavior;
- operational complexity and recovery behavior;
- three-signal correlation UX.

Any critical privacy, tenancy or product-path isolation failure eliminates a candidate regardless of lower cost/latency.

## 11. Traceability

- `PROD-011`: authorized opaque trace-link surface connected to the real/reference cockpit projection.
- `PROD-012`: W3C correlation, provider/eval/repair spans, bounded metrics, structured logs, OTLP-compatible export.
- `PROD-014`: metadata allowlist/redaction and scoped trace-link authorization.
- `RISK-0035`: durable product events remain live truth; telemetry is explicitly non-authoritative.
- `RISK-0037`: raw content/secrets default-off and high-cardinality metric dimensions rejected.
