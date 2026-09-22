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

## W005 micro-fan-in 1

O Orchestrator reconstruiu lifecycle por Issues/branches/results/PRs/CI e aceitou dez dos onze inputs obrigatórios de pesquisa.

### INTEGRATED — 10/11

- `W005-T001-A01` — measurable Production Contract acceptance — Issue #151 / PR #170.
  - `PROD-001..017` decompostos em evidência observável;
  - hard invariants existentes preservados; SLO/capacity/latency/cost/audience/retention/partner-workflow thresholds permanecem evidence-gated.

- `W005-T002-A01` — frontend/API/live Evidence Cockpit — Issue #152 / PR #171.
  - boundary HTTP tipado/versionado + OpenAPI e SSE como live feed default com cursor/replay/de-dup/snapshot fallback aceitos como decisões arquiteturais task-local;
  - autorização/redação ocorre server-side antes da serialização; source/citation refs são opacas/estáveis;
  - frontend/editor implementation continua `PENDING_EVIDENCE`.

- `W005-T003-A01` — orchestration/durability/concurrency — Issue #153 / PR #169.
  - exact 9/9, checkpoint/resume e process restart preservados no harness;
  - 15 runs de overhead sintético: p50 `46.236 ms`, p95 `64.228 ms`, max `89.156 ms`;
  - `lost_update_observed=true` foi reproduzido em stale same-run writes no SQLiteRunStore atual;
  - SQLiteRunStore não é authority multi-replica de produção; framework/runtime winner permanece `PENDING_EVIDENCE`.

- `W005-T004-A01` — identity/tenancy/data/storage/security — Issue #154 / PR #175.
  - authentication separada de tenant authorization; tenant/resource binding server-side e defesa em profundidade são invariantes;
  - pooled relational + explicit tenant keys + RLS/equivalent é `CANDIDATE`, não database winner;
  - arbitrary server filesystem path é proibido no boundary de produção; private object quarantine→validate→promote + immutable provenance é candidate lifecycle;
  - identity/database/storage vendors permanecem `NO_VENDOR_PREFERENCE`;
  - se PostgreSQL/RLS for escolhido, runtime roles/patch levels entram como release gates, incluindo a current security advisory registrada no resultado.

- `W005-T005-A01` — eval science / human calibration / EDD — Issue #155 / PR #172.
  - duas streams humanas cegas/independentes por item + adjudication acionada pelo protocolo é a metodologia default de calibração;
  - DEV/CALIBRATION/HELD_OUT são source-grouped; uncertainty para 3×3 é clusterizada por source;
  - LLM/model judge fica como sensor secundário calibrado e nunca substitui human gold/hard gates;
  - external eval framework continua `PENDING_EVIDENCE`; audience thresholds continuam `DIAGNOSTIC_ONLY` até human calibration + frozen held-out.

- `W005-T006-A01` — adaptive runtime/provider/model/routing — Issue #156 / PR #173.
  - optimizer fica dentro de envelope determinístico de eligibility + hard gates, com revalidação pós-rota;
  - rules/cascade é initial champion candidate e learned/contextual routing é challenger;
  - retries/fallback compartilham budget end-to-end e typed failure taxonomy;
  - policy/catalog são versionados e rollbackable; provider/model continua `NO_OVERALL_PROVIDER_MODEL_PREFERENCE / PENDING_REPRESENTATIVE_BAKEOFF`.

- `W005-T007-A01` — observability/telemetry/safe live evidence — Issue #157 / PR #178.
  - OTel/W3C/OTLP/Collector é candidate boundary para T010; backend permanece `NO_OVERALL_PREFERENCE`;
  - durable ordered product events são separados de sampled telemetry e são a authority do live cockpit;
  - raw source/prompts/outputs ficam OFF por default em telemetry; metric IDs high-cardinality não viram labels;
  - microbenchmark de 20k events mede payload/redaction/cardinality mechanics sem virar capacity/SLO claim.

- `W005-T008-A01` — deployment/reliability/capacity/recovery — Issue #158 / PR #176.
  - managed-container e cluster-scheduler classes permanecem candidates com `NO_OVERALL_PREFERENCE`;
  - load validation usa baseline + concurrency ladder + arrival staircase + burst + soak + controlled saturation + post-recovery;
  - capacity é reportada como saturation interval, não “N users” inventado;
  - restart/resume e clean backup/restore definidos devem ser 100% PASS antes de production claim; RTO/RPO/SLO continuam unknown até evidência.

- `W005-T013-A01` — developer platform/repository/toolchain/CI-CD — Issue #164 / PR #177.
  - GitHub Actions e CI hardening/reproducibility/supply-chain controls são aceitos como task-local `LOCK`;
  - full-SHA action pinning, least-privilege token, authoritative lockfile/frozen installs, lock-keyed cache, SBOM + artifact attestations/provenance entram no target;
  - Python manager (uv lead vs Poetry/PDM), JS manager/workspace e Nx/Turborepo permanecem `PENDING_EVIDENCE`; local wrapper e SBOM encoding permanecem `NO_PREFERENCE` onde indicado.

- `W005-T014-A01` — financial document parsing/extraction/source grounding — Issue #165 / PR #179.
  - fail-closed source trust é reafirmado: number/text recall não substitui page/table/cell semantic provenance;
  - diagnostic fixture: pypdf/pdftotext preservaram anchors mas tiveram structured role-pair recall `0.00`; PyMuPDF/pdfplumber tiveram `1.00` no fixture digital simples; OCR/text paths não provaram table semantics;
  - production parser permanece `PENDING_EVIDENCE / NO_PRODUCTION_PARSER_WINNER`;
  - next bakeoff deve comparar PyMuPDF/pdfplumber/Docling/Textract/Azure/Google no mesmo corpus financeiro real com provenance/role metrics, latency/cost/security/licensing.

Todos os PRs acima passaram os gates CI aplicáveis antes da integração.

### RESULT_RECEIVED_NOT_ACCEPTED — W005-T009-A01

`W005-T009-A01` completou lifecycle/provenance e trouxe material útil: hard-gate-first comparison, paired design, BCa uncertainty, randomization tests, multiple-comparison control e Pareto reporting.

Entretanto, A01 tentou `LOCK` de score escalar `40/30/15/15` e practical-effect thresholds fixos enquanto o próprio resultado reconhece que esses números são policy choices sem representative human/business evidence. Isso conflita com o DRG, com a ausência de pesos fornecidos pelo case e com a regra do operador de decisão baseada em dados.

Disposition:
- A01 é preservado como diagnostic research, mas **não é accepted input de T010**;
- fresh `W005-T009-A02` é obrigatório;
- A02 deve preservar hard gates, paired design, uncertainty e Pareto, remover pesos/thresholds não suportados e usar `NO_PREFERENCE/PENDING_EVIDENCE` para scalar utility até evidência representativa/sensitivity analysis justificar promoção.

### PLANNED — gated fan-in

- `W005-T010` — production architecture synthesis; depende de T001..T009 + T013 + T014 — Issue #160.
- `W005-T011` — independent production architecture red-team; depende de T010 — Issue #161.
- `W005-T012` — final W005 fan-in + implementation wave plan; depende de T010/T011 — Issue #162.

T010 continua bloqueada somente porque T009 ainda não possui um accepted attempt.

## Production truth after micro-fan-in

- acceptance semantics, API/live feed, security boundaries, eval protocol, adaptive-routing envelope, observability contract, reliability methodology, developer-platform controls e parser evidence constraints possuem research evidence aceita;
- nenhuma dessas decisões equivale a implementação ou production validation;
- SQLite/local state atual possui blocker reproduzido para stale concurrent same-run writes;
- identity/database/object-storage/cloud/orchestration/provider/model/frontend/editor/observability-backend/parser winners não estão selecionados;
- human-calibrated production audience thresholds permanecem open;
- capacidade/SLO/RTO/RPO/retention/business utility weights não são inventados;
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

Task-local W005 decisions não alteram silenciosamente a lista `D-####`; T010 deve sintetizar promoções canônicas e manter `NO_PREFERENCE/PENDING_EVIDENCE` quando o evidence gate não fechar.

## Current success bottleneck

`W005-T009-A02_QUANT_METHOD_REPAIR`

## Evidence boundary

- W004 case mechanics/evidence: preserved;
- W005 required research inputs accepted: `10/11`;
- W005-T009-A01: `RESULT_RECEIVED_NOT_ACCEPTED`;
- human gold/agreement/preference: **not observed**;
- audience thresholds: `DIAGNOSTIC_ONLY`;
- blanket production readiness: **false / not claimed**;
- submission completed: **not claimed**.

## Next action

1. create fresh `W005-T009-A02` after STATE 0043 becomes canonical, with explicit prohibition on ungrounded scalar weights/utility thresholds;
2. integrate T009-A02 if evidence-valid;
3. unlock T010 only at `11/11` accepted research inputs;
4. execute T010 synthesis → T011 independent red-team → T012 final fan-in/Phase 9 implementation DAG;
5. only then open production implementation waves.

## Recovery point

Resume from STATE 0043. Accepted W005 inputs: T001,T002,T003,T004,T005,T006,T007,T008,T013,T014. T009-A01 is received but rejected for ungrounded scalar-weight lock. T010/T011/T012 remain gated. No production technology winner may be inferred beyond explicit accepted evidence.
