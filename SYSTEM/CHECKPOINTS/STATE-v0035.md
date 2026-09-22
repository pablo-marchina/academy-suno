# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.7.0`

`STATE_VERSION: 0035`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 7 — Blind Review, Final Deliverable & Defense`

`LAST_COMMITTED_WAVE: W004-AUTOMATED-CALIBRATION-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE.
- `D-0017` continua LOCKED: `MODEL_AUTOMATED_BLIND_CALIBRATION` pode satisfazer o critical path W004-T005→T008, mas nunca vira human gold; claims de human agreement/preference/validation permanecem proibidos e thresholds continuam `DIAGNOSTIC_ONLY`.
- W004-T005 A02 está INTEGRATED sob D-0017. Actions `35670345067`, artifact `10670369391`, fresh-clone verification PASS.
- T005 A02 fez join pós-freeze 36/36 por `blind.output_sha256 == frozen.content_sha256`; target não foi exposto durante A03 e held-out permaneceu intocado.
- target→automated calibration: exact match `18/36 = 0.500000`; ordinal MAE `0.500000`; diagnostic Cohen kappa `0.250000`; diagnostic quadratic weighted kappa `0.437500`; 3 itens exigem atenção por non-compensatory factual/concept checks.
- `human_gold_eligible=false`, `human_agreement_observed=false`, `human_preference_observed=false` permanecem invariantes.
- W004-T006 A01 e W004-T007 A01 estão READY e podem rodar em paralelo a partir deste estado.
- T006 deve medir semantic-off/on incremental value contra o reference set automatizado aceito, mantendo hard source/factual/policy failures invariantes e sem human-preference claim.
- T007 deve produzir comparação provider/model evidence-bounded. T004 A08 já fornece Groq `openai/gpt-oss-120b` mechanics observados: Models/Responses HTTP 200, latency `349.694 ms`, usage `84/61/145`, derived cost `4.92e-05 USD`, strict importer PASS. Qualidade/model selection só pode ser afirmada com comparação diretamente observada e comparável.
- W004-T008 permanece PLANNED e depende de T005/T006/T007 mais T001/T003.
- T019/T020/T021 permanecem PASS em demo/package/durability: accepted MP4 SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, 69.12s, independent review PASS e cópia byte-identical persistida em `artifacts/submission/final-demo.mp4`.
- T016 é fallback histórico não material porque T017/T019/T020/T021 fecharam o caminho real de demo; não deve bloquear o critical path atual.
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
`T001 T002 T003 T004 T005 T009 T010 T011 T012 T013 T014 T015 T017 T018 T019 T020 T021`

### READY
- `W004-T006-A01` — semantic-off/on ablation, Issue #86.
- `W004-T007-A01` — provider/model comparison, Issue #87.

### PLANNED
- `W004-T008-A01` — final clean-E2E fan-in, Issue #88, after T006/T007.

### HISTORICAL / NON-CRITICAL
- `W004-T005-A01` — BLOCKED under protocol 1.6.0 for absent humans; superseded operationally by D-0017, never relabeled complete.
- `W004-T016-A01` — screen-recording fallback branch; real demo path completed elsewhere.

## Current success bottleneck

`SEMANTIC_AND_PROVIDER_MODEL_EVIDENCE_FANOUT`

O critical path agora é totalmente executável internamente: T006 e T007 em paralelo, depois T008 e reviews/scorecards finais.

## Evidence boundary

- accepted calibration class: `MODEL_AUTOMATED_BLIND_CALIBRATION`;
- human gold/agreement/preference: **not observed**;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- human sample: optional enhancement, not dependency;
- provider mechanics do not imply quality;
- completion may proceed only if final claims stay within these boundaries and residual absence of human evidence remains explicit.

## Next action

1. dispatch `W004-T006-A01` and `W004-T007-A01` in parallel from STATE 0035;
2. integrate accepted results and release T008;
3. execute T008 clean-E2E final proof;
4. reconcile final reviews, risks, traceability, Success/Partner/Quality scorecards and stop conditions.

## Recovery point

Resume from STATE 0035. T005 A02 is integrated under D-0017. T006/T007 are READY from the same canonical base; T008 waits on their accepted integration.
