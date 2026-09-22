# DR-0001 — Evidence Cockpit frontend/API/live-event architecture research

`DR_ID: DR-0001`

`TASK_ATTEMPT_ID: W005-T002-A01`

`DATE: 2026-09-22`

`DECISION_RESEARCH_GATE: SATISFIED_FOR_RESEARCH_OUTPUT`

`PRODUCTION_LOCK_SCOPE: PARTIAL`

## Decision question

Which frontend, API and live-update architecture should carry the real multi-user Evidence Cockpit while preserving the repository's strongest existing evidence semantics: explicit per-claim states, non-compensatory failures, source/run/job/attempt provenance, repair before/after, and no synthetic production-readiness score?

Subquestions:
1. What browser application boundary can support workspace/document/run navigation, live graph, 3×3, source explorer, eval/repair/experiments/traces/ops/audit/research?
2. Should run updates use SSE, WebSocket or polling?
3. What API/event contract preserves tenant authorization, replay and safe redaction?
4. Should rich editing use a dedicated editor engine, and can one be selected now?
5. Can React/Vite versus Next.js be selected before the developer-platform research in W005-T013?

## Constraints

Hard constraints:
- `SYSTEM/PRODUCTION_CONTRACT.md`, especially PROD-002/005/011/012/017;
- multi-user/multi-tenant and server-side authorization;
- typed/versioned API;
- no arbitrary server filesystem path for untrusted users;
- real live evidence, not demo-only parallel architecture;
- hard failures and unknown evidence remain visible/non-compensatory;
- safe-by-default traces/source views;
- deployment/test evidence before production claim;
- DRG forbids a stack winner based only on preference.

Important coordination constraints:
- W005-T013 independently owns repository/package/build/test/CI research;
- W005-T004 owns broader auth/tenancy/data security;
- W005-T006 owns workflow/runtime architecture;
- W005-T008 owns observability architecture;
- therefore this DR may lock interface/transport semantics that are already discriminated, but must leave framework/editor/toolchain choices pending where upstream evidence is absent.

## Alternatives considered

### A0 — current Python recipient/static cockpit baseline

Observed in repository:
- synchronous `ThreadingHTTPServer` recipient app;
- inline HTML/CSS;
- local text/PDF input and arbitrary local PDF path;
- static CLI-generated evidence cockpit;
- dependency-light deterministic rendering;
- strong evidence-state/provenance semantics;
- no live multi-user application boundary.

Counterfactual value: very high. Production fit as the *sole* cockpit: low because PROD-011 requires live graph/events, source explorer, experiments/traces/health/audit and PROD-002 forbids arbitrary untrusted filesystem paths.

### A1 — React browser app built with Vite + Python API

Shape:
- Python remains authoritative product/API/workflow boundary;
- browser app consumes versioned HTTP resources and SSE;
- production UI can build to static assets;
- no Node server is inherently required for the production UI if SSR/BFF is not needed.

Potential benefit: isolates the interaction-heavy cockpit without creating a second backend business-logic plane.

Open evidence: exact bundle/dependency/build/test/CI/deploy footprint must be measured after W005-T013 establishes the toolchain.

### A2 — Next.js App Router + Python API

Shape:
- React application with App Router;
- optional server components/BFF/server functions and Node runtime;
- can also behave as an SPA, but its value proposition includes server rendering/runtime features.

Potential benefit: useful if SSR, BFF auth mediation or server-side UI composition yields measurable product/operational value.

Risk: absent such value, it adds another server/runtime boundary beside the Python service and increases deployment/security patch surface.

Open evidence: same product-slice bakeoff as A1 plus clear evidence that server-side Next capabilities pay for the extra boundary.

### Editor E0 — raw textarea / hand-built contenteditable

Small dependency surface. Keep for raw-text ingest. Bespoke rich-editor behavior is not justified for citations/comments/structured provenance/collaboration.

### Editor E1 — Tiptap/ProseMirror family

Supports an extension model and Yjs collaboration. Tiptap's documented Comments/Tracked Changes paths include commercial/provider coupling, which is material if those features are required.

### Editor E2 — Lexical

Supports extensible JSON-serializable nodes/NodeState and React/Yjs collaboration. Official collaboration guidance currently centers `y-websocket`; production bootstrap and provider behavior add operational obligations.

No editor is selected without an identical product-specific spike.

## Criteria

No synthetic weighted total is used. Criteria are evaluated separately because a low score on tenant isolation or evidence integrity cannot be compensated by bundle size.

| Criterion | Why material |
|---|---|
| evidence integrity | FAIL/REVIEW_REQUIRED/provenance must survive UI refresh/live updates |
| tenant/security boundary | server must never overshare source/trace/event content |
| live semantics | reconnect/replay/stale behavior must be explicit |
| interaction/IA fit | PROD-011 needs many linked evidence views |
| deploy topology | avoid unjustified runtime planes and operational burden |
| testability | route, contract, reconnect and accessibility behavior must be automatable |
| accessibility | dynamic cockpit must remain usable without graph/color/mouse dependence |
| dependency/lock-in | editor/framework/provider coupling must be visible |
| bundle/runtime footprint | must be measured on the same product slice before framework lock |
| reversibility | early contracts should not make later framework/editor changes expensive |

## Systematic search protocol

Search buckets:
1. repository baseline and production contract;
2. browser live-transport standards and API behavior;
3. current official React/Vite/Next documentation/releases;
4. current official OpenAPI specification;
5. official Tiptap and Lexical editor/collaboration documentation;
6. W3C accessibility guidance for dynamic/region-based interfaces.

Primary sources were preferred: repository code/contracts, WHATWG, RFC Editor, framework/editor vendor docs and W3C. MDN was used as a browser API cross-check.

Stopping rule: stop when each bucket has at least one primary source, every material alternative has official documentation, and two successive searches do not introduce a new architecture class or a new hard constraint. Saturation was reached after the transport/auth detail that native `EventSource` exposes credentials mode but not arbitrary headers; later searches refined versions/deployment details without changing the architecture classes.

## Source table

Accessed 2026-09-22.

| ID | Source | Type | Evidence used |
|---|---|---|---|
| S01 | repository `app/recipient/server.py` | primary/local | current recipient HTTP/HTML/input boundary |
| S02 | repository `app/evidence_cockpit.py`, `src/suno_content/cockpit/*`, `docs/cockpit/README.md` | primary/local | static projection, evidence states, provenance, 3×3/repair/telemetry semantics |
| S03 | repository `SYSTEM/PRODUCTION_CONTRACT.md` | primary/local | PROD-002/011/012/017 hard requirements |
| S04 | https://html.spec.whatwg.org/multipage/server-sent-events.html | standard | SSE reconnection, `Last-Event-ID`, `text/event-stream`, event IDs/retry |
| S05 | https://www.rfc-editor.org/info/rfc6455/ | standard | WebSocket frame lengths and server frames not masked |
| S06 | https://developer.mozilla.org/en-US/docs/Web/API/EventSource/EventSource | browser reference | native EventSource constructor options: URL + `withCredentials` |
| S07 | https://developer.mozilla.org/en-US/docs/Web/API/WebSocket | browser reference | bidirectionality; classic WebSocket lacks backpressure |
| S08 | https://react.dev/blog/2026/09/09/react-19-3 | primary/vendor | React 19.3 current release observed |
| S09 | https://vite.dev/releases and https://vite.dev/guide/build | primary/vendor | current Vite 8.3 patch line; static production build boundary |
| S10 | https://nextjs.org/docs/app and https://nextjs.org/blog | primary/vendor | App Router/server-client model; current 16.3.3 Active LTS security guidance |
| S11 | https://spec.openapis.org/oas/v3.2.1.html | standard | language-agnostic typed HTTP description; 3.2.1 current spec observed |
| S12 | https://tiptap.dev/docs/editor/extensions/functionality/collaboration | primary/vendor | Yjs collaboration packages/model |
| S13 | https://tiptap.dev/docs/editor/extensions/functionality/comments and https://tiptap.dev/docs/tracked-changes/guides/comments-integration | primary/vendor | comments/tracked-changes commercial/provider coupling |
| S14 | https://lexical.dev/docs/concepts/nodes | primary/vendor | custom/serializable node model and NodeState |
| S15 | https://lexical.dev/docs/collaboration/react | primary/vendor | Yjs collab, officially supported y-websocket path, production bootstrap caveat |
| S16 | https://www.w3.org/WAI/standards-guidelines/aria/ | standard/guidance | dynamic content, live regions, keyboard semantics |
| S17 | https://www.w3.org/WAI/tutorials/page-structure/regions/ | standard/guidance | semantic regions/responsive structure |

Freshness notes:
- React 19.3 was published 2026-09-09.
- OpenAPI 3.2.1 was published 2026-09-10.
- Lexical 0.51.0 was released 2026-09-17, but version freshness is not a selection criterion by itself.
- Vite documentation reports regular patches on 8.3.
- Next's 2026-08 security guidance identifies 16.3.3 as Active LTS; this demonstrates maintenance reality, not disqualification.

## Reproducible benchmark

Artifact:
- `experiments/w005_t002_cockpit_architecture/transport_probe.py`
- `experiments/w005_t002_cockpit_architecture/probe_results.json`

Parameters per scenario:
- 10,000 deterministic events;
- requested minimum JSON payload 256 / 768 / 2048 bytes;
- polling interval 1,000 ms;
- polling batch 25 events;
- WebSocket server frame header derived from RFC 6455 payload-length rules;
- SSE exact text framing includes `id`, `event`, `data`;
- excludes HTTP/TLS/TCP setup, compression, proxy buffering, CPU and real network latency.

Observed application-framing overhead over compact JSON:

| mean JSON event | SSE | WebSocket server text frame | polling batches |
|---:|---:|---:|---:|
| 388.89 B | 14.914% | 1.029% | 0.575% |
| 777.00 B | 7.465% | 0.515% | 0.288% |
| 2057.00 B | 2.820% | 0.194% | 0.109% |

Polling delay model at 1 s, uniform arrival:
- mean 500.0 ms;
- p50 499.95 ms;
- p95 949.95 ms;
- p99 989.95 ms.

Replay check:
- cursor 5,000 → replayed 5,000 events;
- first 5,001; last 10,000;
- gap-free in the deterministic durable-log model;
- zero duplicates.

Interpretation boundary: this benchmark does **not** prove network latency, proxy compatibility or capacity. It discriminates application framing and the inherent poll-timer delay. Durable replay is an application/storage property, not a transport guarantee.

## Findings

### F1 — A live-run feed is naturally one-way

Run/job/eval/repair/telemetry updates flow server → browser; user commands already require authenticated/idempotent HTTP semantics. Using one bidirectional socket for both concerns is not required.

### F2 — SSE resume semantics fit the run event log

WHATWG defines event IDs and `Last-Event-ID` on reconnect. With a durable monotonic run cursor, this maps directly to replay/de-duplication. The application still must specify replay horizon and snapshot fallback.

### F3 — WebSocket saves framing bytes but adds semantics not needed for telemetry

The probe shows lower per-event application framing. That difference is small relative to typical 0.4–2 KB domain events and does not provide replay or backpressure automatically. WebSocket is justified where true bidirectional collaboration is required, not as a universal feed by default.

### F4 — polling is a useful fallback but a poor default for “live”

Batch framing is efficient, but a 1 s interval inherently adds about 500 ms mean / 950 ms p95 timer delay under the model and creates repeated requests. Reducing the interval increases request overhead.

### F5 — native EventSource constrains auth topology

The browser constructor provides URL and credentials mode, not an arbitrary headers dictionary. Same-origin secure session-cookie SSE is straightforward; bearer-header-only auth requires fetch-stream/polyfill/BFF handling. This is a cross-task dependency on T004 and must be explicit.

### F6 — current Python UI semantics should be preserved, not discarded

Its strongest properties are evidence discipline and low hidden complexity. The production cockpit should reuse/port those semantics through typed projections rather than create a new “pretty dashboard” that averages away unknowns/failures.

### F7 — React/Vite is architecturally simpler than Next when Python remains the API

Vite can produce static production assets, which permits a clean browser/Python boundary. Next adds useful server/BFF/SSR capabilities, but those capabilities need a demonstrated requirement; otherwise they create a second server plane. This is a rationale for a leading candidate, not enough evidence to lock the framework.

### F8 — rich editor selection is not yet evidence-complete

Both Tiptap and Lexical can represent structured rich content and collaborate through Yjs-related paths, but their provider/feature coupling differs. The Academy-specific requirements—stable citation identities, financial table paste, PT-BR composition, source click-through, serialization and accessibility—need an identical spike before selection.

### F9 — OpenAPI boundary can be locked without locking the minor release

The product contract already requires typed/versioned API semantics and OAS is language agnostic. Exact 3.1.x versus 3.2.x should be selected after generator/linter/client compatibility is measured by T013/implementation.

## Decisions

### D1 — Typed HTTP resource/command boundary

`OUTCOME: LOCK`

Lock the architectural contract: the browser cockpit consumes a versioned typed HTTP API; mutable commands are not hidden inside UI server components or a WebSocket channel. OpenAPI describes the HTTP boundary. Exact OAS minor and code-generation tool remain `PENDING_EVIDENCE`.

Confidence: **HIGH**.

Reversal conditions:
- production runtime synthesis demonstrates a materially safer/simpler equivalent typed interface while preserving external versioning, idempotency and testability;
- not reversible merely because a frontend framework offers server actions.

### D2 — Live run telemetry transport

`OUTCOME: LOCK`

Use SSE as the default browser transport for run/job/eval/repair/telemetry events, backed by durable ordered cursor semantics, `Last-Event-ID`/cursor resume, de-duplication and snapshot fallback.

WebSocket remains allowed for distinct truly bidirectional use cases such as concurrent editor collaboration.

Confidence: **MEDIUM-HIGH**.

Reversal conditions:
- deployment/load tests show unacceptable proxy buffering/connection scaling for the chosen environment;
- auth architecture makes secure same-origin/fetch-stream SSE materially worse than an alternative;
- measured event rate/size requires a binary or backpressured channel;
- a single collaboration socket demonstrably reduces total system complexity without weakening replay/audit separation.

### D3 — server-side authorization/redaction before serialization

`OUTCOME: LOCK`

Snapshots, events, source fragments and trace projections are tenant/user filtered on the server. The frontend never receives a privileged superset and “hides” it client-side.

Confidence: **HIGH**.

Reversal condition: none compatible with PROD-001/014; only implementation mechanism can change.

### D4 — source/citation interaction uses stable opaque references

`OUTCOME: LOCK`

Generated content stores stable citation/source/fragment identifiers and provenance; click-through fetches bounded authorized source context. Raw source text, filesystem paths and privileged trace/provider payloads are not embedded in live events.

Confidence: **HIGH**.

Reversal condition: identifier schema may evolve versionedly, but server-side authorization and provenance binding remain.

### D5 — frontend framework

`OUTCOME: PENDING_EVIDENCE`

React + Vite is the leading candidate when Python remains the authoritative API because it can ship static assets and avoids requiring a second application server. Next.js remains credible if SSR/BFF/server-side UI composition has measured value.

Do **not** lock until W005-T013 provides the production workspace/package/build/test/CI baseline and both candidates run the same thin cockpit slice.

Confidence in pending state: **HIGH**.

Required deciding evidence:
- same slice;
- install/build/CI times;
- production output bytes raw/compressed;
- dependency count;
- Node production runtime requirement;
- route/deep-link/reconnect behavior;
- auth integration;
- automated test effort;
- deployment topology/failure modes.

### D6 — rich editor engine

`OUTCOME: PENDING_EVIDENCE`

Tiptap/ProseMirror and Lexical remain candidates. Plain textarea is retained for simple raw-text ingest only.

Required deciding spike:
- structured citation node/mark with stable IDs;
- source click-through;
- paste financial tables/text;
- PT-BR composition/IME;
- undo/redo;
- 100+ citations;
- JSON/HTML serialization round-trip;
- keyboard/screen-reader path;
- optional two-client collaboration if concurrent editing is actually required;
- dependency/bundle/provider/licensing footprint.

Confidence in pending state: **HIGH**.

### D7 — polling

`OUTCOME: NO_PREFERENCE` as degraded fallback; `NOT_SELECTED` as default live path.

Cursor polling remains a compatibility/degraded-mode option if streaming is unavailable. It is not the primary live cockpit transport.

## Failure modes and mitigations

| Failure mode | Required behavior |
|---|---|
| SSE disconnect | mark data stale, reconnect, resume from cursor |
| cursor gap / replay expired | fetch canonical snapshot, reconcile, resume |
| duplicate event | de-dupe by stable event ID/cursor |
| out-of-order event | reject/reconcile based on run cursor |
| auth expires | terminate stream; re-auth flow; never reconnect anonymously |
| tenant membership revoked | server stops/rejects stream immediately on next auth enforcement point |
| source permission denied | no excerpt or hidden raw payload already present in DOM/state |
| schema version unknown | stop applying event; snapshot/upgrade path |
| event flood | coalesce safe telemetry views; retain durable domain events; do not rely on classic WS buffering |
| graph inaccessible | equivalent textual/table evidence path |
| live region spam | announce bounded state transitions, not raw event firehose |
| framework/editor dependency regression | versioned lockfile + CI/e2e once T013 chooses toolchain |

## Uncertainty

Known unknowns:
- production auth/session mechanism;
- deployment platform/proxy streaming behavior;
- concurrent-user/event-rate capacity targets;
- final JS workspace/package manager/test runner;
- whether true concurrent rich editing is a product requirement;
- product-specific frontend bundle sizes;
- exact OpenAPI minor/tooling interoperability.

These unknowns are deliberately not converted into fake scores or winner claims.

## Traceability

Inputs:
- `SYSTEM/DISPATCH/W005-T002-A01.md`
- `SYSTEM/PRODUCTION_CONTRACT.md`
- `SYSTEM/DECISION_RESEARCH_GATE.md`
- `app/recipient/server.py`
- `app/evidence_cockpit.py`
- `src/suno_content/cockpit/`
- `docs/cockpit/README.md`

Artifacts:
- `docs/experiments/W005-T002-evidence-cockpit-architecture.md`
- `experiments/w005_t002_cockpit_architecture/transport_probe.py`
- `experiments/w005_t002_cockpit_architecture/probe_results.json`
- `SYSTEM/RESULTS/W005-T002-A01.md`

Downstream:
- W005-T004, T006, T008, T013;
- architecture synthesis W005-T010.
