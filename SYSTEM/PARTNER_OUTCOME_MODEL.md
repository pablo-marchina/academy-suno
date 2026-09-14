# PARTNER OUTCOME MODEL

`PARTNER_MODEL_VERSION: 1.0`

## 1. Maximum objective

O objetivo primário é entregar **a solução que mais ajuda o parceiro na dor que realmente importa**, dentro das restrições reais do case.

```text
MAXIMIZE expected_partner_value(
  solution |
  validated_pain,
  root_causes,
  affected_stakeholders,
  current_workflow,
  status_quo,
  desired_outcomes,
  constraints,
  adoption_friction,
  evidence
)
```

O score do case não pode compensar falha de valor para o parceiro.

## 2. Partner Contract

Antes de escolher direção de solução, registrar:

- parceiro e contexto de negócio;
- stakeholder(s) que sentem a dor e stakeholder(s) que decidem;
- pain statement em linguagem operacional;
- frequência, severidade, alcance e urgência;
- custo/tempo/risco/perda/oportunidade associados;
- workflow/comportamento atual e workarounds;
- causas-raiz versus sintomas;
- resultado desejado e definição de sucesso do parceiro;
- restrições reais: orçamento, prazo, sistemas, pessoas, compliance, operação;
- barreiras de adoção e incentivos;
- alternativas/status quo existentes;
- evidência, confiança e unknowns para cada item material.

Unknown crítico deve gerar pesquisa/experimento; não pode ser preenchido por conveniência.

## 3. Pain priority

A dor prioritária é escolhida por combinação de evidência e impacto: severidade, frequência, alcance, custo/risco, urgência estratégica e capacidade de intervenção. O sistema deve evitar atacar o sintoma mais visível quando causa mais material estiver acessível.

## 4. Solution Value Test

Toda alternativa relevante deve ser avaliada em:

- **Pain fit** — resolve a dor prioritária?
- **Root-cause fit** — atua no mecanismo correto ou apenas mascara sintoma?
- **Value magnitude** — quanto benefício provável gera?
- **Incrementality** — é melhor que status quo e alternativas simples?
- **Feasibility** — parceiro consegue implementar com recursos/restrições reais?
- **Adoption** — usuários/owners têm motivo e capacidade para usar?
- **Time-to-value** — quando o parceiro começa a capturar benefício?
- **Measurability** — há métricas leading/lagging verificáveis?
- **Risk/trade-offs** — downside é aceitável/mitigável?
- **Sustainability** — benefício persiste sem esforço desproporcional?
- **Actionability** — existe primeiro passo/piloto claro?

## 5. Partner hard gates

Não há `PARTNER_STATUS: PASS` se qualquer item aplicável falhar:

- dor prioritária e stakeholder estão suficientemente evidenciados;
- causa-raiz/material mechanism está explicitado ou uncertainty está controlada;
- recomendação mapeia diretamente dor → mecanismo → intervenção → outcome;
- valor esperado é maior que status quo e alternativas relevantes ou a preferência está justificada;
- benefício material possui métrica/indicador verificável;
- implementação é plausível nas restrições reais;
- adoção tem owner, incentivos, esforço e rollout considerados;
- riscos/trade-offs críticos estão tratados;
- existe primeiro passo ou piloto concreto;
- solução não depende de premissa crítica não testada sem plano de validação;
- nenhum elemento de alto custo/complexidade permanece sem contribuição clara para valor.

## 6. Partner Jury

Antes da finalização, rodar avaliações independentes pelos pontos de vista:

1. **Partner Advocate** — isso realmente reduz a dor mais importante?
2. **End User / Operator** — eu usaria isso no fluxo real? O que quebra?
3. **Decision Maker / Economic Buyer** — vale prioridade, custo, risco e recursos?
4. **Implementation Owner** — consigo colocar de pé, operar e medir?
5. **Counterfactual Skeptic** — por que não fazer nada ou uma opção mais simples/barata?

Findings críticos viram tasks; consenso sem evidência não fecha gate.

## 7. Adoption test

A recomendação final precisa responder:

- quem é o owner;
- quem precisa mudar comportamento;
- qual incentivo/benefício cada stakeholder recebe;
- esforço de implementação e dependências;
- primeira ação em 7/30/90 dias ou horizonte equivalente;
- piloto/MVP/experimento quando aplicável;
- sinais de sucesso e critérios de kill/pivot;
- como o parceiro captura valor após a entrega do case.

## 8. Anti-solutionism

É proibido manter solução/feature apenas por inovação, tecnologia, estética ou efeito de apresentação. Se componente não melhora Partner Value, requisito obrigatório ou redução de risco, deve ser removido/priorizado para baixo.

## 9. Stop condition

`PARTNER_STOP_CONDITION: PASS` somente quando todos os hard gates aplicáveis passaram, Partner Jury não possui finding crítico aberto, não há alternativa materialmente superior e viável sem avaliação, e ganhos adicionais esperados são pequenos depois de atingir um nível top-tier de utilidade/impacto.
