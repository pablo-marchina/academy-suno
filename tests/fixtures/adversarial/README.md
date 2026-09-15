# Factual adversarial fixtures — factual-v001

Small, versioned corpus for `W002-T006 / EXP-C` factual hard-gate work.

## Files

- `factual_v001.jsonl` — one self-contained source/output mutation per line.
- Oracle/contract: `experiments/hard_gates/factual_hard_gate_spec_v001.json`.
- Standard-library harness: `experiments/hard_gates/validate_factual_fixtures.py`.

## Coverage

The corpus covers numeric magnitude/scale, period, entity, direction, negation, modality, attribution and table-row role corruption. It also includes unsupported causality, source-extraction ambiguity, retrieval-miss routing and an allowed-rounding control.

Each fixture carries stable fixture/corpus version, source spans, adversarial output, `W001-T004` adversarial reference, executable `W001-T009 Failure.code` implementation code, expected severity/decision/support status, and direct future build targets (`B03` and/or `B08`).

## Invariants

`CRITICAL` factual contradictions must fail and cannot be overridden by a semantic judge. Unresolved material `ERROR` blocks auto-PASS. Low-confidence critical extraction and retrieval misses remain review/unverifiable paths rather than being mislabeled as confirmed unsupported claims.

The table fixture includes row/column/unit context; naked values are intentionally insufficient evidence.

## Reproduction

From repository root:

```bash
python experiments/hard_gates/validate_factual_fixtures.py
```

To compare a future B03/B08 evaluator output with the frozen oracle:

```bash
python experiments/hard_gates/validate_factual_fixtures.py \
  --observed path/to/observed_results.jsonl
```

Observed rows use the schema declared in `factual_hard_gate_spec_v001.json`.

## Scope

These are synthetic deterministic fixtures. They do not claim production recall, threshold calibration or semantic-backend quality. Their purpose is to prevent known critical factual mutations from reaching auto-PASS and to give B03/B08 a reproducible contract.
