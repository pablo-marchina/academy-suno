# W005-T004 — Cross-tenant authorization and isolation test plan

`TASK_ID: W005-T004`
`ATTEMPT_ID: A01`
`DATE: 2026-09-22`
`PURPOSE: executable acceptance model for PROD-001/003/004/014/016`

## 1. Non-compensatory hard gates

The following gates are release-blocking. Latency/cost/usability scores cannot compensate for failure.

| Metric | Gate |
|---|---:|
| cross-tenant unauthorized successful operations | `0` |
| private persisted resources missing tenant/provenance binding | `0` |
| operations allowed with missing tenant context where tenant context is required | `0` |
| public/unauthenticated reads of private object storage | `0` |
| quarantine objects processed before CLEAN promotion | `0` |
| runtime DB roles with superuser/table-owner/BYPASSRLS authority | `0` |
| accepted runs/artifacts bound to wrong source hash/version | `0` |

No arbitrary target is set here for auth latency, revocation propagation, upload size, scan latency or capacity. Those thresholds require benchmark/product evidence.

## 2. Canonical fixture

### Principals

- `A_OWNER`: owner of org A.
- `A_EDITOR`: editor in org A workspace A1.
- `A_VIEWER`: read-only user in org A workspace A1.
- `A2_EDITOR`: editor only in org A workspace A2.
- `B_OWNER`: owner of org B workspace B1.
- `OUTSIDER`: authenticated but member of neither org.
- `SERVICE_WORKER`: non-human runtime principal.
- `REVOKED_A_EDITOR`: same identity as A_EDITOR after membership revocation.

### Tenants/resources

```text
ORG_A
  WS_A1 -> DOC_A1, RUN_A1, ARTIFACT_A1
  WS_A2 -> DOC_A2, RUN_A2, ARTIFACT_A2

ORG_B
  WS_B1 -> DOC_B1, RUN_B1, ARTIFACT_B1
```

Every private fixture records stable `organization_id`, `workspace_id`, creator/actor where applicable, source hash and provenance.

## 3. Authorization oracle

Each protected operation has a machine-readable policy expectation:

```text
principal + action + resource -> ALLOW | DENY
```

The test harness must never infer success from HTTP status alone. For writes, verify database/object state after the request. For reads, verify response body/headers do not contain foreign resource data. For asynchronous operations, verify no foreign job/event/artifact was created.

Suggested policy actions:

- `document.create`, `document.read`, `document.delete`, `document.download`;
- `run.create`, `run.read`, `run.cancel`, `run.retry`;
- `artifact.read`, `artifact.export`;
- `workspace.read`, `workspace.manage_members`;
- `audit.read`;
- `experiment.read` where tenant-scoped;
- administrative actions explicitly separated from normal member actions.

## 4. API/IDOR matrix

For **every protected endpoint** and each CRUD/export/run action:

1. allowed own-tenant case succeeds;
2. same-org but insufficient-role case denies;
3. same-org different-workspace case denies unless policy explicitly grants org-wide scope;
4. cross-org resource ID substitution denies;
5. outsider denies;
6. unauthenticated denies;
7. deleted/revoked membership denies;
8. null/omitted tenant selector denies when required;
9. client-supplied role/user/tenant fields cannot elevate authority;
10. collection/list/search endpoints return only authorized rows.

### Required mutations

- swap UUID/resource IDs in path, query and body;
- URL-encode/mixed-case parameter variations where routing allows;
- duplicate parameters;
- mass-assign `organization_id`, `workspace_id`, `owner_id`, `role`;
- filter/sort/search for known foreign identifiers;
- request foreign export/download directly;
- attempt cancel/retry of foreign run;
- attempt to use a valid tenant-A request idempotency key against tenant B.

Expected outcome: no cross-tenant operation changes or returns foreign state.

## 5. Authentication/session/federation tests

- invalid/unknown issuer rejected;
- incorrect audience rejected;
- expired token/session rejected;
- invalid signature rejected;
- nonce/state/PKCE flow errors rejected as applicable;
- session fixation prevention verified on privilege/sign-in transitions;
- organization switch does not retain prior workspace privileges;
- role downgrade/revocation is measured with a live session until denial takes effect;
- email change does not alter resource ownership identity;
- same email from different issuer/subject does not automatically merge identities;
- invitation replay and invitation-to-wrong-org denied;
- IdP group/role claims cannot directly override application membership without configured mapping policy.

Record actual revocation propagation distribution before setting a production SLO.

## 6. Database/RLS tests (if candidate uses PostgreSQL RLS)

### Deployment assertions

- database version is a supported patched release; specifically reject versions before PostgreSQL 18.6/17.11/16.15/15.19/14.24 within those major branches because of CVE-2026-14666;
- runtime role: `rolsuper=false`, `rolbypassrls=false`;
- runtime role is not owner of protected tables;
- protected tables have RLS enabled and required policies installed;
- FORCE RLS applied where owner behavior could otherwise bypass policy;
- migration/owner role credentials are not present in API/worker runtime environment.

### Direct policy cases

Under org A context:

- SELECT org-A rows allowed per role; org-B rows invisible/denied;
- INSERT with org B tenant key denied;
- UPDATE org-A row to org-B tenant key denied;
- UPDATE/DELETE org-B row denied/no-op without leakage;
- missing/invalid tenant context denies all protected access;
- cross-tenant foreign-key/reference creation denied by schema/policy design;
- unique/FK error behavior is checked for unintended foreign-tenant existence leakage.

Repeat for org B and outsider/service roles.

### Connection-pool isolation

Run sequences repeatedly with a small pool to maximize reuse:

1. tenant A transaction → commit → tenant B transaction;
2. tenant A transaction → application exception → tenant B;
3. tenant A transaction → DB error → tenant B;
4. tenant A transaction → timeout/cancel → tenant B;
5. tenant A transaction → retry path → tenant B;
6. role/membership revocation while a connection/plan remains live.

At no point may B observe A's tenant context or data.

## 7. Object storage tests

### Private-by-default

- direct unauthenticated object URL returns no private bytes;
- bucket/container listing unavailable to browser principals;
- public ACL/policy configuration check fails deployment if private store becomes public.

### Upload authorization

- A user cannot mint an upload grant under org B/workspace B1;
- client-supplied filename such as `../b/report.pdf` never controls object path;
- app-generated object key remains under authoritative org/workspace/document binding;
- signed PUT/SAS grant cannot be reused for another object/method;
- wrong checksum/content constraints reject where configured;
- expired grant fails;
- signed grant query/token is absent from logs/traces/analytics.

### Download/delete

- tenant A cannot receive a signed read/delete grant for B object;
- viewer/editor/admin policy is applied before minting;
- foreign raw object key does not bypass resource authorization;
- deleted membership loses ability to mint new grants;
- existing grant exposure window is measured and included in the risk record.

## 8. Secure PDF ingestion negative controls

Corpus must include versioned fixtures for:

- valid PDF;
- spoofed MIME;
- `.pdf` filename with non-PDF bytes;
- corrupt/truncated PDF;
- encrypted/password-protected PDF;
- duplicate bytes under different names;
- traversal/reserved/special-character original filenames;
- malformed structures known to stress parsers;
- resource-exhaustion fixture bounded for test safety;
- scanner unavailable/timeout;
- parser crash;
- object changed after upload intent/checksum expectation.

Assertions:

- every object begins QUARANTINED;
- only successful validation transitions to CLEAN;
- no downstream workflow job exists before CLEAN;
- hash/object-version in run provenance exactly matches validated bytes;
- failed scans cannot be retried into processing without revalidation;
- scanner/parser has no broad object/database privilege and no outbound network by default.

## 9. Queue/cache/worker isolation

- job payload contains immutable tenant/workspace/resource identity, not merely a raw object path;
- worker reloads authoritative resource binding before processing;
- swap tenant ID or resource ID in queued payload → reject;
- cache keys include tenant boundary for tenant-specific values;
- cache poisoning with same logical key in A/B cannot return foreign values;
- worker retry/idempotency cannot attach output to another tenant's run;
- cancellation of foreign job denied at API and worker control plane.

## 10. Secrets and least-privilege tests

- repository secret scanning: no production credentials committed;
- runtime inventory proves each service receives only required secret names/scopes;
- API DB credentials cannot DDL/GRANT/BYPASSRLS;
- scanner credentials cannot list/read all tenants;
- CI/deploy identity cannot read production documents in normal path;
- rotate/revoke one representative credential and verify recovery without code change;
- break-glass use emits high-signal audit event and is not required for normal flow.

## 11. Logging/telemetry redaction tests

Inject unique canary values into:

- PDF body;
- prompt/output fixture;
- access token;
- signed object URL query;
- secret/API key fixture;
- DB connection string.

Then query all accessible logs/traces/metrics/analytics artifacts. Hard assertion: token/secret/signed-query canaries never appear in plaintext. Document/prompt canaries may appear only if a separately governed content-capture mode was explicitly enabled for the test; default path must omit/redact them.

Telemetry should retain safe correlation via opaque `organization_id/workspace_id/document_id/run_id`, source hash, event type, latency, cost/tokens and classified error details.

## 12. Deletion, retention and backup tests

For a test document:

1. enumerate source object/version, extracted text/chunks, embeddings/index records, runs/artifacts and content-bearing telemetry refs;
2. execute policy-authorized deletion;
3. verify all online derivatives are inaccessible/deleted/tombstoned as specified;
4. verify audit event records actor/reason/resource without leaking content;
5. verify future signed grants cannot be minted;
6. document backup lifecycle separately — immutable backup expiry is not falsely represented as immediate deletion;
7. perform full backup/restore fixture and reconcile tenant row/object counts + hashes.

If PostgreSQL RLS is used, backup tooling should fail loudly rather than silently filtering rows; test the chosen procedure accordingly.

## 13. Fuzz/property-based layer

Property to enforce across generated fixtures:

> For any principal P, resource R and action A, if P lacks current authorization for R's organization/workspace, executing A cannot reveal or mutate R and cannot create a derivative/job/audit payload containing R's private data outside the authorized security boundary.

Generate:

- random tenant/resource UUID swaps;
- null/empty/oversized IDs;
- duplicate tenant memberships;
- revoked memberships;
- nested resources with mismatched parent IDs;
- random ordering/interleaving of A/B requests over a reused connection pool.

Persist seed/config for any failure.

## 14. Evidence artifact schema

Each security run should persist machine-readable results:

```json
{
  "suite_version": "...",
  "deployment_sha": "...",
  "database_version": "...",
  "cases_total": 0,
  "cases_passed": 0,
  "cross_tenant_unauthorized_successes": 0,
  "private_resources_missing_tenant_provenance": 0,
  "quarantine_bypasses": 0,
  "raw_private_object_public_reads": 0,
  "secret_or_token_plaintext_leaks": 0,
  "failures": []
}
```

Do not reduce the suite to one weighted score. Report hard-gate counts and latency/operational metrics separately.

## 15. Exit criteria

This plan is implementation-ready when the production architecture selects concrete API/database/object-store/runtime components. Production readiness may only claim this security slice after:

- all non-compensatory gates pass;
- the suite is run against the same real product path used by the final system;
- artifacts are persisted with deployment/config provenance;
- security findings are either fixed or explicitly block the claim.
