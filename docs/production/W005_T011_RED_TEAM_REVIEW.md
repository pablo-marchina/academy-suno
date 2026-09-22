# W005-T011 — Independent Production Architecture Red-Team

`ARTIFACT_ID: W005-T011-RED-TEAM-V001`

`TASK_ID: W005-T011`
`ATTEMPT_ID: A01`
`ROLE: Red Team + Security/Reliability Reviewer + Evidence Auditor`
`BASE_STATE_VERSION: 0040`
`BASE_COMMIT_SHA: 1cfeb9803036767f4b2cf14320e885751c266f10`
`OBSERVED_STATE_VERSION: 0046`
`OBSERVED_MAIN_SHA_AT_START: 9978f6cc0a4038e85dde9fe72069471bcbe4d220`
`CONTINUITY_CHECK: PASS`
`REVIEW_TARGET: W005-T010-A01 / PR #183 accepted via canonical STATE 0046`
`PRODUCTION_READY_CLAIM: NOT_AUTHORIZED`

## 1. Scope and evidence boundary

This review independently attacks the accepted T010 synthesis rather than re-summarizing it. It checks:

- all `PROD-001..PROD-017` requirements;
- every material `LOCK` declared by `docs/production/W005_TARGET_PRODUCTION_ARCHITECTURE.md`;
- hidden local/single-user assumptions;
- cross-tenant/security failures;
- decision-research/DRG traceability and promotion quality;
- failure/recovery/event consistency gaps;
- eval circularity / W004-calibration leakage;
- observability leakage and product-vs-telemetry truth boundaries;
- fake-demo/final-evidence drift;
- non-compensatory hard-gate behavior.

Primary reviewed refs:

- `SYSTEM/PRODUCTION_CONTRACT.md` (`PROD-001..017`);
- `SYSTEM/DECISION_RESEARCH_GATE.md`;
- `SYSTEM/ASSUMPTION_RISK_REGISTER.md` (`RISK-0021`, `RISK-0031..0040`);
- `SYSTEM/RESULTS/W005-T002-A01.md`;
- `SYSTEM/RESULTS/W005-T004-A01.md`;
- `SYSTEM/RESULTS/W005-T005-A01.md`;
- `SYSTEM/RESULTS/W005-T007-A01.md`;
- `SYSTEM/RESULTS/W005-T010-A01.md`;
- `SYSTEM/RESULTS/W005-T013-A01.md`;
- `docs/production/W005_TARGET_PRODUCTION_ARCHITECTURE.md`;
- `docs/production/W005_IMPLEMENTATION_DAG_AND_ACCEPTANCE_GATES.md`;
- relevant DR records under `docs/decisions/research/` including `DR-0001-evidence-cockpit-frontend-api-live-events.md`, `DR-0701-observability-telemetry-safe-live-evidence.md`, `DR-5401..5403`, and W005-T005 decision records.

Severity semantics:

- `CRITICAL`: design could authorize a hard-gate violation or cross-tenant/false-production claim if followed as written.
- `HIGH`: material production/DRG/evidence gap that should be resolved before T012 accepts the architecture as implementation authority.
- `MEDIUM`: important ambiguity/control gap that can be closed during the explicit bakeoff/schema increments.
- `LOW`: hardening/traceability improvement with bounded direct impact.

## 2. Executive disposition

`CRITICAL_FINDINGS: 0`
`HIGH_FINDINGS: 3`
`MEDIUM_FINDINGS: 4`
`LOW_FINDINGS: 1`

T010 is directionally strong and correctly refuses a `PRODUCTION_READY` claim. It also preserves the most important non-compensatory boundaries: tenant/source/provenance gates, no production audience-threshold inheritance from W004, 9/9 branch identity, real-provider path, and telemetry not being authoritative product state.

However, T012 should not accept the T010 matrix unchanged. Three material corrections are required before the synthesis becomes implementation authority:

1. remove/repair a DRG status promotion inconsistency for repository strategy;
2. make durable state ↔ durable product-event consistency an explicit atomic/reconcilable contract with failure evidence;
3. eliminate ambiguity that the static W004 cockpit can ever become a recipient/final-evidence fallback path.

No high score, architecture benefit, or broad `17/17 mapped` coverage compensates for these gates.

## 3. Findings

### H-01 — Repository strategy was promoted from `PENDING_EVIDENCE` to `LOCK`

**Severity:** HIGH  
**Type:** factual decision-state inconsistency + DRG evidence gap  
**Refs:** `PROD-015`; `RISK-0034`; `RISK-0040`; `W005-T013-A01`; T010 decision matrix `Repository strategy`.

T013 explicitly classified **Repository/build graph** as `PENDING_EVIDENCE`: keep one repository as the current baseline, but do not add Nx/Turborepo or another graph layer until topology/CI evidence justifies it. T010 changed that into:

> `LOCK` — keep the existing single repository through initial production migration.

The defensible invariant is **do not migrate repository topology without evidence**. The topology itself is not evidence-complete enough to be a `LOCK` under the DRG.

**Impact:** A no-change default has been converted into a stronger architecture decision than its source task authorized. This weakens DRG provenance and could hide a later topology requirement behind an already-frozen status.

**Required remediation:**

- change specific repository topology to `PENDING_EVIDENCE` or `NO_MIGRATION_WITHOUT_EVIDENCE`;
- preserve the current monorepo as baseline/counterfactual, not as an evidence-won immutable topology;
- if T012 wants a true `LOCK`, require a DR record that directly compares repository topology alternatives on the selected deployable/workspace graph.

**Blocker recommendation:** blocker for T012 accepting the T010 decision matrix unchanged; not a blocker for continuing contract/schema work.

---

### H-02 — Product state and durable live-event consistency lacks an explicit atomicity/reconciliation contract

**Severity:** HIGH  
**Type:** architectural risk + missing failure evidence  
**Refs:** `PROD-003`, `PROD-011`, `PROD-013`, `PROD-017`; `RISK-0021`, `RISK-0035`; T010 invariants 8–9; T010 end-to-end step 20; T010 DAG Increments 1/4/7.

T010 correctly separates:

1. authoritative durable product/run state;
2. durable ordered product/domain events used for replay/live cockpit;
3. sampled observability.

But the artifacts do not define how a state transition and its durable event become failure-consistent. The text says state transitions append durable events, yet does not require one of:

- same-transaction state + outbox/event append;
- idempotent transactionally coupled outbox;
- CDC with proven ordering/ownership semantics;
- deterministic reconciliation/gap repair tied to `run_revision`.

A crash between state commit and event commit can therefore produce a run that is correct in storage but stale/incomplete in the Evidence Cockpit; the inverse can expose an event for state that never committed. Replay correctness alone does not close this gap.

**Impact:** direct risk of live-product evidence diverging from authoritative state after partial failure, creating exactly the stale/synthetic-evidence class T010 says must be impossible.

**Required remediation:**

- add an explicit state/event consistency contract in Increment 1;
- selected substrate must prove atomic commit or deterministic reconciliation under crash/failure injection;
- add acceptance tests for `state committed/event missing`, `event committed/state missing`, duplicate delivery, reordering, consumer restart, and replay after repair;
- define invariant linking `run_revision`/event sequence to authoritative committed state.

**Blocker recommendation:** blocker for T012 accepting PROD-003/011/017 architecture coverage as implementation-complete enough to freeze the event substrate.

---

### H-03 — `LOCK`ing the static W004 cockpit as a “fallback” creates dual-path/fake-demo ambiguity

**Severity:** HIGH  
**Type:** architectural risk + final-evidence path ambiguity  
**Refs:** `PROD-005`, `PROD-011`, `PROD-017`; `RISK-0021`, `RISK-0024`, `RISK-0035`; Production Contract single-real-product-path principle; T002/T010 static cockpit decision.

T002 and T010 correctly say the static W004 cockpit is not the sole production UI and should be retained for diagnostic/counterfactual value. The risky word is **fallback**. A recipient/final-evidence runtime that can fall back from the real live product to a static/manifests-driven cockpit violates the single-real-product-path principle even if clearly engineered.

The implementation DAG partly mitigates this by requiring the production vertical slice to show the current run correlated by run/job/event IDs and not a fixture/static surrogate, but the decision matrix still leaves room for a dual presentation path.

**Impact:** final evidence could accidentally demonstrate a mechanics/static projection rather than the same real provider/workflow/event path used by the product; stale data could also be presented as current.

**Required remediation:**

- reclassify W004 static cockpit as `DIAGNOSTIC_ONLY / COUNTERFACTUAL`, not a production/final-evidence fallback;
- production recipient routes must never automatically fall back to static evidence;
- any diagnostic view must be unmistakably labeled and excluded from final production-claim evidence;
- final-evidence gate must prove current source hash, run/job/event IDs, provider/catalog/policy/evaluator versions and live persistence identity for what is shown.

**Blocker recommendation:** blocker for PROD-017 final-evidence acceptance; fix terminology/control before T012 architecture acceptance.

---

### M-01 — SSE is locked before browser credential topology is fully frozen

**Severity:** MEDIUM  
**Type:** evidence gap / integration dependency  
**Refs:** `PROD-001`, `PROD-002`, `PROD-011`, `PROD-014`; `RISK-0031`; T002 “Native EventSource auth must be designed, not assumed”; T004 identity/session architecture.

T002 explicitly records that native `EventSource` does not support arbitrary bearer-header injection and that same-origin secure session-cookie SSE, fetch-stream/polyfill, or BFF topology must be selected deliberately. T010 locks SSE as default browser transport while identity vendor/session details remain open.

The transport lock is still plausible, but it is conditional on a compatible credential topology and CSRF/session/revocation model.

**Required remediation:** add a G2A/G2D acceptance test for the exact chosen browser-auth topology: authorization on initial connect and resume, revoked membership/session, org switch, cross-tenant cursor replay, CSRF/cookie policy where applicable, and reconnect after auth expiry.

**Blocker recommendation:** not a blocker to retain SSE as default; blocker to claim the live transport security path is production-proven.

---

### M-02 — Decision-record identifiers are not globally unambiguous

**Severity:** MEDIUM  
**Type:** factual traceability defect  
**Refs:** `PROD-015`; `RISK-0040`; `SYSTEM/DECISION_RESEARCH_GATE.md` required `DR-####` records.

The research directory contains at least two records with the same `DR-0001` identifier:

- `DR-0001-evidence-cockpit-frontend-api-live-events.md`;
- `DR-0001-orchestration-durability-runtime.md`.

T005 also persists decision records with task-derived filenames rather than canonical `DR-####` identifiers.

Content quality may still be strong, but exact audit references such as “DR-0001” are ambiguous and cannot act as globally stable decision IDs.

**Required remediation:** introduce unique stable DR IDs (or formally define a namespaced ID scheme), update references, and have T012 cite exact DR paths/IDs for every material `LOCK`.

**Blocker recommendation:** not a blocker to implementation spikes; blocker to claiming fully clean PROD-015 traceability.

---

### M-03 — OTel/OTLP/Collector `LOCK` must stay bounded to the interface boundary

**Severity:** MEDIUM  
**Type:** evidence-boundary risk  
**Refs:** `PROD-012`, `PROD-014`, `PROD-015`; `RISK-0037`, `RISK-0040`; T007 `CANDIDATE_FOR_T010_LOCK`; T010 OTel/Collector lock.

T007 provides strong primary-source support and a useful synthetic probe, but explicitly states its benchmark does **not** measure network/TLS/proxy/backend behavior and records maturity caveats for collector redaction/tail-sampling components. T010 promotes the vendor-neutral W3C/OTel/OTLP/Collector boundary to `LOCK`.

This promotion is acceptable only if interpreted narrowly as an instrumentation/export abstraction. It must not silently lock collector topology, processor chain, sampling mode, retention, or a direct cockpit dependency on telemetry.

**Required remediation:** T012 should restate the lock as **W3C trace context + OTel semantic/instrumentation boundary + OTLP-compatible export boundary**, while collector topology/processors remain evidence-gated and tested under T008/Increment 7 failure injection.

**Blocker recommendation:** no blocker if the lock is narrowed explicitly; otherwise PROD-015 evidence scope is overstated.

---

### M-04 — Job/provider retry idempotency semantics are under-specified

**Severity:** MEDIUM  
**Type:** architectural risk  
**Refs:** `PROD-002`, `PROD-003`, `PROD-006`, `PROD-010`, `PROD-013`; `RISK-0033`, `RISK-0039`; T010 steps 12–19; Increment 2C.

T010 requires stable IDs, bounded retries, resume, optimistic version/ownership semantics and zero silent stale overwrites. It does not fully specify the commit model for a provider attempt that times out after the provider actually completed, nor how duplicate worker delivery is de-duplicated before cost/output/eval side effects are accepted.

Exactly-once remote model invocation is generally not available; the architecture therefore needs explicit at-least-once execution with idempotent acceptance semantics.

**Required remediation:** define immutable `attempt_id`/provider-call identity, unique accepted-output commit constraints, CAS/ownership lease semantics, late-result handling, duplicate-cost accounting, and replay rules. Add fail-injection cases where timeout/worker crash occurs after remote success but before local commit.

**Blocker recommendation:** not a T010 design blocker if added to Increment 2C; production runtime cannot pass PROD-006/013 without it.

---

### L-01 — Event cursor scope should be explicit to avoid cross-tenant metadata leakage

**Severity:** LOW  
**Type:** optional security hardening  
**Refs:** `PROD-001`, `PROD-011`, `PROD-014`; `RISK-0031`, `RISK-0037`; T007 live-event envelope.

The live-event design uses monotonic `event_id` + `Last-Event-ID`/cursor semantics and server-side authorization. It does not explicitly state whether sequence numbers are global, tenant-scoped or run-stream-scoped.

A globally enumerable cursor is not automatically a data leak, but run-scoped opaque cursors reduce timing/existence metadata exposure and simplify authorization reasoning.

**Recommended improvement:** scope replay cursors to the authorized stream/resource or make them opaque capabilities that are validated together with tenant/run authorization; never allow cursor-only lookup to select another tenant's stream.

**Blocker recommendation:** none if endpoint authorization is correct; add adversarial negative tests.

## 4. Every `LOCK` decision challenged

| T010 `LOCK` | Red-team outcome | Evidence / challenge |
|---|---|---|
| typed/versioned HTTP resource/command API | UPHOLD | Directly satisfies PROD-002; T002 DRG supports reversible implementation. |
| OpenAPI-described boundary | UPHOLD | T002 supports it; exact OAS/tooling remains reversible. |
| SSE default browser run feed | CONDITIONAL | Keep default, but close M-01 browser credential/revocation topology and real proxy/load evidence. |
| durable cursor/replay/de-dupe/snapshot | CONDITIONAL | Semantics sound; H-02 requires atomic/reconcilable link to authoritative state. |
| server-side authorization/redaction before serialization | UPHOLD | Required by PROD-001/014; T002/T004/T007 aligned. |
| stable opaque source/citation refs | UPHOLD | Correct anti-path/authorization abstraction. |
| static W004 cockpit as diagnostic/fallback | CHALLENGE | H-03: diagnostic/counterfactual yes; production/final-evidence fallback no. |
| stable `(issuer,subject)` → internal `user_id` | UPHOLD | T004 evidence; vendor-independent invariant. |
| application-owned deny-by-default authz | UPHOLD | Non-negotiable multi-tenant invariant. |
| first-class tenant/resource binding + data-plane defense | UPHOLD | Required by PROD-001/RISK-0031. |
| private tenant-bound object boundary + quarantine lifecycle | UPHOLD | Required by PROD-004/RISK-0032; provider remains open. |
| parser-agnostic normalized provenance + fail-closed source trust | UPHOLD | Correctly separates architecture from parser winner. |
| stable workflow IDs / 9-way fan-out / resume / lossless join / retry≠repair | UPHOLD | Required by PROD-006; runtime remains pending. |
| current SQLiteRunStore barred as multi-replica authority | UPHOLD | Reproduced stale same-run lost update is sufficient negative evidence. |
| deterministic adaptive safety envelope | UPHOLD | Critical gates correctly outside optimizer. |
| immutable provider catalog/policy/version/rollback identity | UPHOLD | Required for PROD-010 auditability. |
| non-compensatory eval hard gates + versioned evaluator config | UPHOLD | PROD-007/009 core invariant. |
| blind independent human calibration method | UPHOLD | T005 explicitly locks method; empirical thresholds still absent. |
| model judge as calibrated secondary sensor only | UPHOLD | Prevents circularity; no human-gold inheritance. |
| W005 v002 multidimensional benchmark method | UPHOLD | Preserves hard gates and avoids unsupported scalar utility. |
| durable product events separate from sampled telemetry | UPHOLD_WITH_FIX | Separation is correct; H-02 state↔event failure consistency must be added. |
| W3C + OTel + OTLP/Collector boundary | NARROW | M-03: lock interface/instrumentation boundary, not collector topology/processors/backend. |
| raw sensitive GenAI telemetry off by default | UPHOLD | Strong privacy/security invariant. |
| bounded metric-label allowlist | UPHOLD | Correct cardinality/privacy control. |
| deployment invariants (decoupled work/shared state/backpressure/health/migrations/restore) | UPHOLD | Vendor/runtime class remains open as required. |
| GitHub Actions CI platform | UPHOLD_WITH_REVERSAL | Existing control plane + no evidenced blocker is a reasonable baseline lock; retain T013 reversal condition. |
| CI/supply-chain hardening controls | UPHOLD | Full-SHA, least privilege, lock-derived installs, SBOM/attestation are control requirements, not package-manager locks. |
| keep existing single repository through initial migration | CHALLENGE | H-01: source task classified repository/build graph as PENDING_EVIDENCE. |

No other material `LOCK` found in the T010 decision matrix is silently accepted here.

## 5. PROD-001..017 coverage review

| PROD | Review | Red-team disposition |
|---|---|---|
| PROD-001 Identity/tenant isolation | COVERED_BY_DESIGN | Strong T004 invariants/test model; implementation/adversarial proof still future. |
| PROD-002 Production API boundary | COVERED_BY_DESIGN | Typed/versioned API and controlled upload; M-04 idempotent attempt/side-effect semantics should be explicit. |
| PROD-003 Durable shared persistence | MATERIAL_GAP | Runtime/store still pending by design; H-02 adds missing state↔event consistency requirement. |
| PROD-004 Secure object storage | COVERED_BY_DESIGN | Quarantine/hash/provenance lifecycle strong; real controls still unexecuted. |
| PROD-005 Real provider path | COVERED_CONDITIONALLY | Provider remains unresolved correctly; H-03 prevents static/fake final UI substitution. |
| PROD-006 Stateful 3×3 | COVERED_BY_DESIGN | 9/9/lossless/resume semantics preserved; M-04 must be proven in runtime bakeoff. |
| PROD-007 Hybrid eval | COVERED_BY_DESIGN | Non-compensatory hard gates + secondary sensors correctly separated. |
| PROD-008 Human-calibrated audience evidence | CORRECTLY_NOT_PASS | T005 explicitly keeps thresholds `DIAGNOSTIC_ONLY`; no W004 automated calibration inheritance observed. |
| PROD-009 Eval-driven CI/CD | COVERED_BY_DESIGN | Release lanes defined; empirical CI execution remains Phase 9 evidence. |
| PROD-010 Adaptive policy | COVERED_BY_DESIGN | Safety envelope and auditability strong; provider/router winners remain pending. |
| PROD-011 Live Evidence Cockpit | MATERIAL_GAP | H-02 and H-03 must be fixed before live evidence can be trusted under failure/final demo. |
| PROD-012 Observability | COVERED_CONDITIONALLY | T007 architecture is strong; M-03 narrows what is actually locked. |
| PROD-013 Reliability/capacity | CORRECTLY_NOT_PASS | T010 defines methodology/gates and avoids invented SLO/capacity. |
| PROD-014 Security/privacy | COVERED_BY_DESIGN | Threat model/negative tests defined; M-01/L-01 add auth/cursor tests. |
| PROD-015 Research-gated architecture | MATERIAL_GAP | H-01 decision-status inflation + M-02 DR identity ambiguity; M-03 lock scope must stay precise. |
| PROD-016 Reproducible deployment | CORRECTLY_NOT_PASS | Toolchain/deploy freeze follows selected topology; no premature production claim. |
| PROD-017 Production-grade final evidence | MATERIAL_GAP | H-03 must guarantee final evidence uses only the real live product path; H-02 must guarantee live evidence survives partial failure coherently. |

`PROD_MAPPING_CHECK: 17/17 reviewed`

This is a coverage review, not a production PASS. T010 was correct not to equate architecture mapping with production readiness.

## 6. Hard-gate / non-compensation audit

No evidence was found that T010 allows a high aggregate score, lower cost, lower latency, or UX benefit to compensate for:

- critical factual/source/policy/schema failure;
- tenant isolation failure;
- missing required provenance;
- branch loss/duplication;
- stale same-run overwrite;
- untrusted filesystem path exposure;
- W004 automated audience calibration being reused as production human evidence.

T005 explicitly preserves D-0017 as historical W004 automated evidence only and requires independent human calibration + frozen held-out replication before production audience thresholds. T010 carries this boundary correctly.

## 7. Missing DRG / counterfactuals

Required follow-up DRG/evidence, without silently choosing alternatives:

1. repository topology decision status must be corrected (H-01); any future topology lock needs selected-product workload evidence;
2. the selected state/event substrate must compare atomic-outbox / transactional-event / CDC / reconciliation patterns under the actual chosen store/runtime; T011 does **not** select one;
3. if SSE credential topology cannot pass the chosen identity/session/security model, the live transport decision must reopen rather than be forced;
4. OTel/OTLP remains the locked abstraction only if implementation evidence preserves telemetry-outage independence and security; collector/backend topology remains open;
5. provider/job idempotent acceptance semantics must be benchmarked/failure-injected with the selected workflow substrate.

## 8. Remediation priority

### Before T012 architecture acceptance

- fix H-01 repository-strategy status;
- add H-02 explicit state/event consistency contract + acceptance scenarios;
- fix H-03 static cockpit classification/final-evidence exclusion;
- normalize/cross-reference DR IDs sufficiently for exact PROD-015 auditability;
- narrow OTel/Collector lock wording if needed.

### Before production vertical-slice claim

- close M-01 exact SSE/browser auth topology;
- close M-04 provider/job retry idempotent acceptance semantics;
- execute cross-tenant/event/trace/cursor adversarial tests;
- execute runtime crash/replay/event-gap failure injection.

### Before `PRODUCTION_READY`

All Production Contract runtime/security/reliability/deployment evidence must pass; none of this review authorizes a shortcut.

## 9. Final red-team disposition

`RED_TEAM_STATUS: COMPLETE_WITH_MATERIAL_REMEDIATIONS`

`T010_ARCHITECTURE_RECOMMENDATION: ACCEPT_DIRECTIONALLY_BUT_DO_NOT_FREEZE_UNCHANGED`

The architecture is coherent enough to continue controlled contract/schema and bakeoff work, but T012 should incorporate the high-severity corrections before treating T010 as final implementation authority. No newly discovered technology alternative is selected here; all unresolved material alternatives remain DRG/evidence work.
