# Human calibration protocol v001 — W004

`PROTOCOL: w004-human-calibration-v001`  
`CORPUS_VERSION: w004-corpus-v001`  
`OUTPUT_VERSION: w004-natural-v001`  
`STATUS: READY_FOR_INDEPENDENT_ANNOTATION`  
`MODE: DIAGNOSTIC_ONLY`

## Purpose

Prepare an executable, independent human-calibration workflow for the frozen W004 development outputs without turning generation targets into gold and without exposing held-out sources to tuning.

This protocol inherits the audience rubric from `data/evals/gold/rubric_v001.json`, uses the W004-specific record schema in `data/evals/w004/annotation_schema_v001.json`, and freezes the operational plan in `data/evals/w004/annotation_plan_v001.json`.

## Frozen population

- split unit: `SOURCE_DOCUMENT`;
- development sources: 4;
- held-out sources: 2;
- development outputs: 36 = 4 sources × 3 formats × 3 requested audience targets;
- held-out outputs generated for this calibration: 0;
- annotator packet: `data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64`.

The six-source W004 corpus expands the three-source bootstrap but remains below the stronger 18-document design target. It is therefore sufficient to run independent calibration and measure agreement, but **not** sufficient by itself to justify a production threshold freeze.

## Non-circularity invariant

The workflow keeps three variables distinct:

```text
generation_target_level != human_gold_level != evaluator_predicted_level
```

The requested generation target is provenance only. It is hidden from primary annotators and is never copied into `human_gold_level`.

A human gold label may be promoted downstream only from independent annotations with recorded provenance and adjudication where required.

## Roles

Each development item is annotated by:

1. `PRIMARY_A` — independent first annotation;
2. `PRIMARY_B` — independent second annotation;
3. `ADJUDICATOR` — distinct role used only for triggered cases.

The protocol defines workflow roles, not actual people or Suno staffing assumptions.

## Blind packet contract

Primary annotators may receive only information needed to judge the output and its source evidence. The primary interface must not reveal:

- `generation_target_level` or an expected audience class;
- evaluator prediction, scores, thresholds or judge rationale;
- generator/model identity, generation method or prompt version;
- the other primary annotator's label or notes;
- any held-out item or tuning result derived from held-out material.

Opaque item identifiers may be shown. Source evidence needed for factual/material-preservation checks may be shown, but the source's split designation must not be used to imply an expected label.

## Annotation procedure

For every item, each primary independently records a valid `w004-annotation-record-v001` containing:

- global audience label: `BEGINNER | INTERMEDIATE | ADVANCED | UNSCORABLE`;
- D1–D5 ordinal rubric dimensions;
- `mixed_level_flag`;
- non-compensatory checks for factual critical preservation, material concept preservation and native format contract;
- confidence and notes;
- `unscorable_reason` when applicable.

The global audience label is a rubric-backed judgment, not a blind arithmetic average of D1–D5.

## Pre-adjudication agreement

Agreement is computed **before** adjudication with:

```bash
python experiments/human_calibration/compute_agreement.py \
  --a experiments/human_calibration/annotations_primary_a.jsonl \
  --b experiments/human_calibration/annotations_primary_b.jsonl \
  --out experiments/human_calibration/agreement_report.json
```

Required outputs:

- paired item count;
- raw agreement and disagreement rate;
- `UNSCORABLE` rate per annotator;
- Cohen's kappa across all paired labels when mathematically defined;
- quadratic weighted kappa on scorable ordinal pairs when mathematically defined;
- disagreement item IDs for adjudication queue construction.

Agreement metrics are evidence about rubric/data stability. A weak kappa or high adjudication burden is a finding; it must not be hidden by majority vote or threshold manipulation.

## Adjudication triggers

An item enters adjudication if any of these are true:

- primary audience labels differ;
- either primary uses `UNSCORABLE`;
- any non-compensatory check differs;
- either primary records `FAIL` or `REVIEW_REQUIRED` in a non-compensatory check.

The adjudicator may review both primary records and the same source/output evidence. The generation target remains forbidden as adjudication evidence.

The adjudicator records:

- the final rubric-backed audience judgment;
- D1–D5 dimensions;
- final non-compensatory checks;
- references to both primary annotation IDs;
- a written adjudication rationale.

## Gold promotion rule

No single primary record becomes gold automatically.

For later W004-T005 processing, a downstream `human_gold_level` may be materialized only when annotation provenance is reconstructable and the source is declared `BLIND_HUMAN_ADJUDICATION`. If the protocol cannot resolve an item defensibly, preserve `UNSCORABLE` instead of forcing a class.

## Held-out isolation

The two held-out source documents remain outside this calibration run. Their contents may exist in source provenance, but they must not be generated, annotated, scored for iterative error analysis, or used to tune prompts/features/weights/thresholds in W004-T002/T005.

Any held-out inspection that materially informs tuning contaminates the version. The correct response is a new versioned split, not silent reuse.

## Threshold policy

`threshold_freeze_allowed = false` for this preparation.

Reasons:

- no observed independent human agreement exists yet;
- the expanded W004 corpus has six source documents, not the stronger 18-document target;
- source-family coverage remains limited;
- no target→human or human→evaluator matrix has been observed on this corpus.

W004-T005 may compute those matrices and measure agreement. Thresholds remain `DIAGNOSTIC_ONLY` unless evidence is sufficient and the policy is explicitly versioned later.

## Required handoff to W004-T005

Before W004-T005 can claim human-calibration completion, it must persist:

1. complete primary A and primary B annotation files;
2. a pre-adjudication agreement report;
3. adjudication records for every triggered item;
4. target→human confusion matrix on development data;
5. human→evaluator confusion matrix on development data;
6. uncertainty/failure slices with sample counts;
7. explicit confirmation that held-out remained unexposed;
8. either evidence supporting a later threshold proposal or an explicit continued `DIAGNOSTIC_ONLY` disposition.

## Validation

Preparation invariants can be checked with:

```bash
python experiments/human_calibration/validate_preparation.py
```

The validator checks source-level split integrity, 36 frozen development outputs, absence of held-out generated items, absence of pre-populated human gold, artifact hashes, and forbidden-field leakage in the blinded packet.
