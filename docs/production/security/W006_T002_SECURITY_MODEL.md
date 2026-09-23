# W006-T002 Identity / Tenancy / Session / SSE Security Substrate

`TASK_ID: W006-T002`  
`ATTEMPT_ID: A01`  
`CONTRACT_INPUT: W006-T001-A02`  
`IMPLEMENTATION_STATUS: CANDIDATE_SUBSTRATE_WITH_EXECUTABLE_ADVERSARIAL_TESTS`  
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`

## 1. Scope and decision boundary

This artifact defines the portable security invariants implemented by
`src/suno_content/security/` and exercised by
`tests/integration/foundation/test_tenant_security.py`.

It intentionally does **not** select an identity provider, relational engine,
RLS implementation, object-store vendor, session store, or cursor persistence
backend. Those material choices remain evidence-gated by the Decision Research
process. The in-process directory and cursor vault are a reference substrate
and deterministic security harness, not a claim that in-memory state is
production persistence.

The implementation consumes the accepted W006-T001 contract direction:

- tenant authority is explicit in `org_id + workspace_id`;
- protected resources are tenant/provenance bound;
- replay cursor is opaque/position-oriented and is not a tenant selector;
- an authorized stream is identified independently by tenant/workspace/run;
- telemetry is allowlist/default-deny.

## 2. Trust boundaries

### External identity boundary

External authentication contributes only the stable principal tuple
`(issuer, subject)`. That tuple maps to one internal `user_id`.

External claims such as organization/workspace name, e-mail domain, group text,
URL parameters, cursor contents, or request payload tenant IDs are **not**
authorization authority.

Remapping the same `(issuer, subject)` to a different internal user fails
closed.

### Application authorization boundary

Workspace membership is application-owned, server-authoritative state.
Every protected request resolves the current session, then resolves the active
membership for the session's current `org_id + workspace_id`.

Authorization is deny-by-default. Roles have explicit actions; there is no
wildcard/fallback permission path.

Every access decision revalidates the captured security context against current
session and membership state. Session revocation, membership revocation, role
change, membership epoch change, or organization/workspace switch therefore
invalidates stale contexts.

### Resource/data/object/event/trace boundary

Protected resources carry:

- `org_id`;
- `workspace_id`;
- `resource_id`;
- `provenance_id`;
- security surface (`api`, `data`, `object`, `event`, `trace`).

The authorizer first checks that the resource tenant exactly equals the
server-authoritative context tenant, then evaluates the explicit role/action
permission. Cross-tenant access is rejected before serialization/return.

Object keys, database predicates, trace selectors, and API route parameters are
therefore implementation inputs only; adapters must bind them to the resolved
tenant context rather than treating them as authority.

## 3. Browser credential topology selected for API + SSE

The browser topology for this substrate is:

1. same-origin browser requests;
2. a **host-only, Secure, HttpOnly, SameSite=Lax, Path=/** session cookie;
3. no browser bearer/session credential in URL query parameters;
4. no browser bearer credential in the `Authorization` header for this
   topology;
5. mutating API methods require a separate session-bound CSRF header;
6. SSE uses `GET` with the same secure session cookie;
7. SSE resume position is carried only as an opaque `Last-Event-ID` cursor;
8. credentials are never encoded in `Last-Event-ID`.

The framework/IdP/session-store implementation remains replaceable. An HTTP
adapter must preserve these properties and issue high-entropy session/CSRF
credentials using a production-grade secret/session store.

## 4. SSE and replay authorization

The cursor vault models the required security semantics independently of a
storage vendor.

Cursor issuance requires an already-authorized `EVENT_CONNECT` decision for an
explicit `AuthorizedStream(org_id, workspace_id, run_id)`.

A cursor token is opaque and does not expose tenant/run selectors. The
server-side cursor record is bound to:

- authorized stream;
- session ID and session epoch;
- membership ID and membership epoch;
- last event revision.

Resume requires all of the following again:

- current non-revoked/non-expired session;
- current active membership;
- exact current tenant/workspace match;
- `EVENT_RESUME` permission;
- exact stream match;
- exact session/membership epoch match.

Therefore the cursor cannot independently select a tenant/run, and revocation
or org switching invalidates replay authority.

The reference vault is intentionally non-durable. A production cursor backend
must preserve these semantics and pass the same adversarial suite before
promotion.

## 5. Revocation and organization switching

Session revocation increments a session epoch and marks the session inactive.

Membership revocation increments a membership epoch and marks membership
inactive.

Organization/workspace switching:

1. validates that the user has an active membership in the target workspace;
2. changes only server-side session authority;
3. increments the session epoch;
4. invalidates the old context and old replay cursors.

A switched session cannot retain prior-tenant API/object/event access merely
because the browser still possesses an old resource ID or cursor.

## 6. Service-identity separation

The substrate requires four distinct service principals:

| Identity | Allowed capability family |
|---|---|
| runtime | serve API, tenant-bound data/object read/write |
| migrator | schema migration only |
| worker | execute jobs plus tenant-bound data/object read/write |
| backup | backup read / restore write |

All four identity IDs must be present, non-empty, and distinct.

The policy explicitly denies, among other combinations:

- runtime → schema migration;
- runtime → backup/restore;
- worker → schema migration;
- worker → backup/restore;
- migrator → application runtime/job work.

Concrete cloud/database IAM roles remain deployment-specific evidence work.

## 7. Secret and credential exposure control

Telemetry attributes use the exact accepted T001 allowlist as the starting
boundary. Unknown attributes are dropped. Non-scalar values are dropped.
Credential-shaped field names are denied even if accidentally introduced.

Product-event payload sanitization recursively removes credential-shaped fields
and redacts configured secret canary values.

The deterministic adversarial test injects the same secret canary into nested
event data, telemetry status, authorization/cookie-shaped fields, and unknown
raw payloads, then proves the serialized sanitized output contains the canary
zero times.

This is defense in depth, not a substitute for secret management. Production
adapters must avoid putting credentials/raw secrets into events or telemetry in
the first place.

## 8. Defined adversarial acceptance matrix

The foundation test suite defines the following deterministic cases:

| Gate | Defined evidence |
|---|---|
| stable principal mapping | same external principal cannot be rebound to another internal user |
| authoritative workspace resolution | a user cannot create a session for a workspace without an active app membership |
| cross-tenant API | foreign API resource denied |
| cross-tenant data | foreign data resource denied |
| cross-tenant object | foreign object resource denied |
| cross-tenant event | foreign event stream/resource denied |
| cross-tenant trace | foreign trace resource denied |
| deny-by-default authz | viewer write denied |
| tenant/provenance binding | protected resource without provenance rejected |
| revoked session | API, SSE connect and SSE resume denied |
| revoked membership | SSE connect and resume denied |
| org switch | old context, prior-tenant object and prior-tenant cursor denied |
| cross-tenant cursor | cursor from tenant A cannot resume tenant B stream |
| cursor opacity | issued cursor does not expose org/workspace/run IDs |
| browser credential topology | query/bearer credential, missing CSRF and cross-origin SSE rejected |
| session expiry | expired session denied |
| service identity separation | duplicate/missing separation or forbidden capability denied |
| secret canary | serialized sanitized event + telemetry contains zero canary/credential fields |

The hard-gate interpretation is fail-closed: an unexpected success in any
defined negative case fails the suite.

## 9. What this proves and what remains open

This substrate provides executable evidence for the application-level security
invariants above. It does **not** yet prove:

- production IdP integration;
- production session-store durability/rotation;
- a selected relational engine or RLS implementation;
- object-store IAM/isolation;
- production SSE proxy/load behavior;
- durable event/replay storage;
- cloud/runtime IAM enforcement;
- full end-to-end vertical-slice isolation after T003–T006 integration;
- penetration testing, dependency scanning, deployment hardening, or production
  readiness.

Those remain downstream evidence obligations, including W006 fan-in,
integration, observability/SRE, and red-team qualification tasks.
