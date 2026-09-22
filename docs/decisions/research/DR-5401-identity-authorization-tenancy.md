# DR-5401 — Identity, authorization and tenant-context architecture

`TASK_ID: W005-T004`
`ATTEMPT_ID: A01`
`RESEARCH_DATE: 2026-09-22`
`STATUS: CANDIDATE / NO_VENDOR_PREFERENCE`
`CONFIDENCE: HIGH for security invariants; MEDIUM for candidate application model; LOW for vendor selection`

## 1. Decision question

What production identity/authentication, organization/workspace, RBAC/authorization and tenant-context architecture should Academy Suno use to satisfy PROD-001/014 without prematurely selecting a vendor?

## 2. Workload / constraints

Academy Suno must be a real multi-user, multi-tenant product. Private documents, runs and generated artifacts must never cross tenant boundaries. The current project has no verified Suno identity provider, SSO requirement, user-count target or procurement constraint. Therefore vendor choice is not evidence-complete.

Hard requirements:

- explicit `organization/workspace/user/run` dimensions;
- authorization on every protected operation;
- cross-tenant unauthorized success = `0` in the defined adversarial suite;
- every private persisted resource has tenant/provenance binding;
- standards-based federation so an enterprise IdP can be connected later without changing application resource identity;
- no trust in client-supplied tenant IDs or roles as authorization facts;
- secrets and session/token material never enter normal telemetry.

## 3. Alternatives

### A. Managed B2B identity platform
Examples evaluated as capability references: WorkOS/AuthKit, Clerk Organizations, Auth0 Organizations. Advantages include hosted authentication, organization membership primitives and enterprise SSO integrations. Trade-offs include vendor-specific organization/role APIs, feature-tier pricing, connection pricing and migration coupling.

### B. Self-hosted identity provider
Keycloak is the representative candidate: standards-based OIDC/SAML, realms, roles and groups with full operational control. Trade-off: the product team owns security patching, high availability, upgrades, backups, monitoring and federation configuration.

### C. Integrated application platform identity
Supabase Auth + Postgres/RLS is a representative integrated option. It can reduce integration surface, but couples identity/data-policy decisions and should not be selected before the broader W005 architecture fan-in.

### D. Application-built credential system
Rejected as a production default. Building password/MFA/federation infrastructure in-product creates avoidable credential-security and lifecycle burden when standards-compliant identity systems already exist.

## 4. Evaluation criteria

Defined before a vendor outcome:

1. standards interoperability (OIDC/OAuth 2.0, enterprise federation path);
2. phishing-resistant MFA/passkey capability or integration path;
3. organization membership + role/permission model;
4. safe session/token lifecycle and revocation behavior;
5. separation between external identity and internal resource ownership;
6. auditability and least privilege;
7. SSO/SCIM readiness without assuming Suno policy;
8. operational burden, availability responsibility and patching burden;
9. pricing/lock-in and migration surface;
10. ability to enforce application-owned tenant authorization independently of provider claims.

No weighted total score is used because user scale, SSO connection count, enterprise procurement policy and operational ownership are unknown.

## 5. Systematic source search

Search categories on 2026-09-22:

- current digital identity standards/guidance;
- OAuth/OIDC security requirements;
- authorization guidance;
- official vendor organization/RBAC documentation;
- self-hosted identity documentation;
- integrated-platform RLS/auth documentation;
- current pricing/plan pages where available.

Stopping rule: search stopped after standards/security requirements were supported by primary sources and materially different vendor classes (managed B2B, self-hosted, integrated platform) were covered. Further vendor pages changed implementation details/pricing but did not alter the architectural invariant that application authorization must remain provider-independent. Vendor selection remains open because representative enterprise requirements and hands-on bakeoff evidence are absent.

## 6. Source table

| Source | Type / freshness | Supported claim | Limitation |
|---|---|---|---|
| NIST SP 800-63-4, July 2025 — https://csrc.nist.gov/pubs/sp/800/63/4/final | Primary standard/guidance | Current identity proofing/authentication/federation baseline; supersedes 800-63-3 | Government-oriented assurance guidance; not a vendor-selection benchmark |
| RFC 9700, Jan 2025 — https://www.rfc-editor.org/info/rfc9700/ | IETF BCP | OAuth redirect flows require modern defenses; public clients must use PKCE and confidential clients are recommended to use it | Does not define Academy Suno roles/data model |
| OpenID Connect Core — https://openid.net/specs/openid-connect-core-1_0.html | Standard | Issuer/audience/nonce validation and federated identity semantics | Does not provide application authorization |
| OWASP Authorization Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | Security guidance, current | Validate authorization on every request; deny by default | General guidance, not a product-specific implementation |
| WorkOS RBAC — https://workos.com/docs/rbac | Vendor primary docs, current | Organization-scoped roles/permissions and enterprise identity mapping capabilities | Vendor claims; no Academy Suno bakeoff |
| Clerk Organizations — https://clerk.com/docs/guides/organizations/overview | Vendor primary docs, current | Multi-tenant organization context and role/permission capabilities | Vendor claims; no Academy Suno bakeoff |
| Auth0 Organizations — https://auth0.com/docs/manage-users/organizations/create-first-organization | Vendor primary docs, current | Organization membership/connections/roles capabilities | Plan-dependent; no Academy Suno bakeoff |
| Keycloak Server Administration Guide — https://www.keycloak.org/docs/latest/server_admin/ | Vendor/project primary docs, current | Self-hosted realms, users, groups and roles | Operational burden must be measured in target deployment |
| Supabase RLS guide — https://supabase.com/docs/guides/database/postgres/row-level-security | Vendor primary docs, current | Integrated Auth/Postgres policy pattern; RLS should be enabled/tested on exposed tables | Coupled platform candidate; no target-stack decision yet |

Current pricing pages were inspected only as volatility evidence; prices are not copied into a locked decision because they can change and the required connection/user counts are unknown.

## 7. Primary evidence first

Standards and security guidance establish the invariant layer. Vendor documentation is used only to show that credible implementation classes exist; vendor marketing is not treated as proof of superiority.

## 8. Security / reliability / cost / lock-in

### Security invariants

- Use OIDC/OAuth 2.0 authorization-code flow with PKCE (`S256`) for browser/native-style public clients; validate issuer, audience, nonce/state as applicable.
- External identity maps to an internal identity by stable `(issuer, subject)`; **email is not the primary authorization key**.
- Authentication establishes a principal. Authorization is computed by the application from current membership + permission + resource tenant binding.
- A client-supplied `organization_id`, `workspace_id`, user ID or role is never accepted as authority. It is a selector that must be checked against the authenticated principal.
- Keep organization/workspace membership state in application-owned storage so provider migration does not rewrite resource ownership.
- Provider group/role claims may seed/synchronize memberships, but do not bypass application authorization.
- Revocation/membership changes must be measurable and tested for propagation; no arbitrary revocation SLO is invented in this research task.
- Support phishing-resistant authenticators/passkeys where the selected IdP and deployment policy allow; exact assurance level requires stakeholder policy.

### Candidate internal model

```text
users(id, status, ...)
external_identities(user_id, issuer, subject, ... UNIQUE(issuer, subject))
organizations(id, ...)
organization_memberships(organization_id, user_id, role, status, ...)
workspaces(id, organization_id, ...)
workspace_memberships(workspace_id, user_id, role, status, ...)  # only if workspace ACL differs
resources(..., organization_id, workspace_id, created_by_user_id, ...)
audit_events(..., organization_id, workspace_id, actor_user_id, action, resource_type, resource_id, ...)
```

Minimal role vocabulary should remain small and permission-backed. Candidate roles: `org_owner`, `org_admin`, `workspace_editor`, `workspace_viewer`, plus non-human service principals. The final permission catalog belongs to implementation design and must be regression tested.

### Reliability and operations

- Managed providers externalize availability/patching but create dependency on their service and plan limits.
- Self-hosted providers reduce SaaS dependency but move patching, HA, backup, federation and incident response onto the Academy Suno operator.
- Sessions/tokens should be short-lived enough for risk posture, with revocation and reauthentication behavior defined by the selected provider; exact durations remain pending evidence/policy.

### Cost and lock-in

No current volume model exists. Per-user or per-enterprise-connection pricing may dominate at different scales, while self-hosting shifts spend into operations. This prevents a defensible vendor winner now.

## 9. Reproducible benchmark / experiment

Vendor selection requires a later bakeoff using one identical reference flow per candidate:

1. sign-in and token validation;
2. create/join organization;
3. organization switch;
4. role downgrade/revocation;
5. SSO connection path if required;
6. service-to-service identity;
7. export audit events;
8. failover/provider outage behavior;
9. migration/export of users and membership identifiers;
10. operator time + integration code surface + observed end-to-end auth latency.

Dataset: tenants A/B, five users and role matrix defined in `docs/security/W005-T004-cross-tenant-authz-test-plan.md`.

No live vendor account benchmark was executed in A01, so no vendor may be promoted.

## 10. Raw results + uncertainty

Observed across primary docs: each credible vendor class can support standards-based authentication and some organization/role mechanism, but these features do not prove application data isolation. Authorization completeness and tenant binding remain Academy Suno responsibilities.

Unknowns that materially affect selection: Suno SSO/SCIM requirements, IdP, number of organizations/users, data residency, procurement constraints, availability target, operating team, budget and desired self-hosting responsibility.

## 11. Decision

`NO_VENDOR_PREFERENCE`.

Architectural invariants are strong enough to promote as candidate requirements:

- standards-based OIDC/OAuth identity;
- stable internal user/org/workspace identifiers separated from provider identity;
- application-owned authorization state;
- per-request resource authorization;
- deny-by-default cross-tenant behavior;
- SSO/SCIM-ready adapter boundary rather than vendor-specific ownership keys.

The exact identity provider remains `PENDING_EVIDENCE` for W005-T010/T012 or a dedicated implementation bakeoff.

## 12. Confidence

- Security/identity invariants: **HIGH** — standards + OWASP converge and do not depend on product scale.
- Internal application model: **MEDIUM-HIGH** — directly satisfies current requirements, but final permission granularity depends on UX/workflow.
- Vendor preference: **LOW / intentionally none** — missing target requirements and benchmark.

## 13. Reversal conditions

Reopen the model if:

- Suno mandates a specific enterprise IdP/protocol or data-residency control;
- selected platform cannot export stable external identity identifiers/memberships;
- production workflows require resource sharing across organizations;
- measured vendor integration/latency/availability/cost materially changes the Pareto frontier;
- a target regulatory assurance level requires stronger identity proofing than currently known.

## 14. Traceability

- PROD-001: explicit identity/organization/workspace/user binding and authorization.
- PROD-014: authz tests, least privilege, session/token controls.
- PROD-016: externalized secrets/configuration and reproducible provider adapter boundary.
- RISK-0031: cross-tenant leakage controlled by provider-independent application authz + data-layer enforcement.
- RISK-0037: tokens/session values excluded from telemetry.
