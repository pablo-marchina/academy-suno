# CHECKPOINT — STATE v0019

`PROTOCOL_VERSION: 1.6.0`
`STATE_VERSION: 0019`
`WAVE: W003`
`STATUS: ACTIVE`

## Integrated through this checkpoint

- W003-T001…T008 accepted and integrated.
- T008 calibration release gate is implemented and tested, but its evidence disposition is intentionally `DIAGNOSTIC_ONLY` because current gold-v001 has no independent human labels/agreement sufficient for threshold freeze.
- Anti-gaming release gate: PASS.
- Audience calibration: NOT_COMPUTABLE with current valid evidence.
- Semantic ablation: NOT_RUN / NO_BACKEND_PREFERENCE.
- Provider comparison: NOT_COMPARABLE / NO_PREFERENCE.
- Held-out tuning exposure remains forbidden.
- Hard source/factual/policy precedence remains non-compensatory.

## DAG recovery

`W003-T009` is the only remaining required W003 task and becomes READY after this checkpoint is merged and its Issue is rebound to the exact post-merge main SHA.

## Recovery rule

Resume from canonical `SYSTEM/STATE.md` at STATE 0019, then read Issue #67 and `SYSTEM/DISPATCH/W003-T009-A01.md`. Do not freeze audience thresholds, semantic backend, provider/model, parser library, or real pricing without new measured evidence.
