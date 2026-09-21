# Final demo durable copy — W004-T021-A01

`STATUS: BYTE_IDENTICAL_PERSISTED`  
`TASK_ID: W004-T021`  
`ATTEMPT_ID: A01`  
`PRODUCTION_READINESS_CLAIM: NOT_MADE`

## Evaluator-facing artifact

The accepted T019 final demo is now stored as an exact repository-controlled binary at:

- repository path: `artifacts/submission/final-demo.mp4`;
- immutable persistence commit: `4d803a6ed8ad2018759bc649ac134602122fe82b`;
- immutable GitHub URL: `https://github.com/pablo-marchina/academy-suno/blob/4d803a6ed8ad2018759bc649ac134602122fe82b/artifacts/submission/final-demo.mp4`;
- immutable raw URL: `https://raw.githubusercontent.com/pablo-marchina/academy-suno/4d803a6ed8ad2018759bc649ac134602122fe82b/artifacts/submission/final-demo.mp4`;
- SHA-256: `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`;
- size: `1,388,430` bytes.

This file was copied byte-for-byte from the verified accepted Actions artifact. It was not transcoded, regenerated or re-recorded.

## Accepted source provenance

- source workflow: `W004 T019 Final Paced Demo Capture`;
- source Actions run: `35636285651`;
- accepted primary artifact ID: `10656720873`;
- artifact name: `w004-t019-final-demo-ffaa235e31667d1aab9a1f24253e647579e394e1`;
- accepted artifact ZIP SHA-256: `7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`;
- source capture commit: `ffaa235e31667d1aab9a1f24253e647579e394e1`;
- accepted MP4 filename: `final-demo.mp4`;
- accepted MP4 SHA-256: `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`;
- accepted MP4 size: `1,388,430` bytes;
- independent T020 review: `VIDEO_PACKAGE_REVIEW: PASS`.

Machine-readable provenance is in `artifacts/submission/W004-T021-A01-provenance.json`; the exact T019 artifact-contained manifest is retained at `artifacts/submission/W004-T019-A01-source-manifest.json`; the checksum file is `artifacts/submission/final-demo.sha256`.

## Byte-identity verification

Preservation Actions run `35651729045`, job `106505497873`, completed successfully. The job enforced all of the following:

1. downloaded artifact `10656720873` directly through the GitHub Actions artifact API;
2. verified the downloaded ZIP SHA-256 against `7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`;
3. extracted `final-demo.mp4` without media transformation;
4. verified source MP4 SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5` and exact size `1,388,430` bytes before persistence;
5. copied the source bytes directly to `artifacts/submission/final-demo.mp4` and verified `sha256sum` plus byte-for-byte `cmp`;
6. committed the durable copy as `4d803a6ed8ad2018759bc649ac134602122fe82b`;
7. read the persisted binary back from GitHub by the exact remote commit through the Contents API raw media endpoint;
8. re-verified the read-back SHA-256, size and byte-for-byte `cmp` against the extracted accepted source.

Result: `REMOTE_READBACK_BYTE_IDENTITY: PASS`.

## Evidence boundaries remain unchanged

The durable copy does not widen what the demo proves:

```text
mechanics:                         MECHANICS_ONLY
audience thresholds:               DIAGNOSTIC_ONLY
provider quality/latency/usage:    PRODUCTION_UNKNOWN / BLOCKED
human evidence claim:              false
provider evidence claim:           false
production-readiness claim:        false
BCB negative-control bypass:       false
```

The BCB PDF negative-control remains intentionally fail-closed (`SOURCE_BLOCKED / REVIEW_REQUIRED / LOW`) where table-role provenance is ambiguous. Persisting the accepted video does not relax human/provider prerequisites and does not authorize release or production readiness.

## Retention disposition

The accepted MP4 is no longer solely dependent on the expiring Actions artifact (`2026-12-20T18:06:45Z`). A byte-identical copy now exists in repository-controlled Git storage at an immutable commit. Canonical integration into `main` remains an Orchestrator action; this worker does not self-integrate state or release readiness.
