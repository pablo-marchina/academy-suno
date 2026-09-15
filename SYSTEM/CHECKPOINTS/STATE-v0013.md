# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0013`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 2 — Discovery & Evidence`

`LAST_COMMITTED_WAVE: W002-MATERIALIZED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001 está COMPLETE e é a base arquitetural/evaluativa aceita;
- W002 está ACTIVE contra o checkpoint de W001 e foi desenhada para `FOUNDATION_CORRECTNESS_AND_EXPERIMENTAL_PROOF`;
- fan-out inicial W002-T001…T006 tem ownership paths disjuntos e pode rodar em paralelo após bind do SHA pós-merge nas Issues;
- T001 implementa domain/provenance contracts;
- T002 executa real-source fixtures + parser/source-trust bakeoff (EXP-A);
- T003 implementa policy hard-gate slice + adversarial policy tests;
- T004 implementa format schemas/generation contracts;
- T005 executa LangGraph vs plain-async smoke test (EXP-B);
- T006 constrói factual adversarial fixtures/hard-gate test spec (EXP-C factual slice);
- T007/T008/T009 são micro-fan-ins de factual backbone, policy core e 3×3 generation core;
- T010 fecha W002 e decide locks provisórios com base em evidência;
- parser/framework/provider/semantic backend/thresholds continuam provisórios até seus experimentos;
- hard factual/policy/source gates não podem ser enfraquecidos para facilitar implementação;
- deadline, submission, owner/decision maker e workflow interno Suno permanecem UNKNOWN e não bloqueiam a demo defensável.

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

Nenhum blocker impede o fan-out W002-T001…T006. External unknowns continuam limitando apenas production/ROI/internal-policy claims.

## Active wave

`W002` — Foundation Correctness & Early Experiments.

### READY after post-merge bind
- `W002-T001` — domain schemas + provenance spine — Issue #33.
- `W002-T002` — real fixtures + parser/source trust bakeoff — Issue #34.
- `W002-T003` — executable policy hard-gate slice — Issue #35.
- `W002-T004` — format schemas + generation contracts — Issue #36.
- `W002-T005` — LangGraph vs plain async EXP-B — Issue #37.
- `W002-T006` — factual adversarial fixtures / EXP-C — Issue #38.

### PLANNED fan-in
- `W002-T007` depends T001,T002,T006.
- `W002-T008` depends T001,T003.
- `W002-T009` depends T001,T004.
- `W002-T010` depends T005,T007,T008,T009.

## Current success bottleneck

`FOUNDATION_CORRECTNESS_AND_EXPERIMENTAL_PROOF`

O principal risco agora é implementação incorreta ou escolha de stack por preferência. W002 deve produzir evidência executável antes de lockar parser/orchestrator e antes de investir em semantic sophistication/UI polish.

## Pending decisions

- LangGraph vs simple fallback após W002-T005/EXP-B;
- parser/fallback após W002-T002/EXP-A;
- hard factual/policy implementation após T003/T006/T007/T008;
- provider/model apenas em wave posterior com measured quality/cost/latency;
- semantic backend após ablation;
- audience thresholds após development gold.

## Next action

1. merge STATE 0013/W002 materialization;
2. bind exact post-merge main SHA into Issues #33–#38 and set READY;
3. revalidate lease to STATE 0013/current main;
4. user starts six workers T001…T006;
5. Orchestrator reconstructs lifecycle from task signals and micro-fan-ins accepted results as soon as dependency sets complete.

## Recovery point

Retomar de `STATE_VERSION 0013` e `SYSTEM/CHECKPOINTS/STATE-v0013.md`. W002-T001…T006 são o fan-out inicial; T007…T010 não devem iniciar antes de suas dependências.