# Academy Suno — Product Evolution Master Plan (candidate EP-00)

**Captured:** 2026-10-15  
**Authority:** Operator-directed Orchestrator `ORCH-G003-S001`, lease `ORCH-G003`, manual takeover recorded on `control/orchestrator-lease`.  
**Baseline:** `STATE 0064`, `main 2a3b028d4bc4e502a8839f9d984dd6d1bd337b25`.  
**Status:** `PROPOSAL / RESEARCH INTAKE / NOT PRODUCTION APPROVED`.  
**Relationship:** Additive evolution portfolio; `W007` remains the active production-closure wave and its dependency gating is unchanged.

## Executive product hypothesis

Move from source -> exactly 3 audiences × 3 native formats -> hybrid evaluation -> targeted repair -> aggregate to a trusted financial-editorial workflow with structured fact provenance, source-aware numerical checking, nine-output semantic coherence, human-calibrated comprehension, editorial approval and reproducible evidence.

**Do not substitute a separate demo system.** All improvements must reuse the accepted source/run/job/attempt/provenance spine, typed boundaries, secure tenant/resource binding, non-compensatory gates and exact 9-way aggregation.

## Frozen evidence boundary at intake

- Historical 3×3/E2E/repair/reference evidence is accepted only for its stated bounded scope; it is **not** production qualification.
- W006-T014 assessed 17/17 production rows, with only PROD-015 fully PASS at the entry boundary.
- W007-T001 and W007-T004 are accepted; W007-T002-A01 and W007-T005-A01 are immutable BLOCKED attempts.
- W007-T003, T006, T007, T008, T009, T010 are dependency-gated. No W007 worker may be prematurely kicked off.
- T002 retry needs real authenticated/authorized GCP and AWS project contexts, billing/budget, isolated recovery/migration testing authorization and executable same-image deployment path.
- T005 retry needs actual two independent blinded primary annotators per item and a different human adjudicator. LLM annotations are **not** human gold.
- W007-T004 diagnostic parser results do **not** lock a production parser. The trusted extraction contract currently lacks structured table/cell provenance.
- Production readiness = `FALSE / NOT_AUTHORIZED`, SLO/capacity/provider/parser/frontend/deploy winners still evidence-gated.

## Twelve product capabilities and gates

| ID | Capability | Required additions | Evidence required before promotion |
|---|---|---|---|
| M01 | Financial Truth Engine | source fragments with page/table/cell provenance; financial_claim, evidence links, periods, units, qualifiers; immutable source binding | source-original numeric/table gold tests, zero ambiguous accepted critical provenance, E2E 9/9 |
| M02 | Financial Independent Verifier | deterministic math/sign/unit/period checks; optional allowed structured CVM/BCB source reconciliation; distinguish source conflicts | seeded error-detection cases, false alarm rate, reproducible calculations, no silent overrides |
| M03 | Source Revision Watch | approved feeds, source/version hashes, claim diffs, downstream impact + editor notifications | idempotent update/rescan, no auto-publication, revision audit; authorized rights and quotas |
| M04 | Audience Intelligence | richer PT-BR rubrics, concept retention, human comprehension measurement and calibrated classification | two actual blinded annotator streams, independent adjudication, DEV/CAL/HELD_OUT, uncertainty |
| M05 | Cross-Output Consistency | nine-variant claim comparison, projection vs actual, conditionals, time/units and justified omissions; targeted repair | injected contradictions caught, benign differences retained, hard gates non-compensatory, 9/9 |
| M06 | Editorial Trust Workspace | claim/source viewer, 3×3 comparison, comments, assignment, review/approve, revision/CAS and re-eval | safe same-path E2E, cross-tenant/authz tests, concurrent edit tests, actual editorial usability |
| M07 | Policies & Compliance as Code | versioned hard/soft rules per org/format/source/audience; financial recommendation restrictions | no hard override; compliance owner signoff; traceable policy revisions |
| M08 | Suno Evidence Passport | verifiable source→claim→output→eval→repair→approval manifest, safe exports and digests | tamper detection, redaction, no 'absolute truth' claim |
| M09 | Competitive Benchmark Lab | preregistered direct-prompt/facts/eval+repair/Suno baselines; paired source-group data and ablations | raw metrics, uncertainty, missingness, hard-gate then Pareto and valid no-preference |
| M10 | Adaptive Quality/Cost | versioned model/prompt/retrieval/repair policy, budgets, shadow/canary/rollback | human+provider qualification, quality-cost-latency-reliability evidence and safe rollback |
| M11 | Editorial Exports/Integrations | versioned Markdown/HTML/carousel schema/video script, scoped CMS sandbox when authorized | roundtrip validation, approval & authz gates, zero autonomous social publication |
| M12 | Editorial Value Analytics | versioned business events, time-to-approval/rework/approved-cost, comparison to manual baseline | deduped observed event data, privacy, controlled pilot, no fabricated ROI/causality |

## Cross-cutting contracts

- **Safety / finance:** source hash, line/table provenance, critical fact/source/policy/schema failures fail closed; narrative simplicity never outranks material financial accuracy.
- **Multi-tenancy:** user/org/workspace/resource/run binding for every new entity, event, search, export, passport, cursor, queue and cache; independent deny-by-default authorization and redaction.
- **Durability:** no stale same-run overwrite, stable attempt identities, at-least-once remote execution with idempotent acceptance, state↔event logical consistency, replay/resume, backup/restore and rollback proof.
- **Experiments:** frozen datasets, source-group correlated analysis, honest missingness, human labels classified separately from model sensors, no scalar winner by intuition.
- **Delivery:** same live product path in UI, APIs, traces, exports, docs, experiments and technical video (<= 5 min). Out of scope: publishing to networks, synthetic video avatar, millisecond quotes/trading, personalized investment advice.
- **Decision Research Gate:** every material framework/provider/schema migration/policy/default requires a DR record with >=3 material alternatives where available, source search, workload benchmark, risk, uncertainty, reversal conditions and explicit status `LOCK | NO_PREFERENCE | PENDING_EVIDENCE`.

## Stage gates (logical, not invented dates)

| Gate | Work | Exit condition |
|---|---|---|
| F0 | Orchestrator takeover, charter, inventory, external blocker requests | current lease/provenance PASS; candidate charter recorded without changing W007 |
| F1 | Partner/editor discovery, architecture and data contracts, benchmark preregistration | representative requirements and unknowns, DRG records, dataset methodology |
| F2 | M01, M02 spike, M04 protocol, M05 and M09 v1 | source-original and adversarial experiments; no critical regression |
| F3 | M06, M07, M08 | secure editorial review/approval/passport same-path E2E |
| F4 | M03, M11, M12 | allowed-source versioning, export contracts, privacy-aware metrics |
| F5 | M10 and M09 enhanced; M04 human calibration | no hard-gate relaxation, human and provider evidence, rollback |
| F6 | W007 closure + all applicable production gate tests, independent audit | PROD-001..017 PASS where applicable, release runbook/video/rollback; otherwise remain NOT_AUTHORIZED |

## EP package dependency DAG

| Package | Target | Dependencies | Gate/output |
|---|---|---|---|
| EP-00 | Charter and authority | Orchestrator lease, STATE | scope/limits/traceability intake |
| EP-01 | Editorial/Compliance discovery | EP-00 | actual owner/workflow or explicit unknown, usability hypothesis |
| EP-02 | Current contracts and gap inventory | EP-00 | source/extraction/claim/workflow/API/schema inventory |
| EP-03 | Corpus and benchmark preregistration | EP-00 | source grouped splits, leakage barriers, raw metrics |
| EP-04 | Human annotation capability | EP-00 + external people | actual two independent streams + adjudicator availability |
| EP-05 | Cloud qualification capability | EP-00 + external cloud account | GCP/AWS context, budget, permissions, approved failure trials |
| EP-06 | Financial model and DRG | EP-01,02,03 | schema alternative/bakeoff decision |
| EP-07 | Structured table-cell adapter | EP-06, W007-T004 | trust-preserving extraction contract/fixtures |
| EP-08 | Claims ledger and API | EP-06,07 | tenant-bound claims and provenance verified |
| EP-09 | Independent verifier | EP-08 | deterministic tests, false alerts |
| EP-10 | Nine-output consistency | EP-08 | critical contradictions and targeted repair |
| EP-11 | Human-calibrated audience validation | EP-03,04 | held-out human scientific evidence |
| EP-12 | Editorial workspace | EP-01,08,10 + qualified authz | review/approve secure E2E |
| EP-13 | Policy engine | EP-01,08,12 | hard/soft versions and tests |
| EP-14 | Evidence passport | EP-08,12,13 | integrity+privacy verifiable export |
| EP-15 | Extended benchmark lab | EP-03,08,10,11 | raw controlled comparisons |
| EP-16 | Revision watch | EP-08,10,12 | authorized diff/impact queue |
| EP-17 | Exports and integration APIs | EP-12,13,14 | validated content roundtrip |
| EP-18 | Value analytics | EP-01,12,15 | measured editorial baseline and pilot |
| EP-19 | Adaptive router | EP-11,15 + qualified W007 | safe rollout and rollback |
| EP-20 | Security/reliability/observability | across features + W007 | threat, tenant, replay, restore, load and supply-chain proofs |
| EP-21 | Independent final audit | EP-20 + required predecessors | production evidence, runbook, same-product video <= 5 min |

**No work in this table is implicitly DONE, no EP receives a canonical dispatch until Orchestrator materializes an accepted wave/issue/attempt, and a blocked W007 successor stays blocked.** Parallel candidate work may be researched off critical-path, then integrated only under protocol.

## Priority / action order

1. Keep W007 blockers explicit. Obtain human and cloud capability externally; retry **with fresh attempt IDs only** when actually available.
2. Prepare EP-01 / EP-02 / EP-03 as independent bounded research/diagnostic workstreams; no provider or platform defaults.
3. Identify and fix table/cell provenance in the trusted ingestion contract before choosing production OCR parser.
4. Build M01 and M05 after contracts and baseline; preserve exact nine jobs, lossless join, fail-closed critical gates.
5. Build the editor-facing same-path workflow and use actual editorial feedback to distinguish product value from engineering volume.
6. Only after empirical evidence, consider rollout of policies, exports, monitoring, analytics and adaptive routing.
7. Continue independent red-team, audit, regression and release-gate checks throughout rather than deferring safety to the end.

## Required missing operator/partner inputs (never infer)

- Authorized GCP project, AWS account, billing/budget/regions, destructive-but-isolated qualification permission and practical access mechanisms.
- Real independent human primary annotators and a different adjudicator.
- Suno editorial/compliance owner, real workflow volumes, data rights, retention and SLA/cost expectations.
- Submission date and precise mechanism.

## Record posture

This file is an **intake portfolio** and does not supersede `SYSTEM/STATE.md`, `SYSTEM/PRODUCTION_CONTRACT.md`, `SYSTEM/DECISION_RESEARCH_GATE.md`, W007 accepted dispatches, contracts or scorecards. Any choice to extend the canonical roadmap, launch a new wave or change hard gates requires a separate Orchestrator-integrated change, revalidation and checkpoint.
