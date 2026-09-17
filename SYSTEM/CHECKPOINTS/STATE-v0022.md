# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0022`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 5 — Build, Implementation & Adoption`

`LAST_COMMITTED_WAVE: W004-BLOCKER-PIVOT`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 está ACTIVE;
- W004-T001/T002/T003 permanecem INTEGRATED: evidence cockpit, corpus W004 com 6 source documents/36 development outputs cegáveis e parser/source-trust role-aware estão disponíveis na `main`;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: o provider-neutral harness está integrado, mas nenhuma chamada real credenciada foi executada; provider latency/usage/cost/content-quality seguem `PRODUCTION_UNKNOWN`;
- W004-T005 A01 executou continuity PASS e terminou `TASK_BLOCKED` porque duas streams primárias de anotação humana genuinamente independentes para os 36 blind development items não estavam disponíveis; nenhum pseudo-human/model gold foi fabricado;
- audience thresholds continuam `DIAGNOSTIC_ONLY`, target→human e human→evaluator observed matrices continuam indisponíveis até existir human gold independente válido;
- W004-T006 permanece bloqueada por T005; W004-T007 permanece bloqueada por human evidence + provider real; W004-T008 permanece downstream desses gates;
- para não paralisar o projeto em dependências externas, W004 adiciona três tarefas paralelas seguras: T009 blind annotation operator/handoff, T010 manual credential-safe provider execution/import path e T011 README/demo/release hardening com unknowns explícitos;
- nenhuma dessas tarefas substitui os gates humanos/provider: elas reduzem fricção, melhoram reprodutibilidade e avançam deliverables enquanto os blockers externos permanecem verdadeiros;
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

### BLOCKED external evidence
- `W004-T004-A01` — real provider execution unavailable; harness integrated — Issue #84.
- `W004-T005-A01` — independent human primary annotations unavailable — Issue #85.

### READY after post-merge bind
- `W004-T009-A01` — blind annotation operator + human handoff — Issue #95.
- `W004-T010-A01` — manual credential-safe provider execution/import path — Issue #96.
- `W004-T011-A01` — README/demo/release hardening + clean smoke — Issue #97.

### PLANNED fan-ins
- `W004-T006` — semantic backend ablation — depends valid T005 human gold.
- `W004-T007` — provider/model comparison — depends valid human evidence + observed provider runs.
- `W004-T008` — clean-E2E release proof — depends T001,T003,T005,T006,T007; T011 may pre-harden its packet but cannot replace these gates.

## Current success bottleneck

`EXTERNAL_HUMAN_AND_PROVIDER_EVIDENCE_WITH_RELEASE_HARDENING_IN_PARALLEL`

O maior gap de validade continua externo: duas anotações humanas cegas e independentes e pelo menos uma execução provider/model credenciada/observada. O maior ganho seguro interno é tornar esses dois handoffs mínimos e auditáveis e, em paralelo, completar documentação/demo/smoke sem transformar unknowns em PASS.

## Pending decisions

- audience thresholds: somente após human gold + agreement/adjudication suficiente; senão `DIAGNOSTIC_ONLY`;
- semantic backend: somente após ablation no mesmo development gold válido;
- provider/model: somente após runs observáveis comparáveis + quality evidence válida; ausência de secret não é evidence;
- parser implementation: continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- production/release readiness: somente após W004-T008 + final review; T011 é preparação, não release approval;
- LangGraph continua opcional/non-blocking enquanto plain async é evidence leader.

## Next action

1. mergear STATE 0022 e bindar SHA pós-merge nas Issues #95–#97;
2. executar W004-T009/T010/T011 em paralelo;
3. manter #84/#85 abertos como blockers externos e nunca reinterpretar harness/preparation como evidence observado;
4. quando duas human annotation streams válidas existirem, iniciar novo attempt de T005;
5. quando provider credential autorizado existir, iniciar nova execução via caminho preparado por T010 e depois reavaliar T007.

## Recovery point

Retomar de `STATE_VERSION 0022` e `SYSTEM/CHECKPOINTS/STATE-v0022.md`. T004/T005 estão blocked por evidence externo; T009/T010/T011 são os próximos workers seguros.