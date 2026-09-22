# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.8.0`

`STATE_VERSION: 0043`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 8 — Production Scope & Decision Research Foundation`

`LAST_COMMITTED_WAVE: W005-RESEARCH-MICRO-FANIN-1`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução — elevando o alvo para produto real multiusuário, production-grade no escopo comprovado, quantitative/eval-driven, adaptive onde seguro e integralmente observável.

## Scope foundation

D-0018 permanece `LOCKED`. W004 é baseline/evidência histórica válida, não o target final de engenharia. `SYSTEM/PRODUCTION_CONTRACT.md` e `SYSTEM/DECISION_RESEARCH_GATE.md` são obrigatórios. “Sem demo” continua significando sem sistema fake/descartável exclusivo para demonstração; o vídeo obrigatório <=5:00 deve mostrar o mesmo produto real.

## Preserved W004 truth

- W001, W002, W003 e W004 estão COMPLETE no escopo interno executável original.
- W004-T005 A02 permanece `MODEL_AUTOMATED_BLIND_CALIBRATION`; human gold/agreement/preference continuam **not observed** e thresholds de audiência continuam `DIAGNOSTIC_ONLY`.
- W004-T006 permanece `NO_BACKEND_PREFERENCE` após delta semântico observado `+0.000000`.
- W004-T007-A05 permanece comparação Groq bounded e `NO_OVERALL_MODEL_PREFERENCE`.
- W004-T008-A02 permanece clean-E2E source→9→eval→repair→aggregate `9/9` PASS com provenance válida.
- W004-T019/T020/T021 permanecem evidência válida do vídeo W004 real `69.120s <= 300s`, independente/revisado/durável.
- nenhuma dessas evidências, isoladamente, autoriza `PRODUCTION_READY`.

## W005 lifecycle reconstruction — micro-fan-in 1

O Orchestrator reconstruiu o lifecycle das Issues/branches/results e integrou três attempts válidos após seus gates aplicáveis:

### INTEGRATED

- `W005-T001-A01` — production requirements / measurable acceptance — Issue #151, PR #170.
  - `PROD-001..017` decompostos em evidência de aceitação observável;
  - hard invariants já contratuais preservados, incluindo zero cross-tenant unauthorized access nos testes definidos, exact `9/9`, zero branch loss/duplication, zero critical-schema false PASS e 100% PASS nos cenários de restart/resume e backup/restore definidos antes de claim;
  - SLO/capacity/latency/cost/audience/retention/partner-workflow thresholds não fornecidos permanecem evidence-gated, sem números inventados;
  - nenhuma stack foi selecionada.

- `W005-T002-A01` — frontend/API/live Evidence Cockpit architecture research — Issue #152, PR #171.
  - `LOCK` para propriedades arquiteturais suportadas pela evidência: boundary HTTP tipado/versionado descrito por OpenAPI; SSE como feed default de run/job/eval/repair/telemetry com cursor durável + replay/de-dup + snapshot fallback; autorização/redação server-side antes de serialização; stable opaque source/citation refs;
  - React+Vite vs Next.js e Tiptap/ProseMirror vs Lexical permanecem `PENDING_EVIDENCE` até T013/spikes equivalentes;
  - polling é fallback; WebSocket fica condicionado a necessidade real de colaboração bidirecional;
  - System Integrity e Foundation Regression passaram antes da integração.

- `W005-T003-A01` — orchestration/durability/concurrency runtime bakeoff — Issue #153, PR #169.
  - baseline atual preservou exact 9/9, retry-vs-repair isolation, checkpoint/resume e process restart no harness controlado;
  - 15 execuções sintéticas de overhead de orchestration/storage: p50 `46.236 ms`, p95 `64.228 ms`, max `89.156 ms`; não é end-user/provider latency;
  - foi reproduzido `lost_update_observed=true` em duas conexões stale escrevendo o mesmo run, evidenciando ausência de CAS/version ownership/per-run lease no `SQLiteRunStore` atual;
  - decisão de runtime permanece `PENDING_EVIDENCE`: SQLiteRunStore não é production multi-replica authority; LangGraph/DBOS/Temporal também não são winners por documentação; challenger deve passar common workload harness em shared production-capable state.

Nenhum dos três resultados autoriza `PRODUCTION_READY` nem bulk Phase 9 implementation.

## W005 current runtime status

### INTEGRATED — 3/11 required research inputs
- `W005-T001` — Issue #151 / PR #170.
- `W005-T002` — Issue #152 / PR #171.
- `W005-T003` — Issue #153 / PR #169.

### RUNNING — 8/11 required research inputs
- `W005-T004` — Multi-tenant identity/data/storage/security architecture research — Issue #154.
- `W005-T005` — Eval science, human calibration & quantitative EDD research — Issue #155.
- `W005-T006` — Adaptive AI runtime/provider/model/routing research — Issue #156.
- `W005-T007` — Observability, telemetry & safe live evidence research — Issue #157.
- `W005-T008` — Deployment, reliability, capacity & recovery research — Issue #158.
- `W005-T009` — Cross-cutting benchmark harness & quantitative decision methodology — Issue #159.
- `W005-T013` — Developer platform, repository toolchain & CI/CD systematic research — Issue #164.
- `W005-T014` — Financial document parsing, extraction & source-grounding bakeoff — Issue #165.

Todos os oito emitiram `TASK_STARTED` válido após `CONTINUITY_CHECK: PASS`. Ausência de terminal significa `RUNNING`, não conclusão nem garantia de processo em background.

### PLANNED — gated fan-in
- `W005-T010` — production architecture synthesis; depende de T001..T009 + T013 + T014 — Issue #160.
- `W005-T011` — independent production architecture red-team; depende de T010 — Issue #161.
- `W005-T012` — final W005 fan-in + implementation wave plan; depende de T010/T011 — Issue #162.

T010 continua bloqueada enquanto qualquer um dos onze inputs obrigatórios não estiver `INTEGRATED`.

## Production truth after first fan-in

- `PROD-001..017` possuem agora acceptance decomposition explícita, mas a maioria ainda carece de implementação/evidência operacional.
- interface contract/live transport possui decisões parciais evidence-backed; frontend/editor framework continua desbloqueado.
- o `SQLiteRunStore` atual possui blocker reproduzido para same-run stale multi-replica writes e não pode ser promovido a source of truth de produção.
- orchestration framework winner continua `PENDING_EVIDENCE` até common-harness candidate execution.
- identity/tenancy/authz/shared persistence/secure uploads/deployment/security/reliability/live observability completos ainda não estão provados.
- parser/document-intelligence implementation permanece unlocked até T014/fan-in.
- developer platform/repository/package manager/build/test/CI-CD choices permanecem unlocked até T013/fan-in.
- human-calibrated production audience thresholds permanecem open; D-0017 não se estende a human/production claims.
- capacidade/SLO targets não são inventados.
- external deadline, submission mechanism, named Suno owner/workflow e ROI baseline permanecem `UNKNOWN`.

## Locked decisions

- `D-0001` GitHub canonical.
- `D-0002` Workers do not integrate.
- `D-0003` Versioned parallelism.
- `D-0004` Executable guardrails.
- `D-0005` Exclusive lease.
- `D-0006` Attempt provenance.
- `D-0007` Checkpoints/DAG.
- `D-0009` Loop until gates/stop.
- `D-0011` Partner Contract/Jury/Adoption.
- `D-0012` Balanced Total Success dominant.
- `D-0013` Traceability + assumptions gates.
- `D-0014` Blind Review + deadline reserve.
- `D-0015` Durable worker lifecycle signals.
- `D-0016` Foundation invariants locked; implementation identities evidence-driven.
- `D-0017` automated blind calibration evidence substitution waiver only for declared W004 scope.
- `D-0018` production-grade Autopilot + systematic Decision Research Gate.

Task-local W005 decisions aceitas nesta micro-integração não alteram silenciosamente a lista `D-####`; T010 deve sintetizar quais delas merecem promoção/registro canônico adicional e preservar `PENDING_EVIDENCE` onde aplicável.

## Current success bottleneck

`COMPLETE_REMAINING_W005_RESEARCH_INPUTS`

O critical path imediato é receber, validar e integrar T004/T005/T006/T007/T008/T009/T013/T014. Não aguardar todos para validar resultados independentes: micro-fan-in continua permitido. T010 só abre quando `11/11` inputs estiverem aceitos.

## Evidence boundary

- W004 case mechanics/evidence: preserved;
- W005 research inputs integrated: `3/11`;
- human gold/agreement/preference: **not observed**;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- production runtime winner: **not selected**;
- frontend/editor winner: **not selected**;
- blanket production readiness: **false / not claimed**;
- submission completed: **not claimed**.

## Next action

1. monitorar Issues #154,#155,#156,#157,#158,#159,#164,#165 por RESULT + exactly-one terminal signal;
2. validar provenance, branch diff, DRG coverage e CI/benchmark gates de cada resultado recebido;
3. integrar resultados válidos por micro-fan-in sem esperar siblings independentes;
4. manter T010 bloqueada até `11/11` research inputs `INTEGRATED`;
5. quando T010 liberar, executar synthesis → T011 red-team → T012 final fan-in/implementation DAG;
6. somente então abrir Phase 9 production implementation waves.

## Recovery point

Resume from STATE 0043. Active wave: `SYSTEM/WAVES/W005.json`. Integrated: T001,T002,T003. Running: T004,T005,T006,T007,T008,T009,T013,T014. Planned/gated: T010,T011,T012. No production framework/model/provider/database/parser/frontend/auth/storage/toolchain/deployment winner may be inferred beyond the explicit task-local evidence accepted above.
