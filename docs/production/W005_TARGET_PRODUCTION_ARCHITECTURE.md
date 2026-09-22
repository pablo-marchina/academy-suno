# W005 Target Production Architecture — Evidence-backed synthesis

`ARTIFACT_ID: W005-T010-PRODUCTION-ARCHITECTURE-V001`

`TASK_ID: W005-T010`
`ATTEMPT_ID: A01`
`STATUS: SYNTHESIS_COMPLETE`
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`

## 1. Purpose and evidence boundary

This artifact synthesizes the eleven accepted W005 research inputs required by `SYSTEM/DISPATCH/W005-T010-A01.md` into a target production architecture without converting missing evidence into consensus.

Accepted fan-in:

- `W005-T001-A01` — production requirements / evidence taxonomy;
- `W005-T002-A01` — Evidence Cockpit, typed API and live events;
- `W005-T003-A01` — orchestration durability/runtime bakeoff;
- `W005-T004-A01` — identity, tenancy, data, object storage and security;
- `W005-T005-A01` — production evaluation science / EDD;
- `W005-T006-A01` — adaptive provider/model/runtime policy;
- `W005-T007-A01` — observability and safe live evidence;
- `W005-T008-A01` — deployment/reliability/capacity methodology;
- `W005-T009-A02` — accepted cross-cutting benchmark methodology v002;
- `W005-T013-A01` — developer platform/toolchain/CI/supply chain;
- `W005-T014-A01` — financial-document parsing/source grounding.

The synthesis preserves W004 components that remain evidence-backed, rejects unearned rewrites, and uses only three final decision states for material choices: `LOCK`, `NO_PREFERENCE`, and `PENDING_EVIDENCE`.

`LOCK` means the architectural/control property is supported strongly enough to be treated as a production requirement/default at this layer. It does not imply that every vendor/product used to realize the property is locked.

## 2. Governing invariants

The target system MUST preserve these non-compensatory invariants:

1. single real product path from upload/source through final recipient UI;
2. authenticated multi-user execution with authoritative tenant/workspace/resource binding;
3. no arbitrary untrusted server filesystem path input;
4. source/provenance ambiguity fails closed;
5. exact stateful `3 audiences × 3 formats = 9` branch identity and lossless join;
6. transport retry is distinct from quality repair;
7. critical factual/source/policy/schema/tenant/provenance failures are never optimizer rewards and never averaged away;
8. accepted product state is durable outside any individual API/worker process;
9. live cockpit state comes from durable product state/events, not sampled telemetry;
10. raw sensitive document/prompt/output content is off by default in telemetry;
11. every material policy/config/model/parser/evaluator/runtime version is auditable;
12. production claims require production-equivalent security/reliability/deployment evidence.

## 3. Target logical architecture

```text
Authenticated browser / Evidence Cockpit
        |
        | typed/versioned HTTP commands/resources
        | SSE live feed (durable cursor/replay/snapshot)
        v
+-------------------------- Product API --------------------------+
| principal mapping | authz | tenant context | idempotency       |
| validation        | upload grants / source access | commands   |
+------------------------+------------------+---------------------+
                         |                  |
                         |                  +--> Authorized read projections
                         |                       (runs, 3x3, sources, evals,
                         |                        repair, audit, experiments)
                         v
              Durable command/work boundary
                         |
                         v
+---------------------- Workflow runtime -------------------------+
| stable run/job/branch IDs | resume | bounded retry | fan-out 9 |
| source gate | provider route | eval | repair | lossless join   |
+-----------+------------------+-------------------+--------------+
            |                  |                   |
            |                  |                   +--> Provider adapters
            |                  |                        + versioned routing policy
            |                  |
            |                  +--> Eval / experiment subsystem
            |                       + hard gates
            |                       + calibrated secondary judges
            |                       + human calibration datasets
            |
            +--> Source/document subsystem
                 private quarantine object
                    -> validate/hash/classify
                    -> parse/OCR candidate
                    -> canonical ParsedDocument
                    -> provenance/anchor/source-trust gate

Authoritative persistence plane
  - shared durable run/workflow state
  - tenant/resource data
  - append-only/auditable history where applicable
  - private object/document versions
  - versioned experiment/policy/config records
  - durable ordered product events

Live product plane
  durable ordered product events
      -> authorized/redacted projection
      -> SSE cursor/replay/snapshot
      -> Evidence Cockpit

Observability plane (not authoritative run state)
  W3C trace context + OTel traces/metrics/structured logs
      -> OTLP / Collector boundary
      -> backend(s) pending evidence

Developer/release plane
  GitHub Actions
      -> deterministic regression + offline experiments
      -> locked installs once manager chosen
      -> SBOM + artifact provenance/attestation
      -> deploy/recovery/load evidence
```

## 4. End-to-end source → parse/provenance → 9 → eval → repair → aggregate live path

### 4.1 Source intake

1. User authenticates; API resolves principal and authoritative organization/workspace server-side.
2. Upload intent is authorized against the target workspace/resource.
3. Bytes enter private quarantine under a server-generated opaque object key. Original filename remains display metadata only.
4. System records immutable source hash/object version plus tenant/workspace/document identity.
5. Type/structure/size/resource validation and malware/sandbox/CDR controls run as applicable. Exact production limits remain declared-and-tested/evidence-gated rather than invented.
6. Only a validated object can be promoted to the clean source area.

### 4.2 Parse and provenance

7. Text-layer preflight determines whether the document is digital/scanned/table-bearing/ambiguous.
8. A parser/OCR candidate executes behind a parser-agnostic adapter.
9. Output is normalized to a canonical `ParsedDocument` carrying page/span/table/cell provenance where available.
10. Source trust evaluates semantic provenance completeness. Parser success/no exception never increases trust by itself.
11. Table-derived evidence is eligible only when required row/column/role provenance is resolvable. Ambiguous table/OCR text remains fail-closed / review-required.

### 4.3 Stateful 3×3 workflow

12. A durable `run_id` is created with versioned source, policy, prompt/retrieval/evaluator/repair/catalog identities.
13. Fan-out creates exactly nine stable `(audience, format)` branch/job identities.
14. Each branch selects only provider/model routes already eligible under deterministic capability/security/policy constraints.
15. Provider calls use one bounded end-to-end deadline/retry budget and typed failure taxonomy; fallback is capability-equivalent and audited.
16. Output is evaluated by non-compensatory hard gates plus quantitative/semantic sensors.
17. Recoverable quality failures may trigger bounded targeted repair; repair is not transport retry.
18. Repaired output is freshly re-evaluated under the same hard gates.
19. The aggregate step is allowed only after keyed 9/9 completion with zero accepted loss/duplication and explicit review/failure states retained.

### 4.4 Live evidence and telemetry

20. State transitions append durable ordered domain/product events carrying monotonic event IDs, run revision, typed domain IDs, visibility classification and trace correlation.
21. Server-side authorization/redaction occurs before event/snapshot/source/trace serialization.
22. The browser consumes the default one-way run feed by SSE using cursor/`Last-Event-ID`, de-duplication and snapshot fallback.
23. The cockpit labels live/reconnecting/stale/snapshot-required state and never presents stale/synthetic evidence as current.
24. Separately, W3C/OTel traces, metrics and structured logs export via OTLP/Collector. Telemetry loss/degradation must not corrupt the durable product path.

## 5. Material decision matrix

| Area | Decision state | Target decision | Evidence basis / boundary | Reversal condition |
|---|---|---|---|---|
| Product boundary | `LOCK` | typed/versioned HTTP resource/command API | T002 + PROD-002 | only if an alternative preserves typed/versioned contract with superior representative evidence |
| API description | `LOCK` | OpenAPI-described boundary | T002 | exact OAS/tooling version may change |
| API framework | `NO_PREFERENCE` | framework not selected | no same-workload framework bakeoff | representative implementation benchmark + security/ops evidence |
| Live run transport | `LOCK` | SSE default for server→browser run events | T002 probe + one-way event semantics | proxy/load/auth/event-rate evidence materially fails |
| Live replay | `LOCK` | durable monotonic cursor + de-dupe + snapshot fallback | T002/T007 | substrate may change if equivalent durability/replay proven |
| WebSocket | `PENDING_EVIDENCE` | collaboration-only candidate, not universal telemetry | T002 | product proves bidirectional collaboration need |
| Frontend framework | `PENDING_EVIDENCE` | React+Vite vs Next.js | T002 requires same-slice T013 benchmark | same cockpit slice build/deploy/CI evidence |
| Structured editor | `PENDING_EVIDENCE` | Tiptap/ProseMirror vs Lexical | no Academy citation/IME/table/a11y spike | representative editor spike |
| Static W004 cockpit | `LOCK` | preserve as diagnostic/fallback baseline only | T002 | may be retired only after production cockpit supersedes its evidence semantics |
| Identity protocol boundary | `LOCK` | standards-based external identity mapped by stable `(issuer, subject)` to internal `user_id` | T004 | only if replacement preserves stable principal mapping and security properties |
| Identity provider/vendor | `NO_PREFERENCE` | managed B2B/self-hosted/integrated candidates remain open | missing Suno IdP/SSO/SCIM/procurement/residency evidence | partner requirements + bakeoff |
| Authorization | `LOCK` | application-owned deny-by-default membership/permission/resource checks; server resolves tenant context | T004 | mechanism may evolve; invariant cannot weaken |
| Tenant isolation | `LOCK` | first-class org/workspace/user/run binding + independent data-plane defense in depth | T004 + PROD-001 | only stronger equivalent isolation |
| Relational/data engine | `PENDING_EVIDENCE` | pooled tenant-keyed relational + RLS/equivalent is leading candidate, not winner | T004; backup/perf/adversarial bakeoff absent | identical security/perf/restore benchmark |
| PostgreSQL-specific RLS | `PENDING_EVIDENCE` | candidate if PostgreSQL chosen; runtime role must not bypass RLS and fixed security patch level is mandatory | T004 | alternative data engine or changed advisory state |
| Private object storage | `LOCK` | private tenant-bound object boundary, server-generated keys, quarantine→validate→clean, immutable provenance | T004 | provider may change; lifecycle/security invariant remains |
| Object-store/scanner vendor | `NO_PREFERENCE` | no vendor selected | missing same-workload cost/security/ops evidence | representative bakeoff + policy requirements |
| Parser architecture | `LOCK` | parser-agnostic cascade + canonical normalized provenance + fail-closed source trust | T014 | cannot reverse without equal/better corruption detection/provenance evidence |
| Parser/OCR winner | `PENDING_EVIDENCE` | PyMuPDF/pdfplumber/Docling/Textract/Azure/Google shortlist | T014 diagnostic fixture not sufficient to rank production | same real-financial corpus benchmark |
| Workflow semantics | `LOCK` | stable run/job/branch IDs, exact 9-way fan-out/join, resume, retry/repair separation | W004 baseline + T003 | implementation may change, semantics may not weaken |
| Current `SQLiteRunStore` production authority | `LOCK` | **not permitted as multi-replica production authority in current form**; retain local/baseline use only | T003 reproduced stale same-run lost update | may re-enter only with shared backend + ownership/CAS + same-worker probes passing |
| Workflow/runtime framework | `PENDING_EVIDENCE` | current custom baseline vs LangGraph vs DBOS vs Temporal | candidates not run under identical shared-state harness | common production-capable durability benchmark |
| Adaptive safety envelope | `LOCK` | deterministic eligibility/hard gates outside optimizer; post-route hard-gate validation | T006 + PROD-010 | invariant cannot be relaxed by optimizer evidence |
| Routing policy form | `PENDING_EVIDENCE` | deterministic rules/cascade is implementation control; learned router remains challenger | no representative cross-provider/held-out bakeoff | offline→shadow→canary evidence |
| Provider/model winner | `NO_PREFERENCE` | no overall provider/model preference | W004 bounded evidence + T006 no live representative fan-out | representative multi-provider benchmark |
| Provider catalog/policy versioning | `LOCK` | immutable versioned candidate catalog, pricing snapshot, policy, rollback target and telemetry | T006 | storage/mechanism may change; auditability remains |
| Eval hard-gate architecture | `LOCK` | non-compensatory factual/source/policy/schema gates + versioned evaluator config | T005/T009 | hard gates can only tighten/replace with equivalent evidence |
| Human calibration method | `LOCK` | blind independent primary streams + triggered adjudication + pre-adjudication agreement | T005 | pilot evidence may justify more streams, not weaker independence |
| Model judge role | `LOCK` | calibrated secondary sensor only; never human gold and never overrides critical gates | T005 | only independent evidence could change role |
| Audience thresholds | `PENDING_EVIDENCE` | remain `DIAGNOSTIC_ONLY` | human gold/held-out evidence absent | independent calibration + held-out replication |
| External eval framework | `PENDING_EVIDENCE` | native typed harness is authoritative baseline; Promptfoo/DeepEval/LangSmith challengers | no representative tooling bakeoff | same dataset/config/tooling benchmark |
| Cross-cutting benchmark method | `LOCK` | hard gates → raw multidimensional metrics → uncertainty where meaningful → point Pareto → no preference when unresolved | accepted T009-A02 v002 | business utility only after representative evidence + sensitivity stability |
| Scalar utility/weights | `PENDING_EVIDENCE` | prohibited as default | T009-A02 | representative human/business utility evidence, frozen before outcomes |
| Product live events vs telemetry | `LOCK` | durable product events are separate from sampled observability | T007 | alternative must prove equivalent transactional durability/replay/isolation/outage independence |
| Trace/metric/log boundary | `LOCK` | W3C Trace Context + OpenTelemetry + OTLP/Collector boundary; core code backend-neutral | T007 high-confidence candidate promoted by synthesis | representative alternative must materially improve without losing portability/security/coverage |
| Raw GenAI content telemetry | `LOCK` | OFF by default; metadata-first, audited opt-in only | T004/T007 | explicit approved requirement + narrower safe design insufficient |
| Metric label policy | `LOCK` | bounded label allowlist; high-cardinality IDs stay in traces/logs/events, not default metric labels | T007 | bounded-ID use proven necessary and safe |
| Observability backend | `NO_PREFERENCE` | Grafana/Phoenix/Langfuse/etc. unresolved | no identical workload ops/cost/security bakeoff | representative backend benchmark |
| Deployment class | `NO_PREFERENCE` | managed-container vs cluster scheduler remain viable; workflow overlay depends on runtime choice | T008 | workload/cost/ops evidence |
| Deployment invariants | `LOCK` | replaceable API, decoupled long work, shared durable state, explicit backpressure/idempotency, distinct health, bounded scaling, controlled migrations, clean restore proof | T008 | invariant may only be strengthened |
| Capacity/SLO/RTO/RPO values | `PENDING_EVIDENCE` | do not invent values; report saturation interval and measured recovery | T001/T008/T009 | representative benchmark + owner/business target |
| CI platform | `LOCK` | GitHub Actions | T013 | reopen only on evidenced platform blocker |
| CI/supply-chain policy | `LOCK` | full-SHA third-party actions, least privilege, authoritative lock, cache keyed by lock/runtime/OS, SBOM, artifact provenance/attestation | T013 | implementation detail may evolve; control intent remains |
| Python package manager | `PENDING_EVIDENCE` | uv lead; Poetry/PDM live challengers | real production dependency topology not frozen | representative lock/sync/CI benchmark |
| JS package manager | `PENDING_EVIDENCE` | pnpm lead for multi-package; npm simplicity baseline; Yarn challenger | production Node topology not proven | frontend topology + representative benchmark |
| Repository strategy | `LOCK` | keep the existing single repository through initial production migration; no task-graph layer without evidence | T013 migration boundary | measured multi-deployable CI pain justifies change |
| Task graph (Nx/Turborepo) | `PENDING_EVIDENCE` | do not add yet | no demonstrated repeated graph/caching need | representative CI graph + complexity evidence |
| Local environment wrapper | `NO_PREFERENCE` | pinned native runtime and Dev Container both valid behind same canonical command contract | T013 | service/native-dependency requirements |
| SBOM encoding | `NO_PREFERENCE` | CycloneDX vs SPDX open | consumer requirement absent | deployment/consumer requirement |

## 6. Current-component migration disposition

### Preserve

- fail-closed source trust and explicit ambiguity;
- source/provenance binding and corruption fixtures;
- stable 3×3 branch identity and lossless join semantics;
- transport-retry vs branch-quality-repair separation;
- non-compensatory hard gates;
- native typed evaluation semantics and W004 diagnostics;
- static Evidence Cockpit as a diagnostic/fallback artifact;
- current `AsyncGraphOrchestrator` as behavioral reference/counterfactual;
- existing clean-checkout regression evidence as historical baseline.

### Wrap behind stable interfaces

- provider calls behind provider-neutral candidate/catalog/routing interfaces;
- parser implementations behind canonical `ParsedDocument`/provenance adapters;
- workflow implementation behind explicit run/job/checkpoint/event interfaces;
- persistence behind shared-state repositories with version/ownership semantics;
- identity provider behind principal-mapping adapter;
- object storage behind private tenant-bound object interface;
- observability behind OTel/OTLP boundary;
- frontend behind typed API/SSE contracts rather than direct local files.

### Replace in production path

- arbitrary local PDF filesystem path input from untrusted users;
- local-only `SQLiteRunStore` as multi-replica authority in its current stale-write form;
- `ThreadingHTTPServer`/inline synchronous recipient surface as the sole production product boundary;
- static/generated dashboard data as the live source of truth;
- ad-hoc inline dependency installation as final reproducible build method;
- movable third-party GitHub Action major tags in hardened release workflows.

### Benchmark before selecting/replacing

- workflow runtime and shared state substrate;
- relational database/data-plane topology and object storage provider;
- frontend framework and structured editor;
- production parser/OCR stack;
- provider/model portfolio and learned router;
- external eval framework;
- observability backend;
- deployment topology;
- Python/JS package managers and any task-graph layer.

## 7. Failure and consistency rules

### 7.1 Durable writes

Accepted state transitions MUST reject stale same-run writes or otherwise serialize/lease ownership so that a prior snapshot cannot silently overwrite newer accepted state. A sequence number alone is insufficient if the whole-run payload is stale.

### 7.2 Idempotency

Commands that can be retried MUST carry stable idempotency/work identity. Duplicate delivery may create additional attempt records but must not create duplicate accepted logical branch results.

### 7.3 Backpressure

The system MUST expose bounded in-flight work/retries and explicit admit/defer/reject behavior. Provider/DB/worker concurrency limits are versioned operating values and remain evidence-gated.

### 7.4 Telemetry failure

Collector/backend outage MUST NOT block or mutate durable product state. Telemetry export failures are observable operational failures, not run-state failures unless a separately defined hard audit requirement cannot be persisted.

### 7.5 Live reconnect

A reconnecting client either replays from a durable cursor or receives an explicit snapshot-required condition. Silent event gaps and silently regressive run revisions are invalid.

## 8. Security/privacy control plane

The production design requires:

- application authorization on every protected resource/action;
- independent tenant isolation/data-plane defense in depth;
- separate DB migrator/API/worker/backup/service identities;
- private object storage with short-lived scoped grants only after current authz;
- no signed grants, credentials, cookies, tokens, raw document text, prompts or outputs in default telemetry;
- queue/cache/work identities include tenant/resource identity and are revalidated by workers;
- retention class, expiry/legal-hold/deletion orchestration modeled even while exact calendar remains policy-pending;
- cross-tenant, object-key substitution, stale membership, connection-pool contamination, telemetry canary, upload abuse and backup/restore isolation tests.

If PostgreSQL/RLS is selected, deployment must additionally enforce non-owner/non-superuser/non-`BYPASSRLS` runtime roles and a fixed security patch level satisfying current advisories at release time.

## 9. Evidence and experiment plane

Every material experiment result MUST retain:

- workload/dataset/config versions;
- `source_group_id` to preserve 3×3 correlation;
- raw observations and failures;
- evidence class and missingness;
- hard-gate eligibility;
- paired/block uncertainty where meaningful;
- point Pareto among eligible systems;
- no manufactured scalar preference when trade-offs remain;
- experiment provenance, seeds/config and reversal conditions.

Human calibration uses versioned DEV/CALIBRATION/HELD_OUT partitions and independent blinded streams. Production audience thresholds remain diagnostic until independent calibration and held-out replication exist.

## 10. PROD-001..017 traceability

| PROD | Architecture/control path | Required evidence before production claim | Current synthesis state |
|---|---|---|---|
| PROD-001 | principal mapper → app authz → authoritative tenant context → data-plane isolation | adversarial API/DB/object/queue tests; unauthorized cross-tenant success `0` | architecture `LOCK`; vendor/data engine pending |
| PROD-002 | typed/versioned HTTP + validation/idempotency/backpressure; no arbitrary path | contract/integration/overload tests; declared/tested limits | contract `LOCK`; framework/limits pending |
| PROD-003 | shared durable run/data state + append/audit + backup/restore | restart/redeploy, same-run multi-worker safety, clean restore | current SQLite production authority rejected; replacement pending |
| PROD-004 | private quarantine object → validation/hash → clean → parser/provenance | upload abuse, provenance, object isolation, retention/deletion tests | lifecycle `LOCK`; provider/limits pending |
| PROD-005 | provider-neutral adapters/catalog/policy with real configured providers | representative provider/model quality/cost/latency/reliability benchmark | interfaces `LOCK`; winner `NO_PREFERENCE` |
| PROD-006 | durable exact 9-way workflow, resume, retry/repair separation, lossless keyed join | branch coverage `9/9`; accepted loss/duplication `0`; restart scenarios | semantics `LOCK`; runtime pending |
| PROD-007 | hybrid hard gates + quantitative/secondary semantic sensors + versioned config | critical compensation `0`; critical schema false-pass `0`; regression artifacts | architecture `LOCK` |
| PROD-008 | blind independent human streams + adjudication + grouped splits | real human labels, agreement/confusion, uncertainty, held-out replication | method `LOCK`; thresholds pending |
| PROD-009 | GitHub Actions deterministic lane + offline probabilistic/human promotion lane | baseline/candidate same data/config; release hard-gate blocks; artifacts retained | platform/method `LOCK` |
| PROD-010 | versioned adaptive policy inside deterministic hard-gate envelope | offline→shadow→canary evidence; rollback proof; route telemetry | envelope `LOCK`; optimizer/provider pending |
| PROD-011 | durable events → authorized SSE replay/snapshot → cockpit | live/reconnect/stale correctness, 3×3/source/eval/repair/trace projections | live contract `LOCK`; frontend tool pending |
| PROD-012 | W3C/OTel → OTLP/Collector → backend | clean-run trace completeness, metrics/logs correlation, export failure and cardinality tests | boundary `LOCK`; backend/sampling pending |
| PROD-013 | staged load curve + saturation interval + failure/restart/restore matrix | raw p50/p95/p99/throughput/queue/error/resource/cost observations; 100% defined restart/restore scenarios | methodology/invariants `LOCK`; targets pending |
| PROD-014 | threat model + least privilege + input/tenant/secret/telemetry controls | adversarial suite, secret canaries, dependency/supply-chain verification | controls `LOCK`; implementation evidence pending |
| PROD-015 | DRG records + accepted T009 v002 decision surface | every material production choice traced to research/benchmark or explicitly pending | `LOCK` process; multiple technology winners pending |
| PROD-016 | reproducible manifests/locks + declarative deploy + health/migrations/secrets | clean install/build/deploy, migration/restart, artifact provenance, runbook | controls `LOCK`; final toolchain/deploy class pending |
| PROD-017 | same real path in UI/evidence/video | real provider/workflow/live cockpit evidence and applicable gates; final video `<=5:00` | architecture `LOCK`; final evidence future |

## 11. Open evidence queue created by this synthesis

The following are not architecture defects; they are explicit evidence gaps that block production locks/claims where applicable:

1. common-harness workflow/runtime + shared-state bakeoff;
2. adversarial/performance/restore data-engine bakeoff;
3. real-financial same-corpus parser/OCR bakeoff;
4. same-slice frontend framework/editor benchmark;
5. representative multi-provider/model routing benchmark;
6. independent human calibration and held-out audience threshold work;
7. external eval tooling bakeoff if framework selection becomes blocking;
8. observability backend operational/cost/security bakeoff;
9. production-equivalent deployment/load/failure/recovery execution;
10. Python/JS package-manager benchmark on the selected dependency topology;
11. partner/external facts: real identity topology, retention policy, concurrency, SLO/SLA/RTO/RPO, budget/ops owner, submission/finalization mechanism.

Until those inputs exist, the correct state is `NO_PREFERENCE` or `PENDING_EVIDENCE`, not an inferred winner.
