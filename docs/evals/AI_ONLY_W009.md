# W009-T001 — AI-only source-grounded diagnostic harness

`TASK_ID=W009-T001`; `ATTEMPT_ID=A01`; `DESIGN_STATUS=DIAGNOSTIC_IMPLEMENTED`.

## Objective and evidence class

The operator requested exclusively AI-based audience evaluation, not human reviewers. This task prepares an **offline, deterministic pre-judge harness** and a reproducibly blinded candidate packet for future AI-model evaluation. It implements actual source/number/direction/period etc checks through the existing `suno_content.factual.checks.evaluate_case` code and reads the canonical `AudienceLevel` / `OutputFormat` enums for exact 3 × 3 branch validation.

It does **NOT** call a provider or model judge; `judge_status=NOT_RUN` is always emitted by the current implementation. No human labels, human-gold agreement, model quality metrics, production thresholds, ROI, user comprehension, or production readiness may be inferred from this result. A PASS on a **SYNTHETIC_FIXTURE** demonstrates only the bounded heuristic + integrity tests, not financial correctness on primary-source documents.

## Input contract / evidence limits

JSON list of runs; each has:

- `schema_version: ai_only_w009.input.v1`;
- stable `run_id`, `source_group_id` representing the primary financial document/event (do not partition article and PDF editions separately), `evidence_class` (`SYNTHETIC_FIXTURE`, `SOURCE_GROUNDED_DIAGNOSTIC` or `PROVIDER_OBSERVED` — self-declared, not provider-attested);
- `generator: {provider, model, version}` or explicit `synthetic_fixture` identity for unit fixtures. `judge` optional metadata only; same generator provider+model+version as judge is rejected, but mere different naming **does not prove** independence;
- `source: {status: PASS|FAIL|REVIEW_REQUIRED, spans:[{span_id, text}]}`, nonempty unique IDs; input source hash/source integrity must be verified by the upstream system for external evidence;
- up to nine `variants`, each `{audience, format, output, hard_gates}` with exactly five explicit mandatory source/factual/policy/schema/provenance statuses. Unknown, missing or duplicate branches reject input; absent branches produce REVIEW_REQUIRED rather than false acceptance.

The `source.status` and variant hard gates are supplied diagnostics, not independently recomputed trust/authentication checks. Factual evidence is additionally checked by existing deterministic `evaluate_case` and may worsen the overall status but never improve an upstream FAIL/REVIEW. The classifier does **not** check every financial sentence; its heuristics have false-negative and false-positive risk. `PASS` means no failure observed by this specific harness, not that all facts have been validated.

## Blinding / splitting preregistration

- Split function: `SHA256(split_salt + "|" + source_group_id)` first 12 hex digits mod 100, buckets 0..59 DEV, 60..79 CALIBRATION, 80..99 HELD_OUT. These are deterministic allocation shares chosen **before** any data, not accuracy thresholds.
- Source group stays in the same split across multiple runs / formats; the same source or revisions must share a stable group ID upstream. Linked-source equivalence beyond identical ID is not proved by hashing.
- A `blind_id` is SHA256 of split salt + run ID + target level + target format, truncated to 24 hex chars. This is a deterministic pseudonym, **not a cryptographic anonymization or a privacy proof**.
- Blinded packets include only `target_audience`, `target_format`, selected source span texts, candidate output and rubric version `machine_judge_secondary_v1_NOT_EXECUTED`. They omit generator ID, run ID and oracle outcome. Target audience and format must remain visible for the task.
- A future real judge adapter must version provider/model/prompt/rubric, implement order-swapped repeated blind judging, independent model checks, immutable provider observations, paired dataset comparisons and source-group held-out guard. This task does **not** fabricate responses by the model.

## Non-compensatory decisions

1. Fail if any of five mandatory hard gates, or existing deterministic factual evaluator, returns FAIL.
2. Review if any of those returns REVIEW_REQUIRED, or at least one of nine branches is missing.
3. PASS only when every supplied gate and bounded factual check passes and all nine branches are present.
4. No model/judge score may override FAIL or REVIEW_REQUIRED. No adaptive threshold freeze occurs.
5. Reject nonempty `human_gold` or `human_annotations` fields rather than renaming AI output.

## Reproducibility

```bash
python -m pip install "pydantic==2.13.4"
PYTHONPATH=src python -m unittest discover -s tests/ai_only_w009 -p 'test_*.py' -v
PYTHONPATH=src python experiments/ai_only_w009/harness.py \
  --input /path/to/controlled-corpus.json \
  --output /tmp/suno-eval-report.json \
  --blind-output /tmp/suno-blind-packets.json \
  --split-salt "w009-preregistered-split-policy-v1"
```

The JSON examples in `tests/ai_only_w009/test_harness.py` are **synthetic-only**. Real model/API costs are zero **only for the automated offline unit test**, not a promise for future evaluation. Do not commit production source texts, personal inputs or secrets into public repository or put raw blinded packets on Render public staging.

## Benchmark protocol for next iteration

Compare the same source group corpus and seed across: direct ungrounded prompting baseline; source anchored generation; source anchored + deterministic gate; anchored + independent model-judge + targeted repair (if real provider authorized). Keep generator and evaluator independent, model/judge outputs actually observed, order-reversal/repeat observations, source-original tests including percentage/scale/period/direction/conditional/table-role confusions, clean positive cases, source grouped DEV/CAL/HELD_OUT. Log per-run raw metrics and missingness with source hashes; use hard-gate then multidimensional eligible Pareto before any ranking. Missing independent judge and real primary-source test => `PENDING_EVIDENCE`; no arbitrary winner, scalar business utility or audience thresholds from synthetic fixtures.

## Design dependencies / next work

- W008-T003 official corpus and metric preregistration, currently READY; do not promote synthetic unit fixtures to a real financial benchmark.
- W008-T002 accepted schema-transport gap: structured PDF table cells are not passed by `PdfExtraction` → `IngestResult`, so a table role PASS is not certified by this harness.
- Independent generative AI evaluators must be integrated only after provider model identity/cost/data handling are authorized, maintaining result history and controlled source disclosure.
- Current Render Free service is read-only staging; harness is offline, not exposed as unauthenticated public API.
- New auth/security implementation tasks are deprioritized per 2026-10-15 operator directive. **Existing fail-closed source/factual/schema and public-service restrictions remain** and product cannot claim production-ready without required gates.

**Implementation files:** `experiments/ai_only_w009/harness.py`, `tests/ai_only_w009/test_harness.py`, CI `.github/workflows/ai-only-w009.yml`.  
**Evidence class:** CODE_AND_SYNTHETIC_TEST, no real provider judging observed.
