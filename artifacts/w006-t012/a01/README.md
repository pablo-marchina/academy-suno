# W006-T012-A01 reproducible evidence

This directory records the acceptance contract for the observability/live-ops worker attempt.

The executable evidence lives in `tests/integration/w006/test_observability_live_ops.py` and the exact locked GitHub Actions workflow `.github/workflows/w006-t012-observability.yml`.

The test surface exercises the accepted real/reference 3×3 path and proves, within that scope:

- inbound/outbound W3C `traceparent` propagation;
- nine provider + nine evaluation spans and explicit repair instrumentation;
- safe source/run/job/attempt correlation references;
- low-cardinality metric labels;
- OTLP/HTTP JSON trace/metric/log payloads on standard signal paths;
- default redaction / attribute allowlisting for credentials and private content;
- an opaque cockpit trace link resolved only under exact server-side org/workspace/run scope;
- telemetry/export failure isolation from durable completion and product-event replay;
- durable product events remain the cockpit truth plane.

`acceptance_matrix.json` is a machine-readable statement of required outcomes and evidence boundaries. It is not a production benchmark and does not authorize a backend, sampling, retention, SLO, capacity or production-readiness claim.
