# Gold benchmark v001 — independent audience/evaluator calibration

`BENCHMARK_VERSION: gold-v001`  
`STATUS: DIAGNOSTIC_ONLY`  
`BASE_COMMIT_SHA: bd29959b081d8f70a40b420ab715f66ac5e59154`  
`ANNOTATION_SCHEMA: annotation-record-v001`  
`RUBRIC_VERSION: audience-gold-rubric-v001`

## Purpose

This benchmark establishes an independent, reproducible path for calibrating audience sophistication and the evaluator without circularly treating a requested generation target as human truth.

The benchmark is intentionally **diagnostic-only** at v001. The repository currently contains three accepted primary-source fixtures and no independent human annotations/agreement. No audience threshold, classifier cutoff, judge prompt threshold or release floor may be frozen from this version alone.

## Evidence base

The design reconciles the accepted findings in:

- `SYSTEM/RESULTS/W001-T002-A01.md` — multidimensional PT-BR audience complexity; Flesch is a sensor, not a level oracle;
- `SYSTEM/RESULTS/W001-T005-A01.md` — source-document split, blind human gold, agreement/adjudication and held-out isolation;
- `SYSTEM/RESULTS/W001-T009-A01.md` — non-compensatory Hybrid Evaluator hierarchy;
- `SYSTEM/RESULTS/W002-T010-A01.md` — B11 as the next calibration bottleneck and explicit leakage/instability kill criteria.

Only already accepted public primary-source fixtures are used. No Suno-internal labels, annotators, workflow roles or partner ground truth are invented.

## Benchmark population

`data/evals/gold/benchmark_manifest_v001.json` freezes the current source identities and expected evaluation grid.

Current accepted source documents:

1. `copom_277_2026_03` — `COPOM_POLICY`;
2. `petrobras_2t26_results` — `EARNINGS_RESULTS`;
3. `petrobras_capex_fato_relevante_2024_08_08` — `ISSUER_MATERIAL_DISCLOSURE`.

Each source defines an expected `3 audience levels × 3 native formats = 9` item grid:

- audiences: `BEGINNER`, `INTERMEDIATE`, `ADVANCED`;
- formats: `ARTICLE`, `CAROUSEL`, `SHORT_VIDEO`.

Therefore v001 expects 27 future output items once generated and frozen. The manifest does **not** pretend those outputs or human labels already exist.

## Source-document split and held-out isolation

The split unit is the **source document**, never an individual output. All nine variants derived from one source must remain in the same split.

For this three-source diagnostic bootstrap, assignment is deterministic:

```text
split_key = SHA256("gold-v001" + source_id)
```

The lowest key is held out globally; the other two sources are development:

- `HELD_OUT`: `petrobras_capex_fato_relevante_2024_08_08`;
- `DEVELOPMENT`: `petrobras_2t26_results`;
- `DEVELOPMENT`: `copom_277_2026_03`.

This bootstrap is **not** the final statistically useful split proposed in W001-T005. With an expanded corpus, a new benchmark version should move toward the planned family-stratified design (nominally 18 documents: 12 development and 6 held-out, 4/2 per family where evidence supports those families).

### Held-out discipline

Held-out material is forbidden from:

- feature selection;
- threshold or weight tuning;
- prompt/judge tuning;
- iterative error analysis;
- daily regression CI;
- relabeling motivated by evaluator disagreement.

Held-out use is limited to a declared release/final evaluation after the development policy is frozen. Any premature manual inspection that materially informs tuning contaminates the version and requires a new versioned split.

## Anti-circularity contract

Three variables remain distinct throughout the lifecycle:

```text
generation_target_level != human_gold_level != evaluator_predicted_level
```

`generation_target_level` answers what was requested. `human_gold_level` records what independent blinded annotators perceive under the rubric. `evaluator_predicted_level` is the model/evaluator output being calibrated.

The annotation schema therefore excludes from the annotator payload:

- generation target;
- evaluator prediction/scores;
- generator model identity;
- prompt version;
- expected label;
- other annotators' labels before independent submission.

A requested target can never be promoted automatically to gold. `gold_labels` remain empty until human workflow evidence exists.

## Annotation rubric

`data/evals/gold/rubric_v001.json` versions five audience dimensions:

1. `D1_JARGON_CONTEXTUALIZATION`;
2. `D2_BACKGROUND_ASSUMED`;
3. `D3_CONCEPTUAL_DEPTH`;
4. `D4_CONTENT_FOCUS`;
5. `D5_TECHNICITY_PRESERVATION`.

The global label is `BEGINNER | INTERMEDIATE | ADVANCED | UNSCORABLE`. It is a rubric-backed judgment, not a blind arithmetic average of dimensions. `mixed_level_flag=true` records material conflicts; `UNSCORABLE` avoids forcing truncated/incoherent/mixed outputs into a false class.

Audience fit cannot compensate for loss of truth. The rubric separately records three non-compensatory checks:

- factual critical preservation;
- material concept preservation;
- native format contract, when applicable.

Canonical format code/tests remain the source of truth for structural Article/Carousel/ShortVideo checks.

## Independent annotation and review workflow

1. **Freeze identity.** Freeze benchmark version, source identity/hash metadata, output bytes/text hash, format and opaque `item_id` before annotation.
2. **Prepare blind packet.** Provide only the source/evidence required to judge the item plus the output under review. Strip target, evaluator result, generator identity/prompt and peer labels.
3. **Primary A.** `PRIMARY_A` submits a complete `annotation-record-v001` independently.
4. **Primary B.** `PRIMARY_B` independently submits the same schema without seeing A.
5. **Agreement report.** Before adjudication, report raw agreement, disagreement rate, `UNSCORABLE` rate and Cohen's kappa when mathematically applicable. Ordinal weighted agreement may be added only if predeclared/versioned. Report slices only when sample size supports interpretation.
6. **Adjudication.** A distinct `ADJUDICATOR` reviews disagreements, `UNSCORABLE` cases requiring resolution, or non-compensatory check disagreements; rationale is persisted. The generation target is not evidence during adjudication.
7. **Gold promotion.** A final `human_gold_level` may enter the manifest/data layer only with annotation IDs and `gold_label_source=BLIND_HUMAN_ADJUDICATION`. A single model/requested label never qualifies.
8. **Development calibration.** Features, weights, thresholds and evaluator policy are tuned only on development gold.
9. **Freeze before held-out.** Evaluator/rubric versions and operational thresholds are frozen before any held-out scoring used as release evidence.

The protocol defines roles, not actual people or partner staffing.

## Agreement and threshold policy

No universal numeric agreement threshold is invented here. Agreement is evidence to assess whether the rubric/dataset supports calibration; a weak or unstable result is a finding, not something to hide with majority vote.

For v001:

```text
threshold_policy.freeze_allowed = false
threshold_policy.mode = DIAGNOSTIC_ONLY
```

Reasons:

- only three source documents;
- one document per current family;
- no independent human annotation yet;
- no measured agreement/adjudication rate;
- no natural generated 3×3 corpus frozen yet.

Thresholds remain diagnostic until an expanded development sample and reproducible agreement justify a versioned freeze.

## Kill criteria / invalidation rules

The benchmark version must not support calibration/release claims if any of these occur:

- variants from one source cross development/held-out splits;
- held-out evidence informs tuning or iterative prompt/error analysis;
- requested target is copied into human gold;
- annotators see evaluator scores/predictions, expected label or peer labels before independent submission;
- a single annotation is silently promoted to gold;
- source/output identity or annotation provenance cannot be reconstructed;
- rubric/schema changes occur without a version bump;
- agreement remains unstable/non-reproducible after rubric review;
- sample/slice imbalance makes a claimed threshold unsupported;
- factual/material-concept failures are compensated by readability/audience scores.

When instability or sample insufficiency applies, the correct disposition is `DIAGNOSTIC_ONLY`, not a fabricated cutoff.

## Reproduction

From repository root:

```bash
python experiments/gold/validate_benchmark.py
```

The validator checks split-unit invariants, the canonical 3×3 grid, deterministic split keys, held-out tuning prohibition, fixture provenance consistency, anti-circular annotation fields, human-gold promotion requirements and threshold-freeze posture.

## Version lifecycle

Once real annotations start against `gold-v001`, semantic changes to sources, split policy, schema or rubric require a new benchmark version. New documents may be accumulated in a successor version; do not silently mutate held-out membership after observing evaluator behavior.
