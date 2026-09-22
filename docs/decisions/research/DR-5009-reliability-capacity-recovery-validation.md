# DR-5009 — Reliability, capacity and recovery validation method

`STATUS: DECISION_PROPOSAL`
`TASK: W005-T008-A01`
`RESEARCH_DATE: 2026-09-22`
`DECISION: COMBINED_OPEN_AND_CLOSED_LOAD_MODEL + CONTROLLED_FAILURE_INJECTION + RESTORE_DRILL`
`CONFIDENCE: HIGH for methodology / LOW for any future numeric production target until measured`

## 1. Decision question

What validation method should Academy Suno use to establish production capacity, overload behavior, restart/resume reliability and backup/restore evidence without inventing user-count, latency, SLO, RTO or RPO claims?

This record chooses a **measurement method**, not numeric production targets and not a deployment vendor.

## 2. Workload / constraints

The production contract requires increasing-load curves, p50/p95/p99-style operational evidence, failure/retry testing, restart/resume, backup/restore and a documented saturation point. Current concurrency, SLO/SLA, business RTO/RPO and external deployment target are unknown.

The workload is mixed:

- short request/control-plane operations such as upload/start/status/read;
- long-running document-to-3x3 work with provider calls, evaluation and repair;
- potentially asynchronous work whose useful capacity is governed by queue age/backlog, worker throughput and downstream provider/database limits rather than HTTP throughput alone;
- hard correctness invariants (branch identity, provenance, no duplicate accepted result, recoverable run state) that cannot be traded for throughput.

## 3. Alternatives

### A — Closed-model virtual-user test only

A fixed number of users/clients waits for each request before issuing the next. This is simple and useful for concurrency/resource interaction, but coordinated waiting can hide overload and it does not directly represent an offered arrival rate.

Disposition: `RETAIN_AS_ONE_VIEW`, not sufficient alone.

### B — Open-model arrival-rate staircase only

Requests/jobs arrive at a controlled rate independent of response time. k6's arrival-rate executors are a representative implementation of this model. It exposes dropped/unscheduled work and makes queue growth visible under overload.

Disposition: `RETAIN_AS_ONE_VIEW`, not sufficient alone because the product also has stateful user/run concurrency and long-job occupancy effects.

### C — Production traffic replay/shadow only

Replay or shadow real production traffic can be highly representative, but there is no production traffic source or approved privacy boundary yet. It also cannot safely replace deliberate beyond-saturation and destructive recovery tests.

Disposition: `PENDING_FUTURE_EVIDENCE`, not available as the primary W005 method.

### D — Combined closed + open load tests, controlled failure injection and explicit restore drill

Use both concurrency-oriented and arrival-oriented stages, then inject dependency/process failures and perform a restore into a clean environment. Keep hard correctness gates independent from latency/throughput optimization.

Disposition: `SELECTED_METHOD` for T010/T012 consideration.

## 4. Evaluation criteria

The method must:

1. expose tail latency and queueing under rising demand;
2. find a bounded saturation region rather than claim an arbitrary user count;
3. distinguish offered load from completed throughput;
4. expose dropped/admission-rejected work instead of hiding it;
5. correlate resource saturation and downstream limits with run/job/request IDs;
6. prove restart/resume and backup/restore with binary scenario evidence;
7. test retry amplification/backpressure under dependency degradation;
8. preserve correctness hard gates under overload;
9. produce raw data that can be rerun and compared across deployment candidates;
10. keep SLO, RTO, RPO and budget targets `UNKNOWN` until owner/business evidence exists.

## 5. Required measurement set

At every load stage record, where applicable:

- latency distributions: p50, p95, p99 for API operations, queue wait, job/run completion and important downstream calls;
- offered rate, admitted rate, completed throughput and dropped/rejected rate;
- queue depth and oldest-work age/queue delay;
- success, validation error, timeout, cancellation, retry and permanent-failure rates;
- retry attempts per logical operation and duplicate-delivery/idempotency outcomes;
- CPU, memory, process/thread pressure, file descriptors, network and container/node throttling where exposed;
- database pool usage, active connections, lock/wait symptoms and storage latency;
- worker active/idle count and per-worker concurrency;
- provider latency, 429/5xx/timeouts and concurrency/rate-limit signals;
- replica counts and scale-out/scale-in events;
- cost when available: idle cost, test-window cost and cost per completed logical run;
- correctness: accepted branch count, duplicate/lost accepted outputs, provenance binding and terminal state;
- recovery: detection time, service-unavailable interval, run resume/retry result, measured data loss if any and restore duration.

OpenTelemetry-compatible trace/log correlation is an implementation candidate, not selected here; whichever telemetry stack is used must correlate request/run/job/tenant dimensions without leaking protected content.

## 6. Saturation-point method

Do **not** report “supports N users” unless a representative user-workload model and confidence basis exist.

Instead report a **saturation interval**:

`[highest observed stable offered load, first observed unstable offered load]`

A step is unstable when one or more of these conditions is reproducibly observed:

- completed throughput no longer increases materially while offered load rises and queue age/backlog continues to grow without recovery;
- tail latency/queue time diverges over the measurement window rather than settling;
- admission drops/timeouts/retry amplification rise because a resource/downstream hard limit is reached;
- a correctness hard gate fails;
- a declared resource or dependency quota reaches its safe operating bound.

The precise statistical change-point rule may be refined by W005-T009. Until then the raw curve, repeated observations and uncertainty band must be preserved; a single noisy step is not a strong capacity claim.

## 7. Load stages

Stage names are stable; exact durations and step sizes are harness parameters, not SLOs.

| Stage | Purpose | Load shape | Required result |
|---|---|---|---|
| `L0_VALIDATE` | verify harness + telemetry | single logical run | all metrics/correlation fields observable |
| `L1_BASELINE` | measure isolated service/runtime cost | low steady load | raw latency/resource/cost baseline |
| `L2_CONCURRENCY_LADDER` | expose occupancy/contention | closed-model increasing concurrency | curve until first instability or configured safety ceiling |
| `L3_ARRIVAL_STAIRCASE` | expose admission/queue behavior | open-model increasing arrival rate | offered/admitted/completed/drop + queue curve |
| `L4_BURST` | impulse overload/recovery | short burst above stable load | bounded queue/rejection and recovery behavior |
| `L5_SOAK` | expose leaks/slow degradation | long hold below saturation | memory/queue/error drift or stable behavior |
| `L6_CONTROLLED_SATURATION` | observe failure boundary | limited step above last stable region | saturation mechanism identified without uncontrolled blast radius |
| `L7_POST_RECOVERY` | verify return to service | stable reference load | compare with pre-failure baseline |

Recommended initial harness defaults for an experiment implementation may use short warmup/measurement windows and then lengthen them based on observed variance; these defaults are not production objectives. T009 should own final sampling/CI policy.

## 8. Failure and recovery scenarios

Each scenario must have a predeclared invariant and binary scenario outcome in addition to quantitative timing.

| ID | Injection / drill | Required invariant |
|---|---|---|
| `FAIL-API-01` | terminate one API replica during active requests | accepted durable run state remains queryable; other ready replica(s) serve when topology claims redundancy |
| `FAIL-WORKER-01` | terminate worker during a 3x3 run | run reaches safe retry/resume/blocked terminal behavior; no duplicate accepted branch/result |
| `FAIL-DB-01` | make durable DB temporarily unavailable | bounded retries/backpressure; no false success; recovery is observable |
| `FAIL-QUEUE-01` | make queue/broker unavailable where present | no silently lost accepted job; admission/defer/failure contract is explicit |
| `FAIL-STORE-01` | object/source store unavailable | source-dependent execution fails closed; no fabricated content/path fallback |
| `FAIL-PROVIDER-01` | inject 429/5xx/timeouts/latency | retry budget/bounded concurrency protects the system; hard gates remain enforced |
| `FAIL-OTEL-01` | telemetry backend unavailable | telemetry loss does not corrupt product state; loss is itself detectable if architecture claims buffered export |
| `DEPLOY-01` | rolling restart/deploy | version transition preserves accepted state and compatible requests/jobs, or deployment is explicitly serialized |
| `MIGRATION-01` | migration rehearsal with rollback/failure path | schema transition is controlled and does not race per replica |
| `REC-RESTART-01` | full application restart/redeploy with active persisted run | defined run resumes/retries to a valid terminal state with provenance |
| `REC-BACKUP-01` | restore a captured backup into clean production-equivalent environment | declared dataset/run artifacts can be verified and used; integrity checks pass |

`REC-RESTART-01` and `REC-BACKUP-01` must be `100% PASS` for the defined scenarios before a production-ready claim, matching the Production Contract. This does not imply that all possible failures are covered.

## 9. RTO/RPO policy

RTO and RPO must be reported as two separate things:

- **measured recovery observations** from drills;
- **target objectives** approved from business/operating requirements.

The current target RTO/RPO remain `UNKNOWN`. An observed restore time or observed data-loss amount must not be retroactively declared the target merely because the drill achieved it.

## 10. Retry and overload policy to validate

Google SRE guidance warns that retries can amplify overload and recommends overload control/load shedding. Therefore the benchmark must explicitly observe:

- maximum logical retry budget;
- retry delay/jitter policy;
- concurrency caps against providers/database;
- admission rejection/defer behavior;
- queue bounds and oldest-work age;
- whether a liveness restart increases overload rather than repairing a dead process.

The selected implementation values remain evidence-driven and workload-specific.

## 11. Systematic source search

Search categories on 2026-09-22:

- SRE overload/cascading-failure/capacity guidance;
- latency/traffic/errors/saturation measurement;
- open-model arrival-rate load generation and threshold/result mechanics;
- startup/readiness/liveness implications during overload;
- autoscaling on resource vs backlog/event metrics;
- observability signal correlation;
- contingency/recovery and restore planning.

Stopping rule: primary sources cover load-shape semantics, overload/failure mechanisms, operational metrics and recovery evidence. More generic sources cannot supply Academy Suno's missing traffic mix, business RTO/RPO, provider quotas or target environment. The next information gain comes from executing this plan on candidate architectures.

## 12. Source table

| Source | Type | Supported use | Limitation |
|---|---|---|---|
| https://sre.google/sre-book/addressing-cascading-failures/ | Google SRE primary guidance | load-test until failure/beyond; overload, queues and cascading failure | not a project workload measurement |
| https://sre.google/sre-book/monitoring-distributed-systems/ | Google SRE primary guidance | latency, traffic, errors, saturation; tail distributions | not a target/SLO source |
| https://sre.google/workbook/handling-overload/ | Google SRE primary guidance | retry budgets/load shedding/overload controls | implementation remains open |
| https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/constant-arrival-rate/ | k6 official | open-model arrival-rate mechanics | k6 itself is only a harness candidate |
| https://grafana.com/docs/k6/latest/using-k6/thresholds/ | k6 official | machine-checkable benchmark thresholds | numeric examples are not Academy targets |
| https://grafana.com/docs/k6/latest/using-k6/metrics/reference/ | k6 official | latency/error/drop metric capabilities | product metrics still require instrumentation |
| https://opentelemetry.io/docs/specs/otel/logs/ | OpenTelemetry specification | trace/span/resource correlation model | telemetry implementation is owned by T007/T010 |
| https://kubernetes.io/docs/concepts/workloads/pods/probes/ | Kubernetes official | startup/readiness/liveness separation under failure | only applies directly if this runtime class is used |
| https://csrc.nist.gov/pubs/sp/800/34/r1/final | NIST final publication | contingency/recovery planning discipline | organization-specific RTO/RPO still external |

## 13. Decision

`COMBINED_METHOD` is the proposed W005 reliability/capacity validation standard:

- closed-model concurrency ladder **plus** open-model arrival staircase;
- burst, soak and controlled beyond-saturation stage;
- explicit hard-correctness gates at every stage;
- dependency/process failure injection;
- restart/resume drill;
- clean-environment backup/restore drill;
- raw curve + saturation interval + uncertainty, not a fabricated user-capacity claim.

No numeric performance target, SLO, RTO, RPO, autoscaling threshold or replica count is selected by this record.

## 14. Confidence and reversal conditions

Confidence is HIGH that a combined method is necessary for this mixed synchronous/asynchronous workload and contract; LOW for future numeric targets until observed.

Reopen if:

- T009 defines a statistically stronger protocol that preserves all hard gates and load-shape coverage;
- real production traffic becomes safely available and materially changes representativeness;
- T003 selects an execution model that cannot be represented by these job/run stages;
- partner/business requirements supply explicit load/SLO/RTO/RPO constraints that require additional scenarios;
- benchmark execution reveals a dominant bottleneck invisible to the current metrics.

## 15. Traceability

Affects: `PROD-002`, `PROD-003`, `PROD-013`, `PROD-016`; `RISK-0018`, `RISK-0021`, `RISK-0033`, `RISK-0038`.

Executable/proposed matrix: `docs/production/reliability/W005_T008_LOAD_FAILURE_RECOVERY_PLAN.md`.
