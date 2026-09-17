# W004 human calibration execution

This directory is the execution handoff from W004-T002 to W004-T005.

## Inputs

- `data/evals/w004/source_manifest_v001.json`
- `data/evals/w004/frozen_outputs_manifest_v001.json`
- `data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64`
- `data/evals/w004/annotation_schema_v001.json`
- `data/evals/w004/annotation_plan_v001.json`
- `data/evals/gold/rubric_v001.json`
- `docs/evals/human_calibration/protocol_v001.md`

## 1. Validate preparation

```bash
python experiments/human_calibration/validate_preparation.py
```

Expected posture:

- 4 development source documents;
- 2 held-out source documents;
- 36 frozen development outputs;
- 36 blind items;
- zero held-out generated outputs;
- zero pre-populated human-gold labels;
- no forbidden target/evaluator/generator fields in the blind bank;
- threshold freeze remains disabled.

## 2. Collect independent primaries

Materialize annotation records conforming to `w004-annotation-record-v001` as:

```text
experiments/human_calibration/annotations_primary_a.jsonl
experiments/human_calibration/annotations_primary_b.jsonl
```

Do not commit a primary file until the corresponding annotator has completed it independently. PRIMARY_A must not see PRIMARY_B and vice versa before both submissions are frozen.

## 3. Compute agreement before adjudication

```bash
python experiments/human_calibration/compute_agreement.py \
  --a experiments/human_calibration/annotations_primary_a.jsonl \
  --b experiments/human_calibration/annotations_primary_b.jsonl \
  --out experiments/human_calibration/agreement_report.json
```

The report includes the adjudication queue and does not authorize threshold freeze.

## 4. Adjudicate triggered items

A distinct `ADJUDICATOR` reviews every queued item and writes:

```text
experiments/human_calibration/annotations_adjudicated.jsonl
```

Adjudication records must reference both primary annotation IDs and provide a rationale. The requested generation target is not admissible evidence.

## 5. W004-T005 outputs

W004-T005 should then construct development-only:

- target → human confusion matrix;
- human → evaluator confusion matrix;
- agreement/adjudication metrics;
- format/source/level slices with explicit sample counts;
- uncertainty and failure analysis;
- an explicit decision to remain `DIAGNOSTIC_ONLY` unless evidence is sufficient for a separately versioned threshold proposal.

Held-out remains untouched until a later declared release evaluation after tuning policy is frozen.
