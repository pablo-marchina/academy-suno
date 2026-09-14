# QUALITY MODEL — Academy Suno

`QUALITY_MODEL_VERSION: 1.1`

## 1. Maximum objective

A qualidade do case é avaliada como a capacidade de **demonstrar e defender a melhor solução para o parceiro**, respeitando briefing, entregáveis, critérios e restrições.

A função objetivo global é hierárquica:

```text
PRIMARY: MAXIMIZE expected_partner_value(final_solution)
CONSTRAINT: satisfy case_objective + mandatory_deliverables + evaluation_criteria + constraints
SECONDARY: MAXIMIZE evaluator confidence in rigor, feasibility, impact and clarity
```

O `SYSTEM/PARTNER_OUTCOME_MODEL.md` define o primary objective; este documento garante excelência do case que comunica/defende essa solução.

## 2. Case Contract

Extrair objetivo central, decisão/pergunta, entregáveis, critérios explícitos/pesos, audiência, restrições, prazo, falhas eliminatórias e padrão de evidência. Unknowns permanecem `UNKNOWN`.

## 3. Rubrica

Prioridade:

1. valor/impacto real para o parceiro;
2. critérios explícitos e entregáveis;
3. resposta direta ao objetivo;
4. evidência e rigor;
5. qualidade/comparação da solução;
6. viabilidade, adoção e impacto;
7. defesa perante audiência;
8. clareza/narrativa/qualidade final.

Pesos explícitos prevalecem; inferidos são marcados. Rubrica não pode ser rebaixada para fabricar sucesso.

## 4. Scorecard

`SYSTEM/QUALITY_SCORECARD.md` registra peso, score, confiança, evidência, gaps e próxima ação de cada critério quando a rubrica estiver calibrada.

## 5. Quality hard gates

- entregáveis obrigatórios completos;
- objetivo central respondido;
- critérios explícitos cobertos;
- restrições respeitadas;
- claims críticos suportados;
- números/premissas consistentes;
- Partner Outcome hard gates aplicáveis em PASS;
- recomendação defensável contra alternativas;
- formato/narrativa adequados;
- Q&A cobre objeções materiais.

## 6. Joint quality loop

```text
CURRENT SOLUTION + CASE
→ PARTNER JURY + RUBRIC GRADER + RED TEAM + EXECUTIVE JUDGE
→ PARTNER SCORECARD + QUALITY SCORECARD
→ RANK GAPS BY expected_partner_value_uplift first, then quality uplift
→ GENERATE PARALLEL TASKS
→ INTEGRATE
→ RE-EVALUATE WHOLE SOLUTION + CASE
→ repeat
```

## 7. Próxima ação

Tasks são priorizadas por hard gate, impacto esperado no parceiro, peso/severidade do gap, probabilidade de resolver, dependências, risco e tempo restante.

## 8. Critério de parada

Só encerrar quando Partner Outcome e Quality stop conditions forem PASS, não houver finding crítico, nenhuma alternativa materialmente superior/viável estiver sem avaliação e o case final estiver alinhado ao briefing.

Quando briefing não fornece escala, usar ambição top-tier; score agregado de qualidade >=95/100 e nenhum critério material <90/100 como referência, sem permitir que score compense Partner Outcome FAIL.

## 9. Anti-gaming

Proibido reduzir critérios, remover gaps difíceis, aceitar consenso como evidência, confundir task completion com valor, ou adicionar complexidade que não ajuda o parceiro/briefing.

## 10. Regra de supremacia

Partner Value prevalece sobre estética e velocidade, dentro das restrições explícitas do case.
