import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "provider_w004" / "run_authorized_attempt.py"
spec = importlib.util.spec_from_file_location("authorized_attempt", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AuthorizedAttemptNormalizationTests(unittest.TestCase):
    def test_raw_openai_prefix(self):
        provider, value, reason = module.normalize_and_classify("sk-example-openai")
        self.assertEqual(provider, "openai")
        self.assertEqual(value, "sk-example-openai")
        self.assertEqual(reason, "raw_openai_prefix")

    def test_raw_anthropic_prefix(self):
        provider, value, reason = module.normalize_and_classify("sk-ant-api03-example")
        self.assertEqual(provider, "anthropic")
        self.assertEqual(value, "sk-ant-api03-example")
        self.assertEqual(reason, "raw_anthropic_prefix")

    def test_openai_assignment_can_identify_future_key_format(self):
        provider, value, reason = module.normalize_and_classify('OPENAI_API_KEY="future-format-value"')
        self.assertEqual(provider, "openai")
        self.assertEqual(value, "future-format-value")
        self.assertEqual(reason, "assignment_OPENAI_API_KEY")

    def test_exported_anthropic_assignment(self):
        provider, value, reason = module.normalize_and_classify("export ANTHROPIC_API_KEY='future-anthropic-value'")
        self.assertEqual(provider, "anthropic")
        self.assertEqual(value, "future-anthropic-value")
        self.assertEqual(reason, "exported_ANTHROPIC_API_KEY")

    def test_generic_assignment_still_requires_key_family(self):
        provider, value, reason = module.normalize_and_classify("PROVIDER_API_KEY=not-identifiable")
        self.assertIsNone(provider)
        self.assertIsNone(value)
        self.assertEqual(reason, "unsupported_or_ambiguous_credential_format")

    def test_service_account_json_value_is_classified_without_persisting_json(self):
        provider, value, reason = module.normalize_and_classify('{"api_key":{"value":"sk-json-example"}}')
        self.assertEqual(provider, "openai")
        self.assertEqual(value, "sk-json-example")
        self.assertEqual(reason, "json_value_openai_prefix")

    def test_multiple_assignments_fail_closed(self):
        provider, value, reason = module.normalize_and_classify(
            "OPENAI_API_KEY=one\nANTHROPIC_API_KEY=two"
        )
        self.assertIsNone(provider)
        self.assertIsNone(value)
        self.assertEqual(reason, "ambiguous_multiple_api_key_assignments")


if __name__ == "__main__":
    unittest.main()
