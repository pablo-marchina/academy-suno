# Final Review / Submission Checklist

This checklist is intentionally conservative. A checked mechanics/demo item must never be used to imply that external evidence gates passed.

## Reproducibility and artifact integrity

- [ ] Fresh checkout uses the README clean-start commands successfully.
- [ ] `python scripts/release_smoke/run_release_smoke.py ...` exits 0 and emits a `PASS` manifest.
- [ ] Cockpit HTML is regenerated from the proof/runstore/telemetry artifacts used by the packet.
- [ ] Demo shows a **persisted** FAIL→repair→PASS lineage with before/after hashes, not an invented slide.
- [ ] Source/run/job/attempt/evidence-scope provenance remains visible.
- [ ] Parser wrong-role corruption remains `FAIL`; missing provenance is not promoted to PASS.
- [ ] No secret, token, credential or private annotation identity is present in committed artifacts.

## Evidence-state integrity

- [ ] `PROVEN` claims include a precise scope.
- [ ] Audience threshold claims remain `DIAGNOSTIC_ONLY` unless valid human calibration later changes the evidence.
- [ ] Real provider/model quality, latency, usage and cost remain `PRODUCTION_UNKNOWN` until observed valid evidence exists.
- [ ] External missing evidence is called `BLOCKED`; downstream work not yet executed is called `PENDING`.
- [ ] No aggregate score hides a `FAIL`, `BLOCKED`, `PENDING` or unknown state.

## External blockers — must be resolved before a positive final release claim

- [ ] **Human evidence:** two genuinely independent blind primary streams for all 36 development items exist with provenance and completion checks.
- [ ] **Human calibration:** pre-adjudication agreement and predeclared adjudication have been executed; observed target→human and human→evaluator matrices are versioned.
- [ ] **Provider evidence:** at least the provider/model executions required by T007 are credentialed, observed, provenance-complete and comparable.
- [ ] **Provider economics:** latency/usage are observed and cost, if claimed, uses observed usage plus eligible official pricing provenance.
- [ ] **Semantic decision:** T006 ablation uses the same valid development human gold and does not alter hard-gate semantics.
- [ ] **W004-T008:** final clean E2E release proof is complete and references the exact above evidence.

## Submission packaging

- [ ] Evidence packet placeholders have been replaced only by real versioned artifacts; unresolved placeholders remain visibly `PENDING`.
- [ ] Demo stays within the hard 5:00 cap (target script: 4:40).
- [ ] Demo/video never calls deterministic-stub output “provider quality” or “production”.
- [ ] README, demo and evidence packet use the same evidence-state vocabulary.
- [ ] Deadline, submission mechanism, named owner/decision maker and any partner workflow unknowns have been resolved or explicitly disclosed as unknowns.
- [ ] Final claim language matches the strongest evidence actually present at submission time.

## Stop condition

If any required external blocker above is unchecked, W004-T011 artifacts may still be submitted for review as preparation, but production/release readiness must remain `PENDING`. T011 does not replace W004-T008.
