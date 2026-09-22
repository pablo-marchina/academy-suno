# DR-5402 — Tenant data isolation and durable persistence

`TASK_ID: W005-T004`
`ATTEMPT_ID: A01`
`RESEARCH_DATE: 2026-09-22`
`STATUS: CANDIDATE / PENDING_IMPLEMENTATION_BAKEOFF`
`CONFIDENCE: HIGH for invariants; MEDIUM for pooled+RLS candidate`

## 1. Decision question

Which data-partitioning and database isolation model should Academy Suno carry into the W005 production synthesis while preserving zero cross-tenant access, multi-replica durability and a reversible path to stronger isolation?

## 2. Workload / constraints

Relevant production requirements demand shared durable persistence, explicit tenant binding, zero unauthorized cross-tenant access in defined tests, backup/restore and multi-user/multi-replica operation. Tenant count, workload size, geographic residency and per-tenant regulatory isolation are currently unknown. W004 local-state behavior is a historical baseline, not a production storage target.

## 3. Alternatives

### A. Pooled shared database/shared schema
All tenants share tables; every private row carries a tenant/organization partition key. Application authorization plus database row-level controls enforce isolation.

Pros: operational simplicity, efficient resource use, consistent migrations, strongest fit to unknown early tenant scale.

Risks: one missed predicate/policy can expose another tenant; RLS configuration/role mistakes can bypass intended policy; shared blast radius.

### B. Schema-per-tenant
One database with per-tenant schemas.

Pros: clearer logical separation, some tenant-specific migration flexibility.

Risks: schema proliferation, migration/connection complexity and higher operational burden; tenant-aware routing remains necessary.

### C. Database-per-tenant / silo
Dedicated database (or equivalent isolated data plane) per tenant.

Pros: strongest operational/data-plane separation and easier tenant-specific residency/restore boundaries.

Risks: provisioning, migrations, observability, connection pools, backup and cost scale with tenant count.

### D. Bridge/hybrid
Pool by default; selected tenants/resources move to a silo or stronger isolation tier behind the same application-owned tenant boundary.

Pros: preserves pooled efficiency while allowing later compliance/residency/isolation escalation.

Risks: routing/provisioning complexity and need to keep semantics consistent across tiers.

## 4. Evaluation criteria

1. zero cross-tenant unauthorized access under adversarial tests;
2. durable shared persistence across replicas/restarts;
3. migration and backup/restore operability;
4. tenant-specific restore/deletion/residency path;
5. least-privileged runtime credentials;
6. failure blast radius;
7. connection-pool safety;
8. observability/auditability;
9. operational burden and cost under unknown scale;
10. reversibility if a tenant requires stronger isolation.

Hard security gates are not compensable by cost or convenience.

## 5. Systematic source search

Search categories on 2026-09-22:

- primary PostgreSQL RLS documentation and current security advisories;
- cloud-architecture guidance on pooled/silo/bridge multi-tenancy;
- integrated RLS implementation/testing guidance;
- authorization guidance for tenant context.

Stopping rule: research reached saturation once pooled, schema-separated, silo and hybrid patterns were covered; current RLS semantics/security limitations were verified; and no source removed the need for an application authorization layer. Performance/cost winner remains unproven because no production workload sizing exists.

## 6. Source table

| Source | Type / freshness | Supported claim | Limitation |
|---|---|---|---|
| PostgreSQL 18 Row Security Policies — https://www.postgresql.org/docs/current/ddl-rowsecurity.html | Primary DB docs, current | RLS policy semantics; referential-integrity checks can bypass RLS and policy design can create races/covert channels | Does not design Academy Suno tenant context |
| PostgreSQL CVE-2026-14666 — https://www.postgresql.org/support/security/CVE-2026-14666/ | Primary security advisory, 2026-08-13 | RLS cached plans could disregard role changes before fixed releases; fixed in 18.6/17.11/16.15/15.19/14.24 | Specific vulnerability, not a general rejection of RLS |
| AWS SaaS partitioning models — https://docs.aws.amazon.com/whitepapers/latest/multi-tenant-saas-storage-strategies/saas-partitioning-models.html | Cloud architecture guidance, current | Silo/bridge/pool are distinct valid isolation models with different trade-offs | AWS-oriented examples |
| AWS bridge model — https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/the-bridge-model.html | Cloud architecture guidance, current | Hybrid isolation can apply pool/silo at different layers | Does not prescribe Postgres implementation |
| Azure multitenant storage approaches — https://learn.microsoft.com/azure/architecture/guide/multitenant/approaches/storage-data | Cloud architecture guidance, current | Shared and dedicated data approaches; RLS is possible but adds identity propagation/policy complexity | Azure framing |
| Supabase RLS guide — https://supabase.com/docs/guides/database/postgres/row-level-security | Vendor primary docs, current | Practical RLS enablement and operation-specific policy testing | Integrated-platform-specific examples |
| OWASP Authorization Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | Security guidance, current | Authorization must be checked consistently on protected requests | Application-level, not database isolation alone |

## 7. Primary evidence first

PostgreSQL documentation/security advisories define the exact RLS safety properties and current version floor. Cloud architecture guidance is used to compare tenant partitioning patterns, not to pick a cloud provider.

## 8. Security / reliability / cost / lock-in

### Candidate architecture

Carry forward a **pooled relational data plane with explicit tenant keys and RLS as defense-in-depth**, plus an architectural escape hatch to a bridge/silo tier when a tenant requires stronger isolation. This is a `CANDIDATE`, not a production lock.

Private entities should carry `organization_id` and, where relevant, `workspace_id`. Prefer composite uniqueness/foreign-key patterns that make cross-tenant references structurally invalid, e.g. `(organization_id, id)` and `(organization_id, workspace_id)` where the schema permits it.

### RLS invariants if PostgreSQL is selected

- Every private table: `ENABLE ROW LEVEL SECURITY`; use `FORCE ROW LEVEL SECURITY` where owner behavior would otherwise weaken policy.
- Runtime service role is **not** superuser, table owner or `BYPASSRLS`.
- Migration/DDL role is separate from runtime role and is not available to ordinary API/worker code.
- Missing/invalid tenant context fails closed.
- Operation-specific `USING` / `WITH CHECK` policies cover SELECT/INSERT/UPDATE/DELETE as applicable.
- Application authorization still runs before data access; RLS is a second boundary, not a substitute.
- Parameterized queries and least privilege remain mandatory; arbitrary SQL execution would undermine assumptions about tenant context.
- Connection-pool checkout/return and exception paths must not leak prior tenant context.
- RLS policy dependencies should avoid unnecessarily complex cross-table lookups; PostgreSQL documents race/covert-channel concerns for some policy patterns.
- Referential-integrity behavior must be included in threat tests because PostgreSQL integrity checks are not ordinary RLS-filtered reads.
- Production version gate: reject PostgreSQL releases vulnerable to CVE-2026-14666. Minimum fixed patch levels from the advisory are 18.6 / 17.11 / 16.15 / 15.19 / 14.24 for those major versions.

### Candidate service principals

- `db_migrator`: DDL/migrations only; no normal request path.
- `api_runtime`: required CRUD only; no DDL, ownership, superuser or BYPASSRLS.
- `worker_runtime`: only tables/operations needed for queued jobs and artifact status.
- `backup_operator`: explicit backup/restore permissions; audited and not exposed to app requests.
- `break_glass_admin`: exceptional, strongly audited, not used by automation.

### Reliability

Pooled relational storage is operationally attractive while scale and tenant-specific requirements are unknown, but backup/restore must prove that all tenant rows are included. PostgreSQL documents `row_security=off` as a useful backup-safety behavior because it errors rather than silently omitting rows that would be filtered.

### Cost / lock-in

No provider or database service is chosen. Pooling tends to share infrastructure efficiently; silo models increase per-tenant operational/resource overhead. Without tenant count and workload curves, cost comparison is directional only.

## 9. Reproducible benchmark / experiment

A Phase 9 implementation spike must run the same fixture across the candidate storage model:

### Fixture

- org A: users A-owner/A-editor/A-viewer; workspaces A1/A2;
- org B: B-owner; workspace B1;
- outsider user;
- documents/runs/artifacts in each workspace.

### Security cases

- direct SELECT/INSERT/UPDATE/DELETE attempts across orgs;
- tenant key mutation on UPDATE;
- cross-tenant foreign-key/reference creation;
- absent/null/forged tenant context;
- runtime role inspection proving no superuser/owner/BYPASSRLS;
- transaction/connection reuse A → B after normal completion and exception/retry;
- role revocation on long-lived connections;
- backup/restore completeness;
- connection-pool and cache key isolation.

### Performance/operations cases

Measure with identical data volume and concurrency:

- p50/p95/p99 query latency for tenant-scoped reads/writes;
- throughput and saturation curve;
- connection count/pool utilization;
- migration time;
- backup and restore duration;
- tenant-specific export/delete/restore operator steps;
- policy/migration complexity proxy (changed lines / policy count / test count), without turning it into a compensatory security score.

No representative database benchmark was executed in this research-only attempt. Performance preference therefore remains pending.

## 10. Raw results + uncertainty

Evidence supports RLS as a useful row-level boundary but not an infallible one: role configuration, policy design, referential-integrity behavior, connection state and database patch level all matter. The August 2026 PostgreSQL advisory makes patch-level verification a concrete security acceptance gate.

Unknown: expected tenant count, highest tenant data size, residency requirements, per-tenant restore obligations, workload concurrency and acceptable isolation premium.

## 11. Decision

`CANDIDATE`: pooled shared relational storage with explicit tenant keys + application authorization + database RLS/row policy defense-in-depth, designed so selected tenants can move to a silo tier without changing resource identity.

`NO_DATABASE_PROVIDER_PREFERENCE` and `PENDING_IMPLEMENTATION_BAKEOFF`.

Schema-per-tenant is not promoted because it adds migration/provisioning complexity without evidence that it meets a requirement better than the candidate. Database-per-tenant remains a valid escalation path for regulatory/residency/blast-radius needs.

## 12. Confidence

- Explicit tenant keys + two-layer authorization/isolation: **HIGH**.
- Pooled+RLS as initial default candidate: **MEDIUM** — appropriate under current unknown scale, but must pass the adversarial/operational benchmark.
- Specific database/provider: **LOW / no preference**.

## 13. Reversal conditions

Promote or replace the candidate if:

- a tenant contract/regulation requires physical/dedicated data isolation;
- measured RLS/pool complexity or performance fails the acceptance suite;
- tenant-specific restore/residency cannot be met safely in the pool;
- operational evidence shows a silo/bridge architecture materially reduces critical risk at acceptable cost;
- a non-Postgres technology proves equivalent isolation, durability and operability with lower risk in the representative workload.

## 14. Traceability

- PROD-001: tenant-bound rows and zero cross-tenant access target.
- PROD-003: shared durable persistence, restart/redeploy survival, backup/restore.
- PROD-014: authz/RLS adversarial testing, least privilege.
- PROD-016: reproducible migrations, roles and configuration.
- RISK-0031: primary cross-tenant leakage control.
- RISK-0033: removes local-only persistence from production candidate architecture.
