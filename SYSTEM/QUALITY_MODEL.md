# QUALITY MODEL — Academy Suno

`QUALITY_MODEL_VERSION: 1.0`

## 1. Maximum objective

O objetivo dominante do sistema é **maximizar a qualidade esperada do case final segundo o que realmente será avaliado**.

Velocidade, paralelismo, quantidade de análises, volume de pesquisa e sofisticação técnica são meios. Nenhum deles pode ser otimizado em detrimento do resultado final.

A função objetivo é:

```text
MAXIMIZE expected_evaluator_quality(final_case | case_objective, mandatory_deliverables, evaluation_criteria, constraints, evidence)
```

## 2. Case Contract

Antes de otimizar o case, o Orchestrator deve extrair do briefing e registrar um `CASE_CONTRACT` contendo:

- objetivo central do case;
- pergunta/decisão que a entrega precisa responder;
- entregáveis obrigatórios e opcionais;
- critérios explícitos de avaliação e pesos, quando fornecidos;
- expectativas implícitas razoavelmente inferíveis da audiência/banca;
- restrições de formato, prazo, escopo, dados e implementação;
- penalidades ou falhas eliminatórias;
- padrão de evidência necessário;
- audiência e contexto de decisão.

Se algum item crítico não for conhecido, ele é marcado `UNKNOWN`; o sistema não inventa requisitos.

A Phase 1 não pode fechar sem Case Contract suficiente para construir uma rubrica de qualidade defensável.

## 3. Rubrica de avaliação

A rubrica deve priorizar nesta ordem:

1. critérios explícitos do case;
2. aderência aos entregáveis e restrições;
3. resposta direta ao objetivo central;
4. qualidade da evidência e rigor analítico;
5. qualidade da recomendação/solução;
6. viabilidade e impacto;
7. capacidade de defesa perante a audiência;
8. clareza, narrativa e qualidade final da entrega.

Pesos explícitos fornecidos pelo case prevalecem. Pesos inferidos devem ser marcados como inferência e justificados.

A rubrica não pode ser alterada para facilitar aprovação. Mudança material exige nova informação sobre o case ou `DECISION_REVIEW`.

## 4. Scorecard

`SYSTEM/QUALITY_SCORECARD.md` registra o estado corrente da qualidade.

Quando a rubrica estiver calibrada, cada critério recebe:

- peso;
- score normalizado 0–100;
- confiança da avaliação;
- evidência que sustenta o score;
- gaps concretos;
- melhor próxima ação para elevar o score.

O score agregado é uma ferramenta de priorização, não substitui os hard gates.

## 5. Hard gates

Independentemente do score agregado, o case não pode ser considerado final se qualquer item aplicável falhar:

- todos os entregáveis obrigatórios estão completos;
- a entrega responde diretamente ao objetivo central;
- todos os critérios explícitos estão cobertos;
- restrições do briefing são respeitadas;
- não existem claims críticos sem suporte adequado;
- números e premissas materiais são consistentes;
- não existe finding crítico de Red Team sem tratamento;
- recomendação principal é defensável contra alternativas relevantes;
- narrativa e formato final estão adequados à audiência;
- Q&A/defesa cobre as objeções materiais previsíveis.

## 6. Quality loop

Após existir uma primeira solução avaliável, o Orchestrator executa ciclos:

```text
CURRENT CASE
   ↓
FULL EVALUATION
   ↓
RUBRIC GRADER + RED TEAM + EXECUTIVE JUDGE
   ↓
QUALITY SCORECARD
   ↓
RANK GAPS BY expected_quality_uplift + criticality
   ↓
GENERATE PARALLEL TASKS / DISPATCHES
   ↓
WORKERS
   ↓
SYNTHESIS + INTEGRATION
   ↓
RE-EVALUATE FULL CASE
   ↓
repeat
```

A avaliação deve olhar o case completo, não apenas o trabalho produzido no ciclo mais recente.

## 7. Escolha automática da próxima ação

O Orchestrator prioriza tarefas pelo impacto esperado sobre a qualidade final, considerando:

- hard gate bloqueado;
- peso do critério afetado;
- severidade do gap;
- probabilidade de a tarefa resolver o gap;
- dependências/caminho crítico;
- risco de uma premissa estar errada;
- custo/tempo restante.

Tarefas de baixo impacto não devem ocupar o caminho crítico enquanto houver gaps materiais de maior valor.

## 8. Critério de parada

O loop só pode encerrar normalmente quando:

- todos os hard gates aplicáveis = `PASS`;
- `QUALITY_STATUS = PASS`;
- nenhum critério explícito material estiver abaixo do threshold calibrado;
- não houver finding crítico aberto;
- nenhuma alternativa materialmente superior permanecer sem avaliação;
- revisão final estiver alinhada ao briefing e aos entregáveis;
- ganhos marginais esperados dos próximos ciclos forem pequenos **depois** de os requisitos de qualidade acima terem sido atingidos.

Threshold padrão quando o briefing não fornece escala própria: equivalente a nível top-tier, com score agregado >= 95/100 e nenhum critério material < 90/100. O Orchestrator deve recalibrar estes valores quando a escala real do case for conhecida, sem reduzir a ambição de resultado.

Se o target não puder ser atingido por falta de informação, prazo ou decisão externa, o sistema usa `HUMAN_DECISION_REQUIRED`; não declara sucesso artificialmente.

## 9. Anti-gaming

É proibido melhorar artificialmente o score por:

- reduzir pesos ou thresholds sem nova evidência;
- remover um critério difícil;
- marcar gap como resolvido sem evidência;
- confundir completude de tarefa com qualidade do case;
- aceitar consenso entre agentes como substituto de validação;
- produzir complexidade que não melhora o resultado avaliado.

## 10. Regra de supremacia

Em conflito entre velocidade operacional e qualidade final, a qualidade final prevalece, respeitando restrições reais de prazo e recursos do case.
