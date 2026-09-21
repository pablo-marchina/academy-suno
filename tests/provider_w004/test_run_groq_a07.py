import importlib.util
import json
import tempfile
import unittest
from email.message import Message
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "provider_w004" / "run_groq_a07.py"
spec = importlib.util.spec_from_file_location("run_groq_a07", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class GroqA07Tests(unittest.TestCase):
    def test_redact_strips_groq_keys(self):
        safe = module.redact("gsk_REAL and gsk_OTHER", "gsk_REAL")
        self.assertNotIn("gsk_", safe)

    def test_safe_headers_keeps_only_diagnostic_allowlist(self):
        h = Message(); h["Server"]="cloudflare"; h["CF-Ray"]="abc"; h["Authorization"]="secret"
        out = module.safe_headers(h)
        self.assertEqual(out["server"], "cloudflare")
        self.assertEqual(out["cf-ray"], "abc")
        self.assertNotIn("authorization", out)

    def test_candidate_priority(self):
        snap = {"models":{"openai/gpt-oss-120b":{},"openai/gpt-oss-20b":{}}}
        self.assertEqual(module.choose(["openai/gpt-oss-20b","openai/gpt-oss-120b"], snap), "openai/gpt-oss-120b")

    def test_pricing_file_parses(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.json"; p.write_text(json.dumps({"kind":"official_provider_pricing","provider":"Groq","models":{}}))
            self.assertEqual(module.load_snapshot(str(p))["provider"], "Groq")

if __name__ == "__main__": unittest.main()
