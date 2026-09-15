# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0007`

`QUALITY_STATUS: FOUNDATION_PROVEN_CALIBRATION_ACTIVE`

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

W002-T010 confirmou uma foundation coerente e evidence-backed, mas explicitou corretamente que ela não é um produto calibrado end-to-end. W003 prioriza o que ainda bloqueia qualidade defensável: gold/held-out, claim grounding, graph/state RunStore, audience metrics anti-gaming, clean combined regression, targeted repair, telemetry e calibration.

## Hard gates

Status: `ACTIVE_CALIBRATION_AND_E2E`

1. pipeline funcional baseado em estado/grafo — `PARTIAL_STRONG`: plain-async semantics provadas; explicit graph/state RunStore pendente W003-T003;
2. cobertura 3 níveis × 3 formatos — `FOUNDATION_PASS`: planner 9 jobs + native schemas passam; actual provider generation quality ainda não medida;
3. framework híbrido determinístico — `FOUNDATION_PASS_PARTIAL_SCOPE`: factual/policy/source hard gates executáveis; claim-level/semantic ablation pendentes;
4. legibilidade PT-BR calibrada — `W003_ACTIVE`;
5. densidade/contextualização de termos financeiros — `W003_ACTIVE`;
6. factuality/grounding contra fonte — `DETERMINISTIC_FOUNDATION_PASS / CLAIM_LEVEL_ACTIVE`;
7. auto-correção com feedback mensurável — `PARTIAL`: branch-local proof existe; evaluator-driven loop W003-T006;
8. interface comparativa com métricas/rastreabilidade — `DESIGNED_NOT_BUILT`;
9. testes automatizados/reprodutíveis — `STRONG_PARTIAL`: clean combined CI W003-T005;
10. matriz de confusão dos níveis — `W003-T008 PLANNED`;
11. análise custo/latência — `W003-T007 PLANNED`;
12. README/documentação reproduzível — `PENDING`;
13. vídeo real comprovando código/interface — `PENDING`;
14. vídeo <=5:00 — `CONTROLLED_BY_PLAN`.

## Accepted foundation evidence

- factual-v001 13/13 + oracle PASS;
- policy current adversarial contract PASS;
- native format 14/14 + generation 4/4 PASS;
- source/table-role provenance gate;
- plain async fan-out/join/local repair/checkpoint/history runtime proof;
- no provider/parser/backend lock sem evidência.

## Open quality gaps

1. Independent gold/development/held-out e annotation agreement.
2. Claim-level grounding e semantic ablation sem override dos hard gates.
3. PT-BR readability/terminology/ACV features com anti-gaming tests.
4. Explicit graph/state RunStore end-to-end e clean-checkout application CI.
5. Targeted repair + telemetry + calibration/confusion matrix.
6. Provider/model measured comparison, evidence cockpit, README/report e release/video proof em waves posteriores.
7. Resolver deadline/submission quando informação existir.

## Next quality action

Executar W003 fan-out T001–T005; liberar fan-ins por DAG. UI polish/provider preference continuam subordinados a calibration/grounding/end-to-end proof.
