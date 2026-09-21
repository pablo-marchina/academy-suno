import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "provider_w004" / "run_groq_a06.py"
spec = importlib.util.spec_from_file_location("run_groq_a06", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class GroqA06Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.snapshot_path = Path(self.tmp.name) / "pricing.json"
        self.snapshot_path.write_text(json.dumps({
            "kind": "official_provider_pricing",
            "provider": "Groq",
            "retrieved_at": "2026-09-21T22:18:00Z",
            "effective_at": "2026-09-21",
            "currency": "USD",
            "models": {
                "openai/gpt-oss-120b": {"source_url": "https://console.groq.com/docs/model/openai/gpt-oss-120b", "prices_per_million_tokens": {"input": 0.15, "output": 0.60}},
                "openai/gpt-oss-20b": {"source_url": "https://console.groq.com/docs/model/openai/gpt-oss-20b", "prices_per_million_tokens": {"input": 0.075, "output": 0.30}}
            }
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_redaction_removes_exact_and_groq_shaped_secret(self):
        secret = "gsk_REALISH_SECRET_123"
        safe = module.redact(f"denied {secret}; repeated gsk_OTHER_SECRET", secret)
        self.assertNotIn("gsk_", safe)
        self.assertIn("[REDACTED_GROQ_KEY]", safe)

    def test_candidate_priority_prefers_120b_then_20b(self):
        snapshot = module.load_pricing(str(self.snapshot_path))
        self.assertEqual(module.choose_candidate(["openai/gpt-oss-20b", "openai/gpt-oss-120b"], snapshot), "openai/gpt-oss-120b")
        self.assertEqual(module.choose_candidate(["openai/gpt-oss-20b"], snapshot), "openai/gpt-oss-20b")
        self.assertIsNone(module.choose_candidate(["other/model"], snapshot))

    def test_cost_uses_selected_model_pricing(self):
        snapshot = module.load_pricing(str(self.snapshot_path))
        usage = {"input_tokens": 1000, "output_tokens": 250, "total_tokens": 1250, "observed": True}
        self.assertEqual(module.derive_cost(snapshot, "openai/gpt-oss-120b", usage)["value"], 0.0003)
        self.assertEqual(module.derive_cost(snapshot, "openai/gpt-oss-20b", usage)["value"], 0.00015)

    def test_missing_secret_fails_before_network(self):
        env = "W004_A06_TEST_MISSING"
        os.environ.pop(env, None)
        result = module.execute("A06", env, "unused.txt", str(self.snapshot_path), 0.1)
        self.assertEqual(result["status"], "BLOCKED_NO_CREDENTIAL")
        self.assertEqual(result["attempt_id"], "A06")

    def test_non_groq_secret_fails_before_network(self):
        env = "W004_A06_TEST_NON_GROQ"
        os.environ[env] = "sk-not-groq"
        try:
            result = module.execute("A06", env, "unused.txt", str(self.snapshot_path), 0.1)
        finally:
            os.environ.pop(env, None)
        self.assertEqual(result["status"], "BLOCKED_PROVIDER_CLASSIFICATION")
        self.assertEqual(result["error"]["code"], "not_groq_gsk")


if __name__ == "__main__":
    unittest.main()
