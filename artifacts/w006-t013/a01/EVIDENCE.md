# W006-T013-A01 evidence manifest

This file points to the raw GitHub Actions evidence produced by the qualification run. The worker intentionally does not restate missing production scenarios as PASS.

## Source

- Worker head: `e47b786cfb05c6369498882b149bfce8f8a3b7b7`
- PR merge ref executed by Actions: `afd1fdd79674a36828871cb6752be43a120b99ba`
- Workflow run: `36024743151`
- Qualification job: `107718293041`
- Actions artifact id: `10818383025`
- Artifact name: `w006-t013-a01-afd1fdd79674a36828871cb6752be43a120b99ba`
- Artifact digest: `sha256:e872ed8b624b51b9570fc7b0eae4549c38e08d067610a374245708c8ba80319b`

## Raw bundle contents

- `qualification.json` — complete security/restart/recovery/capacity output, including per-run rows.
- `qualification-stdout.json` — console capture of the qualification output.
- `qualification-pytest.txt` — selected regression output (`43 passed, 4 subtests passed`).
- `runstore-failure-harness.json` — 14/14 durable-state scenarios and raw metrics.
- `environment.txt` — GitHub SHA/ref, runner OS/arch, Python and uv versions, platform/kernel.
- `toolchain-SHA256SUMS` — hashes for `uv.lock`, `pyproject.toml`, `toolchain.lock.json`.
- `release-workflow-audit.json` — pinned-action and token-permission audit (`PASS`).
- `release-verification.json` — artifact/SBOM/provenance verification (`PASS`).
- `release/` and `release-repeat/` — independently generated release artifact, SBOM and provenance copies used for byte comparison.
- `SHA256SUMS` — evidence digest manifest.

## Key evidence digests

- `environment.txt`: `5f5223c4b0636ca3e67a88d9f15848364bb813d3e5ce2bb017fe40306362b4dd`
- `toolchain-SHA256SUMS`: `60b38ef0dde7e592270207164978da05fb30a569757cf17601d3374095dceade`
- `qualification-pytest.txt`: `948627f3b0f17e170e6168f21462734e7a025e8879b30801dc09add30c886ba1`
- `runstore-failure-harness.json`: `85c84014f18ec35821de89a3dd741c6a06c58b18fd15b34b09ea13a28979e814`
- `qualification.json`: `a31da3bec138a65752c29ad2306a71860ebbd43e7008ddc149aa985721028bbb`
- `release-workflow-audit.json`: `e4ecce189beac8f2dfd165d5d343d7612f4bdb447b3a0d65d58a5ea7d09c697a`
- `release-verification.json`: `b5d88e438f1962a33da82b89eda48ab9a818fac2d5e4a1990ca205d356569f35`
- release artifact: `e4183a4bf24d98598c1e5b52e520f23aaab7dbb85c4131dd396fc6229ca60022`
- SBOM: `f2237a3043bcf449aa09345e120a0be769ccf8bca65d63c03adc1eca126ead8b`
- provenance: `3b88ed47c6e447fe8df39a8d8909ce48020d2216a4fbc06d56d9672edd30db26`

## Evidence boundary

Reference scope status: `PASS_REFERENCE_SCOPE`.

Production deployment/migration/rollback: `MISSING_PRODUCTION_EVIDENCE` because no representative locked production runtime/database/deployment topology exists in the task environment.

Production readiness: `NOT_AUTHORIZED`. Supported users/SLO/RTO/RPO: `NOT_CLAIMED`.
