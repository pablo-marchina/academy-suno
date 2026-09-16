# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0018`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 2 — Discovery & Evidence`

`LAST_COMMITTED_WAVE: W003-REPAIR-TELEMETRY-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001 e W002 estão COMPLETE; W003 está ACTIVE;
- W003-T001…T007 estão integradas;
- T001 criou `gold-v001` com split por source document, rubric/annotation workflow e leakage kill criteria; por `n=3` e ausência de agreement humano independente, thresholds permanecem `DIAGNOSTIC_ONLY` e não podem ser congelados;
- T002 implementou claim-level grounding, provenance resolver e unified HybridDecision; focused grounding core passou 8/8 e semantic sensor continua incapaz de compensar source/factual/policy hard fail;
- T003 implementou graph/state explícito + SQLite RunStore; runtime proof completou 9/9 jobs, branch-local quality repair, transport retry separado, reopen/resume e 28 history snapshots persistentes;
- T004 implementou readability PT-BR versionada, ontologia financeira e ACV multidimensional com anti-gaming fixtures; 15 testes focados passaram e não existe scalar/threshold de audiência não validado;
- T005 provou `Foundation Regression` + `System Integrity` em clean checkout no GitHub Actions;
- T006 implementou targeted repair orientado por failure codes/metrics: 7/7 focused tests PASS; o controlled proof fechou FAIL→diagnostic feedback→repair→fresh re-evaluation→PASS em 1 tentativa, com accepted siblings imutáveis, bounded stop criteria e fresh SOURCE/DETERMINISTIC_FACTUAL/POLICY run IDs;
- T007 implementou telemetry provider-neutral versionada: 6 focused tests PASS; stage latency, transport retry, quality repair, usage e custo observável têm lineage; usage/cost ausentes permanecem N/A e qualquer custo exige pricing versionado; demo pricing é sintético, não claim comercial;
- os branches T006/T007 também passaram `System Integrity` e `Foundation Regression` antes da integração;
- W003-T008 está logicamente READY para calibration/ablation/anti-gaming release gate; deve receber SHA exato da main pós-merge;
- W003-T009 continua bloqueada até T008 integrar; T005/T006/T007 já satisfazem as demais dependências;
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

Nenhum blocker impede W003-T008. Independent human agreement, provider/model, parser library final, semantic backend e partner internal unknowns permanecem gaps experimentais/de produção. Thresholds podem permanecer diagnósticos se evidence/agreement forem insuficientes; T008 não pode forçar um lock.

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

### READY after post-merge bind
- `W003-T008` — calibration/ablation/anti-gaming release gate — Issue #66.

### PLANNED fan-in
- `W003-T009` — W003 end-to-end proof/synthesis — Issue #67; depends T005,T006,T007,T008.

## Current success bottleneck

`CALIBRATION_ABLATION_AND_RELEASE_GATE`

Repair e telemetry deixaram de ser o principal risco. O maior ganho agora é testar o evaluator/audience stack contra development gold sem contaminar held-out, medir confusion matrices e ablations, executar anti-gaming gates e decidir por evidência quais sinais podem ser promovidos além de diagnóstico. Hard source/factual/policy precedence continua não compensatória.

## Pending decisions

- final orchestration framework: plain async lidera; LangGraph requer unchanged challenger runtime recheck;
- parser library/fallback final: behavioral contract provado, implementation lock pendente expanded corpus/raw bytes;
- provider/model somente após measured quality/cost/latency;
- semantic backend somente após ablation incremental e sem hard-gate override;
- audience thresholds/floors somente se development evidence + agreement suportarem; estado atual permanece diagnóstico;
- telemetry backend/pricing/provider usage normalization finais permanecem deployment/provider decisions;
- B13 evidence cockpit e B14 release proof permanecem para wave posterior salvo T009 replanejar por evidência.

## Next action

1. mergear STATE 0018 / repair+telemetry integration;
2. bindar SHA exato pós-merge na Issue #66 e marcar W003-T008 READY executável;
3. fechar Issues #64/#65 e revalidar lease para STATE 0018/current main;
4. iniciar W003-T008-A01;
5. após T008 integrar, liberar W003-T009 para o end-to-end proof/synthesis da wave.

## Recovery point

Retomar de `STATE_VERSION 0018` e `SYSTEM/CHECKPOINTS/STATE-v0018.md`. W003-T001…T007 são evidência integrada; T008 é o próximo task seguro.
