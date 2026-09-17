# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0021`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 5 — Build, Implementation & Adoption`

`LAST_COMMITTED_WAVE: W004-INITIAL-EVIDENCE-FANOUT-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 está ACTIVE;
- W004-T001 está integrada: B13 evidence cockpit é uma projeção read-only dos artifacts/RunStore/telemetry/calibration existentes, preserva provenance source/run/job/attempt, exibe 3×3, repair before/after, telemetry e estados explícitos `PROVEN`, `DIAGNOSTIC_ONLY`, `NOT_COMPUTABLE`, `NOT_RUN`, `NOT_COMPARABLE`, `PRODUCTION_UNKNOWN`, `FAIL`, `REVIEW_REQUIRED`, sem aggregate green score compensatório;
- W004-T002 está integrada: `w004-corpus-v001` expandiu o bootstrap para 6 source documents com split por source (4 DEVELOPMENT / 2 HELD_OUT), congelou 36 outputs naturais de development (4 fontes × 3 formatos × 3 targets), manteve zero held-out generation e preparou blind double annotation + adjudication + agreement tooling; human gold/agreement observado ainda não existe;
- W004-T003 está integrada: source-trust/parser bakeoff generalizou para Copom, CVM ITR/schema evolution e Petrobras 1T26; 8/8 focused tests PASS e os probes mostram que 100% value coverage não compensa perda de table/row/column/unit/period role; parser implementation permanece `UNLOCKED`, raw-byte cross-parser replay e OCR/scanned coverage seguem abertos;
- W004-T004 entregou e teve aceito no staging um provider-neutral telemetry harness com N/A-safe usage/cost e pricing provenance guardrails, mas a tentativa terminou `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: nenhum provider/model call real foi executado, observed latency/usage/cost permanecem `N/A`/`PRODUCTION_UNKNOWN` e provider/model preference continua não autorizada;
- worker heads T001/T002 passaram `System Integrity` + `Foundation Regression`; o staging T003/T004 também passou os dois gates antes do fan-in final;
- W003 mechanics continuam PROVEN no escopo controlado; audience thresholds continuam `DIAGNOSTIC_ONLY`; semantic backend permanece `NOT_RUN/NO_BACKEND_PREFERENCE`;
- o maior bottleneck executável agora é `INDEPENDENT_HUMAN_ANNOTATION_AGREEMENT_AND_CALIBRATION`; provider execution real é um blocker externo paralelo e necessário antes de W004-T007/provider comparison;
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

## Active wave

`W004` — Representative Evidence, Cockpit & Release Proof.

### INTEGRATED
- `W004-T001` — evidence cockpit / evidence graph — Issue #81 / PR #93.
- `W004-T002` — representative corpus + independent human-calibration preparation — Issue #82 / PR #94.
- `W004-T003` — parser/source generalization bakeoff — Issue #83 / PR #91.

### BLOCKED with accepted harness evidence
- `W004-T004` — provider/model execution harness + observed telemetry — Issue #84 / PR #90; harness integrated, real credentialed provider execution still blocked externally.

### READY after post-merge bind
- `W004-T005` — human annotation/agreement/audience calibration — Issue #85; dependency T002 satisfied.

### PLANNED fan-ins
- `W004-T006` — semantic backend ablation — Issue #86; depends T005.
- `W004-T007` — provider/model comparison — Issue #87; depends T004 real-run evidence + T005.
- `W004-T008` — clean-E2E release proof + evidence packet — Issue #88; depends T001,T003,T005,T006,T007.

## Current success bottleneck

`INDEPENDENT_HUMAN_ANNOTATION_AGREEMENT_AND_CALIBRATION`

A preparation anti-circularity está pronta e o held-out continua protegido. O maior ganho marginal seguro agora é executar duas anotações primárias independentes + adjudicação no development frozen set, medir agreement antes da adjudicação e produzir target→human e human→evaluator matrices sem usar requested target como gold. Em paralelo, provider execution real continua um gap externo, mas não deve bloquear T005/T006.

## Pending decisions

- audience thresholds somente após independent human gold + agreement/adjudication suficiente; caso contrário permanecem `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation incremental no development gold produzido por T005;
- provider/model somente após quality + latency + usage/cost observados em runs comparáveis; T004 A01 não fornece esse evidence;
- parser implementation somente após same-raw-byte comparison entre candidatos e cobertura OCR/scanned; current role-hard-gate contract permanece obrigatório;
- production/release readiness somente após W004-T008 e final reviews;
- LangGraph recheck é opcional/non-blocking enquanto plain async continua evidence leader.

## Next action

1. mergear STATE 0021 com T001/T002/T003 integradas e T004 harness aceito porém external-run BLOCKED;
2. bindar SHA exato pós-merge na Issue #85 e marcar W004-T005 READY;
3. fechar Issues #81/#82/#83; manter #84 aberta/BLOCKED até nova tentativa credenciada;
4. executar W004-T005-A01 sem expor held-out;
5. após T005, liberar T006 e reavaliar se existe provider evidence suficiente para T007; sem isso, provider comparison permanece bloqueada.

## Recovery point

Retomar de `STATE_VERSION 0021` e `SYSTEM/CHECKPOINTS/STATE-v0021.md`. W004-T001/T002/T003 estão integradas; T004 possui harness integrado mas execução real bloqueada; T005 é o próximo worker seguro.