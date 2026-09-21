# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0027`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 6 — Adversarial Optimization`

`LAST_COMMITTED_WAVE: W004-REAL-CI-VIDEO-EVIDENCE-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 está ACTIVE;
- W004-T001/T002/T003 permanecem INTEGRATED: evidence cockpit, corpus W004 com 6 source documents/36 development outputs cegáveis e parser/source-trust role-aware estão disponíveis;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: provider-neutral harness existe, mas nenhuma chamada real credenciada foi executada; latency/usage/cost/content-quality reais seguem `PRODUCTION_UNKNOWN`;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- W004-T009/T010/T011/T012 permanecem INTEGRATED: operador humano cego, caminho manual provider secret-safe, README/demo/evidence packet e clean task-specific release smoke estão disponíveis;
- W004-T013 permanece INTEGRATED com `BLIND_REVIEW: NOT_PASS`; o primeiro review não é automaticamente supersedido por evidência técnica posterior;
- W004-T014/T015 permanecem INTEGRATED: app recipient-facing real para texto/PDF e relatório/submission packet consolidado existem;
- W004-T016 A01 permanece BLOCKED como fallback manual, com deterministic capture package integrado; ele não produziu vídeo;
- W004-T017 está INTEGRATED: GitHub Actions run `35625349017` executou a app recipient-facing real em Playwright/Chromium no task SHA `f95bd26f178b21314aa5d4b3eb8b086643490aee`, baixou um PDF público real do Banco Central do Brasil sem fallback sintético, exerceu ingestão de texto e PDF, 3×3/evidence view e persisted `FAIL → repair → PASS`, gravou vídeo real de browser, converteu para MP4 e verificou hashes/duração;
- o MP4 T017 tem SHA-256 `f04852fb11183e4e6bc8690d80c5ef26d6993edc6aa7ec71660b9e3b670c3bc4`, duração observada por ffprobe `7.200s` e hard-cap técnico `<=300s` PASS;
- o PDF BCB usado no run tem SHA-256 `4ac6a958cbff7571aad3f0125042f4b71890a70ec36e9ad9009b537e6458ce68`; DOM/content assertions confirmaram visita aos elementos requeridos durante a gravação;
- Actions artifacts aceitos: primary capture `10652146281` (digest `sha256:55f825ce911938f548c3cb480aa06c66b4bbe2a40bf50ce842077431e5607ca9`) e provenance `10652031268`; ambos reportam expiração em `2026-12-20T16:24:02Z`;
- T017 prova o hard gate técnico de existência de gravação real e duração abaixo de 5 minutos no escopo da task, mas **não** prova por si só que 7,2s constituem uma demonstração final inteligível/convincente para o avaliador;
- W004-T018 está materializada para reexecutar blind/adversarial review sobre o pacote atual + vídeo concreto T017; `BLIND_REVIEW` permanece `NOT_PASS` até esse julgamento;
- audience thresholds continuam `DIAGNOSTIC_ONLY`; target→human/human→evaluator matrices continuam indisponíveis; semantic backend segue sem preferência;
- W004-T006 permanece bloqueada por T005; W004-T007 por human evidence + provider real; W004-T008 permanece final fan-in dependente desses gates;
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
- `W004-T002` — representative corpus + blind human-calibration preparation — Issue #82 / PR #94.
- `W004-T003` — parser/source generalization bakeoff — Issue #83 / PR #91.
- `W004-T009` — blind human annotation operator/handoff — Issue #95 / PR #100.
- `W004-T010` — manual credential-safe provider evidence path — Issue #96 / PR #101.
- `W004-T011` — README/demo/release hardening — Issue #97 / PR #99.
- `W004-T012` — clean release-smoke CI — Issue #102 / PR #105.
- `W004-T013` — first blind/adversarial review — Issue #103 / PR #106.
- `W004-T014` — recipient-facing PDF/text interactive app — Issue #107 / PR #112.
- `W004-T015` — consolidated experimental report/submission packet — Issue #108 / PR #111.
- `W004-T017` — real CI browser demo capture — Issue #115 / PR #117 / Actions run `35625349017`.

### BLOCKED external/fallback evidence
- `W004-T004-A01` — real provider execution unavailable — Issue #84.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.
- `W004-T016-A01` — worker-local screen recording unavailable; deterministic manual capture fallback retained — Issue #109 / PR #114.

### READY after post-merge bind
- `W004-T018-A01` — fresh blind/adversarial review of current package + concrete T017 video — Issue #118.

### PLANNED
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires valid human evidence + observed provider runs.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007; T017 video evidence does not replace these evidence gates.

## Current success bottleneck

`BLIND_VIDEO_USABILITY_REVIEW_PLUS_EXTERNAL_HUMAN_PROVIDER_EVIDENCE`

A barreira técnica de produzir uma gravação real em ambiente reproduzível foi superada por T017: app real, PDF público, browser real, DOM assertions, hashes, artifact provenance e duração observada. O próximo gate interno é verificar cegamente se o vídeo concreto de 7,2s é de fato suficiente como demonstração evaluator-facing e se F-001/F-008 podem ser encerrados sem confundir existência técnica com comunicação convincente. Em paralelo, human gold independente e provider execution real continuam blockers externos irredutíveis.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- T017 technical capture pode encerrar o requisito de existência/duração somente se T018 confirmar que o artifact concreto é evaluator-usable; duração `7.200s` não é automaticamente sinônimo de demo final suficiente;
- artifact T017 deve ser copiado para storage de submissão durável se o horizonte relevante puder ultrapassar `2026-12-20T16:24:02Z`, preservando SHA/digest/provenance;
- production/release readiness somente após human/provider prerequisites + W004-T008 + final blind review;
- LangGraph continua opcional/non-blocking enquanto plain async é evidence leader.

## Next action

1. mergear STATE 0027 e bindar SHA pós-merge na Issue #118;
2. executar W004-T018 sobre pacote + vídeo real T017;
3. se T018 aceitar F-001/F-008, atualizar review/traceability e seguir apenas com blockers externos/fan-ins dependentes;
4. se T018 considerar 7,2s insuficientes como demo evaluator-facing, produzir novo capture artifact usando a infraestrutura T016/T017 sem perder provenance;
5. manter #84/#85 abertos como blockers externos;
6. quando dois humanos concluírem exports válidos via T009, iniciar novo attempt de T005;
7. quando credential autorizado existir, executar T010 manual workflow e reavaliar T004/T007.

## Recovery point

Retomar de `STATE_VERSION 0027` e `SYSTEM/CHECKPOINTS/STATE-v0027.md`. T017 está integrado com evidence técnica concreta; T018 é o próximo worker interno seguro; T004/T005 continuam external-blocked.
