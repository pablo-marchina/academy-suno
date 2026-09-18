from __future__ import annotations

import base64
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from suno_content.annotation.operator import (
    CHECKS,
    CORPUS_VERSION,
    DIMENSIONS,
    EXPECTED_ITEMS,
    OPERATOR_VERSION,
    OperatorError,
    create_session,
    export_jsonl,
    import_jsonl,
    load_blind_bank,
    load_session,
    make_record,
    status,
    submit_record,
)


class OperatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self._contracts()
        self._bank()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_json(self, rel: str, value: object) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def _contracts(self) -> None:
        self._write_json(
            "data/evals/w004/annotation_schema_v001.json",
            {
                "properties": {"annotation_schema_version": {"const": "w004-annotation-record-v001"}},
                "x_blinding": {
                    "forbidden_annotator_input_fields": [
                        "generation_target_level",
                        "human_gold_level",
                        "evaluator_predicted_level",
                        "evaluator_scores",
                        "generation_model_id",
                        "generation_method",
                        "prompt_version",
                        "expected_label",
                        "other_annotator_labels",
                    ]
                },
            },
        )
        self._write_json(
            "data/evals/w004/annotation_plan_v001.json",
            {
                "corpus_version": CORPUS_VERSION,
                "development_item_count": EXPECTED_ITEMS,
                "blinding": {
                    "show_generation_target": False,
                    "show_evaluator_output": False,
                    "show_generator_identity_or_prompt": False,
                    "show_peer_annotation_before_primary_submission": False,
                    "show_held_out_items": False,
                },
                "threshold_policy": {"freeze_allowed": False},
            },
        )
        self._write_json(
            "data/evals/gold/rubric_v001.json",
            {"rubric_version": "audience-gold-rubric-v001"},
        )

    def _items(self):
        return [
            {
                "blind_item_id": f"BI-{i:03d}",
                "split": "DEVELOPMENT",
                "format": "ARTICLE",
                "output_text": f"Blinded output {i}",
                "source_check_context": {"excerpt": f"Evidence {i}"},
            }
            for i in range(1, EXPECTED_ITEMS + 1)
        ]

    def _bank(self, items=None) -> None:
        items = items or self._items()
        decoded = "".join(json.dumps(item) + "\n" for item in items).encode()
        payload = base64.b64encode(gzip.compress(decoded))
        path = self.root / "data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)

    def _record(self, session, item_id):
        return make_record(
            session,
            item_id,
            audience_label="INTERMEDIATE",
            dimensions={key: 1 for key in DIMENSIONS},
            mixed_level_flag=False,
            checks={key: "PASS" for key in CHECKS},
            confidence="HIGH",
            notes="human judgment",
        )

    def test_bank_rejects_forbidden_and_held_out(self):
        items = self._items()
        items[0]["source_check_context"] = {"generation_target_level": "BEGINNER"}
        self._bank(items)
        with self.assertRaisesRegex(OperatorError, "forbidden field"):
            load_blind_bank(self.root)

        items = self._items()
        items[0]["split"] = "HELD_OUT"
        self._bank(items)
        with self.assertRaisesRegex(OperatorError, "HELD_OUT"):
            load_blind_bank(self.root)

    def test_roles_are_separate_and_locked(self):
        a_path = self.root / "a.json"
        b_path = self.root / "b.json"
        a = create_session(self.root, a_path, "PRIMARY_A", "human-a")
        b = create_session(self.root, b_path, "PRIMARY_B", "human-b")
        self.assertEqual(a["operator_version"], OPERATOR_VERSION)
        self.assertNotEqual(a["session_id"], b["session_id"])
        with self.assertRaisesRegex(OperatorError, "record role"):
            submit_record(self.root, b_path, self._record(a, a["item_ids"][0]))

    def test_export_complete_and_role_safe_import(self):
        a_path = self.root / "a.json"
        a = create_session(self.root, a_path, "PRIMARY_A", "human-a")
        submit_record(self.root, a_path, self._record(a, a["item_ids"][0]))
        with self.assertRaisesRegex(OperatorError, "incomplete"):
            export_jsonl(self.root, a_path, self.root / "a.jsonl")

        a = load_session(self.root, a_path)
        for item_id in a["item_ids"][1:]:
            submit_record(self.root, a_path, self._record(a, item_id))
        self.assertTrue(status(load_session(self.root, a_path))["complete"])

        output, provenance = export_jsonl(self.root, a_path, self.root / "a.jsonl")
        self.assertEqual(len(output.read_text().splitlines()), EXPECTED_ITEMS)
        prov = json.loads(provenance.read_text())
        self.assertEqual(prov["annotation_role"], "PRIMARY_A")
        self.assertTrue(prov["complete_primary_stream"])

        a2 = self.root / "a2.json"
        create_session(self.root, a2, "PRIMARY_A", "human-a")
        self.assertTrue(import_jsonl(self.root, a2, output)["complete"])

        b = self.root / "b.json"
        create_session(self.root, b, "PRIMARY_B", "human-b")
        with self.assertRaisesRegex(OperatorError, "record role"):
            import_jsonl(self.root, b, output)

    def test_target_and_peer_fields_are_rejected(self):
        path = self.root / "a.json"
        session = create_session(self.root, path, "PRIMARY_A", "human-a")
        record = self._record(session, session["item_ids"][0])
        record["generation_target_level"] = "INTERMEDIATE"
        with self.assertRaisesRegex(OperatorError, "schema-forbidden"):
            submit_record(self.root, path, record)

        record = self._record(session, session["item_ids"][0])
        record["other_annotator_labels"] = ["BEGINNER"]
        with self.assertRaisesRegex(OperatorError, "schema-forbidden"):
            submit_record(self.root, path, record)


if __name__ == "__main__":
    unittest.main()
