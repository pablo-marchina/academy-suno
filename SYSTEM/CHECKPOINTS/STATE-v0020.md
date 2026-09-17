# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0020`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 5 — Build, Implementation & Adoption`

`LAST_COMMITTED_WAVE: W003-COMPLETE-W004-ACTIVE`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 está ACTIVE;
- W003-T009 fechou o mechanics proof end-to-end: source → 9 jobs → evaluation → targeted repair → lossless join/aggregate, com RunStore pause/reopen/resume, um transport retry separado de um quality repair e hard-gate non-compensation;
- W003 mechanics estão PROVEN no escopo controlado; real provider/model quality, provider latency/usage/cost, semantic-backend value, parser generalization e real-model repair convergence permanecem PRODUCTION_UNKNOWN;
- audience calibration permanece `DIAGNOSTIC_ONLY`: gold-v001 não possui human gold/agreement independente suficiente; target→human e human→evaluator observed matrices continuam NOT_COMPUTABLE e threshold freeze não é autorizado;
- anti-gaming e held-out isolation estão executáveis; semantic ablation permanece NOT_RUN/NO_BACKEND_PREFERENCE; provider comparison permanece NOT_COMPARABLE/NO_PREFERENCE;
- plain async continua líder provisório por runtime evidence; LangGraph é challenger opcional e não bloqueia o critical path;
- o maior bottleneck migrou de arquitetura para `REPRESENTATIVE_HUMAN_PROVIDER_PARSER_EVIDENCE_AND_RELEASE_PROOF`;
- W004 materializa evidence cockpit, representative corpus/human calibration, provider evidence, parser generalization e downstream release proof sem converter unknowns em escolhas por preferência;
- deadline, submission, owner/decision maker e workflow interno Suno permanecem UNKNOWN e limitam production/ROI claims.

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

## W003 outcome

`W003_MECHANICS: PROVEN`
`W003_CALIBRATION: DIAGNOSTIC_ONLY`
`PRODUCTION_RELEASE_READINESS: NOT_CLAIMED`

T009 proof scope: 9/9 jobs, one branch-local repair, one independent transport retry, persistent reopen/resume, telemetry lineage and hard-gate non-compensation. The deterministic stub is mechanics evidence only and is not LLM/provider-quality evidence.

## Active wave

`W004` — Representative Evidence, Cockpit & Release Proof.

### READY after post-merge bind
- `W004-T001` — evidence cockpit / evidence graph — Issue #81.
- `W004-T002` — representative corpus + independent human-calibration preparation — Issue #82.
- `W004-T003` — parser/source generalization bakeoff — Issue #83.
- `W004-T004` — provider/model execution harness + observed telemetry — Issue #84.

### PLANNED fan-ins
- `W004-T005` — human annotation/agreement/audience calibration — Issue #85; depends T002.
- `W004-T006` — semantic backend ablation — Issue #86; depends T005.
- `W004-T007` — provider/model comparison — Issue #87; depends T004,T005.
- `W004-T008` — clean-E2E release proof + evidence packet — Issue #88; depends T001,T003,T005,T006,T007.

## Current success bottleneck

`REPRESENTATIVE_HUMAN_PROVIDER_PARSER_EVIDENCE_AND_RELEASE_PROOF`

A arquitetura e o control loop deixaram de ser o principal unknown. O maior ganho marginal agora é obter ground truth humano independente, runs de provider observáveis, parser generalization e um cockpit que preserve provenance/unknowns; depois executar release proof em clean checkout.

## Pending decisions

- audience thresholds somente após independent human gold + agreement/adjudication suficiente;
- semantic backend somente após ablation incremental no mesmo development gold;
- provider/model somente após quality + latency + usage/cost observados em runs comparáveis;
- parser implementation somente após expanded raw-byte/source bakeoff;
- production/release readiness somente após W004-T008 e final reviews;
- LangGraph recheck é opcional/non-blocking enquanto plain async continua evidence leader.

## Next action

1. mergear STATE 0020/W003 close + W004 materialization;
2. bindar SHA exato pós-merge nas Issues #81–#84 e marcar READY;
3. fechar Issue #67 e revalidar lease;
4. executar W004-T001..T004 em paralelo;
5. liberar T005/T006/T007/T008 por dependências, sem false precision.

## Recovery point

Retomar de `STATE_VERSION 0020` e `SYSTEM/CHECKPOINTS/STATE-v0020.md`. W003 está COMPLETE; W004-T001..T004 são os próximos workers seguros.