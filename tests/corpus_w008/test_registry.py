from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_FILE = ROOT / "experiments" / "corpus_w008" / "validate_registry.py"
REGISTRY = ROOT / "experiments" / "corpus_w008" / "registry.v1.json"
spec = importlib.util.spec_from_file_location("w008_corpus", MODULE_FILE)
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


class CorpusPreregistrationTests(unittest.TestCase):
    def test_four_family_inventory_and_no_fake_run(self) -> None:
        report = validator.validate_registry(load())
        self.assertEqual(report["validation"], "PASS_PREREGISTRATION_ONLY")
        self.assertEqual(report["historical_family_coverage"], ["BCB", "FRASER", "PETROBRAS"])
        self.assertEqual(report["not_acquired_families"], ["CVM"])
        self.assertEqual(report["observed_original_groups_from_prior_work"], 3)
        self.assertEqual(report["new_original_downloads"], 0)
        self.assertEqual(report["new_executed_source_generation_benchmarks"], 0)
        self.assertEqual(report["synthetic_control_count"], 13)
        self.assertEqual(report["predeclared_metric_count"], 9)
        self.assertEqual(report["predeclared_candidate_count"], 4)
        self.assertFalse(report["human_gold_eligible"])
        self.assertEqual(report["candidate_preference"], "PENDING_EVIDENCE")
        self.assertEqual(report["model_judge_status"], "NOT_RUN")

    def test_source_group_partition_identical_to_integrated_w009(self) -> None:
        spec2 = importlib.util.spec_from_file_location(
            "w009_integrated_harness", ROOT / "experiments" / "ai_only_w009" / "harness.py"
        )
        assert spec2 is not None and spec2.loader is not None
        w009 = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(w009)
        reg = load()
        salt = reg["partition"]["salt"]
        for group in reg["source_groups"]:
            self.assertEqual(
                validator.group_split(group["group_id"], salt=salt),
                w009.source_group_split(group["group_id"], split_salt=salt),
            )

    def test_reject_unacquired_cvm_fabricated_hash(self) -> None:
        reg = load()
        reg["source_groups"][-1]["source_sha256"] = "f" * 64
        with self.assertRaisesRegex(validator.RegistryError, "invented hash"):
            validator.validate_registry(reg)
        reg = load()
        reg["source_groups"][-1]["record_status"] = "HISTORICAL_REPOSITORY_ACCEPTED"
        with self.assertRaises(validator.RegistryError):
            validator.validate_registry(reg)

    def test_reject_original_missing_hash_or_source_ref(self) -> None:
        reg = load()
        reg["source_groups"][0]["source_sha256"] = "not-a-hash"
        with self.assertRaisesRegex(validator.RegistryError, "valid 64-char"):
            validator.validate_registry(reg)
        reg = load()
        reg["source_groups"][0]["ref"] = "UNVERIFIED"
        with self.assertRaisesRegex(validator.RegistryError, "actual W007"):
            validator.validate_registry(reg)

    def test_reject_leaked_or_renamed_control(self) -> None:
        reg = load()
        reg["adversarial_controls"][0]["kind"] = "HUMAN_GOLD"
        with self.assertRaisesRegex(validator.RegistryError, "cannot be promoted"):
            validator.validate_registry(reg)
        reg = load()
        reg["adversarial_controls"][0]["group_id"] = "nonexistent"
        with self.assertRaisesRegex(validator.RegistryError, "source-group"):
            validator.validate_registry(reg)
        reg = load()
        reg["adversarial_controls"][0]["failure_code"] = None
        with self.assertRaisesRegex(validator.RegistryError, "oracle"):
            validator.validate_registry(reg)

    def test_missingness_and_no_invented_pareto(self) -> None:
        reg = load()
        reg["current_observations"]["point_pareto"] = ["DIRECT"]
        with self.assertRaisesRegex(validator.RegistryError, "no executed benchmark"):
            validator.validate_registry(reg)
        reg = load()
        reg["study_missingness"]["human_gold"] = "HUMAN_GOLD"
        with self.assertRaisesRegex(validator.RegistryError, "waiver"):
            validator.validate_registry(reg)

    def test_competitors_and_metric_coverage_cannot_shrink(self) -> None:
        reg = load()
        reg["candidate_methods"].pop()
        with self.assertRaisesRegex(validator.RegistryError, "four comparable"):
            validator.validate_registry(reg)
        reg = load()
        reg["metric_definitions"].pop()
        with self.assertRaisesRegex(validator.RegistryError, "nine predeclared"):
            validator.validate_registry(reg)

    def test_no_dup_source_groups_or_oracle_ids(self) -> None:
        reg = load()
        reg["source_groups"][1]["group_id"] = reg["source_groups"][0]["group_id"]
        with self.assertRaisesRegex(validator.RegistryError, "duplicate group_id"):
            validator.validate_registry(reg)
        reg = load()
        reg["adversarial_controls"][1]["id"] = reg["adversarial_controls"][0]["id"]
        with self.assertRaisesRegex(validator.RegistryError, "duplicate id"):
            validator.validate_registry(reg)

    def test_report_json_round_trip_has_no_primary_source_body(self) -> None:
        report = validator.validate_registry(load())
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "inventory.json"
            dest.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
            reconstructed = json.loads(dest.read_text(encoding="utf-8"))
        self.assertEqual(reconstructed["observed_original_groups_from_prior_work"], 3)
        self.assertNotIn("source_text", reconstructed)
        self.assertNotIn("model_winner", reconstructed)
        self.assertEqual(reconstructed["measured_metric_count"], 0)

    def test_partition_depends_only_on_group_and_salt(self) -> None:
        reg = load()
        salt = reg["partition"]["salt"]
        a = "petrobras-2t26"
        self.assertEqual(validator.group_split(a, salt=salt), validator.group_split(a, salt=salt))
        with self.assertRaisesRegex(validator.RegistryError, "source group"):
            validator.group_split("", salt=salt)
        with self.assertRaisesRegex(validator.RegistryError, "salt"):
            validator.group_split(a, salt="")


if __name__ == "__main__":
    unittest.main()
