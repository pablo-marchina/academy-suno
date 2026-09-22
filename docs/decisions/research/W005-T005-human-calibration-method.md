# DR — W005-T005 human calibration and statistical method

`DR_ID: W005-T005-DR01`  
`STATUS: LOCK`  
`DATE: 2026-09-22`  
`SCOPE: production audience calibration / human evidence / uncertainty`

## Decision question

What evidence design is strong enough to calibrate production audience evaluation without reusing W004 automated blind calibration as human gold?

## Candidates

### A — Single reviewer / single label per item

Low operational cost, but no independent agreement estimate and weak protection against reviewer-specific bias. It cannot satisfy `PROD-008` as written.

**Disposition:** rejected for production threshold evidence.

### B — Two blind independent primary streams + triggered adjudication

Two independent labels are collected before either annotator sees the other label, generation target, evaluator prediction, model/prompt identity or baseline/candidate identity. Pre-adjudication agreement is retained; disagreement and critical-check conflicts trigger adjudication. Gold is promoted only from traceable independent/adjudicated human evidence.

**Disposition:** `LOCK` as the default production design.

### C — Three-or-more independent raters with majority/latent aggregation

Can improve robustness or support richer uncertainty modeling, but cost/benefit depends on disagreement rate, slice risk and annotator expertise. No representative project measurement yet proves that the extra stream is necessary for every item.

**Disposition:** `NO_PREFERENCE` versus targeted expansion of candidate B until pilot evidence exists; use it for high-uncertainty/high-risk slices when justified.

## Evidence

- NIST AI RMF MEASURE calls for documented TEVV, representative human evaluation and independent/internal experts not limited to front-line developers: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- NIST ARIA 200-3 (2026) structures holistic evaluation around model testing, red teaming and user testing: https://doi.org/10.6028/NIST.AI.200-3
- van der Lee et al. summarize best practices for human evaluation of generated text, emphasizing explicit design/reporting: https://aclanthology.org/W19-8643/
- James (LREC 2026) reviews agreement metrics by annotation type and recommends transparent reporting including uncertainty/disagreement patterns: https://aclanthology.org/2026.lrec-1.347/
- Oortwijn et al. provide a systematic disagreement-resolution approach: https://aclanthology.org/2021.humeval-1.15/
- Amidei et al. caution that disagreement can reflect genuine language variability rather than a defect to hide: https://aclanthology.org/C18-1281/

## Locked method

1. Split at source-document/near-duplicate group level into DEV, CALIBRATION and HELD_OUT.
2. Keep primary human streams independent and blind to generation target, system identity and evaluator output.
3. Report pre-adjudication confusion and agreement before any consensus operation.
4. For exactly two ordinal streams, report raw agreement plus weighted kappa when defined; for designs with >2 raters/missingness, use an agreement statistic appropriate to the scale such as Krippendorff alpha. Do not reduce validity to one coefficient.
5. Cluster uncertainty by source document because the 3×3 outputs share the same source.
6. Adjudicate disagreements and critical-check conflicts without revealing forbidden target/evaluator information.
7. Preserve `UNSCORABLE/UNRESOLVED` instead of forcing a gold class.
8. Freeze calibration choices before HELD_OUT; any held-out-driven tuning contaminates that split version.
9. Size samples from a declared estimand + precision/power target using pilot variance/rates; no arbitrary universal item count.
10. Audience thresholds remain `DIAGNOSTIC_ONLY` until calibrated and replicated with sufficient independent human evidence.

## Statistical reporting contract

- Bernoulli pass/failure rates: finite-sample interval (for example Wilson); planning may use `n ≈ z² p(1-p)/e²` with pilot `p` or conservative `0.5` variance assumption.
- Paired baseline/candidate metrics: paired effect + source-cluster bootstrap CI.
- Pairwise preference: win/tie/loss plus uncertainty; exact binomial on non-ties when appropriate or a predeclared pairwise model for richer designs.
- Formal multiple-primary-metric claims: multiplicity policy declared before result inspection.
- Critical factual/source/policy regressions: non-compensatory; observed tolerance remains zero where the Production Contract applies.

## Limitations

- The method does not determine annotator staffing or domain-expert availability.
- No production threshold is locked here.
- Human judgment is not automatically valid merely because it is human; qualification, rubric design, source evidence and disagreement analysis remain necessary.

## Reversal conditions

Reopen this decision if a pilot shows that two streams cannot produce interpretable evidence for a material slice, domain expertise requirements change materially, reviewer availability makes the design infeasible, or a validated alternative demonstrates equivalent independence/uncertainty with lower operational burden.
