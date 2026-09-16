from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Any, Mapping


JsonObject = dict[str, Any]
EVENT_SCHEMA_VERSION = "telemetry.event.v1"
SUMMARY_SCHEMA_VERSION = "telemetry.summary.v1"


class TelemetryEventKind(str, Enum):
    STAGE_STARTED = "stage_started"
    STAGE_COMPLETED = "stage_completed"
    STAGE_FAILED = "stage_failed"
    TRANSPORT_RETRY = "transport_retry"
    QUALITY_REPAIR = "quality_repair"
    RUN_STATE_OBSERVED = "run_state_observed"
    BRANCH_STATE_OBSERVED = "branch_state_observed"


@dataclass(frozen=True, slots=True)
class UsageObservation:
    """Provider-neutral metered usage.

    Quantities are keyed by caller-defined meter ids (for example
    ``input_tokens`` or ``provider_x.cache_read_tokens``). ``complete`` is an
    explicit assertion by the adapter that all billable meters for the call
    were observed. Absent usage must be represented as ``None`` rather than a
    zero-valued observation.
    """

    quantities: Mapping[str, Decimal | int | float | str]
    complete: bool = False
    source: str = "observed"

    def __post_init__(self) -> None:
        normalized: dict[str, Decimal] = {}
        for meter_id, raw_value in self.quantities.items():
            meter = str(meter_id).strip()
            if not meter:
                raise ValueError("usage meter id must not be empty")
            value = Decimal(str(raw_value))
            if value < 0:
                raise ValueError("usage quantities must be >= 0")
            normalized[meter] = value
        object.__setattr__(self, "quantities", normalized)
        if not self.source.strip():
            raise ValueError("usage source must not be empty")

    def to_dict(self) -> JsonObject:
        return {
            "quantities": {key: str(value) for key, value in sorted(self.quantities.items())},
            "complete": self.complete,
            "source": self.source,
        }


@dataclass(frozen=True, slots=True)
class PricingTable:
    """Versioned prices expressed as currency per one meter unit."""

    version: str
    currency: str
    unit_prices: Mapping[str, Decimal | int | float | str]

    def __post_init__(self) -> None:
        if not self.version.strip():
            raise ValueError("pricing version must not be empty")
        if not self.currency.strip():
            raise ValueError("pricing currency must not be empty")
        normalized: dict[str, Decimal] = {}
        for meter_id, raw_value in self.unit_prices.items():
            meter = str(meter_id).strip()
            if not meter:
                raise ValueError("pricing meter id must not be empty")
            value = Decimal(str(raw_value))
            if value < 0:
                raise ValueError("unit prices must be >= 0")
            normalized[meter] = value
        object.__setattr__(self, "unit_prices", normalized)

    def price(self, usage: UsageObservation | None) -> "CostObservation | None":
        if usage is None or not usage.complete:
            return None
        if any(meter not in self.unit_prices for meter in usage.quantities):
            return None
        amount = sum(
            (quantity * self.unit_prices[meter] for meter, quantity in usage.quantities.items()),
            Decimal("0"),
        )
        return CostObservation(
            amount=amount,
            currency=self.currency,
            pricing_version=self.version,
        )


@dataclass(frozen=True, slots=True)
class CostObservation:
    amount: Decimal
    currency: str
    pricing_version: str

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("cost amount must be >= 0")
        if not self.currency.strip():
            raise ValueError("cost currency must not be empty")
        if not self.pricing_version.strip():
            raise ValueError("pricing_version must not be empty")

    def to_dict(self) -> JsonObject:
        return {
            "amount": str(self.amount),
            "currency": self.currency,
            "pricing_version": self.pricing_version,
        }


@dataclass(frozen=True, slots=True)
class TelemetryEvent:
    event_id: str
    sequence: int
    run_id: str
    kind: TelemetryEventKind
    observed_at: str
    monotonic_ns: int
    stage: str | None = None
    job_id: str | None = None
    operation_attempt: int | None = None
    parent_event_id: str | None = None
    duration_ns: int | None = None
    usage: UsageObservation | None = None
    cost: CostObservation | None = None
    details: JsonObject = field(default_factory=dict)
    schema_version: str = EVENT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.event_id.strip() or not self.run_id.strip():
            raise ValueError("event_id and run_id must not be empty")
        if self.sequence < 1:
            raise ValueError("event sequence must be >= 1")
        if self.monotonic_ns < 0:
            raise ValueError("monotonic_ns must be >= 0")
        if self.duration_ns is not None and self.duration_ns < 0:
            raise ValueError("duration_ns must be >= 0")
        if self.operation_attempt is not None and self.operation_attempt < 1:
            raise ValueError("operation_attempt must be >= 1")

    def to_dict(self) -> JsonObject:
        return {
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "sequence": self.sequence,
            "run_id": self.run_id,
            "kind": self.kind.value,
            "observed_at": self.observed_at,
            "monotonic_ns": self.monotonic_ns,
            "stage": self.stage,
            "job_id": self.job_id,
            "operation_attempt": self.operation_attempt,
            "parent_event_id": self.parent_event_id,
            "duration_ns": self.duration_ns,
            "usage": None if self.usage is None else self.usage.to_dict(),
            "cost": None if self.cost is None else self.cost.to_dict(),
            "details": _json_safe(self.details),
        }


def _json_safe(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)
