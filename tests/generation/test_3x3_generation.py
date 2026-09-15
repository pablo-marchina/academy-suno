from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.domain import AudienceLevel, OutputFormat, SourceProvenance  # noqa: E402
from suno_content.generation.contracts import build_3x3_variant_specs  # noqa: E402


class ThreeByThreePlanningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = SourceProvenance(
            source_id="source-001",
            source_hash="b" * 64,
            artifact_ref="raw/source.pdf",
        )

    def build(self):
        return build_3x3_variant_specs(
            source=self.source,
            source_backbone_ref="backbone/source-001/v1",
            policy_context_ref="policy/source-001/v1",
            prompt_version="prompt-v3",
            output_schema_version="format-native-v1",
        )

    def test_builds_exact_cartesian_3x3(self) -> None:
        specs = self.build()
        self.assertEqual(len(specs), 9)
        self.assertEqual(len({spec.job_id for spec in specs}), 9)
        self.assertEqual(
            {(spec.audience, spec.format) for spec in specs},
            {(audience, fmt) for audience in AudienceLevel for fmt in OutputFormat},
        )

    def test_plan_is_deterministic_and_canonical(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual([spec.job_id for spec in first], [spec.job_id for spec in second])
        self.assertEqual([spec.canonical_json() for spec in first], [spec.canonical_json() for spec in second])

    def test_source_and_contract_refs_are_shared_without_provider_model(self) -> None:
        specs = self.build()
        for spec in specs:
            self.assertEqual(spec.source, self.source)
            self.assertEqual(spec.source_backbone_ref, "backbone/source-001/v1")
            self.assertEqual(spec.policy_context_ref, "policy/source-001/v1")
            self.assertNotIn("provider", type(spec).model_fields)
            self.assertNotIn("model", type(spec).model_fields)

    def test_input_change_changes_job_ids(self) -> None:
        first = self.build()
        changed = build_3x3_variant_specs(
            source=self.source,
            source_backbone_ref="backbone/source-001/v2",
            policy_context_ref="policy/source-001/v1",
            prompt_version="prompt-v3",
            output_schema_version="format-native-v1",
        )
        self.assertNotEqual([spec.job_id for spec in first], [spec.job_id for spec in changed])


if __name__ == "__main__":
    unittest.main()
