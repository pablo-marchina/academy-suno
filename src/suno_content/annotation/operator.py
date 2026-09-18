"""Blind, local W004 primary-annotation operator."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OPERATOR_VERSION = "w004-annotation-operator-v001"
SCHEMA_VERSION = "w004-annotation-record-v001"
CORPUS_VERSION = "w004-corpus-v001"
RUBRIC_VERSION = "audience-gold-rubric-v001"
EXPECTED_ITEMS = 36
PRIMARY_ROLES = ("PRIMARY_A", "PRIMARY_B")
LABELS = ("BEGINNER", "INTERMEDIATE", "ADVANCED", "UNSCORABLE")
DIMENSIONS = (
    "D1_JARGON_CONTEXTUALIZATION",
    "D2_BACKGROUND_ASSUMED",
    "D3_CONCEPTUAL_DEPTH",
    "D4_CONTENT_FOCUS",
    "D5_TECHNICITY_PRESERVATION",
)
CHECKS = (
    "FACTUAL_CRITICAL_PRESERVATION",
    "MATERIAL_CONCEPT_PRESERVATION",
    "FORMAT_NATIVE_CONTRACT",
)
CHECK_VALUES = {
    "FACTUAL_CRITICAL_PRESERVATION": {"PASS", "FAIL", "REVIEW_REQUIRED"},
    "MATERIAL_CONCEPT_PRESERVATION": {"PASS", "FAIL", "REVIEW_REQUIRED"},
    "FORMAT_NATIVE_CONTRACT": {"PASS", "FAIL", "NOT_APPLICABLE", "REVIEW_REQUIRED"},
}
FORBIDDEN = {
    "generation_target_level",
    "human_gold_level",
    "evaluator_predicted_level",
    "evaluator_scores",
    "generation_model_id",
    "generation_method",
    "prompt_version",
    "expected_label",
    "other_annotator_labels",
}
ALLOWED_RECORD_KEYS = {
    "annotation_schema_version",
    "corpus_version",
    "annotation_id",
    "item_id",
    "annotator_id",
    "annotation_role",
    "rubric_version",
    "audience_label",
    "audience_dimensions",
    "mixed_level_flag",
    "unscorable_reason",
    "non_compensatory_checks",
    "confidence",
    "notes",
}
REQUIRED_RECORD_KEYS = ALLOWED_RECORD_KEYS - {"unscorable_reason"}

BANK = Path("data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64")
SCHEMA = Path("data/evals/w004/annotation_schema_v001.json")
PLAN = Path("data/evals/w004/annotation_plan_v001.json")
RUBRIC = Path("data/evals/gold/rubric_v001.json")


class OperatorError(ValueError):
    pass


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _pairs(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key), child
            yield from _pairs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _pairs(child)


def _item_id(item: dict[str, Any]) -> str:
    value = item.get("item_id", item.get("blind_item_id"))
    if not isinstance(value, str) or not value:
        raise OperatorError("blind item has no opaque item id")
    return value


def validate_contract(root: Path) -> None:
    schema = _json(root / SCHEMA)
    plan = _json(root / PLAN)
    rubric = _json(root / RUBRIC)
    const = schema.get("properties", {}).get("annotation_schema_version", {}).get("const")
    if const != SCHEMA_VERSION:
        raise OperatorError("annotation schema version drift")
    schema_forbidden = set(schema.get("x_blinding", {}).get("forbidden_annotator_input_fields", []))
    if schema_forbidden != FORBIDDEN:
        raise OperatorError("forbidden-field contract drift")
    if plan.get("corpus_version") != CORPUS_VERSION:
        raise OperatorError("corpus version drift")
    if plan.get("development_item_count") != EXPECTED_ITEMS:
        raise OperatorError("development item count drift")
    flags = plan.get("blinding", {})
    required_false = (
        "show_generation_target",
        "show_evaluator_output",
        "show_generator_identity_or_prompt",
        "show_peer_annotation_before_primary_submission",
        "show_held_out_items",
    )
    if any(flags.get(key) is not False for key in required_false):
        raise OperatorError("annotation plan no longer satisfies blinding")
    if plan.get("threshold_policy", {}).get("freeze_allowed") is not False:
        raise OperatorError("threshold freeze must remain disabled")
    if rubric.get("rubric_version") != RUBRIC_VERSION:
        raise OperatorError("rubric version drift")


def load_blind_bank(root: Path) -> tuple[list[dict[str, Any]], str]:
    validate_contract(root)
    raw = (root / BANK).read_bytes()
    try:
        decoded = gzip.decompress(base64.b64decode(b"".join(raw.split()), validate=True))
    except Exception as exc:
        raise OperatorError(f"cannot decode blind bank: {exc}") from exc

    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line_no, raw_line in enumerate(decoded.decode("utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        item = json.loads(raw_line)
        if not isinstance(item, dict):
            raise OperatorError(f"blind bank line {line_no} is not an object")
        item_id = _item_id(item)
        if item_id in seen:
            raise OperatorError(f"duplicate blind item: {item_id}")
        seen.add(item_id)
        for key, value in _pairs(item):
            if key in FORBIDDEN:
                raise OperatorError(f"blind item {item_id} leaks forbidden field {key}")
            if key in {"split", "source_split"} and isinstance(value, str) and value.upper() == "HELD_OUT":
                raise OperatorError(f"blind item {item_id} exposes HELD_OUT material")
        items.append(item)
    if len(items) != EXPECTED_ITEMS:
        raise OperatorError(f"blind bank must contain exactly {EXPECTED_ITEMS} items")
    return items, _sha256(decoded)


def create_session(root: Path, path: Path, role: str, annotator_id: str) -> dict[str, Any]:
    if path.exists():
        raise OperatorError(f"session already exists: {path}")
    if role not in PRIMARY_ROLES:
        raise OperatorError("only PRIMARY_A and PRIMARY_B are supported")
    if not annotator_id.strip():
        raise OperatorError("annotator_id must be a non-empty pseudonym")
    items, bank_hash = load_blind_bank(root)
    session = {
        "operator_version": OPERATOR_VERSION,
        "session_id": f"{role.lower()}-{secrets.token_hex(6)}",
        "annotation_role": role,
        "annotator_id": annotator_id.strip(),
        "annotation_schema_version": SCHEMA_VERSION,
        "corpus_version": CORPUS_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "blind_bank_decoded_sha256": bank_hash,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "item_ids": [_item_id(item) for item in items],
        "records": [],
    }
    _write(path, session)
    return session


def validate_record(record: dict[str, Any], session: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise OperatorError("annotation record must be an object")
    extra = set(record) - ALLOWED_RECORD_KEYS
    missing = REQUIRED_RECORD_KEYS - set(record)
    if extra:
        raise OperatorError(f"annotation record has schema-forbidden keys: {sorted(extra)}")
    if missing:
        raise OperatorError(f"annotation record missing keys: {sorted(missing)}")
    if record.get("annotation_schema_version") != SCHEMA_VERSION:
        raise OperatorError("annotation schema version mismatch")
    if record.get("corpus_version") != CORPUS_VERSION:
        raise OperatorError("corpus version mismatch")
    if record.get("rubric_version") != RUBRIC_VERSION:
        raise OperatorError("rubric version mismatch")
    if record.get("annotation_role") != session["annotation_role"]:
        raise OperatorError(f"record role must remain {session['annotation_role']}")
    if record.get("annotator_id") != session["annotator_id"]:
        raise OperatorError("annotator_id must match session pseudonym")
    if record.get("item_id") not in set(session["item_ids"]):
        raise OperatorError("record references an unknown/non-development item")
    if not isinstance(record.get("annotation_id"), str) or not record["annotation_id"]:
        raise OperatorError("annotation_id must be non-empty")
    if record.get("audience_label") not in LABELS:
        raise OperatorError("invalid audience_label")
    dims = record.get("audience_dimensions")
    if not isinstance(dims, dict) or set(dims) != set(DIMENSIONS):
        raise OperatorError("audience_dimensions must contain exactly D1-D5")
    if any(type(dims[key]) is not int or not 0 <= dims[key] <= 2 for key in DIMENSIONS):
        raise OperatorError("audience dimension values must be integer 0..2")
    if type(record.get("mixed_level_flag")) is not bool:
        raise OperatorError("mixed_level_flag must be boolean")
    checks = record.get("non_compensatory_checks")
    if not isinstance(checks, dict) or set(checks) != set(CHECKS):
        raise OperatorError("non_compensatory_checks must contain exactly three checks")
    for key in CHECKS:
        if checks[key] not in CHECK_VALUES[key]:
            raise OperatorError(f"invalid non-compensatory value for {key}")
    if record.get("confidence") not in {"LOW", "MEDIUM", "HIGH"}:
        raise OperatorError("invalid confidence")
    if not isinstance(record.get("notes"), str):
        raise OperatorError("notes must be a string")
    reason = record.get("unscorable_reason")
    if record["audience_label"] == "UNSCORABLE" and (not isinstance(reason, str) or not reason.strip()):
        raise OperatorError("UNSCORABLE requires unscorable_reason")
    if record["audience_label"] != "UNSCORABLE" and reason is not None and not isinstance(reason, str):
        raise OperatorError("unscorable_reason must be string or null")


def validate_session_records(session: dict[str, Any], complete: bool = False) -> list[dict[str, Any]]:
    by_item: dict[str, dict[str, Any]] = {}
    annotation_ids: set[str] = set()
    for record in session["records"]:
        validate_record(record, session)
        item_id = record["item_id"]
        if item_id in by_item:
            raise OperatorError(f"duplicate annotation for {item_id}")
        if record["annotation_id"] in annotation_ids:
            raise OperatorError("duplicate annotation_id")
        by_item[item_id] = record
        annotation_ids.add(record["annotation_id"])
    if complete and set(by_item) != set(session["item_ids"]):
        raise OperatorError(f"primary stream incomplete: {len(by_item)}/{len(session['item_ids'])}")
    return [by_item[item_id] for item_id in session["item_ids"] if item_id in by_item]


def load_session(root: Path, path: Path) -> dict[str, Any]:
    session = _json(path)
    items, bank_hash = load_blind_bank(root)
    expected_ids = [_item_id(item) for item in items]
    expected = {
        "operator_version": OPERATOR_VERSION,
        "annotation_schema_version": SCHEMA_VERSION,
        "corpus_version": CORPUS_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "blind_bank_decoded_sha256": bank_hash,
    }
    if not isinstance(session, dict):
        raise OperatorError("session must be an object")
    for key, value in expected.items():
        if session.get(key) != value:
            raise OperatorError(f"session {key} mismatch")
    if session.get("annotation_role") not in PRIMARY_ROLES:
        raise OperatorError("invalid primary role")
    if session.get("item_ids") != expected_ids:
        raise OperatorError("session item population/order drift")
    if not isinstance(session.get("annotator_id"), str) or not session["annotator_id"]:
        raise OperatorError("invalid session annotator_id")
    if not isinstance(session.get("records"), list):
        raise OperatorError("session records must be a list")
    validate_session_records(session)
    return session


def status(session: dict[str, Any]) -> dict[str, Any]:
    records = validate_session_records(session)
    done = {record["item_id"] for record in records}
    remaining = [item for item in session["item_ids"] if item not in done]
    return {
        "session_id": session["session_id"],
        "annotation_role": session["annotation_role"],
        "annotator_id": session["annotator_id"],
        "completed": len(done),
        "total": len(session["item_ids"]),
        "complete": not remaining,
        "next_item_id": remaining[0] if remaining else None,
        "remaining_item_ids": remaining,
    }


def get_blind_item(root: Path, session: dict[str, Any], item_id: str | None = None) -> dict[str, Any]:
    items, _ = load_blind_bank(root)
    by_id = {_item_id(item): item for item in items}
    chosen = item_id or status(session)["next_item_id"]
    if chosen is None:
        raise OperatorError("session is already complete")
    if chosen not in by_id or chosen not in session["item_ids"]:
        raise OperatorError("unknown blind item")
    return by_id[chosen]


def make_record(
    session: dict[str, Any],
    item_id: str,
    *,
    audience_label: str,
    dimensions: dict[str, int],
    mixed_level_flag: bool,
    checks: dict[str, str],
    confidence: str,
    notes: str,
    unscorable_reason: str | None = None,
) -> dict[str, Any]:
    digest = hashlib.sha256(f"{session['session_id']}|{item_id}".encode()).hexdigest()[:20]
    record = {
        "annotation_schema_version": SCHEMA_VERSION,
        "corpus_version": CORPUS_VERSION,
        "annotation_id": f"ann-{digest}",
        "item_id": item_id,
        "annotator_id": session["annotator_id"],
        "annotation_role": session["annotation_role"],
        "rubric_version": RUBRIC_VERSION,
        "audience_label": audience_label,
        "audience_dimensions": dimensions,
        "mixed_level_flag": mixed_level_flag,
        "unscorable_reason": unscorable_reason,
        "non_compensatory_checks": checks,
        "confidence": confidence,
        "notes": notes,
    }
    validate_record(record, session)
    return record


def submit_record(root: Path, path: Path, record: dict[str, Any]) -> dict[str, Any]:
    session = load_session(root, path)
    if record.get("item_id") in {row["item_id"] for row in session["records"]}:
        raise OperatorError("item already annotated")
    validate_record(record, session)
    session["records"].append(record)
    _write(path, session)
    return status(session)


def import_jsonl(root: Path, session_path: Path, input_path: Path) -> dict[str, Any]:
    session = load_session(root, session_path)
    if session["records"]:
        raise OperatorError("import requires an empty session; streams are never merged")
    records: list[dict[str, Any]] = []
    for line_no, raw in enumerate(input_path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise OperatorError(f"{input_path}:{line_no} is not an object")
        records.append(value)
    session["records"] = records
    validate_session_records(session, complete=True)
    _write(session_path, session)
    return status(session)


def export_jsonl(root: Path, session_path: Path, output_path: Path) -> tuple[Path, Path]:
    session = load_session(root, session_path)
    records = validate_session_records(session, complete=True)
    payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")
    provenance_path = output_path.with_suffix(output_path.suffix + ".provenance.json")
    _write(
        provenance_path,
        {
            "operator_version": OPERATOR_VERSION,
            "session_id": session["session_id"],
            "annotation_role": session["annotation_role"],
            "annotator_id": session["annotator_id"],
            "corpus_version": CORPUS_VERSION,
            "annotation_schema_version": SCHEMA_VERSION,
            "rubric_version": RUBRIC_VERSION,
            "blind_bank_decoded_sha256": session["blind_bank_decoded_sha256"],
            "item_count": len(records),
            "complete_primary_stream": True,
            "export_jsonl_sha256": _sha256(payload.encode("utf-8")),
            "independence_note": (
                "One primary stream only. Preserve separate A/B sessions and freeze both "
                "exports before cross-annotator review."
            ),
        },
    )
    return output_path, provenance_path


def _choice(prompt: str, choices) -> str:
    choices = tuple(choices)
    while True:
        value = input(f"{prompt} [{'/'.join(choices)}]\n> ").strip().upper()
        if value in choices:
            return value
        print("Invalid choice; no default is selected.")


def _dim(prompt: str) -> int:
    while True:
        value = input(f"{prompt} [0/1/2]\n> ").strip()
        if value in {"0", "1", "2"}:
            return int(value)
        print("Enter 0, 1, or 2; no value is inferred.")


def interactive_record(root: Path, session: dict[str, Any], item_id: str | None = None) -> dict[str, Any]:
    item = get_blind_item(root, session, item_id)
    chosen = _item_id(item)
    print(json.dumps(item, indent=2, ensure_ascii=False))
    dimensions = {key: _dim(key) for key in DIMENSIONS}
    label = _choice("Global audience label", LABELS)
    mixed = _choice("Materially mixed audience level?", ("YES", "NO")) == "YES"
    checks = {key: _choice(key, sorted(CHECK_VALUES[key])) for key in CHECKS}
    confidence = _choice("Confidence", ("LOW", "MEDIUM", "HIGH"))
    reason = None
    if label == "UNSCORABLE":
        while not reason:
            reason = input("Why is this item UNSCORABLE?\n> ").strip()
    notes = input("Notes (may be empty)\n> ")
    return make_record(
        session,
        chosen,
        audience_label=label,
        dimensions=dimensions,
        mixed_level_flag=mixed,
        checks=checks,
        confidence=confidence,
        notes=notes,
        unscorable_reason=reason,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="W004 blind primary annotation operator")
    parser.add_argument("--repo-root", default=".", type=lambda p: Path(p).expanduser().resolve())
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate")
    p = sub.add_parser("init")
    p.add_argument("--session", required=True, type=Path)
    p.add_argument("--role", required=True, choices=PRIMARY_ROLES)
    p.add_argument("--annotator-id", required=True)

    for name in ("status", "show", "annotate"):
        p = sub.add_parser(name)
        p.add_argument("--session", required=True, type=Path)
        if name in {"show", "annotate"}:
            p.add_argument("--item-id")

    p = sub.add_parser("submit")
    p.add_argument("--session", required=True, type=Path)
    p.add_argument("--record", required=True, type=Path)

    p = sub.add_parser("import")
    p.add_argument("--session", required=True, type=Path)
    p.add_argument("--input", required=True, type=Path)

    p = sub.add_parser("export")
    p.add_argument("--session", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.repo_root
    try:
        if args.command == "validate":
            items, bank_hash = load_blind_bank(root)
            print(json.dumps({"status": "PASS", "item_count": len(items), "blind_bank_decoded_sha256": bank_hash}, indent=2))
            return 0
        if args.command == "init":
            print(json.dumps(status(create_session(root, args.session, args.role, args.annotator_id)), indent=2))
            return 0

        session = load_session(root, args.session)
        if args.command == "status":
            result = status(session)
        elif args.command == "show":
            result = get_blind_item(root, session, args.item_id)
        elif args.command == "annotate":
            result = submit_record(root, args.session, interactive_record(root, session, args.item_id))
        elif args.command == "submit":
            result = submit_record(root, args.session, _json(args.record))
        elif args.command == "import":
            result = import_jsonl(root, args.session, args.input)
        elif args.command == "export":
            output, provenance = export_jsonl(root, args.session, args.output)
            result = {"status": "PASS", "output": str(output), "provenance": str(provenance)}
        else:
            raise OperatorError("unknown command")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OperatorError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
