# Experimental Report — evidence-bounded consolidation

`TASK: W004-T015-A01`  
`REPORT_STATUS: CONSOLIDATED_CURRENT_EVIDENCE`  
`BASE_STATE_VERSION: 0024`  
`BASE_COMMIT_SHA: 83a5ffc1eacdd245773845eeae9d4542aa683c4f`  
`PRODUCTION_READINESS_CLAIM: NOT_MADE`

## 1. Purpose and evidence contract

This report closes the packaging gap identified as blind-review finding F-007 by consolidating the versioned experimental evidence that already exists in the repository. It is an evidence report, not a release approval and not a production-readiness declaration.

Every material statement is interpreted under one of these evidence classes:

- **FACT** — directly observed and persisted in a versioned repository artifact or an identified CI execution.
- **DIAGNOSTIC_EVIDENCE** — useful controlled/synthetic/fixture evidence that does not justify calibration, provider selection or production generalization.
- **INFERENCE** — a reasoned interpretation of facts; never treated as an observed measurement.
- **UNKNOWN** — evidence is absent or was not observable; no replacement value is inferred.
- **PENDING / BLOCKED** — a defined evidence-producing step has not executed, or requires an external action/input that is not currently available.

These classes must not be averaged into a readiness percentage. A hard `FAIL`, `REVIEW_REQUIRED`, `BLOCKED`, `PENDING`, `PRODUCTION_UNKNOWN` or `UNKNOWN` remains visible even when adjacent mechanics are proven.

## 2. Executive evidence summary

| Area | Current posture | Evidence class | Boundary |
|---|---|---|---|
| source → exact 3×3 jobs → evaluation → repair → aggregate mechanics | `PROVEN` within `MECHANICS_ONLY` | FACT | deterministic-stub mechanics, not provider/content-quality evidence |
| persistent RunStore reopen/resume and lossless 9/9 join | `PROVEN` within controlled proof | FACT | no production load claim |
| source/factual/policy non-compensation | `PROVEN` within controlled proof | FACT | representative production recall remains unmeasured |
| targeted FAIL→repair→fresh re-evaluation→PASS lineage | `PROVEN` within controlled proof | FACT | real-model convergence/quality remains unknown |
| telemetry schema, retry/repair separation and N/A-safe usage/cost semantics | `PROVEN` mechanically | FACT | real provider latency/usage/cost remains unknown |
| audience feature + anti-gaming contract | anti-gaming `PASS`; thresholds `DIAGNOSTIC_ONLY` | FACT + DIAGNOSTIC_EVIDENCE | no calibrated numeric thresholds |
| target→human confusion matrix | `BLOCKED / PENDING` | PENDING / BLOCKED | requires genuine independent human gold |
| human→evaluator confusion matrix | `BLOCKED / PENDING` | PENDING / BLOCKED | requires genuine independent human gold |
| parser/source-trust behavior on current W004 fixtures | `PROVEN` within fixture scope | FACT | parser implementation winner and raw-byte/OCR generalization remain pending |
| clean task-specific release smoke | `PASS` | FACT | internal release mechanics only |
| provider/model quality | `PRODUCTION_UNKNOWN / BLOCKED` | UNKNOWN / BLOCKED | no authorized observed provider run |
| provider latency / usage / commercial cost | `PRODUCTION_UNKNOWN / BLOCKED` | UNKNOWN / BLOCKED | no authorized observed provider run + eligible pricing provenance |
| semantic backend incremental value | `NOT_RUN / PENDING` | PENDING | requires valid development human gold |
| production/release readiness | `PENDING` | PENDING | final fan-in and open gates remain |

## 3. System architecture under test

### 3.1 Architecture flow

The integrated architecture is evidence-driven rather than provider-driven:

1. **source/provenance boundary** — source identity and structural provenance are retained; table facts are gated on role/unit/period evidence where applicable;
2. **typed 3×3 planning** — three audience levels × three native formats produce exactly nine keyed jobs;
3. **provider-neutral generation boundary** — the orchestration mechanics do not require a specific model/provider;
4. **evaluation** — source, deterministic factual and policy checks act as non-compensating hard gates; audience/semantic signals cannot override them;
5. **targeted branch repair** — diagnostic failure codes select local repair directives; accepted sibling outputs remain immutable;
6. **fresh re-evaluation** — every repaired attempt must run fresh source/factual/policy gates with new execution identities;
7. **persistent orchestration** — RunStore persists branch/run states and supports checkpoint/reopen/resume;
8. **telemetry** — run/job/operation-attempt events preserve latency, retry/repair lineage, failures/review states and guarded usage/cost fields;
9. **evidence cockpit** — renders existing versioned artifacts and explicit evidence states without creating a second truth store;
10. **release packet** — carries observed proof, provenance and unresolved evidence gaps forward without filling unknowns by inference.

Primary implementation/evidence references include:

- `src/suno_content/orchestration/**`
- `src/suno_content/runstore/**`
- `src/suno_content/grounding/**`
- `src/suno_content/evals/audience/**`
- `src/suno_content/repair/**`
- `src/suno_content/telemetry/**`
- `src/suno_content/cockpit/**`
- `experiments/w003_e2e/run_proof.py`
- `scripts/release_smoke/run_release_smoke.py`

### 3.2 Architecture evidence

**FACT.** The W003 E2E proof materializes exactly nine jobs (`BEGINNER|INTERMEDIATE|ADVANCED × ARTICLE|CAROUSEL|SHORT_VIDEO`), executes them through the integrated async orchestration/RunStore path, performs one controlled quality repair and one independent transport retry, reopens persisted state, and completes a lossless 9/9 join.

**FACT.** W004-T012 executed the release smoke in a clean GitHub Actions checkout and observed `job_count=9`, `joined_output_count=9`, final phase `complete`, focused release-smoke pytest `1 passed`, and task acceptance assertions `PASS`.

**BOUNDARY.** The controlled E2E uses `provider_mode=deterministic_stub` and explicitly persists `evidence_scope=MECHANICS_ONLY`. It is not evidence of provider/model quality, production throughput, or economic efficiency.

## 4. Source trust and parser evidence

### 4.1 Hard source-trust rule

For structured/table facts, retaining a numeric token is insufficient. Source-ready evidence must preserve applicable structural roles such as table, row, column, unit and period. Missing structural provenance cannot be promoted to `PASS`; incorrect non-null provenance is a hard failure.

### 4.2 W004 parser/source-trust bakeoff

**FACT.** W004-T003 expanded the behavior contract across three materially different primary-source families: Copom minutes/reference-scenario data, CVM ITR schema evolution and Petrobras earnings/results tables.

Observed aggregate behavior:

| Probe | Aggregate state | Min value coverage | Min provenance accuracy | Interpretation |
|---|---:|---:|---:|---|
| provenance-preserving reference | `PASS` | 1.0 | 1.0 | safe behavior on current fixtures |
| flat-value-only | `REVIEW_REQUIRED` | 1.0 | 0.0 | values alone are insufficient |
| wrong-role probe | `FAIL` | 1.0 | 0.9048 | role corruption rejected despite full value coverage |
| wrong-unit probe | `FAIL` | 1.0 | 0.9429 | unit/table corruption rejected despite full value coverage |

**FACT.** The task reported `8/8` focused parser tests passing.

**UNKNOWN / PENDING.** Raw source bytes were not available for persisted hash/replay in that experiment (`raw_bytes_sha256=null`), scanned/OCR-heavy behavior is not closed, and multiple viable parser implementations were not compared on identical raw bytes. Therefore parser implementation identity remains `UNLOCKED`; no parser/vendor winner is claimed.

## 5. Factuality, grounding and hard-gate behavior

**FACT.** The integrated decision contract gives source, deterministic factual and policy failures precedence over soft audience/semantic improvements.

**FACT.** The W003 proof contains a non-compensation probe in which audience-clean content with a wrong factual value remains non-PASS because the deterministic factual gate fails.

**FACT.** Targeted repair cannot reuse pre-repair gate results: source, deterministic factual and policy checks require fresh execution IDs after every repair.

**INFERENCE.** This control structure reduces the risk that readability or stylistic improvement launders a factual error into acceptance. It does not by itself establish representative real-model factual precision/recall.

Traceability: `REQ-012`, `REQ-013`, `REQ-017`, `CRIT-001`; principal risks `RISK-0001`, `RISK-0005`, `RISK-0021`.

## 6. Audience adaptation metrics and calibration posture

### 6.1 Implemented diagnostic surface

The evaluation framework has versioned PT-BR readability, finance terminology/ontology, concept/context coverage and audience complexity diagnostics. The calibration gate keeps `generation_target_level`, `human_gold_level` and `evaluator_predicted_level` as distinct variables.

The executable metric contract can compute, when valid development gold exists:

- target→human confusion matrix;
- human→evaluator confusion matrix;
- per-level precision, recall, F1 and support;
- macro precision, recall and F1;
- accuracy.

Held-out rows are rejected from calibration input.

### 6.2 Current calibration state

**FACT.** The W004 corpus freezes six source identities: four development and two held-out, split at source-document level with held-out tuning exposure forbidden.

**FACT.** Thirty-six natural development outputs are frozen: `4 development sources × 3 formats × 3 requested audience levels`. `human_gold_level` is null and target labels are not gold.

**FACT.** The blind bank and schemas support two independent primaries plus adjudication, and agreement tooling supports raw agreement, Cohen's kappa, quadratic weighted kappa, confusion matrix and deterministic adjudication queue.

**FACT.** Current threshold posture remains `freeze_allowed=false`, numeric thresholds remain null and audience calibration remains `DIAGNOSTIC_ONLY/NOT_COMPUTABLE` until genuine independent human evidence exists.

### 6.3 Target → human confusion matrix

`STATUS: BLOCKED / PENDING`

| Human \ Target | Beginner | Intermediate | Advanced |
|---|---:|---:|---:|
| Beginner | PENDING | PENDING | PENDING |
| Intermediate | PENDING | PENDING | PENDING |
| Advanced | PENDING | PENDING | PENDING |

Required evidence before population:

1. a genuine independent `PRIMARY_A` human stream over the complete frozen development bank;
2. a second genuinely independent `PRIMARY_B` human stream;
3. pre-adjudication agreement calculation;
4. adjudication under the versioned protocol where triggered;
5. versioned human-gold provenance.

Requested generation targets must never be copied into this matrix as truth.

### 6.4 Human → evaluator confusion matrix

`STATUS: BLOCKED / PENDING`

| Evaluator \ Human gold | Beginner | Intermediate | Advanced |
|---|---:|---:|---:|
| Beginner | PENDING | PENDING | PENDING |
| Intermediate | PENDING | PENDING | PENDING |
| Advanced | PENDING | PENDING | PENDING |

This matrix requires valid human gold first. No pseudo-human, model-as-human, target-as-gold or unprovenanced substitute is acceptable.

Traceability: `REQ-004`, `REQ-005`, `REQ-006`, `REQ-010`, `REQ-011`, `REQ-016`, `REQ-019`; assumptions `A-0004`, `A-0006`, `A-0009`, `A-0010`; risks `RISK-0002`, `RISK-0003`, `RISK-0004`, `RISK-0014`, `RISK-0020`, `RISK-0023`.

## 7. Anti-gaming evidence

**FACT.** The calibration/release gate reports `anti_gaming.status=PASS` for the integrated deterministic anti-gaming evidence.

Mandatory failure modes include:

- jargon stuffing;
- sentence chopping / fragmentation;
- acronym manipulation;
- required concept deletion.

The evidence packet also carries alias stuffing and glossary dumping cases.

**FACT.** The anti-gaming contract is stronger than the current human calibration evidence: it is executable on controlled fixtures, while audience-level threshold calibration remains unavailable without independent human gold.

**BOUNDARY.** Anti-gaming PASS is not equivalent to calibrated audience-level accuracy or representative human preference.

## 8. Targeted repair evidence

**FACT.** The targeted repair layer maps evaluator failure codes to typed local directives rather than generic self-reflection. Retrieval/extraction failures such as `RETRIEVAL_MISS` and `EXTRACTION_AMBIGUITY` are not treated as prose-rewrite problems.

**FACT.** Controlled repair evidence begins with `beginner:carousel` in `FAIL`, derives directives for factual correction, concept restoration and first-use explanation, mutates only the failed branch, runs fresh hard gates and reaches `PASS` in one repair attempt.

**FACT.** The clean W004-T012 smoke persisted distinct before/after hashes:

- before: `2daec349f65ac35140f7c35cf78cfe22ef9b8c53516ea63f7884ba80a9691ee8`;
- after: `c031b71292c25cdb4c28605945f7df8f19c399d5fb9eef4b58b6dbbfc1b0a64e`;
- before status: `FAIL`;
- after status: `PASS`;
- fresh hard gates: `true`;
- accepted siblings immutable: `true`.

**UNKNOWN.** Representative real-model repair convergence, quality, latency and cost have not been measured.

## 9. Telemetry and auditability

The versioned telemetry model records run/job/operation-attempt lineage, stage duration, transport retry vs quality repair, terminal failure/review visibility, optional provider usage and guarded cost.

**FACT.** Unobserved usage/cost is represented as `null/N/A`, not zero.

**FACT.** Cost can only be produced from complete observed usage plus a versioned pricing table; synthetic demo pricing is not eligible as provider commercial cost evidence.

**FACT.** The controlled telemetry demo demonstrates the mechanism, including one transport retry, one quality repair and preserved failed/review-required branches. That synthetic demo cost is diagnostic only.

**FACT.** The W003/W004 clean mechanics proof deliberately leaves provider usage and observed cost absent rather than backfilling values.

Traceability: `REQ-020`, `PAIN-004`; risks `RISK-0005`, `RISK-0017`, `RISK-0019`, `RISK-0021`, `RISK-0022`.

## 10. Provider/model quality, latency, usage and cost

`STATUS: PRODUCTION_UNKNOWN / BLOCKED`

| Measure | Current value | Evidence class | What would make it observable |
|---|---|---|---|
| provider/model content quality | `PRODUCTION_UNKNOWN` | UNKNOWN / BLOCKED | authorized observed provider runs + source/human quality evidence |
| end-to-end/provider latency | `PRODUCTION_UNKNOWN` | UNKNOWN / BLOCKED | observed provider/model/version runs |
| provider-reported usage | `PRODUCTION_UNKNOWN` | UNKNOWN / BLOCKED | observed provider usage fields with provenance |
| commercial cost | `PRODUCTION_UNKNOWN` | UNKNOWN / BLOCKED | observed complete usage + eligible official pricing provenance |
| provider/model preference | `NOT_AUTHORIZED` | PENDING | comparable observed evidence; no preference by demo |

A manual secret-safe execution/export/import path exists in `experiments/provider_manual/**` and `.github/workflows/provider-manual-evidence.yml`.

**FACT.** The safe no-secret demonstration returned `BLOCKED_NO_CREDENTIAL`, `observed_run=false`, `mechanics_eligible_for_t007=false` and did not fabricate latency, usage, cost or content-quality evidence.

**FACT.** Strict import rejects non-observed/incomplete mechanics evidence, synthetic/ineligible pricing, missing model-version provenance, missing response fingerprint, secret-like fields and embedded content-quality claims.

**BOUNDARY.** Harness readiness is not provider evidence. No provider/model quality, speed, usage, cost or preference conclusion is made in this report.

## 11. Clean release smoke and parser/cockpit evidence

W004-T012 converted an earlier compile-only limitation into observed task-specific clean CI execution.

**FACT.** GitHub Actions run `35605139400`, job `106350276042`, execution head `bd6e90021aa007be23de555d3751612372192a4b`, Ubuntu 24.04.5 LTS, Python 3.13.15, conclusion `success`.

**FACT.** The task-specific focused test reported `1 passed in 0.45s`.

**FACT.** The smoke verified:

- exact 9/9 mechanics;
- persisted FAIL→repair→PASS lineage;
- fresh hard gates and sibling immutability;
- cockpit evidence markers and before/after hashes;
- parser reference `PASS`, flat-value `REVIEW_REQUIRED`, wrong-role `FAIL`, wrong-unit `FAIL`;
- parser implementation `UNLOCKED`;
- human matrices still blocked/pending;
- provider quality/latency/cost still production-unknown/blocked;
- semantic ablation still pending;
- no production-readiness claim.

Persisted evidence:

- `docs/release/release_smoke/W004-T012-A01-manifest.json`
- `docs/release/release_smoke/W004-T012-A01-ci-provenance.json`
- GitHub Actions artifact `10641632565`, digest `sha256:18e17939b212c6cb43a36d5a7d3298378c81792b9b0047b954324d760c5787f4`

## 12. Evidence cockpit

**FACT.** The evidence cockpit is a read-only projection over persisted RunStore, telemetry, calibration and proof artifacts. It does not create a second authoritative evidence store.

It renders:

- 3×3 audience/format evidence cells;
- source/run/job/attempt provenance;
- source traceability;
- repair lineage with before/after states and hashes;
- telemetry and retry/repair distinctions;
- explicit `PROVEN`, `DIAGNOSTIC_ONLY`, `NOT_COMPUTABLE`, `NOT_RUN`, `NOT_COMPARABLE`, `PRODUCTION_UNKNOWN`, `FAIL`, `REVIEW_REQUIRED` states;
- no aggregate readiness score.

**PENDING.** Blind review found that the current cockpit is a generated read-only HTML surface and may be weaker than a strict interactive application/dashboard reading. Recipient-facing interaction is a separate adherence issue and must not be hidden by the cockpit's audit strengths.

## 13. Trade-offs and design decisions

### 13.1 Hard gates over aggregate scoring

Trade-off: stricter rejection/review can reduce apparent pass rate and increase intervention. Benefit: factual/source/policy failures cannot be averaged away by readability or other positive soft metrics.

### 13.2 Targeted repair over generic retry

Trade-off: typed repair requires more evaluator structure and explicit failure taxonomy. Benefit: repairs are local, bounded, auditable, and do not silently rewrite accepted siblings.

### 13.3 Provider neutrality over early provider lock-in

Trade-off: no provider-specific optimization or claimed winner yet. Benefit: orchestration, telemetry and evidence contracts can be exercised without turning an unobserved provider preference into architecture truth.

### 13.4 Diagnostic audience metrics over premature thresholds

Trade-off: current report cannot publish a final accuracy threshold or calibrated confusion matrices. Benefit: target-as-gold circularity and tiny-sample overconfidence are explicitly prevented.

### 13.5 Structural provenance over value-only extraction

Trade-off: ambiguous/flat extractions may be held for review even when all numeric tokens are present. Benefit: row/column/unit/period corruption is not silently accepted.

### 13.6 Explicit unknowns over polished completeness

Trade-off: the packet visibly contains blocked and unknown sections. Benefit: it is auditable and does not fabricate human/provider evidence to make the deliverable appear complete.

## 14. Blind-review reconciliation

The W004-T013 adversarial review returned `BLIND_REVIEW: NOT_PASS`. This report directly addresses only finding F-007 and must not be interpreted as closing the other findings.

| Finding | Current status after this report | Notes |
|---|---|---|
| F-001 final real demo video absent | OPEN | outside T015; final real artifact still required |
| F-002 raw PDF/text recipient ingest not demonstrated | OPEN | outside T015 |
| F-003 interactive app/dashboard adherence risk | OPEN | outside T015 |
| F-004 central proof is deterministic-stub mechanics | CONTROLLED / DISCLOSED | evidence boundary preserved |
| F-005 independent human calibration absent | BLOCKED / PENDING | explicitly represented, not fabricated |
| F-006 real provider evidence absent | BLOCKED / PRODUCTION_UNKNOWN | explicitly represented, not fabricated |
| F-007 consolidated experimental report absent | ADDRESSED BY T015 ARTIFACT | this document |
| F-008 actual <=5:00 duration unverified | OPEN | only final recording can close |
| F-009 traceability wording scope | ORCHESTRATOR FOLLOW-UP | no canonical edit by this worker |
| F-010 submission logistics/owner/workflow unknown | OPEN | retained as unknown |

## 15. Traceability summary

### Requirements and pains materially covered by this report

- `PAIN-001` — multi-audience complexity: frozen corpus, audience diagnostics and explicit human-calibration gap.
- `PAIN-002` — simplification losing nuance: hard factual/source gates, concept coverage and targeted repair.
- `PAIN-003` — generic LLM judge subjectivity: independent gold protocol, non-compensating deterministic gates, semantic ablation pending valid gold.
- `PAIN-004` — professional auditability: provenance, persistent state, telemetry, repair lineage and cockpit.
- `PAIN-005` — scalable trusted multichannel transformation: exact 3×3 mechanics proven; quality/economics still evidence-bounded.
- `REQ-001` — structural source-trust/parser evidence; recipient-facing raw ingest still pending.
- `REQ-002` — explicit graph/state and persistent RunStore mechanics.
- `REQ-003`, `REQ-007..009` — exact 3×3 native-format mechanics.
- `REQ-004..006`, `REQ-010..011` — audience diagnostics/calibration machinery; genuine human calibration pending.
- `REQ-012` — factual/grounding hard gates.
- `REQ-013`, `REQ-017` — targeted repair and fresh re-evaluation.
- `REQ-014`, `REQ-018` — evidence cockpit audit surface; stronger interactive recipient UI still pending.
- `REQ-015` — reproducible GitHub/CI history.
- `REQ-016` — automated evaluation/release-smoke suites.
- `REQ-019` — report and confusion-matrix sections; observed matrices remain blocked.
- `REQ-020` — provider telemetry/cost contract; observed values remain blocked.
- `REQ-021` — reproduction/reporting instructions.
- `REQ-022`, `REQ-023` — final video remains outside this report and open.
- `CRIT-001` — hard factual/eliminatory requirements are non-compensating.

Canonical detail remains in `SYSTEM/TRACEABILITY_MATRIX.md`; this report does not replace it.

## 16. Assumptions and risks carried forward

### Assumptions not closed

- `A-0001`: final video operational interpretation <=5:00 is controlled planning, actual runtime still unobserved.
- `A-0002`: internal owner/decision-maker remains unknown.
- `A-0003`: transformation + trust layer as primary value remains a supported hypothesis, not measured ROI.
- `A-0004`: calibrated audience levels need independent gold; preparation supports this but evidence remains incomplete.
- `A-0006`: no partner-provided gold dataset; two genuine independent humans still required.
- `A-0007`: brand-voice imitation remains optional/open.
- `A-0008`: parser reliability is partially supported structurally; raw-byte/OCR and recipient ingest remain open.
- `A-0011`: operational partner gains such as time/rework/reuse remain unmeasured.

### Principal active/residual risks

- `RISK-0001`: factual drift strongly controlled in the core but never assumed eliminated.
- `RISK-0002`, `RISK-0014`: gaming/format effects reduced by anti-gaming gates; human calibration still required.
- `RISK-0003`, `RISK-0020`, `RISK-0023`: circular or non-independent human gold remains an external validity gate.
- `RISK-0004`: six-source corpus is broader but still a sample-limitation risk; no population generalization claim.
- `RISK-0005`: bounded repair/retry mechanics reduce runaway-loop risk; real-model convergence remains unknown.
- `RISK-0006`: final real <=5:00 video remains critical/open.
- `RISK-0010`: structural corruption detection improved; raw PDF/OCR extraction remains open.
- `RISK-0011`: submission owner/workflow remains unknown.
- `RISK-0017`, `RISK-0019`, `RISK-0022`: provider drift/cost/evidence risks remain until real authorized observed runs exist.
- `RISK-0021`: mechanics-vs-production evidence laundering is actively guarded by explicit scope labels.
- `RISK-0024`: recipient-facing interactive/raw-ingest proof remains open.
- `RISK-0025`: report fragmentation is reduced by this consolidated artifact.

## 17. Reproducibility

### 17.1 Clean-start foundation + release smoke

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --disable-pip-version-check --no-cache-dir \
  'pydantic==2.13.4' 'pytest==9.0.2'
python experiments/foundation_regression/run_foundation_regression.py
python scripts/release_smoke/run_release_smoke.py \
  --workdir /tmp/academy-suno-release-smoke \
  --output /tmp/academy-suno-release-smoke/manifest.json
python -m pytest -q tests/release_smoke/test_release_smoke.py
```

### 17.2 Parser/source-trust bakeoff

```bash
python3 experiments/parser_w004/run_bakeoff.py \
  --output /tmp/parser-w004-results.json
python3 -m unittest discover -s tests/parser_w004 -p 'test_*.py' -v
```

### 17.3 Human-calibration preparation validation

```bash
python experiments/human_calibration/validate_preparation.py
```

Agreement/matrix computation must only be run after two genuine primary human streams exist. See:

- `docs/evals/human_calibration/protocol_v001.md`
- `experiments/human_calibration/README.md`
- `experiments/human_calibration/compute_agreement.py`

### 17.4 Calibration release gate

```bash
python -m unittest discover -s tests/calibration -p 'test_*.py' -v
```

Expected current evidence posture remains diagnostic/blocked where human/provider inputs are absent.

### 17.5 Provider manual path

Do not treat path readiness as observed provider evidence. Operator instructions and strict import semantics are in:

- `docs/provider_manual/README.md`
- `.github/workflows/provider-manual-evidence.yml`

A real run must be authorized and preserve provider/model/version/endpoint, observed usage/latency and eligible official pricing provenance before corresponding claims are populated.

## 18. Artifact index

### Consolidated/current release evidence

- `docs/report/EXPERIMENTAL_REPORT.md` — this report.
- `docs/submission/SUBMISSION_PACKET.md` — recipient-facing evidence index and gap register.
- `docs/release/EVIDENCE_PACKET.md` — upstream release-preparation evidence shell.
- `docs/release/FINAL_REVIEW_CHECKLIST.md` — release stop conditions.
- `docs/release/release_smoke/W004-T012-A01-manifest.json` — observed clean-smoke task manifest.
- `docs/release/release_smoke/W004-T012-A01-ci-provenance.json` — observed CI provenance.

### Human/audience evidence

- `data/evals/w004/source_manifest_v001.json`
- `data/evals/w004/frozen_outputs_manifest_v001.json`
- `data/evals/w004/annotation_schema_v001.json`
- `data/evals/w004/annotation_plan_v001.json`
- `docs/evals/human_calibration/protocol_v001.md`
- `experiments/human_calibration/compute_agreement.py`
- `experiments/human_calibration/validate_preparation.py`
- `experiments/calibration/release_gate_report_v001.json`

### Mechanics/repair/telemetry evidence

- `experiments/w003_e2e/run_proof.py`
- `experiments/repair/run_controlled_repair.py`
- `experiments/telemetry/demo_summary_v001.json`
- `scripts/release_smoke/run_release_smoke.py`

### Parser/source evidence

- `experiments/parser_w004/observed_results.json`
- `docs/parser_w004/README.md`

### Provider evidence path

- `experiments/provider_manual/**`
- `docs/provider_manual/README.md`
- `docs/provider_manual/provider-observed-evidence-v1.schema.json`

### Canonical traceability/risk context

- `SYSTEM/TRACEABILITY_MATRIX.md`
- `SYSTEM/ASSUMPTION_RISK_REGISTER.md`
- `SYSTEM/STATE.md`

## 19. Current conclusion

**FACT:** internal mechanics, repair lineage, evidence-cockpit rendering contract, source-trust fixture behavior and clean task-specific release smoke have versioned observed evidence in their explicitly limited scopes.

**DIAGNOSTIC_EVIDENCE:** audience metrics and anti-gaming controls are useful and executable, but numeric audience thresholds and human-level classification performance are not calibrated.

**BLOCKED / UNKNOWN:** genuine two-human calibration, observed provider/model quality, provider latency/usage/commercial cost and provider preference are unavailable and remain explicit.

**PENDING:** semantic ablation on valid human gold, recipient-facing raw-ingest/interactive adherence work, final real <=5:00 video and final W004 release fan-in/review.

Therefore this report makes **no production-readiness claim** and no provider/model/parser implementation preference. Its purpose is to make the current evidence — including missing evidence — reconstructible and reviewable without fabrication.
