# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.7.0`

`STATE_VERSION: 0036`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 7 — Blind Review, Final Deliverable & Defense`

`LAST_COMMITTED_WAVE: W004-SEMANTIC-PROVIDER-EVIDENCE-FANIN`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE.
- `D-0017` continua LOCKED: `MODEL_AUTOMATED_BLIND_CALIBRATION` satisfaz o critical path W004-T005→T008, mas nunca vira human gold; claims de human agreement/preference/validation permanecem proibidos e thresholds continuam `DIAGNOSTIC_ONLY`.
- W004-T005 A02 permanece INTEGRATED sob D-0017: 36/36 DEVELOPMENT joined pós-freeze por hash; exact target→automated `18/36 = 0.500000`; ordinal MAE `0.500000`; diagnostic Cohen kappa `0.250000`; diagnostic quadratic weighted kappa `0.437500`; 3 non-compensatory attention items; held-out intocado.
- W004-T006 A01 está INTEGRATED: semantic-off/on sobre 36/36 DEVELOPMENT, hard-gate invariant 36/36, hard-fail compensation `0`, decision changed `33`, REVIEW_REQUIRED resolved `33`; automated-reference accuracy `0.083333` com semantic-off e `0.083333` com semantic-on, delta `+0.000000`; decisão `NO_BACKEND_PREFERENCE`.
- W004-T007 A01 é histórico FAILED_CLEANLY por provider output truncation e nunca foi aceito.
- W004-T007 A02 está INTEGRATED com comparação observada Groq 120B vs 20B em quatro DEVELOPMENT sources / 8 chamadas, mesmo prompt/config e A03 fora do quality gold.
- T007 A02 bounded source-preservation: 120B `3/4`, quality `0.952083`, numeric recall `0.958333`, concept recall `1.000000`, mean latency `1529.626 ms`, derived cost `0.0016681500 USD`; 20B `1/4`, quality `0.856250`, numeric recall `0.875000`, concept recall `1.000000`, mean latency `987.818 ms`, derived cost `0.0009480750 USD`.
- T007 decision permanece `NO_OVERALL_MODEL_PREFERENCE`: a evidência mostra trade-off bounded source-preservation/latency/cost, não human preference ou general production superiority.
- `human_gold_eligible=false`, `human_agreement_observed=false`, `human_preference_observed=false` permanecem invariantes.
- W004-T008 A01 agora está READY: todas as dependências T001/T003/T005/T006/T007 estão satisfeitas. Deve executar clean-checkout release proof, source→9→eval→repair→aggregate, cockpit evidence e pacote final sem converter unknowns em PASS.
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
- `W004-T008-A01` — final clean-E2E release proof, Issue #88.

### HISTORICAL / NON-CRITICAL
- `W004-T005-A01` — BLOCKED sob protocol 1.6.0 por ausência de humanos; superseded operacionalmente por D-0017, nunca relabelado complete.
- `W004-T007-A01` — FAILED_CLEANLY_PROVIDER_OUTPUT_TRUNCATION; sem accepted comparison artifact.
- `W004-T016-A01` — screen-recording fallback branch; real demo path completed elsewhere.

## Current success bottleneck

`FINAL_CLEAN_E2E_RELEASE_PROOF`

O critical path é W004-T008-A01, seguido por reconciliação final de reviews, risks, traceability e scorecards.

## Evidence boundary

- accepted calibration class: `MODEL_AUTOMATED_BLIND_CALIBRATION`;
- human gold/agreement/preference: **not observed**;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- human sample: optional enhancement, not dependency;
- semantic result: no measured reference-accuracy gain for tested deterministic proxy;
- provider/model result: bounded trade-off only, no overall model preference;
- completion may proceed only if final claims stay within these boundaries and residual absence of human evidence remains explicit.

## Next action

1. dispatch `W004-T008-A01` from STATE 0036;
2. execute clean-E2E release proof and final evidence packet;
3. integrate accepted T008 result;
4. reconcile final reviews, risks, traceability, Success/Partner/Quality scorecards and stop conditions.

## Recovery point

Resume from STATE 0036. T005/T006/T007 are integrated under D-0017 evidence boundaries. T008 is READY and is the only remaining critical-path task before final reconciliation.
