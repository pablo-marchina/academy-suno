from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class FriendlyAnnotationEntrypointTests(unittest.TestCase):
    def test_module_help_runs_from_clean_repo_root(self):
        result = subprocess.run(
            [sys.executable, "-m", "app.annotation.friendly", "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Interface guiada em português", result.stdout)
        self.assertIn("--session", result.stdout)


if __name__ == "__main__":
    unittest.main()
