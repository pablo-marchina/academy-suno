# W007-T001 — Representative production topology qualification protocol

`TASK_ID: W007-T001`  
`ATTEMPT_ID: A01`  
`CONSUMER: W007-T002-A01`  
`PROTOCOL_STATE: PREDECLARED / NOT_EXECUTED_IN_T001`  
`PRODUCTION_TOPOLOGY_LOCK: NONE`

## Purpose

This procedure converts the W006-T014 production-topology blockers into an executable T002 deployed bakeoff. T001 defines **what must be measured and how candidates remain eligible**; it does not manufacture production evidence.

Machine-readable authority: `artifacts/w007-t001/a01/qualification-protocol.json`.

Candidate authority: `artifacts/w007-t001/a01/topology-candidates.json`.

Decision method: W005-BENCHMARK-METHODOLOGY-V002 — hard gates -> raw multidimensional metrics -> uncertainty/missingness -> point Pareto.

## Candidate set

- `B0_REFERENCE_CONTROL` — current accepted W006 semantics, `DIAGNOSTIC_ONLY`, never production-eligible.
- `C1_GCP_CLOUD_RUN` — Cloud Run request service + continuous worker pool + Cloud SQL PostgreSQL HA/PITR + private Cloud Storage + Secret Manager + OTLP.
- `C2_AWS_ECS_FARGATE` — ECS Fargate API/worker services + ALB + RDS PostgreSQL Multi-AZ/PITR + private S3 + Secrets Manager + OTLP.
- `C3_GKE_AUTOPILOT` — GKE Autopilot API/worker Deployments + Cloud SQL PostgreSQL HA/PITR + private Cloud Storage + Secret Manager/WIF + OTLP.

Runtime framework selection is orthogonal. T002 must preserve the W006 common acceptance semantics and execute eligible runtime candidates on representative PostgreSQL-backed deployment where supported. No runtime framework is locked by T001.

## Fixed comparability controls

Before observing performance outcomes, T002 must freeze:

1. source SHA and immutable OCI image digest;
2. Python `3.13.15`, `uv@0.12.18`, `pyproject.toml` and `uv.lock`;
3. versioned exact 3x3 input corpus and branch IDs;
4. provider-effect proxy/configuration used for the topology-only workload;
5. target geography and service/database sizing policy;
6. load-ladder stopping/budget rule;
7. candidate execution order/rotation;
8. IaC revision and candidate-specific adapter delta;
9. OTLP semantic configuration and evidence schema.

Use the same application image everywhere. Candidate-specific infrastructure adapters/IaC are allowed; business/workflow semantics are not.

## Non-compensatory eligibility gates

A candidate execution is ineligible on any violation:

| Gate | Required |
|---|---:|
| critical hard-gate compensation | `0` |
| cross-tenant unauthorized success | `0` |
| required accepted provenance missing | `0` |
| exact accepted branch coverage | `9/9` |
| accepted join branch loss | `0` |
| accepted join branch duplication | `0` |
| critical schema violation promoted | `0` |
| silent stale same-run overwrite | `0` |
| duplicate accepted branch output | `0` |
| uncommitted event accepted as authoritative | `0` |
| private quarantine bypass | `0` |
| secret/credential canary leakage | `0` |
| defined restart/resume | `100% PASS` |
| defined backup/restore | `100% PASS` |

A faster or cheaper candidate never compensates for a failed gate.

## Execution phases

### P0 — build, deploy and evidence identity

Build once from the frozen toolchain. Persist source SHA, image digest, lock digest, IaC revision, database migration revision and exact candidate resource configuration.

Deploy from clean credentials/context. Record region, compute/task/pod resources, min/max/desired replica behavior, database class/HA/backups, object configuration, network/LB configuration, identities, secret refs and telemetry topology.

### P1 — shared state and multi-replica correctness

Run at least two concurrently eligible API/worker units or provider-equivalent multi-instance execution.

Prove no correctness dependence on local filesystem/process affinity. Execute duplicate delivery, concurrent ownership/CAS, stale writer, out-of-order result, timeout after external side effect but before authoritative acceptance, process crash before checkpoint, fresh-process reopen and fencing.

Persist physical side-effect attempts separately from authoritative accepted outputs.

### P2 — exact 3x3 + deployed security

Execute all nine stable identities: beginner/intermediate/advanced x article/carousel/short_video.

Run cross-tenant attempts across API/data/object/event/trace. Exercise session/revocation/org-switch/cursor behavior once the candidate's deployed adapters exist. Exercise upload size/type/content/path abuse, quarantine transition and immutable source hashes.

Verify separate least-privilege service identities and negative secret/object permissions.

### P3 — load, queue and backpressure

Use an adaptive ladder starting at concurrency `1`, then double (`1,2,4,8,...`) until the first **observed** saturation/guardrail/provider limit or the predeclared budget ceiling. This is a discovery protocol, not a supported-user target.

At every rung persist raw request/run observations and:

- latency p50/p95/p99 + queue wait;
- successful runs/branches per unit time;
- errors/retries/backpressure decisions;
- CPU/memory;
- DB connection/lock/wait evidence;
- replica/task/pod counts and scale events;
- candidate infrastructure cost/usage.

Repeat independent windows wherever variance matters; retain outliers. A budget-limited or incomplete rung is censored/missing, never silently replaced by a lower level.

### P4 — failure/failover/redeploy

During in-flight runs:

- kill/restart API and worker units;
- interrupt DB connectivity;
- trigger provider-supported managed-DB HA failover where safely available;
- inject delayed duplicates/stale owners after recovery;
- deny object access temporarily;
- interrupt telemetry export separately;
- rotate/revoke a secret version;
- execute rolling/revision deployment.

Measure interruption and recovery. Do **not** label observed values SLO/RTO.

### P5 — backup and point-in-time restore

Create a known recovery point, mutate state afterward, then restore into an isolated target. Execute PITR where supported.

Connect a fresh app deployment to the restored target and verify tenant/run/job/branch identities, source hashes, authoritative events and replay.

Record restore duration, latest restorable point, missing/mismatched records and operator steps. The defined restore scenario must be `100% PASS` before any production claim.

### P6 — schema migration and rollback

Use an expand/contract fixture:

1. deploy schema/application `N`;
2. apply additive `N+1`;
3. run mixed-version reads/writes;
4. backfill/reconcile;
5. roll application back while schema remains backward compatible;
6. verify exact branch/state/provenance identity.

Measure migration duration, blocking/lock time, errors, incompatible reads/writes and rollback duration.

A destructive down-migration is never declared reversible without an executed restore/PITR route.

### P7 — observability

Export W3C/OTel-compatible traces, metrics and structured logs through OTLP with request/run/job/tenant correlation.

Persist:

- export/ingest success/failure;
- dropped telemetry;
- queryability;
- ingest/query latency if observable;
- cardinality;
- backend billable usage/cost;
- redaction/canary results.

Telemetry stays non-authoritative. Collector/backend outage must not corrupt product state/events.

### P8 — deployment and operational burden

From a clean environment execute fresh deploy, health/startup checks, normal rollout and rollback. Record every automated/manual step, wall-clock operation duration, intervention, prerequisite and recovery from failed steps.

Link deployment identity to source/build/image/IaC/migration identity.

Documentation-only capability is not measured operations evidence.

### P9 — cost and decision

Capture a dated pricing snapshot and actual metered usage where available for:

- compute;
- database;
- load balancer/network;
- object storage;
- backup/restore storage/operations;
- telemetry;
- secrets.

Report cost per qualification window and per successful exact-3x3 run when computable. Otherwise emit `NOT_OBSERVED` with reason; never infer a zero.

Apply:

1. hard-gate eligibility;
2. raw multidimensional evidence;
3. uncertainty/missingness;
4. point Pareto.

No scalar utility.

## Required evidence bundle from T002

At minimum:

- deployment manifest/identity for every candidate;
- candidate resource/IaC snapshot;
- raw exact-3x3 observations;
- raw load-ladder observations;
- raw failure/failover/restart observations;
- backup/PITR restore evidence;
- migration/rollback evidence;
- security negative-test evidence;
- observability ingest/query/redaction evidence;
- metered usage/cost evidence;
- candidate hard-gate table;
- uncertainty/missingness report;
- point-Pareto decision artifact;
- final T002 RESULT with `LOCK`, `NO_PREFERENCE` or `PENDING_EVIDENCE`.

## Decision rule

`LOCK` is allowed only if every required hard gate passes, required objective families are observed, no material candidate is excluded without an evidence-backed reason, and the decision remains supported under repetition/uncertainty.

If multiple eligible candidates remain nondominated, return `NO_PREFERENCE`.

If a required objective is missing or a representative comparison cannot be completed, return `PENDING_EVIDENCE`.

A singleton Pareto point is not automatically a lock if a material objective/candidate is missing or the evidence is not representative.

## Evidence saturation / early termination

Research is saturated only when a further systematic source pass introduces no materially different candidate, failure mode, constraint or evidence capable of changing protocol/eligibility.

Execution is different: T002 must complete each eligible predeclared candidate. A candidate that fails a hard gate may stop later unsafe/costly phases after preserving the failure evidence; an early performance lead is never a stopping reason.

## Reopen conditions

Reopen a later topology lock on material workload/geography/compliance change, provider/runtime version or price/limit change, hard-gate incident, newly observable missing objective, newly feasible material alternative, or representative business utility evidence frozen before outcomes.

## Production boundary

This protocol closes planning ambiguity only. Until T002 executes representative deployed evidence:

`PRODUCTION_RUNTIME_LOCK: NONE`  
`PRODUCTION_DATABASE_LOCK: NONE`  
`PRODUCTION_DEPLOYMENT_LOCK: NONE`  
`PRODUCTION_READY_CLAIM: FALSE / NOT_AUTHORIZED`
