# Phase 9 production contracts v1

`CONTRACT_PACKAGE_VERSION: 1.0.0`  
`AUTHORITY_ATTEMPT: W006-T001-A02`

This task-owned package implements the contract and Decision Research traceability foundation authorized by the accepted W005 Phase 9 fan-in. It does not modify or extend the repository protocol and it does not select an evidence-gated database, workflow runtime, parser/OCR stack, model/provider, evaluator framework, observability backend, frontend framework, deployment class, or package manager.

## 1. Stable identity and protected-resource binding

`EntityIdentity` gives each `user`, `document`, `run`, `job`, `branch`, `attempt`, `evaluation`, `repair`, and `experiment` a stable opaque identity inside an authoritative `org_id + workspace_id` scope. `StableIdentitySet` carries the complete cross-stage identity vocabulary.

`ProtectedResourceIdentity`, `CommandEnvelope`, and `PersistenceRecord` require both tenant scope and a `ProvenanceBinding`. IDs are locators/correlation keys only; possession of an ID never authorizes access.

A protected resource is invalid when required `org_id`, `workspace_id`, resource identity, or provenance is absent. Server-side authorization resolves the tenant/resource independently of any replay cursor, artifact reference, provider reference, or user-supplied opaque identifier.

## 2. State transition, event, and revision contract

Every accepted authoritative transition uses `StateTransition` and has:

- stable `transition_id` and `mutation_id`;
- tenant/resource identity;
- `previous_revision` and `result_revision`;
- optional ownership epoch where the substrate exposes one;
- a timestamp.

Semantic invariant: for an accepted mutation, `result_revision` must be the authoritative successor of the expected resource revision; a stale expected revision is rejected rather than silently overwritten. JSON Schema enforces field presence/type; the storage/runtime implementation enforces cross-field monotonic/CAS semantics.

`EventEnvelope` requires the same transition identity plus `resource_id`, `result_revision`, and its own `event_revision`. A logical product event can represent only an authoritative committed transition or deterministic reconciliation of one. Sampled telemetry is never authoritative product-event history.

Physical delivery may be at-least-once. Consumers deduplicate logical projection by stable event/transition identity and authoritative revisions.

## 3. Replay cursor is not authority

`AuthorizedStream` contains the tenant/workspace/run scope authorized by the server. `ReplayCursor` contains only an opaque cursor token and `last_event_revision`; its schema forbids tenant/resource/run selectors.

A `ReplayRequest` therefore combines an already-authorized stream with a replay position. Implementations must reject a cursor supplied for a different authorized stream, and must never derive authorization, tenant, resource, or run identity from cursor contents.

## 4. Parsed-document and provenance contract

`SourceProvenanceRef` binds accepted parsed material to tenant/workspace/document identity, an immutable source artifact hash, and a renderer/page/region/node/table/cell/derived anchor when available.

Every `ParsedNode` has at least one provenance reference. `ParsedDocument` requires source artifact plus source provenance. Parsers must preserve available lineage and must not invent unavailable offsets/coordinates. Derived nodes retain parent provenance identities.

No parser/OCR winner is selected by this boundary.

## 5. Provider and evaluator metadata

`ProviderMetadata` and `EvaluatorMetadata` are opaque provenance abstractions. They allow provider/model capability, policy/catalog/pricing, evaluator version, rubric, and calibration identities to be recorded without selecting any concrete provider or evaluation framework.

## 6. Persistence ownership/revision/CAS

`PersistenceRecord` is tenant/provenance bound and revisioned. It covers documents, blobs, provenance, runs, jobs, branches, attempts, events, artifacts, evaluations, repairs, experiments, indexes, and publish attempts.

`CasWriteIntent` requires `expected_revision`, `expected_ownership_epoch`, and idempotent `mutation_id`. Implementations reject stale revision/ownership rather than accepting last-writer-wins overwrite. Immutable large material is referenced through `sha256` `ContentAddressRef`.

This is a storage contract, not a database selection.

## 7. Telemetry allowlist/default deny

`TelemetryEnvelope.attributes` accepts only the schema allowlist. Everything else is denied by default.

Raw document bodies, parser/extractor/provider payloads, prompts/generated content, request/response headers, cookies, bearer tokens, API keys, credentials, connection strings, arbitrary filesystem paths, and private backend object locations are excluded by default. Sensitive diagnostics belong in separately authorized/quarantined artifacts, with telemetry carrying only safe references/hashes.

## 8. Decision Research canonical registry and aliases

Registry: `docs/decisions/DECISION_RESEARCH_REGISTRY.v1.json`  
Schema: `decision-research-registry.schema.json`

Canonical Decision Research references use `dr://DR-####`. Each canonical reference resolves to exactly one source record. Source records remain untouched historical evidence and are pinned in the registry by repo-relative path plus source blob SHA.

Legacy identifiers are explicit aliases. If a legacy alias maps to multiple source records, its resolution is `AMBIGUOUS_REQUIRES_SOURCE` and bare use fails closed. The historical duplicate `DR-0001` is intentionally represented this way; source-qualified aliases resolve each record unambiguously.

Binding rules:

- a whole record is binding only when the exact source record supports that scope;
- mixed records use `SOURCE_LOCKED_SUBCLAIMS`; only exact source `LOCK` subclaims bind;
- `PENDING_EVIDENCE`, `NO_PREFERENCE`, candidate states and unresolved vendor/framework/runtime/parser/backend/package-manager choices remain non-binding;
- registry normalization never rewrites source evidence or turns an open choice into a winner.

## 9. Versioning

All package contracts use `contract_version = 1.0.0` and JSON Schema Draft 2020-12. Backward-incompatible shape/semantic changes require a new contract version. Consumers fail closed on unsupported major versions or unknown/ambiguous canonical decision references.

## 10. Reproducible validation

Reference validator: `validate_contracts.py`.

It checks schema structural validity, validates the registry instance against its schema, checks canonical ID/reference uniqueness and source resolvability, exercises legacy/collision resolution, runs representative negative contract cases, and can review the git changed-file set against the protocol/canonical denylist.

The reference runner uses the standards-oriented Python `jsonschema` implementation only for validation; this is task validation tooling, not a product/runtime/package-manager selection. Any conforming Draft 2020-12 validator may reproduce the schema checks.

Example from repository root:

```bash
python docs/production/contracts/v1/validate_contracts.py --base-ref main
```

The task does not introduce numeric performance/quality targets.
