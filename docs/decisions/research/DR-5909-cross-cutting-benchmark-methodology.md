# DR-5909 — Cross-cutting quantitative benchmark and decision methodology

`TASK_ID: W005-T009`
`ATTEMPT_ID: A02`
`RESEARCH_DATE: 2026-09-22`
`DECISION: STATISTICAL_METHOD_LOCK + MULTIDIMENSIONAL_DECISION_SURFACE_LOCK; BUSINESS_UTILITY_PENDING_EVIDENCE`
`CONFIDENCE: HIGH for the hard-gate/paired/raw-metric/Pareto/statistical contract; LOW for any universal business utility because representative preference evidence is absent`

## Decision question

What reusable quantitative comparison methodology should W005/W006 use for material architecture/model/provider/eval/runtime decisions without inventing business utility, practical-effect thresholds, SLOs or winner rules?

## Workload / constraints

The Academy Suno workload contains correlated 3x3 outputs derived from the same source, deterministic safety/quality invariants, stochastic model/provider behavior, task-specific architecture/reliability measurements and currently bounded human/business evidence. Production Contract requirements demand baseline-vs-candidate comparability, multiobjective quantitative evidence, reliability/capacity measurement without invented targets, and a DRG before production locks.

Relevant risks: RISK-0004 small-corpus generalization; RISK-0034 preference-driven stack lock; RISK-0038 invented capacity targets; RISK-0040 research bureaucracy without decision value.

## Alternatives

| Alternative | Strength | Material failure mode | Disposition |
|---|---|---|---|
| A. Fixed weighted scalar score + thresholds | Easy ranking/reporting | Encodes unsupported utility and can hide trade-offs | REJECT |
| B. Hard gates + raw multidimensional metrics + uncertainty + point Pareto; no overall winner unless evidence resolves trade-off | Preserves evidence boundary and non-compensation | May legitimately end in `NO_PREFERENCE` | **LOCK default** |
| C. Lexicographic priority rules | Clear when business priorities are known | Priority order is arbitrary without representative evidence | PENDING_EVIDENCE |
| D. Evidence-elicited scalar/utility model + sensitivity analysis | Can support a decision when priorities are real and robust | Requires representative elicitation and robustness evidence | CONDITIONAL / PENDING_EVIDENCE |

## Evaluation criteria declared before decision

- compatibility with Production Contract and DRG;
- non-compensation of hard failures;
- preservation of raw units/trade-offs;
- statistical validity under pairing/source correlation;
- explicit missingness/evidence-class handling;
- reproducibility and anti-cherry-picking;
- ability to represent cost/latency/reliability without inventing targets;
- ability to integrate future human/business utility evidence without rewriting historical results.

No weights were assigned to these criteria because no defensible criterion utility was provided and the decision can be made by hard requirements plus qualitative dominance of the methodology contract.

## Systematic source search

Search date: 2026-09-22. Sources were prioritized in this order: canonical project contracts/results, official scientific-library documentation, then established optimization documentation. Search categories: paired bootstrap/BCa, paired permutation tests, multiple-testing FWER, constrained multiobjective optimization, and canonical W003/W004 evidence boundaries.

Stopping rule: stop when the required statistical/constraint mechanics are covered by authoritative sources, A01 failure modes are resolved, and an additional search round does not introduce a material method alternative or contradiction relevant to this task. No vendor benchmark is required because this task defines comparison methodology rather than selecting a vendor.

## Source table

| Source | Type/date | Supported claim | Limitation |
|---|---|---|---|
| `SYSTEM/CONSTITUTION.md` + `SYSTEM/DECISION_RESEARCH_GATE.md` | canonical | hard gates non-compensatory; no artificial single score; NO_PREFERENCE valid | project policy, not external statistics evidence |
| `SYSTEM/PRODUCTION_CONTRACT.md` | canonical | quantitative-first; baseline/candidate same config; no invented quality/latency/capacity thresholds | does not choose statistical estimator |
| W003/W004 accepted results summarized by STATE 0044 | canonical evidence | source/branch identity, bounded evidence classes, unknowns must remain explicit | samples remain bounded |
| SciPy `scipy.stats.bootstrap` current manual | primary library docs, checked 2026-09-22 | paired resampling, BCa, confidence level, seeded RNG, degenerate-data caveat | library behavior, not business materiality |
| SciPy `scipy.stats.permutation_test` current manual | primary library docs, checked 2026-09-22 | paired permutation modes, exact-vs-randomized execution, seeded RNG | test choice still depends on estimand/null |
| statsmodels `multipletests` current manual | primary library docs, checked 2026-09-22 | Holm step-down Bonferroni FWER correction available | multiplicity family must be predeclared |
| pymoo constraint handling 0.6.2 docs | technical docs, checked 2026-09-22 | feasibility/constraints can be handled separately from objective optimization | optimization package is illustrative, not project authority |

## Findings

1. **Pair/block identity must be first-class.** Repeated 3x3 outputs from the same source are correlated; source-level inference must not count them as independent source samples.
2. **Deterministic invariants and stochastic metrics need different evidence mechanics.** Binary hard gates are pass/fail; CIs/tests apply where repeated/probabilistic sampling is meaningful.
3. **Statistical detectability and business materiality are different variables.** An interval excluding zero does not establish that the effect matters operationally.
4. **Point Pareto reporting is sufficient to expose objective trade-offs without utility assumptions.** A threshold-aware/epsilon frontier is valid only when the thresholds themselves have evidence provenance.
5. **A scalar or lexicographic utility can be valid later, but only as an evidence-bearing object.** It needs representative priority elicitation plus sensitivity analysis; rank instability implies `NO_PREFERENCE`.
6. **No universal sample size, SLO, capacity target or practical-effect threshold is defensible here.** Those belong in workload-specific manifests backed by evidence/power/precision or explicit external constraints.

## Decision

### `STATISTICAL_METHOD_LOCK`

Lock the paired/block-preserving experiment hygiene, explicit estimands/units, uncertainty for meaningful repeated measurements, seeded reproducible resampling, predeclared inferential families and Holm FWER correction when that family-wise question is actually asked.

### `MULTIDIMENSIONAL_DECISION_SURFACE_LOCK`

Lock the default decision order: hard gates -> raw multidimensional metrics -> uncertainty -> point Pareto -> `NO_PREFERENCE` when trade-offs remain unresolved.

### `BUSINESS_UTILITY_PENDING_EVIDENCE`

No scalar weights, practical-effect thresholds, latency/cost anchors, SLOs, capacity targets or priority ordering are locked by this task. Future utility is allowed only with representative evidence, predeclaration and sensitivity analysis.

No technology/provider/model winner is selected by this DR.

## Reversal conditions

Reopen the statistical contract if the workload violates the assumed pairing/block structure, a better validated estimator/test is required for a declared estimand, or downstream evidence shows materially misleading coverage. Reopen the business-utility status when representative partner/human/business evidence supplies priorities/thresholds and a sensitivity analysis demonstrates a robust preferred set.

## Traceability

- PROD-009 — comparable baseline/candidate experiment and persisted artifacts.
- PROD-013 — reliability/capacity measurement without invented target.
- PROD-015 — material decision research, benchmark, uncertainty and reversal conditions.
- RISK-0004 — source/block identity, bounded-scope claim and held-out policy.
- RISK-0034 — no stack/provider preference without representative benchmark evidence.
- RISK-0038 — no fabricated capacity/SLO target.
- RISK-0040 — stopping rule and executable schema/validator keep research decision-oriented.
