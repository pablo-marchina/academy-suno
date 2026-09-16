# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0017`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 2 — Discovery & Evidence`

`LAST_COMMITTED_WAVE: W003-INITIAL-FANOUT-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001 e W002 estão COMPLETE; W003 está ACTIVE;
- W003-T001…T005 estão integradas sobre a mesma base STATE 0016 / `bd29959b081d8f70a40b420ab715f66ac5e59154`;
- T001 criou `gold-v001` com split por source document, rubric/annotation workflow e leakage kill criteria; por `n=3` e ausência de agreement humano independente, thresholds permanecem `DIAGNOSTIC_ONLY` e não podem ser congelados;
- T002 implementou claim-level grounding, provenance resolver e unified HybridDecision; focused grounding core passou 8/8 e semantic sensor continua incapaz de compensar source/factual/policy hard fail;
- T003 implementou representação explícita de graph/state + SQLite RunStore: runtime proof completou 9/9 jobs, branch-local quality repair, transport retry separado, reopen/resume e 28 history snapshots persistentes;
- plain async continua líder provisório por runtime evidence; LangGraph segue `PENDING_RUNTIME_RECHECK` porque a dependência não estava disponível, sem conclusão negativa ou lock de framework;
- T004 implementou readability PT-BR versionada, ontologia financeira e ACV multidimensional com anti-gaming fixtures; 15 testes focados passaram e não existe scalar/threshold de audiência não validado;
- T005 fechou a limitação de W002-T010: `Foundation Regression` e `System Integrity` passaram em clean checkout no GitHub Actions;
- W003-T006 (targeted repair) e W003-T007 (telemetry) estão logicamente READY após integração das dependências e devem receber SHA exato da main pós-merge;
- W003-T008 continua bloqueada até T007 integrar; W003-T009 continua bloqueada até T005,T006,T007,T008 integrarem;
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

Nenhum blocker impede W003-T006/T007. Gold humano/agreement, provider/model, parser library final, semantic backend e partner internal unknowns permanecem gaps experimentais/de produção, não blockers do próximo fan-in.

## Active wave

`W003` — Calibration, Grounding & End-to-End Evidence.

### INTEGRATED
- `W003-T001` — golden/dev/held-out benchmark + annotation workflow — Issue #59 / PR #73.
- `W003-T002` — claim-level grounding + unified HybridDecision — Issue #60 / PR #70.
- `W003-T003` — explicit graph/state orchestration + persistent RunStore — Issue #61 / PR #72.
- `W003-T004` — terminology + PT-BR readability + ACV/anti-gaming — Issue #62 / PR #71.
- `W003-T005` — clean-checkout foundation regression + application CI — Issue #63 / PR #69.

### READY after post-merge bind
- `W003-T006` — targeted repair + re-evaluation — Issue #64.
- `W003-T007` — telemetry/cost-latency — Issue #65.

### PLANNED fan-ins
- `W003-T008` — calibration/ablation/anti-gaming release gate — Issue #66; depends T001,T002,T004,T007.
- `W003-T009` — W003 end-to-end proof/synthesis — Issue #67; depends T005,T006,T007,T008.

## Current success bottleneck

`TARGETED_REPAIR_TELEMETRY_AND_CALIBRATION_FANIN`

A foundation combinada e o graph/state proof já são executáveis. O maior ganho agora é ligar findings a repairs locais mensuráveis, instrumentar run/job/attempt sem inventar custo e então calibrar/ablar sobre development gold preservando held-out e hard-gate precedence.

## Pending decisions

- final orchestration framework: plain async lidera; LangGraph requer unchanged challenger runtime recheck;
- parser library/fallback final: behavioral contract provado, implementation lock pendente expanded corpus/raw bytes;
- provider/model somente após measured quality/cost/latency;
- semantic backend somente após ablation incremental e sem hard-gate override;
- audience thresholds/floors somente após development gold + agreement suficiente; estado atual é diagnóstico, não lock;
- B13 evidence cockpit e B14 release proof permanecem para wave posterior salvo T009 replanejar por evidência.

## Next action

1. mergear STATE 0017 / W003 initial fan-out integration;
2. bindar SHA exato pós-merge nas Issues #64 e #65 e marcar READY executável;
3. revalidar lease para STATE 0017/current main;
4. iniciar W003-T006-A01 e W003-T007-A01 em paralelo;
5. após T007 integrar, liberar T008; depois T009 conforme DAG.

## Recovery point

Retomar de `STATE_VERSION 0017` e `SYSTEM/CHECKPOINTS/STATE-v0017.md`. W003-T001…T005 são evidência integrada; T006/T007 são o próximo fan-out seguro.
