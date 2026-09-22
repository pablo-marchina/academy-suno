# DR-5008 — Deployment/runtime topology for production research

`STATUS: NO_OVERALL_PREFERENCE`
`TASK: W005-T008-A01`
`RESEARCH_DATE: 2026-09-22`
`CONFIDENCE: HIGH on invariants / MEDIUM on hosting-topology comparison / LOW on external target fit`

## 1. Decision question

Which deployment/runtime topology classes are viable for the Academy Suno production path, and which invariants should T010 carry forward before any cloud/runtime is selected?

This record does **not** choose a cloud, orchestrator, queue, database, workflow engine or hosting vendor. The external deployment target, real concurrency, SLO/SLA, budget and Suno operational ownership remain unknown.

## 2. Workload / constraints

Relevant contract and risk traceability:

- `PROD-002`: typed/versioned production API; idempotency; timeout/retry/backpressure handling.
- `PROD-003`: shared durable persistence; run state survives restart/redeploy; backup/restore demonstrated.
- `PROD-013`: load curve, saturation point, failure/retry, restart/resume and backup/restore evidence.
- `PROD-016`: reproducible deployment, health/startup/restart behavior, migrations, config/secrets separation.
- `RISK-0018`: isolated components may fail on clean checkout/integration.
- `RISK-0021`: mechanics proof must not be promoted to production readiness.
- `RISK-0033`: local SQLite/state is not a safe assumption for multi-replica/multi-user runtime.
- `RISK-0038`: capacity may not be claimed without load evidence.

Observed repository baseline is a Python application with orchestration modules and a local SQLite RunStore implementation under `src/suno_content/runstore/sqlite.py`. That is useful as a case baseline and counterfactual, not evidence for shared multi-replica production persistence.

## 3. Alternatives

### A — Single host / Compose-style services with local process supervision

Shape: one host, one or a few containers, optional local queue/database, restart policy and healthchecks.

Evidence: current Docker documentation supports restart policies, healthchecks and dependency startup ordering. This is useful for reproducible development, integration environments and possibly low-criticality single-host operation.

Strengths:

- lowest operational surface and easiest clean deployment;
- straightforward local reproduction;
- useful baseline for measuring the real cost of additional infrastructure.

Material limitations for this project:

- a single host remains a failure domain;
- local filesystem/SQLite state conflicts with the Production Contract's shared durable multi-replica requirement;
- process restart alone does not prove durable workflow resume, backup/restore or multi-user concurrency;
- horizontal capacity and disruption behavior are weak unless another scheduler/control plane is added.

Disposition: `BASELINE_ONLY` for production synthesis unless the product scope is explicitly reduced to a single-host service and the Production Contract is changed. It is not eligible to support a current `PRODUCTION_READY` claim with local state.

### B — Managed container service: stateless API + external durable state + asynchronous worker service

Shape: independently deployable API and worker containers; external database/object storage; optional durable queue; platform handles request-driven or metric-driven replica scaling.

Representative primary evidence: current Cloud Run documentation exposes request-concurrency and CPU-driven autoscaling, scale-to-zero/minimum instances, and maximum-instance caps. AWS ECS documentation shows target tracking and queue-backlog-per-task autoscaling for asynchronous workers. These are examples of the **class**, not vendor endorsements.

Strengths:

- lower control-plane burden than managing a cluster;
- independent API/worker scaling is possible;
- maximum replicas/concurrency can protect cost and downstream dependencies;
- well suited to stateless request serving when long work is externalized.

Trade-offs / risks:

- background work semantics, maximum request duration, scale-to-zero/cold start and telemetry details are platform specific;
- queue/provider semantics can introduce at-least-once delivery and therefore require idempotent workers;
- autoscaling on CPU alone can miss queue/backlog or single-thread hotspots;
- backing database/provider connection limits can become the true saturation point.

Disposition: `CANDIDATE` pending workload benchmark and T010 synthesis.

### C — Cluster scheduler/orchestrator: replicated API + worker pools + external durable state

Shape: Kubernetes-style Deployments or equivalent for API and workers, explicit health probes, rolling rollout policy, autoscaling, disruption policy and event-driven scaling adapter where needed.

Primary evidence: Kubernetes Deployments provide declarative replicas and controlled rolling updates; startup/readiness/liveness probes have distinct semantics; HPA supports horizontal scaling, while queue/event scaling can be supplied through external metrics systems such as KEDA. Kubernetes documents that PodDisruptionBudgets protect voluntary evictions only and do not guarantee availability under node failure.

Strengths:

- explicit control over replicas, rollout, health, disruption and scaling policy;
- clean separation of request-serving and background workers;
- event/backlog-driven worker scaling can be represented directly;
- portable container contract and strong testability of failure modes.

Trade-offs / risks:

- highest control-plane/operational burden of the candidates;
- misconfigured liveness can amplify overload by restarting healthy-but-saturated workloads;
- PDBs are not a substitute for redundancy or failure testing;
- cluster/node autoscaling latency and quotas become part of saturation behavior;
- requires stronger deployment/runbook ownership than currently known.

Disposition: `CANDIDATE` pending workload benchmark, cost/ops evidence and external target constraints.

### D — Durable workflow service + activity/worker pools layered on B or C

Shape: the API persists/starts a durable workflow; independently replicated workers poll task queues and execute activities; workflow state/resume is provided by a workflow service.

Representative evidence: Temporal documents durable execution that resumes after process/network/infrastructure failure; its workers and task queues can be scaled independently. This topology is an overlay, not a hosting platform by itself.

Strengths:

- directly addresses long-running workflow restart/resume semantics;
- isolates workflow durability from web request lifetime;
- task queues provide a natural backpressure boundary and worker separation.

Trade-offs / risks:

- extra stateful/control-plane dependency and operational/cost burden;
- workflow determinism/versioning/migration model becomes a material architecture constraint;
- overlaps W005-T003, which owns orchestration/durability bakeoff and must decide whether this class is justified.

Disposition: `PENDING_T003`; T008 does not select it.

## 4. Evaluation criteria

No synthetic single score is used. Hard gates are non-compensatory.

| Criterion | Required evidence |
|---|---|
| durable shared state | restart/redeploy + replica concurrency + backup/restore |
| request isolation | API replica loss must not lose accepted run state |
| worker durability | kill mid-run; resume/retry without duplicate accepted output |
| backpressure | bounded queue/in-flight work; explicit overload rejection/defer behavior |
| idempotency | duplicate submission/delivery produces one accepted logical result |
| cancellation | queued/running cancellation is observable and does not corrupt run state |
| replica scaling | measured scale-out/in behavior under workload; no invented user count |
| downstream protection | max concurrency/replicas/connection pools protect DB/provider limits |
| health semantics | startup/readiness/liveness are distinct; overloaded != dead |
| rollout/migration | old/new versions can coexist safely or deployment is explicitly serialized |
| observability | request/run/job/tenant correlation; queue age/depth, retries, saturation |
| recovery | binary restart/resume and backup/restore scenarios pass |
| cost/ops burden | idle cost + cost/completed run + operator steps/tooling |
| reversibility | migration path and lock-in documented before promotion |

## 5. Target deployment invariants for T010

These are architecture **constraints**, not a stack selection:

1. The production API tier is treated as replaceable/stateless with respect to accepted run state; durable state must live outside an individual API process/container.
2. Long-running AI/document workflow work must not depend on the lifetime of the initiating HTTP request. Whether this is a queue worker, durable workflow engine or another mechanism is pending T003/T010 evidence.
3. API and worker capacity must be independently controllable. Worker scaling should consider work backlog/oldest-work age or equivalent demand signals, not CPU alone, when asynchronous work exists.
4. Every work item needs stable run/job identity, idempotency semantics and attempt/retry provenance. At-least-once delivery must not create duplicate accepted branches/results.
5. Backpressure is explicit: bounded in-flight work, bounded retries, admission/rejection/defer behavior and downstream concurrency limits are observable.
6. Health has distinct meanings: startup gate, readiness/admission gate, and liveness/process-dead gate. Saturation alone must not automatically trigger restart storms.
7. Replica count and per-replica concurrency have upper bounds tied to measured downstream limits; unbounded autoscaling is prohibited.
8. Stateful dependencies are external/shared and have connection/quota protection. Local SQLite/filesystem remain development/baseline mechanisms unless a later DRG changes the Production Contract scope.
9. Schema/data migrations are controlled one-shot operations, not races executed independently by every replica. Rolling deployments must preserve compatibility across versions or be explicitly serialized.
10. Deploy configuration is declarative/reproducible; secrets/config are externalized; image/version provenance is recorded.
11. Backup/restore is not considered proven until a production-equivalent restore drill succeeds and measured recovery data is persisted.
12. The same runtime path used for final evidence must be the real product path; mechanics-only local success does not satisfy production reliability gates.

## 6. Systematic source search

Search categories on 2026-09-22:

- container restart/health and dependency startup;
- replicated deployment and rolling update behavior;
- startup/readiness/liveness semantics;
- voluntary-disruption guarantees and limitations;
- CPU/custom/event/backlog-driven autoscaling;
- managed-container concurrency and max-instance protection;
- asynchronous queue worker autoscaling;
- durable workflow/worker topology;
- overload, load shedding and retry amplification.

Stopping rule: primary sources now cover every evaluation criterion above at the topology level; additional vendor pages would mostly repeat known mechanisms and cannot resolve the missing project-specific workload, target-cloud, budget or operating-owner facts. The remaining differentiator is empirical benchmark evidence, not more generic documentation.

## 7. Source table

| Source | Type / freshness | Supported claim | Limitation |
|---|---|---|---|
| https://docs.docker.com/engine/containers/start-containers-automatically/ | Docker official, accessed 2026-09-22 | restart policies and their scope | single-host/container restart is not HA |
| https://docs.docker.com/compose/how-tos/startup-order/ | Docker official, current | health-gated dependency startup | Compose semantics do not prove multi-host resilience |
| https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ | Kubernetes official, current | replicas, rolling update, rollback, scale | no claim that Kubernetes is needed here |
| https://kubernetes.io/docs/concepts/workloads/pods/probes/ | Kubernetes official, current | startup/readiness/liveness separation; bad liveness can cascade | probe values remain workload-specific |
| https://kubernetes.io/docs/tasks/run-application/configure-pdb/ | Kubernetes official, current | PDB limits voluntary disruption only | not an availability guarantee |
| https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/ | Kubernetes official, current | horizontal scaling from resource/custom metrics | cluster/node capacity still matters |
| https://keda.sh/docs/2.20/concepts/scaling-deployments/ | KEDA official, current branch | event-source/backlog-driven replica scaling | Kubernetes-specific add-on |
| https://docs.cloud.google.com/run/docs/about-instance-autoscaling | Google Cloud official, current | CPU/concurrency autoscaling, scale-to-zero, max/min interactions | vendor-specific behavior |
| https://docs.cloud.google.com/run/docs/about-concurrency | Google Cloud official, current | per-instance concurrency affects cost/scaling and must match code | vendor-specific limits/defaults change |
| https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-queue.html | AWS official, current | backlog-per-task is more useful than raw queue depth | vendor-specific example |
| https://docs.temporal.io/ | Temporal official, accessed 2026-09-22 | durable execution / resume class | T003 owns whether to adopt |
| https://sre.google/sre-book/addressing-cascading-failures/ | Google SRE primary engineering guidance | test until failure, overload rejection, queue limits, capacity planning | not project-specific benchmark data |

## 8. Decision

`NO_OVERALL_PREFERENCE` between managed-container and cluster-scheduler hosting classes.

The evidence is sufficient to **reject local single-process/local-state mechanics as production evidence**, and to carry the topology invariants in section 5 into T010. It is **not** sufficient to select Kubernetes, Cloud Run, ECS, Temporal, KEDA, a queue, database, cloud or autoscaling target.

The required next discriminator is the workload-specific benchmark/recovery plan in `docs/production/reliability/W005_T008_LOAD_FAILURE_RECOVERY_PLAN.md`, plus T003/T004/T007/T009/T013 inputs.

## 9. Reversal conditions

Reopen the invariants or candidate set if any of the following becomes true:

- authoritative partner requirements impose a specific cloud/runtime, residency, network or operations model;
- T003 proves a workflow runtime whose execution model materially changes worker/queue topology;
- T004 selects persistence with constraints incompatible with the candidate topology;
- representative benchmarks show the API can safely own the full workflow lifetime with equal restart/resume correctness and materially lower operational burden;
- cost/ops evidence shows a candidate class violates budget or support capacity;
- new workload evidence shows queue/event scaling is unnecessary or harmful;
- recovery tests expose a failure mode requiring a different isolation boundary.

## 10. Traceability

Affects: `PROD-002`, `PROD-003`, `PROD-013`, `PROD-016`; `RISK-0018`, `RISK-0021`, `RISK-0033`, `RISK-0038`.

Benchmark artifact: `docs/production/reliability/W005_T008_LOAD_FAILURE_RECOVERY_PLAN.md`.
