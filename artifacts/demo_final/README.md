# Final demo evidence — W004-T019

Repository-side records in this directory bind the final paced demo to the exact task commit, GitHub Actions run, immutable artifact metadata, source hashes, MP4 hash, measured duration, dimensions/fps/audio state, DOM assertions and representative post-encode frame validation.

Primary record: `W004-T019-A01-ci-evidence.json`.

Observed binding:

- successful run `35636285651` on capture commit `ffaa235e31667d1aab9a1f24253e647579e394e1`;
- primary artifact ID `10656720873`, ZIP digest `sha256:7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`;
- `final-demo.mp4` SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`;
- measured duration `69.12 s`, H.264 `1280×720`, `25 fps`, no audio;
- nine representative frames decoded from the exported MP4 all passed post-encode validation;
- success text and real BCB PDF are bound by exact SHA-256 values;
- BCB remains a labelled fail-closed negative-control, not a bypassed success case.

The MP4 bytes themselves stay in the immutable GitHub Actions artifact rather than being committed to git. The repository evidence record must not be interpreted as human calibration, provider/model-quality evidence, independent blind-review approval or production readiness.
