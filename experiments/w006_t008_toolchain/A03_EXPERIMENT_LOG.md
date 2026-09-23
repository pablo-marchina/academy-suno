# W006-T008-A03 experiment log

## Binding protocol

- DR: `docs/decisions/research/DR-6009-reproducible-toolchain-supply-chain-pareto.md`
- DR preregistration commit: `bec4fd2d948d35f407647b89a0eb1cf1194dbd40`
- machine protocol commit: `bbd226d46e45e7bfce86e400f8c0956208202497`
- decision mechanics: hard gates -> raw metrics -> repeat/range uncertainty -> point Pareto
- prohibited: scalar weights, composite utility, min-max preference scoring, synthetic neutral objectives, hard-gate compensation

## Binding package-manager measurement

- workflow run: `35888663207` (`SUCCESS`)
- artifact: `10764356042`
- artifact digest: `sha256:70e5e5de89b308a48f2e19d54650a6dcc5a484eca6be744cfc9b9d4425051b18`
- branch head: `bbd226d46e45e7bfce86e400f8c0956208202497`
- PR merge SHA: `331eb513c5a27166b5dade81e5f8ccd049a4f3f7`
- raw benchmark SHA-256: `4d390a2154364ae5ce108e42bc62b22a0a1767ccf4fa6f31801a279599a9b249`
- platform: `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39`
- Python: 3.13.15
- repeats: 3 per candidate

| candidate | hard gates | first lock median s | first sync median s | warm sync median s | lock digest stable |
|---|---|---:|---:|---:|---|
| uv 0.12.18 | PASS | 0.0207 | 0.0392 | 0.0096 | yes |
| Poetry 2.5.1 | PASS | 2.3400 | 2.4442 | 0.8529 | yes |
| PDM 2.29.2 | PASS | 29.1955 | 14.1363 | 0.5791 | yes |

Point Pareto frontier: `[uv]`.

Complete raw repeats, ranges, return codes and lock digests are persisted in `a03-candidate-observation-dataset.json` and the immutable workflow artifact.

## Binding selected-baseline supply-chain validation

- workflow run: `35888663048` (`SUCCESS`)
- supply artifact: `10764027447`, digest `sha256:68b9c088272ccfb91cf9b697daa582e5236e6cd60195bf0e2758a0c59c90af79`
- attestation artifact: `10764306756`, digest `sha256:94eb54cd4a909b0820d1de26b4cc7c56129a8e1319ffe39dc3d814faca234cd3`
- clean locked install/build/test: PASS
- deterministic double-build: PASS
- movable release Action refs: 0
- broad release token permissions: 0
- pull-request reusable cache write: skipped
- SPDX verification: PASS
- local provenance verification: PASS
- GitHub build attestation + verification: PASS
- production-ready claim: false

## Interpretation

Fresh A03 evidence satisfies the preregistered scoped lock rule: all required objective vectors are complete and comparable; uv is the only non-dominated eligible candidate; selected-baseline supply-chain gates pass. No A01/A02 decision result is used as A03 authority.
