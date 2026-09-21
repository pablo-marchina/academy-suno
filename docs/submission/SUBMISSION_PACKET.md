# Submission Packet — evidence index and stop conditions

`TASK: W004-T019-A01`  
`BASE_STATE_VERSION: 0028`  
`BASE_COMMIT_SHA: 584a23406291a42c29eb795d34bedd2de0357647`  
`PACKET_STATUS: UPDATED_WITH_FINAL_DEMO_TASK_SCOPE_EVIDENCE`  
`PRODUCTION_READINESS_CLAIM: NOT_MADE`

## 1. What this packet is

This document is the submission-facing index for evidence currently present in the repository. It points reviewers to the recipient app, the final paced browser capture, the consolidated experimental report, executable proof paths, observed CI provenance, open human/provider blockers and the remaining final-review gate.

It is not a release sign-off. `W004-T019` closes specific task-scope gaps around recipient-facing ingest, interactive browser demonstration and measured <=5:00 video evidence; it does not manufacture human calibration, provider quality evidence or production readiness.

## 2. Start here

1. **Recipient app quick start:** `README.md` → `Evaluator quick start — recipient app`.
2. **Final paced demo evidence:** `docs/demo/final/README.md`.
3. **Machine-readable final-demo binding:** `artifacts/demo_final/W004-T019-A01-ci-evidence.json`.
4. **Final demo task result:** `SYSTEM/RESULTS/W004-T019-A01.md`.
5. **Consolidated experimental report:** `docs/report/EXPERIMENTAL_REPORT.md`.
6. **Evidence-state shell / future fan-in slots:** `docs/release/EVIDENCE_PACKET.md`.
7. **Release stop conditions:** `docs/release/FINAL_REVIEW_CHECKLIST.md`.
8. **Prior adversarial review that motivated T019:** `docs/review_current/BLIND_ADVERSARIAL_REVIEW.md`.

## 3. Evidence-state legend

- `PROVEN` — observed/reproducible within the named scope.
- `PASS_TASK_SCOPE` — task acceptance evidence passed; this is not release/production approval.
- `DIAGNOSTIC_ONLY` — controlled signal; insufficient for threshold freeze/selection/generalization.
- `PRODUCTION_UNKNOWN` — no valid real provider/production observation supports the claim.
- `BLOCKED` — requires an external action/input that has not occurred.
- `PENDING` — a defined downstream validation/review has not run.
- `FAIL` / `REVIEW_REQUIRED` — hard negative/review states remain visible and are never averaged away.

## 4. Submission claim register

| Claim | Current state | Primary evidence | Submission-safe wording |
|---|---|---|---|
| recipient-facing text/PDF ingest | `PROVEN` in T019 task scope | T019 real-browser run | app accepts pasted text or PDF and exposes provenance/source trust in the browser |
| successful source path | `PROVEN` in T019 task scope | T019 MP4 + DOM assertions | controlled text input reached `SOURCE_READY / PASS` with exact input SHA-256 |
| exact 3×3 workflow mechanics | `PROVEN / MECHANICS_ONLY` | T019 + W004-T012/W003 proofs | exactly 9 audience × format cells were rendered on the successful path; this is mechanics, not provider-quality evidence |
| branch-local repair | `PROVEN` in controlled proof | T019 visible repair panel + persisted W003/W004 evidence | persisted `FAIL → repair → PASS` with fresh hard gates and accepted-sibling immutability |
| source-trust fail-closed behavior on real BCB PDF | `PROVEN` for this observed negative-control | T019 MP4 + source hash | real BCB PDF remained `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW`; all 9 downstream rows stayed blocked |
| final paced browser video | `PASS_TASK_SCOPE` | Actions run `35636285651` | exported H.264 MP4 measured `69.12 s`, below the `300 s` hard cap |
| exported-frame integrity | `PASS_TASK_SCOPE` | T019 post-encode validation | nine representative frames decoded from the final MP4 passed variance/distinctness and same-state screenshot comparisons |
| audience thresholds | `DIAGNOSTIC_ONLY` | calibration gate | metrics exist; numeric thresholds are not calibrated/frozen |
| target→human matrix | `BLOCKED / PENDING` | human-calibration protocol | requires two genuine independent human streams |
| human→evaluator matrix | `BLOCKED / PENDING` | human-calibration protocol | requires valid human gold first |
| provider/model content quality | `PRODUCTION_UNKNOWN / BLOCKED` | provider manual path | no authorized observed provider quality evidence yet |
| provider latency/usage | `PRODUCTION_UNKNOWN / BLOCKED` | provider manual path | no authorized observed provider telemetry yet |
| provider commercial cost | `PRODUCTION_UNKNOWN / BLOCKED` | provider manual path | no observed usage + eligible official pricing evidence yet |
| provider/model preference | `NOT_AUTHORIZED` | evidence policy | no preference can be inferred from mechanics/demo evidence |
| final release / production readiness | `PENDING` | W004-T008/final review | T019 does not replace final fan-in/review |

## 5. Final paced demo — observed provenance

Successful capture identity:

- workflow: `W004 T019 Final Paced Demo Capture`;
- Actions run: `35636285651`;
- job: `106454369407`;
- capture commit: `ffaa235e31667d1aab9a1f24253e647579e394e1`;
- runner: Ubuntu `24.04.5 LTS`;
- Python: `3.13.15`;
- Chromium: `140.0.7339.16`;
- Playwright: `1.55.0`;
- helper tests: `4 passed`;
- workflow conclusion: `success`.

Primary immutable artifact:

- artifact ID: `10656720873`;
- name: `w004-t019-final-demo-ffaa235e31667d1aab9a1f24253e647579e394e1`;
- ZIP digest: `sha256:7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`;
- download: `https://github.com/pablo-marchina/academy-suno/actions/runs/35636285651/artifacts/10656720873`;
- GitHub-reported expiry: `2026-12-20T18:06:45Z`.

Exported video:

- file: `final-demo.mp4`;
- SHA-256: `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`;
- measured duration: `69.12 s`;
- duration gate: `PASS` against hard cap `300 s`;
- codec: H.264;
- dimensions: `1280×720`;
- frame rate: `25 fps`;
- audio track: absent;
- MP4 size: `1,388,430` bytes.

Source binding:

- controlled success-text SHA-256: `a58f8201f9a034cf45ed970c2d000d714eec2e326395340c1ee9938af1301e93`;
- real Banco Central do Brasil PDF SHA-256: `4ac6a958cbff7571aad3f0125042f4b71890a70ec36e9ad9009b537e6458ce68`;
- BCB PDF size: `9,427,775` bytes;
- PDF magic bytes validated;
- synthetic fallback: not used.

The browser recording shows the success path first and the BCB document second as a labelled negative-control. The BCB source is deliberately not bypassed to force a green demo.

## 6. What the final demo visibly proves

The successful run asserted and recorded these states in the actual recipient UI:

1. home page exposes `MECHANICS_ONLY`, `DIAGNOSTIC_ONLY` and `PRODUCTION_UNKNOWN` boundaries;
2. a controlled text source reaches `SOURCE_READY / PASS` and displays its exact input SHA-256;
3. the successful path renders all 9/9 audience × format cells as `PLANNED_MECHANICS_ONLY`;
4. the repair panel exposes persisted `FAIL → repair → PASS` lineage plus fresh-gate and sibling-immutability truth values;
5. the non-claim panel preserves `DIAGNOSTIC_ONLY` and `PRODUCTION_UNKNOWN` boundaries;
6. the real BCB PDF displays its exact raw-byte SHA and remains `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` because table-role provenance is ambiguous;
7. all 9/9 BCB downstream rows remain `BLOCKED_SOURCE` in both job and status fields.

Nine representative frames were decoded from the exported MP4 at approximately `1.164`, `6.758`, `11.450`, `19.051`, `27.663`, `36.265`, `42.935`, `53.435` and `63.094` seconds. Every post-encode frame gate passed. This validation inspects final video bytes rather than trusting only DOM state or metadata.

## 7. Evidence boundaries preserved by T019

```text
mechanics:                         MECHANICS_ONLY
audience thresholds:               DIAGNOSTIC_ONLY
provider quality/latency/usage:    PRODUCTION_UNKNOWN / BLOCKED
provider commercial cost:          PRODUCTION_UNKNOWN / BLOCKED
human evidence claim:              false
provider evidence claim:           false
production-readiness claim:        false
BCB negative-control bypass:       false
```

T019's successful capture therefore does not imply that audience thresholds are calibrated, a provider is good or preferred, human truth exists, or the system is production-ready.

## 8. Human calibration — required visible blockers

### 8.1 Independent primary streams

- `PRIMARY_A`: `BLOCKED` until one genuine human independently annotates the complete frozen development bank.
- `PRIMARY_B`: `BLOCKED` until a second genuine human independently annotates the same blinded bank.
- operational independence must be genuine, not only two role labels from the same person/process.
- held-out sources remain forbidden for tuning/calibration.

### 8.2 Target → human confusion matrix

`STATUS: BLOCKED / PENDING`

Do not populate from requested generation targets. Expected future evidence must come from valid independent human annotation.

### 8.3 Human → evaluator confusion matrix

`STATUS: BLOCKED / PENDING`

This requires valid human gold after the versioned agreement/adjudication protocol.

### 8.4 Preparation artifacts

- `data/evals/w004/source_manifest_v001.json`
- `data/evals/w004/frozen_outputs_manifest_v001.json`
- `data/evals/w004/annotation_schema_v001.json`
- `data/evals/w004/annotation_plan_v001.json`
- `docs/evals/human_calibration/protocol_v001.md`
- `experiments/human_calibration/compute_agreement.py`
- `experiments/human_calibration/validate_preparation.py`

Current frozen development surface: 4 development sources × 3 formats × 3 target levels = 36 natural outputs. Two additional source identities are held out at source-document level.

## 9. Provider/model — required visible blockers

```text
content quality: PRODUCTION_UNKNOWN / BLOCKED
latency:         PRODUCTION_UNKNOWN / BLOCKED
usage:           PRODUCTION_UNKNOWN / BLOCKED
commercial cost: PRODUCTION_UNKNOWN / BLOCKED
preference:      NOT_AUTHORIZED
```

Prepared execution path:

- `.github/workflows/provider-manual-evidence.yml`
- `experiments/provider_manual/run_manual_provider.py`
- `experiments/provider_manual/provider_evidence.py`
- `experiments/provider_manual/import_provider_evidence.py`
- `docs/provider_manual/README.md`
- `docs/provider_manual/provider-observed-evidence-v1.schema.json`

The path is credential-safe and manual-only. A no-secret demonstration correctly remained `BLOCKED_NO_CREDENTIAL`; it is not a provider observation.

For a provider mechanics artifact to become comparable, future evidence must include exact provider/model/version/endpoint provenance, observed latency, provider-reported usage, eligible official-pricing provenance if cost is claimed, derived cost from that observed usage/pricing, and a response fingerprint. Content-quality evidence remains separate and must come from valid source/human evaluation.

## 10. Parser/source-trust packet

Primary references:

- `experiments/parser_w004/observed_results.json`
- `docs/parser_w004/README.md`
- `SYSTEM/RESULTS/W004-T003-A01.md`

Submission-safe facts:

- provenance-preserving reference: `PASS`;
- flat value-only behavior: `REVIEW_REQUIRED` even at 100% value coverage;
- wrong-role probe: `FAIL`;
- wrong-unit/table probe: `FAIL`;
- parser implementation: `UNLOCKED`;
- T019 confirms the recipient path remains fail-closed on the real BCB PDF when table-role provenance is unavailable.

Residual gap: same-raw-byte cross-parser comparison and OCR/scanned-document coverage remain pending.

## 11. Repair / telemetry / audit packet

Primary references:

- `experiments/w003_e2e/run_proof.py`
- `experiments/repair/run_controlled_repair.py`
- `experiments/telemetry/demo_summary_v001.json`
- `app/evidence_cockpit.py`
- `docs/cockpit/README.md`

Submission-safe facts:

- one controlled branch persists a before `FAIL` and after `PASS` with distinct hashes;
- all source/factual/policy hard gates run fresh after repair;
- accepted siblings remain immutable;
- transport retry and quality repair are distinct event classes;
- unobserved usage/cost remains `null/N/A`;
- hard failures/review states remain visible in aggregate/cockpit views;
- no aggregate green/readiness score is computed;
- T019 makes the persisted repair lineage visible inside the evaluator-facing recipient flow.

## 12. Reproduction commands

### Recipient app

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --disable-pip-version-check --no-cache-dir \
  'pydantic==2.13.4' 'pypdf==5.9.0'
PYTHONPATH=src python app/recipient/server.py --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765`.

### Clean foundation + release smoke

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --disable-pip-version-check --no-cache-dir \
  'pydantic==2.13.4' 'pytest==9.0.2'
python experiments/foundation_regression/run_foundation_regression.py
python scripts/release_smoke/run_release_smoke.py \
  --workdir /tmp/academy-suno-release-smoke \
  --output /tmp/academy-suno-release-smoke/manifest.json
python -m pytest -q tests/release_smoke/test_release_smoke.py
```

### Parser/source-trust

```bash
python3 experiments/parser_w004/run_bakeoff.py \
  --output /tmp/parser-w004-results.json
python3 -m unittest discover -s tests/parser_w004 -p 'test_*.py' -v
```

### Human-preparation validation

```bash
python experiments/human_calibration/validate_preparation.py
```

Do not compute/promote human matrices until the two genuine independent primary streams exist.

## 13. Prior blind-review findings after T019 task-scope remediation

The prior integrated blind/adversarial review was `NOT_PASS`; T019 is a remediation task, not a self-issued blind-review PASS. Status below records what T019 changed while preserving the need for independent downstream review.

| Finding | Prior severity | Status after T019 task scope |
|---|---|---|
| F-001 final real demo video absent | CRITICAL | `ADDRESSED_IN_T019_TASK_SCOPE`; real MP4 exists, independent review still pending |
| F-002 recipient-facing raw PDF/text ingest not demonstrated | HIGH | `ADDRESSED_IN_T019_TASK_SCOPE`; both text and real PDF exercised in browser |
| F-003 interactive app/dashboard adherence risk | HIGH | `ADDRESSED_TECHNICALLY_IN_T019`; recipient app is directly runnable and recorded; evaluator review pending |
| F-004 central 3×3 proof is deterministic-stub mechanics | HIGH | `CONTROLLED_BY_DISCLOSURE`; remains `MECHANICS_ONLY` |
| F-005 independent human calibration absent | HIGH | `BLOCKED / PENDING` |
| F-006 real provider evidence absent | HIGH | `BLOCKED / PRODUCTION_UNKNOWN` |
| F-007 consolidated experimental report absent | HIGH | `ADDRESSED` by `docs/report/EXPERIMENTAL_REPORT.md` |
| F-008 actual <=5:00 duration unverified | MEDIUM | `ADDRESSED_IN_T019_TASK_SCOPE`; ffprobe measured `69.12 s` |
| F-009 traceability wording scope | MEDIUM | orchestrator/final-review follow-up |
| F-010 submission logistics/owner/workflow unknown | MEDIUM | external/operational follow-up remains |

## 14. Traceability anchors

The detailed canonical matrix remains `SYSTEM/TRACEABILITY_MATRIX.md`. Relevant anchors for this packet include:

- `PAIN-001..005` — audience complexity, nuance preservation, evaluator bias, auditability and trusted multichannel scale;
- `REQ-001..021` — source ingestion/trust, graph/state, 3×3 generation, audience/format/eval/repair/cockpit/report/reproducibility;
- `REQ-022..023` — final real video and measured <=5:00 evidence are now observed in T019 task scope, pending canonical fan-in/final review;
- `CRIT-001` — hard factual/eliminatory requirements are non-compensating.

Assumption/risk context remains canonical in `SYSTEM/ASSUMPTION_RISK_REGISTER.md`. T019 does not mutate those canonical records.

## 15. Final submission stop conditions

Do not claim final release/production readiness while any required item below remains unresolved:

1. two genuine independent human primary annotation streams are absent where final claims require human calibration;
2. required pre-adjudication agreement/adjudication and observed confusion matrices are absent;
3. real authorized provider evidence sufficient for any intended provider/model comparison is absent;
4. any commercial cost claim lacks observed usage + eligible official pricing provenance;
5. semantic-ablation decision is required but not measured on valid human gold;
6. independent post-remediation evaluator/blind review has not completed the intended T020 check;
7. final clean fan-in/review has not produced the required W004-T008/final release result;
8. external submission logistics/ownership remain unresolved if required by the challenge process.

The former T015 stop conditions for “recipient-facing raw ingest unproven”, “final video absent” and “<=5:00 unverified” are specifically addressed by T019 task-scope evidence. They must not be reintroduced as unknowns unless a later review finds a concrete defect in that evidence.

## 16. Non-claims

This packet makes no claim that:

- audience thresholds are calibrated;
- the target label is human truth;
- a provider/model is superior or preferred;
- real provider latency/usage/cost has been measured;
- a parser implementation has won a same-byte bakeoff;
- deterministic-stub outputs demonstrate provider quality;
- the T019 task PASS is an independent blind-review PASS;
- the system is production-ready or release-approved.

The packet is useful only if reviewers can distinguish what is observed, diagnostic, inferred, unknown, blocked and pending without consulting hidden assumptions.

## Durable final demo artifact

The accepted T019 MP4 is preserved byte-identically at `artifacts/submission/final-demo.mp4`. See `docs/submission/FINAL_DEMO_ARTIFACT.md` for hash, provenance, and scope boundaries.
