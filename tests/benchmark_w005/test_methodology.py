import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "experiments/benchmark_w005/validate_methodology.py"

spec = importlib.util.spec_from_file_location("validate_w005_methodology", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

class BenchmarkMethodologyContractTest(unittest.TestCase):
    def test_methodology_invariants(self):
        module.validate()

    def test_artifacts_exist(self):
        self.assertTrue((ROOT / "docs/evals/benchmark_methodology_w005.md").is_file())
        self.assertTrue((ROOT / "data/evals/w005/benchmark_methodology_v001.json").is_file())
        self.assertTrue((ROOT / "data/evals/w005/benchmark_result_v001.schema.json").is_file())

if __name__ == "__main__":
    unittest.main()
