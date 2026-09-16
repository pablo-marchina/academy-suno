# Telemetry audit demo

This experiment exercises the provider-neutral telemetry hooks delivered by
`W003-T007-A01` without depending on a provider SDK.

It demonstrates:

- versioned append-only events with run/job/operation-attempt lineage;
- deterministic stage timing using an injected monotonic clock;
- a transport retry that is distinct from a quality-repair attempt;
- observed metered usage and cost only when a complete usage observation and a
  versioned pricing table are both present;
- preservation of failed/review-required branch states in the aggregate.

Run from a repository checkout with:

```bash
PYTHONPATH=src python experiments/telemetry/runtime_demo.py
```
