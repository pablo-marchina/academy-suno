# Blind / Adversarial Review — W004-T013-A01

## Review identity

- `TASK_ID: W004-T013`
- `ATTEMPT_ID: A01`
- `BASE_STATE_VERSION: 0023`
- `BASE_COMMIT_SHA: 2fcf016ade631e9307ec0d222d633c066adf4c88`
- `WORKER_BRANCH: worker/W004-T013-A01`
- role: Critic / Auditor

## Method and scope

The evaluator pass treated the package as a recipient-facing submission rather than granting credit for internal intent. The blind-pass inputs were the primary case transcription plus the current submission-facing artifacts and executable entry points: `README.md`, `docs/demo/DEMO_SCRIPT.md`, `docs/release/EVIDENCE_PACKET.md`, `docs/release/FINAL_REVIEW_CHECKLIST.md`, `docs/cockpit/README.md`, `app/evidence_cockpit.py`, and the current parser/source-trust documentation. Requirement/risk IDs were mapped only after the findings were formed.

Searches of the repository were also used to check whether a final demo recording/link, presentation/deck, interactive web framework, or raw PDF-upload/ingestion entry point was discoverable in the current package.

## Review outcome

`BLIND_REVIEW: NOT_PASS`

This is **not** a claim that the implemented mechanics are poor. The package is unusually disciplined about separating `PROVEN`, `DIAGNOSTIC_ONLY`, `PRODUCTION_UNKNOWN`, `BLOCKED`, and `PENDING`. The negative review status comes from mandatory submission/evidence gaps that a final recipient cannot waive:

1. a final real demo video is not present/discoverable, despite the video being an eliminatory requirement;
2. independent human calibration/confusion-matrix evidence is still absent;
3. real provider quality/latency/usage/cost evidence is still absent;
4. the current recipient-facing UI is a read-only HTML renderer over persisted artifacts rather than a clearly interactive document-to-3x3 application;
5. the current package does not demonstrate a raw PDF/text ingestion path from a real document through the end-user flow;
6. a consolidated final experimental report is not yet present; the release packet explicitly identifies itself as a preparation shell.

No positive final/release PASS is valid while the required human/provider gates remain absent.

## Deliverable audit

| Deliverable | Current evaluator status | Evidence visible to recipient | Gap / interpretation |
|---|---|---|---|
| DEL-001 — structured adaptation pipeline + GitHub | `PARTIAL / MECHANICS_PROVEN` | exact 3×3 mechanics, graph/state/RunStore, repair lineage, parser/source-trust probes | no current recipient-facing raw PDF/text ingestion path was found; W004 parser fixtures are manually curated and raw-byte replay/OCR remain open |
| DEL-002 — hybrid evaluation suite | `PARTIAL / STRONG_CORE, CALIBRATION_BLOCKED` | deterministic hard gates, PT-BR readability/domain diagnostics, grounding/factuality, anti-gaming posture | audience thresholds remain diagnostic until independent human gold exists |
| DEL-003 — autocorrection / reflection | `PASS_WITHIN_CONTROLLED_SCOPE` | persisted deterministic FAIL→repair→fresh re-evaluation→PASS lineage | scope must stay `MECHANICS_ONLY`; this is not provider/model quality evidence |
| DEL-004 — demo interface/dashboard | `PARTIAL / ADHERENCE_RISK` | 3×3 comparison, provenance, repair and telemetry rendered to HTML | current `app/evidence_cockpit.py` is a CLI that renders a read-only HTML snapshot from existing artifacts; no interactive upload/run application was found |
| DEL-005 — demo video + technical presentation | `FAIL / CRITICAL_SUBMISSION_GAP` | storyboard target 4:40 with hard cap 5:00 | no final recording or submission video link is discoverable; actual runtime and live proof are unverified; no separate presentation/deck was found if one is expected |
| DEL-006 — experimental report + documentation | `PARTIAL / BLOCKED` | strong README, component docs, evidence packet shell | no consolidated final experimental report; required confusion matrices and observed provider cost/latency trade-offs remain unavailable |

## Findings

### F-001 — CRITICAL — Final real demo video is absent from the current package

**Class:** internally fixable submission artifact, with dependencies on whatever evidence is available at recording time.

**Maps to:** `REQ-022`, `REQ-023`, `CRIT-001`, `RISK-0006`, `A-0001`.

**Observed:** the repository contains a detailed `docs/demo/DEMO_SCRIPT.md` targeting 4:40, but no final recording, immutable video artifact, or external video link was discoverable in the current package. A storyboard does not satisfy the case rule that absence of the video, or a video that does not prove real code/interface operation, invalidates the technical delivery.

**Required action before submission:** record the real demo, keep measured runtime below 5:00, show actual code plus interface operation, persist/link the exact submission artifact, and record its duration/version in the release packet/checklist.

---

### F-002 — HIGH — Raw PDF/text ingestion is not demonstrated in the recipient-facing flow

**Class:** internally fixable case-adherence gap.

**Maps to:** `REQ-001`, `RISK-0010`, `A-0008`.

**Observed:** the case requires receiving real public financial documents in PDF/text. The current W004 parser corpus is documented as manually curated from primary sources; raw response bytes were unavailable and OCR remains outside the attempt. Repository search and the current app/demo entry points did not surface a user-facing raw PDF/text ingestion/upload path that is exercised in the release story.

**Why this matters:** a judge can reasonably ask, “Where do I give the system a real document?” and the current demo plan begins from proof artifacts rather than from that case input boundary.

**Required action:** expose one minimal, reproducible real-document entry point and demo at least one actual PDF/text source through provenance-preserving ingestion into the pipeline. Preserve the existing fail-closed source-trust semantics; do not claim parser production readiness without raw-byte/OCR evidence.

---

### F-003 — HIGH — Current dashboard is a static/read-only HTML evidence projection, not clearly the interactive application described by the case

**Class:** internally fixable deliverable-adherence risk.

**Maps to:** `REQ-014`, `REQ-018`, `PAIN-004`.

**Observed:** `app/evidence_cockpit.py` is an argparse CLI that loads existing RunStore/proof/telemetry/calibration artifacts and writes HTML. Its own documentation correctly calls it a “read-only projection.” No Streamlit/FastAPI/Gradio-style interactive upload/run surface was discoverable.

**Why this matters:** the brief describes an interactive demo application/dashboard for document processing, side-by-side outputs, source traceability and evaluator metrics. The current cockpit is strong as an audit view, but a recipient may judge the input-to-output application requirement as only partially satisfied.

**Required action:** either add a minimal interactive local web surface that invokes the real pipeline and then opens the evidence view, or obtain explicit organizer confirmation that the generated HTML cockpit satisfies the interface deliverable. Until then, canonical status should avoid implying this interpretation is closed.

---

### F-004 — HIGH — Demo mechanics are real, but generation evidence remains deterministic-stub/mechanics-only

**Class:** mixed; internal communication risk plus external provider dependency.

**Maps to:** `REQ-003`, `REQ-017`, `RISK-0021`, `RISK-0022`.

**Observed:** README and demo script correctly disclose that the controlled 3×3 proof uses `deterministic_stub` and `MECHANICS_ONLY`. This is good evidence discipline. However, the planned demo’s central end-to-end proof is therefore proof of orchestration/repair mechanics, not observed model/provider content quality.

**Required action:** preserve the explicit scope language. When authorized provider evidence exists, add an observed comparable run without replacing the deterministic regression proof. Before then, never describe the controlled proof as “real provider generation,” “production quality,” or evidence of provider preference.

---

### F-005 — HIGH — Audience calibration and required confusion matrices remain externally blocked

**Class:** external evidence blocker.

**Maps to:** `REQ-004`, `REQ-005`, `REQ-006`, `REQ-010`, `REQ-011`, `REQ-019`, `RISK-0003`, `RISK-0004`, `RISK-0020`, `RISK-0023`, `A-0004`, `A-0006`.

**Observed:** the package accurately states that two genuinely independent blind human primary streams, agreement/adjudication, target→human matrix, and human→evaluator matrix do not yet exist. Thresholds are therefore `DIAGNOSTIC_ONLY`.

**Required action:** obtain two genuinely independent human annotation streams through the existing operator, execute the predeclared agreement/adjudication protocol, and version both required matrices. No model/pseudo-human or requested target labels may substitute for human gold.

---

### F-006 — HIGH — Real provider quality/latency/usage/cost trade-offs remain externally blocked

**Class:** external evidence blocker.

**Maps to:** `REQ-020`, `RISK-0017`, `RISK-0019`, `RISK-0022`.

**Observed:** the package correctly keeps provider quality, latency, usage and commercial cost as `PRODUCTION_UNKNOWN/BLOCKED`. The manual credential-safe path exists, but no authorized observed provider execution is present.

**Required action:** execute the existing manual provider evidence path with an authorized credential/runtime, persist provider/model/version/usage/latency provenance, and compute commercial cost only from observed eligible usage plus official pricing provenance.

---

### F-007 — HIGH — No consolidated final experimental report is present

**Class:** internally fixable packaging gap, with sections externally blocked.

**Maps to:** `REQ-019`, `REQ-020`, `REQ-021`, DEL-006.

**Observed:** the README and evidence packet are strong supporting documents, but `docs/release/EVIDENCE_PACKET.md` explicitly identifies itself as a “release-preparation shell,” not final approval/report. No separate final experimental report consolidating methodology, experiments, matrices, cost/latency trade-offs, limitations and reproducibility was discoverable.

**Required action:** create a final report artifact now with a stable structure and current evidence; keep missing human/provider sections visibly blocked. Populate the matrices and observed economics only after valid evidence arrives. This prevents the final fan-in from becoming last-minute document assembly.

---

### F-008 — MEDIUM — The 4:40 storyboard controls schedule risk, but actual <=5:00 compliance is unverified

**Class:** internally fixable demo QA.

**Maps to:** `REQ-023`, `RISK-0006`, `A-0001`.

**Observed:** the storyboard has a sensible 20-second buffer and explicit overrun cuts, but only the final rendered recording can prove the hard cap.

**Required action:** measure the final exported video duration; fail submission QA if it is above 5:00. Preserve the explicit unknown/blocker section and FAIL→repair proof when trimming.

---

### F-009 — MEDIUM — Some canonical traceability statuses are stronger than a blind recipient can independently verify today

**Class:** internal consistency/proposal; worker does not modify canonical files.

**Maps to:** `REQ-001`, `REQ-014`, `REQ-018`, `RISK-0010`.

**Observed:** traceability currently records the interface as implemented and ingestion/source readiness as structurally advanced. The underlying caveats are documented, but a blind recipient sees a static evidence renderer and manually curated parser fixtures rather than an interactive raw-document workflow.

**Proposed canonical follow-up:** reword those rows, if the Orchestrator agrees, so they distinguish (a) implemented evidence rendering/source-trust contracts from (b) still-open end-user interactive ingestion/demo proof. No historical evidence should be downgraded; only the scope should be made recipient-proof.

---

### F-010 — MEDIUM — Submission logistics and partner operating context remain unresolved

**Class:** external/organizational unknown.

**Maps to:** `RISK-0011`, `A-0002`.

**Observed:** deadline, submission mechanism, named owner/decision maker and internal Suno workflow are still unknown. The final checklist already acknowledges this.

**Required action:** resolve or explicitly disclose these items before packaging. At minimum, identify the actual submission channel and artifact constraints so a technically correct package is not rejected operationally.

## Overclaim / consistency scan

### Strong controls already working

- README explicitly labels the deterministic proof `MECHANICS_ONLY` and says it is not provider-quality evidence.
- Evidence packet keeps human matrices as placeholders rather than fabricating them.
- Provider quality/latency/usage/cost stay `PRODUCTION_UNKNOWN/BLOCKED`.
- Parser documentation refuses to select a winner without same-raw-byte comparison and keeps OCR/raw replay open.
- Demo script explicitly says `MECHANICS_ONLY` does not imply provider quality or production readiness.
- The 5:00 contradiction is handled conservatively with a 4:40 target.

### Language to keep avoiding

Do not use any of the following until the matching evidence exists:

- “production ready” / “release ready”;
- “calibrated audience thresholds”;
- “validated confusion matrix” without independent human gold;
- “provider/model winner”;
- “real provider cost” from synthetic pricing;
- “production parser” or “parser winner”;
- “interactive app complete” unless the recipient-facing interaction expected by DEL-004 is actually demonstrated.

## Prioritized internal fixes

1. **P0 — Record/package the final <=5:00 video** and bind it to the exact code/artifact version shown.
2. **P0 — Close the visible input-boundary gap:** provide a minimal real PDF/text → provenance → pipeline demo path.
3. **P0/P1 — Make DEL-004 recipient-proof:** add a minimal interactive application layer or obtain explicit acceptance of the static cockpit interpretation.
4. **P1 — Create the consolidated experimental report shell now**, with blocked sections explicit and exact insertion points for T005/T006/T007/T008.
5. **P1 — Rehearse the final demo from clean checkout** after T012 and measure actual recording duration.
6. **P1 — Reconcile traceability wording** so “implemented” claims carry the same scope visible to a blind evaluator.
7. **P2 — Resolve submission logistics/owner/workflow unknowns** before final packaging.

These internal actions can proceed without fabricating or waiting for external human/provider evidence. They do not replace T005/T006/T007/T008.

## External blockers that must remain blockers

1. two genuinely independent human primary annotation streams;
2. agreement/adjudication and observed target→human + human→evaluator matrices;
3. authorized observed provider runs with comparable quality/latency/usage/cost provenance;
4. downstream semantic ablation on valid human gold;
5. final W004-T008 clean E2E fan-in and final review.

## Adversarial questions the final defense must answer

- “Show me where I upload or provide a real financial PDF/text and how it reaches the 3×3 output.”
- “Is this dashboard actually running the system, or only rendering previously generated evidence?”
- “Which result is human-validated versus only deterministic/mechanics evidence?”
- “Where are the two confusion matrices required by the brief?”
- “Which latency and cost numbers were actually observed from a credentialed provider run?”
- “What exactly changed during FAIL→repair→PASS, and can you prove siblings were untouched?”
- “Why should I trust the parser on a raw PDF if current W004 fixtures were manually curated?”
- “Where is the final video, what is its measured runtime, and which commit did it demonstrate?”
- “What remains unknown, and which unknowns would block production adoption?”

## Acceptance summary

- review against case requirements/deliverables: **DONE**;
- <=5:00 constraint reviewed: **DONE — storyboard controlled, final runtime unverified**;
- overclaims/inconsistencies/demo/repro risks identified: **DONE**;
- findings mapped to REQ/RISK + severity: **DONE**;
- internal fixes separated from external blockers: **DONE**;
- final PASS withheld while human/provider evidence is absent: **DONE**.
