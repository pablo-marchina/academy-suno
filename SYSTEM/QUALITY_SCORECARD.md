# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0006`

`QUALITY_STATUS: CORE_FOUNDATION_EXECUTABLE`

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

A foundation crítica agora é executável e reconciliada: provenance/domain, source-trust, factual backbone, policy engine e 3×3 native-format planning compartilham contratos canônicos. Isso ainda não equivale a pipeline end-to-end nem a qualidade final: audience calibration, claim-level grounding, targeted repair, interface, confusion matrix, custo/latência e deliverables permanecem pendentes.

## Hard gates

Status: `ACTIVE_PARTIAL_EXECUTION`

1. pipeline funcional baseado em estado/grafo — `PARTIAL`: plain-async state semantics executadas; explicit final graph/orchestrator lock ainda pendente;
2. cobertura de 3 níveis × 3 formatos — `FOUNDATION_PASS`: planner determinístico produz 9 jobs únicos e formatos nativos passam testes; geração por provider ainda downstream;
3. framework híbrido com componente determinístico — `PARTIAL_PASS`: factual/policy/source deterministic gates executáveis; semantic layer ainda downstream;
4. legibilidade PT-BR calibrada — `PENDING`;
5. densidade/contextualização de termos financeiros — `PENDING`;
6. factuality/grounding contra fonte — `FOUNDATION_PASS_PARTIAL_SCOPE`: factual-v001 oracle + backbone passam; claim-level broader grounding ainda pendente;
7. auto-correção com feedback mensurável — `PARTIAL`: branch-local repair proof existe; evaluator-driven repair end-to-end pendente;
8. interface comparativa com métricas e rastreabilidade — `DESIGNED_NOT_BUILT`;
9. testes automatizados/reprodutíveis — `STRONG_PARTIAL`: domain, policy, factual, format, generation e experiment suites existem;
10. matriz de confusão dos níveis — `PENDING`;
11. análise custo/latência — `PENDING`;
12. README/documentação reproduzível — `PENDING`;
13. vídeo real comprovando código e interface — `PENDING`;
14. regra operacional de duração <=5:00 — `CONTROLLED_BY_PLAN`.

## Quality evidence gained

- provenance canônico é obrigatório por schema e chega a paragraph/slide/video segment;
- source readiness para fatos de tabela exige semantic role context; number overlap isolado não basta;
- factual-v001: 13 fixtures executadas, oracle comparison PASS, known CRITICAL mutations bloqueadas;
- policy engine integrado: recommendation/personalization/modality/attribution/caveat/source-mixing permanecem hard/review semantics não compensáveis;
- `HF-11` foi mantido como failure code dedicado para untraceable source mixing;
- Article/Carousel/ShortVideo continuam nativos e a suíte de formatos passou 14/14;
- 3×3 planner canônico passou 4/4 integration tests e mantém provider/model fora do domain contract;
- plain async provou fan-out/join/local repair/checkpoint/history; LangGraph continua pending runtime recheck.

## Open quality gaps

1. T010 deve verificar coerência cross-package e consolidar os locks provisórios sem extrapolar a evidência.
2. Construir gold/development benchmark, congelar held-out e calibrar audience/ACV/legibilidade/terminologia.
3. Implementar B08 claim-level grounding + semantic ablation sem permitir override dos hard gates determinísticos.
4. Provar targeted repair driven por failure codes sem regressão factual/policy.
5. Construir pipeline end-to-end e evidence cockpit com source lineage.
6. Medir custo/latência e comparar provider/model com baseline simples.
7. Construir report/confusion matrix/README e rehearsal de vídeo <=5:00.
8. Resolver deadline/submission quando informação existir.

## Next quality action

Executar W002-T010 e usar sua síntese para materializar a próxima wave; evitar UI polish e provider lock antes de fechar gold/grounding/repair/end-to-end proof.