# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0014`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 2 — Discovery & Evidence`

`LAST_COMMITTED_WAVE: W002-FANOUT-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001 está COMPLETE e continua sendo a base arquitetural/evaluativa aceita;
- W002 está ACTIVE; W002-T001…T006 foram recebidas com lifecycle/proveniência válidos e integradas pelo Orchestrator;
- T001 implementou contratos Pydantic v2 de domínio/proveniência, serialização determinística e invariantes de hard-gate; 12 testes focados passaram no worker;
- T002/EXP-A materializou fixtures públicas reais de Copom/policy, fato relevante e earnings/results e demonstrou que presença de números não basta: fatos de tabela exigem row/column/unit/period-role provenance antes de `SOURCE_READY`;
- EXP-A não lockou biblioteca de parser; flat text é fallback aceitável somente quando não destrói estrutura material, caso contrário deve resultar em `REVIEW_REQUIRED`/fallback;
- T003 implementou policy gates determinísticos com `PASS | REVIEW_REQUIRED | FAIL`, recommendation/personalization/caveat/modality/attribution/source-mixing adversarial cases e disclaimer sem poder compensatório;
- política interna específica da Suno continua `UNKNOWN`; nenhum workflow/disclaimer interno foi inventado;
- T004 implementou contratos nativos de Article/Carousel/ShortVideo, source-ref hooks e separação audience × format; a suíte precisa ser reexecutada no fan-in porque o worker não conseguiu executá-la no próprio ambiente;
- T005/EXP-B executou o baseline plain-async com 9-way fan-out, join, branch-local repair, checkpoint/resume e history; o challenger LangGraph foi implementado, mas não executado por ausência da dependência no ambiente;
- consequência de EXP-B: plain async é o orchestrator provisório com evidência executada; LangGraph permanece `PENDING_RUNTIME_RECHECK`, sem lock positivo nem rejeição definitiva;
- T006/EXP-C materializou corpus factual adversarial versionado com 13 fixtures, 12 failure codes e oracle/harness independente de semantic judge; validação do contrato e comparação oracle passaram;
- hard factual/policy/source gates permanecem não compensáveis; semantic/LLM judge continua sensor secundário;
- as dependências de W002-T007, T008 e T009 estão todas integradas; os três micro-fan-ins podem rodar em paralelo após bind do SHA pós-merge;
- W002-T010 permanece PLANNED e depende de T005 + T007 + T008 + T009;
- provider/model, semantic backend, audience thresholds e parser library final continuam provisórios;
- deadline, submission, owner/decision maker e workflow interno Suno permanecem UNKNOWN e não bloqueiam uma demo defensável.

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

## Open blockers

Nenhum blocker impede W002-T007…T009. LangGraph runtime proof e parser final são decisões pendentes, não bloqueios para os micro-fan-ins.

## Active wave

`W002` — Foundation Correctness & Early Experiments.

### INTEGRATED
- `W002-T001` — domain schemas + provenance spine — Issue #33.
- `W002-T002` — real fixtures + parser/source trust bakeoff — Issue #34.
- `W002-T003` — executable policy hard-gate slice — Issue #35.
- `W002-T004` — format schemas + generation contracts — Issue #36.
- `W002-T005` — LangGraph vs plain async EXP-B — Issue #37.
- `W002-T006` — factual adversarial fixtures / EXP-C — Issue #38.

### READY after post-merge bind
- `W002-T007` — factual backbone + deterministic anchors — Issue #39.
- `W002-T008` — policy engine integrated with canonical domain contracts — Issue #40.
- `W002-T009` — 3×3 generation core integrated with canonical contracts — Issue #41.

### PLANNED
- `W002-T010` — foundation synthesis / provisional architecture decision — Issue #42; depends T005,T007,T008,T009.

## Current success bottleneck

`MICRO_FANIN_CORE_INTEGRATION_AND_RUNTIME_PROOF`

A fundação independente existe; o risco dominante agora é reconciliar os tipos/contratos em um core único sem duplicação semântica, provar os hard gates contra os fixtures aceitos e obter uma 3×3 generation foundation coerente. LangGraph só poderá voltar a liderar se o challenger executar e superar o baseline simples por evidência.

## Pending decisions

- LangGraph vs plain async final/provisional lock: plain async lidera por evidência executada; LangGraph requer runtime recheck;
- parser/fallback final: source-trust contract está definido, library lock requer corpus maior/raw-byte replay;
- `HF-11` source-mixing code deve ser aceito ou aliasado em T008 preservando a mesma hard-fail semantics;
- factual hard-gate implementation deve satisfazer o oracle de T006 em T007;
- format contracts devem ser reconciliados com T001 sem tipos duplicados em T009;
- provider/model somente em wave posterior com measured quality/cost/latency;
- semantic backend após ablation;
- audience thresholds após development gold.

## Next action

1. mergear esta integração / `STATE 0014`;
2. bindar o SHA exato da nova main nas Issues #39–#41 e marcar READY;
3. revalidar lease para STATE 0014/current main;
4. iniciar T007, T008 e T009 em paralelo;
5. integrar cada fan-in seguro; quando os três estiverem integrados, liberar T010 juntamente com T005 já integrada.

## Recovery point

Retomar de `STATE_VERSION 0014` e `SYSTEM/CHECKPOINTS/STATE-v0014.md`. W002-T001…T006 são evidência integrada; W002-T007…T009 são o próximo fan-out de micro-integração; T010 continua bloqueada por dependências.