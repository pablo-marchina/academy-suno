from __future__ import annotations

import importlib.util
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

SCRIPT = Path(__file__).resolve().parents[2] / "app" / "hosting" / "render_staging.py"
spec = importlib.util.spec_from_file_location("render_staging", SCRIPT)
assert spec is not None and spec.loader is not None
staging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(staging)


class RenderFreeStagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), staging.StagingHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=5)
        cls.server.server_close()

    def test_live_health_matches_committed_canonical_enums(self) -> None:
        with urlopen(self.url + "/healthz", timeout=4) as res:
            obj = json.load(res)
            self.assertEqual(res.status, 200)
            self.assertEqual(obj["branches_defined"], 9)
            self.assertEqual(obj["canonical_audiences"], ["ADVANCED", "BEGINNER", "INTERMEDIATE"])
            self.assertEqual(obj["canonical_formats"], ["ARTICLE", "CAROUSEL", "SHORT_VIDEO"])
            self.assertTrue(obj["contract_valid"])
            self.assertFalse(obj["production_ready"])
            self.assertFalse(obj["neon_database_connected"])
            self.assertEqual(res.headers["Cache-Control"], "no-store")
            self.assertEqual(res.headers["X-Content-Type-Options"], "nosniff")

    def test_root_is_explicitly_staging_only(self) -> None:
        with urlopen(self.url, timeout=4) as res:
            body = res.read().decode("utf-8")
            self.assertIn("não é o produto pronto", body)
            self.assertIn("NOT_AUTHORIZED", body)
            self.assertNotIn('action="/process"', body)

    def test_no_product_readiness_claim(self) -> None:
        with self.assertRaises(HTTPError) as cm:
            urlopen(self.url + "/readyz", timeout=4)
        self.assertEqual(cm.exception.code, 503)
        self.assertFalse(json.load(cm.exception)["production_ready"])

    def test_upload_write_and_filesystem_route_closed(self) -> None:
        with self.assertRaises(HTTPError) as cm:
            urlopen(Request(self.url + "/process", data=b"hello", method="POST"), timeout=4)
        self.assertEqual(cm.exception.code, 405)
        self.assertEqual(cm.exception.headers["Allow"], "GET, HEAD")
        with self.assertRaises(HTTPError) as cm2:
            urlopen(self.url + "/src/suno_content/domain/enums.py", timeout=4)
        self.assertEqual(cm2.exception.code, 404)

    def test_head_no_response_body(self) -> None:
        with urlopen(Request(self.url + "/healthz", method="HEAD"), timeout=4) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), b"")


if __name__ == "__main__":
    unittest.main()
