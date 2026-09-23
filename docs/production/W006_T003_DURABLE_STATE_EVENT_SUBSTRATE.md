# W006-T003 — Durable state↔event reference substrate and failure harness

`TASK_ID: W006-T003`  
`ATTEMPT_ID: A01`  
`CONTRACT_PACKAGE: docs/production/contracts/v1`  
`EVIDENCE_STATUS: REFERENCE_CANDIDATE_PASS`  
`TECHNOLOGY_STATUS: PENDING_EVIDENCE / NO_PRODUCTION_WINNER`

## Purpose

This artifact implements and tests the state↔durable-product-event invariants required by the accepted W005 final fan-in and the W006-T001-A02 contracts. It is deliberately a **reference candidate**, not a database/backend selection.

The candidate uses Python stdlib `sqlite3` to make the invariants executable with no new runtime dependency. The accepted W005 authority explicitly bars the existing SQLite run store from multi-replica production authority as-is, and this task does not reverse that decision. A production substrate still requires DRG-compliant representative comparison plus downstream runtime/security/capacity/recovery evidence.

## Contract mapping

The implementation consumes the T001 v1 semantics directly:

- `StateTransition`: stable `transition_id`, `mutation_id`, tenant/resource identity, `previous_revision`, `result_revision`, and ownership epoch;
- `CasWriteIntent`: stale `expected_revision` or `expected_ownership_epoch` fails closed;
- `EventEnvelope`: stable `event_id`, transition identity, resource identity, result revision, monotonic run-scoped `event_revision`, event type/schema and timestamp;
- replay position is not authority: replay always requires server-supplied `org_id + workspace_id + run_id` scope;
- physical delivery may be at least once while logical projection is idempotent.

## Reference architecture

`SQLiteDurableStateEventStore` persists four logical surfaces:

1. `resources` — latest authoritative tenant-scoped resource state and CAS revision;
2. `transitions` — append-only authoritative transition/audit history;
3. `outbox` — delivery work keyed one-to-one to committed transitions;
4. `projection_receipts` — consumer-side logical deduplication by stable transition identity.

A state mutation, transition row, run event revision allocation and outbox row are written under one `BEGIN IMMEDIATE` transaction. Pre-commit injected failures roll the full unit back. A post-commit crash leaves the authoritative transition and pending outbox durable, and retry with the same `mutation_id` returns the existing committed transition instead of creating another one.

Logical replay is rebuilt from immutable authoritative transitions rather than delivery acknowledgement state. Therefore publisher failure cannot erase logical event truth. `reconcile_outbox()` deterministically reconstructs any missing outbox delivery row from authoritative transition history.

Projection accepts an event only when its tenant/run/transition/event/revision tuple matches an authoritative committed transition. Duplicate physical delivery is ignored after the first accepted projection.

## Audit and recovery

Transition rows are protected by append-only update/delete triggers. `audit_invariants()` detects:

- authoritative state whose current revision has no matching transition;
- transition whose resulting revision is absent from authoritative state;
- transition missing its outbox row.

Backup uses SQLite online backup plus `PRAGMA integrity_check`. Restore copies the backup into a fresh store and re-runs integrity validation before use.

No numeric RTO/RPO is claimed; those targets remain evidence/external-owner gated.

## Common failure harness

Executable harness: `tests/runstore/failure_harness_w006_t003.py`  
Raw observed evidence: `artifacts/w006-t003/failure-harness.json`

Observed local run covered 14 scenarios, including every W005 §4 required case plus transactional partial-write and backup/restore checks:

- four pre-commit fault points rollback atomically;
- state commit + publisher crash before delivery;
- retry after worker/publisher crash;
- duplicate physical delivery;
- out-of-order physical delivery;
- consumer crash after side effect before checkpoint;
- consumer restart from an earlier cursor;
- stale cursor replay;
- reconciliation after intentional outbox gap;
- attempted projection without authoritative committed transition;
- concurrent same-run stale revision;
- telemetry backend outage while product state/event path continues;
- cross-tenant cursor isolation;
- backup/restore.

Observed hard-gate metrics:

| Metric | Observed |
|---|---:|
| scenarios passed | `14/14` |
| silent stale overwrite accepted | `0` |
| permanent logical event gap after reconciliation | `0` |
| event without authoritative committed transition | `0` |
| duplicate logical projection | `0` |
| cross-tenant replay success | `0` |
| restart/replay/repair pass rate | `100%` |
| backup/restore pass rate | `100%` |

Unit-level regression coverage is in `tests/runstore/test_durable_state_events.py`. The repository foundation regression now includes `tests/runstore` and executes the common failure harness, failing closed if any non-compensatory metric drifts.

## Evidence boundary / non-claims

This attempt proves the contract semantics and a reproducible failure harness for the reference candidate. It does **not** prove or claim:

- SQLite is the production database or event substrate;
- multi-replica/distributed consensus behavior;
- representative latency, throughput, saturation, failover time, RTO or RPO;
- managed-service durability/SLA properties;
- cross-region or disaster-recovery topology;
- production readiness of the overall product.

The correct downstream use is to run the same logical harness against production substrate candidates and promote a default only through the project Decision Research Gate and evidence fan-in (`W006-T007`).
