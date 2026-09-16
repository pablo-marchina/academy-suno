# Audience feature probe — B07

This probe exercises the deterministic `audience-features-v001` vector against four anti-gaming patterns:

- explained beginner terminology;
- jargon/alias stuffing;
- sentence chopping;
- required-concept removal.

Run from the repository root:

```bash
python experiments/audience_features/run_probe.py
```

The output is diagnostic only. It intentionally contains no calibrated audience score or pass/fail threshold. Calibration belongs to the independent gold/dev/held-out workflow in W003.
