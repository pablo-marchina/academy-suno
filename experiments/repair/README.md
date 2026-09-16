# Targeted repair controlled proof

Run with:

```bash
PYTHONPATH=src python experiments/repair/run_controlled_repair.py
```

The fixture intentionally begins with a deterministic factual mismatch plus missing-concept/unexplained-jargon diagnostics. The repair callback receives only the failing branch and a typed request derived from those findings. The demo then re-evaluates with fresh SOURCE / DETERMINISTIC_FACTUAL / POLICY run IDs, reports before/after metric deltas and checks accepted-sibling hashes are unchanged.

This is a controlled proof of lifecycle/invariants, not evidence that arbitrary model-generated repairs converge in production.
