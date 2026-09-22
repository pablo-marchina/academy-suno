#!/usr/bin/env python3
from __future__ import annotations
import base64, gzip, json
from pathlib import Path
p=Path('data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64')
raw=gzip.decompress(base64.b64decode(b''.join(p.read_bytes().split()), validate=True)).decode('utf-8')
rows=[json.loads(x) for x in raw.splitlines() if x.strip()]
print(json.dumps({'count':len(rows),'keys':sorted(rows[0]),'first':rows[0]}, ensure_ascii=False, indent=2))
