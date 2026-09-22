# W005 Production Requirements & Acceptance Package

`TASK: W005-T001-A01`  
`STATUS: RESEARCH_INPUT_TO_ARCHITECTURE`  
`CLAIM_BOUNDARY: NOT_PRODUCTION_READY`  
`STACK_SELECTION: NONE`  
`RESEARCH_CHECKED: 2026-09-22`

## 1. Purpose

Turn `D-0018` and `SYSTEM/PRODUCTION_CONTRACT.md` into measurable, testable production requirements without selecting frontend, auth, database, cloud, workflow, model/provider, parser, observability, deployment, or security products.

This package is an input to W005 architecture synthesis. It does **not** authorize a production stack, does not claim production readiness, and does not replace the Decision Research Gate (DRG).

## 2. Continuity and source-of-truth posture

The dispatch was cut from `STATE 0040` / `1cfeb9803036767f4b2cf14320e885751c266f10`. The observed worker/main base for this attempt is `d626172f3e49da7dc04a91d399f69979612495ba` / `STATE 0042`.

The intervening W005 readiness reconciliation explicitly preserves T001's objective and the Production Contract while adding T013/T014 research coverage. No material conflict was found. The attempt therefore preserves its original provenance and proceeds under `CONTINUITY_CHECK: PASS`.

Authoritative inputs:

- `SYSTEM/PRODUCTION_CONTRACT.md`
- `SYSTEM/CASE_CONTRACT.md`
- `SYSTEM/DECISIONS.md` (`D-0018`, with `D-0017` claim limits preserved)
- `SYSTEM/DECISION_RESEARCH_GATE.md`
- `SYSTEM/TRACEABILITY_MATRIX.md`
- `SYSTEM/ASSUMPTION_RISK_REGISTER.md`
- `docs/review_current/W005_START_READINESS_REVIEW.md`

## 3. Measurement vocabulary

Every production requirement is assigned one of these threshold dispositions.

| Disposition | Meaning | May architecture invent a number? |
|---|---|---|
| `HARD_CONTRACT` | Already fixed by the Production Contract / briefing / locked decision. | No; preserve the existing value exactly. |
| `DECLARED_AND_TESTED` | A concrete operating value must exist before production claim (for example timeout, upload limit, retention rule), but the value is not supplied by the case. Acceptance tests verify the declared value is enforced. | No; value requires owner/risk/research input before freeze. |
| `TO_BE_ESTABLISHED_BY_EVIDENCE` | Quality, latency, cost, capacity, reliability or similar target whose numeric threshold requires representative measurement/benchmark. | No. |
| `UNKNOWN_EXTERNAL` | Depends on a partner/business/legal/operational fact not present in the repository. | No; keep explicit until evidence arrives. |
| `BINARY_EVIDENCE_GATE` | Pass/fail evidence can be required without choosing a numerical target. | No numeric invention needed. |

### Existing hard invariants (must not be weakened)

- critical factual/source/policy hard-gate compensation: `0`;
- cross-tenant unauthorized access in defined tests: `0`;
- runs/jobs without provenance binding: `0`;
- required 3x3 branch coverage: `9/9`;
- accepted join losing/duplicating branches: `0`;
- critical schema violations promoted as PASS: `0`;
- defined backup/restore and restart/resume scenarios: `100% PASS` before a production claim;
- final technical video: `<= 5:00`.

Any quality/audience/latency/cost/capacity target not listed above remains `TO_BE_ESTABLISHED_BY_EVIDENCE`.

## 4. Evidence classes

These are task-local evidence classes for acceptance planning; they do not introduce canonical project statuses.

| Class | Evidence | Minimum property |
|---|---|---|
| `EC-1 CONTRACT` | locked decision/contract/briefing | exact source reference and unchanged invariant |
| `EC-2 DETERMINISTIC_TEST` | automated regression/integration/adversarial test | reproducible inputs, expected outcome, machine-readable result |
| `EC-3 RUNTIME_OBSERVATION` | real run telemetry | correlated request/run/job/tenant context and timestamp/config version |
| `EC-4 RESILIENCE_RECOVERY` | failure, restart, resume, backup/restore, load exercise | scenario definition, injected condition, measured outcome, artifact |
| `EC-5 SECURITY_PRIVACY` | threat model, authz/isolation/abuse/secrets/scanning evidence | attack/control mapping, negative tests, findings disposition |
| `EC-6 HUMAN_CALIBRATION` | independent human annotation/evaluation | blinded/versioned protocol, independent streams or justified equivalent, agreement/adjudication, split discipline |
| `EC-7 RESEARCH_BENCHMARK` | DRG research/bakeoff | decision question, alternatives, primary sources, representative workload, limitations, uncertainty, reversal conditions |
| `EC-8 LIVE_PRODUCT_EVIDENCE` | final live recipient-facing product evidence | same real product path, correlated provenance, no hidden fixture substitution |

A production claim needs the classes applicable to the requirement. A local smoke test or demo fixture never substitutes for `EC-3`/`EC-4`/`EC-5` where the contract asks for production evidence.

## 5. PROD-001..017 acceptance matrix

### PROD-001 — Identity and tenant isolation

**Requirement.** Authenticated identities and explicit organization/workspace/user/run dimensions must be bound to authorization and persisted private resources.

**Acceptance tests / measurable outcomes.**

1. Every defined protected action is exercised across an authorization matrix containing allowed and denied cases; every expected denial is denied (`BINARY_EVIDENCE_GATE`).
2. Cross-tenant unauthorized access observed in the defined adversarial suite = `0` (`HARD_CONTRACT`).
3. Private persisted data/artifacts lacking tenant binding = `0` (`HARD_CONTRACT`, where the resource is tenant-scoped).
4. Role/membership changes are auditable and become effective according to a declared lifecycle (`DECLARED_AND_TESTED`).
5. Authentication/session characteristics (session lifetime, re-authentication conditions, recovery, SSO if required) remain `UNKNOWN_EXTERNAL` until owner/security requirements are known.

**Evidence:** EC-2, EC-3, EC-5.  
**Case linkage:** PAIN-004, PAIN-005; REQ-014, REQ-018, REQ-021.  
**Risks:** RISK-0021, RISK-0031, RISK-0037.  
**Downstream:** T004 must research tenancy/authz/data-control alternatives; T010 may only freeze the model after DRG evidence.

### PROD-002 — Production API boundary

**Requirement.** Recipient-facing/system integration boundaries are typed, versioned, validated and bounded, with safe retry/idempotency/backpressure behavior.

**Acceptance tests / measurable outcomes.**

1. Supported API payloads conform to a versioned machine-readable contract; invalid payload/schema cases are rejected (`BINARY_EVIDENCE_GATE`).
2. Untrusted users cannot cause arbitrary server filesystem path access (`0` successful defined path-abuse cases; `HARD_CONTRACT` by security intent).
3. Upload/body limits, request timeout, retry ceiling, queue/backpressure policy and idempotency scope are declared and tested at/around boundaries (`DECLARED_AND_TESTED`).
4. Repeating an idempotent operation with the same key does not create duplicate accepted business effects in the defined scenario (`0` duplicates; `BINARY_EVIDENCE_GATE`).
5. Latency/throughput/error targets remain `TO_BE_ESTABLISHED_BY_EVIDENCE`.

**Evidence:** EC-2, EC-3, EC-5, EC-7.  
**Case linkage:** REQ-001, REQ-002, REQ-003, REQ-013, REQ-018.  
**Risks:** RISK-0032, RISK-0038.  
**Downstream:** T002/T004 define boundary/security requirements; T008 measures production behavior; no framework choice here.

### PROD-003 — Durable shared persistence

**Requirement.** Run state and audit evidence survive restart/redeploy and support the required multi-user/multi-replica operating model.

**Acceptance tests / measurable outcomes.**

1. Defined restart/resume scenarios = `100% PASS` before production claim (`HARD_CONTRACT`).
2. Defined backup/restore scenarios = `100% PASS` before production claim (`HARD_CONTRACT`).
3. A completed/accepted run's required state is recoverable after process replacement/redeploy (`BINARY_EVIDENCE_GATE`).
4. Multi-replica concurrency behavior is tested for lost update/duplicate work/corruption under a representative workload; allowed anomaly count must be declared by invariant and, for correctness-critical state, is `0` (`DECLARED_AND_TESTED`).
5. Audit/provenance events that are required to be append-only cannot be silently overwritten in the defined mutation tests (`0` silent overwrites; `BINARY_EVIDENCE_GATE`).
6. RPO/RTO numbers remain `TO_BE_ESTABLISHED_BY_EVIDENCE` unless an owner/business requirement is supplied.

**Evidence:** EC-2, EC-4, EC-7.  
**Case linkage:** REQ-002, REQ-013, REQ-016, REQ-018, REQ-021.  
**Risks:** RISK-0021, RISK-0033.  
**Downstream:** T004/T008 must benchmark persistence/recovery choices; current local SQLite is baseline evidence, not production proof.

### PROD-004 — Secure document/object storage

**Requirement.** User documents and generated/private artifacts enter controlled storage with explicit content, path, provenance and retention controls.

**Acceptance tests / measurable outcomes.**

1. Only explicitly supported input formats pass the production ingest boundary (`BINARY_EVIDENCE_GATE`).
2. File/body size limit is declared and enforced; boundary tests below/at/above the limit behave as specified (`DECLARED_AND_TESTED`).
3. Filename/path traversal and arbitrary-path test corpus produces `0` unauthorized filesystem accesses (`BINARY_EVIDENCE_GATE`).
4. Every accepted source has a source hash and provenance binding; missing required provenance = `0` (`HARD_CONTRACT`).
5. Content validation failure is fail-closed for source trust; no invalid source is silently promoted to trusted (`0` promoted invalid cases in defined suite).
6. Retention/deletion policy must be declared before production; exact duration/legal basis remains `UNKNOWN_EXTERNAL` pending owner/legal facts.

**Evidence:** EC-2, EC-5, EC-7.  
**Case linkage:** REQ-001, REQ-012, REQ-018, REQ-021.  
**Risks:** RISK-0010, RISK-0032, RISK-0037.  
**Downstream:** T004 storage/security research and T014 parsing/source-grounding benchmark.

### PROD-005 — Real provider path

**Requirement.** When real providers are configured, the final recipient-facing path uses their real outputs and measures provider behavior instead of substituting an unlabeled mechanics fixture.

**Acceptance tests / measurable outcomes.**

1. For a defined production evidence run, UI-visible output can be traced to the real provider invocation/configuration and resulting artifact (`BINARY_EVIDENCE_GATE`).
2. Any `MECHANICS_ONLY`, fixture, replay or simulated mode is explicitly labeled; unlabeled substitution in final production evidence = `0` (`BINARY_EVIDENCE_GATE`).
3. Provider calls record quality-relevant result linkage plus latency, usage/cost inputs, error and retry observations (`BINARY_EVIDENCE_GATE`; numeric targets evidence-driven).
4. Provider/model quality, latency, cost and reliability targets remain `TO_BE_ESTABLISHED_BY_EVIDENCE` and may vary by workload slice.

**Evidence:** EC-3, EC-7, EC-8.  
**Case linkage:** PAIN-005; REQ-012, REQ-013, REQ-017, REQ-020, REQ-022.  
**Risks:** RISK-0017, RISK-0022, RISK-0024, RISK-0035.  
**Downstream:** T003/T006/T009 research behavior; T010 cannot infer a provider winner from W004 alone.

### PROD-006 — Stateful exact 3x3 AI workflow

**Requirement.** Real document processing preserves the anchor/provenance spine through exactly 3 audiences x 3 native formats, evaluation, repair/review and lossless aggregation.

**Acceptance tests / measurable outcomes.**

1. Required branch coverage = `9/9` (`HARD_CONTRACT`).
2. Accepted join losing/duplicating branches = `0` (`HARD_CONTRACT`).
3. Required run/job provenance bindings missing = `0` (`HARD_CONTRACT`).
4. Stable branch/job identity survives retries/resume in defined interruption scenarios (`BINARY_EVIDENCE_GATE`).
5. Defined restart/resume scenarios = `100% PASS` (`HARD_CONTRACT`).
6. Critical factual/source/policy/schema hard gates cannot be compensated by soft scores (`0` compensated critical failures; `HARD_CONTRACT`).

**Evidence:** EC-2, EC-3, EC-4.  
**Case linkage:** REQ-001..REQ-003, REQ-007..REQ-009, REQ-012, REQ-013, REQ-017, REQ-018.  
**Risks:** RISK-0001, RISK-0013, RISK-0018, RISK-0021, RISK-0039.  
**Downstream:** T003 production orchestration research; W004 baseline is mandatory counterfactual, not an automatic winner.

### PROD-007 — Hybrid evaluation system

**Requirement.** Production evaluation keeps deterministic factual/source/policy/schema controls non-compensatory and versions all evaluator configuration; secondary semantic/judge sensors may inform but not overrule critical gates.

**Acceptance tests / measurable outcomes.**

1. Critical hard-gate compensation observed = `0` (`HARD_CONTRACT`).
2. Critical schema violations promoted as PASS = `0` (`HARD_CONTRACT`).
3. Every eval result links evaluator/config/policy versions and source/run/job provenance (`BINARY_EVIDENCE_GATE`).
4. Regression fixtures prove that a secondary judge cannot turn a critical deterministic failure into PASS (`BINARY_EVIDENCE_GATE`).
5. Readability/audience/semantic thresholds remain `DIAGNOSTIC_ONLY` or `TO_BE_ESTABLISHED_BY_EVIDENCE` until their evidence requirements are met.

**Evidence:** EC-2, EC-3, EC-6, EC-7.  
**Case linkage:** PAIN-001..PAIN-004; REQ-004..REQ-006, REQ-010..REQ-013, REQ-016, REQ-017, REQ-019.  
**Risks:** RISK-0001..RISK-0004, RISK-0014, RISK-0015, RISK-0020, RISK-0036, RISK-0039.  
**Downstream:** T005 evaluation science; T006 adaptive policy must remain outside hard gates.

### PROD-008 — Human-calibrated audience evidence

**Requirement.** Strong production audience-calibration claims require evidence materially stronger than the W004 automated waiver.

**Acceptance tests / measurable outcomes.**

1. Dataset/version and item identity are frozen before scoring (`BINARY_EVIDENCE_GATE`).
2. DEV/CALIBRATION/HELD-OUT separation is explicit; held-out leakage checks pass (`BINARY_EVIDENCE_GATE`).
3. At least two independent human streams per item **or a justified evidence-equivalent protocol** are documented before strong production threshold claims (`BINARY_EVIDENCE_GATE`).
4. Agreement, disagreement/adjudication and uncertainty are reported; no automated-only evidence is mislabeled as human evidence (`0` mislabeled claims).
5. Audience thresholds cannot be frozen from D-0017 alone; until sufficient evidence exists, they remain `DIAGNOSTIC_ONLY` (`HARD_CONTRACT` claim boundary).

**Evidence:** EC-6, EC-7.  
**Case linkage:** PAIN-001, PAIN-003; REQ-004..REQ-006, REQ-010, REQ-011, REQ-019.  
**Risks:** RISK-0003, RISK-0004, RISK-0020, RISK-0023, RISK-0036.  
**Downstream:** T005 must define protocol/power/uncertainty and what evidence-equivalent means; annotator availability remains external.

### PROD-009 — Eval-driven CI/CD

**Requirement.** Material changes are promoted only after the regression/experiment evidence appropriate to deterministic and probabilistic behavior.

**Acceptance tests / measurable outcomes.**

1. Every identified material change class has a mapped required pre-promotion test/eval (`BINARY_EVIDENCE_GATE`).
2. A candidate with a critical hard-gate regression is blocked from release in a controlled negative test (`BINARY_EVIDENCE_GATE`).
3. Probabilistic changes compare baseline and candidate on the same versioned dataset/configuration before promotion (`BINARY_EVIDENCE_GATE`).
4. Experiment inputs, outputs, metrics/config versions and decision disposition are persisted and reproducible (`BINARY_EVIDENCE_GATE`).
5. Statistical/sample-size thresholds for probabilistic promotion remain `TO_BE_ESTABLISHED_BY_EVIDENCE` by T005/T009.

**Evidence:** EC-2, EC-7.  
**Case linkage:** REQ-012, REQ-013, REQ-016, REQ-017, REQ-020, REQ-021.  
**Risks:** RISK-0004, RISK-0015, RISK-0017, RISK-0018, RISK-0034.  
**Downstream:** T005/T009/T013 specify eval methodology and developer-platform enforcement.

### PROD-010 — Adaptive runtime policy

**Requirement.** Adaptive choices may optimize soft objectives only under an auditable/versioned policy that cannot relax deterministic critical gates.

**Acceptance tests / measurable outcomes.**

1. Policy/config version is persisted for every adaptive decision (`BINARY_EVIDENCE_GATE`).
2. Each adaptive decision is reconstructable from permitted inputs, candidate set and resulting choice or is explicitly classified non-deterministic with sufficient trace evidence (`BINARY_EVIDENCE_GATE`).
3. Defined adversarial tests attempting to trade cheaper/faster routing for a critical gate failure yield `0` gate bypasses (`HARD_CONTRACT`).
4. Objective measurements cover quality/factuality/latency/cost/reliability; weights/constraints are declared before production use (`DECLARED_AND_TESTED`).
5. Numeric objective thresholds/weights remain `TO_BE_ESTABLISHED_BY_EVIDENCE`.

**Evidence:** EC-2, EC-3, EC-7.  
**Case linkage:** REQ-012, REQ-013, REQ-017, REQ-020.  
**Risks:** RISK-0005, RISK-0017, RISK-0039.  
**Downstream:** T006 adaptive-runtime research plus T005 eval constraints.

### PROD-011 — Live Evidence Cockpit

**Requirement.** The final frontend exposes real, safely filtered runtime/evidence state for the current product path rather than detached fixtures.

**Acceptance tests / measurable outcomes.**

1. Required surfaces exist: workspace/document/run status; live graph/node events; real 3x3 matrix; source/citations; metric breakdown; repair before/after; experiment comparison; trace explorer; cost/latency/tokens/retries; health/reliability; audit/provenance; research/decision records (`BINARY_EVIDENCE_GATE`).
2. For a controlled live run, every displayed run/job/branch/provider/eval datum links to the same current correlated provenance chain; stale/synthetic substitution = `0` in defined tests.
3. Sensitive content/credentials classified as non-displayable are absent from telemetry/UI exposure in security tests (`0` prohibited exposures in defined corpus).
4. Responsive/viewport/accessibility performance targets are `TO_BE_ESTABLISHED_BY_EVIDENCE`; exact UX implementation is not selected here.

**Evidence:** EC-2, EC-3, EC-5, EC-8.  
**Case linkage:** REQ-014, REQ-018, REQ-020, REQ-022.  
**Risks:** RISK-0024, RISK-0028, RISK-0035, RISK-0037.  
**Downstream:** T002 defines frontend/API/cockpit evidence contract; T007 supplies observability visibility/redaction requirements.

### PROD-012 — Observability

**Requirement.** Traces, metrics and structured logs are correlated across request/run/job/tenant and provider/eval work, exportable and safe for production use.

**Acceptance tests / measurable outcomes.**

1. Defined request -> run -> job -> provider/eval paths can be reconstructed across emitted telemetry using stable correlation context (`BINARY_EVIDENCE_GATE`).
2. Required runtime measurements are queryable for p50/p95/p99 latency, error/retry/queue rates and cost/usage for the declared measurement windows (`BINARY_EVIDENCE_GATE`); target values remain evidence-driven.
3. Telemetry can be exported/consumed outside the application process through a documented interface (`BINARY_EVIDENCE_GATE`).
4. Redaction/classification tests produce `0` prohibited secret/credential exposures in the defined test corpus (`BINARY_EVIDENCE_GATE`).
5. Cardinality/retention/sampling budgets are declared and tested before production (`DECLARED_AND_TESTED`).

**Evidence:** EC-2, EC-3, EC-5, EC-7.  
**Case linkage:** PAIN-004; REQ-018, REQ-020, REQ-021.  
**Risks:** RISK-0035, RISK-0037, RISK-0038.  
**Downstream:** T007 observability research; requirement is signal/correlation/exportability, not an OpenTelemetry/vendor mandate.

### PROD-013 — Reliability and capacity evidence

**Requirement.** Production readiness is supported by measured load, failure, restart/resume and recovery behavior; capacity/SLOs are not fabricated.

**Acceptance tests / measurable outcomes.**

1. A repeatable load curve covers increasing concurrency until an observed saturation/degradation point or an evidence-supported test ceiling; saturation point is recorded, never inferred (`BINARY_EVIDENCE_GATE`).
2. Each load level records p50/p95/p99 latency, throughput, error/retry/queue behavior, resource saturation and cost/usage where applicable (`BINARY_EVIDENCE_GATE`).
3. Defined failure/retry tests, restart/resume tests and backup/restore tests are executed; restart/resume and backup/restore defined scenarios = `100% PASS` before production claim (`HARD_CONTRACT`).
4. SLO/SLA values are either evidence-supported/approved or explicitly `UNKNOWN`; invented targets are prohibited.
5. Capacity claim such as “supports N users” is prohibited unless the tested workload model and confidence/limits support it.

**Evidence:** EC-3, EC-4, EC-7.  
**Case linkage:** REQ-016, REQ-020, REQ-021.  
**Risks:** RISK-0021, RISK-0033, RISK-0038.  
**Downstream:** T008 reliability/deployment research; T009 benchmark/statistics methodology; partner demand remains external.

### PROD-014 — Security and privacy evidence

**Requirement.** Production has a threat model and tested controls for authorization, isolation, untrusted inputs/uploads, secrets, dependencies, privilege and telemetry privacy.

**Acceptance tests / measurable outcomes.**

1. Threat model identifies assets, trust boundaries, tenant boundary, major abuse cases and control/test ownership (`BINARY_EVIDENCE_GATE`).
2. Authz and tenant-isolation negative/adversarial suites pass, including cross-tenant unauthorized access = `0` (`HARD_CONTRACT`).
3. Input/upload abuse suite covers path traversal, type/content mismatch, oversized input and parser failure modes with fail-closed expected outcomes (`BINARY_EVIDENCE_GATE`).
4. Secrets are not committed/logged/exposed in defined scans/tests; runtime secret access follows declared least-privilege policy (`BINARY_EVIDENCE_GATE`).
5. Dependency/software-supply-chain scanning and vulnerability disposition policy are defined and exercised (`BINARY_EVIDENCE_GATE`).
6. Privacy/legal claims (e.g. exact retention/legal basis/residency obligations) remain `UNKNOWN_EXTERNAL` until authoritative requirements are known; no compliance claim is inferred from technical controls alone.

**Evidence:** EC-2, EC-5, EC-7.  
**Case linkage:** PAIN-004, PAIN-005; REQ-001, REQ-012, REQ-018, REQ-021, REQ-024.  
**Risks:** RISK-0031, RISK-0032, RISK-0037.  
**Downstream:** T004 security/privacy/tenancy research; T013 supply-chain/toolchain evidence; T014 parser abuse/source trust.

### PROD-015 — Research-gated architecture

**Requirement.** Every material technology/architecture decision follows the DRG before becoming the production default.

**Acceptance tests / measurable outcomes.**

1. Material production decisions frozen without a DRG-compliant record = `0` (`BINARY_EVIDENCE_GATE`).
2. Each record states decision question, alternatives, current baseline, primary/authoritative sources, criteria, representative benchmark when testable, limitations/uncertainty and reversal conditions (`BINARY_EVIDENCE_GATE`).
3. A spike/bakeoff result is not silently converted into a production lock; promotion requires explicit synthesis/decision disposition (`BINARY_EVIDENCE_GATE`).
4. Existing W001-W004 components remain baseline/counterfactuals and are retained unless evidence supports replacement.

**Evidence:** EC-7.  
**Case linkage:** REQ-015, REQ-016, REQ-020, REQ-021, REQ-024.  
**Risks:** RISK-0007, RISK-0034, RISK-0040.  
**Downstream:** all W005 research tasks; T010 synthesis owns architecture selection, not T001.

### PROD-016 — Reproducible deployment

**Requirement.** The product can be deployed from a clean state with reproducible configuration/migrations, safe secret/config handling and observable health/start/restart behavior.

**Acceptance tests / measurable outcomes.**

1. A documented clean deployment/runbook succeeds from a clean checkout/environment using only declared prerequisites and externalized configuration/secrets (`BINARY_EVIDENCE_GATE`).
2. Health/readiness/startup/restart behavior is declared and exercised (`BINARY_EVIDENCE_GATE`).
3. Schema/data migrations are repeatable in the defined upgrade/rollback or forward-recovery scenarios; failure behavior is documented (`BINARY_EVIDENCE_GATE`).
4. Required artifact/source provenance is verifiable for the deployed release (`BINARY_EVIDENCE_GATE`).
5. Startup/deploy/recovery timing targets remain `TO_BE_ESTABLISHED_BY_EVIDENCE` unless owner constraints exist.

**Evidence:** EC-2, EC-4, EC-7.  
**Case linkage:** REQ-016, REQ-021, REQ-022.  
**Risks:** RISK-0018, RISK-0021, RISK-0033, RISK-0034.  
**Downstream:** T008 deployment/reliability and T013 developer-platform/toolchain research.

### PROD-017 — Production-grade final evidence

**Requirement.** Final evidence demonstrates the same real product path that is claimed for production; the mandatory video remains a bounded evidence artifact, not a substitute system.

**Acceptance tests / measurable outcomes.**

1. Final technical video duration `<= 5:00` (`HARD_CONTRACT`).
2. Demonstrated UI, workflow, provider/eval path and stored evidence can be correlated to the same real run/product path (`BINARY_EVIDENCE_GATE`).
3. Parallel fake/demo-only implementation used to satisfy the final claim = `0` (`BINARY_EVIDENCE_GATE`).
4. Any synthetic/replay/fixture evidence shown is explicitly labeled and cannot be used to satisfy a real-provider/runtime production claim.
5. Every applicable PROD-001..017 requirement is traceable to evidence before `PRODUCTION_READY`; open P0/critical production gaps prohibit that claim.

**Evidence:** EC-1..EC-8 as applicable, especially EC-8.  
**Case linkage:** REQ-022, REQ-023, REQ-021.  
**Risks:** RISK-0006, RISK-0016, RISK-0021, RISK-0024, RISK-0035.  
**Downstream:** final production validation after Phase 9; not closable during W005 research.

## 6. User / organization / workspace assumptions and unknowns

The contract requires these dimensions to be first-class but does not describe Suno's internal identity model. T001 therefore specifies behavior that must be declared/tested without inventing the partner's org chart.

| ID | Known / required | Unknown that must remain explicit | Acceptance implication |
|---|---|---|---|
| `UW-001` | authenticated `user` exists | identity provider / SSO / MFA policy | auth mechanism is a T004 DRG decision; no SSO claim yet |
| `UW-002` | `organization`, `workspace`, `user`, `run` are explicit dimensions | cardinalities and membership topology | chosen membership model must be documented and tested; do not claim it matches Suno internals |
| `UW-003` | RBAC/authz is required | exact roles/permissions/approval chain | role matrix remains `UNKNOWN_EXTERNAL` until owner/workflow evidence; T004 can propose candidate models only |
| `UW-004` | tenant isolation is hard | tenant == organization vs workspace semantics | isolation boundary must be explicitly declared before testing; no hidden default |
| `UW-005` | multi-user/shared runtime is required | concurrent users/jobs target | A-0012 remains open; capacity number requires T008/T009 evidence |
| `UW-006` | private content must be protected | data classification, residency, exact retention/deletion/legal basis | no privacy/compliance claim without authoritative input |
| `UW-007` | audit/provenance required | retention period and operator access model | values must be declared/researched, not invented |
| `UW-008` | strong audience production claims require stronger calibration | availability/identity of independent human annotators | T005 defines protocol; absence cannot be papered over as human evidence |
| `UW-009` | production operations require recovery/incident handling | on-call ownership, support hours, business SLO/SLA | remains `UNKNOWN_EXTERNAL`; technical tests may proceed without fabricated SLA |

## 7. Production claim boundaries

### Allowed before all production gates close

- “baseline mechanics passed within W004 tested scope” when backed by the existing artifact;
- “candidate architecture/control” when clearly marked pending DRG synthesis;
- “diagnostic-only threshold/metric” where calibration is insufficient;
- “observed latency/cost/reliability on workload X” with workload/config/time provenance;
- “production requirement unknown” where external/business evidence is missing.

### Prohibited until evidence exists

- `PRODUCTION_READY` while any applicable PROD requirement lacks its hard evidence;
- “supports N users” without representative load/capacity evidence;
- SLO/SLA numbers invented from current performance or intuition;
- “human validated/gold” based only on D-0017 automated blind calibration;
- “tenant isolated” without adversarial cross-tenant tests;
- “durable/highly available” from local SQLite/single-process smoke evidence;
- “secure/compliant” from the presence of scanners or libraries alone;
- “real provider path” when recipient UI is actually showing unlabeled mechanics-only/fixture output;
- “live cockpit” when evidence is stale/synthetic/unlinked to the current run;
- “production default” for any material stack choice without DRG-compliant synthesis.

## 8. Downstream research / experiment queue

| Need | Why T001 cannot close it | Evidence required | Risks | Primary downstream owner |
|---|---|---|---|---|
| identity/tenancy/authz model | partner topology and technology not known | threat model + alternative analysis + adversarial authz benchmark | RISK-0031 | T004 |
| API/frontend/live cockpit contract | UX/runtime boundary choices open | real-run prototype/bakeoff + stale/synthetic negative controls | RISK-0024,RISK-0035 | T002 |
| orchestration runtime | baseline exists but production concurrency/resume not proven | baseline vs candidates on exact 3x3 + failure/resume workload | RISK-0033,RISK-0039 | T003 |
| persistence/object storage | multi-replica/recovery/privacy controls unresolved | representative write/read/concurrency/recovery/security tests | RISK-0032,RISK-0033 | T004,T008 |
| human calibration/threshold statistics | D-0017 is insufficient for strong production claims | protocol + independent streams/equivalent + uncertainty/held-out | RISK-0020,RISK-0023,RISK-0036 | T005 |
| adaptive policy | objective weights/constraints and safe policy form open | offline/replay experiments under immutable hard gates | RISK-0039 | T006 |
| observability/redaction | signal backend/export/sampling choices open | correlation completeness + overhead/cardinality/redaction benchmark | RISK-0035,RISK-0037 | T007 |
| SLO/capacity/recovery targets | demand/business limits absent | saturation curve + failures + owner/business target input | RISK-0038 | T008,T009 |
| benchmark decision methodology | avoiding cherry-picking/sample noise | representative slices + statistical/uncertainty protocol | RISK-0034,RISK-0040 | T009 |
| developer platform / CI supply chain | manifest/toolchain deliberately not frozen | clean-build/test/release/provenance benchmark under DRG | RISK-0018,RISK-0034 | T013 |
| financial document parsing | production parser/source-trust quality unproven | numeric/date/entity/table-role/unit/provenance corpus benchmark | RISK-0010 | T014 |
| final architecture | requires all independent research inputs | explicit T010 synthesis + DRG records + reversal conditions | RISK-0034,RISK-0040 | T010 |

## 9. Standards / primary guidance used as requirement-shaping references

These sources shape **evidence expectations**, not technology selection or compliance claims.

1. **NIST SP 800-218, SSDF v1.1 (final, 2022).** NIST still lists v1.1 as final while SP 800-218 Rev.1 / SSDF v1.2 is an initial public draft as of this research date. Useful for secure-development practice/evidence structure.  
   - https://csrc.nist.gov/pubs/sp/800/218/final  
   - https://csrc.nist.gov/projects/ssdf/publications
2. **OWASP ASVS 5.0.0.** OWASP identifies 5.0.0 as the latest stable ASVS; useful as a candidate verification catalog for application technical security controls. Exact ASVS level/requirement adoption is a T004 decision, not frozen here.  
   - https://owasp.org/projects/asvs
3. **NIST SP 800-61 Rev.3 (final, April 2025).** Current NIST incident-response guidance; supports requiring incident/recovery preparedness without inventing organization-specific on-call/SLA facts.  
   - https://csrc.nist.gov/pubs/sp/800/61/r3/final
4. **SLSA v1.2 (Approved/current).** Useful for source/build provenance and supply-chain evidence; no SLSA level is mandated by T001.  
   - https://slsa.dev/spec/v1.2/
5. **NIST AI 600-1, Generative AI Profile (final, 2024).** Supports explicit GenAI risk/evaluation posture; it is a risk-management reference, not a provider/model selector.  
   - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
6. **Google SRE — Service Level Objectives.** Explicitly notes SLO target choice is not purely technical and has product/business implications; used here to justify keeping unsupported targets evidence/owner-driven rather than copying current performance.  
   - https://sre.google/sre-book/service-level-objectives/
7. **OpenTelemetry signal concepts.** Current documentation describes traces, metrics and logs as correlatable observability signals. Used only to validate the signal-level requirement shape in PROD-012; OpenTelemetry itself is **not** selected as the production implementation.  
   - https://opentelemetry.io/docs/concepts/signals/

## 10. DRG / decision posture

T001 makes no material stack selection. The acceptance taxonomy above is a decomposition of locked `D-0018`/Production Contract requirements plus current primary guidance.

No new `LOCKED` technology or architecture decision is proposed here. Any candidate framework/control mapping (for example, a specific OWASP ASVS level, SLSA level, auth method, telemetry stack, persistence engine, deployment platform or SLO target) remains **candidate/pending** until its owning W005 research task produces a DRG-compliant record and T010 synthesis explicitly disposes it.

## 11. Definition-of-done check for W005-T001

- [x] complete acceptance matrix for PROD-001..017;
- [x] every measurable requirement has an outcome/test or explicit non-quantification reason;
- [x] existing hard invariants preserved exactly;
- [x] user/tenant/workspace assumptions and unknowns explicit;
- [x] evidence-class map and production-claim boundaries explicit;
- [x] downstream research/experiments linked to current risks and W005 owners;
- [x] no stack selected;
- [x] unsupported thresholds remain `TO_BE_ESTABLISHED_BY_EVIDENCE`, `DECLARED_AND_TESTED`, or `UNKNOWN_EXTERNAL`;
- [x] primary/current guidance checked where it materially shaped acceptance evidence;
- [x] no material recommendation was silently promoted to a locked decision.
