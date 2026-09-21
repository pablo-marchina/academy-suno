# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0024`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 5 — Build, Implementation & Adoption`

`LAST_COMMITTED_WAVE: W004-CLEAN-RELEASE-AND-BLIND-REVIEW-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 está ACTIVE;
- W004-T001/T002/T003 permanecem INTEGRATED: evidence cockpit, corpus W004 com 6 source documents/36 development outputs cegáveis e parser/source-trust role-aware estão disponíveis;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: provider-neutral harness existe, mas nenhuma chamada real credenciada foi executada; latency/usage/cost/content-quality reais seguem `PRODUCTION_UNKNOWN`;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- W004-T009/T010/T011 permanecem INTEGRATED: operator humano cego, caminho manual provider secret-safe e README/demo/evidence packet/release-smoke runner estão disponíveis;
- W004-T012 está INTEGRATED: clean task-specific GitHub Actions executou o release smoke e o focused test; 9/9 mechanics, persisted FAIL→repair→PASS, fresh hard gates, sibling immutability, cockpit markers e parser gates foram observados; external human/provider/semantic gaps permaneceram BLOCKED/PENDING;
- W004-T013 está INTEGRATED com `BLIND_REVIEW: NOT_PASS`; o review separou blockers externos de gaps internos e identificou: F-001 vídeo final real ausente (CRITICAL), F-002 raw PDF/text ingest não demonstrado recipient-facing (HIGH), F-003 interface atual read-only e potencialmente insuficiente como app interativa (HIGH), F-007 relatório experimental consolidado ausente (HIGH), além de F-005/F-006 externos e F-008 duração real ainda não medida;
- W004-T014 e W004-T015 estão materializadas para corrigir ingest/UI recipient-facing e relatório/submission packet em paralelo;
- W004-T016 permanece PLANNED após T014/T015 para produzir o vídeo final real e medir duração <=5:00;
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

### BLOCKED external evidence
- `W004-T004-A01` — real provider execution unavailable — Issue #84.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.

### READY after post-merge bind
- `W004-T014-A01` — recipient-facing interactive app + real PDF/text ingestion — Issue #107.
- `W004-T015-A01` — consolidated experimental report + submission packet — Issue #108.

### PLANNED
- `W004-T016-A01` — actual <=5:00 demo artifact after T014/T015 — Issue #109.
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires valid human evidence + observed provider runs.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007; internal hardening/re-review cannot replace these evidence gates.

## Current success bottleneck

`RECIPIENT_FACING_ADHERENCE_AND_FINAL_VIDEO_WITH_EXTERNAL_HUMAN_PROVIDER_GATES`

O release smoke interno agora tem evidence observada, mas o blind review encontrou gaps submission-facing reais. O maior ganho interno é fechar raw ingest + interface interativa + relatório e então produzir o vídeo final real <=5:00. Em paralelo, human gold e provider execution permanecem blockers externos irredutíveis e não podem ser simulados.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- app recipient-facing deve demonstrar real PDF/text input sem transformar extraction ambiguity em PASS;
- production/release readiness somente após human/provider prerequisites + W004-T008 + final blind review + concrete video artifact;
- LangGraph continua opcional/non-blocking enquanto plain async é evidence leader.

## Next action

1. mergear STATE 0024 e bindar SHA pós-merge nas Issues #107/#108;
2. executar W004-T014/T015 em paralelo;
3. manter #84/#85 abertos como blockers externos;
4. após T014/T015 integradas, liberar T016 para vídeo final real/medido;
5. quando dois humans concluírem exports válidos via T009, iniciar novo attempt de T005;
6. quando credential autorizado existir, executar T010 manual workflow e reavaliar T004/T007.

## Recovery point

Retomar de `STATE_VERSION 0024` e `SYSTEM/CHECKPOINTS/STATE-v0024.md`. T012/T013 estão integradas; T014/T015 são os próximos workers internos seguros; T016 depende deles; T004/T005 continuam external-blocked.
