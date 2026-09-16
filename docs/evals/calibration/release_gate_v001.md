# Calibration / Ablation / Anti-Gaming Release Gate v001

## Scope

This gate executes W003-T008 on the **development** side of `gold-v001` only. It is deliberately unable to tune, inspect, or learn from the held-out source. Any calibration row not explicitly marked `DEVELOPMENT` is rejected.

Current split:

- development: `copom_277_2026_03`, `petrobras_2t26_results`;
- held-out: `petrobras_capex_fato_relevante_2024_08_08` with `tuning_exposure=FORBIDDEN`.

## Current evidence posture

`gold-v001` still has no promoted independent human gold labels and no independent human agreement/adjudication statistics. The manifest itself sets `threshold_policy.freeze_allowed=false`.

Therefore the current release-gate result is **DIAGNOSTIC_ONLY**. No numeric audience threshold, floor, semantic-backend cutoff, provider/model preference, or provider-cost claim is frozen by this task.

This is a limitation of evidence, not a software failure and not permission to substitute requested generation targets for human truth.

## Metrics contract

When valid development rows become available, `experiments/calibration/release_gate.py` computes two separate evaluations:

1. `generation_target_level → human_gold_level`: measures whether generated material was perceived by independent humans at the requested level. The requested target is treatment/intent, never gold.
2. `human_gold_level → evaluator_predicted_level`: measures evaluator classification performance against independent human gold.

For each relation the harness emits a deterministic truth-row / prediction-column confusion matrix, per-level precision/recall/F1/support, macro precision/recall/F1, and accuracy.

Held-out rows are rejected before either computation.

## Anti-gaming release gate

The release gate consumes the already-integrated T004 anti-gaming evidence and requires the mandatory failure modes to remain observable:

- jargon stuffing → `JARGON_STUFFING`;
- sentence chopping / format fragmentation → `SENTENCE_CHOPPING`;
- acronym manipulation → `ACRONYM_HACK`;
- concept deletion → `REQUIRED_CONCEPT_OMISSION`.

The persisted evidence packet also carries alias stuffing and glossary dumping. Missing a mandatory case or its expected flag fails the anti-gaming gate.

The current evidence packet is grounded in `SYSTEM/RESULTS/W003-T004-A01.md`, where the audience evaluator's focused suite passed 15 tests. W003-T008 does not fabricate a new human-gold claim from those deterministic fixtures.

## Semantic ablation contract

Semantic evidence is incremental only. The gate compares development-gold runs with semantic disabled/enabled and checks that source/factual/policy hard-fail codes remain identical. A semantic-enabled `PASS` while a hard-fail code remains present is a release-gate failure.

No measured development-gold semantic ablation rows are available in the current evidence packet, so the persisted disposition is:

- `status=NOT_RUN`;
- `decision=NO_BACKEND_PREFERENCE`.

This does not count as evidence against a semantic backend; it means backend selection remains open.

## Provider / model / cost comparison contract

A provider/model/backend candidate is comparable only when its evidence is measured and includes observed quality and latency. Pricing marked `SYNTHETIC` is excluded from provider-cost evidence.

The T007 telemetry demo uses synthetic demo pricing, so the current gate returns `NOT_COMPARABLE` and `NO_PREFERENCE`. This preserves the explicit N/A / provenance semantics of the telemetry contract.

## Current release blockers

The v001 report persists exactly four evidence blockers:

- `NO_INDEPENDENT_HUMAN_GOLD_LABELS`;
- `NO_INDEPENDENT_HUMAN_AGREEMENT`;
- `MANIFEST_FREEZE_NOT_AUTHORIZED`;
- `AUDIENCE_CONFUSION_METRICS_NOT_COMPUTABLE`.

Anti-gaming is PASS. There is no semantic hard-gate invariant failure; semantic ablation is simply not yet measurable on development human gold.

## Kill criteria

Stop release calibration immediately if any of the following occurs:

- held-out data is touched by tuning or iterative error analysis;
- requested target is promoted to gold;
- gold lacks versioned independent annotation/adjudication provenance;
- a soft/semantic signal compensates source, factual, or policy hard failure;
- a mandatory anti-gaming case is missed;
- synthetic pricing is presented as observed provider cost.

## Reproduction

Focused gate tests:

```bash
python -m unittest discover -s tests/calibration -p 'test_*.py' -v
```

The current worker execution ran the exact persisted gate/test code in an isolated local harness and returned `8/8 PASS`. A network clone was unavailable in the worker shell, so repository-wide clean-checkout validation is delegated to GitHub Actions / integrator evidence rather than claimed locally.

## Files

- `experiments/calibration/release_gate.py`
- `experiments/calibration/current_evidence_v001.json`
- `experiments/calibration/release_gate_report_v001.json`
- `tests/calibration/test_release_gate.py`
- `docs/evals/calibration/release_gate_v001.md`
