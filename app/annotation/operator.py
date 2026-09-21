#!/usr/bin/env python3
"""Repository-local entry point for the W004 blind annotation operator."""

from __future__ import annotations

import sys

# When this file is executed directly (``python app/annotation/operator.py``),
# Python prepends ``app/annotation`` to ``sys.path``. Because this file is named
# ``operator.py``, stdlib imports such as ``collections -> operator`` can then
# resolve back to this file and fail during interpreter startup. Remove only
# that direct-script path before importing modules that depend on stdlib
# ``operator``. Module execution (``python -m app.annotation.operator``) remains
# unaffected because its ``sys.path[0]`` is the repository root, not this folder.
if sys.path:
    _script_dir = __file__.replace("\\", "/").rsplit("/", 1)[0].rstrip("/").lower()
    _path0 = sys.path[0].replace("\\", "/").rstrip("/").lower()
    if _path0 == _script_dir:
        sys.path.pop(0)

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from suno_content.annotation.operator import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
