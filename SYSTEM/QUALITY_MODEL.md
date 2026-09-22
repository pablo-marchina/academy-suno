# QUALITY MODEL — Academy Suno

`QUALITY_MODEL_VERSION: 1.3`

## 1. Role in total success

Quality Model é uma dimensão crítica do `SYSTEM/SUCCESS_MODEL.md`: garante aderência ao briefing, rigor, completude, clareza, diferenciação e defesa do que está sendo entregue. Não pode compensar Partner Outcome FAIL nem ser tratado como secundário dispensável. Para o novo escopo, também impede que demo/local proof seja promovido a production quality sem evidência operacional.

## 2. Contracts

Extrair objetivo/decisão, entregáveis, critérios/pesos, audiência, restrições, prazo, formato, falhas eliminatórias e padrão de evidência do Case Contract; preservar Partner Contract e obedecer `SYSTEM/PRODUCTION_CONTRACT.md`. Unknowns permanecem `UNKNOWN`.

## 3. Quality dimensions

- Brief/Evaluation Fit;
- Evidence & Analytical Rigor;
- Solution comparison/differentiation;
- Deliverable completeness/consistency;
- Communication/storytelling;
- Defense/Q&A;
- submission/format quality;
- production engineering quality;
- evaluation science/calibration quality;
- security/reliability/observability quality;
- decision-research quality.

Pesos explícitos prevalecem; inferidos são marcados.

## 4. Quality hard gates

Entregáveis completos; objetivo respondido; critérios explícitos cobertos; restrições respeitadas; claims/números consistentes; fontes adequadas; solução defensável contra alternativas; formato/narrativa adequados; Q&A e submission readiness completos; production claims apenas com Production Contract PASS aplicável; escolhas materiais research-gated; cross-tenant/auth/security failures críticos não compensáveis; hard factual/source/policy gates não compensáveis; eval regression em mudanças probabilísticas materiais.

## 5. Quantitative-first evaluation

Quando uma propriedade é mensurável, usar dados em vez de rótulos vagos. Reportar distribuição/percentis e uncertainty quando relevantes. Não esconder regressão atrás de score agregado. Quality gates devem preservar slices, hard failures, cost/latency/reliability e dataset version.

## 6. Adaptive quality

Adaptação é aceitável em routing/model/prompt/retrieval/repair/budget desde que a política seja versionada, observável e incapaz de relaxar hard gates. Determinismo protege invariantes; adaptação otimiza trade-offs.

## 7. Evaluation loop

Quality Scorecard alimenta o Success Scorecard. Findings do Evaluator, Red Team, Evidence/Consistency Auditor, Security/Reliability review e Blind Judge viram gaps priorizados pelo Success Model.

## 8. Anti-gaming

Proibido reduzir critérios, esconder unknowns, confundir task completion com qualidade, usar consenso como evidência, chamar automated calibration de human gold, chamar demo de production readiness, congelar stack sem DRG, ou melhorar estética enquanto hard gate material permanece falhando.

## 9. Stop

`QUALITY_STATUS: PASS` + `STOP_CONDITION: PASS` somente com gates PASS e material final alinhado aos contratos, consistente, reproduzível e defensável.
