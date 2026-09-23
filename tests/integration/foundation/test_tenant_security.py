from __future__ import annotations

import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.security import (  # noqa: E402
    AccessSurface,
    Action,
    AuthenticationError,
    AuthorizationError,
    AuthorizedStream,
    BrowserCredentialPolicy,
    BrowserRequestCredential,
    CredentialTopologyError,
    DenyByDefaultAuthorizer,
    Membership,
    PrincipalBinding,
    ReplayCursorVault,
    ReplayDenied,
    Role,
    SecurityDirectory,
    ServiceCapability,
    ServiceIdentity,
    ServiceIdentityKind,
    TenantIsolationError,
    TenantResource,
    require_service_capability,
    sanitize_event_payload,
    sanitize_telemetry_attributes,
    validate_service_identity_separation,
)


class TenantSecurityFoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = SecurityDirectory()
        self.directory.bind_principal(
            PrincipalBinding(issuer="https://idp.example", subject="sub-alice", user_id="user-alice")
        )
        self.directory.bind_principal(
            PrincipalBinding(issuer="https://idp.example", subject="sub-bob", user_id="user-bob")
        )
        self.directory.put_membership(
            Membership(
                membership_id="m-alice-a",
                user_id="user-alice",
                org_id="org-a",
                workspace_id="ws-a",
                role=Role.EDITOR,
            )
        )
        self.directory.put_membership(
            Membership(
                membership_id="m-alice-b",
                user_id="user-alice",
                org_id="org-b",
                workspace_id="ws-b",
                role=Role.EDITOR,
            )
        )
        self.directory.put_membership(
            Membership(
                membership_id="m-bob-b",
                user_id="user-bob",
                org_id="org-b",
                workspace_id="ws-b",
                role=Role.VIEWER,
            )
        )
        self.directory.create_session(
            session_id="sess-alice",
            user_id="user-alice",
            org_id="org-a",
            workspace_id="ws-a",
            csrf_token="csrf-alice",
        )
        self.directory.create_session(
            session_id="sess-bob",
            user_id="user-bob",
            org_id="org-b",
            workspace_id="ws-b",
            csrf_token="csrf-bob",
        )
        self.authorizer = DenyByDefaultAuthorizer(self.directory)
        self.cursors = ReplayCursorVault(self.directory, self.authorizer)

    def _resource(
        self,
        surface: AccessSurface,
        *,
        org_id: str,
        workspace_id: str,
        suffix: str,
    ) -> TenantResource:
        return TenantResource(
            surface=surface,
            org_id=org_id,
            workspace_id=workspace_id,
            resource_id=f"{surface.value}-{suffix}",
            provenance_id=f"prov-{suffix}",
        )

    def test_principal_mapping_is_stable_and_tenant_claims_are_not_authority(self) -> None:
        self.assertEqual(
            self.directory.resolve_principal("https://idp.example", "sub-alice"),
            "user-alice",
        )
        with self.assertRaises(AuthenticationError):
            self.directory.bind_principal(
                PrincipalBinding(
                    issuer="https://idp.example",
                    subject="sub-alice",
                    user_id="user-bob",
                )
            )
        with self.assertRaises(AuthorizationError):
            self.directory.create_session(
                session_id="forged-tenant",
                user_id="user-bob",
                org_id="org-a",
                workspace_id="ws-a",
                csrf_token="csrf-forged",
            )

    def test_cross_tenant_unauthorized_success_is_zero_across_defined_surfaces(self) -> None:
        context = self.directory.resolve_context("sess-alice")
        attempts = (
            (AccessSurface.API, Action.API_READ),
            (AccessSurface.DATA, Action.DATA_READ),
            (AccessSurface.OBJECT, Action.OBJECT_READ),
            (AccessSurface.EVENT, Action.EVENT_CONNECT),
            (AccessSurface.TRACE, Action.TRACE_READ),
        )
        unauthorized_successes = 0
        for surface, action in attempts:
            resource = self._resource(
                surface,
                org_id="org-b",
                workspace_id="ws-b",
                suffix="foreign",
            )
            try:
                self.authorizer.require(context, resource, action)
            except TenantIsolationError:
                continue
            unauthorized_successes += 1
        self.assertEqual(unauthorized_successes, 0)

    def test_same_tenant_positive_path_and_deny_by_default_role_policy(self) -> None:
        alice = self.directory.resolve_context("sess-alice")
        for surface, action in (
            (AccessSurface.API, Action.API_READ),
            (AccessSurface.DATA, Action.DATA_READ),
            (AccessSurface.OBJECT, Action.OBJECT_READ),
            (AccessSurface.EVENT, Action.EVENT_CONNECT),
            (AccessSurface.TRACE, Action.TRACE_READ),
        ):
            self.authorizer.require(
                alice,
                self._resource(surface, org_id="org-a", workspace_id="ws-a", suffix="owned"),
                action,
            )

        bob = self.directory.resolve_context("sess-bob")
        with self.assertRaises(AuthorizationError):
            self.authorizer.require(
                bob,
                self._resource(
                    AccessSurface.DATA,
                    org_id="org-b",
                    workspace_id="ws-b",
                    suffix="write",
                ),
                Action.DATA_WRITE,
            )

    def test_protected_resource_requires_provenance(self) -> None:
        with self.assertRaises(ValueError):
            TenantResource(
                surface=AccessSurface.DATA,
                org_id="org-a",
                workspace_id="ws-a",
                resource_id="run-1",
                provenance_id="",
            )

    def test_revoked_session_denies_api_sse_connect_and_resume(self) -> None:
        context = self.directory.resolve_context("sess-alice")
        stream = AuthorizedStream("org-a", "ws-a", "run-a")
        cursor = self.cursors.issue(context, stream, last_event_revision=7)
        self.directory.revoke_session("sess-alice")

        failures = 0
        for operation in (
            lambda: self.authorizer.require(
                context,
                self._resource(
                    AccessSurface.API,
                    org_id="org-a",
                    workspace_id="ws-a",
                    suffix="api",
                ),
                Action.API_READ,
            ),
            lambda: self.authorizer.require_stream(context, stream, Action.EVENT_CONNECT),
            lambda: self.cursors.resume(context, stream, cursor_token=cursor),
        ):
            try:
                operation()
            except (AuthenticationError, ReplayDenied):
                failures += 1
        self.assertEqual(failures, 3)

    def test_revoked_membership_denies_sse_connect_and_resume(self) -> None:
        context = self.directory.resolve_context("sess-alice")
        stream = AuthorizedStream("org-a", "ws-a", "run-a")
        cursor = self.cursors.issue(context, stream, last_event_revision=9)
        self.directory.revoke_membership("user-alice", "org-a", "ws-a")

        with self.assertRaises(AuthorizationError):
            self.authorizer.require_stream(context, stream, Action.EVENT_CONNECT)
        with self.assertRaises((AuthorizationError, ReplayDenied)):
            self.cursors.resume(context, stream, cursor_token=cursor)

    def test_org_switch_invalidates_old_context_and_prior_tenant_cursor(self) -> None:
        old_context = self.directory.resolve_context("sess-alice")
        old_stream = AuthorizedStream("org-a", "ws-a", "run-a")
        old_cursor = self.cursors.issue(old_context, old_stream, last_event_revision=11)

        self.directory.switch_workspace("sess-alice", org_id="org-b", workspace_id="ws-b")
        new_context = self.directory.resolve_context("sess-alice")
        self.assertEqual((new_context.org_id, new_context.workspace_id), ("org-b", "ws-b"))

        with self.assertRaises(AuthenticationError):
            self.authorizer.require(
                old_context,
                self._resource(
                    AccessSurface.API,
                    org_id="org-a",
                    workspace_id="ws-a",
                    suffix="stale",
                ),
                Action.API_READ,
            )
        with self.assertRaises(TenantIsolationError):
            self.authorizer.require(
                new_context,
                self._resource(
                    AccessSurface.OBJECT,
                    org_id="org-a",
                    workspace_id="ws-a",
                    suffix="old-object",
                ),
                Action.OBJECT_READ,
            )
        with self.assertRaises((TenantIsolationError, ReplayDenied)):
            self.cursors.resume(new_context, old_stream, cursor_token=old_cursor)

    def test_cross_tenant_cursor_replay_success_is_zero(self) -> None:
        alice = self.directory.resolve_context("sess-alice")
        alice_stream = AuthorizedStream("org-a", "ws-a", "run-a")
        cursor = self.cursors.issue(alice, alice_stream, last_event_revision=13)

        bob = self.directory.resolve_context("sess-bob")
        bob_stream = AuthorizedStream("org-b", "ws-b", "run-b")
        cross_tenant_successes = 0
        try:
            self.cursors.resume(bob, bob_stream, cursor_token=cursor)
        except ReplayDenied:
            pass
        else:
            cross_tenant_successes += 1
        self.assertEqual(cross_tenant_successes, 0)
        self.assertNotIn("org-a", cursor)
        self.assertNotIn("ws-a", cursor)
        self.assertNotIn("run-a", cursor)

    def test_browser_credential_topology_is_cookie_only_and_csrf_bound(self) -> None:
        policy = BrowserCredentialPolicy(self.directory)
        context = policy.authenticate(
            BrowserRequestCredential(
                method="GET",
                session_cookie="sess-alice",
                same_origin=True,
                is_sse=True,
                last_event_id="opaque-cursor",
            )
        )
        self.assertEqual(context.user_id, "user-alice")

        context = policy.authenticate(
            BrowserRequestCredential(
                method="POST",
                session_cookie="sess-alice",
                same_origin=True,
                csrf_header="csrf-alice",
            )
        )
        self.assertEqual(context.workspace_id, "ws-a")

        for request in (
            BrowserRequestCredential(
                method="GET",
                session_cookie="sess-alice",
                same_origin=True,
                query_params={"access_token": "do-not-put-credentials-in-url"},
            ),
            BrowserRequestCredential(
                method="GET",
                session_cookie="sess-alice",
                same_origin=True,
                authorization_header="Bearer browser-token",
            ),
            BrowserRequestCredential(
                method="POST",
                session_cookie="sess-alice",
                same_origin=True,
            ),
            BrowserRequestCredential(
                method="GET",
                session_cookie="sess-alice",
                same_origin=False,
                is_sse=True,
            ),
        ):
            with self.assertRaises(CredentialTopologyError):
                policy.authenticate(request)

    def test_expired_session_is_denied(self) -> None:
        self.directory.create_session(
            session_id="expired",
            user_id="user-alice",
            org_id="org-a",
            workspace_id="ws-a",
            csrf_token="csrf-expired",
            expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
        )
        with self.assertRaises(AuthenticationError):
            self.directory.resolve_context("expired")

    def test_runtime_migrator_worker_backup_identities_are_separate_and_least_privilege(self) -> None:
        identities = (
            ServiceIdentity("svc-runtime", ServiceIdentityKind.RUNTIME),
            ServiceIdentity("svc-migrator", ServiceIdentityKind.MIGRATOR),
            ServiceIdentity("svc-worker", ServiceIdentityKind.WORKER),
            ServiceIdentity("svc-backup", ServiceIdentityKind.BACKUP),
        )
        validate_service_identity_separation(identities)
        require_service_capability(identities[0], ServiceCapability.API_SERVE)
        require_service_capability(identities[1], ServiceCapability.SCHEMA_MIGRATE)
        require_service_capability(identities[2], ServiceCapability.JOB_EXECUTE)
        require_service_capability(identities[3], ServiceCapability.BACKUP_READ)

        with self.assertRaises(AuthorizationError):
            require_service_capability(identities[0], ServiceCapability.SCHEMA_MIGRATE)
        with self.assertRaises(AuthorizationError):
            require_service_capability(identities[2], ServiceCapability.BACKUP_READ)
        with self.assertRaises(AuthorizationError):
            validate_service_identity_separation(
                (
                    ServiceIdentity("same", ServiceIdentityKind.RUNTIME),
                    ServiceIdentity("same", ServiceIdentityKind.MIGRATOR),
                    ServiceIdentity("svc-worker", ServiceIdentityKind.WORKER),
                    ServiceIdentity("svc-backup", ServiceIdentityKind.BACKUP),
                )
            )

    def test_secret_credential_canary_leak_is_zero_in_product_event_and_telemetry(self) -> None:
        canary = "SECRET_CANARY_W006_T002"
        event = sanitize_event_payload(
            {
                "status": "running",
                "nested": {
                    "authorization": f"Bearer {canary}",
                    "cookie": f"session={canary}",
                    "safe": f"prefix-{canary}",
                },
            },
            secret_values=(canary,),
        )
        telemetry = sanitize_telemetry_attributes(
            {
                "trace_id": "trace-1",
                "status": f"error:{canary}",
                "authorization": f"Bearer {canary}",
                "unexpected_raw_payload": {"secret": canary},
            },
            secret_values=(canary,),
        )
        serialized = json.dumps({"event": event, "telemetry": telemetry}, sort_keys=True)
        self.assertNotIn(canary, serialized)
        self.assertNotIn("authorization", serialized.lower())
        self.assertNotIn("cookie", serialized.lower())
        self.assertTrue(telemetry["redacted"])


if __name__ == "__main__":
    unittest.main()
