# DR-7001 — Representative production topology candidates and qualification gate

- **Task:** W007-T001 / A01
- **Research date:** 2026-09-24
- **Decision state:** `PENDING_DEPLOYED_EVIDENCE`
- **Production topology lock:** `NONE`
- **Confidence:** HIGH that the candidate set and protocol cover the current W006-T014 topology blockers; LOW for any production winner because T001 intentionally does not execute deployed comparative evidence.

## Decision question

Which materially different production topology classes are feasible enough to advance to W007-T002 representative deployment, and what exact evidence must T002 collect before any production runtime/database/deployment topology can be locked?

This record is a research/qualification decision, not a substrate winner selection. The accepted W006-T014 audit leaves production runtime/shared persistence/event deployment, identity/object/secrets controls, observability topology, recovery, migration/rollback, capacity and operational cost unqualified. W005-BENCHMARK-METHODOLOGY-V002 therefore remains binding: non-compensatory hard gates -> raw multidimensional evidence -> uncertainty/missingness -> point Pareto. No scalar score or preference is introduced.

## Workload / constraints

The topology must support the same real Academy Suno product path and accepted semantic floor:

- multi-user/multi-tenant request, run, job and artifact identity;
- exact `3 audiences x 3 formats = 9` accepted branch identities with lossless join;
- durable shared state/events across process/redeploy/restart;
- idempotent accepted outputs while exposing physical external side-effect attempts;
- fail-closed stale ownership/fencing, provenance, schema and tenant gates;
- controlled object upload/quarantine/accepted flow;
- portable correlated traces, metrics and structured logs;
- reproducible build/deploy from Python `3.13.15` + `uv@0.12.18`;
- deploy, migration, rollback, backup/restore and failure qualification;
- no production SLO/RTO/RPO/capacity target invented before deployed measurements.

The current W006 reference path remains a semantic control only. Its local/runner evidence cannot be promoted to production topology evidence.

## Alternatives

### B0 — accepted W006 reference control (`DIAGNOSTIC_ONLY`)

The existing reference/local execution path is retained as a counterfactual semantic floor. It is not production-eligible because it has no representative multi-replica production database/event substrate, deployment identity, production IAM/object/secrets adapters or deployed observability topology.

### C1 — Google Cloud Run + Cloud SQL PostgreSQL

Deployment class: **serverless managed containers**.

- request API/SSE: Cloud Run service;
- continuous background workers: Cloud Run worker pool;
- shared database: Cloud SQL for PostgreSQL, regional HA, PITR enabled;
- object storage: private Cloud Storage quarantine/accepted buckets or namespaces;
- secrets: Secret Manager, direct API and explicit version usage;
- workload identity: distinct service identities with least-privilege IAM;
- telemetry: OTLP-compatible OpenTelemetry Collector as sidecar or dedicated service;
- deployment: immutable image digest, declarative IaC, immutable Cloud Run revisions.

Material distinction: request-driven serverless serving/revision model plus a managed continuous worker-pool resource. Current Cloud Run documentation states worker pools are for continuous background work and **do not autoscale**; therefore T002 must measure and document worker sizing/scaling rather than assume service autoscaling behavior transfers to workers.

### C2 — Amazon ECS Fargate + RDS PostgreSQL

Deployment class: **managed long-lived container tasks**.

- request API/SSE: ECS Fargate service behind Application Load Balancer;
- background workers: separate ECS Fargate worker service;
- shared database: RDS for PostgreSQL Multi-AZ with automated backup/PITR;
- object storage: private S3 quarantine/accepted buckets or prefixes;
- secrets: AWS Secrets Manager;
- workload identity: separate task role and task-execution role, least privilege;
- telemetry: OTLP-compatible OpenTelemetry Collector sidecar/service;
- deployment: immutable image digest, declarative IaC, rolling service deployment with circuit-breaker rollback or a predeclared blue/green path.

Material distinction: explicit desired-count long-lived task scheduling, load balancer and service deployment controller rather than a request-serverless or Kubernetes controller model.

### C3 — GKE Autopilot + Cloud SQL PostgreSQL

Deployment class: **managed Kubernetes**.

- request API/SSE: GKE Autopilot Deployment/Service;
- background workers: separate Autopilot Deployment;
- shared database: Cloud SQL for PostgreSQL, regional HA, PITR enabled;
- object storage: private Cloud Storage quarantine/accepted buckets or namespaces;
- secrets: Secret Manager;
- workload identity: Kubernetes ServiceAccounts through Workload Identity Federation;
- telemetry: OTLP-compatible OpenTelemetry Collector sidecar or Deployment;
- deployment: immutable image digest, Kubernetes manifests/IaC, rolling Deployment, startup/readiness/liveness probes, PodDisruptionBudget and HPA.

Material distinction: Kubernetes pod/controller/HPA/PDB/workload-identity control surface. Autopilot removes node administration but preserves a materially different scheduling, rollout and operational model. Operational burden is an empirical T002 metric, not an assumed disadvantage.

## Why this three-candidate set is materially informative

C1 vs C3 deliberately holds much of the cloud data-plane family constant while changing the deployment/controller class; this helps isolate serverless-revision versus Kubernetes operational behavior. C2 adds a cross-cloud managed-task counterfactual with a different service/deployment/IAM model. Together they cover three materially different deployment classes without manufacturing a fourth candidate merely for vendor count.

The runtime framework is a separate decision axis. W006 already executed custom/CAS, LangGraph and DBOS against a common local acceptance floor and correctly retained `PENDING_EVIDENCE`. T001 therefore does not lock a runtime. T002 must bind eligible runtime candidates to representative PostgreSQL-backed deployed topology where supported. Temporal remains an `OPEN_CHALLENGER_CONDITIONAL`: execute it only if a remaining durability/operations hypothesis can plausibly change hard-gate eligibility or Pareto membership after the minimum runtime set is tested.

## Predeclared evaluation criteria

### Non-compensatory hard gates

Every production-eligible candidate must preserve:

- critical hard-gate compensation = `0`;
- cross-tenant unauthorized success = `0`;
- accepted required provenance missing = `0`;
- exact branch coverage = `9/9`;
- accepted join loss/duplication = `0`;
- critical schema violations promoted = `0`;
- silent stale same-run overwrite = `0`;
- duplicate accepted branch output = `0`;
- uncommitted event accepted as authoritative = `0`;
- private quarantine bypass = `0`;
- secret/credential canary leakage = `0`;
- defined restart/resume = `100% PASS`;
- defined backup/restore = `100% PASS`.

Any hard-gate failure makes that execution ineligible regardless of latency, cost or throughput.

### Raw objectives after eligibility

T002 must capture, with units and sample counts:

- request/run latency raw samples + p50/p95/p99 and queue wait;
- successful run/branch throughput;
- error/retry/duplicate-physical-side-effect rates;
- CPU, memory, DB connections/waits and replica/task/pod state;
- observed recovery/failover interruption;
- deploy, migration, rollback and restore durations plus manual interventions/procedure steps;
- telemetry ingest/query/drop/cardinality evidence;
- measured billable usage/cost by compute, database, network/LB, object, backup, telemetry and secrets when observable;
- all missingness/confounders.

No one-dimensional score is permitted.

## Representative qualification protocol

The executable contract is `artifacts/w007-t001/a01/qualification-protocol.json`; the human-readable procedure is `docs/production/W007_T001_TOPOLOGY_QUALIFICATION_PROTOCOL.md`.

Key experiment controls:

1. build one immutable application image from the frozen toolchain and deploy the same digest everywhere;
2. run the same exact 3x3 identities/corpus and same authoritative acceptance semantics;
3. predeclare target geography and service sizing before outcomes; record unavoidable provider/region mismatch as a confounder;
4. require multi-instance/process execution and shared durability;
5. use an adaptive load ladder starting at concurrency 1 and doubling until observed saturation/guardrail/provider limit or a predeclared budget ceiling, so no capacity target is invented;
6. retain all raw observations/outliers and repeat windows where variance matters;
7. execute failure/failover, backup/PITR restore, expand/contract migration, application rollback, telemetry outage and secret rotation;
8. capture actual provider billing/usage where possible and mark unavailable values `NOT_OBSERVED`;
9. apply hard gates -> raw metrics -> uncertainty/missingness -> point Pareto.

Provider/model quality selection is outside T002. The topology benchmark must use the same provider-effect proxy/configuration so external model changes do not confound substrate measurements; fresh current-provider selection remains W007-T006.

## Security/reliability/cost/lock-in treatment

Security controls are tested as hard eligibility properties, not traded for performance. Reliability includes actual deployed failure, restart, database HA failover and restore behavior. Cost is captured from current pricing snapshots plus measured usage; promotional credits are excluded from comparative unit cost. Lock-in is described structurally (service/revision, ECS task/service, Kubernetes API/controller, managed database/object/IAM surfaces) and remains a qualitative/raw operational dimension unless a representative migration cost can be measured.

No SLO, RTO, RPO or supported-user count is set here. T002 records observed recovery and saturation; later promotion may set targets only from evidence.

## Systematic source search

Research date: **2026-09-24**.

Search categories were predeclared around each component/failure surface:

- Cloud Run worker pools/autoscaling + Cloud SQL HA/PITR + Cloud Storage consistency + Secret Manager;
- ECS Fargate autoscaling/deployment rollback + RDS Multi-AZ/PITR + ECS IAM + S3/Secrets Manager;
- GKE Autopilot/HPA/Workload Identity + Cloud SQL;
- OpenTelemetry OTLP portability;
- DBOS production PostgreSQL/HA and LangGraph PostgreSQL checkpoint availability.

Primary provider documentation and protocol specifications were preferred. Accepted Academy execution evidence is used for Academy-specific semantics; vendor benchmark claims are not treated as Academy performance evidence.

Full machine-readable source register: `artifacts/w007-t001/a01/source-register.json`.

## Primary source table

| Source | Authority | Claim supported | Limitation |
|---|---|---|---|
| Cloud Run worker pools — https://docs.cloud.google.com/run/docs/deploy-worker-pools | Google Cloud | continuous background resource/revisions; worker pools do not autoscale | no Academy workload measurement |
| Cloud Run autoscaling — https://docs.cloud.google.com/run/docs/about-instance-autoscaling | Google Cloud | request-service autoscaling surface | not a capacity target |
| Cloud SQL HA — https://docs.cloud.google.com/sql/docs/postgres/high-availability | Google Cloud | managed PostgreSQL HA/failover capability | failover must be executed |
| Cloud SQL PITR — https://docs.cloud.google.com/sql/docs/postgres/backup-recovery/pitr | Google Cloud | PITR creates a recovery target | no Academy RTO/RPO |
| Cloud Storage consistency — https://docs.cloud.google.com/storage/docs/consistency | Google Cloud | current object consistency semantics | tenant/IAM behavior still tested |
| ECS deployment rollback — https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeploymentCircuitBreaker.html | AWS | rolling deployment circuit breaker/rollback | execute chosen path |
| ECS IAM roles — https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-iam-roles.html | AWS | task/execution-role separation | policy correctness remains empirical |
| RDS Multi-AZ — https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html | AWS | synchronous standby/failover topology | no Academy recovery time |
| RDS PITR — https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html | AWS | restore to new DB instance at point in time | no Academy RPO |
| GKE Autopilot — https://docs.cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview | Google Cloud | managed Kubernetes deployment class | no operational-burden score |
| GKE HPA — https://docs.cloud.google.com/kubernetes-engine/docs/concepts/horizontalpodautoscaler | Google Cloud | pod scaling from resource/custom/external metrics | thresholds must be measured |
| GKE Workload Identity — https://docs.cloud.google.com/kubernetes-engine/docs/how-to/workload-identity | Google Cloud | WIF always enabled in Autopilot | least-privilege bindings still tested |
| OTLP 1.11.0 — https://opentelemetry.io/docs/specs/otlp/ | OpenTelemetry | stable traces/metrics/logs OTLP transport | no backend selection |
| DBOS production checklist — https://docs.dbos.dev/production/checklist | DBOS | production PostgreSQL/HA and migration considerations | vendor claims are not Academy benchmark results |
| LangGraph PostgreSQL checkpoint package — https://pypi.org/project/langgraph-checkpoint-postgres/ | PyPI package authority | PostgreSQL checkpoint adapter availability | must be pinned/researched/executed before promotion |

## Research stopping rule / saturation

Source research stops when each criterion has current high-authority evidence and one additional systematic pass introduces no materially different deployment class, hard-gate failure mode, constraint or evidence capable of changing T002 eligibility/protocol. That condition is met for T001 planning.

This is **not** decision saturation for a production lock. T002 deployed evidence is mandatory.

## Decision

`PENDING_DEPLOYED_EVIDENCE`.

Advance `C1_GCP_CLOUD_RUN`, `C2_AWS_ECS_FARGATE` and `C3_GKE_AUTOPILOT` as representative candidates for T002. Retain `B0_REFERENCE_CONTROL` as diagnostic/counterfactual only.

`PRODUCTION_TOPOLOGY_LOCK: NONE`.

A lock is permitted only after T002 executes every predeclared eligible candidate (unless a hard gate safely terminates later phases), captures required objectives without material missingness, and the resulting decision remains supported under uncertainty. If multiple eligible candidates remain nondominated, emit `NO_PREFERENCE`; if required objectives are missing, emit `PENDING_EVIDENCE`.

## Reversal / reopen conditions

Reopen candidate research or any later lock when:

- production workload, geography, residency/compliance constraints materially change;
- provider/runtime versions, pricing or limits materially change;
- a new hard-gate failure/security/reliability incident appears;
- a previously missing required objective becomes measurable;
- a materially different feasible candidate could alter Pareto membership;
- representative business utility evidence becomes available and is frozen before outcomes.

## Traceability

Primary production rows addressed by the protocol: `PROD-001`, `PROD-002`, `PROD-003`, `PROD-004`, `PROD-006`, `PROD-012`, `PROD-013`, `PROD-014`, `PROD-016`, `PROD-017`.

This task changes no canonical STATE, ledger, wave manifest or production readiness claim.
