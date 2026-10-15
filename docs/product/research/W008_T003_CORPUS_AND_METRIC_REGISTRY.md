# W008-T003 — Corpus, metrics and evidence registry v1

**Task:** W008-T003-A01 (EP-03), **preregistered before any new financial-model benchmark**  
**Registry:** `experiments/corpus_w008/registry.v1.json`  
**Validator:** `experiments/corpus_w008/validate_registry.py`  
**Status:** `DESIGN_FROZEN / NEW_FINANCIAL_EVAL_NOT_RUN`

## What exists and what does not

The registry contains **four source-family entries**: three historically collected, SHA-256-stamped source-original PDFs in accepted W007-T004 parser research (Petrobras, BCB, FRASER), plus one explicitly missing **CVM** primary original. These are **NOT** four current verified finance source originals for W008; there was no new provider or PDF evaluation. There is no evidence of a pure image-only primary financial source original.

The 13 adversarial rows map to existing **synthetic-only** `tests/factual/observed_factual_v001.jsonl` failure-code controls, not to verified statements from source-original PDFs. Each remains `SYNTHETIC_EXISTING_FIXTURE` and cannot count toward a source-grounded factuality denominator or human/AI agreement.

Source group IDs, source URLs, prior exact hashes and reasons for missingness live in the JSON; a planning manifest is not a new official PDF acquisition or a license grant. The preserved original record is `SYSTEM/RESULTS/W007-T004-A01.md`, along with its underlying `artifacts/w007-t004/a01/raw-evidence.json`. W008-T002 found the flat `PdfExtraction` → `IngestResult` table-cell transport gap; the test plan does not bypass the production trust gate to grade flat table text as authoritative cell gold.

## Metric registry (nine frozen dimensions)

| ID | Unit | Source-group metric definition | Eligibility / missingness |
|---|---|---|---|
| critical_false_accept_count | count ↓ | Materially contradicted source facts incorrectly accepted | Needs verified originals and controlled source-grounded claim counter; not derivable from 13 synthetic tests |
| false_support_rate | fraction ↓ | Unsupported marked-supported / admissible audited claims | Unknown denominator pending legitimate source-grounded attribution |
| numeric_period_unit_preservation | fraction ↑ | Source numeric-unit-period relations preserved / verified source relations | Need cell/row/column provenance; no fabricated table gold |
| cross_output_claim_contradictions | count ↓ | Contradictions across complete nine outputs sharing exact claim, time and qualifier | Nine **actual generated outputs** needed |
| provenance_traceability | fraction ↑ | Resolvable material claims / all audited claims | Source hashes/typed span-cell locators required |
| audience_diagnostic | rubric_measure ↑ | Blind independent AI-based PT-BR clarity/technicality diagnostic | NOT_RUN; no human comprehension, no calibrated threshold |
| latency_p95 | milliseconds ↓ | p95 wall-clock latency across comparable repeated workload | NOT_RUN; no timing inferred from source-inventory |
| cost_total | USD ↓ | Provider + infra + processing costs under workload | NOT_RUN; free grant does not establish zero total cost |
| recovery_integrity | count ↓ | Lost/duplicated branch/event identities on controlled restart/retry | NOT_RUN; staging boot is not durability |

Every metric must have named source, evidence class, measurement unit, clear denominator/estimator and missingness. After actual trials start, raw rows should be under separate versioned non-public controlled artifacts for sensitive content; no raw user content or secrets should be committed to a public repo.

**Zero new measured metric values** is the correct record for this task. `summary_statistics=null`, `confidence_intervals=null`, `point_pareto=null`; no universal weighted scalar is permitted by accepted W005-T009-A02 until business utility and sensitivity evidence exist.

## Preventing leakage in research and implementation

- Source-group key (primary document or event) defines train/calibration/held-out unit; different byte versions of a source event must share its group. Nine branches from the same run are not nine independent samples.
- Frozen W009 split algorithm `sha256_prefix12_mod100` with salt `w009-preregistered-split-policy-v1`: DEV 60%, CALIBRATION 20%, HELD_OUT 20% **allocation policy**. Percentages are bucket assignments, not empirical achieved coverage.
- `experiments/corpus_w008/validate_registry.py` verifies parity to the integrated W009 harness, explicit CVM missingness, exact source hashes and W007 evidence ref, 13 control/oracle mapping, four candidate IDs, nine dimension IDs and impossibility of silently filling Pareto/statistics.
- Changing split salt or inventing alternate `source_group_id` to get a desired held-out result is forbidden. No synthetic fixture labeled `SOURCE_ORIGINAL`, `HUMAN_GOLD` or `PROVIDER_OBSERVED` without the respective independent raw evidence.
- Sampling sufficiency and group balance remain unknown with only three historical originals. A split with zero observed held-out or calibration groups is valid as a **manifest report**, but invalid for meaningful out-of-sample candidate comparison.

## Failure taxonomy

Reuses the actual accepted factual oracle codes:
`FACT_NUMERIC_MAGNITUDE_MISMATCH`, `FACT_SCALE_UNIT_MISMATCH`, `FACT_PERIOD_MISMATCH`, `FACT_ENTITY_ROLE_SWAP`, `FACT_DIRECTION_MISMATCH`, `FACT_NEGATION_INVERSION`, `FACT_MODALITY_PROMOTION`, `FACT_ATTRIBUTION_ERROR`, `FACT_TABLE_ROLE_MISMATCH`, `FACT_UNSUPPORTED_CAUSAL_CLAIM`, `FACT_SOURCE_EXTRACTION_AMBIGUOUS`, `FACT_RETRIEVAL_MISS_REVIEW`, plus clean `EXP-C-C01`.

Synthetic seeds support regression tests of code behavior, not precision/recall against real readers or financial documents. Critical source/factual/policy/schema/tenant/provenance failure means infeasible candidate, regardless of possible higher rubric scores. Unknown/ambiguous evidence means REVIEW, not implicit acceptance.

## Evidence and next executable step

```bash
python experiments/corpus_w008/validate_registry.py --output /tmp/w008-corpus-registry-validation.json
PYTHONPATH=src python -m unittest discover -s tests/corpus_w008 -p 'test_*.py' -v
```

When original CVM, a genuine image-only financial source and source-original per-claim benchmark are available, acquire bytes with rights/quarantine/hash, preregister strict sample inclusion rules, run the same four candidate methods, persist source-group paired raw observations, compare only eligible measured dimensions. Operator explicitly chose AI-only; do not hire human annotators or mark automated judges as human evidence. Any future external model-judge use requires legitimate independently versioned configured model and trace/cost evidence.

**Promotions prohibited now:** PROD-008 human thresholds, M04 audience validity, provider winner, parser default, M05 complete cross-output guarantee, production readiness. Current DRG outcome `PENDING_EVIDENCE`.

