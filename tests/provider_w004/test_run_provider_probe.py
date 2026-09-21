import importlib.util
import json
import os
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "provider_w004" / "run_provider_probe.py"
spec = importlib.util.spec_from_file_location("probe", MODULE_PATH)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class ProbeTests(unittest.TestCase):
    def test_usage_unobserved_stays_na(self):
        usage = probe.extract_usage("openai_responses", {})
        self.assertFalse(usage["observed"])
        self.assertEqual(usage["input_tokens"], "N/A")

    def test_synthetic_pricing_is_not_commercial_evidence(self):
        snapshot = {
            "kind": "synthetic",
            "source_url": "N/A",
            "currency": "USD",
            "prices_per_million_tokens": {"input": 1, "output": 1},
        }
        prov = probe.pricing_provenance(snapshot)
        self.assertFalse(prov["commercial_evidence_eligible"])
        usage = {"input_tokens": 100, "output_tokens": 50, "total_tokens": 150, "observed": True}
        self.assertEqual(probe.compute_cost(usage, snapshot)["value"], "N/A")

    def test_official_pricing_can_derive_cost_only_with_observed_usage(self):
        snapshot = {
            "kind": "official_provider_pricing",
            "source_url": "https://provider.example/pricing",
            "retrieved_at": "2026-09-17T00:00:00Z",
            "effective_at": "2026-09-17",
            "currency": "USD",
            "prices_per_million_tokens": {"input": 2.0, "output": 8.0},
        }
        usage = {"input_tokens": 1000, "output_tokens": 250, "total_tokens": 1250, "observed": True}
        cost = probe.compute_cost(usage, snapshot)
        self.assertTrue(cost["derived"])
        self.assertEqual(cost["value"], 0.004)

    def test_missing_credential_returns_explicit_blocker_without_network(self):
        class Args:
            attempt_id = "A02"
            provider = "example"
            protocol = "openai_responses"
            model = "example-model"
            model_version = None
            endpoint = "https://example.invalid/v1/responses"
            api_key_env = "W004_TEST_KEY_SHOULD_NOT_EXIST"
            prompt = "ping"
            prompt_file = None
            pricing_snapshot = None
            timeout = 0.1
        os.environ.pop(Args.api_key_env, None)
        result = probe.execute(Args())
        self.assertEqual(result["status"], "BLOCKED_NO_CREDENTIAL")
        self.assertEqual(result["attempt_id"], "A02")
        self.assertEqual(result["latency_ms"], "N/A")
        self.assertFalse(result["content_quality_evidence"])

    def test_openai_request_has_bounded_output(self):
        request = probe.build_request(
            "openai_responses",
            "https://api.example/v1/responses",
            "not-a-real-key",
            "example-model",
            "ping",
        )
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(body["max_output_tokens"], 128)

    def test_anthropic_request_has_bounded_output(self):
        request = probe.build_request(
            "anthropic_messages",
            "https://api.example/v1/messages",
            "not-a-real-key",
            "example-model",
            "ping",
        )
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(body["max_tokens"], 128)


if __name__ == "__main__":
    unittest.main()
