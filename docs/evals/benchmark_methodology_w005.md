# W005 Quantitative Benchmark Methodology v001

**Task:** W005-T009-A01  
**Methodology ID:** `W005-BENCHMARK-METHODOLOGY-V001`  
**Evidence posture:** `DIAGNOSTIC_ONLY` until the relevant human/calibration evidence exists  
**Scope:** benchmark/evaluation contract only; no new production architecture and no live provider run

## 1. Purpose and non-claims

This methodology creates one reproducible comparison contract for W005-T010..T013 to compare candidate production decisions across four headline objectives:

1. factuality;
2. end-user value;
3. latency;
4. cost.

It intentionally separates **eligibility** from **preference**. Critical factual, material-concept, financial-relevance, pairing, or unresolved review failures are non-compensatory constraints. A high weighted score cannot rescue an ineligible candidate.

The current W004 evidence remains bounded. W004-T005 has automated calibration but no independent human gold/agreement; W004-T006 found no measured semantic-proxy gain and no backend preference; W004-T007 provides real but bounded provider/model observations and explicitly no overall model preference; W004-T008 proves the internal clean E2E release path without making a blanket production-readiness claim. This methodology does not upgrade those evidence classes.

## 2. Evidence and contract mapping

| Source | Reused invariant |
|---|---|
| `SYSTEM/RESULTS/W003-T009-A01.md` | exact 3x3 mechanics; hard-gate non-compensation; telemetry lineage; cost may be unknown rather than synthesized |
| `SYSTEM/RESULTS/W004-T005-A02.md` | 36-item frozen DEVELOPMENT population; automated calibration is `DIAGNOSTIC_ONLY`; held-out remains untouched |
| `SYSTEM/RESULTS/W004-T006-A01.md` | semantic diagnostics may not weaken hard gates; current delta does not justify a backend preference |
| `SYSTEM/RESULTS/W004-T007-A05.md` | same-task candidate observations expose measured quality, latency, tokens and observed cost; bounded result is not an overall production winner |
| `SYSTEM/RESULTS/W004-T008-A02.md` | clean-checkout E2E/release proof remains evidence-bounded |
| `data/evals/gold/rubric_v001.json` | factual and material-concept preservation are non-compensatory; audience labels are judgments, not blind averages |
| `experiments/hard_gates/factual_hard_gate_spec_v001.json` | critical factual failures are disqualifying |
| `SYSTEM/PRODUCTION_CONTRACT.md` | PROD-009 telemetry, PROD-013 provider/model evidence, PROD-015 quantitative superiority require quality + latency + cost evidence |
| `SYSTEM/ASSUMPTION_RISK_REGISTER.md` | controls for RISK-0013 serialization boundaries, RISK-0015 contract drift and RISK-0018 clean-checkout reproducibility |

## 3. Unit of comparison and pairing

The primary experimental unit is:

`evidence_item_id x audience x format`

A comparison is valid only when baseline and candidate are evaluated on the same frozen evidence item, audience, format and predeclared stratum. The canonical `pair_key` is:

`[evidence_item_id, audience, format, stratum_id]`

Minimum strata are audience, format, source family and criticality. Extra strata are permitted only when declared before candidate results are inspected.

Rules:

- preserve pair identity through scoring, resampling and statistical testing;
- freeze prompts/configs and, where stochastic generation is used, record seeds/config hashes;
- never silently drop provider/model failures or missing outputs;
- no synthetic imputation into primary quality estimands;
- report pair coverage and missingness separately;
- never use held-out evidence for tuning, anchor selection or threshold tuning.

## 4. Unified 0-100 scoring

Every scored axis is normalized to `[0, 100]`.

### 4.1 Factuality — 40%

Use a rubric/evaluator score explicitly mapped to 0-100. If the source score is already `[0,1]`, multiply by 100. If it is ordinal, the run manifest must declare the fixed mapping before execution. Critical factuality remains a separate hard gate regardless of numeric score.

### 4.2 End-user value — 30%

Combine only predeclared, source-grounded rubric components that represent usefulness to the requested audience/format (for example material-concept preservation, audience fit, clarity/actionability and format-native usefulness). The exact component list and within-axis weights must be frozen in the run manifest. Human-dependent claims remain `DIAGNOSTIC_ONLY` until independent human evidence exists.

### 4.3 Latency utility — 15%

Raw latency remains `latency_ms`. The headline score uses a clipped linear utility between two **frozen, external-to-results** anchors:

- `good_anchor`: utility 100;
- `bad_anchor`: utility 0;
- between anchors: linear interpolation;
- below/above anchors: clip to 100/0.

The anchors must be supplied by the benchmark run manifest before candidate results are observed. Candidate-relative min-max scaling is prohibited because adding/removing a candidate would change every score.

### 4.4 Cost utility — 15%

Raw cost remains `cost_usd`, based only on observed usage plus a versioned pricing snapshot. The headline utility follows the same frozen-anchor rule as latency. Unknown cost stays `null` and makes the affected cost comparison `NOT_COMPUTABLE`; it is never replaced with synthetic provider cost.

### 4.5 Headline aggregate

For hard-gate-eligible rows/systems:

`headline = 0.40*factuality + 0.30*end_user_value + 0.15*latency_utility + 0.15*cost_utility`

All component values are on `[0,100]`; therefore the headline is on `[0,100]`.

The headline is a reporting summary, **not** a release gate and **not** a substitute for the Pareto view.

## 5. Disjunctive hard gates

Failure semantics are disjunctive:

`ineligible = ANY(gate in {FAIL, REVIEW_REQUIRED})`

The v001 gates are:

1. `FACTUAL_CRITICAL_PRESERVATION` — inherit canonical factual critical semantics;
2. `MATERIAL_CONCEPT_PRESERVATION` — a material source concept cannot disappear for readability/simplicity;
3. `FINANCIAL_RELEVANCE_CRITICAL` — material entity/period/scale/direction/unit or required-financial-concept error capable of changing the financial/investment interpretation;
4. `PAIRING_AND_COVERAGE` — no primary claim when the predeclared paired comparison is invalid or failures were silently discarded.

`NOT_APPLICABLE` is allowed only where the underlying canonical contract allows it. `REVIEW_REQUIRED` is not treated as PASS.

Ineligible systems may still appear in audit tables but are excluded from winner claims and the Pareto frontier.

## 6. Pareto frontier

Among hard-gate-eligible systems, compute nondominance on raw/meaningful objectives:

- maximize factuality score;
- maximize end-user-value score;
- minimize raw `latency_ms`;
- minimize raw `cost_usd`.

Point dominance: A dominates B when A is no worse on all four objectives and strictly better on at least one.

Also publish a **practical-epsilon frontier** so tiny numerical differences do not masquerade as material trade-offs. v001 epsilons are:

- factuality: 2.0 points;
- end-user value: 2.0 points;
- latency: 5% relative;
- cost: 5% relative.

These are benchmark decision thresholds, not production SLOs. They are versioned and must be revisited when representative human/business evidence can support better thresholds.

For every candidate publish `point_frontier`, `practical_epsilon_frontier`, and `dominated_by`.

## 7. Statistical policy

### 7.1 Estimands

Primary: paired mean difference, candidate minus baseline, within the same pair keys.

Secondary:

- paired median difference;
- relative latency change;
- relative cost change;
- predeclared stratum-level effects.

Every result reports `n_pairs` and coverage.

### 7.2 Confidence intervals

Use a paired 95% BCa bootstrap, resampling pair indices as blocks. Default v001:

- 10,000 resamples;
- fixed seed `905009`.

If BCa is numerically impossible, a documented paired percentile fallback is allowed; the fallback must be persisted in the result.

### 7.3 Randomization/permutation test

Use the paired randomization/sign-flip null on within-pair deltas.

- exact enumeration when `n_pairs <= 20`;
- otherwise Monte Carlo with 100,000 resamples;
- fixed seed `905009`;
- two-sided primary test unless a directional hypothesis was preregistered.

Stratified comparisons must preserve strata during randomization.

### 7.4 Multiplicity

For the predeclared family of candidate x primary-objective superiority tests, control family-wise error at `alpha=0.05` using Holm adjustment. Exploratory analyses are labeled exploratory and cannot drive a production lock.

### 7.5 Statistical + practical classification

Minimum practical effects in v001:

- factuality: 2.0/100 points;
- end-user value: 2.0/100 points;
- latency: 5% relative;
- cost: 5% relative.

A `BETTER` claim requires all of:

1. all hard gates eligible;
2. favorable point estimate at least the practical-effect threshold;
3. 95% CI favorable beyond zero;
4. Holm-adjusted p-value `< 0.05`.

If statistically distinguishable but below the practical threshold, classify `NEGLIGIBLE`. If the point estimate is practically large but uncertainty/significance criteria fail, classify `INCONCLUSIVE`. Missing required evidence is `NOT_COMPUTABLE`.

Statistical significance never upgrades `DIAGNOSTIC_ONLY` evidence into a human-validated or production-wide claim.

## 8. Reproducibility and audit contract

Every run persists:

- repository commit SHA;
- methodology ID/version;
- benchmark manifest and rubric versions;
- baseline/candidate IDs and provider/model versions;
- generation config SHA-256;
- pricing snapshot ID;
- random seeds;
- input/output artifact SHA-256 values;
- pair/stratum IDs;
- gate states and evidence refs;
- raw objective values and 0-100 utilities;
- CI/test method, resample count, raw p and Holm-adjusted p;
- pair coverage/missingness;
- Pareto membership and dominance provenance;
- UTC timestamp.

Machine-readable values must be JSON-native scalars. At DB/SQL boundaries, `bytes`, row objects or framework-specific scalar wrappers must be normalized before serialization (RISK-0013).

Methodology/rubric/strata/anchors/thresholds are frozen before candidate execution (RISK-0015).

The validator is dependency-light and intended to run from a clean checkout; missing/mismatched required inputs fail closed (RISK-0018).

## 9. Decision Research Gate record

### Trigger/problem

W005-T009 must choose a benchmark aggregation/statistical policy that downstream production-research tasks can reuse without erasing critical constraints or turning bounded W004 observations into a production winner.

### Baseline/counterfactual

Continue W004-style task-specific metrics and qualitative `NO_PREFERENCE` outcomes without one common cross-task quantitative contract.

### Alternatives considered

| Alternative | Advantages | Failure mode |
|---|---|---|
| A. equal-weight additive score (25/25/25/25) | simplest single number | underweights factual/end-user quality and invites compensation |
| B. quality-heavy additive score + hard gates + Pareto (40/30/15/15) | interpretable headline, keeps quality primary, constraints prevent compensation, Pareto exposes trade-offs | weights are a policy choice and need versioning |
| C. multiplicative/geometric utility | punishes weak dimensions automatically | less interpretable around zero/missing metrics; still does not replace explicit safety gates |

**Decision: `LOCK` B for benchmark methodology v001**, not as a production-stack decision. Reversal conditions: representative human/business evidence supports different weights/effect thresholds, or downstream sensitivity analysis shows material ranking instability. Any change requires a new methodology version; historical results remain bound to v001.

### External research used

- SciPy bootstrap documentation: paired resampling and BCa confidence intervals — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
- SciPy permutation-test documentation: paired sample randomization/sign-flip semantics and exact-vs-randomized execution — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html
- statsmodels multiple-testing documentation: Holm step-down FWER control — https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html
- pymoo constraint-handling documentation: feasibility-first treatment motivates hard-gate eligibility before objectives — https://pymoo.org/constraints/

### Evidence saturation / stopping rule

Stop methodology research when: (a) the score/gate/statistical contract covers all dispatch requirements, (b) every material rule is machine-readable, (c) W003/W004 evidence can be represented without claim inflation, and (d) no new source changes the selected statistical/constraint treatment. No live provider benchmark is needed for this methodology task.

## 10. Machine-readable artifacts

- `data/evals/w005/benchmark_methodology_v001.json` — frozen methodology/config contract;
- `data/evals/w005/benchmark_result_v001.schema.json` — result interchange schema for T010-T013;
- `experiments/benchmark_w005/validate_methodology.py` — dependency-light invariant validator;
- `tests/benchmark_w005/test_methodology.py` — clean-checkout contract tests.

## 11. Downstream use by T010-T013

1. Freeze the benchmark manifest, anchors, strata, candidates and thresholds before seeing candidate results.
2. Emit one record per system per pair key.
3. Evaluate hard gates first.
4. Normalize eligible numeric axes to 0-100 without candidate-relative scaling.
5. Compute the headline score for reporting.
6. Compute point and practical-epsilon Pareto frontiers on raw objectives.
7. Run paired CIs/randomization tests; apply Holm across the predeclared family.
8. Preserve evidence class and unknowns.
9. Make a production decision only in the downstream Decision Research Gate, never from the headline score alone.
