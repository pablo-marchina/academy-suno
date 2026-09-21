# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.7.0`

`STATE_VERSION: 0034`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 7 — Blind Review, Final Deliverable & Defense`

`LAST_COMMITTED_WAVE: W004-AUTOMATED-CALIBRATION-WAIVER`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE;
- W004-T001/T002/T003/T004/T009/T010/T011/T012/T013/T014/T015/T017/T018/T019/T020/T021 estão INTEGRATED;
- W004-T004 A08 permanece aceito em mechanics scope: Groq Models + Responses HTTP `200`, `openai/gpt-oss-120b`, latência observada `349.694 ms`, usage `84/61/145`, custo derivado `4.92e-05 USD`, strict T007 import e fresh-clone PASS;
- PR #137 persistiu uma validação automatizada cega completa sobre os 36 itens DEVELOPMENT: Actions run `35668224695`, artifact `10669817144`, validator `MODEL_AUTOMATED`, Groq `openai/gpt-oss-120b`, 36/36 IDs únicos, blind leakage guardrails PASS, fresh-clone byte identity PASS, output SHA-256 `adae7376415cd7052b8b2b84002ce0a7a5890047cb86e98dbe456747c7fe1bb4`;
- distribuição A03: BEGINNER `6`, INTERMEDIATE `28`, ADVANCED `2`, UNSCORABLE `0`; factual preservation `33 PASS / 3 FAIL`; material concept preservation `33 PASS / 3 FAIL`; format-native `36 PASS`; custo derivado `0.0179265 USD` para `52235` tokens totais;
- A03 permanece explicitamente `human_gold_eligible=false` e não é PRIMARY_A/PRIMARY_B. Nenhum human agreement foi observado ou fabricado;
- `D-0017` introduz um `EVIDENCE_SUBSTITUTION_WAIVER` explícito e autorizado pelo operador: A03 passa a poder satisfazer a dependência de calibração de `W004-T005 → T006/T007 → T008` como `MODEL_AUTOMATED_BLIND_CALIBRATION`, sem virar human gold;
- a ausência de duas streams humanas deixa de ser hard blocker deste case e passa a risco residual controlado. Claims de human gold/agreement/preference/validation continuam proibidos; uma amostra humana futura é melhoria opcional, não dependência do critical path;
- W004-T005 A01 permanece histórico BLOCKED sob o protocolo anterior. O próximo attempt deve ser `A02`, reutilizando somente a evidência A03 aceita e produzindo pacote/matrizes de calibração automatizada com provenance explícita;
- após T005 A02 aceito, T006 e T007 podem rodar em paralelo. T006 usa o mesmo reference set A03 para semantic ablation diagnóstica; T007 combina source-grounded quality checks/A03 com mechanics/custo/latência observados e não pode declarar human preference;
- audience thresholds permanecem `DIAGNOSTIC_ONLY`; provider/model ou semantic-backend preference somente podem ser qualificadas pelo escopo da evidência realmente observada;
- T019/T020/T021 permanecem PASS no escopo de demo/package/durability: MP4 aceito SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, `69.12s`, H.264 1280×720 25fps, review independente sem novos CRITICAL/HIGH e cópia byte-identical persistida em `artifacts/submission/final-demo.mp4`;
- W004-T016 continua somente fallback não material; T017/T019/T020/T021 fecharam o caminho real de demo;
- deadline, submission mechanism, owner/decision maker e workflow interno Suno permanecem UNKNOWN.

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
- `D-0016` Foundation invariants lockados; implementation identities permanecem evidence-driven.
- `D-0017` W004 automated blind calibration evidence substitution waiver; A03 destrava o critical path sem claim de human gold.

## W004 lifecycle

### INTEGRATED
- `W004-T001` — evidence cockpit — Issue #81 / PR #93.
- `W004-T002` — corpus + blind human-calibration preparation — Issue #82 / PR #94.
- `W004-T003` — parser/source generalization bakeoff — Issue #83 / PR #91.
- `W004-T004` — accepted Groq provider mechanics — Issue #84 / accepted attempt A08 / PR #133 / Actions run `35664987180`.
- `W004-T009` — blind annotation operator — Issue #95 / PR #100.
- `W004-T010` — credential-safe provider evidence path — Issue #96 / PR #101.
- `W004-T011` — README/demo/release hardening — Issue #97 / PR #99.
- `W004-T012` — clean release-smoke CI — Issue #102 / PR #105.
- `W004-T013` — first blind/adversarial review — Issue #103 / PR #106.
- `W004-T014` — recipient-facing PDF/text app — Issue #107 / PR #112.
- `W004-T015` — consolidated experimental report/submission packet — Issue #108 / PR #111.
- `W004-T017` — real CI browser demo capture — Issue #115 / PR #117 / Actions run `35625349017`.
- `W004-T018` — direct blind review of T017 — Issue #118 / PR #120 — `NOT_PASS` for evaluator usability.
- `W004-T019` — paced final demo + evaluator-facing package refresh — Issue #121 / PR #124 / Actions run `35636285651`.
- `W004-T020` — independent final blind/adversarial review — Issue #122 / PR #126 — `VIDEO_PACKAGE_REVIEW: PASS`.
- `W004-T021` — durable byte-identical accepted-video preservation — Issue #127 / accepted attempt A02 / PR #130 / Actions run `35651949452`.

### HISTORICAL BLOCKED/FALLBACK
- `W004-T005-A01` — blocked under protocol 1.6.0 for missing two independent humans — Issue #85; superseded operationally by `D-0017`, not relabeled as complete.
- `W004-T016-A01` — worker-local screen recording unavailable; deterministic manual fallback retained — Issue #109 / PR #114.

### READY / PLANNED
- `W004-T005-A02` — READY: integrate accepted 36-item automated blind calibration A03 under `D-0017`, preserving non-human evidence class and producing calibration matrices/summary.
- `W004-T006` — PLANNED after T005 A02: semantic backend ablation on the accepted automated calibration reference set.
- `W004-T007` — PLANNED after T005 A02: provider/model comparison using source-grounded + automated calibration quality evidence and real provider mechanics/cost/latency.
- `W004-T008` — PLANNED fan-in after T005/T006/T007: final clean-E2E release proof and evidence package.

## Current success bottleneck

`AUTOMATED_CALIBRATION_INTEGRATION_AND_DOWNSTREAM_ABLATIONS`

O blocker humano externo foi removido por waiver explícito sem fabricar human gold. O critical path agora é interno e executável: transformar A03 em resultado T005 formal, executar T006/T007 com claims limitados à classe automatizada e então fechar T008 + reviews finais.

## Evidence waiver boundary

- Classe aceita: `MODEL_AUTOMATED_BLIND_CALIBRATION`.
- Artifact primário: `artifacts/evals/w004/model_validation_a03.jsonl` + provenance/summary.
- Human gold: **não observado**.
- Human agreement/preference: **claims proibidos**.
- Audience thresholds: `DIAGNOSTIC_ONLY`.
- Human sample: opcional, não bloqueante.
- Production validation baseada em humanos: não autorizada.
- Completion do case/deliverable pode prosseguir se scorecards tratarem a ausência humana como risco controlado e nenhum claim final ultrapassar a evidência.

## Pending decisions

- semantic backend somente após T006; qualquer preferência deve declarar que foi medida contra automated blind calibration, não human gold;
- provider/model preference somente após T007 e somente no escopo de datasets/configs comparáveis; human preference permanece UNKNOWN;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- o PDF BCB deve permanecer fail-closed enquanto faltar cell-role provenance; no demo-only bypass;
- production/release readiness somente após T005/T006/T007/T008 + final applicable reviews e scorecards reconciliados sob `D-0017`.

## Next action

1. executar `W004-T005-A02` a partir de STATE 0034, consumindo A03 como `MODEL_AUTOMATED_BLIND_CALIBRATION` e nunca como human gold;
2. integrar T005 A02 e liberar `W004-T006` + `W004-T007` em paralelo;
3. integrar T006/T007 e executar `W004-T008` clean-E2E final;
4. rodar reviews finais aplicáveis, atualizar Success + Partner + Quality + risks/traceability e verificar stop conditions;
5. manter qualquer human sample futura como enhancement opcional fora do critical path.

## Recovery point

Retomar de `STATE_VERSION 0034`. Protocolo `1.7.0` e `D-0017` autorizam a substituição explícita do gate humano por A03 no escopo W004-T005→T008, preservando `human_gold_eligible=false` e os claims proibidos. O próximo attempt legítimo é `W004-T005-A02`.
