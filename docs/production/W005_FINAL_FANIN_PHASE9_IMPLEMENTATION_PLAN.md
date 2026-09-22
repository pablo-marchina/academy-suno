# W005 Final Fan-in & Phase 9+ Implementation Authority Plan

`ARTIFACT_ID: W005-T012-FINAL-FANIN-V001`

`TASK_ID: W005-T012`
`ATTEMPT_ID: A01`
`ROLE: Synthesizer + Project Auditor + Orchestrator Support`
`OBSERVED_STATE_VERSION: 0047`
`OBSERVED_MAIN_SHA_AT_START: d522e6cbbcbdfb067c41242e79b3be16594b5981`
`STATUS: FINAL_FANIN_COMPLETE`
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`
`PHASE9_IMPLEMENTATION_STARTED: FALSE`

## 1. Purpose and authority boundary

This artifact reconciles accepted `W005-T010-A01` with accepted `W005-T011-A01` and converts their combined evidence into the implementation authority proposed for Phase 9+.

It does **not** modify canonical coordination state, does not authorize a production-ready claim, and does not convert unresolved material choices into winners. Where this artifact conflicts with T010 on the specific red-team findings below, this artifact is the corrected worker recommendation for Orchestrator acceptance.

The governing rules remain:

1. single real product path;
2. non-compensatory critical gates;
3. production claims require production-equivalent evidence;
4. material alternatives require DRG evidence before production/default promotion;
5. `NO_PREFERENCE` and `PENDING_EVIDENCE` are valid outcomes;
6. W004 mechanics/static artifacts are historical baselines and diagnostics, not substitutes for production evidence.

## 2. Final normalized decision authority

### 2.1 Corrected decisions from T011

| Area | Final T012 state | Final authority | Reversal / promotion condition |
|---|---|---|---|
| Repository topology | `PENDING_EVIDENCE` | **LOCK only the invariant:** no repository migration/topology layer without evidence. Existing repository is the current baseline/counterfactual, not an evidence-won immutable topology. | Real selected dependency/deploy graph + DRG-compliant topology/CI benchmark may justify keeping or changing topology. |
| Static W004 cockpit | `DIAGNOSTIC_ONLY / COUNTERFACTUAL` | May be retained for regression comparison and historical evidence inspection. It is **not** a production route, recipient fallback, or final-evidence fallback. | It may be retired after equivalent diagnostic value exists elsewhere; it may never be promoted by convenience alone. |
| State ↔ durable product events | `LOCK` invariant; implementation `PENDING_EVIDENCE` | Every accepted authoritative state transition must have an auditable, crash-consistent logical product-event representation. Substrate must prove atomic state+outbox semantics or deterministic reconciliation with equivalent guarantees. | Selected state/event substrate passes the common failure-injection contract in §4. |
| SSE browser feed | `LOCK` as default one-way transport, conditional | SSE remains default server→browser run transport only. Security/credential topology must pass connect/resume/revocation/org-switch/cross-tenant-cursor tests. SSE is not the durability substrate. | Reopen if representative proxy/load/auth evidence materially fails. |
| Decision Research references | `LOCK` reference rule | Bare duplicate numeric IDs are not sufficient. Until a normalized registry exists, every relied-on decision record is referenced by exact repo-relative path (and commit/blob identity when freezing evidence). | A globally unique registry/ID migration can replace path-qualified references without losing history. |
| Observability boundary | `LOCK` narrowly | W3C Trace Context + OpenTelemetry semantic/instrumentation API + OTLP-compatible export boundary are locked. Collector topology, processors, sampling, retention and backend remain evidence-gated. | Representative evidence may change implementation while preserving portable correlation/export semantics. |
| Provider/job execution | `LOCK` semantics | Remote execution is treated as at-least-once; local acceptance is idempotent. Attempts have immutable identity, late-result rules, duplicate-delivery handling and duplicate-cost accounting. | A stronger substrate may simplify implementation, but cannot weaken accepted-output uniqueness/auditability. |
| Event replay cursor | `LOCK` security invariant | Cursor is authorized together with tenant/resource/run stream. Cursor-only lookup may not select another tenant/resource. Prefer opaque or run-stream-scoped cursor representation. | Representation may change if equivalent authorization/non-enumerability properties are proven. |

### 2.2 T010 locks upheld without material change

The following remain valid architectural/control locks, subject to their already-declared implementation boundaries:

- typed/versioned HTTP resources/commands and OpenAPI-described boundary;
- server-side authorization/redaction before serialization;
- stable external principal mapping to internal identity plus app-owned deny-by-default authorization;
- first-class tenant/workspace/resource binding and independent data-plane isolation;
- private object lifecycle with quarantine → validate → promote and immutable source provenance;
- parser-independent canonical provenance and fail-closed source trust;
- stable exact 9-way workflow identity, lossless join, resume, and retry/repair separation;
- current `SQLiteRunStore` barred from multi-replica production authority in its current form;
- deterministic safety envelope outside adaptive optimization;
- versioned/auditable provider catalog/policy/config/rollback identity;
- non-compensatory eval hard gates and blind independent human-calibration method;
- model judges as calibrated secondary sensors only;
- W005 benchmark method: hard gates → raw multidimensional metrics → uncertainty → point Pareto → no forced winner;
- product events remain distinct from sampled telemetry;
- raw sensitive GenAI content off by default in telemetry and bounded metric label allowlist;
- replaceable API / decoupled long work / shared durable state / explicit backpressure/idempotency / health / migrations / restore proof;
- GitHub Actions plus full-SHA third-party actions, least privilege, authoritative lockfiles after manager selection, SBOM and artifact provenance/attestation.

### 2.3 Choices explicitly not frozen

These remain `PENDING_EVIDENCE` or `NO_PREFERENCE` until a DRG-valid representative comparison distinguishes them:

- API framework;
- frontend framework/editor;
- identity provider/vendor and object-store/scanner vendor;
- relational/data engine and PostgreSQL-specific RLS choice;
- parser/OCR route/winner;
- workflow/runtime/shared-state implementation;
- provider/model overall winner and learned routing default;
- external eval framework;
- audience thresholds;
- observability backend, collector topology/processors/sampling/retention;
- deployment class;
- SLO/capacity/RTO/RPO numeric targets;
- Python/JS package managers;
- repository topology and Nx/Turborepo/task-graph layer;
- local environment wrapper and SBOM encoding where no consumer requirement distinguishes alternatives;
- scalar/business utility weights.

## 3. Explicit disposition of every T011 finding

| Finding | T012 disposition | Implementation gate / owner path | Status after T012 |
|---|---|---|---|
| `H-01` repository strategy status inflation | T010 topology `LOCK` is withdrawn. Only `NO_REPOSITORY_MIGRATION_WITHOUT_EVIDENCE` is locked; topology remains `PENDING_EVIDENCE`. | Phase 9 toolchain/topology task evaluates actual selected graph before any topology migration. | `CORRECTED_IN_AUTHORITY`; topology evidence still open. |
| `H-02` state↔event consistency gap | Add explicit crash-consistency contract in §4 and common failure harness. Substrate promotion blocked until it passes. | State/event contract + runtime/shared-state tasks; Data/Architecture/Reliability ownership. | `CARRIED_AS_P0_IMPLEMENTATION_BLOCKER_UNTIL_PASS`. |
| `H-03` static W004 cockpit fallback drift | Reclassify static cockpit to `DIAGNOSTIC_ONLY / COUNTERFACTUAL`; forbid production/final-evidence fallback. Add final-evidence binding contract in §6. | Vertical slice + final evidence tasks; UX/Auditor ownership. | `CORRECTED_IN_AUTHORITY`. |
| `M-01` SSE browser credential topology | Keep SSE default but make auth/session integration proof mandatory: connect/resume/revocation/auth-expiry/org-switch/cross-tenant cursor. | Identity/tenancy/SSE security task. | `CARRIED_TO_REQUIRED_SECURITY_GATE`. |
| `M-02` ambiguous DR identifiers | Exact repo-relative path is mandatory reference now; Phase 9 creates global unique DR registry/namespacing before new production defaults rely on bare IDs. | Contract/traceability task + Orchestrator/Auditor review. | `CONTROLLED_NOW`; normalization work still required. |
| `M-03` OTel lock too broad | Narrow lock to W3C + OTel semantic/instrumentation + OTLP-compatible export boundary. Collector topology/processors/sampling/retention/backend remain open. | Observability integration + backend DRG task. | `CORRECTED_IN_AUTHORITY`. |
| `M-04` retry/idempotency under-specified | Add explicit at-least-once execution + idempotent accepted-output contract in §5. | Runtime/shared-state task + provider/adaptive task. | `CARRIED_AS_REQUIRED_RUNTIME_GATE`. |
| `L-01` event cursor scope | Cursor always validated with authorized stream; cursor alone cannot select tenant/run. Add adversarial negative tests. | Contract/schema + identity/live-event test tasks. | `CONTROLLED_BY_REQUIRED_CONTRACT_AND_TEST`. |

No T011 material finding is silently closed by prose. Items depending on runtime evidence remain implementation blockers until their defined gates pass.

## 4. State ↔ durable event consistency contract

This contract is implementation-neutral and is a hard entry condition for promoting the production state/event substrate.

### 4.1 Logical invariants

For every accepted authoritative state transition:

1. a stable `transition_id` exists;
2. the authoritative resource/run revision monotonically advances or is rejected by ownership/CAS rules;
3. a corresponding logical product event exists with tenant/workspace/resource/run identity, transition identity, resulting revision, event type/schema version and trace correlation;
4. a consumer-visible event must never represent a state transition that is not authoritative/committed;
5. a committed state transition must not become permanently invisible to the event/replay plane;
6. physical delivery may be at-least-once; logical projection is idempotent;
7. replay/snapshot truth is derived from authoritative persisted state/event history, never from sampled telemetry;
8. repair/reconciliation is deterministic, auditable and tenant-scoped.

### 4.2 Allowed implementation families

A candidate may satisfy the contract using, for example:

- state + transactional outbox in the same durable transaction;
- transactionally coupled append/event log;
- CDC/outbox with proven ownership/ordering semantics;
- another mechanism with equivalent proof;
- deterministic reconciliation keyed by authoritative revision if atomic coupling is not available.

T012 does not select among these families without representative substrate evidence.

### 4.3 Required failure-injection matrix

The chosen substrate must persist raw evidence for at least these defined cases:

- state commit succeeds and publisher/event emission crashes before delivery;
- event/outbox processing is retried after worker/publisher crash;
- duplicate delivery of the same logical event;
- out-of-order physical delivery;
- consumer crash after side effect but before acknowledgement/checkpoint;
- consumer restart from prior cursor;
- stale cursor requiring replay or explicit snapshot fallback;
- reconciliation after an intentionally created state/event gap;
- attempted event/projection without corresponding authoritative committed state;
- concurrent same-run transitions with stale revision/ownership;
- telemetry exporter/backend unavailable while product state/event path continues;
- cross-tenant cursor supplied to an otherwise authorized endpoint.

### 4.4 Acceptance gates

Before substrate promotion:

- silent stale overwrite accepted = `0`;
- authoritative transitions permanently missing from logical replay after reconciliation procedure = `0`;
- consumer-visible logical events without corresponding authoritative committed transition = `0`;
- duplicate logical projection after defined duplicate deliveries/restarts = `0`;
- cross-tenant replay success in defined tests = `0`;
- all defined restart/replay/repair scenarios = `100% PASS` before production claim;
- raw sequence/revision/reconciliation evidence is persisted.

No invented latency or reconciliation-time SLO is introduced here.

## 5. Provider/job attempt and idempotent acceptance contract

Exactly-once remote provider invocation is not assumed. The production workflow must tolerate at-least-once delivery/execution while accepting each logical branch result at most once for a given accepted generation/revision.

Required semantics:

- immutable internal `attempt_id` per execution attempt;
- stable `job_id` / `branch_id` and source/run revision linkage;
- request/config digest covering provider/model/catalog/policy/prompt/retrieval/parser/evaluator/repair versions that materially affect the attempt;
- external provider request/call identity persisted when available, but never required for internal correctness;
- accepted output commit protected by uniqueness + revision/ownership/CAS semantics;
- duplicate worker delivery or retry may execute remotely again, but cannot create duplicate accepted branch state;
- a late result from a superseded/cancelled/failed ownership epoch is recorded as late evidence and cannot silently overwrite a newer accepted state;
- all observed attempts, including duplicates/retries/timeouts, contribute to reliability and cost accounting where usage/cost evidence is available;
- timeout-after-remote-success-before-local-commit is a mandatory failure-injection case;
- repair attempt identity is distinct from transport retry identity.

Acceptance gates:

- duplicate accepted branch outputs caused by duplicate delivery/retry = `0`;
- stale/late result overwriting newer accepted output = `0`;
- accepted output missing attempt/config provenance = `0`;
- provider/policy/catalog identity missing from accepted adaptive run = `0`;
- duplicate/retry attempts omitted from available usage/cost accounting = `0` for the defined harness.

## 6. Final evidence identity contract

Production/final evidence must be generated from the same real path used by the product. A screen, video frame or exported evidence bundle used for a production claim must be traceable to live authoritative identities.

Minimum evidence manifest for an accepted final run:

- source/document immutable hash + document version/object identity;
- organization/workspace/resource identity (redacted/pseudonymized for public evidence when needed, while preserving audit linkage);
- `run_id` and run revision;
- branch/job/attempt identities for the 9-way path;
- event stream/cursor/revision identities used by the displayed live projection;
- provider/model identity plus catalog/policy version;
- parser/provenance schema version;
- prompt/retrieval/config identity where applicable;
- evaluator config/version and repair policy/version;
- experiment/dataset identity for evaluated claims;
- trace/build/commit/deploy identity sufficient to correlate the executable artifact;
- authoritative persistence proof for the run and replay/snapshot used by the UI.

Hard rules:

- static W004 cockpit/manifests may not substitute for the live recipient route;
- fixtures/synthetic/counterfactual views must be visibly labeled and excluded from production-claim evidence;
- stale/snapshot-required UI state cannot be represented as current live truth;
- final technical video remains `<=5:00`, but it demonstrates the same product path rather than a parallel demo architecture.

## 7. Decision Research traceability normalization

T011 found duplicate `DR-0001` identifiers. Until the repository is normalized, T012 establishes this safe reference rule for implementation work:

`DR_REF = <exact repo-relative decision-record path>[@<evidence commit/blob>]`

Rules:

1. no new implementation decision may cite a bare ambiguous number such as only `DR-0001`;
2. promotion records cite exact decision-record path(s), representative benchmark artifact(s), requirement/risk refs and reversal conditions;
3. a Phase 9 traceability task creates a globally unique registry/namespaced ID scheme and maps existing records without destroying history;
4. renaming files is optional if the registry provides stable unique IDs; references must remain resolvable;
5. a material production/default promotion remains blocked when its exact evidence record cannot be uniquely identified.

This closes ambiguity for immediate referencing without pretending the historical registry is already clean.

## 8. Production Contract implementation coverage

No row below is a production PASS. This table identifies the implementation/evidence path required to earn one.

| PROD | Phase 9+ implementation/evidence path | Required gate class | Current T012 state |
|---|---|---|---|
| PROD-001 | identity/tenant/authz + data/object/event isolation + cross-tenant adversarial suite | Security hard gate | `IMPLEMENTATION_REQUIRED` |
| PROD-002 | typed/versioned API, input validation, idempotent commands, timeout/backpressure | Contract + deterministic + runtime | `DESIGN_MAPPED` |
| PROD-003 | shared durable state + state/event contract + backup/restore | Reliability/data hard gate | `P0_EVIDENCE_BLOCKER` |
| PROD-004 | private object quarantine/validation/hash/provenance/retention implementation | Security/source evidence | `IMPLEMENTATION_REQUIRED` |
| PROD-005 | real provider path in recipient-facing vertical slice | Runtime/live evidence | `IMPLEMENTATION_REQUIRED` |
| PROD-006 | exact 9-way durable workflow, resume, lossless join, retry≠repair, idempotent acceptance | Deterministic + failure injection | `P0_EVIDENCE_BLOCKER` |
| PROD-007 | production evaluator config + hard gates + calibrated secondary sensors | Eval evidence | `IMPLEMENTATION_REQUIRED` |
| PROD-008 | independent blind human calibration + held-out replication | Human evidence | `EXTERNAL/HUMAN_EVIDENCE_REQUIRED` |
| PROD-009 | PR deterministic lane + offline paired experiments + release blocking | CI/eval evidence | `IMPLEMENTATION_REQUIRED` |
| PROD-010 | versioned adaptive policy inside deterministic safety envelope | Benchmark + shadow/canary evidence | `PENDING_REPRESENTATIVE_EVIDENCE` |
| PROD-011 | real live cockpit from durable events/replay/snapshot; SSE auth/cursor tests | Live-product + security | `IMPLEMENTATION_REQUIRED` |
| PROD-012 | portable correlated telemetry + backend selection evidence | Observability evidence | `IMPLEMENTATION_REQUIRED` |
| PROD-013 | load/failure/restart/restore/capacity qualification | Reliability/performance | `IMPLEMENTATION_REQUIRED` |
| PROD-014 | threat model, least privilege, authz/tenant/upload/secrets/dependency evidence | Security | `IMPLEMENTATION_REQUIRED` |
| PROD-015 | DRG-compliant exact path/registry + raw benchmarks + reversal conditions | Decision-quality gate | `TRACEABILITY_NORMALIZATION_REQUIRED` |
| PROD-016 | reproducible manifests/locks/build/deploy/migrations/runbook | Build/deploy evidence | `IMPLEMENTATION_REQUIRED_AFTER_SUBSTRATE_SELECTION` |
| PROD-017 | final live evidence bound to source/run/job/attempt/event/config/build identities | Final audit hard gate | `BLOCKED_ON_IMPLEMENTATION_AND_EVIDENCE` |

## 9. Phase 9+ exact proposed next-wave task graph

The following IDs are **proposed worker task IDs for the Orchestrator to materialize** after accepting/integrating T012. They do not become canonical merely by appearing here.

```text
W006-T001  Contract/schema + DR traceability normalization
   |
   +--> W006-T002  Identity/tenancy/session/SSE security substrate
   +--> W006-T003  Durable state↔event consistency substrate + failure harness
   +--> W006-T004  Secure source ingestion + parser/OCR real-corpus bakeoff
   +--> W006-T005  Workflow/shared-state + at-least-once/idempotent-attempt bakeoff
   +--> W006-T006  Frontend/editor same-slice live-cockpit bakeoff

T002,T003,T004,T005,T006
   \    |    |    |    /
        v
W006-T007  Production substrate evidence fan-in / decision promotion gate
        |
        v
W006-T008  Reproducible toolchain + repository-topology evidence freeze
        |
        +-------------------+
        |                   |
        v                   v
W006-T009  Real production vertical slice
                            W006-T010 Eval/human-calibration foundation
        |                   |
        +---------+---------+
                  v
W006-T011 Provider/model/adaptive runtime benchmark & promotion
        |
        +--------------+
        |              |
        v              v
W006-T012 Observability/live-ops integration
                       |
        +--------------+
        v
W006-T013 Security + reliability + capacity + recovery qualification
        |
        v
W006-T014 Final live evidence + production-claim audit
```

### W006-T001 — Contract/schema + DR traceability normalization

**Role:** API/Domain Architect + Evidence Auditor.

**Outputs:** versioned resource/command schemas; stable org/workspace/user/document/run/job/branch/attempt/eval/repair/experiment IDs; event envelope/revision/cursor contract; parsed-document/provenance contract; provider/evaluator metadata; persistence ownership/CAS contract; telemetry allowlist; unique DR registry/namespaced references.

**Hard acceptance:** protected resource contracts cannot omit tenant/provenance identity; critical schema violation promoted = `0`; cursor cannot select tenant/resource by itself; event/state contract fields required; exact decision references globally unambiguous.

**Parallelism:** unlocks T002–T006.

### W006-T002 — Identity/tenancy/session/SSE security substrate

**Role:** Security + Identity + API.

**Work:** principal mapping; deny-by-default app authz; authoritative workspace resolution; candidate data/object isolation; chosen browser credential topology for API/SSE; session revocation/org switching; separate runtime/migrator/worker/backup identities.

**Hard acceptance:** cross-tenant unauthorized success across API/data/object/event/trace defined tests = `0`; connect/resume with revoked session/membership denied; org-switch does not retain prior-tenant event/source access; cross-tenant cursor replay success = `0`; secret/credential canary leak = `0`.

**Decision boundary:** IdP/data/object vendors remain evidence-gated unless DRG evidence supports promotion.

### W006-T003 — Durable state↔event consistency substrate + failure harness

**Role:** Data + Reliability Architecture.

**Work:** implement candidate shared durable state + event/outbox/reconciliation semantics; common harness from §4; backup/restore design; append/audit history where applicable.

**Hard acceptance:** all §4 defined failure scenarios pass; stale same-run silent overwrite = `0`; permanent logical event gap after reconciliation = `0`; event without authoritative transition = `0`; duplicate logical projection = `0`; defined restart/replay/repair scenarios `100% PASS` before production claim.

**Decision boundary:** database/workflow/event technology winner remains evidence-gated until common harness results exist.

### W006-T004 — Secure source ingestion + parser/OCR real-corpus bakeoff

**Role:** Data/Document Intelligence + Eval.

**Work:** controlled upload/quarantine; real public financial corpus; local/managed parser candidates behind canonical schema; digital/scanned/malformed/encrypted/table-heavy cases; raw outputs/resource/cost/latency observations.

**Hard acceptance:** accepted evidence missing source hash/provenance = `0`; ambiguous table/OCR role promoted as trusted evidence = `0`; preservation/source-group metrics reported raw; candidate decision uses hard-gate eligibility + uncertainty + Pareto, not arbitrary scalar score.

### W006-T005 — Workflow/shared-state + at-least-once/idempotent-attempt bakeoff

**Role:** Workflow/Runtime + Reliability + Provider Platform.

**Work:** exact 9-way workload over materially different runtime/shared-state candidates; immutable attempt identity; duplicate delivery; timeout-after-remote-success-before-commit; worker crash/restart; ownership/CAS/lease semantics; late results and duplicate-cost accounting.

**Hard acceptance:** 9/9 accepted branch coverage; accepted join loss/duplication = `0`; duplicate accepted output = `0`; stale/late overwrite = `0`; defined restart/resume scenarios `100% PASS` before production claim; raw overhead/ops burden persisted.

### W006-T006 — Frontend/editor same-slice live-cockpit bakeoff

**Role:** Product Frontend + UX + Security.

**Slice:** authenticated workspace → upload/source → live run → 3×3 → citations → eval/repair → reconnect/replay/snapshot.

**Hard acceptance:** candidate consumes same production API/event contract; live state derives only from current durable state/events; static W004 path unavailable as recipient fallback; cross-tenant source/event/trace projection success = `0`; failed/review-required cells remain explicit; accessibility/dynamic-update evidence persisted.

### W006-T007 — Production substrate evidence fan-in / decision promotion gate

**Role:** Synthesizer + Project Auditor + Production Architect.

**Dependencies:** T002–T006.

**Work:** apply DRG + W005-v002 decision method; promote only evidence-supported defaults; retain `NO_PREFERENCE/PENDING_EVIDENCE` where alternatives remain Pareto/incomparable; bind exact DR refs/reversal conditions.

**Hard acceptance:** no material production/default winner lacking exact DR evidence; no hard-gate violator eligible; no scalar utility used without representative utility evidence; T011/T012 contracts preserved.

### W006-T008 — Reproducible toolchain + repository-topology evidence freeze

**Role:** Developer Platform + Supply Chain + Release Engineering.

**Dependencies:** T007 selected real dependency/deploy topology.

**Work:** benchmark package managers on actual graph; decide repository topology/task graph only from measured need; authoritative manifests/locks; canonical commands; full-SHA actions; least privilege; lock-derived caches; SBOM; attestation/provenance verification.

**Hard acceptance:** clean locked install/build/test PASS; movable third-party release Actions = `0`; unnecessarily broad release token permissions = `0`; releasable artifact has verifiable SBOM + provenance; repository migration occurs only with DRG evidence.

### W006-T009 — Real production vertical slice

**Role:** Full-stack Production Integration.

**Dependencies:** T007 + T008.

**Path:** auth → workspace → secure upload → parse/provenance → durable 9-way workflow → eval/repair → aggregate → durable events → live cockpit.

**Hard acceptance:** current live run correlated by source/run/job/attempt/event identities; accepted provenance missing = `0`; 9/9 with zero accepted loss/duplication; arbitrary untrusted server filesystem path route = `0`; replay/reconnect PASS; telemetry outage does not corrupt/block product result; tenant adversarial suite remains PASS.

### W006-T010 — Eval/human-calibration foundation

**Role:** Eval Science + Human Calibration.

**Dependencies:** T001 + source/eval schema stability; can progress in parallel with late integration work.

**Work:** versioned DEV/CALIBRATION/HELD_OUT source-group partitions; two blind independent human streams per item by default or justified equivalent; agreement/adjudication; secondary judge calibration; paired baseline/candidate experiments.

**Hard acceptance:** automated/model-only label called human gold = `0`; hard-gate compensation = `0`; audience thresholds remain `DIAGNOSTIC_ONLY` until independent calibration + held-out replication.

**External dependency:** actual human annotation is a human/external evidence requirement; absence blocks strong audience-threshold claims but must not be disguised as completion.

### W006-T011 — Provider/model/adaptive runtime benchmark & promotion

**Role:** AI Runtime + Eval + FinOps.

**Dependencies:** T009 + T010 evidence contracts.

**Work:** refresh exact provider/model/pricing/lifecycle facts; representative same-corpus comparisons; static candidates → deterministic cascade → learned shadow router if justified → bounded canary only if evidence supports it.

**Hard acceptance:** hard-gate violating output accepted for cost/latency = `0`; capability-ineligible fallback = `0`; invalid auth/config/tenant/policy blindly retried = `0`; accepted run missing policy/catalog/pricing identity = `0`; canary critical failure rollback behavior PASS; forced winner on unresolved Pareto tradeoff = `0`.

### W006-T012 — Observability/live-ops integration

**Role:** Observability + SRE + Security.

**Dependencies:** T009; backend selection remains DRG-gated.

**Work:** W3C propagation; OTel instrumentation; OTLP-compatible export; provider/eval/repair spans; bounded metrics; authorized cockpit trace links; backend comparison on real workload.

**Hard acceptance:** raw credentials/secrets in telemetry = `0`; raw private content emitted by default = `0`; high-cardinality tenant/run/job IDs as default metric labels = `0`; controlled 9-branch traceability PASS; telemetry backend/export outage leaves product path healthy; backend/collector topology not promoted without evidence.

### W006-T013 — Security + reliability + capacity + recovery qualification

**Role:** Security Red Team + SRE + Project Auditor.

**Dependencies:** T009 + T011 + T012.

**Work:** threat model; authz/upload/tenant/secret/supply-chain adversarial suites; concurrency ladder/arrival staircase/burst/soak/saturation; restart/resume; state/event repair; backup/restore; deployment/migration rollback.

**Hard acceptance:** all defined security zero-tolerance gates pass; restart/resume and backup/restore defined scenarios `100% PASS`; publish measured saturation interval and raw p50/p95/p99/queue/throughput/resource/cost observations; no invented supported-user count/SLO/RTO/RPO.

### W006-T014 — Final live evidence + production-claim audit

**Role:** Independent Auditor + Demo/Technical Communication.

**Dependencies:** T010 + T011 + T013 and all applicable contract gates.

**Work:** map `PROD-001..017` to actual evidence; verify final-evidence identity contract; regenerate final <=5:00 technical video from same real product path; verify no static/fake fallback; classify every remaining gap.

**Hard acceptance:** every applicable production contract row is either evidence-backed PASS or explicit `PRODUCTION_UNKNOWN/BLOCKER`; no compensation across hard gates; final video <=5:00; final evidence manifest binds source/run/job/attempt/event/config/build/deploy identities; static/counterfactual data used as live proof = `0`.

## 10. Safe parallelism and critical path

### Parallel after T001

- T002 identity/security;
- T003 state/event substrate;
- T004 parser/source;
- T005 workflow/runtime;
- T006 frontend same-slice.

These tasks share contracts but should not concurrently edit the same authoritative implementation files without ownership boundaries. Spikes/benchmarks remain isolated until T007 evidence fan-in.

### Critical path

`T001 → {T002..T006} → T007 → T008 → T009 → T011/T012 → T013 → T014`

T010 human-calibration foundation can begin after its schema/data prerequisites and run partly in parallel, but strong audience-production claims cannot pass T014 until its human evidence gate is satisfied.

## 11. Migration from W004 without unnecessary rewrite

### Preserve as tested semantics / regression controls

- fail-closed source trust and ambiguity handling;
- corruption fixtures and source/provenance binding;
- exact 3×3 branch identity and lossless join semantics;
- transport retry vs quality repair distinction;
- non-compensatory hard gates;
- native typed evaluation semantics;
- current orchestrator behavior as counterfactual/reference where useful;
- clean-checkout/regression evidence as historical baseline.

### Wrap behind stable interfaces

- providers;
- parsers/OCR;
- workflow runtime/shared persistence;
- identity/session;
- private object storage;
- telemetry/export backend;
- frontend implementation behind typed API/event contracts.

### Explicitly block from production authority

- current arbitrary untrusted filesystem-path input;
- current local SQLite whole-run behavior as multi-replica shared authority;
- static/manifests-driven cockpit as production/final-evidence path;
- synchronous/request-lifetime coupling for long work;
- unlocked/ad-hoc install path as final build method;
- movable third-party release Actions;
- any automatic fallback from live product to W004 static evidence.

## 12. Autonomous vs human/external blockers

### Autonomous implementation/evidence work

T001–T009 and T011–T013 are implementable autonomously to the extent credentials/services required by the chosen candidate are available. Missing vendor credentials are candidate-specific evidence limitations, not permission to fabricate results.

### Human/external evidence

The following remain genuinely external and must stay explicit:

- independent human calibration streams for strong audience-threshold claims;
- actual Suno owner/internal workflow/SSO/SCIM/procurement/residency requirements if they are to constrain production choices;
- business ROI baseline/utility weights;
- external deadline/submission mechanism;
- externally owned SLO/SLA/RTO/RPO targets when required.

Their absence does not justify invented values. It limits the claims that can pass T014.

## 13. Quantitative gates carried forward

Only evidence-backed hard numbers are frozen:

- critical factual/source/policy hard-gate compensation = `0`;
- cross-tenant unauthorized success in defined tests = `0`;
- accepted provenance binding missing = `0`;
- exact required branch coverage = `9/9`;
- accepted join losing/duplicating branches = `0`;
- critical schema violations promoted = `0`;
- stale same-run overwrite silently accepted = `0`;
- duplicate accepted branch output from retry/delivery = `0`;
- static/counterfactual evidence used as production live truth = `0`;
- arbitrary untrusted server-path production input = `0`;
- private quarantine bypass in defined tests = `0`;
- secret/credential canary leak in product events/telemetry = `0`;
- defined restart/resume scenarios = `100% PASS` before production claim;
- defined backup/restore scenarios = `100% PASS` before production claim;
- final technical video = `<=5:00`.

Quality, audience, latency, cost, capacity, retention, sampling, SLO, RTO and RPO thresholds remain evidence/external-owner gated.

## 14. Risks and traceability

Primary risks directly controlled by this plan:

- `RISK-0021` mechanics proof mistaken for production readiness → no production PASS from design mapping; T014 independent final audit;
- `RISK-0031` cross-tenant leakage → T002/T003/T006/T009/T013 adversarial zero-success gates;
- `RISK-0033` local state under multi-replica → T003/T005 common failure harness and selected shared authority;
- `RISK-0034` stack-by-fashion rewrite → T007/T008 DRG/Pareto promotion only;
- `RISK-0035` stale/synthetic frontend evidence → §4 + §6 + T006/T009/T014;
- `RISK-0036` weak audience threshold promotion → T010 human evidence boundary;
- `RISK-0037` sensitive observability leakage → narrow OTel boundary + T012/T013 redaction/adversarial tests;
- `RISK-0038` invented capacity → T013 measured saturation interval only;
- `RISK-0039` adaptive cost/latency bypassing quality → T011 deterministic hard-gate envelope;
- `RISK-0040` DRG bureaucracy/ambiguity → exact-path refs now, unique registry in T001, benchmark-linked promotion in T007.

## 15. Exit condition for W005 / entry condition for Phase 9

W005 final fan-in is implementation-ready when the Orchestrator accepts/integrates this T012 result and plan.

That acceptance may unlock the proposed Phase 9/W006 implementation wave, but it must **not** be interpreted as:

- product production readiness;
- completion of `PROD-001..017` evidence;
- selection of open vendors/frameworks;
- proof of human audience calibration;
- proof of capacity/SLO/recovery targets;
- project completion.

The immediate next canonical action belongs to the Orchestrator: review T012, integrate if valid, then materialize the next-wave tasks from §9 with their dependencies and evidence gates.