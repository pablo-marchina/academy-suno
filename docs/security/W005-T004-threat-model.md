# W005-T004 — Multi-tenant security threat model

`TASK_ID: W005-T004`
`ATTEMPT_ID: A01`
`DATE: 2026-09-22`
`SCOPE: identity, tenant authorization, data/object isolation, PDF ingestion, secrets, audit and telemetry`

## Security objective

Protect every private Academy Suno resource so an authenticated or unauthenticated actor cannot read, mutate, trigger processing for, or infer another tenant's content through normal product interfaces, background jobs, object storage, telemetry or administrative tooling. Security-critical boundaries fail closed.

Hard acceptance properties inherited from the Production Contract:

- defined cross-tenant unauthorized successes: `0`;
- private persisted resources with tenant/provenance binding: `100%`;
- arbitrary server filesystem paths accepted from untrusted production input: `0`;
- source/run/artifact operations without required provenance: `0`.

## Assets

1. User identities, sessions, tokens and authenticators.
2. Organization/workspace memberships, roles and permissions.
3. Uploaded source PDFs and object versions.
4. Extracted facts, citations, page/chunk derivatives and embeddings.
5. 3×3 workflow runs, outputs, evals and repair artifacts.
6. Audit trail and security events.
7. Signed transfer URLs/SAS/session URIs.
8. Database credentials, API keys, model/provider credentials and signing keys.
9. Database backups/object versions and recovery artifacts.
10. Telemetry: traces, logs, prompts/outputs, cost/latency and identifiers.
11. Deployment/CI identities and administrative credentials.

## Trust boundaries

```text
[Browser/User]
    | 1: OIDC/session
    v
[Identity Provider] ---- federation metadata / claims ----> [API]
                                                   | 2
                                                   v
                                   [Authorization + Tenant Context]
                                      |          |          |
                                      |3         |4         |5
                                      v          v          v
                               [Relational DB] [Object] [Queue/Cache]
                                               Storage
                                      \          |          /
                                       \         |         /
                                        v        v        v
                                      [Workers / Parser Sandbox]
                                               | 6
                                               v
                                      [External AI Providers]
                                               |
                                               v
                                        [Observability]

[CI/CD + Operators] ---- privileged control plane ----> runtime/data services
```

Boundary expectations:

1. Browser does not become trusted because it is authenticated. IDs/roles/tenant selectors are still untrusted request data.
2. API establishes current principal, membership and permission before resource access.
3. DB enforces tenant row boundary independently where supported.
4. Object store is private; access is exact-object scoped and tenant-bound.
5. Jobs/cache entries carry stable tenant/resource identity and are revalidated by workers.
6. External providers receive only data explicitly permitted by provider/data policy; secrets never transit prompts.
7. Observability is metadata-first and redacted; it is not an unrestricted content replica.
8. CI/deploy/operator privileges are separated from ordinary data access.

## Threats, controls and verification

| ID | Threat / abuse case | Primary controls | Required verification |
|---|---|---|---|
| TM-01 | IDOR/BOLA: actor guesses another tenant's document/run/artifact ID | Per-request application authz; resource loaded with org/workspace binding; deny by default; DB row policy | Cross-tenant API matrix for every protected verb/endpoint; zero success |
| TM-02 | Tenant-confusion: client changes `organization_id`, workspace, header or route selector | Principal→membership resolution server-side; client value is selector only; app-owned current context | Mutate/null/swap tenant selectors; same token must never cross org |
| TM-03 | Stale membership/role after revoke | Current membership lookup or bounded policy cache; token/session revocation strategy; audit | Role downgrade/removal while sessions/connections live; measure propagation, assert eventual deny before production SLO freeze |
| TM-04 | RLS bypass by owner/superuser/BYPASSRLS or vulnerable DB patch level | Distinct migration/runtime roles; FORCE/ENABLE RLS; no owner/BYPASSRLS runtime; patched DB version | Runtime role assertions; negative direct SQL; version gate rejects PostgreSQL versions vulnerable to CVE-2026-14666 |
| TM-05 | Connection-pool tenant state leaks A→B | Transaction-scoped tenant context; checkout initialization; guaranteed cleanup; absent context deny | A request, connection return, B request; repeat through success/error/retry/cancel paths |
| TM-06 | Cross-tenant FK/reference or mass assignment creates mixed ownership | Tenant columns not client-authoritative; composite constraints/FKs where practical; mutation policies | Attempt create/update with foreign tenant IDs; must fail |
| TM-07 | Object key/path traversal or prefix substitution | Server-generated opaque keys; original name metadata only; no production filesystem path API | Traversal filenames, encoded separators, direct key substitution, cross-prefix signing attempts |
| TM-08 | Signed URL/SAS leakage/replay exposes private object | Exact key/method scope, short expiry, TLS, no logging, temporary/workload credentials, current authz before mint | Inspect logs/traces; expired/wrong-method/wrong-object use denied; raw bucket private |
| TM-09 | Malicious PDF exploits parser or exhausts resources | Quarantine, signature/type checks, sandbox/no-network parser, AV/CDR as applicable, bounded CPU/memory/time/pages | Malformed/corrupt/encrypted/resource-exhaustion fixtures; zero processing before CLEAN |
| TM-10 | Upload MIME/extension spoof bypasses checks | Allowlist + content/signature/structure checks; generated key; scanner state machine | Spoofed MIME/extension/polyglot-style fixtures; reject/quarantine |
| TM-11 | Provenance tampering swaps source bytes after evaluation | Strong source hash, object version, immutable provenance binding, processing starts only on validated version | Modify/re-upload bytes under same display filename; run must bind exact hash/version |
| TM-12 | Queue/cache cross-tenant mix-up | Tenant/resource IDs in job/cache keys; worker reloads and reauthorizes binding; idempotent job identity | Swap tenant/job IDs; poisoned cache key; worker refuses inconsistent binding |
| TM-13 | Secret compromise through code/CI/logs | Central secret manager, dynamic/short-lived credentials where possible, least privilege, rotation/revocation, secret scanning | Repository/CI/log scans; role-permission tests; rotation exercise |
| TM-14 | Telemetry leaks PDFs/prompts/tokens/signed URLs | Metadata-first telemetry; classification/redaction; no secrets/tokens/signed query strings; governed content capture only | Automated log/trace canaries and pattern tests; manual security review |
| TM-15 | Incomplete document deletion leaves derivatives accessible | Explicit retention/deletion graph across source, derivatives, artifacts, indexes and telemetry; audit/tombstone | Delete fixture then probe every storage/index path; backup behavior documented separately |
| TM-16 | Invitation/domain/SSO mapping grants wrong tenant | Verified invitation/membership transition; app-owned org membership; IdP claims mapped through policy | Invite replay, wrong org, changed email/domain, conflicting group mapping tests |
| TM-17 | Tenant enumeration leaks existence or metadata | Non-disclosing authorization errors, rate limits, opaque IDs, no cross-tenant search suggestions | Compare responses/timing/metadata for existent vs non-existent foreign IDs |
| TM-18 | Audit trail altered or omitted | Append-oriented audit events, restricted writer, correlation IDs, immutable export/storage where justified | Unauthorized update/delete attempts; event completeness test on privileged actions |
| TM-19 | Backups silently omit rows due to RLS | Dedicated backup role/procedure; backup verification; PostgreSQL `row_security=off` safety behavior where applicable | Backup/restore fixture with tenants A+B; count/hash reconciliation |
| TM-20 | External AI/provider receives content beyond policy | Provider adapter policy, minimum required payload, tenant/provider configuration, DPA/retention decision elsewhere | Provider request capture in test; assert allowed fields only; separate provider research required |
| TM-21 | Break-glass/operator access becomes routine data bypass | Separate privileged identity, just-in-time where possible, strong MFA, explicit reason, audit/alert | Exercise break-glass path; verify approval/audit and no default app use |
| TM-22 | CSRF/session fixation/mix-up compromises authenticated action | Modern OAuth/OIDC flow, PKCE/nonce/state as applicable, secure cookies/session rotation, exact redirect configuration | Auth flow security tests; invalid issuer/audience/nonce/state/replay rejected |

## Abuse-case narratives

### A. Authenticated tenant-A editor requests tenant-B document

Attacker changes a document UUID in the route. API must load the document with tenant binding and evaluate current tenant-A membership against that resource. Data-layer policy is a second barrier. Response must not expose the document; telemetry records only safe identifiers/classified denial metadata.

### B. Connection reused after exception

A transaction for org A sets tenant context, raises an exception and returns a pooled DB connection. The next request belongs to org B. Cleanup/transaction scoping must ensure the previous context cannot survive. Missing context must deny, not default to broad access.

### C. Malicious PDF with benign filename

A user uploads `report.pdf`, but bytes are malformed or crafted to attack the parser. Extension/MIME alone cannot promote it. The object remains quarantined; scanning/parsing occurs in a bounded sandbox and failure cannot enqueue downstream processing.

### D. Leaked signed download URL

A signed URL appears in telemetry. Because signed grants are possession-based capabilities, this is an incident. The design therefore forbids query strings/tokens in normal logs, keeps grants short-lived and scopes them to one object/method. Provider-specific revocation behavior must be understood before production.

### E. Membership revoked during long-lived DB session

A user's role is removed while a database plan/session remains alive. PostgreSQL CVE-2026-14666 shows why patch-level security is not optional: affected versions could reuse stale row policies after role changes. Deployment must reject vulnerable patch levels and the test suite must exercise live revocation.

## Least-privilege matrix

| Principal | Allowed | Explicitly not allowed |
|---|---|---|
| browser user | application API under own memberships | direct DB/object-store credentials; arbitrary paths; server roles |
| API runtime | tenant-scoped metadata/data operations; mint exact object grants if authorized | DDL, superuser, BYPASSRLS, broad object listing, secret administration |
| DB migrator | schema migrations under controlled deploy | normal request execution; interactive user traffic |
| scanner | read quarantine; write validated status/clean area | org admin, arbitrary DB queries, external network by default |
| workflow worker | read CLEAN assigned source; write assigned run/artifacts | global tenant enumeration; DDL; membership changes |
| observability exporter | metrics/events/redacted metadata | raw secrets/tokens/private document payload by default |
| CI/deployer | deploy/migrate via scoped identity | routine production document read |
| break-glass operator | exceptional diagnosed access under policy | persistent application identity or unaudited normal use |

## Data retention and privacy boundary

Retention must be explicit per resource class and legal basis. The system should support `retention_class`, expiration, legal hold and a deletion workflow without inventing an Academy Suno retention duration. LGPD arts. 15–16 support purpose/necessity-driven treatment termination and elimination subject to statutory retention exceptions; legal interpretation for Suno remains outside this worker's authority.

## Security evidence required before production claim

- cross-tenant API + DB + object + queue/cache test suite PASS with zero unauthorized success;
- runtime role/DB patch/version assertions PASS;
- upload quarantine negative controls PASS;
- secret/log/trace leakage tests PASS;
- backup/restore and deletion/retention scenarios PASS;
- dependency/security scan results attached to target deployment;
- explicit provider/data-processing decisions for external AI and identity/storage vendors.

## Residual risks / unknowns

- Suno enterprise IdP/SSO/SCIM requirements: unknown.
- Production data classification and exact legal retention calendar: unknown.
- Provider DPAs/data residency and external AI retention: separate W005 decision inputs required.
- Real workload scale/capacity: unknown and must be measured.
- No vendor/platform decision is implied by this threat model.
