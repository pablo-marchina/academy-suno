# W005-T008 — Load, failure and recovery benchmark plan

`TASK: W005-T008-A01`
`STATUS: PROPOSED_EXECUTABLE_PLAN`
`PRODUCTION_READY_EVIDENCE: NOT_YET_EXECUTED`
`CAPACITY_TARGET: UNKNOWN`
`SLO_SLA_TARGETS: UNKNOWN`
`RTO_RPO_TARGETS: UNKNOWN`

## Purpose

Provide a reproducible benchmark/recovery protocol for candidate production topologies without inventing capacity or service-level claims. The plan is designed to be implemented by Phase 9 after T010/T012 choose the candidate runtime/persistence stack, and can also be used in bounded W005 spikes.

The plan measures the real Academy Suno product path: accepted request/upload -> durable run identity -> document/source grounding -> 3 audiences x 3 formats -> eval/repair -> aggregate -> persisted/auditable result. Tests may substitute controlled provider fault injectors where the scenario explicitly targets reliability rather than model quality, but such runs must be labeled and cannot be represented as real-provider production evidence.

## 1. Preconditions

Before a capacity/recovery run, persist an experiment manifest containing:

- git commit SHA and image/build identity;
- deployment candidate/topology identifier;
- environment and region/host class without credentials;
- replica/process counts and resource requests/limits where applicable;
- API and worker concurrency settings;
- database/queue/object-store candidate and connection/pool limits;
- provider mode and explicit real-vs-stub/fault-injector evidence class;
- dataset/document corpus version and source hashes;
- evaluator/prompt/policy versions when real workflow execution is used;
- migration/schema version;
- telemetry configuration and redaction mode;
- load-generator version/config;
- experiment start/end timestamps.

Minimum functional preflight:

1. a single real logical run can be created and observed end-to-end;
2. request/run/job/tenant correlation IDs are present in the chosen telemetry path;
3. queue wait/backlog metrics exist if asynchronous work is present;
4. resource and dependency metrics are observable;
5. every accepted run reaches a durable terminal or explicitly recoverable state;
6. destructive tests run only in an isolated test environment with disposable/non-sensitive data.

If a required metric is missing, the benchmark records `OBSERVABILITY_GAP` rather than inferring it.

## 2. Workload profiles

Use versioned profiles instead of an undefined “user”. Initial profiles:

- `P-CONTROL`: create/status/list/read operations with minimal workflow work;
- `P-RUN`: submit one representative document and execute the complete 3x3 workflow;
- `P-MIXED`: a declared mixture of control-plane reads/writes and long runs;
- `P-BURST`: short impulse of run submissions above the last stable admission rate;
- `P-RECOVERY`: active persisted runs specifically selected for failure/restart tests.

Exact document mix and traffic proportions are inputs, not hidden defaults. If partner traffic facts remain unavailable, results are bounded to the synthetic benchmark profile and must not be translated directly into “users supported”.

## 3. Core metrics schema

Persist raw time series/events and a summary row per stage.

Required summary fields:

```text
experiment_id
candidate_id
profile_id
stage_id
run_start_utc
run_end_utc
offered_rate
admitted_rate
completed_rate
dropped_or_rejected_rate
api_latency_p50_ms
api_latency_p95_ms
api_latency_p99_ms
queue_wait_p50_ms
queue_wait_p95_ms
queue_wait_p99_ms
run_duration_p50_ms
run_duration_p95_ms
run_duration_p99_ms
error_rate
retry_rate
timeout_rate
cancellation_rate
queue_depth_max
oldest_work_age_max_ms
api_replica_min
api_replica_max
worker_replica_min
worker_replica_max
cpu_peak
memory_peak
db_pool_peak
db_wait_peak_ms
provider_429_count
provider_5xx_count
provider_timeout_count
accepted_runs
accepted_branches
lost_accepted_branches
duplicate_accepted_branches
provenance_missing_count
cost_observed
hard_gate_result
notes
```

Fields not available for a candidate must be explicit `NA` with reason; do not silently drop them.

## 4. Load execution matrix

### LOAD-00 — Harness validation

- Run one low-load representative logical workflow.
- Verify all expected correlation IDs and metrics exist.
- Verify the expected 3x3 branch identities are countable when the profile is a full run.
- Gate: no capacity conclusion may be drawn from this stage.

### LOAD-01 — Repeated low-load baseline

- Execute the representative profile repeatedly at low load.
- Capture latency/resource/provider/cost distributions and variance.
- Repeat enough times to expose run-to-run variance; T009 may set the final statistical minimum. Persist all raw samples rather than reporting only a mean.

### LOAD-02 — Closed-model concurrency ladder

- Increase concurrent logical clients/jobs monotonically: a small geometric or otherwise predeclared ladder is acceptable.
- Hold each step long enough to pass warmup and observe whether queue/resource metrics settle.
- At each step measure all core metrics and correctness hard gates.
- Stop or reduce load if safety ceilings on provider quota, database connections, cost, or environment health are approached.

Output: concurrency curve and the highest stable/first unstable observed steps.

### LOAD-03 — Open-model arrival-rate staircase

- Drive submissions at a controlled arrival rate independent of response time.
- Increase offered rate in predeclared steps.
- Record offered/admitted/completed/dropped rates separately.
- Observe queue depth and oldest-work age; do not hide dropped iterations/admission rejection.

Output: offered-vs-completed throughput curve and queue/tail-latency behavior.

### LOAD-04 — Burst / impulse

- From a stable steady state, submit a bounded short burst above the stable rate.
- Observe admission control, queue growth, retry amplification and time to return to the reference state.
- Gate: correctness invariants remain hard; overload may degrade latency but may not silently lose or duplicate accepted work.

### LOAD-05 — Soak

- Run below the observed saturation region for a longer window.
- Inspect memory/resource drift, queue-age drift, connection leakage, retry/error trends and autoscaling churn.
- Exact duration is an experiment parameter. Any duration used must be reported; it is not an availability claim.

### LOAD-06 — Controlled saturation

- Intentionally cross the last stable region within configured cost/quota safeguards.
- Identify which resource or downstream dependency first constrains useful throughput.
- Verify overload controls: bounded admission, queue, retries and downstream concurrency.
- Gate: stop on correctness failure, unsafe quota approach or uncontrolled retry/cost amplification.

### LOAD-07 — Post-saturation recovery

- Return to a previously stable load.
- Compare latency, throughput, resource use and queue age against pre-saturation behavior.
- Record whether operator/manual action was required.

## 5. Saturation reporting

Report capacity as observations, not a guessed target:

- `LAST_STABLE_OFFERED_LOAD`
- `FIRST_UNSTABLE_OFFERED_LOAD`
- `SATURATION_INTERVAL`
- `DOMINANT_LIMITER`
- `CONFIDENCE / REPEATABILITY`
- `PROFILE_ID`
- `ENVIRONMENT_ID`

A strong production capacity claim additionally requires the workload profile to be justified as representative and the result to be repeated under the selected production-equivalent environment.

## 6. Failure injection matrix

### FAIL-API-01 — API replica/process loss

Setup: active requests and at least one accepted durable run.

Injection: terminate one API process/replica without graceful application shutdown.

Observe:

- connection/request failures;
- readiness/routing behavior;
- run state persistence;
- duplicate submission behavior when the client retries;
- whether replacement capacity appears when the topology claims it.

Pass invariant: accepted durable run identity/state is not lost; retries obey idempotency. If the candidate claims redundant API serving, another ready replica must continue serving within measured—not predeclared—recovery timing.

### FAIL-WORKER-01 — Worker loss mid-run

Injection: kill the worker while a full 3x3 run is active.

Pass invariant:

- no duplicate accepted logical branch/output;
- persisted run/job state remains attributable;
- system resumes, safely retries, or enters an explicit recoverable/blocked terminal state according to the candidate contract;
- no false `PASS` completion if work was lost.

### FAIL-DB-01 — Durable persistence outage

Injection: make the shared database/store temporarily unavailable.

Pass invariant:

- no false success;
- retries are bounded;
- admission/backpressure behavior is observable;
- recovery does not create duplicate accepted state.

### FAIL-QUEUE-01 — Queue/broker outage (when present)

Pass invariant: accepted jobs are either durably retained or the admission operation fails/defer-signals clearly; no silently lost accepted job.

### FAIL-STORE-01 — Source/object-store outage

Pass invariant: source-dependent execution fails closed or pauses according to contract; no arbitrary local-path/fabricated-content fallback.

### FAIL-PROVIDER-01 — Provider throttling/transient failure

Inject controlled 429, 5xx, timeout and high-latency behavior.

Pass invariant:

- retry budget/concurrency cap prevents unbounded amplification;
- permanent failure remains explicit;
- critical factual/source/policy gates are not bypassed;
- queue/admission pressure is observable.

### FAIL-TELEMETRY-01 — Telemetry backend/export failure

Pass invariant: loss of the observability backend does not corrupt product state; telemetry loss/export backlog is detectable if the candidate claims durable/buffered telemetry.

## 7. Deploy and migration drills

### DEPLOY-01 — Rolling restart / deploy

Run active workload while replacing application version/replicas.

Record:

- request errors;
- readiness changes;
- active-run outcomes;
- version identifiers on spans/events;
- queue/backlog behavior;
- manual interventions.

Pass invariant: accepted durable state persists. Cross-version compatibility must be demonstrated, or the deployment contract must explicitly serialize/drain incompatible work.

### MIGRATION-01 — Schema migration rehearsal

- Run migration as a controlled one-shot operation.
- Test the declared forward/rollback or forward-fix path.
- Verify replicas do not race the migration independently.
- Test old/new application compatibility if rolling deployment is claimed.

No migration strategy is considered proven by “migration command exited 0” alone; application reads/writes must be validated after the transition.

## 8. Restart/resume drill

### REC-RESTART-01

1. create representative runs and persist their run/job/branch identities;
2. interrupt the application/worker layer while at least one run is active;
3. restart/redeploy using the same durable dependencies;
4. query run state before manually resubmitting anything;
5. allow the designed resume/retry mechanism to operate;
6. compare pre/post branch identities and accepted outputs;
7. validate provenance and terminal state.

Binary pass for each defined scenario requires:

- no accepted run disappears;
- no accepted branch identity is lost or duplicated;
- terminal state is valid and attributable;
- any re-execution is represented as retry/attempt provenance rather than a silent duplicate.

The Production Contract requires `100% PASS` across the defined restart/resume scenario set before a production-ready claim.

## 9. Backup/restore drill

### REC-BACKUP-01

A backup is not evidence until restored.

1. capture a backup/snapshot using the candidate-supported method;
2. record source system/version/schema/time and backup identity/checksum where available;
3. provision a clean production-equivalent restore target;
4. restore without relying on the original runtime's mutable local state;
5. run integrity/count/hash checks for the selected dataset/run records/artifacts;
6. start the application against the restored state;
7. query prior runs and execute a bounded new validation transaction/run;
8. record measured restore duration and any data gap relative to the backup point.

Binary pass requires the declared restore dataset to be internally consistent and usable by the application. The Production Contract requires `100% PASS` for the defined backup/restore scenario set before a production-ready claim.

Observed restore time/data gap are evidence; target RTO/RPO remain `UNKNOWN` until approved business/operating requirements exist.

## 10. Correctness hard gates under load

Performance never compensates for these properties:

- required full-run branch coverage remains `9/9` where the full workflow is expected;
- lost or duplicate accepted branches = `0`;
- required provenance missing = `0`;
- false PASS after a critical schema/source/policy failure = `0`;
- retry/replay does not create a second accepted logical result for an idempotent operation;
- defined restart/resume and backup/restore scenarios are all PASS before a production-ready claim.

If a hard gate fails at any load step, mark that step `CORRECTNESS_UNSTABLE` even if throughput remains high.

## 11. Autoscaling validation

For any autoscaled candidate, persist the exact policy and compare demand to replica changes.

API tier:

- test request/concurrency/CPU or equivalent trigger behavior;
- verify scale-out latency and maximum-instance/concurrency limits;
- verify downstream pools/quotas remain protected.

Worker tier:

- prefer job backlog/oldest-work age or equivalent demand signal when asynchronous work dominates;
- compare scaling response to queue growth and provider/database limits;
- verify scale-in does not abandon leased/in-flight work.

CPU-only worker scaling must not be assumed sufficient without evidence; I/O-bound/provider-bound workers can queue while CPU remains low.

## 12. Health/restart validation

Health semantics should distinguish:

- startup: process has initialized enough to be probed;
- readiness: instance can safely accept new traffic/work;
- liveness: process is irrecoverably unhealthy enough that restart is beneficial.

Test slow startup and overload separately. A saturated dependency must not cause aggressive liveness settings to convert overload into a restart storm.

## 13. Tooling candidates

No load/chaos tool is production-selected by this task.

A minimal implementation can use:

- an HTTP/open-arrival harness such as k6 for API/admission traffic;
- a project-specific Python driver for long-running run-state assertions, 3x3 identity/provenance and recovery verification;
- platform/container process termination and dependency proxies/fault stubs for initial failure injection;
- candidate-native metrics plus the telemetry stack selected by T007/T010.

A dedicated chaos framework is optional until its complexity yields additional coverage.

## 14. Result bundle

Each benchmark execution should persist:

```text
artifacts/benchmarks/<experiment_id>/manifest.json
artifacts/benchmarks/<experiment_id>/summary.json
artifacts/benchmarks/<experiment_id>/stage_metrics.csv
artifacts/benchmarks/<experiment_id>/events.jsonl
artifacts/benchmarks/<experiment_id>/failure_matrix.json
artifacts/benchmarks/<experiment_id>/recovery_report.md
```

If raw telemetry is stored externally, persist immutable references and retention/provenance metadata.

## 15. Promotion gates

Before a candidate can support `PRODUCTION_READY` on reliability/capacity/deployment grounds:

- load curve executed on a representative declared workload;
- saturation interval and dominant bottleneck documented;
- p50/p95/p99, throughput, queue/admission, error/retry and resource data persisted;
- no unsupported “N users”, latency SLO or cost claim;
- all defined restart/resume scenarios PASS;
- all defined backup/restore scenarios PASS;
- deploy/startup/readiness/liveness/migration behavior reproduced;
- hard correctness gates hold under tested load/failure conditions;
- environment/build/config provenance is reproducible;
- operational cost/burden and unknowns are stated;
- DRG record includes reversal conditions.

## 16. Current non-claims

This task has designed the benchmark; it has **not** executed production-equivalent load or recovery tests because the production deployment/runtime/persistence candidates are not yet selected by T010/T012.

Therefore:

- saturation point: `NOT_MEASURED`;
- supported concurrent users: `NOT_CLAIMED`;
- production SLO/SLA: `UNKNOWN`;
- RTO/RPO targets: `UNKNOWN`;
- cloud/runtime winner: `NONE`;
- production-ready reliability evidence: `NOT_ESTABLISHED`.
