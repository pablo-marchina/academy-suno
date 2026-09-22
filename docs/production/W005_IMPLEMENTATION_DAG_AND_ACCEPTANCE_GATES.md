# W005 Implementation DAG and Acceptance Gates

`ARTIFACT_ID: W005-T010-IMPLEMENTATION-DAG-V001`

`TASK_ID: W005-T010`
`ATTEMPT_ID: A01`
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`

## 1. Purpose

This artifact turns the W005 production-architecture synthesis into an implementation dependency graph, migration increments, evidence checkpoints and quantitative acceptance gates. It does not authorize Phase 9 implementation before the orchestrator completes the required T010 → T011 → T012 fan-in.

The governing rule is: **do not implement through unresolved material choices as if they were already selected**. Use spikes/bakeoffs to resolve `PENDING_EVIDENCE`; production migration begins only after the downstream synthesis/red-team gates authorize it.

## 2. Conflict reconciliation retained by T010

The fan-in contains compatible research plus several places where one task proposed a useful local heuristic that another accepted method prevents from becoming a universal production rule. T010 preserves those disagreements explicitly.

| Topic | Inputs | Reconciliation |
|---|---|---|
| CI cache practical-effect threshold | T013 proposes a task-local `>=20%` median warm-runtime improvement after repeated cold/warm runs | T009-A02 rejects universal practical-effect thresholds without representative utility evidence. The `20%` number remains an experiment proposal, **not a production lock**. Cache adoption should persist raw timings and use the accepted multidimensional decision surface. |
| Repetition count | T006 suggests `R>=3` initial repetitions for stochastic provider cells | T005/T009 require sample size/uncertainty tied to the estimand and source correlation. `R>=3` may be an exploratory floor, never evidence that uncertainty is sufficient for promotion. |
| Relational/RLS topology | T004 identifies pooled tenant-keyed relational + RLS/equivalent as the strongest current default candidate | T003/T008 require production shared-state/multi-worker/recovery evidence. Therefore the isolation pattern is a candidate, not a database winner. |
| OTel/Collector | T007 marks the vendor-neutral boundary as candidate-for-T010-lock | T010 locks the interface/instrumentation boundary, while keeping the observability backend and sampling percentages open. |
| SSE live feed | T002 selects SSE as default | T007 confirms product events must be durable and independent from telemetry. T010 locks SSE **only as browser transport**, not as the durability mechanism. |
| Current orchestration baseline | T003 validates strong local behavior and reproduces stale same-run lost update | T010 preserves `AsyncGraphOrchestrator` as behavioral control but locks the current `SQLiteRunStore` out of multi-replica production authority until repaired/replaced and re-tested. |
| Parser candidates | T014 shows local structured parsers can preserve roles on a diagnostic fixture | T009 methodology + T014 limitations forbid ranking them for production before same-corpus real-financial evidence. |
| Frontend framework | T002 identifies React+Vite as leading candidate and Next.js as credible | T013 confirms Node/package/build topology is not yet evidenced. Framework remains pending same-slice implementation/build/deploy benchmark. |

## 3. Implementation dependency graph

```text
G0  T010 accepted → T011 red-team → T012 final fan-in
 |
 v
G1  Contract/schema freeze
 |   API resources/commands, IDs, event envelope, ParsedDocument,
 |   run/job/eval/repair/policy/experiment schemas
 |
 +------------------+---------------------+-----------------------+
 |                  |                     |                       |
 v                  v                     v                       v
G2A Identity/data   G2B Secure source     G2C Runtime/shared      G2D UI slice
    security            ingestion/parser      state bakeoff           bakeoff
 |                  |                     |                       |
 +----------+-------+----------+----------+-----------+-----------+
            |                  |                      |
            v                  v                      v
           G3A Production substrate selection / evidence promotion
            |    identity vendor if needed, data engine, object store,
            |    parser route(s), workflow/runtime, frontend framework/editor
            |
            v
           G3B Reproducible toolchain freeze
            |    Python/JS manager benchmark on real selected dependency graph
            |    authoritative manifests + committed lockfiles
            |    reusable CI + full-SHA actions + SBOM/attestation path
            |
            +--------------------------+
            |                          |
            v                          v
           G4A Product vertical slice  G4B Eval/experiment foundation
            |                          |
            +-------------+------------+
                          v
                         G5 Provider/adaptive runtime bakeoff
                          |
                          v
                         G6 Live cockpit + observability integration
                          |
                          v
                         G7 Security/adversarial + load/failure/recovery
                          |
                          v
                         G8 Release evidence / production-claim review
```

No node may be skipped merely to accelerate the demo. Nodes can execute in parallel where their dependencies do not overlap.

## 4. Migration increments

### Increment 0 — Post-T010 governance gate

**Entry:** T010 worker result exists.

**Work:**
- independent T011 red-team of T010;
- T012 final fan-in/architecture acceptance;
- no bulk production implementation before those canonical gates.

**Exit evidence:** downstream orchestrator acceptance/integration. This is a project coordination gate, not a technical implementation gate.

### Increment 1 — Contract and schema freeze

**Goal:** create implementation-neutral boundaries before choosing products.

**Outputs:**
- versioned HTTP/OpenAPI resource/command schema;
- stable IDs for organization/workspace/user/document/run/job/branch/attempt/eval/repair/experiment;
- versioned durable event envelope + cursor/revision semantics;
- canonical `ParsedDocument` and provenance schema;
- provider candidate/catalog/policy interface;
- evaluator/experiment metadata contracts;
- persistence contracts including optimistic version/ownership semantics;
- telemetry attribute/metric allowlists.

**Acceptance gates:**
- schema/version identifiers exist for all interfaces;
- required tenant/provenance fields cannot be omitted from protected/private resources;
- deterministic contract tests show critical schema violations promoted as PASS = `0`;
- event contract has explicit replay/de-dup/snapshot-required behavior;
- no selected vendor/framework is required by a core domain interface.

**Evidence:** EC-1 contract + EC-2 deterministic tests.

### Increment 2A — Identity, tenancy, data and object-security substrate bakeoff

**Goal:** resolve production identity/data/storage choices or retain explicit no-preference while proving the selected implementation candidate's controls.

**Work:**
- implement principal mapping and application-owned authorization boundary;
- implement authoritative server-side org/workspace resolution;
- candidate shared relational/data store with defense-in-depth isolation;
- private object store and quarantine/validate/promote lifecycle;
- separate runtime/migrator/worker/backup identities;
- adversarial fixture matrix across two+ tenants/workspaces/roles.

**Acceptance gates:**
- unauthorized cross-tenant access in defined API/DB/object/queue/cache tests = `0`;
- protected resources without tenant binding accepted = `0`;
- raw private-object public reads = `0`;
- quarantine bypasses = `0`;
- seeded secret/credential canary leaks through logs/traces/events = `0`;
- if PostgreSQL/RLS is used, runtime role is not superuser/owner/`BYPASSRLS` and release patch level is not known-vulnerable at release time;
- clean backup/restore test for the candidate is designed before promotion; target RPO/RTO remains `UNKNOWN` unless externally/evidentially defined.

**Evidence:** deterministic/adversarial/security + restore drill artifacts.

### Increment 2B — Secure source ingestion and parser bakeoff

**Goal:** preserve fail-closed source trust while resolving parser routes on real financial documents.

**Work:**
- build versioned real-public-financial corpus with page/table/cell gold annotations;
- normalize local/managed candidates behind the same `ParsedDocument` adapter;
- include digital, scanned, malformed, encrypted, large and multi-page table cases;
- persist raw candidate outputs, failures, latency/resource/cost observations.

**Acceptance gates:**
- source hash/provenance binding missing on accepted evidence = `0`;
- role-ambiguous table/OCR content promoted to HIGH-trust table evidence = `0`;
- exact numeric/entity/date preservation and semantic table-role metrics reported raw by source group;
- p50/p95 latency, memory/resource use and regional/current cost recorded where applicable;
- candidate selection uses hard-gate eligibility + raw metrics + source-group uncertainty + Pareto; no scalar score or fixed practical-effect threshold without evidence.

**Evidence:** benchmark result conforming to W005 methodology v002 + corruption fixtures + raw parser artifacts.

### Increment 2C — Workflow/runtime/shared-state bakeoff

**Goal:** select/validate a production-capable run-state/workflow substrate without weakening W004 semantics.

**Candidates:** current custom baseline repaired onto shared state, LangGraph, DBOS, Temporal and any materially different candidate justified before freeze.

**Workload:** exact Academy 9-way fan-out, transport retry, quality repair, crash/restart, resume, concurrent independent runs and same-run multi-worker stale-write scenario.

**Acceptance gates:**
- exact required branch coverage = `9/9` in every accepted run;
- accepted join losing/duplicating branches = `0`;
- stale same-run overwrite accepted silently = `0`;
- defined restart/resume scenarios = `100% PASS` before production claim;
- state write/checkpoint counts and p50/p95 runtime overhead reported;
- no claim that synthetic orchestration latency predicts end-user provider latency;
- operational/setup burden recorded as raw evidence, not hidden in a scalar score.

**Evidence:** common-harness raw results + recovery artifacts + DR update.

### Increment 2D — Frontend/framework/editor same-slice bakeoff

**Goal:** select the real recipient UI implementation after API/event contracts are stable.

**Slice:** authenticated workspace → upload/source → live run → real 3×3 → source citations → eval/repair → reconnect.

**Acceptance gates:**
- same API/event contract for all candidates;
- live state comes only from current durable run/events;
- reconnect either replays gap-free or explicitly requires snapshot;
- cross-tenant source/event/trace projection success = `0`;
- failed/review-required cells remain visible and non-compensatory;
- build/test/deploy/bundle/dependency/CI observations persisted;
- accessibility checks include dynamic update behavior and non-graph equivalents;
- editor selection, if needed, includes citation serialization, table behavior, IME and accessibility under the same spike.

**Evidence:** same-slice candidate artifacts + build/CI/deploy measurements.

### Increment 3 — Reproducible toolchain freeze

**This is the first increment that creates the final reproducible manifests/toolchain for the selected production topology.**

It MUST occur only after the material dependency topology from 2A–2D is known. Before this point, isolated spikes may use task-local environments; they must not be misrepresented as the final production dependency surface.

**Work:**
- run uv/Poetry/PDM on the actual selected Python dependency graph;
- if Node/TypeScript exists, run pnpm/npm/Yarn on the actual selected frontend/workspace graph;
- decide whether native package scripts are sufficient; add Nx/Turborepo only if the measured task graph justifies it;
- create authoritative root/project manifests and committed lockfiles;
- replace inline/unlocked install paths in authoritative CI;
- pin third-party Actions to verified full commit SHAs;
- least-privilege workflow permissions;
- lockfile-keyed caches with low-trust cache-write restrictions;
- reusable workflows/composite actions where duplication warrants it;
- SBOM generation and release artifact attestation/provenance verification.

**Acceptance gates:**
- clean environment installs exactly from committed authoritative lock(s): PASS;
- clean environment builds/tests the selected vertical slice from canonical commands: PASS;
- dependency lock repeat is stable under the chosen manager: PASS;
- third-party production/release Actions referenced by movable tags: `0`;
- workflows with unnecessarily broad token permissions in the release path: `0`;
- releasable artifact has generated SBOM: PASS;
- releasable artifact provenance/attestation can be verified from a clean verifier: PASS;
- any cache/task-graph adoption decision follows W005 v002 raw-metric/Pareto method; T013's local `20%` cache heuristic is not treated as a universal hard gate.

**Evidence:** manifest/lock diffs, clean install/build/test logs, CI artifacts, SBOM, attestation verification record.

### Increment 4 — Production vertical slice

**Goal:** run one real end-to-end tenant-safe product slice on the selected substrate.

**Path:** auth → workspace → secure upload → parse/provenance → durable 9-way workflow → eval/repair → aggregate → durable events → live cockpit.

**Acceptance gates:**
- required provenance missing on accepted run/job evidence = `0`;
- exact 9/9 coverage and zero accepted branch loss/duplication;
- current run visible in cockpit is correlated by run/job/event IDs, not a fixture/static surrogate;
- arbitrary untrusted server filesystem path route exists in production API = `0`;
- live replay/reconnect defined scenarios: PASS;
- telemetry outage does not corrupt/block durable product result: PASS;
- tenant boundary adversarial suite remains PASS.

**Evidence:** EC-2/3/5/8 deterministic, runtime, security and live-product evidence.

### Increment 5 — Eval/experiment and human-calibration foundation

**Goal:** turn evaluation into release-control evidence, not a dashboard score.

**Work:**
- freeze versioned DEV/CALIBRATION/HELD_OUT corpus partitions by source group;
- collect two blind independent human primary streams per item by default;
- report pre-adjudication agreement/confusion and triggered adjudication;
- calibrate secondary model/judge sensors against independent human evidence;
- run baseline-vs-candidate paired experiments with source-group correlation preserved.

**Acceptance gates:**
- human gold claim derived only from automated/model labels = `0`;
- critical factual/source/policy hard-gate compensation = `0`;
- critical schema violation promoted as PASS = `0`;
- source-group identity missing where 3×3 outputs share a source = `0`;
- audience production thresholds remain `DIAGNOSTIC_ONLY` until calibration + frozen HELD_OUT replication supports them;
- sample size/uncertainty follows the estimand/pilot evidence, not an arbitrary universal N.

**Evidence:** human annotation packets, agreement/adjudication artifacts, versioned dataset manifests, W005-v002 benchmark outputs.

### Increment 6 — Provider/adaptive runtime promotion

**Goal:** select provider/model/routing defaults only after representative evidence.

**Work:**
- refresh exact provider/model IDs, prices, lifecycle and limits;
- benchmark materially different candidates on the same production-like corpus/config;
- persist token usage, estimated/billed cost where available, latency, reliability, retries/fallbacks and hard-gate outcomes;
- evaluate static candidates first, then deterministic cascade, then learned shadow router; bounded canary only if justified.

**Acceptance gates:**
- hard-gate violating output accepted because of cost/latency advantage = `0`;
- fallback to capability-ineligible route = `0`;
- invalid auth/config/tenant/policy errors blindly retried as transient = `0`;
- policy/catalog/pricing snapshot identity missing from accepted adaptive run = `0`;
- canary critical hard-gate failure triggers stop/rollback behavior: PASS;
- winner emitted when Pareto trade-offs remain unresolved and no business utility evidence exists = `0`.

**Evidence:** representative raw benchmark + shadow/canary/rollback artifacts.

### Increment 7 — Observability/live-operations integration

**Goal:** make the real product inspectable without turning telemetry into a content shadow store.

**Work:**
- W3C trace context across request/queue/resume/fan-in paths;
- OTel traces/metrics/structured logs + OTLP/Collector boundary;
- provider/eval/repair spans;
- bounded metric dimensions;
- authorized trace/source projection to cockpit;
- selected backend only after workload/ops/cost/security comparison.

**Acceptance gates:**
- raw credentials/secrets in telemetry = `0`;
- raw document/prompt/output content emitted by default = `0`;
- high-cardinality run/job/document/tenant IDs used as default metric labels = `0`;
- exact 9 branch identities traceable in controlled acceptance run with sampling disabled: PASS;
- provider/eval/repair correlation: PASS;
- telemetry exporter/backend outage leaves product event/run path healthy: PASS;
- p50/p95/p99, error/retry/queue and cost observations available; target values remain evidence-gated.

**Evidence:** controlled trace set, cardinality/redaction tests, backend failure injection and raw operational measurements.

### Increment 8 — Reliability/capacity/recovery qualification

**Goal:** establish evidence for capacity and recovery without inventing supported-user counts or SLOs.

**Stages:** validate → baseline → concurrency ladder → arrival staircase → burst → soak → controlled saturation → post-recovery.

**Acceptance gates:**
- publish `SATURATION_INTERVAL = [highest observed stable offered load, first observed unstable offered load]` with workload/environment/bottleneck/raw repetitions;
- record p50/p95/p99 API latency, queue wait and logical run duration where applicable;
- record offered/admitted/completed throughput separately;
- record queue age/depth, errors/retries/timeouts/cancellations, DB/worker/provider/resource saturation and cost where available;
- defined restart/resume scenarios = `100% PASS` before production claim;
- defined backup/restore scenarios = `100% PASS` before production claim;
- accepted branch/provenance hard gates remain zero-failure under load/failure tests;
- numeric SLO/SLA/capacity/RTO/RPO target is either evidence/owner-backed or explicitly `UNKNOWN`.

**Evidence:** raw load curves, failure matrix, recovery/restore artifacts, environment manifest.

### Increment 9 — Release/final evidence

**Goal:** prove the same real system that will be defended.

**Acceptance gates:**
- applicable PROD-001..017 traced to evidence and all hard gates PASS;
- no open P0 Production Contract blocker in claimed scope;
- production UI executes the real provider/workflow/eval/repair/storage/event path;
- mechanics/fixture/synthetic evidence is visibly classified and not substituted for production proof;
- final technical video uses the same product path and is `<=5:00`;
- clean deploy/runbook and artifact provenance reproduced.

`PRODUCTION_READY` remains forbidden if any applicable hard gate/evidence class is missing.

## 5. Quantitative gate registry

These are the hard numeric gates already supported by accepted evidence/contract. No additional business/performance thresholds are invented here.

| Gate | Required value |
|---|---:|
| critical factual/source/policy hard-gate compensation | `0` |
| cross-tenant unauthorized success in defined tests | `0` |
| required run/job provenance binding missing | `0` |
| required 3×3 branch coverage | `9/9` |
| accepted join losing/duplicating branches | `0` |
| critical schema violations promoted as PASS | `0` |
| stale same-run overwrite silently accepted in selected production store/runtime | `0` |
| arbitrary untrusted server-path production input | `0` |
| private quarantine bypass in defined tests | `0` |
| secret/credential canary leak in product events/telemetry | `0` |
| restart/resume defined scenarios before production claim | `100% PASS` |
| backup/restore defined scenarios before production claim | `100% PASS` |
| final technical video | `<=5:00` |

All other quality/audience/latency/cost/capacity/retention/sampling/SLO/RTO/RPO thresholds stay `PENDING_EVIDENCE` or externally owned until supported.

## 6. Decision/evidence promotion rules per node

A `PENDING_EVIDENCE` technology can advance to a production default only when:

1. the DR record remains current for the target version/topology;
2. all applicable hard requirements pass;
3. a representative same-workload benchmark exists when the choice is testable;
4. raw observations and failures are persisted;
5. source-group correlation/missingness are preserved where relevant;
6. uncertainty is reported where meaningful;
7. hard-gate-eligible candidates are compared multidimensionally/Pareto;
8. security/reliability/cost/lock-in and migration burden are explicit;
9. no materially superior counterfactual was left unevaluated;
10. confidence and reversal conditions are recorded.

If those conditions do not identify a winner, `NO_PREFERENCE` is the correct production decision state until another implementation constraint forces a bounded choice; in that case the chosen implementation is documented as a reversible operating selection, not falsely upgraded to evidence of superiority.

## 7. Critical path and parallelizable work

After T012 acceptance, the critical path is:

`contracts → production substrate bakeoffs → toolchain freeze → vertical slice → provider/eval/live integration → reliability/security qualification → final evidence`.

Parallelizable after contract freeze:

- identity/data security bakeoff;
- parser corpus/adapters/bakeoff;
- workflow/shared-state bakeoff;
- frontend same-slice bakeoff;
- human calibration corpus preparation;
- toolchain benchmark harness preparation;
- observability backend comparison setup.

The toolchain **freeze** itself waits for the selected dependency topology; human threshold **promotion** waits for independent human evidence; production readiness waits for all applicable security/reliability/recovery gates.

## 8. Risks controlled by the DAG

- `RISK-0001` / `RISK-0010`: parser/source-trust hard gate before generation.
- `RISK-0018`: clean-environment toolchain/build/deploy/recovery evidence.
- `RISK-0021`: explicit separation between research/mechanics and production evidence.
- `RISK-0031`: adversarial authz/data/object/event/trace isolation before vertical-slice promotion.
- `RISK-0032`: production API never exposes arbitrary server paths.
- `RISK-0033`: shared-state/runtime bakeoff blocks SQLite local-state promotion.
- `RISK-0034`: technology selections stay research/benchmark gated.
- `RISK-0035`: durable events, run revisions and reconnect semantics before live UI claim.
- `RISK-0036`: human calibration/held-out work before production audience thresholds.
- `RISK-0037`: metadata-first telemetry + canary/redaction tests.
- `RISK-0038`: saturation interval/raw curves instead of invented user count.
- `RISK-0039`: hard gates remain outside optimizer and apply again after fallback/repair.
- `RISK-0040`: each research node ends in a decision state/reversal condition and feeds implementation, rather than producing documentation without action.
