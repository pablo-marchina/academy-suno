from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from .checks import evaluate_case


def read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_no}: JSON object required")
        rows.append(row)
    return rows


def evaluate_corpus(rows: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    return [evaluate_case(row).oracle_row() for row in rows]


def write_jsonl(rows: Iterable[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n"
    path.write_text(payload, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate factual-v001 with deterministic hard anchors")
    parser.add_argument("corpus", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    observed = evaluate_corpus(read_jsonl(args.corpus))
    write_jsonl(observed, args.output)
    print(f"PASS deterministic-factual: {len(observed)} fixtures -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
