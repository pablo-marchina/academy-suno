# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0025`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 5 — Build, Implementation & Adoption`

`LAST_COMMITTED_WAVE: W004-RECIPIENT-APP-AND-REPORT-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 está ACTIVE;
- W004-T001/T002/T003 permanecem INTEGRATED: evidence cockpit, corpus W004 com 6 source documents/36 development outputs cegáveis e parser/source-trust role-aware estão disponíveis;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: provider-neutral harness existe, mas nenhuma chamada real credenciada foi executada; latency/usage/cost/content-quality reais seguem `PRODUCTION_UNKNOWN`;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- W004-T009/T010/T011/T012 permanecem INTEGRATED: operador humano cego, caminho manual provider secret-safe, README/demo/evidence packet e clean task-specific release smoke estão disponíveis;
- W004-T013 está INTEGRATED com `BLIND_REVIEW: NOT_PASS`; F-001/F-008 vídeo real/duração continuam abertos e F-005/F-006 human/provider continuam external-blocked;
- W004-T014 está INTEGRATED: app HTTP local recipient-facing aceita texto, PDF path e PDF upload, calcula SHA-256 dos bytes brutos, expõe provenance/parser/confidence/source-trust, bloqueia baixa confiança/table-role ambiguity e conecta SOURCE_READY ao planner canônico 3×3; 7 focused tests + System Integrity + Foundation Regression passaram no worker head;
- W004-T015 está INTEGRATED: `docs/report/EXPERIMENTAL_REPORT.md` e `docs/submission/SUBMISSION_PACKET.md` consolidam arquitetura/evidência/reprodutibilidade e preservam confusion matrices e provider metrics como BLOCKED/PENDING/PRODUCTION_UNKNOWN em vez de fabricar valores;
- F-002/F-003/F-007 estão corrigidos no nível de implementação/artefato, mas só a demo final integrada pode provar recipient-facing adherence ao avaliador;
- W004-T016 está READY após bind pós-merge para produzir ou preparar deterministicamente o vídeo final real, medir duração <=5:00 e demonstrar app + PDF/text ingest + 3×3/evidence/repair path;
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

### BLOCKED external evidence
- `W004-T004-A01` — real provider execution unavailable — Issue #84.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.

### READY after post-merge bind
- `W004-T016-A01` — actual <=5:00 demo artifact / deterministic capture package — Issue #109.

### PLANNED
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires valid human evidence + observed provider runs.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007; internal hardening/video cannot replace these evidence gates.

## Current success bottleneck

`FINAL_REAL_VIDEO_AND_EXTERNAL_HUMAN_PROVIDER_EVIDENCE`

Os gaps internos de app recipient-facing e relatório consolidado foram implementados. O próximo hard gate interno é um vídeo real e medido <=5:00 sobre a versão integrada, mostrando ingestão PDF/texto, 3×3/evidence view e FAIL→repair→PASS sem laundering de unknowns. Em paralelo, human gold independente e provider execution real continuam blockers externos irredutíveis.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- production/release readiness somente após human/provider prerequisites + W004-T008 + final blind review + concrete video artifact;
- LangGraph continua opcional/non-blocking enquanto plain async é evidence leader.

## Next action

1. mergear STATE 0025 e bindar SHA pós-merge na Issue #109;
2. executar W004-T016;
3. se capture automática não for possível, aceitar somente `TASK_BLOCKED_MANUAL_CAPTURE_REQUIRED` + deterministic capture package, nunca vídeo fictício;
4. manter #84/#85 abertos como blockers externos;
5. quando dois humanos concluírem exports válidos via T009, iniciar novo attempt de T005;
6. quando credential autorizado existir, executar T010 manual workflow e reavaliar T004/T007.

## Recovery point

Retomar de `STATE_VERSION 0025` e `SYSTEM/CHECKPOINTS/STATE-v0025.md`. T014/T015 estão integradas; T016 é o próximo worker interno seguro; T004/T005 continuam external-blocked.
