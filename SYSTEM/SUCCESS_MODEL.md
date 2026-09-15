# SUCCESS MODEL — Academy Suno

`SUCCESS_MODEL_VERSION: 1.0`

## 1. Definição de sucesso

A melhor entrega é a combinação de **valor real para o parceiro + aderência integral ao case + rigor/evidência + qualidade da solução + viabilidade/adoção + excelência do entregável + capacidade de defesa**, dentro do prazo e das restrições.

Nenhuma dimensão crítica pode compensar a falha de outra por média simples.

```text
MAXIMIZE expected_total_success
SUBJECT TO all critical hard gates and minimum floors
```

## 2. Dimensões de sucesso

1. **Partner Outcome** — resolve dor material e produz resultado útil.
2. **Brief / Evaluation Fit** — responde exatamente ao objetivo, entregáveis, critérios e restrições.
3. **Evidence & Analytical Rigor** — claims, números, causalidade e premissas são defensáveis.
4. **Solution Strength & Differentiation** — alternativa escolhida é superior/relevante e não apenas óbvia ou sofisticada.
5. **Feasibility & Adoption** — parceiro consegue implementar, usar e capturar valor.
6. **Deliverable & Artifact Excellence** — tudo que foi pedido está completo, consistente, utilizável e profissional.
7. **Communication & Defense** — narrativa, clareza, Q&A e persuasão tornam a lógica verificável pela audiência.
8. **Execution Robustness** — riscos, compliance/ética quando aplicável, prazo, submission e dependências estão controlados.

Pesos explícitos do case prevalecem. Sem pesos explícitos, o sistema não inventa precisão: usa hard gates, floors e priorização por bottleneck.

## 3. Regra de otimização

Ordem operacional:

1. fechar qualquer hard gate crítico;
2. elevar a dimensão crítica mais fraca/bottleneck;
3. entre tarefas comparáveis, escolher maior `expected_total_success_uplift` por unidade de tempo/risco;
4. depois otimizar refinamentos marginais.

Partner Value e critérios do case são ambos essenciais. Uma ótima solução que não cumpre o case falha; um case impecável que não ajuda o parceiro também falha.

## 4. Hard gates globais

- Case Contract e Partner Contract suficientemente completos;
- todos os entregáveis/requisitos obrigatórios rastreados;
- Partner Outcome gates PASS;
- Quality gates PASS;
- nenhum claim material sem evidência ou marcação explícita de incerteza;
- nenhuma premissa crítica de alto impacto/alta incerteza sem validação ou plano de controle;
- alternativa recomendada comparada a counterfactuals relevantes;
- implementação/adoção/métricas plausíveis;
- riscos legais, de compliance, privacidade, segurança ou ética tratados quando aplicáveis;
- números/fontes consistentes entre todos os artefatos;
- blind final review PASS;
- checklist de submissão e formato PASS;
- prazo/finalization reserve respeitado.

## 5. Evidence hierarchy

Priorize, quando disponível:

1. evidência direta do parceiro/dados do case;
2. fonte primária oficial;
3. dados/estudos confiáveis e atuais;
4. benchmark comparável;
5. inferência explícita;
6. hipótese a validar.

Consenso entre agentes não eleva o nível de evidência.

## 6. Traceability chain

Toda recomendação/claim material deve poder ser percorrida como:

```text
CASE REQUIREMENT / PARTNER PAIN
→ EVIDENCE
→ ASSUMPTION (se houver)
→ INSIGHT / MECHANISM
→ SOLUTION ELEMENT
→ EXPECTED OUTCOME
→ METRIC
→ DELIVERABLE LOCATION
→ VALIDATION STATUS
```

A fonte canônica é `SYSTEM/TRACEABILITY_MATRIX.md`.

## 7. Uncertainty & risk

`SYSTEM/ASSUMPTION_RISK_REGISTER.md` classifica premissas por impacto e incerteza. High-impact + high-uncertainty vira prioridade de pesquisa/teste e bloqueia conclusão normal se permanecer sem controle.

## 8. Deadline-aware optimization

Quando o prazo for conhecido, o Orchestrator registra `DEADLINE` e `FINALIZATION_RESERVE`. Antes da reserva, explore/otimize; durante a reserva, priorize integração, blind review, correções críticas, consistência e submissão. Trabalho especulativo novo só entra se corrigir hard gate ou risco material.

## 9. Independent final validation

Antes da entrega, execute `SYSTEM/FINAL_REVIEW_PROTOCOL.md`. O Blind Judge deve avaliar apenas briefing/contratos e o material que a banca/parceiro realmente receberá — sem se apoiar na memória interna dos agentes.

## 10. Stop condition

`SUCCESS_STOP_CONDITION: PASS` somente quando:

- `PARTNER_STATUS/PARTNER_STOP_CONDITION = PASS`;
- `QUALITY_STATUS/STOP_CONDITION = PASS`;
- todos os hard gates globais PASS;
- traceability obrigatória completa;
- critical assumptions controladas;
- blind final review PASS;
- nenhuma alternativa materialmente superior e viável permanecer sem avaliação;
- próximos ganhos esperados forem marginais em relação ao tempo/risco restante.
