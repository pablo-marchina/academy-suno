from __future__ import annotations

import hashlib
import json
from typing import Any

from pydantic import BaseModel, ConfigDict


class DomainModel(BaseModel):
    """Strict immutable base for persisted domain contracts."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        validate_default=True,
    )

    def canonical_dict(self) -> dict[str, Any]:
        """Return a JSON-safe representation with explicit null version fields preserved."""
        return self.model_dump(mode="json", exclude_none=False)

    def canonical_json(self) -> str:
        """Serialize deterministically for persistence, hashing, and regression fixtures."""
        return json.dumps(
            self.canonical_dict(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    def canonical_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()
