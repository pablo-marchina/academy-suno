from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping, Sequence


class SecurityError(PermissionError):
    """Base class for fail-closed security decisions."""


class AuthenticationError(SecurityError):
    pass


class AuthorizationError(SecurityError):
    pass


class TenantIsolationError(AuthorizationError):
    pass


class ReplayDenied(AuthorizationError):
    pass


class CredentialTopologyError(AuthenticationError):
    pass


class Role(str, Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    OWNER = "owner"


class AccessSurface(str, Enum):
    API = "api"
    DATA = "data"
    OBJECT = "object"
    EVENT = "event"
    TRACE = "trace"


class Action(str, Enum):
    API_READ = "api.read"
    API_WRITE = "api.write"
    DATA_READ = "data.read"
    DATA_WRITE = "data.write"
    OBJECT_READ = "object.read"
    OBJECT_WRITE = "object.write"
    EVENT_CONNECT = "event.connect"
    EVENT_RESUME = "event.resume"
    TRACE_READ = "trace.read"


ACTION_SURFACE: dict[Action, AccessSurface] = {
    Action.API_READ: AccessSurface.API,
    Action.API_WRITE: AccessSurface.API,
    Action.DATA_READ: AccessSurface.DATA,
    Action.DATA_WRITE: AccessSurface.DATA,
    Action.OBJECT_READ: AccessSurface.OBJECT,
    Action.OBJECT_WRITE: AccessSurface.OBJECT,
    Action.EVENT_CONNECT: AccessSurface.EVENT,
    Action.EVENT_RESUME: AccessSurface.EVENT,
    Action.TRACE_READ: AccessSurface.TRACE,
}

ROLE_PERMISSIONS: dict[Role, frozenset[Action]] = {
    Role.VIEWER: frozenset(
        {
            Action.API_READ,
            Action.DATA_READ,
            Action.OBJECT_READ,
            Action.EVENT_CONNECT,
            Action.EVENT_RESUME,
            Action.TRACE_READ,
        }
    ),
    Role.EDITOR: frozenset(
        {
            Action.API_READ,
            Action.API_WRITE,
            Action.DATA_READ,
            Action.DATA_WRITE,
            Action.OBJECT_READ,
            Action.OBJECT_WRITE,
            Action.EVENT_CONNECT,
            Action.EVENT_RESUME,
            Action.TRACE_READ,
        }
    ),
    Role.OWNER: frozenset(Action),
}


@dataclass(frozen=True, slots=True)
class PrincipalBinding:
    issuer: str
    subject: str
    user_id: str
    active: bool = True


@dataclass(frozen=True, slots=True)
class Membership:
    membership_id: str
    user_id: str
    org_id: str
    workspace_id: str
    role: Role
    active: bool = True
    epoch: int = 0


@dataclass(frozen=True, slots=True)
class Session:
    session_id: str
    user_id: str
    org_id: str
    workspace_id: str
    csrf_digest: str
    session_epoch: int = 0
    revoked: bool = False
    expires_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class SecurityContext:
    session_id: str
    session_epoch: int
    membership_id: str
    membership_epoch: int
    user_id: str
    org_id: str
    workspace_id: str
    role: Role


@dataclass(frozen=True, slots=True)
class TenantResource:
    surface: AccessSurface
    org_id: str
    workspace_id: str
    resource_id: str
    provenance_id: str

    def __post_init__(self) -> None:
        for name in ("org_id", "workspace_id", "resource_id", "provenance_id"):
            if not getattr(self, name):
                raise ValueError(f"{name} is required for a protected resource")


@dataclass(frozen=True, slots=True)
class AuthorizedStream:
    org_id: str
    workspace_id: str
    run_id: str

    def __post_init__(self) -> None:
        if not self.org_id or not self.workspace_id or not self.run_id:
            raise ValueError("authorized stream requires org_id, workspace_id, and run_id")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class SecurityDirectory:
    """Server-authoritative principal, membership and session directory.

    External identity claims establish only ``(issuer, subject)``. Organization
    and workspace authority is resolved from app-owned membership state.
    """

    def __init__(self) -> None:
        self._principals: dict[tuple[str, str], PrincipalBinding] = {}
        self._memberships: dict[tuple[str, str, str], Membership] = {}
        self._sessions: dict[str, Session] = {}

    def bind_principal(self, binding: PrincipalBinding) -> None:
        key = (binding.issuer, binding.subject)
        if not binding.issuer or not binding.subject or not binding.user_id:
            raise ValueError("issuer, subject, and user_id are required")
        existing = self._principals.get(key)
        if existing is not None and existing.user_id != binding.user_id:
            raise AuthenticationError("external principal cannot be remapped to a different user")
        self._principals[key] = binding

    def resolve_principal(self, issuer: str, subject: str) -> str:
        binding = self._principals.get((issuer, subject))
        if binding is None or not binding.active:
            raise AuthenticationError("unknown or inactive external principal")
        return binding.user_id

    def put_membership(self, membership: Membership) -> None:
        if not all(
            (
                membership.membership_id,
                membership.user_id,
                membership.org_id,
                membership.workspace_id,
            )
        ):
            raise ValueError("membership identity fields are required")
        key = (membership.user_id, membership.org_id, membership.workspace_id)
        existing = self._memberships.get(key)
        if existing is not None and existing.membership_id != membership.membership_id:
            raise AuthorizationError("membership identity is immutable for a user/workspace binding")
        self._memberships[key] = membership

    def revoke_membership(self, user_id: str, org_id: str, workspace_id: str) -> Membership:
        key = (user_id, org_id, workspace_id)
        membership = self._memberships.get(key)
        if membership is None:
            raise AuthorizationError("membership does not exist")
        revoked = replace(membership, active=False, epoch=membership.epoch + 1)
        self._memberships[key] = revoked
        return revoked

    def create_session(
        self,
        *,
        session_id: str,
        user_id: str,
        org_id: str,
        workspace_id: str,
        csrf_token: str,
        expires_at: datetime | None = None,
    ) -> Session:
        if session_id in self._sessions:
            raise AuthenticationError("session_id already exists")
        if not csrf_token:
            raise ValueError("csrf_token is required")
        membership = self._active_membership(user_id, org_id, workspace_id)
        session = Session(
            session_id=session_id,
            user_id=user_id,
            org_id=membership.org_id,
            workspace_id=membership.workspace_id,
            csrf_digest=_digest(csrf_token),
            expires_at=expires_at,
        )
        self._sessions[session_id] = session
        return session

    def revoke_session(self, session_id: str) -> Session:
        session = self._sessions.get(session_id)
        if session is None:
            raise AuthenticationError("session does not exist")
        revoked = replace(session, revoked=True, session_epoch=session.session_epoch + 1)
        self._sessions[session_id] = revoked
        return revoked

    def switch_workspace(self, session_id: str, *, org_id: str, workspace_id: str) -> Session:
        session = self._active_session(session_id)
        membership = self._active_membership(session.user_id, org_id, workspace_id)
        switched = replace(
            session,
            org_id=membership.org_id,
            workspace_id=membership.workspace_id,
            session_epoch=session.session_epoch + 1,
        )
        self._sessions[session_id] = switched
        return switched

    def resolve_context(
        self,
        session_id: str,
        *,
        now: datetime | None = None,
    ) -> SecurityContext:
        session = self._active_session(session_id, now=now)
        membership = self._active_membership(
            session.user_id,
            session.org_id,
            session.workspace_id,
        )
        return SecurityContext(
            session_id=session.session_id,
            session_epoch=session.session_epoch,
            membership_id=membership.membership_id,
            membership_epoch=membership.epoch,
            user_id=session.user_id,
            org_id=membership.org_id,
            workspace_id=membership.workspace_id,
            role=membership.role,
        )

    def validate_context(
        self,
        context: SecurityContext,
        *,
        now: datetime | None = None,
    ) -> None:
        current = self.resolve_context(context.session_id, now=now)
        if current != context:
            raise AuthenticationError("security context is stale after session or membership change")

    def verify_csrf(self, session_id: str, csrf_token: str) -> None:
        session = self._active_session(session_id)
        if not secrets.compare_digest(session.csrf_digest, _digest(csrf_token)):
            raise CredentialTopologyError("invalid CSRF token")

    def _active_membership(self, user_id: str, org_id: str, workspace_id: str) -> Membership:
        membership = self._memberships.get((user_id, org_id, workspace_id))
        if membership is None or not membership.active:
            raise AuthorizationError("active workspace membership required")
        return membership

    def _active_session(
        self,
        session_id: str,
        *,
        now: datetime | None = None,
    ) -> Session:
        session = self._sessions.get(session_id)
        if session is None or session.revoked:
            raise AuthenticationError("active session required")
        check_time = now or _utc_now()
        if session.expires_at is not None:
            expiry = session.expires_at
            if expiry.tzinfo is None:
                raise AuthenticationError("session expiry must be timezone-aware")
            if check_time >= expiry:
                raise AuthenticationError("session expired")
        return session


class DenyByDefaultAuthorizer:
    def __init__(self, directory: SecurityDirectory) -> None:
        self._directory = directory

    def require(
        self,
        context: SecurityContext,
        resource: TenantResource,
        action: Action,
    ) -> None:
        self._directory.validate_context(context)
        expected_surface = ACTION_SURFACE.get(action)
        if expected_surface is None or expected_surface is not resource.surface:
            raise AuthorizationError("action is not valid for resource surface")
        if resource.org_id != context.org_id or resource.workspace_id != context.workspace_id:
            raise TenantIsolationError("resource tenant does not match authoritative workspace")
        allowed = ROLE_PERMISSIONS.get(context.role, frozenset())
        if action not in allowed:
            raise AuthorizationError("action denied by app-owned authorization policy")

    def require_stream(
        self,
        context: SecurityContext,
        stream: AuthorizedStream,
        action: Action,
    ) -> None:
        if action not in (Action.EVENT_CONNECT, Action.EVENT_RESUME):
            raise AuthorizationError("invalid stream action")
        self._directory.validate_context(context)
        if stream.org_id != context.org_id or stream.workspace_id != context.workspace_id:
            raise TenantIsolationError("stream tenant does not match authoritative workspace")
        allowed = ROLE_PERMISSIONS.get(context.role, frozenset())
        if action not in allowed:
            raise AuthorizationError("stream action denied by app-owned authorization policy")


@dataclass(frozen=True, slots=True)
class BrowserRequestCredential:
    method: str
    session_cookie: str | None
    same_origin: bool
    authorization_header: str | None = None
    csrf_header: str | None = None
    query_params: Mapping[str, str] | None = None
    last_event_id: str | None = None
    is_sse: bool = False


class BrowserCredentialPolicy:
    """Same-origin browser topology: host-only Secure HttpOnly session cookie.

    Credentials in URLs, query strings, Authorization headers, or Last-Event-ID
    are rejected. Mutating API requests additionally require a session-bound
    CSRF header. SSE uses the same cookie and an opaque Last-Event-ID cursor.
    """

    FORBIDDEN_QUERY_KEYS = frozenset(
        {
            "access_token",
            "authorization",
            "api_key",
            "apikey",
            "credential",
            "session",
            "session_id",
            "token",
        }
    )
    MUTATING_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})
    COOKIE_ATTRIBUTES = ("Secure", "HttpOnly", "SameSite=Lax", "Path=/", "HostOnly")

    def __init__(self, directory: SecurityDirectory) -> None:
        self._directory = directory

    def authenticate(self, request: BrowserRequestCredential) -> SecurityContext:
        method = request.method.upper()
        query = request.query_params or {}
        if not request.same_origin:
            raise CredentialTopologyError("browser credential path requires same-origin request")
        if request.authorization_header:
            raise CredentialTopologyError("browser bearer credentials are not accepted")
        if any(key.lower() in self.FORBIDDEN_QUERY_KEYS for key in query):
            raise CredentialTopologyError("credentials are forbidden in browser query parameters")
        if not request.session_cookie:
            raise AuthenticationError("session cookie required")
        if request.is_sse:
            if method != "GET":
                raise CredentialTopologyError("SSE transport must use GET")
        elif method in self.MUTATING_METHODS:
            if not request.csrf_header:
                raise CredentialTopologyError("mutating browser API request requires CSRF header")
            self._directory.verify_csrf(request.session_cookie, request.csrf_header)
        return self._directory.resolve_context(request.session_cookie)


@dataclass(frozen=True, slots=True)
class _CursorRecord:
    stream: AuthorizedStream
    session_id: str
    session_epoch: int
    membership_id: str
    membership_epoch: int
    last_event_revision: int


class ReplayCursorVault:
    """Reference opaque cursor registry; persistence backend remains evidence-gated."""

    def __init__(
        self,
        directory: SecurityDirectory,
        authorizer: DenyByDefaultAuthorizer,
    ) -> None:
        self._directory = directory
        self._authorizer = authorizer
        self._records: dict[str, _CursorRecord] = {}

    def issue(
        self,
        context: SecurityContext,
        stream: AuthorizedStream,
        *,
        last_event_revision: int,
    ) -> str:
        if last_event_revision < 0:
            raise ValueError("last_event_revision must be >= 0")
        self._authorizer.require_stream(context, stream, Action.EVENT_CONNECT)
        token = secrets.token_urlsafe(32)
        self._records[token] = _CursorRecord(
            stream=stream,
            session_id=context.session_id,
            session_epoch=context.session_epoch,
            membership_id=context.membership_id,
            membership_epoch=context.membership_epoch,
            last_event_revision=last_event_revision,
        )
        return token

    def resume(
        self,
        context: SecurityContext,
        stream: AuthorizedStream,
        *,
        cursor_token: str,
    ) -> int:
        self._authorizer.require_stream(context, stream, Action.EVENT_RESUME)
        record = self._records.get(cursor_token)
        if record is None:
            raise ReplayDenied("unknown opaque replay cursor")
        if record.stream != stream:
            raise ReplayDenied("cursor cannot select or cross an authorized stream")
        if (
            record.session_id != context.session_id
            or record.session_epoch != context.session_epoch
            or record.membership_id != context.membership_id
            or record.membership_epoch != context.membership_epoch
        ):
            raise ReplayDenied("cursor invalidated by session or membership change")
        self._directory.validate_context(context)
        return record.last_event_revision


class ServiceIdentityKind(str, Enum):
    RUNTIME = "runtime"
    MIGRATOR = "migrator"
    WORKER = "worker"
    BACKUP = "backup"


class ServiceCapability(str, Enum):
    API_SERVE = "api.serve"
    DATA_READ = "data.read"
    DATA_WRITE = "data.write"
    OBJECT_READ = "object.read"
    OBJECT_WRITE = "object.write"
    JOB_EXECUTE = "job.execute"
    SCHEMA_MIGRATE = "schema.migrate"
    BACKUP_READ = "backup.read"
    RESTORE_WRITE = "restore.write"


SERVICE_CAPABILITIES: dict[ServiceIdentityKind, frozenset[ServiceCapability]] = {
    ServiceIdentityKind.RUNTIME: frozenset(
        {
            ServiceCapability.API_SERVE,
            ServiceCapability.DATA_READ,
            ServiceCapability.DATA_WRITE,
            ServiceCapability.OBJECT_READ,
            ServiceCapability.OBJECT_WRITE,
        }
    ),
    ServiceIdentityKind.MIGRATOR: frozenset({ServiceCapability.SCHEMA_MIGRATE}),
    ServiceIdentityKind.WORKER: frozenset(
        {
            ServiceCapability.JOB_EXECUTE,
            ServiceCapability.DATA_READ,
            ServiceCapability.DATA_WRITE,
            ServiceCapability.OBJECT_READ,
            ServiceCapability.OBJECT_WRITE,
        }
    ),
    ServiceIdentityKind.BACKUP: frozenset(
        {
            ServiceCapability.BACKUP_READ,
            ServiceCapability.RESTORE_WRITE,
        }
    ),
}


@dataclass(frozen=True, slots=True)
class ServiceIdentity:
    identity_id: str
    kind: ServiceIdentityKind


def validate_service_identity_separation(identities: Sequence[ServiceIdentity]) -> None:
    by_kind = {identity.kind: identity for identity in identities}
    if set(by_kind) != set(ServiceIdentityKind):
        raise AuthorizationError("runtime/migrator/worker/backup identities are all required")
    ids = [identity.identity_id for identity in identities]
    if any(not identity_id for identity_id in ids) or len(ids) != len(set(ids)):
        raise AuthorizationError("service identity IDs must be non-empty and distinct")


def require_service_capability(
    identity: ServiceIdentity,
    capability: ServiceCapability,
) -> None:
    if capability not in SERVICE_CAPABILITIES.get(identity.kind, frozenset()):
        raise AuthorizationError(
            f"{identity.kind.value} identity is not allowed capability {capability.value}"
        )


TELEMETRY_ATTRIBUTE_ALLOWLIST = frozenset(
    {
        "request_id",
        "trace_id",
        "run_id",
        "job_id",
        "branch_id",
        "attempt_id",
        "document_id",
        "transition_id",
        "resource_id",
        "event_type",
        "event_schema_version",
        "status",
        "error_class",
        "duration_ms",
        "latency_ms",
        "byte_count",
        "item_count",
        "retry_count",
        "provider_ref",
        "model_ref",
        "evaluator_ref",
        "artifact_id",
        "content_hash",
        "redacted",
    }
)
SENSITIVE_KEY_FRAGMENTS = (
    "authorization",
    "cookie",
    "credential",
    "password",
    "private_key",
    "secret",
    "session",
    "token",
    "api_key",
    "access_key",
)


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower()
    return any(fragment in normalized for fragment in SENSITIVE_KEY_FRAGMENTS)


def _contains_secret(value: object, secret_values: Sequence[str]) -> bool:
    if not isinstance(value, str):
        return False
    return any(secret and secret in value for secret in secret_values)


def sanitize_telemetry_attributes(
    attributes: Mapping[str, object],
    *,
    secret_values: Sequence[str] = (),
) -> dict[str, object]:
    """Default-deny telemetry attributes matching the accepted T001 allowlist."""
    safe: dict[str, object] = {}
    redacted = False
    for key, value in attributes.items():
        if key not in TELEMETRY_ATTRIBUTE_ALLOWLIST or _is_sensitive_key(key):
            redacted = True
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            if _contains_secret(value, secret_values):
                safe[key] = "[REDACTED]"
                redacted = True
            else:
                safe[key] = value
        else:
            redacted = True
    if redacted:
        safe["redacted"] = True
    return safe


def sanitize_event_payload(
    payload: Mapping[str, object],
    *,
    secret_values: Sequence[str] = (),
) -> dict[str, object]:
    """Recursively remove credential-shaped fields and redact known canaries."""

    def clean(value: object) -> object:
        if isinstance(value, Mapping):
            result: dict[str, object] = {}
            for raw_key, child in value.items():
                key = str(raw_key)
                if _is_sensitive_key(key):
                    continue
                result[key] = clean(child)
            return result
        if isinstance(value, list):
            return [clean(item) for item in value]
        if isinstance(value, tuple):
            return [clean(item) for item in value]
        if _contains_secret(value, secret_values):
            return "[REDACTED]"
        return value

    cleaned = clean(payload)
    assert isinstance(cleaned, dict)
    return cleaned
