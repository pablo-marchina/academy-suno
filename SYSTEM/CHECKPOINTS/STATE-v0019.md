# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0019`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 2 — Discovery & Evidence`

`LAST_COMMITTED_WAVE: W003-CALIBRATION-GATE-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001 e W002 estão COMPLETE; W003 está ACTIVE;
- W003-T001…T008 estão integradas;
- `gold-v001` mantém split por source document, held-out protegido e annotation workflow, mas possui apenas 3 source documents e nenhum human gold label/agreement independente suficiente para threshold freeze;
- claim-level grounding, hard-gate precedence, explicit graph/state + SQLite RunStore, 3×3 planner, audience diagnostics, targeted repair e telemetry estão implementados e testados em seus escopos;
- T006 provou controlled FAIL→diagnostic feedback→local repair→fresh SOURCE/DETERMINISTIC_FACTUAL/POLICY re-evaluation→PASS com bounded stops e siblings imutáveis;
- T007 provou telemetry provider-neutral com run/job/attempt lineage, latency, transport retry ≠ quality repair e N/A-preserving usage/cost; demo pricing permanece sintético;
- T008 implementou calibration/ablation/anti-gaming release gate e passou 8/8 focused tests; held-out tuning exposure é proibida, target solicitado não pode virar gold, hard gates não podem ser compensados por semantic/soft signal e synthetic pricing não pode virar provider-cost evidence;
- T008 current disposition é intencionalmente `DIAGNOSTIC_ONLY`: anti-gaming `PASS`, audience calibration `NOT_COMPUTABLE`, semantic ablation `NOT_RUN`, provider comparison `NOT_COMPARABLE`, threshold freeze `false` e nenhum backend/provider/model preference;
- W003-T009 está logicamente READY para o end-to-end mechanics proof/synthesis; deve receber SHA exato da main pós-merge;
- plain async continua líder provisório por runtime evidence; LangGraph permanece `PENDING_RUNTIME_RECHECK`, sem conclusão negativa ou lock de framework;
- provider/model, parser library final, semantic backend e audience thresholds continuam evidence-driven e não estão lockados;
- deadline, submission, owner/decision maker e workflow interno Suno permanecem UNKNOWN e limitam production/ROI claims, mas não bloqueiam proof/demo técnico defensável.

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

## Open blockers

Nenhum blocker impede W003-T009. Independent human gold/agreement, measured semantic ablation, real provider quality/latency/cost, parser library final e partner internal unknowns permanecem gaps experimentais/de produção. T009 deve separar mechanics proof de model-quality proof e não pode converter ausência de evidência em escolha de provider/backend/threshold.

## Active wave

`W003` — Calibration, Grounding & End-to-End Evidence.

### INTEGRATED
- `W003-T001` — golden/dev/held-out benchmark + annotation workflow — Issue #59 / PR #73.
- `W003-T002` — claim-level grounding + unified HybridDecision — Issue #60 / PR #70.
- `W003-T003` — explicit graph/state orchestration + persistent RunStore — Issue #61 / PR #72.
- `W003-T004` — terminology + PT-BR readability + ACV/anti-gaming — Issue #62 / PR #71.
- `W003-T005` — clean-checkout foundation regression + application CI — Issue #63 / PR #69.
- `W003-T006` — targeted repair + re-evaluation — Issue #64 / PR #75.
- `W003-T007` — telemetry/cost-latency audit layer — Issue #65 / PR #76.
- `W003-T008` — calibration/ablation/anti-gaming release gate — Issue #66 / PR #78.

### READY after post-merge bind
- `W003-T009` — W003 end-to-end proof/synthesis — Issue #67.

## Current success bottleneck

`W003_END_TO_END_MECHANICS_AND_NEXT_WAVE_DECISION`

O calibration gate está construído e protege contra circularidade/gaming, mas evidencia corretamente que audience thresholds e semantic/provider selection não são calibráveis com o dataset atual. O maior ganho agora é executar uma prova auditável source→9 jobs→eval→targeted repair→aggregate com RunStore/telemetry e sintetizar quais gaps viram W004: evidence cockpit, independent human calibration, real provider experiment, parser bakeoff e release proof.

## Pending decisions

- final orchestration framework: plain async lidera; LangGraph requer unchanged challenger runtime recheck;
- parser library/fallback final: behavioral contract provado, implementation lock pendente expanded corpus/raw bytes;
- provider/model somente após measured quality/cost/latency;
- semantic backend somente após development-gold ablation incremental e sem hard-gate override;
- audience thresholds/floors somente após independent human gold + agreement suficiente; estado permanece `DIAGNOSTIC_ONLY`;
- telemetry backend/pricing/provider usage normalization finais permanecem deployment/provider decisions;
- B13 evidence cockpit e B14 release proof serão priorizados por T009 junto com os gaps experimentais restantes.

## Next action

1. mergear STATE 0019 / T008 integration;
2. bindar SHA exato pós-merge na Issue #67 e marcar W003-T009 READY executável;
3. fechar Issue #66 e revalidar lease para STATE 0019/current main;
4. iniciar W003-T009-A01;
5. após T009 integrar, fechar W003 e materializar W004 pelo maior bottleneck demonstrado.

## Recovery point

Retomar de `STATE_VERSION 0019` e `SYSTEM/CHECKPOINTS/STATE-v0019.md`. W003-T001…T008 são evidência integrada; T009 é o fan-in final seguro.
