import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "provider_w004" / "run_groq_a08.py"
spec = importlib.util.spec_from_file_location("run_groq_a08", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class GroqA08Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.p=Path(self.tmp.name)/"pricing.json"
        self.p.write_text(json.dumps({"kind":"official_provider_pricing","provider":"Groq","retrieved_at":"2026-09-21T22:18:00Z","effective_at":"2026-09-21","currency":"USD","models":{"openai/gpt-oss-120b":{"source_url":"https://console.groq.com/docs/model/openai/gpt-oss-120b","prices_per_million_tokens":{"input":0.15,"output":0.60}},"openai/gpt-oss-20b":{"source_url":"https://console.groq.com/docs/model/openai/gpt-oss-20b","prices_per_million_tokens":{"input":0.075,"output":0.30}}}}),encoding="utf-8")
    def tearDown(self): self.tmp.cleanup()
    def test_redaction(self): self.assertNotIn("gsk_",module.redact("gsk_SECRET","gsk_SECRET"))
    def test_candidate_priority(self):
        s=module.load_snapshot(str(self.p)); self.assertEqual(module.choose(["openai/gpt-oss-20b","openai/gpt-oss-120b"],s),"openai/gpt-oss-120b")
    def test_cost(self):
        s=module.load_snapshot(str(self.p)); u={"input_tokens":1000,"output_tokens":250,"total_tokens":1250,"observed":True}; self.assertEqual(module.derive_cost(s,"openai/gpt-oss-120b",u)["value"],0.0003)
    def test_missing_secret_fails_before_client_call(self):
        env="W004_A08_MISSING"; os.environ.pop(env,None); r=module.execute("A08",env,"unused",str(self.p),0.1); self.assertEqual(r["status"],"BLOCKED_NO_CREDENTIAL")
if __name__=="__main__": unittest.main()
