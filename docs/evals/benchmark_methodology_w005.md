# W005 Quantitative Benchmark Methodology v002

**Task:** W005-T009-A02  
**Methodology:** `W005-BENCHMARK-METHODOLOGY-V002`  
**Default:** `NO_PREFERENCE` / `PENDING_EVIDENCE` when business utility is not evidenced  
**Evidence posture:** `DIAGNOSTIC_ONLY` unless a downstream run proves a stronger class

## 1. Decision contract

A02 supersedes rejected A01 v001. The default order is:

1. evaluate non-compensatory hard gates;
2. publish raw multidimensional metrics with units, evidence class and missingness;
3. quantify uncertainty only where repeated/probabilistic measurement makes it meaningful;
4. compute point Pareto among eligible candidates;
5. emit `NO_PREFERENCE` when trade-offs remain unresolved;
6. allow scalar/lexicographic utility only after representative human/business evidence plus sensitivity analysis.

A hard-gate failure is never offset by quality, latency, cost, throughput or an aggregate.

## 2. A01 revalidation

| A01 component | A02 disposition |
|---|---|
| paired identity | **ACCEPT / strengthen** |
| hard-gate non-compensation | **ACCEPT / LOCK** |
| raw quality/latency/cost | **ACCEPT / LOCK** |
| paired/block bootstrap and randomization | **ACCEPT with applicability guard** |
| Holm for a predeclared family | **ACCEPT when applicable** |
| point Pareto | **ACCEPT / LOCK** |
| 40/30/15/15 headline score | **REJECT** |
| fixed 2-point / 5% practical thresholds | **REJECT** |
| fixed-epsilon frontier | **REJECT as default** |
| ranking from synthetic composite | **REJECT** |

The rejected weights/thresholds had no representative business evidence. They remain historical diagnostics only.

## 3. Pairing, grouping and workload slices

Each observation records `evidence_item_id`, `source_group_id`, `stratum_id`, `system_id`, `generation_repeat_id`, `run_id`, and audience/format when applicable. For the 3x3 workload, pair identity is:

`[evidence_item_id, audience, format, stratum_id, generation_repeat_id]`

`source_group_id` is the correlation block. Nine 3x3 outputs from one source **must not** be treated as nine independent source samples. Pair/block identity survives aggregation, resampling and tests. Failed/missing outputs stay in the audit record and are not silently imputed into the primary estimand.

Minimum content slices: audience, format, source family and criticality. Runtime studies may add concurrency, failure mode, tenant boundary, payload size or recovery scenario. These are measurement strata, not invented targets.

Every run declares `REPRESENTATIVE_FOR_DECLARED_SCOPE`, `BOUNDED_DIAGNOSTIC_SAMPLE` or `MECHANICS_ONLY`. The latter two cannot be promoted silently to population-wide evidence. Held-out evidence cannot tune prompts, thresholds, weights, anchors, strata or stopping rules.

## 4. Metric interoperability

Each metric declares ID, raw value, unit/range, direction, evidence class, aggregation level and missingness semantics.

- **Quality:** keep factual/source preservation, material concepts, audience fit, clarity, format compliance and task rubrics as named axes; model/judge output never becomes human gold by aggregation.
- **Latency:** persist raw stage/end-to-end milliseconds and observed distributions. Do not map latency to arbitrary utility.
- **Throughput/capacity:** record observed completion rate, concurrency/load context, queues/resources, error/retry rates and saturation behavior. No production capacity target or SLO is invented.
- **Reliability/recovery:** deterministic scenarios/invariants are PASS/FAIL; repeated probabilistic reliability may use rates/counts/uncertainty with sampling unit declared.
- **Cost:** persist observed usage, pricing snapshot/version/date and computed cost separately from billed cost when available. Unknown stays `NOT_COMPUTABLE`/null.

## 5. Hard gates

Default eligibility:

`INELIGIBLE = any(required_gate in {FAIL, REVIEW_REQUIRED, NOT_COMPUTABLE})`

Shared gates include factual critical preservation, material concept preservation, financial relevance critical and pairing/coverage. Task-specific security, tenant, schema, provenance or recovery gates may be added. Ineligible systems remain visible for audit but cannot be preferred or rescued by soft metrics.

## 6. Raw multidimensional + Pareto

Point Pareto is computed only over predeclared, comparable objectives with known direction and valid observations. A dominates B only when A is no worse on every comparable objective and strictly better on at least one.

If a required objective is missing, emit `PARETO_NOT_COMPUTABLE` for the affected comparison; do not drop the objective post hoc. No fixed epsilon frontier exists in v002. A threshold-aware frontier is permitted only with predeclared `threshold_evidence_refs`.

## 7. `STATISTICAL_METHOD_LOCK`

Locked mechanics:

- preserve pairs and source-group blocks;
- report estimand, unit, pair/block counts, coverage and raw observations;
- use paired/block confidence intervals for stochastic/repeated measurements when the sampling model is meaningful;
- paired/block BCa bootstrap is preferred when valid; a predeclared paired percentile/basic fallback is allowed if BCa is invalid;
- paired randomization/permutation tests are used only when the null and estimand match; exact enumeration when feasible, otherwise seeded Monte Carlo;
- predeclare inferential families; use Holm FWER when that family-wise question is actually asked;
- seed/version randomized procedures and persist library/version/parameters/fallbacks;
- deterministic binary invariants remain PASS/FAIL rather than being forced into CI machinery.

A 95% confidence level and alpha 0.05 are default inferential reporting conventions, not product targets or business-materiality thresholds. A justified run may predeclare another statistical level before candidate outcomes.

Statistical significance does **not** establish business importance. Each inferential result therefore separates `statistical_direction` from `practical_materiality`. Without domain/workload evidence for materiality, the latter is `PENDING_EVIDENCE`, even if an interval excludes zero.

## 8. `BUSINESS_UTILITY_STATUS`

`BUSINESS_UTILITY_STATUS = PENDING_EVIDENCE` by default.

Scalar weights, lexicographic priorities, anchors or practical thresholds may be introduced only when: (a) representative partner/human/business or accepted external constraint evidence supports them; (b) the contract is frozen before candidate outcomes; (c) hard gates remain external to utility; (d) evidence refs are persisted; (e) sensitivity spans the evidence-supported range; and (f) the preferred set is stable. Otherwise emit `NO_PREFERENCE` / `PENDING_EVIDENCE`.

Illustrative/expert-invented weights may be shown only as sensitivity examples and cannot produce a project preference.

## 9. Missingness and anti-cherry-picking

Allowed missingness states: `OBSERVED`, `NOT_APPLICABLE`, `NOT_COMPUTABLE`, `MISSING_CANDIDATE_OUTPUT`, `MEASUREMENT_FAILED`, `WITHHELD_HELD_OUT`. Preserve counts by candidate/slice. Complete-case analyses disclose exclusions and cannot be the only view when exclusions differ materially by candidate.

Before execution freeze/hash: question/claims, candidates/baseline, sample and held-out partition, slices, metrics/directions, hard gates, estimands/tests/family, missingness policy, stopping rule and optional utility evidence. Exploratory analyses are labeled `EXPLORATORY` and cannot alone justify a production lock.

## 10. Stopping / evidence saturation

There is no global numeric sample-size or practical-effect threshold. Each run predeclares a design appropriate to its claim: fixed sample with power/precision basis, full finite-scenario enumeration, sequential design with explicit error control, or research evidence saturation. Stopping when a desired candidate becomes significant/favorable is prohibited. Insufficient materiality evidence may legitimately end in `NO_PREFERENCE` / `PENDING_EVIDENCE`.

## 11. Research basis (revalidated 2026-09-22)

- SciPy `bootstrap`: paired shared-index resampling, BCa, explicit confidence/resample/RNG controls and degenerate-data caveat — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
- SciPy `permutation_test`: paired modes, exact-vs-randomized execution and RNG control — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html
- statsmodels `multipletests`: Holm step-down Bonferroni FWER — https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html
- pymoo constraint handling: feasibility/constraints separated from objective optimization — https://pymoo.org/constraints/

These sources justify mechanics, not Academy business utility. Canonical constraints come from CONSTITUTION, DECISION_RESEARCH_GATE, PRODUCTION_CONTRACT and accepted W003/W004 evidence.

## 12. Artifacts and downstream order

Machine-readable contract: `data/evals/w005/benchmark_methodology_v002.json`; result schema: `data/evals/w005/benchmark_result_v002.schema.json`; executable validator: `experiments/benchmark_w005/validate_methodology_v002.py`; tests: `tests/benchmark_w005/test_methodology_v002.py`; DRG: `docs/decisions/research/DR-5909-cross-cutting-benchmark-methodology.md`.

Downstream: freeze manifest -> execute comparable candidates -> persist raw observations/failures -> hard gates -> raw aggregation -> meaningful uncertainty -> predeclared multiplicity -> point Pareto -> `NO_PREFERENCE/PENDING_EVIDENCE` unless representative utility evidence + stable sensitivity authorizes a preference.
