# W008-T003 — Preregistered financial benchmark protocol

`PROTOCOL_ID=W008-T003-FINANCE-CORPUS-v1`  
`TASK_ID=W008-T003` / `ATTEMPT_ID=A01`  
`EVIDENCE_SCOPE=DESIGN_AND_HISTORICAL_SOURCE_INVENTORY`  
`MODEL_BENCHMARK=NOT_RUN` / `HUMAN_GOLD=UNAVAILABLE_BY_OPERATOR_CHOICE`  
`PRODUCTION_READY=FALSE`

## Research question and constraints

Does an end-to-end evidence-grounded 3 audiences × 3 formats (9 outputs) pipeline preserve financial meaning and citations better than simple generation, when evaluated on the **same primary-source documents** at declared cost, latency, provenance and reliability? The answers require actual repeated runs; this file preregisters the method without manufacturing run results.

User's 2026-10-15 D-0019 waiver supersedes original W008 dispatch's independent human stream requirement for **AI-only diagnostics** but does not turn model ratings into human agreement or comprehension evidence. User's D-0023 directive defers **new** authentication/security feature implementation, not critical factual/source/tenant/policy checks. The reference application with arbitrary PDF filesystem paths remains prohibited on public Render Free staging.

## Candidate methods frozen before observations

The four candidate identifiers are fixed in `experiments/corpus_w008/registry.v1.json`:

1. `DIRECT`: source-conditioned generation without claim anchors (baseline; still respects shared input permissions/source byte identity).
2. `ANCHORED`: same generator and source with provenance anchors; **not** yet automatically a reliable financial verifier.
3. `EVAL_REPAIR`: anchored generation + deterministic gates and targeted local repair, refreshing evaluation after each repair.
4. `FULL_3X3`: full nine-native-format run using source-grounded claims, same frozen model/prompt source, evaluation, repair and lossless join.

All models/providers and decoder knobs, dataset inputs, parsing version, prompts, repair iterations, timeout/failure retries, region and concurrency are frozen and recorded **before** each candidate comparison. Run a baseline and all challengers on identical original source-group splits; if an alternative lacks a needed component, label `NOT_RUN` and exclude it from winner claims, rather than quietly changing the workload.

## Financial source sampling, identity and missingness

Primary-source inventory is a **bounded historical record** from accepted `W007-T004-A01`, NOT a new verified run:

| Family | Group ID | Prior evidence | Limitation |
|---|---|---|---|
| Petrobras | `petrobras-2t26` | source-original PDF, SHA-256 present in accepted W007 parser RESULT | structured cells lost in downstream `PdfExtraction` transport; no fresh generation benchmark |
| BCB | `bcb-rpm-2026-1t` | source-original RPM 1T26, SHA-256 in W007 | digital/chart-heavy, no full source-original claim-gold |
| FRASER | `frb-annual-report-1914` | source-original historical Fed report, SHA-256 in W007 | OCR/text layer exists: NOT pure image-only gold and not a Brazilian contemporary source |
| CVM | `cvm-primary-pending` | **NOT_ACQUIRED** | no official CVM source downloaded/hashed; explicitly excluded from observed original benchmark |

The three original URLs and exact original SHA-256 values are recorded in the JSON registry from `experiments/document_parsing_w007/benchmark.py` + `SYSTEM/RESULTS/W007-T004-A01.md`. This task did not contact those URLs, download bytes, validate live availability, obtain reproduction permissions or acquire a CVM document. Never call a 3-document historical inventory a statistically representative financial corpus. Before held-out-quality evaluation, obtain/verify rights, immutable bytes, SHA, document type/issuer/date, page/table/column/period/units, OCR ambiguity and unbiased sampling rationale.

Adversarial controls use the **13 existing synthetically labelled cases** `EXP-C-F01..F12/C01` from `tests/factual/observed_factual_v001.jsonl`. Their registration under real source-group IDs is an **allocation/stratification grouping convenience only**, not a claim that the fabricated cases are text from those source-original PDFs. The validator prevents rebranding these controls as human/source-original observations.

### Leakage guard

Use `source_group_id` as the indivisible statistical block (same event/company filing, revisions, machine-annotated variants and all nine outputs stay together). Partition exactly by accepted W009-T001 `SHA256("w009-preregistered-split-policy-v1" + "|" + group_id)` first 12 hex characters mod 100:

- DEV 0..59, CALIBRATION 60..79, HELD_OUT 80..99.

This is an **allocation policy**, not evidence that with three historical groups all three split sets are populated or balanced. Small data and source families can yield empty sets; never backfill by duplicating the source under a new group ID. The validator asserts equal partition assignment vs the actually integrated W009 harness in a unit test.

### Sampling plan when source-original study is authorized

Prioritize source-group diversity rather than nine-row pseudo-replication: financial results/dense tables (Petrobras), macro policy with quantitative/chart context (BCB), CVM primary regulatory filing (still missing), authentic scanned image-only primary (still missing). Include positive clean statements and adversarial numeric magnitude, scale, negative sign, period, entity attribution, direction, conditional/modal, table role and unsupported causal claims. Predeclare inclusion/exclusion, licensing, failure severity and denominator; log every attempted download/parse/run, not just passing samples.

No invented target count, coverage percentage, cost, latency, effect size or reader preference is frozen here. Source original acquisition/re-run and held-out split sufficiency will determine whether inferential measurements are meaningful.

## Unit, estimand and inference

Source group is the unit of independent comparison; nine formats × three audience tiers are correlated variants **within** that unit. For each method/source/repetition record `run_id`, stable `source_group_id`, raw source SHA, document/parser/provider/model/config and rubric versions, attempted and accepted branches, versions of underlying claims, observed timestamps/tokens/cost and every hard-gate decision.

Paired contrasts are computed source-group-wise between the four alternatives, not by treating each generated page as an independent observation. If sufficient independent paired groups and repetitions exist, estimate group-block confidence intervals (paired BCa with documented degenerate-data fallback), predeclared matched randomization when test assumptions fit; Holm correction applies only to a predeclared family-wise inferential claim. See accepted W005-T009-A02, `docs/decisions/research/DR-5909-cross-cutting-benchmark-methodology.md`.

For sparse initial data, report each group/metric raw value and explicit uncertainty/missingness instead of reporting unstable confidence intervals or pretending a p-value is evidence of business impact.

## Gates, raw metrics, outcome states

Non-compensatory source/factual/policy/schema/provenance/tenant checks occur **before** any utility/Pareto comparisons; an AI judge cannot override a deterministic material FAIL or REVIEW_REQUIRED. A missing nine-branch identity, source hash/cell role or critical metric invalidates a production-grade comparison, not an implied zero error rate.

The v1 registry freezes nine raw metric definitions including numerator/denominator design, dimension/aggregation and evidence required:
- critical false accepts, false support, numeric/period/unit preservation;
- cross-output contradictions, claim/source provenance traceability;
- PT-BR audience clarity/technical contextualization as `AI_ONLY_DIAGNOSTIC`;
- latency p95, full infrastructure/provider cost, recovery integrity.

`false_support_rate` requires source-grounded adjudicable claims; synthetic oracle tests alone are not representative denominator. `cost_total` must include actual compute/transport costs; `0 USD provider invoice` is not automatically `0 USD total cost`. A metric cannot be reduced to `0` to fill a missing observation. Production readiness, ROI and human comprehension are out of scope.

Use raw multidimensional metrics with units/evidence class/missingness, then eligible point Pareto only when objectives are measured; trade-offs should result in `NO_PREFERENCE`. Promotion to any provider/architecture/quality winner requires actual matched source-group evidence, supported practical materiality (not a made-up threshold), repeatability, DRG and reversal criteria.

## Reproducibility and independent checks

```bash
python experiments/corpus_w008/validate_registry.py --output /tmp/w008-corpus-validation.json
PYTHONPATH=src python -m unittest discover -s tests/corpus_w008 -p 'test_*.py' -v
```

The validator checks source hash/ref eligibility, CVM missingness, 13 old synthetic control IDs against the existing oracle, required four candidate definitions and nine metric definitions, partition parity against W009, nonfabricated `point_pareto=null` and `candidate_preference=PENDING_EVIDENCE`. This checks *preregistration quality*, not actual model success or statistical quality.

## Decision Research Gate and reversibility

Baseline is direct prompting; challengers anchored, eval+repair and full 3×3. Evaluated dimensions above, predeclared before real candidates. Decision **`PENDING_EVIDENCE`**, confidence HIGH for machine-readable preregistration, LOW for unobserved relative method quality; no production/default choice.

Re-open this frozen plan on actual source acquisition changing primary coverage, genuine CVM original availability, controlled reader study (if operator revises human waiver), model-cost permission, substantial split leakage, financial table parsing schema improvements or business utility data. Revisions require distinct version/dataset identifier and held-out leakage review, never silently mutate a used scoring rule.

References: `SYSTEM/DISPATCH/W008-T003-A01.md`, `SYSTEM/RESULTS/W007-T004-A01.md`, `SYSTEM/RESULTS/W005-T009-A02.md`, `docs/product/research/W008_T002_GAP_MATRIX.md`, D-0019/D-0023.
