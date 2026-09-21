import hashlib
from pathlib import Path

EXPECTED_SHA256 = "c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5"
EXPECTED_SIZE = 1_388_430
PATH = Path("artifacts/submission/final-demo.mp4")

def test_final_demo_is_exact_accepted_binary():
    payload = PATH.read_bytes()
    assert len(payload) == EXPECTED_SIZE
    assert hashlib.sha256(payload).hexdigest() == EXPECTED_SHA256
