# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0005`

`QUALITY_STATUS: FOUNDATION_PARTIAL_EXECUTABLE`

`STOP_CONDITION: FAIL`

## Case Contract status

- Objective: `KNOWN`
- Mandatory deliverables: `6 DELIVERABLES IDENTIFIED`
- Explicit evaluation criteria: `REQUIREMENTS/HARD GATES IDENTIFIED`
- Evaluation weights/scale: `NOT PROVIDED`
- Audience: `3 OUTPUT AUDIENCES KNOWN / FINAL EVALUATOR UNKNOWN`
- Constraints/deadline: `SCOPE + VIDEO HARD GATE KNOWN / DATE UNKNOWN`
- Partner Outcome linkage: `VALUE_HYPOTHESIS_SUPPORTED_EXECUTION_PARTIAL`

## Current evaluation

A foundation começou a existir em código/fixtures: provenance/domain contracts, source-trust experiment, policy gates, native format contracts, orchestration baseline e factual adversarial oracle. Ainda não existe pipeline end-to-end nem calibration suficiente para declarar os hard gates finais aprovados.

## Hard gates

Status: `ACTIVE_PARTIAL_EXECUTION`

1. pipeline funcional baseado em estado/grafo — `PARTIAL`: state semantics plain-async executadas; explicit graph/final orchestrator ainda pendente;
2. cobertura de 3 níveis × 3 formatos — `PARTIAL`: contracts existem; fan-out integrado pendente T009;
3. framework híbrido com componente determinístico — `PARTIAL`: deterministic source/policy/factual layers em construção;
4. legibilidade PT-BR calibrada — `PENDING`;
5. densidade/contextualização de termos financeiros — `PENDING`;
6. factuality/grounding contra fonte — `PARTIAL`: provenance/source-trust + adversarial oracle; T007/B08 ainda pendentes;
7. auto-correção com feedback mensurável — `PARTIAL`: branch-local repair proof; evaluator-driven repair end-to-end pendente;
8. interface comparativa com métricas e rastreabilidade — `DESIGNED_NOT_BUILT`;
9. testes automatizados/reprodutíveis — `PARTIAL`: unit/policy/factual/experiment suites já existem;
10. matriz de confusão dos níveis — `PENDING`;
11. análise custo/latência — `PENDING`;
12. README/documentação reproduzível — `PENDING`;
13. vídeo real comprovando código e interface — `PENDING`;
14. regra operacional de duração <=5:00 — `CONTROLLED_BY_PLAN`.

## Quality evidence gained

- source/hash/provenance invariants são schema-level e auditáveis;
- parser acceptance não pode usar apenas token/number coverage; table-role lineage é requisito material;
- recommendation/personalization/modality/attribution/caveat/source-mixing têm policy findings executáveis;
- Article/Carousel/ShortVideo possuem contracts nativos distintos;
- plain async provou 9-way fan-out/repair/checkpoint semantics; LangGraph continua sem runtime proof;
- factual-v001 congela known critical mutations antes da implementação B03/B08.

## Open quality gaps

1. Integrar T001+T002+T006 em factual backbone que satisfaça o oracle.
2. Integrar T001+T003 em policy engine sem tipos duplicados.
3. Integrar T001+T004 em 3×3 generation core e reexecutar os format tests.
4. Reexecutar LangGraph challenger em ambiente com dependência antes de qualquer lock favorável.
5. Construir gold/development benchmark e calibrar audience/evaluator sem held-out leakage.
6. Provar targeted repair sem regressão factual/policy.
7. Construir evidence cockpit e rehearsal <=5:00.
8. Resolver deadline/submission quando informação existir.

## Next quality action

Executar T007/T008/T009 em paralelo e só então permitir T010 decidir a foundation provisória; não adicionar soft-metric sophistication ou UI polish antes de fechar os core integration gaps.