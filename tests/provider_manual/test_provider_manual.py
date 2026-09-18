import argparse
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]
MODULE_DIR = ROOT / "experiments" / "provider_manual"
sys.path.insert(0, str(MODULE_DIR))

import provider_evidence
import run_manual_provider


def observed_probe():
    return {
        "schema_version": "provider-probe-v1",
        "task_id": "W004-T004",
        "captured_at": "2026-09-17T20:00:00+00:00",
        "status": "OBSERVED_RUN",
        "provider": "example",
        "provider_protocol": "openai_responses",
        "model": "example-model",
        "model_version": "2026-09-17",
        "endpoint": "https://provider.example/v1/responses",
        "latency_ms": 123.4,
        "usage": {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120, "observed": True},
        "pricing_provenance": {
            "status": "OBSERVED_SNAPSHOT",
            "kind": "official_provider_pricing",
            "source_url": "https://provider.example/pricing",
            "retrieved_at": "2026-09-17T19:00:00Z",
            "effective_at": "2026-09-17",
            "currency": "USD",
            "commercial_evidence_eligible": True,
        },
        "cost": {"value": 0.001, "currency": "USD", "observed": False, "derived": True},
        "response": {"sha256": "a" * 64, "bytes": 42},
        "content_quality_evidence": False,
    }


class ProviderManualEvidenceTests(unittest.TestCase):
    def test_observed_official_evidence_is_mechanics_eligible_only(self):
        evidence = provider_evidence.export_probe(observed_probe())
        self.assertTrue(evidence["comparison_eligibility"]["mechanics_eligible_for_t007"])
        self.assertFalse(evidence["comparison_eligibility"]["full_provider_comparison_eligible"])
        self.assertEqual(provider_evidence.validate_evidence(evidence), [])

    def test_synthetic_pricing_is_rejected_for_comparison(self):
        probe = observed_probe()
        probe["pricing_provenance"]["kind"] = "synthetic"
        probe["pricing_provenance"]["commercial_evidence_eligible"] = False
        evidence = provider_evidence.export_probe(probe)
        self.assertFalse(evidence["comparison_eligibility"]["mechanics_eligible_for_t007"])
        self.assertIn("official_pricing_provenance_ineligible", provider_evidence.validate_evidence(evidence))

    def test_missing_model_version_is_rejected(self):
        probe = observed_probe()
        probe["model_version"] = "N/A"
        evidence = provider_evidence.export_probe(probe)
        self.assertIn("missing_provenance_model_version", provider_evidence.validate_evidence(evidence))

    def test_secret_like_fields_are_rejected(self):
        evidence = provider_evidence.export_probe(observed_probe())
        evidence["secret"] = "should-never-exist"
        self.assertTrue(
            any(
                finding.startswith("secret_like_fields_present:")
                for finding in provider_evidence.validate_evidence(evidence)
            )
        )

    def test_no_secret_uses_existing_harness_and_stays_blocked_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = argparse.Namespace(
                provider="example",
                protocol="openai_responses",
                model="example-model",
                model_version="2026-09-17",
                endpoint="https://example.invalid/v1/responses",
                api_key_env="W004_T010_TEST_KEY_MISSING",
                prompt="ping",
                prompt_file=None,
                pricing_snapshot=None,
                timeout=0.1,
                probe_output=str(Path(tmp) / "probe.json"),
                evidence_output=str(Path(tmp) / "evidence.json"),
            )
            os.environ.pop(args.api_key_env, None)
            evidence = run_manual_provider.execute_manual(args)
            self.assertEqual(evidence["status"], "BLOCKED_NO_CREDENTIAL")
            self.assertFalse(evidence["observed_run"])
            self.assertFalse(evidence["comparison_eligibility"]["mechanics_eligible_for_t007"])
            self.assertTrue(Path(args.probe_output).exists())
            self.assertTrue(Path(args.evidence_output).exists())


if __name__ == "__main__":
    unittest.main()
