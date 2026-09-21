# Submission Packet — evidence index and stop conditions

`TASK: W004-T015-A01`  
`BASE_STATE_VERSION: 0024`  
`BASE_COMMIT_SHA: 83a5ffc1eacdd245773845eeae9d4542aa683c4f`  
`PACKET_STATUS: PREPARED_WITH_EXPLICIT_BLOCKERS`  
`PRODUCTION_READINESS_CLAIM: NOT_MADE`

## 1. What this packet is

This document is the submission-facing index for the evidence currently present in the repository. It points reviewers to the consolidated experiment report, executable proof paths, observed CI provenance, open blind-review findings and evidence that is still unavailable.

It is not a release sign-off. Missing human/provider/final-video evidence is intentionally visible rather than replaced by proxy values.

## 2. Start here

1. **Consolidated experimental report:** `docs/report/EXPERIMENTAL_REPORT.md`
2. **Project reproduction entry point:** `README.md`
3. **Observed clean release-smoke evidence:**
   - `docs/release/release_smoke/W004-T012-A01-manifest.json`
   - `docs/release/release_smoke/W004-T012-A01-ci-provenance.json`
4. **Evidence-state shell / future fan-in slots:** `docs/release/EVIDENCE_PACKET.md`
5. **Release stop conditions:** `docs/release/FINAL_REVIEW_CHECKLIST.md`
6. **Current adversarial review:** `docs/review_current/BLIND_ADVERSARIAL_REVIEW.md`
7. **Demo storyboard:** `docs/demo/DEMO_SCRIPT.md`

## 3. Evidence-state legend

- `PROVEN` — observed/reproducible within the named scope.
- `DIAGNOSTIC_ONLY` — controlled signal; insufficient for threshold freeze/selection/generalization.
- `PRODUCTION_UNKNOWN` — no valid real provider/production observation supports the claim.
- `BLOCKED` — requires an external action/input that has not occurred.
- `PENDING` — a defined downstream validation/review has not run.
- `FAIL` / `REVIEW_REQUIRED` — hard negative/review states remain visible and are never averaged away.

## 4. Submission claim register

| Claim | Current state | Primary evidence | Submission-safe wording |
|---|---|---|---|
| exact 3×3 workflow mechanics | `PROVEN / MECHANICS_ONLY` | W004-T012 manifest; W003 E2E proof | exact nine-job mechanics executed in controlled clean CI |
| branch-local repair | `PROVEN` in controlled proof | W004-T012 manifest | persisted FAIL→repair→fresh re-eval→PASS with sibling immutability |
| source/factual/policy hard gates | `PROVEN` in controlled proof | W003/W004 release smoke | soft metrics do not compensate hard source/factual/policy failures |
| parser/source-trust behavior | `PROVEN` on current fixtures | W004-T003 result / parser artifacts | provenance-preserving reference passes; unsafe role/unit loss is non-PASS |
| parser implementation winner | `PENDING / UNLOCKED` | parser bakeoff | no implementation winner selected |
| audience thresholds | `DIAGNOSTIC_ONLY` | calibration gate | metrics exist; numeric thresholds are not calibrated/frozen |
| target→human matrix | `BLOCKED / PENDING` | human-calibration protocol | requires two genuine independent human streams |
| human→evaluator matrix | `BLOCKED / PENDING` | human-calibration protocol | requires valid human gold first |
| provider/model content quality | `PRODUCTION_UNKNOWN / BLOCKED` | provider manual path | no authorized observed provider quality evidence yet |
| provider latency/usage | `PRODUCTION_UNKNOWN / BLOCKED` | provider manual path | no authorized observed provider telemetry yet |
| provider commercial cost | `PRODUCTION_UNKNOWN / BLOCKED` | provider manual path | no observed usage + eligible official pricing evidence yet |
| provider/model preference | `NOT_AUTHORIZED` | evidence policy | no preference can be inferred from mechanics/demo evidence |
| clean task-specific smoke | `PASS` | Actions run 35605139400 | observed clean checkout executed smoke + focused test |
| final release / production readiness | `PENDING` | final fan-in not complete | no production-readiness claim |

## 5. Current observed clean-smoke provenance

W004-T012 persisted the following observed CI identity:

- workflow: `W004 T012 Release Smoke`;
- Actions run: `35605139400`;
- job: `106350276042`;
- execution head: `bd6e90021aa007be23de555d3751612372192a4b`;
- runner: Ubuntu 24.04.5 LTS;
- Python: 3.13.15;
- conclusion: `success`;
- focused test: `1 passed in 0.45s`;
- uploaded artifact ID: `10641632565`;
- artifact digest: `sha256:18e17939b212c6cb43a36d5a7d3298378c81792b9b0047b954324d760c5787f4`.

Observed acceptance-critical facts include exact 9/9 mechanics, persisted FAIL→PASS repair lineage, fresh hard-gate execution, accepted-sibling immutability, cockpit evidence markers and parser hard-gate behavior.

This CI run does not supply human calibration or real provider evidence.

## 6. Human calibration — required visible placeholders

### 6.1 Independent primary streams

- `PRIMARY_A`: `BLOCKED` until one genuine human independently annotates the complete frozen development bank.
- `PRIMARY_B`: `BLOCKED` until a second genuine human independently annotates the same blinded bank.
- operational independence must be genuine, not only two role labels from the same person/process.
- held-out sources remain forbidden for tuning/calibration.

### 6.2 Target → human confusion matrix

`STATUS: BLOCKED / PENDING`

```text
Do not populate from requested generation targets.
Expected future artifact: <T005_VALID_RESULT>/target_to_human_confusion.json
```

### 6.3 Human → evaluator confusion matrix

`STATUS: BLOCKED / PENDING`

```text
Requires valid human gold after the versioned agreement/adjudication protocol.
Expected future artifact: <T005_VALID_RESULT>/human_to_evaluator_confusion.json
```

### 6.4 Preparation artifacts

- `data/evals/w004/source_manifest_v001.json`
- `data/evals/w004/frozen_outputs_manifest_v001.json`
- `data/evals/w004/annotation_schema_v001.json`
- `data/evals/w004/annotation_plan_v001.json`
- `docs/evals/human_calibration/protocol_v001.md`
- `experiments/human_calibration/compute_agreement.py`
- `experiments/human_calibration/validate_preparation.py`

Current frozen development surface: 4 development sources × 3 formats × 3 target levels = 36 natural outputs. Two additional source identities are held out at source-document level.

## 7. Provider/model — required visible placeholders

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

## 8. Parser/source-trust packet

Primary references:

- `experiments/parser_w004/observed_results.json`
- `docs/parser_w004/README.md`
- `SYSTEM/RESULTS/W004-T003-A01.md`

Submission-safe facts:

- provenance-preserving reference: `PASS`;
- flat value-only behavior: `REVIEW_REQUIRED` even at 100% value coverage;
- wrong-role probe: `FAIL`;
- wrong-unit/table probe: `FAIL`;
- parser implementation: `UNLOCKED`.

Residual gap: same-raw-byte cross-parser comparison and OCR/scanned-document coverage remain pending.

## 9. Repair / telemetry / audit packet

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
- no aggregate green/readiness score is computed.

## 10. Reproduction commands

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

## 11. Blind-review status and open submission risks

The latest integrated blind/adversarial review is `NOT_PASS`. T015 addresses the missing consolidated report finding F-007, but the remaining findings must remain visible:

| Finding | Severity/posture | Packet status |
|---|---|---|
| F-001 final real demo video absent | CRITICAL | OPEN |
| F-002 recipient-facing raw PDF/text ingest not demonstrated | HIGH | OPEN |
| F-003 interactive app/dashboard adherence risk | HIGH | OPEN |
| F-004 central 3×3 proof is deterministic-stub mechanics | HIGH | CONTROLLED BY DISCLOSURE |
| F-005 independent human calibration absent | HIGH | BLOCKED / PENDING |
| F-006 real provider evidence absent | HIGH | BLOCKED / PRODUCTION_UNKNOWN |
| F-007 consolidated experimental report absent | HIGH | ADDRESSED BY `docs/report/EXPERIMENTAL_REPORT.md` |
| F-008 actual <=5:00 duration unverified | MEDIUM | OPEN |
| F-009 traceability wording scope | MEDIUM | ORCHESTRATOR FOLLOW-UP |
| F-010 submission logistics/owner/workflow unknown | MEDIUM | UNKNOWN / OPEN |

A final submission must not reinterpret T015 completion as blind-review PASS or release readiness.

## 12. Traceability anchors

The detailed canonical matrix remains `SYSTEM/TRACEABILITY_MATRIX.md`. Relevant anchors for this packet include:

- `PAIN-001..005` — audience complexity, nuance preservation, evaluator bias, auditability and trusted multichannel scale;
- `REQ-001..021` — source ingestion/trust, graph/state, 3×3 generation, audience/format/eval/repair/cockpit/report/reproducibility;
- `REQ-022..023` — final real video and measured <=5:00 compliance remain open;
- `CRIT-001` — hard factual/eliminatory requirements are non-compensating.

Assumption/risk context remains canonical in `SYSTEM/ASSUMPTION_RISK_REGISTER.md`, especially `A-0001`, `A-0002`, `A-0004`, `A-0006`, `A-0008`, `A-0011` and `RISK-0001..0006`, `RISK-0010..0011`, `RISK-0017`, `RISK-0019..0025` as applicable.

## 13. Final submission stop conditions

Do not claim final release/production readiness while any required item below remains unresolved:

1. two genuine independent human primary annotation streams are absent;
2. required pre-adjudication agreement/adjudication and observed confusion matrices are absent;
3. real authorized provider evidence sufficient for the intended comparison is absent;
4. any commercial cost claim lacks observed usage + eligible official pricing provenance;
5. semantic-ablation decision is required but not measured on valid human gold;
6. recipient-facing raw-ingest/interactive adherence requirements remain unproven under the final package interpretation;
7. final real video is absent or its exported duration is not observed <=5:00;
8. final clean fan-in/review has not produced the required release result.

## 14. Non-claims

This packet makes no claim that:

- audience thresholds are calibrated;
- the target label is human truth;
- a provider/model is superior or preferred;
- real provider latency/usage/cost has been measured;
- a parser implementation has won a same-byte bakeoff;
- deterministic-stub outputs demonstrate provider quality;
- the current read-only cockpit alone resolves the interactive recipient-app requirement;
- the system is production-ready or release-approved.

The submission packet is complete for its current purpose only when reviewers can distinguish what is observed, diagnostic, inferred, unknown, blocked and pending without consulting hidden assumptions.
