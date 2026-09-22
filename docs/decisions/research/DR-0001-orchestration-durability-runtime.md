# DR-0001 — Orchestration and durability runtime for Academy Suno

- **Task:** W005-T003 / A01
- **Research date:** 2026-09-22
- **Decision state:** `PENDING_EVIDENCE`
- **Confidence:** MEDIUM on the decision state; HIGH on the observed baseline multi-replica safety gap
- **Production lock:** NONE

## 1. Decision question

Which orchestration/durability approach should back Academy Suno's production 3x3 content pipeline while preserving the existing hard invariants: exactly nine branches, lossless fan-in, branch-local quality repair, transport retry separation, crash/restart recovery, inspectable state, and safe execution when production eventually runs more than one process/replica?

The mandatory control is the current `AsyncGraphOrchestrator` + `SQLiteRunStore`. Candidates considered here are LangGraph, DBOS, and Temporal. Temporal is treated as a high-capability but high-burden candidate and must earn its complexity from workload evidence.

## 2. Workload and constraints

The representative workload is the existing 3 audiences x 3 formats graph:

1. plan exactly 9 unique jobs;
2. fan out branch generation;
3. evaluate each branch independently;
4. retry transient transport failures without confusing them with content-quality repair;
5. repair only the branch that fails a quality gate;
6. join exactly the same nine keyed outputs with no loss or duplication;
7. aggregate and durably persist terminal state;
8. resume from checkpoints after process interruption;
9. tolerate future multi-replica execution without stale whole-run writers silently overwriting each other.

Hard requirements are non-compensatory. Latency, developer ergonomics, or lower operational cost cannot compensate for branch loss/duplication, weakened hard gates, or unsafe recovery semantics.

## 3. Alternatives

### A. Mandatory baseline — custom async graph + SQLite RunStore

Current implementation in:

- `src/suno_content/orchestration/engine.py`
- `src/suno_content/orchestration/models.py`
- `src/suno_content/runstore/sqlite.py`

Strengths to test rather than assume: minimal dependencies, explicit graph/invariants, branch-local recovery behavior, append-only state history, and low migration cost because it already exists.

Material concern: the RunStore checkpoints a complete JSON run state. Sequence allocation is serialized with `BEGIN IMMEDIATE`, but there is no optimistic version/CAS assertion, per-run lease, or ownership token that prevents a stale replica from committing an older whole-run snapshot after another replica has advanced the same run.

### B. LangGraph

First-class graph/checkpoint abstraction that is close to the current graph-shaped application. Official persistence documentation positions checkpointers as thread-scoped graph-state snapshots for continuity/fault tolerance. It explicitly recommends a persistent production checkpointer such as Postgres and calls SQLite local file storage a development option.

Material questions still requiring a common harness: reducer/fan-in semantics for the exact 9-way state, branch-local retry/repair mapping, duplicate execution under concurrent workers, Postgres checkpoint write overhead, and migration complexity from the existing RunState model.

### C. DBOS

Library-based durable workflows and queues backed by Postgres. Official architecture documentation describes checkpoint/recovery from the last completed step without a separate orchestration server, while recommending Conductor in production for distributed recovery/HA and operational tooling. Official concurrent-execution documentation describes conflict detection at durable step/outcome boundaries rather than allowing two executors to silently own the same durable progression.

This makes DBOS materially relevant to the specific baseline gap because it combines a Postgres durability substrate with explicit distributed-execution conflict semantics. It is not promoted here because no Academy Suno adapter has yet run the identical 9-way harness.

### D. Temporal

Dedicated durable-execution platform with SDK, workers, task queues, persisted workflow history, replay, and explicit Activity retry policy. Official documentation requires workflow code to remain deterministic and places failure-prone/non-deterministic operations such as API/LLM calls in Activities. This cleanly separates orchestration state from failure-prone side effects, but it also implies the largest migration and operational surface among the candidates considered.

Temporal is therefore not selected merely because it has strong durability semantics; it must demonstrate a workload benefit sufficient to justify the service/worker/task-queue model.

## 4. Evaluation criteria

Criteria were fixed before interpreting the observed results. No aggregate score is used.

| Criterion | Type | Evidence sought |
|---|---|---|
| Exact 9/9 fan-out + lossless join | hard gate | deterministic workload runs |
| No branch loss/duplication | hard gate | repeated execution + failure probes |
| Transport retry separated from quality repair | hard gate | injected transport + quality failures |
| Checkpoint/resume correctness | hard gate | pause/recreate runtime/resume |
| Process crash/restart recovery | hard gate | separate-process restart probe |
| Same-run multi-replica safety | hard gate for production HA | stale/concurrent-writer conflict probe or runtime guarantee |
| Independent-run concurrency | supporting | concurrent writers/runs |
| Orchestration/storage overhead | quantitative | repeated p50/p95 runtime, checkpoint count |
| State inspection / live operations | operational | official runtime capabilities + harness |
| Dependency/infrastructure burden | operational | required DB/services/control plane |
| Migration cost | engineering | semantic/code-model changes |
| Security/cost/lock-in | production | required services, data stores, access boundaries, coupling |

## 5. Systematic source search

### Search strategy

Primary sources were searched first on 2026-09-22 using these categories:

- `[runtime] persistence checkpoints production postgres sqlite`;
- `[runtime] crash restart durable execution recovery`;
- `[runtime] retry policy activities workflow deterministic`;
- `[runtime] concurrent execution multi executor conflict`;
- `[runtime] queues workers distributed recovery observability`;
- Academy Suno source, tests, CI workflow, and observed CI artifacts.

The current repository implementation and clean-checkout CI are treated as the primary source for baseline behavior. Vendor/framework official documentation is used only for documented candidate semantics. No candidate benchmark number from a vendor or unrelated workload is used as a substitute for an Academy Suno common-harness measurement.

### Stopping rule

Search stopped when primary documentation covered persistence, recovery, retry placement, distributed execution, and operational topology for each material candidate, and further documentation could not resolve the remaining decision uncertainty: there is still no identical Academy Suno runtime harness executed against pinned LangGraph, DBOS, and Temporal installations with a production-capable shared state backend. That missing experiment, not additional prose research, is now the decision bottleneck.

## 6. Source table

| Source | Type / date | Authority | Claim supported | Limitation |
|---|---|---|---|---|
| `src/suno_content/orchestration/engine.py` in this repo | primary code / observed 2026-09-22 | Academy Suno implementation | explicit 9-way invariant, lossless join, branch-local repair, transport retry, checkpoints | custom implementation only |
| `src/suno_content/runstore/sqlite.py` in this repo | primary code / observed 2026-09-22 | Academy Suno implementation | append-only history + whole-state checkpoint; no CAS/lease field | code inspection must be combined with concurrent probe |
| `tests/orchestration/test_async_graph.py` | primary test / observed 2026-09-22 | Academy Suno tests | 9/9, retry/repair separation, resume, duplicate-key protection | test suite does not model multi-replica same-run writes |
| PR #169 Foundation Regression run `35727769348`, artifact `10694266553` | primary execution / 2026-09-22 | clean GitHub Actions run | observed repeated baseline metrics and failure/recovery probes | Ubuntu hosted runner; synthetic provider callbacks |
| https://docs.langchain.com/oss/python/langgraph/persistence | official docs / accessed 2026-09-22 | LangChain | checkpointers persist graph state for continuity/fault tolerance; Postgres is a persistent production option; SQLite is local-file development storage | does not prove Academy Suno fan-in/reducer or multi-worker behavior |
| https://docs.temporal.io/ | official docs / accessed 2026-09-22 | Temporal | platform durable execution resumes through crash/network/infrastructure failures | product-level claim; workload integration still required |
| https://docs.temporal.io/develop/python | official docs / accessed 2026-09-22 | Temporal | Python architecture uses Workflows, Activities, Workers, platform primitives | no Academy Suno migration measurement |
| https://docs.temporal.io/encyclopedia/retry-policies | official docs / accessed 2026-09-22 | Temporal | Activities retry by default; workflow code must be deterministic; API/LLM calls belong in Activities | defaults require deliberate limits for this workload |
| https://docs.dbos.dev/architecture | official docs / accessed 2026-09-22 | DBOS | Postgres-backed durable workflows/queues; checkpoint recovery; no separate orchestration server; Conductor recommended for production HA/ops | no Academy Suno adapter benchmark |
| https://docs.dbos.dev/production/workflow-recovery | official docs / accessed 2026-09-22 | DBOS | distributed recovery needs executor identity/coordination or Conductor | operational control plane still exists for strong HA |
| https://docs.dbos.dev/explanations/concurrent-executions | official docs / accessed 2026-09-22 | DBOS | conflicting concurrent executions are detected at checkpoints/outcomes instead of silently both committing progression | documented semantics not yet reproduced in this workload |

## 7. Reproducible experiment

### Harness

`experiments/orchestration_smoke/durability_probe.py` was added and wired into the existing clean-checkout foundation regression. It executes the actual production `AsyncGraphOrchestrator` and `SQLiteRunStore`, not a separate toy implementation.

Injected conditions:

- exactly nine deterministic jobs;
- one transient transport timeout on `advanced:short_video`;
- one content-quality repair on `beginner:carousel`;
- pause after all branches and recreate the runtime before resume;
- a child process that exits after persisted branch completion, followed by recovery in a fresh parent runtime;
- eight independent run writers sharing one SQLite file;
- two separate RunStore connections that both load the same run version and then checkpoint conflicting whole-run snapshots.

Synthetic callbacks intentionally remove model/provider latency so the number measures orchestration/storage overhead. This is not an end-user request-latency benchmark.

### Clean-checkout environment

Observed in Foundation Regression for PR #169:

- Python 3.13.15;
- Ubuntu 24.04 hosted runner;
- pinned shared gate dependencies: Pydantic 2.13.4 and pytest 9.0.2;
- LangGraph not installed in this shared foundation gate;
- DBOS and Temporal also not installed by the gate;
- all pre-existing critical regression suites passed.

Raw observed record: `experiments/orchestration_bakeoff/w005_t003_a01_raw_results.json`.

## 8. Raw results and uncertainty

### Baseline repeated run

15 repetitions of the production baseline all satisfied 9/9 with no observed loss/duplication, one isolated quality repair, and one isolated transport retry.

| Metric | Observed |
|---|---:|
| repetitions | 15 |
| joined outputs | 9/9 every run |
| history snapshots | 28 every run |
| runtime min | 39.283 ms |
| runtime p50 | 46.236 ms |
| runtime p95 | 64.228 ms |
| runtime max | 89.156 ms |

The max outlier is reported rather than discarded. No significance claim is made from 15 synthetic local-I/O repetitions.

### Checkpoint/resume

- paused state: `branches_complete`;
- resumed terminal state: `complete`;
- joined outputs: 9;
- generator calls after resume: unchanged;
- repair calls after resume: unchanged;
- result: PASS.

### Process restart

A spawned child process persisted `branches_complete` and exited. A fresh runtime in the parent loaded the same database and resumed to `complete` with 9 outputs, zero new generator calls, and zero new repair calls. Result: PASS.

### Independent-run shared-file concurrency

Eight writers, each with a distinct run id, wrote 20 checkpoints to the same SQLite file. Every run retained the expected 21 history rows (create + 20 checkpoints). Result: PASS for this same-host/local-file scope.

This is explicitly **not** evidence for a network filesystem or multiple hosts.

### Same-run stale-write probe

Two separate connections loaded the same initial `shared-run` state before either checkpointed. Each appended a different replica mark, then both checkpoint calls succeeded with sequences 2 and 3. The final whole-run JSON contained only one mark.

Observed outcome: `lost_update_observed = true`.

Interpretation: SQLite serialized checkpoint sequence allocation correctly; the unsafe behavior is the RunStore's application-level whole-state last-writer-wins contract. The current baseline has no compare-and-swap version check or lease/ownership mechanism to reject a stale same-run writer.

This fails the future production multi-replica safety requirement as currently implemented.

### Challenger runtime evidence

LangGraph, DBOS, and Temporal were **not** executed in this clean shared gate. Adding unselected orchestration stacks and infrastructure to the foundation CI solely to make this task produce benchmark numbers would itself preselect dependencies and distort the comparison. Therefore no challenger latency/cost number is inferred.

The existing optional LangGraph smoke reports `UNAVAILABLE: No module named 'langgraph'`, which is evidence of missing runtime coverage, not evidence against LangGraph.

## 9. Comparative findings

| Dimension | Current async + SQLite | LangGraph | DBOS | Temporal |
|---|---|---|---|---|
| Academy 9/9 observed | PASS (15/15 here) | not observed in this task | not observed in this task | not observed in this task |
| Resume/restart observed | PASS | not observed | not observed | not observed |
| Same-run concurrent ownership | FAIL in current RunStore probe | production checkpointer exists; exact contender behavior pending common harness | docs describe checkpoint conflict handling | durable history/replay model documented; exact contender harness pending |
| Transport vs quality retry mapping | explicit and observed | needs adapter policy | steps/retry mapping needs adapter | Activities provide explicit failure/retry boundary |
| Production state backend | local SQLite today | official docs point to PostgresSaver for persistent production use | Postgres | Temporal Service persistence |
| Distributed recovery/control | custom work required | depends on deployment/checkpointer/runtime topology | executor coordination; Conductor recommended for HA | built into Temporal service/worker model |
| Operational footprint | lowest today | library + production DB/checkpointer; possible server platform depending deployment | library + Postgres; Conductor recommended for HA/ops | SDK + Temporal Service/Cloud + workers/task queues |
| Migration surface | none, but safety gap must be fixed | graph/state/checkpoint adapter rewrite | workflow/step annotation + DBOS state/queue model | workflow/activity split + deterministic workflow constraints + service operations |
| External lock-in | low vendor lock-in, high custom maintenance | framework state/checkpoint APIs | DBOS workflow/step APIs + system schema/control plane | Temporal workflow/activity/history/service semantics |

No single winner can be established from this table because only the baseline has workload-specific runtime measurements. Architecture documentation can rule out invalid assumptions, but cannot substitute for a controlled benchmark.

## 10. Security, reliability, cost, and lock-in

### Security

All candidates persist workflow state that may include source metadata or generated content. The task did not test encryption, RBAC, secrets handling, network isolation, or tenant boundaries. Any production promotion therefore needs storage/service access controls assessed in the platform/storage decision tasks. The current SQLite file is especially unsuitable as a proxy for production multi-host access control.

### Reliability

- Baseline: good single-process restart behavior; explicit same-run stale-write safety gap reproduced.
- LangGraph: production persistence primitives documented; Academy-specific concurrent ownership semantics not yet measured.
- DBOS: documented conflict handling and distributed recovery model closely address the reproduced gap; common-harness verification is still required.
- Temporal: strongest service-level durable workflow model among these alternatives on paper, but introduces deterministic workflow/activity constraints and the most additional moving parts.

### Cost / operational burden

No vendor price estimate is used as a deciding score because deployment choices are not yet fixed. Infrastructure surface is nevertheless materially different:

- baseline: process + local SQLite today, but a production-safe shared store/ownership mechanism must be added;
- LangGraph: application library plus a production persistent checkpointer such as Postgres;
- DBOS: application library + Postgres, with Conductor recommended for production HA/operations;
- Temporal: application SDK + Temporal Service (self-hosted or Cloud) + worker fleet/task queues.

### Lock-in

The custom baseline avoids framework vendor coupling but transfers orchestration correctness and operations maintenance to this repository. LangGraph, DBOS, and Temporal progressively introduce framework/runtime contracts. Temporal's workflow/activity replay semantics are the largest conceptual migration; DBOS is closer to ordinary Python call structure; LangGraph is closest to the existing graph vocabulary. These are migration observations, not a winner score.

## 11. Decision

**Decision: `PENDING_EVIDENCE`.**

Do **not** lock the current SQLite-backed baseline as the production multi-replica runtime, because the same-run stale-write probe demonstrated a silent lost update. Also do **not** lock LangGraph, DBOS, or Temporal from documentation alone because none has yet passed the identical Academy Suno 9-way, failure, resume, and concurrent-ownership harness under a production-capable shared state backend.

The existing `AsyncGraphOrchestrator` remains the mandatory behavioral control and reference implementation until a challenger proves at least equivalent hard-gate behavior. This is a hold-the-baseline decision, not a production endorsement of SQLiteRunStore.

### Confidence

- **HIGH** that current `SQLiteRunStore` is unsafe for concurrent same-run writers without additional ownership/version control: deterministic probe reproduced a lost update and code inspection explains the mechanism.
- **MEDIUM** that `PENDING_EVIDENCE` is the correct framework-level decision: candidate primary docs are sufficient to identify material alternatives and migration/ops differences, but not to establish a workload winner.

## 12. Reversal / closure conditions

This decision can advance from `PENDING_EVIDENCE` only after a follow-up common-harness experiment does all of the following:

1. pin exact candidate package/runtime versions;
2. implement minimal Academy adapters for at least LangGraph and DBOS; include Temporal if its operational hypothesis remains material after the lighter candidates are tested;
3. use a production-capable shared state backend/topology (for LangGraph/DBOS, Postgres where their production docs require/recommend it; for Temporal, a real local test service or controlled Cloud environment);
4. run the exact 9-way workload and injected transport/quality failures;
5. test process crash and restart at more than one graph boundary;
6. run two workers/replicas against the same logical run and verify duplicate/lost-update behavior explicitly;
7. record p50/p95, checkpoint/state-write counts, failure outcomes, and operational setup commands across multiple repetitions;
8. preserve all hard gates with no relaxation.

A challenger may be locked only if it clears those hard requirements and its reliability/operational benefit justifies migration cost. Temporal must additionally show a benefit not already achieved by a lower-burden candidate.

A custom-baseline path remains viable only if the RunStore gains an explicit same-run ownership/CAS contract on a production shared backend and then passes the same concurrent-worker probes.

## 13. Migration implications

If a challenger is later selected, preserve the current `RunState`/job ids as an external compatibility and audit model rather than silently replacing trace semantics. The migration should map:

- `run_id` -> candidate durable workflow/thread identity;
- branch `job_id` -> durable child/step identity;
- transport retries -> retryable side-effect/activity/step policy;
- quality repair -> application-level branch loop, never transport retry;
- `REVIEW_REQUIRED` -> durable suspended/interrupt state;
- lossless join -> explicit keyed nine-result invariant before aggregation;
- current append-only history -> candidate event/checkpoint visibility or an exported audit projection.

A migration must not reinterpret a failed hard gate as a retryable infrastructure error.

## 14. Traceability

Production references from dispatch:

- `PROD-003`
- `PROD-006`
- `PROD-010`
- `PROD-013`
- `PROD-016`

Risks from dispatch:

- `RISK-0033`
- `RISK-0034`
- `RISK-0039`

Artifacts:

- `experiments/orchestration_smoke/durability_probe.py`
- `experiments/orchestration_smoke/benchmark.py`
- `experiments/orchestration_bakeoff/w005_t003_a01_raw_results.json`
- GitHub PR #169 / Foundation Regression run `35727769348` / artifact `10694266553`

The canonical coordination state is intentionally not modified by this worker task.
