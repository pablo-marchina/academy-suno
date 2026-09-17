# B13 Evidence Cockpit

The cockpit is a **read-only projection** over the evidence the repository already owns. It does not create a second readiness database and it never writes back into `SQLiteRunStore`, proof reports, telemetry, calibration evidence, `STATE`, the task ledger, or wave manifests.

## Evidence contract

The UI exposes the eight evidence states required by W004-T001 exactly as written: `PROVEN`, `DIAGNOSTIC_ONLY`, `NOT_COMPUTABLE`, `NOT_RUN`, `NOT_COMPARABLE`, `PRODUCTION_UNKNOWN`, `FAIL`, and `REVIEW_REQUIRED`.

There is deliberately **no aggregate green/readiness score**. Each claim and each 3×3 job keeps its own state. A factual `FAIL` therefore remains a visible failure even if unrelated readability, latency, or audience diagnostics look good. Missing evidence is rendered as `N/A` or the appropriate unknown state instead of zero or pass.

Every job-level trace exposes source, run, job, attempt when persisted, evidence scope, selected artifact reference, and observation timestamp when available. A missing attempt/source field is shown as `N/A`; the cockpit does not invent lineage.

## What it consumes

Supported inputs are existing versioned artifacts:

- final state from the canonical `SQLiteRunStore`, or the exported append-only `runstore_history_v001.json` produced by the W003 proof;
- W003/W004 proof report JSON, including `repair_lineage` and claim-level `evidence_classification`;
- telemetry summary JSON and optional event JSONL for operation-attempt lineage;
- calibration evidence JSON such as `experiments/calibration/current_evidence_v001.json`.

The generated HTML is a disposable presentation snapshot. Reloading/re-rendering from the source artifacts is the authoritative refresh path.

## Run immediately with repository diagnostics

```bash
PYTHONPATH=src python app/evidence_cockpit.py --output /tmp/evidence-cockpit.html
```

With no explicit inputs, the app uses the repository's current calibration artifact and `experiments/telemetry/demo_summary_v001.json`. That telemetry demo intentionally contains a `FAIL`, a `REVIEW_REQUIRED`, and synthetic pricing. The cockpit keeps the raw synthetic cost visible as diagnostic evidence but shows production/provider cost as `N/A`; it must not be used as real provider economics.

The diagnostic telemetry artifact does not contain a full source or all nine branches, so source fields and absent 3×3 cells remain `N/A`/`NOT_RUN`. That is expected evidence preservation, not a UI error.

## Render the complete W003 mechanics proof

Generate the already-defined W003 evidence artifacts:

```bash
PYTHONPATH=src python experiments/w003_e2e/run_proof.py --output-dir /tmp/w003-proof
```

Then render them:

```bash
PYTHONPATH=src python app/evidence_cockpit.py \
  --runstore-history /tmp/w003-proof/runstore_history_v001.json \
  --proof-report /tmp/w003-proof/proof_report_v001.json \
  --telemetry-events /tmp/w003-proof/telemetry_events_v001.jsonl \
  --output /tmp/evidence-cockpit.html
```

When a proof report is selected and no separate telemetry summary is supplied, the cockpit consumes the report's embedded telemetry summary. This preserves the proof's exact run identity instead of accidentally mixing it with the repository telemetry demo.

## Live RunStore path

For a persisted run that still has its SQLite file:

```bash
PYTHONPATH=src python app/evidence_cockpit.py \
  --runstore-db /path/to/runstore.sqlite3 \
  --run-id <exact-run-id> \
  --telemetry-summary /path/to/telemetry-summary.json \
  --telemetry-events /path/to/telemetry-events.jsonl \
  --calibration /path/to/calibration-evidence.json \
  --output /tmp/evidence-cockpit.html
```

The SQLite path is read through the existing `SQLiteRunStore` adapter; the cockpit does not duplicate its schema.

## UI sections

The HTML contains claim-level evidence states, a fixed beginner/intermediate/advanced × article/carousel/short-video comparison, source traceability, repair before/after with hashes and failure-code deltas, and telemetry for stage latency, transport retry, quality repair, usage, cost provenance, and terminal failures/reviews.

`MECHANICS_ONLY` is displayed as evidence scope when present. It must not be interpreted as provider/model-quality or production-readiness proof. Real provider quality, usage/cost, semantic backend value, parser generalization, and other unresolved W004 evidence stay explicit until their own versioned artifacts exist.
