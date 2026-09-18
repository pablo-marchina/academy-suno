# Release Evidence Packet — skeleton for W004 fan-in

This packet is a **release-preparation shell**, not a release approval. W004-T011 may populate reproducible mechanics/cockpit/parser evidence, but final release proof remains owned by W004-T008 after its human/provider/semantic dependencies are valid.

## 1. Evidence-state legend

- `PROVEN`: observed and reproducible inside the explicitly named scope.
- `DIAGNOSTIC_ONLY`: useful signal, not sufficient for calibration/freeze/selection.
- `PRODUCTION_UNKNOWN`: no valid real-production/provider observation supports the claim.
- `BLOCKED`: evidence acquisition requires an external action that has not happened.
- `PENDING`: downstream evidence/review has not yet been executed.

Never collapse these states into a single readiness percentage or green badge.

## 2. Claim register

| Claim | Current posture | Evidence / location | What is still required |
|---|---|---|---|
| source→9 jobs→eval→repair→aggregate mechanics | `PROVEN` within `MECHANICS_ONLY` | `experiments/w003_e2e/run_proof.py`; release smoke proof report | preserve clean-checkout execution in final T008 |
| persisted FAIL→repair→PASS lineage | `PROVEN` within controlled proof | `proof_report_v001.json#repair_lineage`; cockpit repair panel | final T008 references exact hashes/artifact |
| hard source/factual/policy non-compensation | `PROVEN` within controlled proof | `proof_report_v001.json#non_compensation_probe` | no weakening in final gate |
| evidence cockpit provenance/unknown visibility | `PROVEN` for rendering mechanics | `app/evidence_cockpit.py`; `docs/cockpit/README.md` | final T008 uses same evidence, not a parallel truth store |
| parser/source-trust behavior over W004 fixtures | `PROVEN` for current fixture contract | `experiments/parser_w004/*` | same-raw-byte candidate comparison/OCR remains `PENDING` |
| numeric audience thresholds | `DIAGNOSTIC_ONLY` | calibration evidence has no valid independent agreement | two independent human streams + agreement/adjudication |
| target→human confusion matrix | `BLOCKED` / `PENDING` | **PLACEHOLDER:** `<T005_VALID_RESULT>/target_to_human_confusion.json` | valid human gold only; requested target cannot substitute |
| human→evaluator confusion matrix | `BLOCKED` / `PENDING` | **PLACEHOLDER:** `<T005_VALID_RESULT>/human_to_evaluator_confusion.json` | valid human gold only |
| provider/model quality | `PRODUCTION_UNKNOWN` / `BLOCKED` | **PLACEHOLDER:** `<T007_VALID_RESULT>/quality.json` | authorized observed provider/model executions + valid quality evidence |
| provider latency/usage | `PRODUCTION_UNKNOWN` / `BLOCKED` | **PLACEHOLDER:** `<T007_VALID_RESULT>/telemetry.json` | observed real runs with provider/model/version provenance |
| provider commercial cost | `PRODUCTION_UNKNOWN` / `BLOCKED` | **PLACEHOLDER:** `<T007_VALID_RESULT>/cost.json` | observed usage + eligible official pricing provenance |
| semantic backend value | `PENDING` | **PLACEHOLDER:** `<T006_VALID_RESULT>/ablation.json` | same valid development human gold, on/off comparison |
| production/release readiness | `PENDING` | **PLACEHOLDER:** `SYSTEM/RESULTS/W004-T008-*.md` | clean E2E fan-in + final review |

## 3. Reproduce current non-external evidence

```bash
python scripts/release_smoke/run_release_smoke.py \
  --workdir /tmp/academy-suno-release-smoke \
  --output /tmp/academy-suno-release-smoke/manifest.json
```

Expected current posture:

```text
mechanics_end_to_end              PROVEN
audience_thresholds               DIAGNOSTIC_ONLY
human_confusion_matrices          BLOCKED/PENDING
real_provider_quality_latency_cost PRODUCTION_UNKNOWN/BLOCKED
parser_implementation             PENDING/UNLOCKED
production_release_readiness      PENDING_W004_T008
```

## 4. Provenance record

For every evidence item promoted into the final packet, record:

| Field | Required value |
|---|---|
| source/document id + canonical reference | exact persisted value; never inferred |
| source hash/raw-byte hash | exact value when observed; `UNKNOWN` when unavailable |
| run id | exact run |
| job id | exact branch/job |
| attempt | exact operation/repair attempt when available |
| evidence scope | e.g. `MECHANICS_ONLY`; never omitted when it changes interpretation |
| artifact path | immutable/versioned path or commit ref |
| observed timestamp | persisted timestamp if the source artifact provides it |
| provider/model/version | mandatory for any real-provider evidence |
| pricing provenance | mandatory before any real cost claim |

Unknown fields stay unknown; they are not backfilled from adjacent artifacts.

## 5. Human-calibration placeholders

### Independent annotation completeness

- PRIMARY_A: `BLOCKED` until a genuine independent human completes all 36 development items.
- PRIMARY_B: `BLOCKED` until a second genuine independent human completes all 36 development items.
- held-out: must remain inaccessible during tuning/calibration.
- pre-adjudication agreement: `PENDING`.
- adjudication: `PENDING`.

### Confusion matrices

**Target → human**

```text
PENDING — do not fill from requested target labels.
artifact: <T005_VALID_RESULT>/target_to_human_confusion.json
```

**Human → evaluator**

```text
PENDING — requires valid adjudicated/defined human gold.
artifact: <T005_VALID_RESULT>/human_to_evaluator_confusion.json
```

## 6. Provider quality / latency / cost placeholders

```text
quality: PRODUCTION_UNKNOWN
latency: PRODUCTION_UNKNOWN
usage: PRODUCTION_UNKNOWN
cost: PRODUCTION_UNKNOWN
provider preference: NOT AUTHORIZED
```

A provider harness, synthetic pricing, missing credential or manual path preparation does not satisfy these rows.

## 7. Final T008 insertion points

W004-T008 should add, without rewriting historical evidence:

1. exact clean-checkout release-smoke/CI run identifiers;
2. exact valid T005 human-calibration result and matrices;
3. exact T006 semantic-ablation result;
4. exact T007 provider/model comparable evidence;
5. regression/failure audit and terminal states;
6. final review sign-off;
7. a release conclusion that remains negative/pending if any required evidence is still `BLOCKED`, `PENDING` or `PRODUCTION_UNKNOWN`.

## 8. Non-claims carried by this packet

- No calibrated audience-threshold claim.
- No provider/model quality or preference claim.
- No real provider-cost claim.
- No production-readiness claim.
