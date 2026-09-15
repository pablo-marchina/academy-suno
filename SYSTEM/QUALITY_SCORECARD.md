# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0003`

`QUALITY_STATUS: CALIBRATED_NO_DELIVERABLE`

`STOP_CONDITION: FAIL`

## Case Contract status

- Objective: `KNOWN`
- Mandatory deliverables: `6 DELIVERABLES IDENTIFIED`
- Explicit evaluation criteria: `REQUIREMENTS/HARD GATES IDENTIFIED`
- Evaluation weights/scale: `NOT PROVIDED`
- Audience: `3 OUTPUT AUDIENCES KNOWN / FINAL EVALUATOR UNKNOWN`
- Constraints/deadline: `SCOPE + VIDEO HARD GATE KNOWN / DATE UNKNOWN`
- Partner Outcome linkage: `PARTIAL_EVIDENCE`

## Current evaluation

O briefing já permite calibrar critérios e hard gates, mas não há solução/artefatos para pontuar qualidade. Não inventar pesos ou score agregado.

## Hard gates

Status: `ACTIVE`

1. pipeline funcional baseado em estado/grafo;
2. cobertura de 3 níveis × 3 formatos;
3. framework híbrido com componente determinístico;
4. legibilidade PT-BR calibrada;
5. densidade/contextualização de termos financeiros;
6. factuality/grounding contra fonte;
7. auto-correção com feedback mensurável;
8. interface comparativa com métricas e rastreabilidade;
9. testes automatizados/reprodutíveis;
10. matriz de confusão dos níveis;
11. análise custo/latência;
12. README/documentação reproduzível;
13. vídeo real comprovando código e interface;
14. regra operacional de duração <=5:00 devido ao conflito registrado em A-0001.

## Quality dimensions a usar após baseline

- completeness against brief;
- factual fidelity;
- conceptual preservation;
- audience calibration;
- format fitness;
- evaluator validity/calibration;
- experimental rigor;
- reproducibility;
- UX/demo clarity;
- technical decision quality;
- documentation quality;
- defense/Q&A robustness.

## Open quality gaps

1. Validar métrica de legibilidade PT-BR e thresholds por nível.
2. Construir ontologia/glossário e métricas de contextualização.
3. Definir factuality/grounding em nível de anchors/claims.
4. Criar golden/held-out dataset e ground truth para confusion matrix.
5. Escolher arquitetura por experimento, não por preferência.
6. Definir evaluators específicos por formato.
7. Preparar demo que mostre falha real e repair.
8. Resolver deadline/submission quando informação existir.

## Next quality action

Executar W001 e sintetizar especificação testável do Hybrid Evaluator + arquitetura candidata antes de iniciar build amplo.
