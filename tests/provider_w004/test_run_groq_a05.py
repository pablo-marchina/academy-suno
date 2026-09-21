import importlib.util
import os
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "provider_w004" / "run_groq_a05.py"
spec = importlib.util.spec_from_file_location("run_groq_a05", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class GroqA05Tests(unittest.TestCase):
    def test_redaction_removes_exact_and_groq_shaped_secret(self):
        secret = "gsk_REALISH_SECRET_123"
        text = f"denied for {secret}; repeated gsk_OTHER_SECRET"
        safe = module.redact(text, secret)
        self.assertNotIn("gsk_", safe)
        self.assertIn("[REDACTED_GROQ_KEY]", safe)

    def test_cost_uses_official_120b_snapshot(self):
        usage = {"input_tokens": 1000, "output_tokens": 250, "total_tokens": 1250, "observed": True}
        cost = module.derive_cost(usage)
        self.assertTrue(cost["derived"])
        self.assertEqual(cost["currency"], "USD")
        self.assertEqual(cost["value"], 0.0003)

    def test_missing_secret_fails_before_network(self):
        env = "W004_A05_TEST_MISSING"
        os.environ.pop(env, None)
        result = module.execute("A05", env, "does-not-matter.txt", 0.1)
        self.assertEqual(result["status"], "BLOCKED_NO_CREDENTIAL")
        self.assertEqual(result["attempt_id"], "A05")
        self.assertEqual(result["preflight"]["status"], "NOT_RUN")

    def test_non_groq_secret_fails_before_network(self):
        env = "W004_A05_TEST_NON_GROQ"
        os.environ[env] = "sk-not-groq"
        try:
            result = module.execute("A05", env, "does-not-matter.txt", 0.1)
        finally:
            os.environ.pop(env, None)
        self.assertEqual(result["status"], "BLOCKED_PROVIDER_CLASSIFICATION")
        self.assertEqual(result["error"]["code"], "not_groq_gsk")

    def test_pricing_provenance_is_eligible_and_versioned(self):
        pricing = module.pricing_provenance()
        self.assertTrue(pricing["commercial_evidence_eligible"])
        self.assertEqual(pricing["kind"], "official_provider_pricing")
        self.assertEqual(pricing["currency"], "USD")
        self.assertIn("groq.com", pricing["source_url"])


if __name__ == "__main__":
    unittest.main()
