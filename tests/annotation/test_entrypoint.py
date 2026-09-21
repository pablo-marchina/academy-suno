from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class AnnotationEntrypointTests(unittest.TestCase):
    def test_direct_script_does_not_shadow_stdlib_operator(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [sys.executable, "app/annotation/operator.py", "--help"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("W004 blind primary annotation operator", result.stdout)

    def test_module_invocation_is_supported(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [sys.executable, "-m", "app.annotation.operator", "--help"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("W004 blind primary annotation operator", result.stdout)


if __name__ == "__main__":
    unittest.main()
