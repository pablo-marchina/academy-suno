from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from .models import TelemetryEvent


class TelemetrySink(Protocol):
    def emit(self, event: TelemetryEvent) -> None: ...


class InMemoryTelemetrySink:
    def __init__(self) -> None:
        self.events: list[TelemetryEvent] = []

    def emit(self, event: TelemetryEvent) -> None:
        self.events.append(event)


class JsonlTelemetrySink:
    """Append-only JSONL sink suitable for audit evidence and later ingestion."""

    def __init__(self, path: str | Path, *, fsync: bool = False) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fsync = fsync

    def emit(self, event: TelemetryEvent) -> None:
        payload = json.dumps(
            event.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(payload)
            handle.write("\n")
            handle.flush()
            if self.fsync:
                import os

                os.fsync(handle.fileno())
