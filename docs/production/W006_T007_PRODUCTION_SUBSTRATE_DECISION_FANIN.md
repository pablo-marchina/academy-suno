# W006-T007 — Production Substrate Evidence Fan-In / Decision Promotion Gate

`TASK_ID: W006-T007`  
`ATTEMPT_ID: A01`  
`DECISION_POSTURE: EVIDENCE_GATED`  
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`

## 1. Purpose and authority boundary

This artifact reconciles the accepted Phase 9 substrate evidence from `W006-T002-A01` through `W006-T006-A01` against:

- `SYSTEM/DECISION_RESEARCH_GATE.md`;
- `SYSTEM/PRODUCTION_CONTRACT.md`;
- accepted W005 benchmark methodology v002 (`SYSTEM/RESULTS/W005-T009-A02.md`, `dr://DR-5909`);
- W005 correction authority in `SYSTEM/RESULTS/W005-T011-A01.md` and `SYSTEM/RESULTS/W005-T012-A01.md`;
- the W006 Decision Research registry (`docs/decisions/DECISION_RESEARCH_REGISTRY.v1.json`).

It promotes only evidence-backed contracts/invariants. It does **not** infer a technology winner from a local implementation, a local Pareto singleton, documentation-only capability, or a successful reference harness.

Decision order is fixed:

1. non-compensatory hard-gate eligibility;
2. raw multidimensional evidence and declared uncertainty;
3. point Pareto only among eligible candidates when the comparison is actually representative;
4. promotion only when exact DR evidence, workload evidence, material-risk controls, confidence and reversal conditions exist;
5. otherwise preserve `NO_PREFERENCE`, `PENDING_EVIDENCE`, `DIAGNOSTIC_ONLY`, or equivalent.

No scalar utility is used in this fan-in. No business weights or practical-materiality thresholds are invented.

## 2. Accepted fan-in inputs

### W006-T002 — identity / tenancy / session / SSE security

Accepted evidence establishes a portable fail-closed security substrate with:

- stable external `(issuer, subject)` to internal principal mapping;
- server-authoritative tenant/workspace resolution and application-owned authorization;
- deny-by-default cross-tenant enforcement over API/data/object/event/trace surfaces;
- session and membership revocation, org/workspace switch invalidation, opaque server-bound replay cursors;
- same-origin cookie/CSRF/SSE reference topology;
- least-privilege service identities and default-deny telemetry/redaction.

Defined adversarial outcomes are zero for unauthorized cross-tenant success, revoked-session/membership resume success, prior-tenant access after switch, cross-tenant cursor replay, and credential-canary leakage. T002 explicitly leaves IdP, session store, data engine/RLS-equivalent, object/scanner, event backend, production proxy and cloud IAM choices evidence-gated.

Relevant Decision Research:

- `dr://DR-5401` → `docs/decisions/research/DR-5401-identity-authorization-tenancy.md`: security invariants supported; identity vendor remains `NO_VENDOR_PREFERENCE` / evidence-gated.
- `dr://DR-5402` → tenant-data-isolation research: data substrate remains evidence-gated.
- `dr://DR-5403` → secure-document/object-storage research: object/scanner winner remains evidence-gated.
- `dr://DR-0001#D2` and `#D3`: SSE default transport semantics and server-side authorization/redaction are exact locked subclaims.

### W006-T003 — durable state ↔ event consistency

Accepted evidence establishes an executable logical substrate and reusable common failure floor:

- revision/ownership CAS with stale-write rejection;
- stable mutation idempotency;
- authoritative state + immutable transition history;
- atomic state/transition/outbox persistence in the reference implementation;
- deterministic reconciliation and authoritative replay independent of telemetry/delivery acknowledgement;
- rejection of uncommitted events and idempotent duplicate/replay projection;
- tenant/run-scoped replay authorization;
- backup/restore and invariant audit.

Observed common harness: `14/14 PASS`, including zero silent stale overwrite, zero permanent logical event gaps after reconciliation, zero uncommitted-event projection, zero duplicate logical projection, zero cross-tenant replay, and 100% defined restart/replay/repair and backup/restore scenarios.

The SQLite implementation is reference evidence only and is **not** a production database winner.

Relevant Decision Research:

- `dr://DR-5910` → `docs/decisions/research/DR-0001-orchestration-durability-runtime.md`: production orchestration/runtime remains `PENDING_EVIDENCE`; the current stale whole-run behavior is not a valid production multi-replica authority.
- W005-T012 correction authority locks the logical state↔event consistency and idempotent accepted-output requirements independent of substrate.

### W006-T004 — secure ingestion + parser/OCR bakeoff

Accepted evidence establishes:

- controlled PDF quarantine/preflight with immutable SHA-256 provenance and `source_group_id`;
- fail-closed handling for invalid/encrypted/malformed/active-content inputs;
- explicit `OCR_REQUIRED` / `REVIEW_REQUIRED` routing;
- table-role ambiguity cannot silently become trusted evidence;
- raw parser/OCR latency/failure evidence with source-group accounting.

The observed comparison has `eligible_candidates = []`, `pareto_frontier = []`, and `decision_state = NO_PRODUCTION_PARSER_WINNER`. Source-original bytes were unavailable to the local candidate runner, source-group N was two, scanned structured-role recovery was insufficient, managed candidates were not executed, and production cost/operations evidence was absent.

Relevant Decision Research:

- `dr://DR-0014` → `docs/decisions/research/DR-0014-financial-document-parsing.md`: `PENDING_EVIDENCE`; no parser/OCR winner.

### W006-T005-A02 — workflow/runtime/shared-state bakeoff

Accepted comparative evidence executed custom/CAS, LangGraph `1.2.12` and DBOS `2.31.0` on the exact 3×3 Academy workload and common T003 failure floor. All three pass the defined hard gates; process-crash/recovery evidence distinguishes authoritative accepted-output idempotency from external duplicate provider attempts.

For the task-local point objectives `median_runtime_invocation_ms` and `duplicate_side_effect_attempts`, the local point Pareto set is `[custom_cas]`.

That singleton is **not** a production winner because the comparison held a local SQLite-backed acceptance topology constant and did not measure the intended multi-replica/shared-state production topology, production database/control plane, representative failover/network behavior, saturation/backpressure, operational recovery burden, production security/isolation, or externally billed provider cost.

Exact research record:

- `docs/decisions/research/DR-6005-runtime-shared-state-bakeoff-a02.md` (`DR-6005`; created after the v1 registry snapshot): `DECISION_STATE: PENDING_EVIDENCE`, `PRODUCTION_RUNTIME_LOCK: NONE`, `DATABASE_LOCK: NONE`.
- Prior runtime research canonical registry ref: `dr://DR-5910`.
- Benchmark decision method: `dr://DR-5909`.

Temporal remains an open conditional challenger when a production-topology hypothesis can materially change hard-gate eligibility or Pareto membership.

### W006-T006 — live cockpit same-contract bakeoff

Accepted evidence validates two framework-neutral rendering shells over the same canonical production contract and durable projector:

- state derives only from authoritative snapshot + accepted canonical events;
- reconnect rebuilds snapshot and replays newer events;
- static W004 recipient/cockpit is unavailable as fallback;
- cross-tenant source/event/trace projection success is zero in the defined suite;
- `FAIL` and `REVIEW_REQUIRED` remain explicit;
- accessibility/dynamic-update semantics are asserted;
- replay cursor is not authorization authority.

Decision posture remains `EVIDENCE_GATED_NO_WINNER`: no frontend framework, editor, package manager, UI runtime or deployment class is selected.

Relevant Decision Research:

- `dr://DR-0001#D1` → typed/versioned HTTP/OpenAPI boundary: `LOCK`.
- `dr://DR-0001#D2` → SSE default browser run feed with durable cursor/replay/snapshot semantics: `LOCK`.
- `dr://DR-0001#D3` → server-side authorization/redaction before serialization: `LOCK`.
- `dr://DR-0001#D4` → stable opaque source/citation references with authorized fetch: `LOCK`.
- same record D5/D6 → frontend framework and rich editor remain `PENDING_EVIDENCE`.

## 3. Decision promotion matrix

| Material decision surface | T007 disposition | Exact authority/evidence | Why | Reversal / recheck condition |
|---|---|---|---|---|
| Typed/versioned HTTP resource + command boundary | `LOCK — CARRY FORWARD` | `dr://DR-0001#D1`; W006-T001 contract; W006-T006 executed same contract | Exact DR lock plus integrated implementation evidence | Reopen only if an equivalent typed/versioned interface is materially safer/simpler while preserving idempotency/testability |
| SSE as default one-way browser run feed | `LOCK — CARRY FORWARD, CONDITIONAL ON DEPLOYMENT` | `dr://DR-0001#D2`; T002 security suite; T006 reconnect/projection evidence | Exact DR lock and application-level evidence | Reopen on production proxy/load/auth evidence showing unacceptable scaling/buffering/security burden, materially different event rate/size, or true bidirectional collaboration requirement |
| Server-side authorization/redaction; cursor is not authority | `LOCK — CARRY FORWARD` | `dr://DR-0001#D3`; `dr://DR-5401`; T002/T006 negative tests | Non-compensatory security invariant with zero defined unauthorized successes | Implementation mechanism may change; invariant only reopens if Production Contract changes |
| Stable tenant/provenance-bound source/citation identity | `LOCK — CARRY FORWARD` | `dr://DR-0001#D4`; T001 contracts; T004 source hash/source-group evidence | Exact DR lock and fail-closed ingestion evidence | Identifier schema may version; authorization/provenance binding remains mandatory |
| Application-owned identity/tenant authorization invariants | `LOCK — CARRY FORWARD` | W005-T012 authority + `dr://DR-5401` + T002 adversarial suite | Standards/research and executable fail-closed controls converge; no vendor is implied | Reopen model if mandated enterprise IdP/residency/sharing/regulatory requirements materially change resource ownership or assurance model |
| Same-origin cookie + CSRF browser credential topology | `REFERENCE DEFAULT / NOT A VENDOR LOCK` | `dr://DR-0001#D2` auth-topology caveat; `dr://DR-5401`; T002 executed evidence | Works with native SSE and passes defined revocation/switch/cursor controls; exact IdP/session adapter not selected | Re-evaluate when chosen IdP/proxy/BFF/deployment is known or if secure bearer/fetch-stream/BFF topology proves materially safer/simpler in the real slice |
| Durable logical state↔event consistency, CAS/idempotency/reconciliation/replay invariants | `LOCK — CARRY FORWARD` | W005-T012 H-02/M-04 correction authority; T003 `14/14`; `dr://DR-5910` records technology uncertainty | Required correctness contract is demonstrated independent of production backend | Substrate may change only if it proves equivalent invariants under the common harness; semantics do not relax for latency/cost |
| Production database / shared durable state technology | `PENDING_EVIDENCE` | T003 explicitly no winner; DR registry `dr://DR-5402`, `dr://DR-5910`; T005 DR-6005 database lock NONE | Reference SQLite/local topology is not multi-replica production evidence | Recheck after same common harness on production-capable multi-replica candidates plus failover/partition/recovery/security/ops/capacity evidence |
| Production workflow/runtime | `PENDING_EVIDENCE` | `dr://DR-5910`; DR-6005; T005-A02 | All mandatory candidates pass hard gates locally; local Pareto singleton is topology-limited | Recheck on intended shared-state topology with representative concurrency/failover/saturation/ops; run Temporal if it can change eligibility/frontier |
| Production parser/OCR | `NO_PRODUCTION_PARSER_WINNER` | `dr://DR-0014`; T004 decision | No eligible overall candidate; source-original/scanned-structure/managed-candidate evidence missing | Recheck on immutable source-original corpus + broader groups + structured OCR/document intelligence + identical raw cost/latency/failure capture |
| Fail-closed controlled PDF ingest/quarantine + provenance | `LOCK — CONTRACT/CONTROL` | W005-T012 secure-source authority; `dr://DR-0014`; T004 implementation/tests | Control protects source trust independent of parser winner | Mechanism may change only if same provenance/quarantine/ambiguity gates remain non-compensatory |
| Live cockpit durable projection/reconnect mechanics | `LOCK — CONTRACT/CONTROL` | `dr://DR-0001#D1-D4`; T006 green evidence; T003 authoritative replay | Same-contract rendering mechanics are discriminated without choosing UI framework | Reopen mechanics only on evidence of correctness/security/accessibility regression or materially better equivalent contract |
| Frontend framework / rich editor | `PENDING_EVIDENCE` | `dr://DR-0001` D5/D6; T006 `EVIDENCE_GATED_NO_WINNER` | Framework-neutral bakeoff proves mechanics, not framework economics/deploy fit | Same real slice comparison with build/dependency/runtime/deploy/auth/accessibility/CI evidence |
| Identity provider | `NO_PREFERENCE / PENDING_EVIDENCE` | `dr://DR-5401`; T002 | Application invariants proven, vendor requirements/bakeoff absent | Decide after Suno SSO/SCIM/residency/procurement requirements + identical candidate flow |
| Data isolation engine / RLS-specific choice | `PENDING_EVIDENCE` | `dr://DR-5402`; T002/T003 | Tenant/CAS semantics proven at application/reference level, production engine unselected | Real data-engine bakeoff with tenant isolation, migrations, concurrency/failover/recovery/security/ops |
| Object store / scanner / IAM implementation | `PENDING_EVIDENCE` | `dr://DR-5403`; T002/T004 | Quarantine/provenance controls exist; provider/infrastructure not compared | Identical controlled-upload/security/retention/scanning workload on viable production candidates |
| Observability backend / collector topology / sampling / retention | `NO_PREFERENCE / PENDING_EVIDENCE` | `dr://DR-0701` exact lock scope; W005-T011/T012 correction | Only W3C/OTel semantics + OTLP-compatible portable export boundary are locked | Backend/topology promotion requires same-slice operational evidence and explicit retention/privacy/cost requirements |
| Deployment class / cloud/runtime topology | `NO_PREFERENCE` | `dr://DR-5008`; W005-T012 | Deployment invariants are locked; hosting class is not | Recheck after selected substrate dependency graph with load/recovery/security/operational evidence |
| Reliability/capacity/SLO/RTO/RPO numeric targets | `PENDING_EVIDENCE / UNKNOWN` | `dr://DR-5009`; Production Contract; W005-T012 | Method can bind; values cannot be invented | Freeze only from representative measured load/recovery evidence or explicit external owner requirements |
| Python/JS package managers, task graph, repository topology | `PENDING_EVIDENCE` | `dr://DR-5914`; W005-T011/T012 H-01 correction | Supply-chain controls can bind without freezing topology/package managers | Decide after real dependency graph and clean-build/CI/cache/deploy evidence; repository migration requires positive evidence |
| Static W004 cockpit as production/final-evidence fallback | `PROHIBITED; DIAGNOSTIC_ONLY / COUNTERFACTUAL` | W005-T011 H-03; W005-T012 H-03 correction | Single-real-product-path requirement forbids static substitution | Reversal requires explicit Production Contract change; not a technology bakeoff decision |

## 4. Hard-gate audit

This fan-in applies non-compensatory gates before any preference:

- material production/default winner without exact DR evidence: `0`;
- hard-gate violator retained as eligible: `0`;
- scalar utility or fixed business weights used without representative evidence: `0`;
- parser/OCR winner inferred from digital-only or reconstructed local evidence: `0`;
- runtime/database winner inferred from T005-A02 local `[custom_cas]` Pareto point: `0`;
- frontend/framework winner inferred from framework-neutral shell evidence: `0`;
- identity/data/object/observability/deployment/package-manager vendor winner inferred from portable controls: `0`;
- static/synthetic cockpit promoted as production/final-evidence fallback: `0`;
- W005-T011/T012 state↔event, retry/idempotency, cursor, OTel-scope, repository-topology and static-fallback corrections weakened: `0`.

## 5. Cross-task reconciliation

### T002 × T006 — SSE/browser security

The evidence is mutually compatible: T002 proves the reference browser credential/revocation/cursor security contract; T006 proves both rendering shells can consume the same canonical API/events without making cursor position authority. T007 carries the SSE/default contract and server-side authorization locks from `dr://DR-0001`, while keeping the concrete IdP/session store/framework adapter open.

### T003 × T005 — durable state/events and runtime

T003's `14/14` common failure floor is the substrate-independent correctness gate. T005 demonstrates custom/CAS, LangGraph and DBOS can all satisfy the defined local candidate hard gates while showing different latency/duplicate-side-effect observations. Because the production topology itself is missing, T007 does not reinterpret `[custom_cas]` as a technology winner.

### T004 × production source trust

T004 strengthens the invariant that parsing success cannot increase trust by itself. `pdfplumber` digital reconstruction performance is useful raw evidence but cannot compensate for scan-role failures, missing source-original execution, or missing broader/managed-candidate evidence. The correct production state remains `NO_PRODUCTION_PARSER_WINNER`.

### W005-T011/T012 corrections preserved

T007 preserves all material corrections:

- repository topology is evidence-gated; only “no migration without evidence” is invariant;
- durable state ↔ product-event logical consistency is mandatory;
- static W004 cockpit is diagnostic/counterfactual only;
- SSE must preserve connect/resume/revocation/org-switch/cross-tenant cursor security;
- DR references are exact/canonical where registered and exact repo-relative paths are used for records added after the registry snapshot;
- OTel lock remains limited to W3C trace context + OTel semantic/instrumentation + OTLP-compatible export boundary;
- remote execution is at-least-once with idempotent local accepted output, immutable attempt identity, late/stale rejection and duplicate-side-effect accounting;
- cursor position never independently selects tenant/resource/run authority.

## 6. Production Contract impact

This is a **decision/evidence fan-in**, not a production qualification task. It advances confidence and implementation authority for portions of PROD-001/002/003/004/006/011/014/015, but it does not make any row globally `PASS`.

Key remaining blockers include:

- selected production shared database/event/runtime topology and distributed qualification (`PROD-003/006/013/016`);
- production parser/OCR selection and real-source corpus proof (`PROD-004/005/007` where parsing is involved);
- real vertical-slice framework/infrastructure integration and adversarial security (`PROD-001/002/011/014`);
- provider/model/adaptive-policy promotion and real provider path (`PROD-005/010`);
- representative reliability/capacity/recovery plus deployment evidence (`PROD-013/016`);
- final live single-product-path evidence (`PROD-017`).

`PRODUCTION_READY_FROM_T007: FALSE`.

## 7. Evidence-use rules for downstream T008/T009

1. Treat `LOCK — CARRY FORWARD` rows as interface/correctness/security constraints, not permission to choose an unbenchmarked vendor.
2. Reuse T003's common failure harness or a transport-neutral equivalent preserving every assertion for any database/event/runtime candidate.
3. Do not use T005 local Pareto membership as a production topology result.
4. Do not allow parser text recall/latency to compensate for structured-role/provenance hard-gate failure.
5. Keep raw side-effect attempts/cost separate from authoritative accepted-output idempotency.
6. Keep browser cursor state separate from authorization/stream selection.
7. Final frontend must consume authoritative live state/events; static W004 artifacts remain diagnostic/counterfactual only.
8. Any new material winner requires a Decision Research record with exact evidence, confidence and reversal conditions before freeze.
9. Utility/scalar weighting remains forbidden until representative human/business evidence is frozen before outcomes and sensitivity is stable.

## 8. Fan-in conclusion

The Phase 9 substrate work has produced a strong, executable **contract floor** but not enough representative production-topology evidence to justify most technology locks.

Promoted/carry-forward authority is therefore concentrated in:

- typed/versioned HTTP/OpenAPI semantics;
- SSE default one-way run feed with durable replay/snapshot semantics;
- server-side authorization/redaction and tenant/provenance binding;
- application-owned fail-closed tenant authorization invariants;
- durable state↔event logical consistency, CAS/idempotency/reconciliation/replay semantics;
- controlled fail-closed source ingestion/provenance requirements;
- exact stable 3×3/lossless/idempotent acceptance semantics;
- live cockpit authoritative projection/reconnect mechanics;
- static W004 exclusion from production/final evidence.

Technology choices intentionally remain open where the evidence does not yet distinguish production candidates. This is the required output of an evidence-driven promotion gate, not an incomplete decision.