from __future__ import annotations

import json
import unittest
from pathlib import Path

from experiments.model_validation_w004.run_blind_model_validation import (
    DIMENSIONS,
    FORBIDDEN_INPUT_KEYS,
    MODEL_FIELDS,
    build_prompt,
    load_blind_bank,
    validate_model_record,
)


ROOT = Path(__file__).resolve().parents[2]


class BlindModelValidationTests(unittest.TestCase):
    def test_frozen_blind_bank_is_complete_and_has_no_forbidden_fields(self):
        items, digest = load_blind_bank(ROOT / "data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64")
        self.assertEqual(len(items), 36)
        self.assertEqual(len(digest), 64)
        encoded = json.dumps(items, ensure_ascii=False)
        for key in FORBIDDEN_INPUT_KEYS:
            self.assertNotIn(f'"{key}"', encoded)

    def test_prompt_uses_only_blind_packets_and_rubric(self):
        items, _ = load_blind_bank(ROOT / "data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64")
        rubric = json.loads((ROOT / "data/evals/gold/rubric_v001.json").read_text(encoding="utf-8"))
        prompt = build_prompt(items[:2], rubric)
        self.assertIn("PACKETS=", prompt)
        self.assertIn(items[0]["blind_item_id"], prompt)
        for key in FORBIDDEN_INPUT_KEYS:
            self.assertNotIn(f'"{key}"', prompt)

    def test_model_record_contract(self):
        item_id = "BI-TEST"
        record = {
            "item_id": item_id,
            "audience_label": "INTERMEDIATE",
            "audience_dimensions": {key: 1 for key in DIMENSIONS},
            "mixed_level_flag": False,
            "unscorable_reason": None,
            "non_compensatory_checks": {
                "FACTUAL_CRITICAL_PRESERVATION": "PASS",
                "MATERIAL_CONCEPT_PRESERVATION": "PASS",
                "FORMAT_NATIVE_CONTRACT": "PASS",
            },
            "confidence": "HIGH",
            "notes": "Automated blind rubric judgment.",
        }
        self.assertEqual(set(record), MODEL_FIELDS)
        validate_model_record(record, item_id)

    def test_model_record_rejects_human_role_injection(self):
        item_id = "BI-TEST"
        record = {
            "item_id": item_id,
            "audience_label": "INTERMEDIATE",
            "audience_dimensions": {key: 1 for key in DIMENSIONS},
            "mixed_level_flag": False,
            "unscorable_reason": None,
            "non_compensatory_checks": {
                "FACTUAL_CRITICAL_PRESERVATION": "PASS",
                "MATERIAL_CONCEPT_PRESERVATION": "PASS",
                "FORMAT_NATIVE_CONTRACT": "PASS",
            },
            "confidence": "HIGH",
            "notes": "x",
            "annotation_role": "PRIMARY_A",
        }
        with self.assertRaises(ValueError):
            validate_model_record(record, item_id)


if __name__ == "__main__":
    unittest.main()
