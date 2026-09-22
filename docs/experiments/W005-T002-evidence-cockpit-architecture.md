# W005-T002 — Live Evidence Cockpit architecture experiment

`TASK_ATTEMPT_ID: W005-T002-A01`

`STATUS: RESEARCH_ARTIFACT`

`CLAIM_BOUNDARY: architecture/UX contract; not production implementation or production readiness`

## 1. Baseline observed

The current repository has two useful but intentionally limited surfaces:

1. `app/recipient/server.py` is a synchronous `ThreadingHTTPServer` recipient flow with inline HTML/CSS. It accepts PDF upload, text input, and a local filesystem PDF path. It renders source-trust, 3×3 mechanics, evidence/repair and extracted text in one response.
2. `app/evidence_cockpit.py` is a CLI that reads existing RunStore/proof/telemetry/calibration artifacts and writes a disposable static HTML projection. `src/suno_content/cockpit/*` correctly preserves per-claim evidence states, provenance, FAIL/REVIEW_REQUIRED, repair before/after and no aggregate “green” score.

Those semantics are assets to preserve. The production gap is interaction/runtime architecture: no authenticated multi-user application shell, no typed/versioned production API, no durable live event stream, no server-side tenant-filtered source explorer, and no real-time run graph.

The local-path input is also a deliberate production boundary violation under `PROD-002`; the production UI must use controlled upload/object references rather than arbitrary server filesystem paths.

## 2. Proposed information architecture

The cockpit should be route-addressable so evidence can be deep-linked, refreshed and audited without relying on transient component state.

| Route concept | Primary purpose |
|---|---|
| `/w/:workspaceId` | workspace summary, recent documents/runs, health cues |
| `/w/:workspaceId/documents` | document list/upload state/source trust |
| `/w/:workspaceId/documents/:documentId` | source metadata, extraction, fragments/citations, run history |
| `/w/:workspaceId/runs/:runId` | canonical run cockpit shell |
| `/w/:workspaceId/experiments/:experimentId` | baseline/candidate comparison with dataset/config provenance |
| `/w/:workspaceId/research` | decision/research records exposed read-only |

### Run cockpit shell

Persistent header:
- workspace / document / run identity;
- run phase and blocking state;
- explicit evidence scope;
- last observed event timestamp;
- reconnect/stale indicator;
- actions allowed by authorization only.

Primary navigation:
1. **Overview** — source trust, run status, blockers, branch coverage, claim states.
2. **Live graph** — nodes/edges, node phase, attempts, retry/repair markers, latest event.
3. **3×3** — beginner/intermediate/advanced × article/carousel/short-video; no averaging.
4. **Sources** — source metadata, fragment explorer, citations, extraction warnings.
5. **Evals** — hard gates first, then diagnostics/judges with configuration provenance.
6. **Repair** — immutable before/after, failure-code delta, fresh-gate evidence.
7. **Experiments** — candidate/baseline runs with same dataset/config identity.
8. **Traces** — correlated request/run/job spans and safe span metadata.
9. **Operations** — latency, tokens, retries, queue/health, provider cost evidence state.
10. **Audit & Research** — actor/action provenance and decision/research records.

### Responsive 3×3

Desktop keeps a semantic table because row/column relationships are evidence. Small viewports may render an audience-by-audience stacked representation, but all nine cells remain available, preserve the same order, and retain state text in addition to visual styling. FAIL/REVIEW_REQUIRED cells may not be collapsed into a positive summary.

### Dynamic accessibility

- Prefer semantic HTML regions/headings/tables before ARIA.
- Live operational status changes use a bounded/polite live region; hard errors use an explicit error/status pattern without continuously reading the whole event stream.
- Every graph fact must have a non-graph textual/table representation.
- Source/citation selection, tabs, expandable evidence, and repair comparison must be keyboard operable.
- Focus moves only after explicit user navigation, not on every incoming event.
- Color is never the only carrier of evidence state.

## 3. Source selection and citation click-through

The editor/output viewer and source explorer must share stable citation identities rather than embedding privileged raw source payloads in the generated content.

Suggested citation shape:

```json
{
  "citation_id": "cit_01J...",
  "source_id": "src_01J...",
  "fragment_id": "frag_00042",
  "locator": {"page": 7, "block": 12},
  "source_hash": "sha256:...",
  "claim_ref": "output.block.18",
  "verification_state": "SUPPORTED"
}
```

Click flow:
1. user activates a citation;
2. client requests the fragment by opaque IDs in the active workspace;
3. server re-authorizes workspace/document/source visibility;
4. server returns a bounded sanitized excerpt plus locator/provenance, never an arbitrary path;
5. UI opens the Sources region and highlights the exact fragment;
6. a “view surrounding context” action requests another bounded window;
7. audit can record source-read metadata without logging sensitive document text by default.

No client-side filter is a security boundary. A user who cannot read a source must not receive its excerpt in initial HTML, JSON, event payload, trace metadata or hidden DOM.

## 4. Typed HTTP boundary

Material contract:

- commands/queries use a versioned HTTP API;
- uploads use controlled multipart/object references with limits and content validation;
- create/retry/repair actions accept an idempotency key where duplicate execution matters;
- the API returns opaque artifact/source/trace references;
- request identity, workspace and authorization are resolved server-side;
- error bodies use a versioned machine-readable shape;
- OpenAPI describes the HTTP surface, but the exact OAS minor stays toolchain-gated until W005-T013 validates generator/linter compatibility.

Representative endpoints:

```text
POST /api/v1/workspaces/{workspace_id}/documents
GET  /api/v1/workspaces/{workspace_id}/documents/{document_id}
POST /api/v1/workspaces/{workspace_id}/documents/{document_id}/runs
GET  /api/v1/workspaces/{workspace_id}/runs/{run_id}
GET  /api/v1/workspaces/{workspace_id}/runs/{run_id}/events
POST /api/v1/workspaces/{workspace_id}/runs/{run_id}/jobs/{job_id}/retry
POST /api/v1/workspaces/{workspace_id}/runs/{run_id}/jobs/{job_id}/repair
GET  /api/v1/workspaces/{workspace_id}/sources/{source_id}/fragments/{fragment_id}
GET  /api/v1/workspaces/{workspace_id}/runs/{run_id}/traces
GET  /api/v1/workspaces/{workspace_id}/research/decisions
```

## 5. Live event contract

Run telemetry is server-to-browser and does not require client messages on the same channel. Commands remain normal typed HTTP requests. That makes SSE the default live-run transport candidate.

SSE example:

```text
id: run_01J:00000127
event: job.phase.changed
data: {"schema_version":"run-event.v1","id":"run_01J:00000127","cursor":127,"occurred_at":"2026-09-22T12:00:00Z","workspace_id":"ws_01J","run_id":"run_01J","job_id":"job_03","type":"job.phase.changed","visibility":"workspace","payload":{"from":"generated","to":"evaluating","attempt":2},"redactions":[]}
```

Envelope invariants:

```json
{
  "schema_version": "run-event.v1",
  "id": "run_01J:00000127",
  "cursor": 127,
  "occurred_at": "2026-09-22T12:00:00Z",
  "workspace_id": "ws_01J",
  "run_id": "run_01J",
  "job_id": "job_03",
  "type": "job.phase.changed",
  "visibility": "workspace",
  "payload": {},
  "redactions": []
}
```

Rules:
- `cursor` is monotonic within a run event log.
- `id` is stable and unique for dedupe.
- event records are append-only/durable enough for the supported resume horizon.
- reconnect supplies `Last-Event-ID` or explicit `after` cursor; server re-authorizes before replay.
- client treats delivery as at-least-once and de-duplicates by ID/cursor.
- on cursor gap, schema mismatch or replay horizon expiry, client fetches the canonical run snapshot and resumes from the returned cursor.
- heartbeats contain no domain payload and prevent idle intermediaries from silently holding a dead connection.
- event payloads contain safe projections, not provider prompts, raw documents, credentials or unrestricted trace bodies.
- server emits authorization-filtered events; visibility is informational, not the enforcement mechanism.

Suggested domain event types:

```text
run.created
run.phase.changed
source.trust.changed
job.created
job.phase.changed
job.attempt.started
job.attempt.finished
evaluation.completed
repair.started
repair.completed
review.required
artifact.created
telemetry.updated
run.completed
run.failed
```

### Authentication note

Native browser `EventSource` only exposes URL plus credentials mode, not arbitrary request headers. Therefore the preferred deployment shape is same-origin credentialed SSE using secure HttpOnly session cookies, or a deliberately chosen fetch-stream/polyfill path if the auth architecture requires bearer headers. This must be reconciled with W005-T004 rather than hidden in the frontend.

## 6. SSE, WebSocket and polling split

| Path | Intended use | Resume | Interaction | Outcome |
|---|---|---|---|---|
| SSE | live run graph/status/eval/ops events | `id` / `Last-Event-ID` + durable cursor | server → client | **LOCK for run telemetry contract** |
| WebSocket | true simultaneous editor presence/CRDT collaboration if later required | app/provider-specific | bidirectional | **PENDING_EVIDENCE** |
| cursor polling | degraded fallback / environments that buffer streams | explicit cursor | request/response | **NO_PREFERENCE as fallback; not default** |

The transport probe in `experiments/w005_t002_cockpit_architecture/` measures application framing only. At ~777-byte JSON events, SSE adds 7.465% application framing, server WebSocket frames 0.515%, and 25-event polling batches 0.288% before HTTP/TLS overhead. A 1 s polling interval adds a modeled ~500 ms mean / ~950 ms p95 delivery delay under uniform arrival. The result supports accepting modest SSE text framing in exchange for native one-way semantics and resume primitives; it is not a network-latency benchmark.

Classic WebSocket remains a valid transport where bidirectionality is actually required, but its browser API has no built-in backpressure and replay is application-defined. It should not become the universal cockpit transport merely because an editor may later use a WebSocket collaboration provider.

## 7. Editor architecture

Editing and evidence inspection have different trust semantics:
- source documents are immutable evidence;
- generated outputs may be editable/repaired;
- citations/provenance must remain structured data rather than decoration;
- collaboration is valuable only if the product requirements actually need concurrent editing.

Alternatives:

| Alternative | Strengths for this product | Material risks | Outcome |
|---|---|---|---|
| plain textarea/contenteditable + custom code | smallest dependency surface; adequate for raw-text input | rich structured selection, citations, history, comments and collaboration become bespoke | **LOCK only for simple raw text ingest; not rich editor** |
| Tiptap/ProseMirror | extension model; Yjs collaboration; mature rich-editor concepts | comments/tracked-change paths can introduce paid/provider coupling; collaboration adds Yjs/provider infrastructure | **PENDING_EVIDENCE** |
| Lexical | extensible JSON-serializable nodes/NodeState; React collaboration via Yjs | current official collab guide centers `y-websocket`; collaboration/bootstrap has operational rules; editor-specific regression work still needed | **PENDING_EVIDENCE** |

No rich editor winner is locked in W005-T002. A future bakeoff must implement the same citation node/mark, PT-BR composition/IME, paste from financial tables, undo/redo, 100+ citations, keyboard/screen-reader path, serialization round-trip and optional two-client collaboration scenario. The winner must preserve citation IDs and document semantics across serialize/reload before lock.

## 8. Frontend application alternatives

| Alternative | Deployment/runtime boundary | Fit | Outcome |
|---|---|---|---|
| current Python inline HTML/static cockpit | one Python process / generated HTML; no browser app dependency | excellent evidence-integrity counterfactual; poor live/multi-user composition | **LOCK as diagnostic fallback/baseline, not sole production cockpit** |
| React browser app + Vite build | static production assets can be served independently of the Python API | clean separation for interaction-heavy cockpit; low need for a Node production runtime | **PENDING_EVIDENCE, leading candidate** |
| Next.js App Router | React plus server/runtime/BFF capabilities | useful if SSR/BFF/co-location has demonstrated value; otherwise adds a second server boundary beside Python | **PENDING_EVIDENCE** |

React itself is not controversial enough to justify inventing a winner before W005-T013 establishes the repository/package/build/test/deploy platform. As of the research date React 19.3 is current, Vite’s current supported regular patch line is 8.3, and Next’s current active-LTS security guidance is 16.3.3. Those are freshness observations, not version locks.

A framework bakeoff after T013 should use the same thin cockpit slice:
- authenticated workspace shell;
- one run snapshot;
- one SSE stream;
- one 3×3 matrix;
- one source/citation click-through;
- one repair before/after;
- automated keyboard/accessibility smoke;
- production build artifact.

Record cold install/build, build output bytes (raw + compressed), dependency count, Node/runtime requirement, CI seconds, route refresh behavior, test effort and deploy topology. Do not compare starter-homepage bundles; compare the same product slice.

## 9. Safe telemetry / redaction boundary

Never emit by default:
- access/refresh tokens, cookies, API keys;
- raw provider request/response bodies;
- unrestricted source/document text;
- uploaded filenames when they reveal local paths;
- arbitrary filesystem paths;
- secret environment/config values;
- full exception locals;
- cross-tenant identifiers/content not authorized to the active principal.

Safe-by-default event/trace metadata:
- opaque request/run/job/attempt/trace references;
- stage/phase;
- duration and normalized token/usage counters;
- provider/model IDs only when policy permits;
- error class/code with bounded sanitized message;
- evidence state and failure codes;
- content hashes when policy permits;
- redaction markers explaining omitted fields.

All trace/source “expand” operations are separate authorized reads. The frontend never receives a super-set and hides rows client-side.

## 10. Reconnection and stale-data UX

Connection states are explicit: `LIVE`, `RECONNECTING`, `STALE`, `SNAPSHOT_REQUIRED`.

- When SSE closes unexpectedly, keep last known evidence visible but mark it stale.
- Automatic reconnect may resume from last committed event ID.
- If replay succeeds, clear stale state only after cursors are contiguous.
- If replay cannot be proven contiguous, fetch canonical snapshot and reconcile.
- Never silently reset FAIL/REVIEW_REQUIRED because a live event was missed.
- The visible “last event” timestamp is observational, not a readiness signal.

## 11. Validation gates for implementation

Before production claim:
- server-side cross-tenant authorization tests cover snapshots, events, source fragments, traces and research records;
- reconnect/replay test demonstrates no lost accepted event across process/network interruption within declared replay horizon;
- event payload schema compatibility is version-tested;
- 3×3 render keeps 9/9 identities and non-compensatory states;
- citation click-through proves source hash/fragment provenance and bounded authorization;
- keyboard and screen-reader smoke covers primary workflows;
- live regions do not spam every telemetry event;
- browser app build/dependency footprint is measured on the selected thin slice;
- upload UI has no arbitrary server path control.

## 12. Cross-task handoffs

- **W005-T004**: authentication/session, tenant isolation, object/source access policy decide the exact credential path for SSE and source explorer.
- **W005-T006**: orchestration/runtime decides durable event-log production semantics and resume horizon.
- **W005-T008**: observability decides trace backend/export details; this contract only specifies the safe UI projection.
- **W005-T013**: Node/package/workspace/build/test/CI evidence is required before React/Vite vs Next can be locked.
- **W005-T010**: architecture synthesis should consume the decisions and pending-evidence items here; it must not treat “leading candidate” as a lock.
