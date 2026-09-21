# Final paced demo — W004-T019

This directory documents the evaluator-facing real-browser capture produced by `W004-T019-A01`.

## Observed final capture

- workflow: `W004 T019 Final Paced Demo Capture`
- successful Actions run: `35636285651`
- capture commit: `ffaa235e31667d1aab9a1f24253e647579e394e1`
- primary immutable artifact ID: `10656720873`
- primary artifact: `w004-t019-final-demo-ffaa235e31667d1aab9a1f24253e647579e394e1`
- primary artifact ZIP digest: `sha256:7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`
- artifact download: `https://github.com/pablo-marchina/academy-suno/actions/runs/35636285651/artifacts/10656720873`
- artifact expiry reported by GitHub: `2026-12-20T18:06:45Z`
- MP4: `final-demo.mp4`
- MP4 SHA-256: `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`
- measured duration: `69.12 s` (`PASS` against the `300 s` hard cap)
- video: H.264, `1280×720`, `25 fps`, no audio track
- source text SHA-256: `a58f8201f9a034cf45ed970c2d000d714eec2e326395340c1ee9938af1301e93`
- real BCB PDF SHA-256: `4ac6a958cbff7571aad3f0125042f4b71890a70ec36e9ad9009b537e6458ce68`
- provenance artifact ID: `10656775849`
- provenance artifact ZIP digest: `sha256:0f8e8e786afca176a19b9d0c70c18b9134a37ee91d234dc53a87286b38c692b0`

The CI gate decoded nine representative frames from the exported MP4 itself and compared them with browser screenshots captured at the corresponding states. All nine post-encode frame checks passed; this is not a metadata-only validation.

## Demonstrated order

The capture intentionally shows two source-trust outcomes in this order:

1. a genuine recipient-facing text input reaches `SOURCE_READY / PASS`, exposes its exact input SHA-256, shows all 9/9 audience × format cells as `PLANNED_MECHANICS_ONLY`, surfaces the persisted `FAIL → repair → PASS` lineage and then the non-claim boundaries;
2. the real public Banco Central do Brasil PDF is introduced as a labelled negative-control and remains `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` because table-role provenance is ambiguous. All 9/9 downstream rows remain `BLOCKED_SOURCE`.

The BCB path is not bypassed or promoted merely to create a green demo. The recording preserves `MECHANICS_ONLY`, `DIAGNOSTIC_ONLY`, `PRODUCTION_UNKNOWN/BLOCKED`, no human/provider evidence claim and no production-readiness claim.

## Reproduce the recipient app locally

From a clean checkout with Python 3.11+:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --disable-pip-version-check --no-cache-dir \
  'pydantic==2.13.4' 'pypdf==5.9.0'
PYTHONPATH=src python app/recipient/server.py --host 127.0.0.1 --port 8765
```

Then open `http://127.0.0.1:8765` in a browser. The app accepts either pasted text or an uploaded PDF and renders provenance/source trust, the 3×3 comparison surface, repair evidence and explicit non-claims.

The complete machine-readable CI binding is persisted in `artifacts/demo_final/W004-T019-A01-ci-evidence.json`; task-level conclusions and boundaries are in `SYSTEM/RESULTS/W004-T019-A01.md`.
