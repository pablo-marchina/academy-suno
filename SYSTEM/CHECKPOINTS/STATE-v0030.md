# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0030`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 7 — Blind Review, Final Deliverable & Defense`

`LAST_COMMITTED_WAVE: W004-FINAL-VIDEO-PACKAGE-REVIEW-PASS`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE;
- W004-T001/T002/T003/T009/T010/T011/T012/T013/T014/T015/T017/T018/T019/T020 estão INTEGRATED;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: não existe run credenciado real de provider com quality/latency/usage/cost observados;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- T019 produziu a demo final real da app recipient-facing: Actions run `35636285651`, MP4 SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, duração observada `69.12s <= 300s`, H.264 1280×720 a 25 fps, success path `SOURCE_READY/PASS` primeiro, 9/9 mechanics, persisted `FAIL → repair → PASS`, evidence boundaries e BCB fail-closed safety negative-control sem bypass;
- T020 baixou e verificou diretamente os artifacts aceitos, mediu novamente o MP4 em `69.120000s`, inspecionou frames independentes e concluiu `VIDEO_PACKAGE_REVIEW: PASS` com `NEW_CRITICAL_FINDINGS: 0` e `NEW_HIGH_FINDINGS: 0`;
- F-001/F-002/F-003/F-007/F-008 passam no escopo de video/package review para o artifact exato T019; isso não equivale a project/release/production readiness;
- root README e `docs/submission/SUBMISSION_PACKET.md` estão atuais em relação ao artifact T019 aceito;
- o BCB real permanece corretamente `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` quando table-role provenance é ambígua; isso é safety behavior, não falha a ser ocultada;
- o principal residual interno do vídeo é retenção: os Actions artifacts `10656720873` e `10656775849` expiram em `2026-12-20T18:06:45Z`; T021 foi materializada para preservar byte-a-byte o MP4 aceito em storage durável sem regenerá-lo;
- audience thresholds continuam `DIAGNOSTIC_ONLY`; target→human/human→evaluator matrices seguem indisponíveis; semantic backend e provider/model permanecem sem preferência baseada em evidência;
- W004-T006 permanece dependente de T005; W004-T007 depende de T004/T005; W004-T008 continua fan-in final dependente de human/provider evidence válida;
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

## W004 lifecycle

### INTEGRATED
- `W004-T001` — evidence cockpit — Issue #81 / PR #93.
- `W004-T002` — corpus + blind human-calibration preparation — Issue #82 / PR #94.
- `W004-T003` — parser/source generalization bakeoff — Issue #83 / PR #91.
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

### BLOCKED external/fallback evidence
- `W004-T004-A01` — real provider execution unavailable — Issue #84.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.
- `W004-T016-A01` — worker-local screen recording unavailable; deterministic manual fallback retained — Issue #109 / PR #114.

### READY after post-merge bind
- `W004-T021-A01` — preserve exact accepted T019 MP4/package in durable submission-controlled storage — Issue #127.

### PLANNED
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires valid human evidence + observed provider runs.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007.

## Current success bottleneck

`EXTERNAL_HUMAN_PROVIDER_EVIDENCE_PLUS_DURABLE_VIDEO_STORAGE`

O principal gap interno de apresentação foi fechado em escopo: T020 aprovou independentemente o pacote/vídeo T019 e não encontrou findings CRITICAL/HIGH novos. T021 pode eliminar o residual de retenção do binary. Depois disso, os blockers materiais restantes são externos: duas anotações humanas independentes e execução real/credenciada de provider, que desbloqueiam T005→T006/T007→T008.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- `VIDEO_PACKAGE_REVIEW: PASS` não autoriza project/release/production PASS;
- artifact final deve permanecer byte-identical ao MP4 aceito T019 ao ser preservado em storage durável;
- o PDF BCB deve permanecer fail-closed enquanto faltar cell-role provenance; no demo-only bypass;
- production/release readiness somente após human/provider prerequisites + W004-T008 + final applicable reviews.

## Next action

1. mergear STATE 0030 e bindar W004-T021 à `main` exata;
2. executar T021 para preservar o MP4 aceito em storage durável e verificar SHA-256 byte-a-byte;
3. manter #84/#85 como blockers externos;
4. quando dois humanos concluírem exports válidos via T009, iniciar novo attempt de T005;
5. quando credential autorizado existir, executar T010 e reavaliar T004/T007;
6. liberar T006/T007/T008 somente quando seus prerequisites reais forem satisfeitos.

## Recovery point

Retomar de `STATE_VERSION 0030` e `SYSTEM/CHECKPOINTS/STATE-v0030.md`. T020 está integrado com video/package review PASS; T021 é o próximo worker interno seguro; T004/T005 continuam external-blocked.
