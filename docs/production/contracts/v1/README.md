# Phase 9 production contracts v1

`CONTRACT_PACKAGE_VERSION: 1.0.0`

Authority: `W006-T001-A01`, derived from the accepted W005 Phase 9 fan-in plan. This package defines interfaces only; it does not select a database, workflow engine, parser/OCR provider, model provider, evaluator framework, observability backend, frontend framework, hosting vendor, or public-URL extractor.

## 1. Canonical identity

Every protected resource contract carries `contract_version`, `org_id`, and `workspace_id`. Where applicable it also carries stable opaque `user_id`, `document_id`, `run_id`, `job_id`, `branch_id`, `attempt_id`, `eval_id`, `repair_id`, and `experiment_id`.

Rules:

- IDs are opaque and never authorize access by themselves.
- A cursor, artifact ID, source ID, or provider ID can never select a tenant/resource without authoritative tenant resolution.
- Resource ownership is evaluated server-side against `org_id + workspace_id`.
- Accepted artifacts and evaluations remain traceable to the run/attempt identities that produced them.

## 2. Event envelope and cursor

`EventEnvelope` in `core-contracts.schema.json` is the internal event contract.

Normative invariants:

- stream scope is `(org_id, workspace_id, run_id)`;
- `cursor` is an integer that is **strictly increasing** for committed events in that stream;
- a cursor is a replay position, never an authorization capability;
- reconnect/replay de-duplicates by stable `event_id` and cursor;
- an event must represent an authoritative committed transition or an explicitly reconciled projection; an event cannot silently become the source of truth for tenant identity;
- event payloads may carry artifact references but must not require raw provider/extractor payloads.

## 3. Renderer-aligned provenance and parsed documents

`ProvenanceRef` binds a source artifact hash to `document_id` and an anchor kind (`document`, `page`, `region`, `block`, `node`, `table`, `cell`, or `derived`). Page/region/renderer references are preserved when known.

`ParsedDocument` consists of typed nodes where every accepted node has one or more provenance references. Parsers must not invent character/text offsets when the renderer/source does not supply a stable equivalent. Derived nodes retain parent provenance IDs rather than severing lineage.

This contract allows future parser/OCR candidates to compete behind the same output boundary; it does **not** choose one.

## 4. Provider and evaluator metadata

`ProviderMetadata` and `EvaluatorMetadata` are deliberately provider-neutral. They expose opaque versioned references such as provider/model capability, policy/catalog/pricing identity, evaluator version, rubric, and calibration references.

Concrete provider/model/evaluator selection remains evidence-gated. A metadata record is provenance, not an endorsement or routing decision.

## 5. Persistence and CAS

The canonical persistence record types are:

- `document`
- `blob`
- `provenance`
- `run`
- `event`
- `artifact`
- `evaluation`
- `index`
- `publish_attempt`

Every record is tenant-bound and revisioned. Binary/large immutable material is referenced through content-addressed `sha256` metadata. `CasWriteIntent` requires `expected_revision` plus an idempotent `mutation_id`; implementations must reject stale expected revisions rather than silently overwriting a newer run/resource state.

The schema defines the storage contract, not the backing database/object store.

## 6. Telemetry allowlist and redaction

`TelemetryEnvelope.attributes` is an explicit allowlist. Safe-by-default attributes are identifiers needed for correlation, versions/types/status/error class, bounded counts/durations/latencies/retries, opaque provider/evaluator refs, artifact IDs/hashes, and a redaction marker.

Default deny applies to everything else. In particular, the following MUST NOT be emitted by default into traces, metrics, logs, live events, or audit projections:

- raw extractor/parser backend output;
- raw provider/backend response bodies;
- full source document text or binary payloads;
- prompts or generated content unless a separately authorized, purpose-specific projection explicitly permits it;
- request/response headers;
- cookies, bearer tokens, API keys, credentials, secrets, connection strings;
- arbitrary filesystem paths or private backend object locations.

When debugging requires sensitive material, store it only in a separately authorized/quarantined artifact path and emit a safe artifact/hash reference rather than the raw material.

## 7. Decision Research normalization

Canonical registry: `docs/decisions/DECISION_RESEARCH_REGISTRY.v1.json`.
Schema: `decision-research-registry.schema.json`.

There is one global canonical namespace: `DR-####`. Existing source documents remain immutable evidence records and are resolved through registry aliases. A duplicate legacy `DR-0001` is disambiguated without deleting either source; research documents whose historic IDs were task-local receive canonical registry IDs.

Normalized status semantics:

- `OPEN`: question registered, no sufficient evidence work yet;
- `EVIDENCE_REQUIRED`: evidence is known to be insufficient for promotion;
- `RESEARCHING`: active evidence collection/benchmarking;
- `READY_FOR_DECISION`: evidence record is available for a promotion authority to evaluate;
- `LOCKED`: source decision is explicitly authoritative and may bind runtime/default behavior;
- `DEFERRED`: deliberately postponed, non-binding;
- `REJECTED`: evaluated and rejected, non-binding;
- `SUPERSEDED`: replaced by an explicit canonical successor, non-binding except for history.

Only `LOCKED` decisions or exact source subclaims explicitly marked `LOCK` are binding. Mixed research records use `SOURCE_LOCKED_SUBCLAIMS`: their locked clauses survive normalization, while pending/no-preference clauses remain open. No duplicate DR is created for an already represented claim.

## 8. Versioning and compatibility

All objects in this package carry `contract_version = 1.0.0`. Backward-incompatible field/semantic changes require a new contract version; consumers must fail closed on an unsupported major contract instead of guessing field meaning.

## 9. Evidence-gated boundaries preserved

This task intentionally leaves unresolved: concrete persistence/workflow/runtime providers, parser/OCR winner, provider/model portfolio, evaluator tooling winner, observability backend, production deployment topology, frontend/editor framework, and derived public URL extraction. Those choices require downstream common-harness evidence and DRG promotion.
