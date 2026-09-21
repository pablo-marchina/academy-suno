import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "provider_w004" / "run_authorized_attempt_a04.py"
spec = importlib.util.spec_from_file_location("authorized_attempt_a04", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class A04CredentialClassificationTests(unittest.TestCase):
    def test_raw_groq_key_family(self):
        provider, value, reason = module.normalize_and_classify("gsk_example")
        self.assertEqual((provider, value), ("groq", "gsk_example"))
        self.assertEqual(reason, "raw_groq_gsk")

    def test_raw_xai_key_family(self):
        provider, value, reason = module.normalize_and_classify("xai-example")
        self.assertEqual((provider, value), ("xai", "xai-example"))
        self.assertEqual(reason, "raw_xai_prefix")

    def test_explicit_groq_wrapper_identifies_future_format(self):
        provider, value, reason = module.normalize_and_classify('export GROQ_API_KEY="future-format"')
        self.assertEqual((provider, value), ("groq", "future-format"))
        self.assertEqual(reason, "exported_GROQ_API_KEY")

    def test_explicit_xai_wrapper_identifies_future_format(self):
        provider, value, reason = module.normalize_and_classify("XAI_API_KEY='future-format'")
        self.assertEqual((provider, value), ("xai", "future-format"))
        self.assertEqual(reason, "assignment_XAI_API_KEY")

    def test_openrouter_is_not_misrouted_to_openai(self):
        provider, value, reason = module.normalize_and_classify("sk-or-v1-example")
        self.assertIsNone(provider)
        self.assertIsNone(value)
        self.assertEqual(reason, "identified_openrouter_but_a04_does_not_route_it")

    def test_google_standard_key_is_not_assumed_gemini(self):
        provider, value, reason = module.normalize_and_classify("AIzaExample")
        self.assertIsNone(provider)
        self.assertIsNone(value)
        self.assertEqual(reason, "identified_google_standard_key_but_gemini_not_proven")

    def test_ambiguous_unknown_remains_blocked(self):
        provider, value, reason = module.normalize_and_classify("not-identifiable")
        self.assertIsNone(provider)
        self.assertIsNone(value)
        self.assertEqual(reason, "unsupported_or_ambiguous_credential_format")


if __name__ == "__main__":
    unittest.main()
