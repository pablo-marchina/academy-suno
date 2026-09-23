from __future__ import annotations

import hashlib
import json
import secrets
import time
import urllib.request
from collections.abc import Iterator, Mapping, MutableMapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Protocol


_SCOPE_NAME = "academy-suno.reference-observability"
_HIGH_CARDINALITY_METRIC_LABELS = frozenset(
    {
        "org_id",
        "workspace_id",
        "tenant_id",
        "user_id",
        "request_id",
        "source_id",
        "run_id",
        "job_id",
        "attempt_id",
        "trace_id",
        "span_id",
    }
)
_ALLOWED_METRIC_LABELS = frozenset(
    {
        "operation",
        "component",
        "outcome",
        "phase",
        "provider",
        "model",
        "audience",
        "output_format",
    }
)
_SAFE_ATTRIBUTE_KEYS = frozenset(
    {
        "component",
        "operation",
        "outcome",
        "phase",
        "provider",
        "model",
        "org_ref",
        "workspace_ref",
        "tenant_ref",
        "request_ref",
        "run_ref",
        "source_ref",
        "source_hash",
        "job_ref",
        "attempt_ref",
        "audience",
        "output_format",
        "evaluation_action",
        "repair_attempt",
        "event_count",
        "last_event_revision",
        "event_type",
        "event_revision",
    }
)
_SAFE_ATTRIBUTE_PREFIXES = ("service.", "deployment.")
_SENSITIVE_EXACT_KEYS = frozenset(
    {
        "authorization",
        "cookie",
        "set-cookie",
        "password",
        "api_key",
        "apikey",
        "access_token",
        "refresh_token",
        "credential",
        "credentials",
        "raw_pdf",
        "raw_bytes",
        "prompt",
        "prompt_text",
        "output",
        "output_text",
        "content",
        "document",
        "document_text",
        "source_text",
        "body",
    }
)
_REDACTED = "[REDACTED]"
_CURRENT_TRACE: ContextVar[TraceContext | None] = ContextVar("academy_suno_trace", default=None)


def _is_zero_hex(value: str) -> bool:
    return bool(value) and set(value) == {"0"}


def correlation_ref(value: str) -> str:
    """Stable one-way correlation reference; raw tenant/run/job ids stay out of telemetry."""

    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:24]}"


def _sensitive_key(key: str) -> bool:
    normalized = key.strip().lower().replace("-", "_")
    if normalized in _SENSITIVE_EXACT_KEYS:
        return True
    if (
        "password" in normalized
        or "credential" in normalized
        or "secret" in normalized
        or "cookie" in normalized
    ):
        return True
    return normalized.endswith("_token") or normalized.endswith("_key")


def _safe_scalar(value: Any) -> str | int | float | bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value
    if value is None:
        return "null"
    text = str(value)
    lowered = text.lower()
    if "bearer " in lowered or "basic " in lowered or "api_key=" in lowered:
        return _REDACTED
    return text[:512]


def sanitize_attributes(attributes: Mapping[str, Any] | None) -> dict[str, str | int | float | bool]:
    cleaned: dict[str, str | int | float | bool] = {}
    for raw_key, raw_value in (attributes or {}).items():
        key = str(raw_key)[:128]
        if _sensitive_key(key):
            cleaned[key] = _REDACTED
            continue
        if key not in _SAFE_ATTRIBUTE_KEYS and not key.startswith(_SAFE_ATTRIBUTE_PREFIXES):
            cleaned[key] = _REDACTED
            continue
        cleaned[key] = _safe_scalar(raw_value)
    return cleaned


def bounded_metric_labels(labels: Mapping[str, Any] | None) -> dict[str, str | int | float | bool]:
    cleaned: dict[str, str | int | float | bool] = {}
    for raw_key, raw_value in (labels or {}).items():
        key = str(raw_key).strip().lower()
        if key in _HIGH_CARDINALITY_METRIC_LABELS or key not in _ALLOWED_METRIC_LABELS:
            continue
        cleaned[key] = _safe_scalar(raw_value)
    return cleaned


@dataclass(frozen=True, slots=True)
class TraceContext:
    trace_id: str
    span_id: str
    trace_flags: str = "01"
    tracestate: str | None = None

    @classmethod
    def root(cls, *, sampled: bool = True) -> "TraceContext":
        return cls(
            trace_id=secrets.token_hex(16),
            span_id=secrets.token_hex(8),
            trace_flags="01" if sampled else "00",
        )

    @classmethod
    def parse(cls, traceparent: str, tracestate: str | None = None) -> "TraceContext":
        parts = traceparent.strip().lower().split("-")
        if len(parts) != 4:
            raise ValueError("invalid traceparent field count")
        version, trace_id, span_id, flags = parts
        if version == "ff" or len(version) != 2:
            raise ValueError("invalid traceparent version")
        if len(trace_id) != 32 or len(span_id) != 16 or len(flags) != 2:
            raise ValueError("invalid traceparent field width")
        try:
            int(version + trace_id + span_id + flags, 16)
        except ValueError as exc:
            raise ValueError("traceparent contains non-hex characters") from exc
        if _is_zero_hex(trace_id) or _is_zero_hex(span_id):
            raise ValueError("traceparent ids must be non-zero")
        return cls(trace_id=trace_id, span_id=span_id, trace_flags=flags, tracestate=tracestate)

    def child(self) -> "TraceContext":
        return TraceContext(
            trace_id=self.trace_id,
            span_id=secrets.token_hex(8),
            trace_flags=self.trace_flags,
            tracestate=self.tracestate,
        )

    def traceparent(self) -> str:
        return f"00-{self.trace_id}-{self.span_id}-{self.trace_flags}"


@dataclass(frozen=True, slots=True)
class SpanRecord:
    name: str
    context: TraceContext
    parent_span_id: str | None
    start_time_unix_nano: int
    end_time_unix_nano: int
    attributes: Mapping[str, str | int | float | bool]
    status_code: int

    @property
    def duration_ms(self) -> float:
        return (self.end_time_unix_nano - self.start_time_unix_nano) / 1_000_000


@dataclass(frozen=True, slots=True)
class MetricPoint:
    name: str
    value: float
    unit: str
    time_unix_nano: int
    attributes: Mapping[str, str | int | float | bool]


@dataclass(frozen=True, slots=True)
class LogRecord:
    event: str
    severity_text: str
    time_unix_nano: int
    attributes: Mapping[str, str | int | float | bool]


@dataclass(slots=True)
class SpanHandle:
    context: TraceContext
    attributes: dict[str, str | int | float | bool] = field(default_factory=dict)

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes.update(sanitize_attributes({key: value}))


class TelemetryExporter(Protocol):
    def export(self, snapshot: Mapping[str, Any]) -> None: ...


class OtlpHttpJsonExporter:
    """Minimal OTLP/HTTP JSON exporter for traces, metrics, and logs.

    It intentionally has no retry loop: application code treats export as best effort,
    while retry/queue topology remains a Collector/backend decision under the DRG.
    """

    def __init__(
        self,
        endpoint: str,
        *,
        headers: Mapping[str, str] | None = None,
        timeout_seconds: float = 2.0,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.headers = dict(headers or {})
        self.timeout_seconds = timeout_seconds

    @staticmethod
    def _otlp_value(value: str | int | float | bool) -> dict[str, Any]:
        if isinstance(value, bool):
            return {"boolValue": value}
        if isinstance(value, int):
            return {"intValue": str(value)}
        if isinstance(value, float):
            return {"doubleValue": value}
        return {"stringValue": str(value)}

    @classmethod
    def _attributes(cls, values: Mapping[str, Any]) -> list[dict[str, Any]]:
        return [
            {"key": key, "value": cls._otlp_value(value)}
            for key, value in sorted(sanitize_attributes(values).items())
        ]

    @classmethod
    def trace_payload(cls, snapshot: Mapping[str, Any]) -> dict[str, Any]:
        spans = [
            {
                "traceId": item["trace_id"],
                "spanId": item["span_id"],
                **({"parentSpanId": item["parent_span_id"]} if item.get("parent_span_id") else {}),
                "name": item["name"],
                "kind": 1,
                "startTimeUnixNano": str(item["start_time_unix_nano"]),
                "endTimeUnixNano": str(item["end_time_unix_nano"]),
                "attributes": cls._attributes(item.get("attributes", {})),
                "status": {"code": int(item.get("status_code", 0))},
            }
            for item in snapshot.get("spans", [])
        ]
        return {
            "resourceSpans": [
                {
                    "resource": {"attributes": cls._attributes(snapshot.get("resource", {}))},
                    "scopeSpans": [{"scope": {"name": _SCOPE_NAME}, "spans": spans}],
                }
            ]
        }

    @classmethod
    def metric_payload(cls, snapshot: Mapping[str, Any]) -> dict[str, Any]:
        metrics = []
        for item in snapshot.get("metrics", []):
            metrics.append(
                {
                    "name": item["name"],
                    "unit": item.get("unit", "1"),
                    "gauge": {
                        "dataPoints": [
                            {
                                "attributes": cls._attributes(item.get("attributes", {})),
                                "timeUnixNano": str(item["time_unix_nano"]),
                                "asDouble": float(item["value"]),
                            }
                        ]
                    },
                }
            )
        return {
            "resourceMetrics": [
                {
                    "resource": {"attributes": cls._attributes(snapshot.get("resource", {}))},
                    "scopeMetrics": [{"scope": {"name": _SCOPE_NAME}, "metrics": metrics}],
                }
            ]
        }

    @classmethod
    def log_payload(cls, snapshot: Mapping[str, Any]) -> dict[str, Any]:
        records = [
            {
                "timeUnixNano": str(item["time_unix_nano"]),
                "severityText": item["severity_text"],
                "body": {"stringValue": item["event"]},
                "attributes": cls._attributes(item.get("attributes", {})),
            }
            for item in snapshot.get("logs", [])
        ]
        return {
            "resourceLogs": [
                {
                    "resource": {"attributes": cls._attributes(snapshot.get("resource", {}))},
                    "scopeLogs": [{"scope": {"name": _SCOPE_NAME}, "logRecords": records}],
                }
            ]
        }

    def _post(self, path: str, payload: Mapping[str, Any]) -> None:
        data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        headers = {"Content-Type": "application/json", **self.headers}
        request = urllib.request.Request(
            f"{self.endpoint}{path}",
            data=data,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            body = response.read(4 * 1024 * 1024 + 1)
            if len(body) > 4 * 1024 * 1024:
                raise RuntimeError("OTLP response exceeded 4 MiB safety limit")

    def export(self, snapshot: Mapping[str, Any]) -> None:
        if snapshot.get("spans"):
            self._post("/v1/traces", self.trace_payload(snapshot))
        if snapshot.get("metrics"):
            self._post("/v1/metrics", self.metric_payload(snapshot))
        if snapshot.get("logs"):
            self._post("/v1/logs", self.log_payload(snapshot))


class TelemetryRecorder:
    """OTel-shaped reference recorder with fail-closed privacy and bounded metrics."""

    def __init__(
        self,
        *,
        service_name: str = "academy-suno-reference",
        exporter: TelemetryExporter | None = None,
        sampled: bool = True,
    ) -> None:
        self.service_name = service_name
        self.exporter = exporter
        self.sampled = sampled
        self.spans: list[SpanRecord] = []
        self.metrics: list[MetricPoint] = []
        self.logs: list[LogRecord] = []
        self.export_failures: list[str] = []
        self._exported_span_count = 0
        self._exported_metric_count = 0
        self._exported_log_count = 0

    @property
    def resource(self) -> dict[str, str]:
        return {
            "service.name": self.service_name,
            "service.namespace": "academy-suno",
            "deployment.environment.name": "reference-non-production",
        }

    @staticmethod
    def extract(headers: Mapping[str, str] | None) -> TraceContext | None:
        lowered = {str(key).lower(): str(value) for key, value in (headers or {}).items()}
        traceparent = lowered.get("traceparent")
        if not traceparent:
            return None
        try:
            return TraceContext.parse(traceparent, lowered.get("tracestate"))
        except ValueError:
            return None

    @staticmethod
    def inject(context: TraceContext, headers: MutableMapping[str, str]) -> None:
        headers["traceparent"] = context.traceparent()
        if context.tracestate:
            headers["tracestate"] = context.tracestate

    @contextmanager
    def span(
        self,
        name: str,
        *,
        attributes: Mapping[str, Any] | None = None,
        parent: TraceContext | None = None,
    ) -> Iterator[SpanHandle]:
        current_parent = parent or _CURRENT_TRACE.get()
        context = current_parent.child() if current_parent else TraceContext.root(sampled=self.sampled)
        parent_span_id = current_parent.span_id if current_parent else None
        handle = SpanHandle(context=context, attributes=sanitize_attributes(attributes))
        token = _CURRENT_TRACE.set(context)
        started = time.time_ns()
        perf_started = time.perf_counter_ns()
        status_code = 0
        outcome = "ok"
        try:
            yield handle
            status_code = 1
        except Exception:
            status_code = 2
            outcome = "error"
            raise
        finally:
            elapsed_ns = time.perf_counter_ns() - perf_started
            ended = started + max(1, elapsed_ns)
            self.spans.append(
                SpanRecord(
                    name=name,
                    context=context,
                    parent_span_id=parent_span_id,
                    start_time_unix_nano=started,
                    end_time_unix_nano=ended,
                    attributes=dict(handle.attributes),
                    status_code=status_code,
                )
            )
            self.record_metric(
                "operation.duration",
                elapsed_ns / 1_000_000,
                unit="ms",
                labels={
                    "operation": name,
                    "component": handle.attributes.get("component", "application"),
                    "outcome": outcome,
                },
            )
            _CURRENT_TRACE.reset(token)

    def record_metric(
        self,
        name: str,
        value: float,
        *,
        unit: str = "1",
        labels: Mapping[str, Any] | None = None,
    ) -> None:
        self.metrics.append(
            MetricPoint(
                name=name,
                value=float(value),
                unit=unit,
                time_unix_nano=time.time_ns(),
                attributes=bounded_metric_labels(labels),
            )
        )

    def log(
        self,
        event: str,
        *,
        severity_text: str = "INFO",
        attributes: Mapping[str, Any] | None = None,
    ) -> None:
        self.logs.append(
            LogRecord(
                event=str(event)[:128],
                severity_text=str(severity_text)[:16],
                time_unix_nano=time.time_ns(),
                attributes=sanitize_attributes(attributes),
            )
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "resource": self.resource,
            "spans": [
                {
                    "name": span.name,
                    "trace_id": span.context.trace_id,
                    "span_id": span.context.span_id,
                    "parent_span_id": span.parent_span_id,
                    "start_time_unix_nano": span.start_time_unix_nano,
                    "end_time_unix_nano": span.end_time_unix_nano,
                    "duration_ms": span.duration_ms,
                    "status_code": span.status_code,
                    "attributes": dict(span.attributes),
                }
                for span in self.spans
            ],
            "metrics": [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "time_unix_nano": metric.time_unix_nano,
                    "attributes": dict(metric.attributes),
                }
                for metric in self.metrics
            ],
            "logs": [
                {
                    "event": record.event,
                    "severity_text": record.severity_text,
                    "time_unix_nano": record.time_unix_nano,
                    "attributes": dict(record.attributes),
                }
                for record in self.logs
            ],
            "export_failures": list(self.export_failures),
        }

    def _pending_snapshot(self) -> dict[str, Any]:
        snapshot = self.snapshot()
        snapshot["spans"] = snapshot["spans"][self._exported_span_count :]
        snapshot["metrics"] = snapshot["metrics"][self._exported_metric_count :]
        snapshot["logs"] = snapshot["logs"][self._exported_log_count :]
        return snapshot

    def export_best_effort(self) -> bool:
        if self.exporter is None:
            return True
        snapshot = self._pending_snapshot()
        if not snapshot["spans"] and not snapshot["metrics"] and not snapshot["logs"]:
            return True
        try:
            self.exporter.export(snapshot)
            self._exported_span_count = len(self.spans)
            self._exported_metric_count = len(self.metrics)
            self._exported_log_count = len(self.logs)
            return True
        except Exception as exc:
            self.export_failures.append(f"{type(exc).__name__}:{exc}")
            return False

    def duration_quantiles(self) -> dict[str, float | None]:
        values = sorted(metric.value for metric in self.metrics if metric.name == "operation.duration")
        if not values:
            return {"p50_ms": None, "p95_ms": None, "p99_ms": None}

        def nearest_rank(percentile: float) -> float:
            index = max(0, min(len(values) - 1, int((percentile * len(values) + 0.999999) - 1)))
            return values[index]

        return {
            "p50_ms": nearest_rank(0.50),
            "p95_ms": nearest_rank(0.95),
            "p99_ms": nearest_rank(0.99),
        }


@dataclass(frozen=True, slots=True)
class TraceScope:
    org_id: str
    workspace_id: str
    run_id: str


class OpaqueTraceLinkRegistry:
    """Reference-only server-side trace reference registry with scoped authorization."""

    def __init__(self) -> None:
        self._records: dict[str, tuple[TraceScope, str]] = {}

    def issue(self, scope: TraceScope, trace_id: str) -> str:
        reference = secrets.token_urlsafe(24)
        self._records[reference] = (scope, trace_id)
        return reference

    @staticmethod
    def href(reference: str) -> str:
        return f"/api/v1/observability/traces/{reference}"

    def resolve(self, reference: str, scope: TraceScope) -> str:
        stored = self._records.get(reference)
        if stored is None:
            raise PermissionError("unknown trace reference")
        stored_scope, trace_id = stored
        if stored_scope != scope:
            raise PermissionError("trace reference is not authorized for this scope")
        return trace_id
