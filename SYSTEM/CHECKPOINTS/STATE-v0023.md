# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0023`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 5 — Build, Implementation & Adoption`

`LAST_COMMITTED_WAVE: W004-MITIGATION-AND-RELEASE-HARDENING-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 está ACTIVE;
- W004-T001/T002/T003 permanecem INTEGRATED: evidence cockpit, corpus W004 com 6 source documents/36 development outputs cegáveis e parser/source-trust role-aware estão disponíveis;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: provider-neutral harness existe, mas nenhuma chamada real credenciada foi executada; latency/usage/cost/content-quality reais seguem `PRODUCTION_UNKNOWN`;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- W004-T009 está INTEGRATED: operador local fail-closed para PRIMARY_A/PRIMARY_B, fixed blind bank, held-out inacessível, export/import completo e provenance; ele reduz fricção mas não prova independência física nem satisfaz T005;
- W004-T010 está INTEGRATED: caminho manual-only de provider via workflow_dispatch, secret-safe, versioned export/import e strict comparability validation; ausência de credential continua blocker e esta task não contém provider run observado;
- W004-T011 está INTEGRATED: README clean-start, evidence packet skeleton, demo storyboard alvo 4:40, final-review checklist e release-smoke runner; os CI gates passaram no worker head, mas o novo release-smoke test ainda não foi executado explicitamente pelo workflow existente;
- audience thresholds continuam `DIAGNOSTIC_ONLY`; target→human/human→evaluator matrices continuam indisponíveis; semantic backend segue sem preferência;
- W004-T006 permanece bloqueada por T005; W004-T007 por human evidence + provider real; W004-T008 permanece final fan-in dependente desses gates;
- W004-T012 e W004-T013 foram materializadas para executar clean release-smoke CI e blind/adversarial review enquanto blockers externos persistem;
- deadline, submission, owner/decision maker e workflow interno Suno permanecem UNKNOWN.

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

### BLOCKED external evidence
- `W004-T004-A01` — real provider execution unavailable — Issue #84.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.

### READY after post-merge bind
- `W004-T012-A01` — clean release-smoke CI / task-specific release gate — Issue #102.
- `W004-T013-A01` — blind/adversarial review of current package — Issue #103.

### PLANNED fan-ins
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires valid human evidence + observed provider runs.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007; T011/T012/T013 harden but do not replace these gates.

## Current success bottleneck

`EXTERNAL_HUMAN_PROVIDER_EVIDENCE_WITH_INTERNAL_RELEASE_PROOF_IN_PARALLEL`

Os blockers de validade são agora explicitamente externos e operacionalizados: dois humanos independentes podem usar T009, e provider evidence pode ser executada manualmente via T010 quando um secret autorizado existir. Internamente, o maior ganho restante sem depender desses recursos é executar o release smoke em clean CI e red-team/blind-review do pacote atual.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida; T010 não é provider evidence por si;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- production/release readiness somente após W004-T008 + final reviews;
- LangGraph continua opcional/non-blocking enquanto plain async é evidence leader.

## Next action

1. mergear STATE 0023 e bindar SHA pós-merge nas Issues #102/#103;
2. executar W004-T012/T013 em paralelo;
3. manter #84/#85 abertos como blockers externos;
4. quando dois humans concluírem exports válidos via T009, iniciar novo attempt de T005;
5. quando credential autorizado existir, executar T010 manual workflow e reavaliar T004/T007.

## Recovery point

Retomar de `STATE_VERSION 0023` e `SYSTEM/CHECKPOINTS/STATE-v0023.md`. T009/T010/T011 estão integradas; T012/T013 são os próximos workers internos seguros; T004/T005 continuam external-blocked.
