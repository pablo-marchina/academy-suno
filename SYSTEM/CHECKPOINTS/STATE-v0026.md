# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0026`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 5 — Build, Implementation & Adoption`

`LAST_COMMITTED_WAVE: W004-FINAL-VIDEO-CAPTURE-PIVOT`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 está ACTIVE;
- W004-T001/T002/T003 permanecem INTEGRATED: evidence cockpit, corpus W004 com 6 source documents/36 development outputs cegáveis e parser/source-trust role-aware estão disponíveis;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: provider-neutral harness existe, mas nenhuma chamada real credenciada foi executada; latency/usage/cost/content-quality reais seguem `PRODUCTION_UNKNOWN`;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- W004-T009/T010/T011/T012 permanecem INTEGRATED: operador humano cego, caminho manual provider secret-safe, README/demo/evidence packet e clean task-specific release smoke estão disponíveis;
- W004-T013 permanece INTEGRATED com `BLIND_REVIEW: NOT_PASS`; F-001/F-008 vídeo real/duração continuam abertos e F-005/F-006 human/provider continuam external-blocked;
- W004-T014/T015 permanecem INTEGRATED: app recipient-facing real + relatório/submission packet consolidado existem;
- W004-T016 A01 terminou `TASK_BLOCKED_MANUAL_CAPTURE_REQUIRED`: nenhum vídeo foi fabricado; o pacote determinístico de captura foi aceito no código via PR #114 e inclui exact-SHA preflight, PDF público BCB, source/video hashing, ffprobe hard cap <=300s, timed runbook e focused tests; o hard gate de vídeo permanece aberto porque nenhum vídeo real foi produzido;
- W004-T017 está materializada como rota alternativa para tentar produzir uma gravação real automaticamente em GitHub-hosted CI com browser real, PDF público, duração medida, hashes e artifact provenance;
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
- `W004-T013` — blind/adversarial review — Issue #103 / PR #106.
- `W004-T014` — recipient-facing PDF/text interactive app — Issue #107 / PR #112.
- `W004-T015` — consolidated experimental report/submission packet — Issue #108 / PR #111.

### BLOCKED evidence/capture
- `W004-T004-A01` — real provider execution unavailable — Issue #84.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.
- `W004-T016-A01` — real screen recording unavailable in worker runtime; deterministic capture package integrated — Issue #109 / PR #114.

### READY after post-merge bind
- `W004-T017-A01` — real automated browser/CI capture attempt — Issue #115.

### PLANNED
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires valid human evidence + observed provider runs.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007; video/internal hardening cannot replace these evidence gates.

## Current success bottleneck

`REAL_VIDEO_CAPTURE_PLUS_EXTERNAL_HUMAN_PROVIDER_EVIDENCE`

O pacote manual de captura reduz risco de execução, mas não satisfaz o requisito eliminatório de vídeo. Antes de exigir intervenção manual, T017 tentará uma captura real automatizada em GitHub Actions: app rodando, browser interagindo, PDF financeiro público, artifact de vídeo persistido, duração/hash/proveniência medidos e evidence labels preservados. Em paralelo, human gold independente e provider execution real continuam blockers externos irredutíveis.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- um artifact de browser recording real em CI pode satisfazer o hard gate técnico de vídeo somente se o próprio run provar app real, interações requeridas, duração <=300s, hashes/proveniência e artifact discoverable; screenshots/storyboard não bastam;
- production/release readiness somente após human/provider prerequisites + W004-T008 + final blind review + concrete video artifact;
- LangGraph continua opcional/non-blocking enquanto plain async é evidence leader.

## Next action

1. mergear STATE 0026 e bindar SHA pós-merge na Issue #115;
2. executar W004-T017 como rota CI-first para vídeo real;
3. se T017 produzir artifact válido, integrar e reexecutar blind review sobre pacote + vídeo;
4. se T017 bloquear tecnicamente, o caminho restante para F-001/F-008 é executar o pacote manual T016 em workstation normal;
5. manter #84/#85 abertos como blockers externos;
6. quando dois humanos concluírem exports válidos via T009, iniciar novo attempt de T005;
7. quando credential autorizado existir, executar T010 manual workflow e reavaliar T004/T007.

## Recovery point

Retomar de `STATE_VERSION 0026` e `SYSTEM/CHECKPOINTS/STATE-v0026.md`. T016 está blocked com capture package integrado; T017 é o próximo worker interno seguro; T004/T005 continuam external-blocked.
