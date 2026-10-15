# W008-T002 — Financial-claims compatibility and gap matrix

**Classification:** documentary inventory / implementation-neutral proposal; `NO_PRODUCTION_DEFAULT`.
**Basis:** exact inspected source files listed in `W008_T002_CONTRACT_INVENTORY.md`, W006 accepted scoped results and W007-T004 source-original diagnostics.

| ID | Requirement / target | Baseline already exists | Gap / uncertainty | Proposed bounded experiment | Priority |
|---|---|---|---|---|---|
| G-01 | Preserve PDF table row/column/value provenance | `TableCellProvenance` domain model and W007-T004 parser benchmarks | flat `PdfExtraction` cannot carry structured cells; `IngestResult` only flat text | typed backward-compatible transport adapter; verify actual Petrobras/BCB role evidence remains fail-closed | P0 |
| G-02 | Source-page fragments | `SourceSpan`, `ProvenanceRef`, `ParsedDocument` already typed | no full chain in currently inspected recipient path | source-original page/box/text/structured-cell mapping; verify hash and identity | P0 |
| G-03 | Typed financial claims ledger | typed Anchor/ProvenanceRef and generic `ParsedNode` | no dedicated claim assertion, modality and claim-to-output relation in inspected contracts | alternative schema bakeoff (extend existing, claims package, generic fact graph) | P1 |
| G-04 | Financial time/units/qualifiers | AnchorKind covers numeric/date/period, TableCell raw/normalized values | distinction period/accounting perimeter/forecast not formalized in recipient extraction | adversarial comparisons, qualified claim normalization & numerical checker | P1 |
| G-05 | Cross-output claim consistency | 3×3 variant identity and hard gates/reference E2E | no observed shared nine-output contradiction scoring by claim | nine-output negative-control corpus; targeted repair + fresh eval | P1 |
| G-06 | Human comprehension | versioned eval foundation and blind annotation schema | zero actual independent human primary streams or adjudicated gold | real blinded double annotation and separate adjudication with held-out | P0 external |
| G-07 | Editorial review and approval | live projected source/3×3 evidence and authz substrate reference | no verified editor/reviewer/approver versioned workflow in inspected live cockpit | approval state machine + two editor CAS and revocation E2E | P1, W007 gated |
| G-08 | Passport integrity | SHA-256 source identities and run/attempt/event manifests | no demonstrated portable per-piece source→claim→approval manifest | canonical export format + integrity, privacy and mutation tests | P2 |
| G-09 | Independent financial checks | source trust and factual-eval gates | no complete independent CVM/BCB numerical reconciliation observed | local deterministic calculations, optional official source diff and false-alert benchmark | P2 |
| G-10 | Source revisions and impact | immutable source identity | no observed source_version→claim→nine-output impact traversal | approved-source version-watch spike, diff and editorial approval | P3 |
| G-11 | Exports / CMS | native output formats and existing reference UI | approved secure export schema/CMS roundtrip not verified | versioned article/carousel/script export; authz/privacy and idempotency tests | P3 |
| G-12 | Editorial-value analytics | correlated reference telemetry | ROI/approval times and actual editorial baseline unknown | real event taxonomy; user-approved comparison with manual workflow | P3 |
| G-13 | Operational assurance | W006 reference tests and W007 qualification plan | no cloud-qualified GCP/AWS topology, human reference or full-prod readiness | resume exact W007 dependency-gated experiments with authorized external evidence | BLOCKER |

## Required compatibility decisions

- **Do not replace existing** `TableCellProvenance`, `ProvenanceRef`, `SourceSpan` or `Anchor` simply to rename them Financial Truth Engine.
- Preserve immutable source bytes and version/hash identity; table-role and qualifier confidence must be distinct from generic text-extraction confidence.
- Schema evolution needs explicit versioning, migration/rollback, authz and persisted event/replay plan.
- A source-grounded extraction result may be `REVIEW_REQUIRED` even when text was successfully parsed.
- Source claims and per-variant output claims are different objects. Referential binding must survive targeted repair and historical versions.
- No new schema lock from this report. EP-06 should supply DRG research, workload comparison, uncertainty and reversal conditions.

## Workstream mapping and measurable gates

| Product target | EP dependencies | Evidence |
|---|---|---|
| M01 Financial Truth Engine | EP-06 → EP-07 → EP-08 | source-original table-role, claim/support lineage, tenant-bound persistence |
| M02 Independent verifier | EP-08 → EP-09 | math/units/period error detections, false positives and contradiction disposition |
| M04 Audience Intelligence | EP-03 → EP-04 → EP-11 | real human agreement, calibration and held-out |
| M05 Cross-output consistency | EP-08 → EP-10 | critical cross-variant contradiction fail-closed and repair regression |
| M06 Editorial Workspace | EP-01,EP-08,EP-10 + W007 authz | multiuser e2e, revision, approval and leakage security tests |
| M07–M08 Policy/Passport | EP-12 → EP-13 → EP-14 | no critical policy override, integrity and redaction |
| M09–M10 Benchmark/adaptive | EP-03,EP-11,EP-15 + W007 | paired raw results, hard gates, eligible Pareto, rollback |
| M03/M11/M12 operational expansion | EP-12 and qualified owners | allowed source changes, secure exports and measured editorial value |

## Recommendation

Start compatibility research at **G-01 + G-02**, not a speculative new graph framework. Then quantify incremental value of claims and nine-output consistency. Research-only status `PENDING_EVIDENCE`. External W007 cloud/human blockers remain unchanged.
