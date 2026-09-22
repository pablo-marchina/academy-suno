# Production evaluation protocol v001 — W005

`PROTOCOL_ID: suno-production-eval-v001`  
`TASK: W005-T005-A01`  
`STATUS: EXECUTABLE_DESIGN`  
`THRESHOLD_STATUS: DIAGNOSTIC_ONLY_UNTIL_HUMAN_CALIBRATION`  
`EVIDENCE_BOUNDARY: D-0017 automated blind calibration is historical W004 evidence only`

## 1. Purpose

Define an executable evaluation-science contract for the production Academy Suno system. This protocol implements `PROD-007`, `PROD-008`, and `PROD-009` without converting model-generated labels into human gold and without inventing audience/quality pass thresholds.

The protocol separates deterministic safety/factual invariants, automated quantitative sensors, calibrated model-judge sensors, independent human evidence, offline experiments, CI regression gates, and online drift monitoring. Critical factual/source/policy failures remain visible and non-compensatory.

## 2. Evidence classes

Every observation MUST declare one evidence class:

| Evidence class | Meaning | Allowed use |
|---|---|---|
| `MACHINE_DETERMINISTIC` | Programmatic invariant/check with versioned implementation | Hard gates and reproducible metrics when the check itself is valid for the property |
| `MODEL_AUTOMATED_BLIND_CALIBRATION` | Blind model-based/automated evidence such as W004 A03 | Diagnostic evidence; never human gold |
| `MODEL_JUDGE_CALIBRATED` | Structured model judge whose prompt/model/version has been calibrated against independent human evidence | Secondary scalable sensor; never overrides critical hard gates |
| `HUMAN_INDEPENDENT_CALIBRATION` | Independent blind human streams with provenance and pre-adjudication agreement | May support audience calibration/threshold proposals when coverage and uncertainty are sufficient |
| `HUMAN_ADJUDICATED_GOLD` | Final human label after protocol-defined adjudication | Reference label for calibration/held-out analysis, with disagreement history retained |
| `ONLINE_OBSERVED` | Production telemetry/feedback with deployment provenance | Drift/monitoring and DEV corpus expansion; not automatically gold |

Evidence classes never silently upgrade. A derived artifact MUST retain the weakest materially relevant provenance needed to interpret its claim.

## 3. Evaluation unit and slice identity

The atomic evaluation row is a generated branch bound to:

`source_document_id × source_version × audience × format × system_version × run_id`.

For baseline-vs-candidate experiments, rows are paired by the same frozen source and requested branch identity. Corpus manifests MUST retain these slice dimensions at minimum:

- source/document family and document identity;
- audience: `BEGINNER | INTERMEDIATE | ADVANCED`;
- format: `ARTICLE | INSTAGRAM | VIDEO_SCRIPT` (or the versioned production format enum);
- source-language / output-language where applicable;
- parser/extractor version;
- generator provider/model/prompt/config version;
- evaluator configuration version;
- source risk flags (tables, dense numerics, dates, named entities, required concepts);
- split and near-duplicate cluster identity.

Do not hard-code a source-family distribution before a corpus census. Representation targets are versioned after the observed production/source population and critical risk slices are documented.

## 4. DEV / CALIBRATION / HELD-OUT separation

### 4.1 Grouped split invariant

The split unit is the source-document group, not an individual generated output. All audience/format variants of a source, and all near-duplicate/source-family derivatives capable of leaking content, travel together.

- `DEV`: prompt/evaluator/parser development, error analysis, feature work, rubric iteration.
- `CALIBRATION`: fit/tune model-judge prompts, diagnostic thresholds, weights, mappings and calibration models after the design is frozen.
- `HELD_OUT`: release evidence only. It MUST NOT drive tuning.

A held-out source inspected in a way that materially changes prompts, evaluator logic, thresholds, rubrics or model selection is contaminated. It is reclassified to DEV and a new versioned held-out set is selected before any release claim.

### 4.2 Versioning

Each corpus release has a manifest hash plus immutable identifiers for source hashes, split assignment and near-duplicate group. Changing membership or labels creates a new corpus version; it never rewrites the meaning of an old version.

## 5. Representative corpus expansion

Use a staged evidence plan rather than a fixed arbitrary count.

1. **Census** — map observed source families, document lengths/structures, numeric/entity/date density, audience/format branches, and known failure modes from W004 and production-like traffic.
2. **Coverage pilot** — include every critical risk/slice class needed to discover annotation problems and estimate variance/error rates. Pilot rows are DEV/CALIBRATION, never retroactively HELD_OUT.
3. **Precision planning** — use pilot variance/rates to calculate the additional sample required for the declared uncertainty objective.
4. **Calibration collection** — collect independent human labels on the frozen CALIBRATION manifest.
5. **Held-out replication** — evaluate a separately frozen HELD_OUT manifest after evaluator/threshold choices are locked.
6. **Production refresh** — sample new production-like cases into DEV; rotate future held-out versions when distribution or system behavior changes.

### 5.1 Sample-size rationale

No universal `n` is encoded here. Before collection, an experiment record MUST declare the estimand and required precision or minimum detectable effect.

For a Bernoulli failure/pass rate, a planning approximation may use:

`n ≈ z_(1-α/2)^2 * p * (1-p) / e^2`

where `p` comes from a pilot (or `0.5` only as a conservative variance assumption), and `e` is the desired half-width. Final reporting uses an interval suitable for finite samples (for example Wilson), not the Wald approximation.

For paired baseline-vs-candidate metrics, determine sample size/power from the observed paired-difference distribution (or a justified simulation), the predeclared smallest material effect/non-inferiority margin, alpha, and desired power. Cluster by source document so nine correlated 3×3 outputs do not masquerade as nine independent documents.

If those inputs are unknown, the status is `PENDING_EVIDENCE`; do not fabricate a sample count or threshold.

## 6. Human annotation and adjudication

### 6.1 Independence

Production audience-threshold evidence uses at least two independent primary streams per item unless an alternative protocol has a documented research justification and equivalent independence evidence.

Primary annotators MUST NOT see:

- generation target audience as an expected answer;
- evaluator/model-judge predictions, scores, thresholds or rationale;
- system/model/prompt identity or baseline/candidate identity;
- the other primary annotation;
- held-out tuning analyses.

Annotators may see source evidence required for factual/material-preservation judgments. Item order is randomized. For pairwise candidate judgments, left/right presentation is randomized and the mapping is hidden.

A person must not populate both independent primary streams for the same item. Training examples and rubric qualification are separated from scored packets.

### 6.2 Annotation payload

Each primary record contains:

- opaque item/packet ID and annotation schema version;
- pseudonymous annotator/stream ID;
- rubric version and training/qualification version;
- packet/source/output hashes;
- global audience label plus criterion-level ordinal judgments;
- factual, numeric, entity, date, material-concept and format-contract checks;
- confidence and `UNSCORABLE`/reason when needed;
- annotation timestamp and tool version;
- free-text evidence note constrained to the displayed source/output.

The generation target remains provenance, not human gold.

### 6.3 Pre-adjudication agreement

Agreement is always computed before adjudication and never overwritten.

Report:

- paired item count and missingness;
- raw agreement and confusion matrix;
- `UNSCORABLE` rate by stream;
- Cohen's kappa for two-stream nominal/global labels when defined;
- quadratic weighted kappa for ordered labels when defined;
- Krippendorff's alpha (appropriate measurement level) when there are more than two raters, missing ratings, or a study design requiring it;
- criterion-level disagreement and disagreement slices;
- clustered bootstrap confidence intervals by source document for agreement estimates when feasible.

Do not treat a high agreement coefficient as proof of validity, nor a low coefficient as something to hide. Disagreement may expose ambiguous rubric language, genuinely subjective cases, insufficient expertise or poor task design.

### 6.4 Adjudication

Adjudication is triggered by any primary disagreement on the global audience label, `UNSCORABLE`, or a non-compensatory check, and may be triggered for predefined high-risk slices.

The adjudicator receives both primary records only after they are frozen, plus the same source/output evidence. The hidden generation target, evaluator score and candidate identity remain excluded as decision evidence. The adjudication artifact links both primaries and preserves the disagreement reason.

No unresolved item is forced into gold. Preserve `UNSCORABLE`/`UNRESOLVED` when evidence is insufficient.

## 7. Metric families

### 7.1 Non-compensatory hard gates

Critical failures are reported as counts/rates and item IDs, never averaged away:

- unsupported or materially altered factual claims;
- numeric/value/unit/sign errors;
- entity/date identity errors that change meaning;
- material required-concept loss or contradiction;
- source/provenance binding failure;
- policy/compliance failure;
- critical schema/branch/format-contract violation when promotion would be unsafe.

For release comparison, a new critical hard-gate regression is a release block. Its tolerance is exactly zero under the Production Contract where the invariant applies.

### 7.2 Quantitative/diagnostic metrics

Report per slice and overall with units/config version:

- PT-BR readability distribution;
- jargon/term density and contextualization;
- concept, numeric, entity and date preservation;
- native format-contract metrics;
- audience evaluator confusion matrix against adjudicated human labels;
- calibration error / class-conditional precision and recall when probabilities or class predictions are exposed;
- latency/cost/retry only as experiment context, not substitutes for quality.

Target→human confusion is a useful diagnostic of generation controllability. Human→evaluator confusion measures the evaluator. Neither becomes human evidence if the human side is absent.

### 7.3 Model-judge sensors

Model judges are secondary evidence. Every judge record includes provider/model snapshot, prompt/rubric hash, temperature/sampling config, input hash, output, rationale/structured fields, latency/cost, and retry count.

Before a judge can be used for release evidence:

1. calibrate it against independent human labels on CALIBRATION;
2. measure agreement/error by audience, format and source-risk slices;
3. run order/position swap checks for pairwise tasks;
4. measure repeated-run stability where sampling or provider nondeterminism exists;
5. freeze judge prompt/model/config before HELD_OUT;
6. preserve deterministic hard gates outside the judge.

Any framework's built-in default score threshold is ignored unless independently justified for this corpus.

## 8. Baseline-vs-candidate offline experiment

Every material prompt/model/generator/evaluator/parser/runtime change gets an experiment manifest before results are inspected.

Required design:

1. freeze dataset/corpus version and split;
2. declare baseline and candidate system/config hashes;
3. declare primary metrics, critical gates, exploratory metrics, smallest material effect or non-inferiority margin where known;
4. run baseline and candidate on the same source groups and branch identities;
5. retain raw outputs and evaluator artifacts for both arms;
6. pair comparisons by source/branch; cluster uncertainty by source document;
7. report aggregate and all predeclared slices, including sample counts;
8. do not tune on HELD_OUT after seeing results;
9. persist experiment metadata and artifact hashes.

### 8.1 Statistical reporting

Normalize metric direction so positive paired delta means candidate improvement when useful.

For each primary metric report:

- baseline and candidate point estimates;
- paired delta/effect size;
- confidence interval from a method appropriate to the estimand, preferring source-cluster bootstrap for correlated 3×3 outputs;
- sample/source count and missingness;
- slice results;
- test/non-inferiority definition if a formal decision claim is made.

Pairwise human preference additionally reports win/tie/loss. Binary non-tie preference can use an exact binomial interval; richer pairwise designs may use a predeclared Bradley-Terry-style model, with assumptions and uncertainty reported.

When multiple primary hypotheses are used for a formal family-wise claim, the experiment declares the multiplicity policy before analysis (for example Holm correction). Exploratory metrics stay labeled exploratory.

## 9. CI / release regression model

CI has separate evidence lanes rather than one blended score.

### Lane A — deterministic PR gate

Run on every material PR when technically applicable:

- schema/type/source binding;
- 3×3 branch identity and lossless join;
- deterministic factual/numeric/entity/date fixtures;
- required-concept invariants;
- format contracts;
- evaluator/config version integrity;
- dataset split/leakage validators.

Any applicable critical regression blocks release.

### Lane B — offline probabilistic regression

For material probabilistic changes, run baseline and candidate on a frozen versioned dataset/config. CALIBRATION can guide iteration. Promotion evidence uses frozen acceptance rules and, when the claim requires it, independent HELD_OUT replication.

For an oriented soft metric `m`, define:

`Δ_m = metric(candidate) - metric(baseline)`

and a confidence interval `[L_m, U_m]` for the paired delta. A non-inferiority rule can be written as:

`L_m >= -τ_m`

where `τ_m` is the predeclared smallest acceptable regression derived from human calibration/business tolerance. If `τ_m` is unknown, its status is `PENDING_EVIDENCE`; no arbitrary numeric value is inserted.

Critical gates do not use a compensatory `τ`: observed critical regression tolerance is zero.

### Lane C — human-calibration promotion gate

Audience production thresholds remain `DIAGNOSTIC_ONLY` until:

- independent human streams exist with provenance;
- pre-adjudication agreement/confusion/uncertainty are reported;
- threshold candidates are calibrated on CALIBRATION only;
- the threshold rule is frozen before HELD_OUT;
- held-out evidence demonstrates the declared operating characteristics with uncertainty sufficient for the intended claim.

## 10. Online evaluation and drift

Online eval is a monitoring/sampling layer, not a shortcut around offline evidence.

### 10.1 Sampling

Use stratified production sampling across audience, format, source family/risk, provider/model/version and hard-gate outcome. The sampling rate is selected from a declared detection-latency/annotation-budget objective, not a folklore percentage. Oversample rare critical failures and newly introduced versions while preserving weights needed for population estimates.

### 10.2 Monitors

Track at minimum:

- critical hard-gate failures and failure category;
- evaluator score/label distributions and `UNSCORABLE`/review rates;
- source/slice distribution shift;
- provider/model/prompt/evaluator versions;
- cost/latency/retry distributions;
- human disagreement/adjudication burden on sampled reviews;
- calibrated judge-vs-human residuals on refreshed review batches.

Distribution/drift alerts use thresholds estimated from a stable reference window and the desired false-alert/detection objective. No generic PSI/KS numeric threshold is adopted without project evidence.

### 10.3 Feedback lifecycle

Production examples selected for investigation enter DEV first. They cannot be injected into the current HELD_OUT set. Confirmed new failure modes produce versioned fixtures/slices, and material distribution or provider changes trigger a new calibration/held-out version.

Critical factual/source/policy incidents remain individually visible even if aggregate metrics look healthy.

## 11. Anti-circularity and leakage checklist

An evaluation run is invalid for threshold promotion if any of these hold:

- generation target was copied into `human_gold`;
- the same person supplied both nominally independent primary streams for an item;
- annotators saw model/evaluator predictions before freezing their own labels;
- HELD_OUT findings changed the evaluated system without rotating the split version;
- a judge was calibrated and evaluated on the same items without an independent held-out check;
- candidate and baseline used materially different source groups for a paired claim;
- duplicate/near-duplicate documents cross split boundaries;
- an external framework's default threshold was accepted without project evidence.

## 12. Dataset and experiment artifacts

Machine-readable schemas are defined in:

- `data/evals/production/eval_dataset_schema_v001.json`;
- `data/evals/production/experiment_metadata_schema_v001.json`.

Every experiment persists a manifest, raw arm outputs, evaluator/judge outputs, aggregate report, slice report, uncertainty report and hashes sufficient to reconstruct provenance.

## 13. Reversal / reopen conditions

Reopen this protocol if:

- human pilot evidence shows the rubric is not interpretable/reliable for a material slice;
- production source/audience/format distribution changes materially;
- a model judge/provider/version change causes calibration/stability drift;
- a new critical failure category is discovered;
- the selected eval tooling cannot reproduce required provenance or non-compensatory semantics;
- regulatory/partner constraints require different reviewer qualifications or retention/privacy handling.

## 14. Evidence basis

Primary/authoritative and research sources consulted for this protocol:

- NIST AI RMF Core, MEASURE: independent assessors, representative human evaluation, documented TEVV and production monitoring: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- NIST, *ARIA Evaluation Planning Manual: Elements of ARIA-Style AI Evaluations* (2026), combining model testing, red teaming and user testing: https://doi.org/10.6028/NIST.AI.200-3
- NIST Generative AI Profile (AI 600-1): https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- van der Lee et al., *Best practices for the human evaluation of automatically generated text* (INLG 2019): https://aclanthology.org/W19-8643/
- James, *Counting on Consensus: Selecting the Right Inter-Annotator Agreement Metric for NLP Annotation and Evaluation* (LREC 2026): https://aclanthology.org/2026.lrec-1.347/
- Oortwijn et al., *Interrater Disagreement Resolution* (HumEval 2021): https://aclanthology.org/2021.humeval-1.15/
- Amidei et al., *Rethinking the Agreement in Human Evaluation Tasks* (COLING 2018): https://aclanthology.org/C18-1281/
- Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (2023), documenting position, verbosity and self-enhancement biases: https://arxiv.org/abs/2306.05685
- Liu et al., *G-Eval* (2023), including observed human correlation and model-evaluator bias concerns: https://arxiv.org/abs/2303.16634

## 15. Current disposition

- deterministic critical gates: `LOCK` as non-compensatory;
- dual-stream blind human calibration + adjudication: `LOCK` as the default production evidence design, with justified equivalent protocols allowed;
- LLM/model judge: `LOCK` as secondary calibrated sensor, not sole authority;
- audience production thresholds: `PENDING_EVIDENCE` / `DIAGNOSTIC_ONLY`;
- external eval framework: `PENDING_EVIDENCE` pending representative bakeoff; see the tooling DR.
