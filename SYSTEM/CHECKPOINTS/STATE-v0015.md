# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0015`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 2 — Discovery & Evidence`

`LAST_COMMITTED_WAVE: W002-CORE-FANINS-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001 está COMPLETE e continua sendo a base arquitetural/evaluativa aceita;
- W002 está ACTIVE; W002-T001…T009 estão integradas e W002-T010 é o único fan-in restante;
- T001 definiu o canonical domain/provenance spine em Pydantic v2, serialização determinística e invariantes não compensatórios;
- T002/EXP-A provou que number/token coverage não basta para source trust: fatos de tabela exigem row/column/unit/period-or-metric role provenance; parser library continua desbloqueada;
- T003/T008 produziram policy engine integrado ao domain core com `FAIL > REVIEW_REQUIRED > PASS`, policy version/provenance auditáveis e `HF-11` dedicado para untraceable source mixing; disclaimer não compensa hard fail e política interna Suno continua UNKNOWN/configurável;
- T004/T009 reconciliaram Article/Carousel/ShortVideo com enums/provenance canônicos e implementaram planner determinístico de 3 audiences × 3 formats; native-format suite passou 14/14 e 3×3 suite 4/4;
- T005/EXP-B executou plain async com 9-way fan-out, join, branch-local repair, checkpoint/resume e history; LangGraph continua `PENDING_RUNTIME_RECHECK` porque seu challenger não executou no ambiente do experimento;
- T006/T007 materializaram factual-v001 + factual backbone/deterministic anchors; oracle comparison passou, 13/13 factual tests passaram e known CRITICAL mutations não podem auto-PASS;
- source extraction ambiguity, retrieval miss e confirmed unsupported claim permanecem estados distintos para evitar falsa certeza;
- hard factual/policy/source gates permanecem não compensatórios; semantic/LLM judge continua sensor secundário;
- W002-T010 está READY logicamente; após merge de STATE 0015 deve receber o SHA exato da main antes do worker iniciar;
- provider/model, semantic backend, audience thresholds e parser library final continuam evidence-driven e não estão lockados;
- deadline, submission, owner/decision maker e workflow interno Suno permanecem UNKNOWN e limitam production/ROI claims, mas não bloqueiam uma demo defensável.

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

Nenhum blocker impede W002-T010. LangGraph runtime proof, parser final, gold calibration, provider/model, semantic backend e internal partner unknowns são decisões/gaps posteriores, não dependências bloqueantes para a síntese W002.

## Active wave

`W002` — Foundation Correctness & Early Experiments.

### INTEGRATED
- `W002-T001` — domain schemas + provenance spine — Issue #33.
- `W002-T002` — real fixtures + parser/source trust bakeoff — Issue #34.
- `W002-T003` — executable policy hard-gate slice — Issue #35.
- `W002-T004` — format schemas + generation contracts — Issue #36.
- `W002-T005` — LangGraph vs plain async EXP-B — Issue #37.
- `W002-T006` — factual adversarial fixtures / EXP-C — Issue #38.
- `W002-T007` — factual backbone + deterministic anchors — Issue #39.
- `W002-T008` — policy engine integrated to canonical domain — Issue #40.
- `W002-T009` — canonical 3×3 generation core — Issue #41.

### READY after post-merge bind
- `W002-T010` — foundation synthesis / provisional architecture decision — Issue #42.

## Current success bottleneck

`W002_SYNTHESIS_AND_FOUNDATION_DECISION`

Os principais componentes de foundation agora existem e foram testados isolada/integrativamente. O próximo risco dominante é sintetizar as evidências sem lock indevido, verificar coerência do foundation combinado e escolher a próxima wave pelo maior gap de sucesso — provavelmente gold/audience calibration, claim-level grounding/repair e end-to-end evidence cockpit, mas T010 deve confirmar por evidência.

## Pending decisions

- orchestrator provisional posture: plain async lidera por runtime evidence; LangGraph requer recheck antes de qualquer lock positivo;
- parser/fallback final: source-trust contract está provado, mas library lock requer corpus maior/raw-byte replay;
- provider/model somente com measured quality/cost/latency;
- semantic backend após ablation e sem poder de override sobre deterministic hard gates;
- audience thresholds somente após development gold e separação de held-out;
- next wave B06–B14 deve ser priorizada por T010 usando total-success bottleneck, não por ordem nominal do backlog.

## Next action

1. mergear STATE 0015/core fan-ins;
2. bindar o SHA exato pós-merge na Issue #42/dispatch e marcar T010 READY executável;
3. revalidar lease para STATE 0015/current main;
4. iniciar W002-T010-A01;
5. integrar T010, fechar W002 e materializar a próxima wave a partir dos gaps/kill criteria aceitos.

## Recovery point

Retomar de `STATE_VERSION 0015` e `SYSTEM/CHECKPOINTS/STATE-v0015.md`. W002-T001…T009 são evidência integrada; W002-T010 é o único trabalho restante desta wave.