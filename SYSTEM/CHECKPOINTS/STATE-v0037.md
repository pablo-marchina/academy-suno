# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.7.0`

`STATE_VERSION: 0037`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 7 — Blind Review, Final Deliverable & Defense`

`LAST_COMMITTED_WAVE: W004-T007-PROVENANCE-REPAIR`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE.
- `D-0017` continua LOCKED: `MODEL_AUTOMATED_BLIND_CALIBRATION` satisfaz o critical path W004-T005→T008, mas nunca vira human gold; claims de human agreement/preference/validation permanecem proibidos e thresholds continuam `DIAGNOSTIC_ONLY`.
- W004-T005 A02 permanece INTEGRATED sob D-0017: 36/36 DEVELOPMENT joined pós-freeze por hash; exact target→automated `18/36 = 0.500000`; ordinal MAE `0.500000`; diagnostic Cohen kappa `0.250000`; diagnostic quadratic weighted kappa `0.437500`; 3 non-compensatory attention items; held-out intocado.
- W004-T006 A01 permanece INTEGRATED: semantic-off/on sobre 36/36 DEVELOPMENT, hard-gate invariant 36/36, hard-fail compensation `0`, automated-reference accuracy `0.083333` off e `0.083333` on, delta `+0.000000`; decisão `NO_BACKEND_PREFERENCE`.
- W004-T007 A01/A03/A04 são históricos failed-cleanly. A02 produziu bytes observados, mas é `NON_CANONICAL_DIAGNOSTIC_PROVENANCE_INVALID` porque emitiu `TASK_BLOCKED` e depois `TASK_COMPLETE` sob o mesmo attempt ID; seus bytes permanecem no histórico e não satisfazem o DAG.
- W004-T007 A05 é o attempt canônico INTEGRATED: Actions `35672174577`, oito chamadas Groq observadas, quatro DEVELOPMENT sources, mesmo prompt/config, A03 automated labels fora do quality gold, lifecycle attempt-valid e fresh-clone PASS.
- T007 A05 bounded source-preservation: 120B `3/4`, quality `0.952083`, numeric recall `0.958333`, concept recall `1.000000`, mean latency `1914.879 ms`, total tokens `3643`, derived cost `0.0016201500 USD`; 20B `2/4`, quality `0.927083`, numeric recall `0.958333`, concept recall `1.000000`, mean latency `1032.527 ms`, total tokens `3977`, derived cost `0.0009102750 USD`.
- T007 decision permanece `NO_OVERALL_MODEL_PREFERENCE`: a evidência mostra trade-off bounded source-preservation/latency/cost, não human preference ou general production superiority.
- `human_gold_eligible=false`, `human_agreement_observed=false`, `human_preference_observed=false` permanecem invariantes.
- W004-T008 A01 executou um proof técnico PASS em Actions `35672482500`, porém iniciou antes da reparação de provenance e consumiu STATE 0036 que ainda promovia T007-A02; portanto A01 é `NON_CANONICAL_DEPENDENCY_PROVENANCE_DRIFT`, PR #145 foi fechado sem merge e o attempt não satisfaz T008.
- O próximo attempt legítimo de T008 é `A02`, a partir deste STATE 0037 e do main pós-reparação, reutilizando somente evidência canônica T007-A05.
- T019/T020/T021 permanecem PASS em demo/package/durability: accepted MP4 SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, 69.12s, independent review PASS e cópia byte-identical persistida em `artifacts/submission/final-demo.mp4`.
- T016 é fallback histórico não material porque T017/T019/T020/T021 fecharam o caminho real de demo.
- deadline, submission mechanism, owner/decision maker e workflow interno Suno continuam UNKNOWN.

## Locked decisions

- `D-0001` GitHub canônico.
- `D-0002` Workers não integram.
- `D-0003` Paralelismo versionado.
- `D-0004` Guardrails executáveis.
- `D-0005` Lease exclusivo.
- `D-0006` Proveniência por tentativa.
- `D-0007` Checkpoints/DAG.
- `D-0009` Loop até gates/stop.
- `D-0011` Partner Contract/Jury/Adoption.
- `D-0012` Balanced Total Success dominante.
- `D-0013` Traceability + assumptions gates.
- `D-0014` Blind Review + deadline reserve.
- `D-0015` Lifecycle de worker observável por sinais duráveis.
- `D-0016` Foundation invariants lockados; implementation identities evidence-driven.
- `D-0017` automated blind calibration evidence substitution waiver para W004-T005→T008.

## W004 lifecycle

### INTEGRATED
`T001 T002 T003 T004 T005 T006 T007 T009 T010 T011 T012 T013 T014 T015 T017 T018 T019 T020 T021`

### READY
- `W004-T008-A02` — fresh final clean-E2E release proof, Issue #88, using canonical T007-A05.

### HISTORICAL / NON-CANONICAL
- `W004-T005-A01` — BLOCKED sob protocol 1.6.0 por ausência de humanos; superseded operacionalmente por D-0017, nunca relabelado complete.
- `W004-T007-A01` — FAILED_CLEANLY_PROVIDER_OUTPUT_TRUNCATION.
- `W004-T007-A02` — NON_CANONICAL_DIAGNOSTIC_PROVENANCE_INVALID; multiple terminal signals.
- `W004-T007-A03/A04` — failed cleanly before accepted provider comparison.
- `W004-T008-A01` — NON_CANONICAL_DEPENDENCY_PROVENANCE_DRIFT; technical PASS preserved, PR #145 closed without merge.
- `W004-T016-A01` — screen-recording fallback branch; real demo path completed elsewhere.

## Current success bottleneck

`FINAL_CLEAN_E2E_RELEASE_PROOF_ATTEMPT_VALID`

O critical path é W004-T008-A02, seguido por reconciliação final de reviews, risks, traceability e scorecards.

## Evidence boundary

- accepted calibration class: `MODEL_AUTOMATED_BLIND_CALIBRATION`;
- human gold/agreement/preference: **not observed**;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- human sample: optional enhancement, not dependency;
- semantic result: no measured reference-accuracy gain for tested deterministic proxy;
- provider/model result: attempt-valid A05 bounded trade-off only, no overall model preference;
- completion may proceed only if final claims stay within these boundaries and residual absence of human evidence remains explicit.

## Next action

1. dispatch `W004-T008-A02` from STATE 0037;
2. execute clean-E2E release proof using canonical T007-A05 evidence;
3. integrate accepted T008 A02 result;
4. reconcile final reviews, risks, traceability, Success/Partner/Quality scorecards and stop conditions.

## Recovery point

Resume from STATE 0037. T005/T006/T007-A05 are integrated under D-0017 evidence boundaries. T008-A02 is READY and is the only remaining critical-path task before final reconciliation.
