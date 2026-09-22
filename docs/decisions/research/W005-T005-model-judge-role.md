# DR — W005-T005 model-judge role

`DR_ID: W005-T005-DR03`  
`STATUS: LOCK`  
`DATE: 2026-09-22`  
`SCOPE: structured semantic / LLM-as-a-judge sensors`

## Decision question

May an LLM/model judge act as the sole production authority for audience/content-quality release decisions?

## Alternatives

### A — Model judge as primary/sole arbiter

Attractive for scale, but it creates circularity when generation and evaluation share model families or biases, and it can hide critical factual failures behind an aggregate score.

**Disposition:** rejected.

### B — Calibrated model judge as a secondary sensor

Use a structured rubric, freeze judge prompt/model/config, calibrate against independent human labels, retain deterministic critical gates outside the judge, and continuously measure judge residuals/drift.

**Disposition:** `LOCK`.

### C — No model judge

Avoids model-judge bias but gives up a useful scalable sensor for semantic/subjective qualities that are difficult to fully encode deterministically.

**Disposition:** not preferred as a blanket rule; judge use is optional per property, but when used it follows candidate B.

## Evidence

- Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, report useful human correspondence while explicitly identifying position, verbosity and self-enhancement biases: https://arxiv.org/abs/2306.05685
- Liu et al., *G-Eval*, show improved correlation with human judgments for NLG while also noting potential bias toward LLM-generated text: https://arxiv.org/abs/2303.16634
- NIST AI RMF MEASURE calls for documented test sets/metrics and evaluation under deployment-like conditions, with independent assessors where appropriate: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

## Locked controls

1. A model judge never sets `human_gold=true` and never receives evidence class `HUMAN_*`.
2. Critical factual/source/policy/schema/provenance gates remain deterministic or independently evidenced and non-compensatory.
3. Calibrate judge behavior against independent human CALIBRATION labels before using it for a strong release claim.
4. Freeze provider/model snapshot, judge prompt/rubric, sampling config and parsing logic before HELD_OUT evaluation.
5. Pairwise judges randomize candidate order and run an order-swap check; inconsistent verdicts remain visible.
6. Measure repeated-run stability for nondeterministic judges.
7. Report error/confusion by audience, format and source-risk slices, not only aggregate correlation.
8. Track generator/judge model-family relationship; same-family evaluation is not forbidden but is an explicit circularity risk requiring human calibration.
9. Any tool/library default threshold remains diagnostic until justified on the project's calibration evidence.
10. Judge version change, provider drift or material calibration residual shift triggers recalibration/reopen.

## Release use

A calibrated judge may contribute to a predeclared soft-metric release rule only after its operating characteristics are measured against independent human evidence. It cannot compensate for a critical hard-gate regression and cannot by itself freeze production audience thresholds.

## Reversal conditions

Reopen only if a future evaluator demonstrates independent, validated operating characteristics sufficient to replace the specific human/deterministic evidence lane for a defined property, with documented error bounds, anti-circularity controls and equivalent provenance. This must be established empirically, not inferred from model capability claims.
