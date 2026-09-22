# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.7.0`

`STATE_VERSION: 0038`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 7 — Blind Review, Final Deliverable & Defense`

`LAST_COMMITTED_WAVE: W004-INTERNAL-RELEASE-PROOF-COMPLETE`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002, W003 e W004 estão COMPLETE no escopo interno executável. O projeto permanece `ACTIVE` porque o Success Model exige finalização/submission verificadas e esses dados externos seguem desconhecidos.
- `D-0017` permanece LOCKED. A calibração aceita é `MODEL_AUTOMATED_BLIND_CALIBRATION`; ela satisfaz a dependência T005→T008, mas nunca vira human gold. Human gold/agreement/preference/validation continuam **not observed** e thresholds seguem `DIAGNOSTIC_ONLY`.
- W004-T005 A02: 36/36 DEVELOPMENT, exact target→automated `18/36 = 0.500000`, ordinal MAE `0.500000`, Cohen kappa diagnóstico `0.250000`, quadratic weighted kappa diagnóstico `0.437500`, 3 non-compensatory attention items, held-out intocado.
- W004-T006 A01: hard-gate invariant 36/36, hard-fail compensation `0`, automated-reference accuracy `0.083333` semantic-off e `0.083333` semantic-on, delta `+0.000000`; decisão `NO_BACKEND_PREFERENCE`.
- W004-T007 canônico é A05. Actions `35672174577`, oito chamadas Groq observadas, quatro DEVELOPMENT sources, mesmo prompt/config, A03 labels fora do quality gold, fresh-clone PASS. A02 permanece somente `NON_CANONICAL_DIAGNOSTIC_PROVENANCE_INVALID`.
- T007 A05: 120B preservation `3/4`, quality `0.952083`, numeric recall `0.958333`, concept recall `1.000000`, mean latency `1914.879 ms`, cost `0.0016201500 USD`; 20B preservation `2/4`, quality `0.927083`, numeric recall `0.958333`, concept recall `1.000000`, mean latency `1032.527 ms`, cost `0.0009102750 USD`; decisão `NO_OVERALL_MODEL_PREFERENCE`.
- W004-T008 A02 está INTEGRATED e fecha o clean-E2E final com provenance válida. Actions `35672891477` PASS em clean checkout; artifact `10671996898`, digest `sha256:20a514d9dd1ab76a64b9b7762a17a691174fc173e08636b55ddf54844b37f175`; source→9→eval→repair→aggregate `9/9`; repair `FAIL→PASS`, fresh hard gates true, siblings immutable true; canonical dependency T007-A05; fresh-clone PASS.
- O final demo durável continua byte-identical em `artifacts/submission/final-demo.mp4`, SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, `69.120s <= 300s`; T020 independent video/package review PASS com zero novos CRITICAL/HIGH.
- W004-T016 é fallback histórico superseded pelo caminho real T017/T019/T020/T021; no longer required for W004 completion.
- Final Review Protocol: contract/artifact/technical evidence está reconciliado; blind review independente permanece PASS no escopo do pacote real T020. O stop condition global não pode virar PASS enquanto deadline, submission mechanism e finalization reserve não forem verificáveis.
- deadline, submission mechanism, named owner/decision maker e workflow interno Suno permanecem `UNKNOWN`. Esses unknowns não são convertidos em fatos nem em PASS.

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
`T001 T002 T003 T004 T005 T006 T007 T008 T009 T010 T011 T012 T013 T014 T015 T017 T018 T019 T020 T021`

### CANCELLED / SUPERSEDED
- `W004-T016-A01` — fallback de captura manual superseded por T017/T019/T020/T021; não é mais requisito material.

### HISTORICAL / NON-CANONICAL
- `W004-T005-A01` — BLOCKED sob protocol anterior; D-0017 autorizou substituição sem relabelar esse attempt.
- `W004-T007-A01/A03/A04` — failed cleanly.
- `W004-T007-A02` — non-canonical diagnostic devido a multiple terminal signals.
- `W004-T008-A01` — non-canonical dependency-provenance drift; PR #145 fechado sem merge.

## Current success bottleneck

`EXTERNAL_FINALIZATION_AND_SUBMISSION_FACTS`

Não há trabalho técnico interno restante no critical path de W004. Os blockers remanescentes dependem de fatos externos: deadline/finalization reserve, mecanismo/formato final de submissão e, para adoção real, owner/workflow interno Suno.

## Evidence boundary

- calibration: `MODEL_AUTOMATED_BLIND_CALIBRATION` only;
- human gold/agreement/preference/validation: **not observed**;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- semantic backend: `NO_BACKEND_PREFERENCE`;
- overall provider/model: `NO_OVERALL_MODEL_PREFERENCE`;
- T008: `T008_INTERNAL_RELEASE_PROOF_PASS_READY_FOR_FINAL_RECONCILIATION` completed;
- blanket production readiness: **not claimed**;
- submission completed: **not claimed**.

## Next action

1. obtain/verify submission deadline and mechanism when they become externally available;
2. verify finalization reserve and exact submission checklist against those facts;
3. if named Suno owner/workflow becomes available, update adoption/Partner evidence; otherwise retain UNKNOWN;
4. only set `PROJECT_STATUS: COMPLETE` when Success + Partner + Quality stop conditions and global blind/traceability/assumption requirements satisfy the Success Model.

## Recovery point

Resume from STATE 0038. W004 internal execution is complete with T008-A02 integrated. Do not reopen automated calibration/provider/semantic work absent new material evidence; resume only on external finalization facts, new critical finding, or explicit operator scope change.
