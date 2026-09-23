# W006-T010 evaluation / human-calibration foundation

This directory is the executable foundation for `W006-T010-A01`. It consumes the accepted W005 evaluation-science design and the W006 T001/T004 boundaries without claiming unavailable human evidence.

## What is materialized

- `data/evals/production/w006/partition_manifest_v001.json` — versioned `DEV / CALIBRATION / HELD_OUT` membership at **source-group** granularity. Nine 3×3 siblings and parser/OCR derivatives never increase independent source `N`.
- `data/evals/production/w006/human_annotation_record_schema_v001.json` — blind independent-primary/adjudication record contract. Human evidence classes exclude model-only labels.
- `data/evals/production/w006/judge_calibration_contract_v001.json` — secondary judge calibration gate; human reference is mandatory before promotion.
- `data/evals/production/w006/paired_experiment_contract_v001.json` — exact baseline/candidate pairing, source-group clustering and non-compensatory hard-gate rules.
- `data/evals/production/w006/evaluator_config_v001.json` — versioned hybrid evaluator foundation with audience thresholds explicitly `DIAGNOSTIC_ONLY`.
- `foundation_status_v001.json` — explicit evidence-status boundary.
- `validate_foundation.py` — standard-library validator and protocol fixtures.
- `validation_report.json` — observed validation output.

The detailed collection/adjudication protocol and annotator form live in `docs/evals/human_calibration/foundation_w006_v001.md` and `docs/evals/human_calibration/annotation_form_w006_v001.md`.

## Validate

```bash
python experiments/eval_foundation_w006/validate_foundation.py
python -m unittest tests/evals/test_eval_foundation_w006.py
```

The validator must report `model_only_human_gold_acceptances = 0`, `hard_gate_compensation_paths = 0`, `audience_threshold_status = DIAGNOSTIC_ONLY`, and `held_out_replication_status = NOT_RUN`.

## Evidence boundary

This task does **not** contain independent human annotations. `PRIMARY_A`, `PRIMARY_B`, agreement/adjudication metrics, human confusion matrices, calibrated model-judge performance and HELD_OUT replication remain external empirical work. Synthetic protocol fixtures in the validator exercise rejection/identity semantics only and are never called human gold.

W006-T004's `NO_PRODUCTION_PARSER_WINNER` is preserved. Parser selection is not part of this task.
