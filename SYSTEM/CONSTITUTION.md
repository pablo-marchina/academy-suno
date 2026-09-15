# SYSTEM CONSTITUTION

`PROTOCOL_VERSION: 1.5.0`

## 1. Purpose

Este protocolo existe para produzir a melhor entrega possível como uma combinação inseparável de valor ao parceiro, aderência ao case, rigor, solução, viabilidade, execução do deliverable e defesa — com continuidade e paralelismo seguros.

## 2. Invariantes

1. GitHub é fonte de verdade; memória de chat é cache.
2. `SYSTEM/STATE.md` é o único estado canônico corrente.
3. Somente Orchestrator com lease ativo altera arquivos canônicos.
4. Workers nunca integram suas próprias conclusões.
5. Toda tarefa tem `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION`, `BASE_COMMIT_SHA`.
6. IDs/attempts não são reutilizados.
7. Decisão `LOCKED` não muda silenciosamente.
8. Tarefas independentes devem ser paralelizadas quando isso não reduz qualidade.
9. Resultado baseado em estado antigo é potencialmente stale.
10. Nenhuma fase avança sem gate.
11. Todo incremento de estado cria checkpoint imutável.
12. Toda wave tem DAG/ready queue.
13. Resultado relevante é persistido no GitHub.
14. **A função objetivo dominante é maximizar sucesso total balanceado conforme `SYSTEM/SUCCESS_MODEL.md`.**
15. Nenhuma média/score agregado pode compensar falha de hard gate crítico.
16. Partner Outcome e Quality Model são componentes obrigatórios do Success Model; nenhum deles sozinho define sucesso.
17. Todo requisito/pain/claim material deve possuir traceability até a entrega.
18. Premissa crítica de alto impacto/alta incerteza precisa ser validada ou explicitamente controlada.
19. Finalização exige blind review independente do contexto interno.
20. `PROJECT_STATUS: COMPLETE` exige Success + Partner + Quality stop conditions PASS.

## 3. Success architecture

```text
CASE + PARTNER EVIDENCE
→ CASE CONTRACT + PARTNER CONTRACT
→ SUCCESS MODEL / SCORECARDS
→ TRACEABILITY + ASSUMPTION/RISK REGISTER
→ DISCOVERY / DIAGNOSIS
→ SOLUTION PORTFOLIO + COUNTERFACTUALS
→ BUILD / IMPLEMENTATION / ADOPTION
→ PARTNER JURY + RED TEAM + EVALUATOR
→ SUCCESS BOTTLENECK ANALYSIS
→ PARALLEL IMPROVEMENT TASKS
→ BLIND FINAL REVIEW
→ FINAL DELIVERY
```

O Orchestrator fecha hard gates primeiro, depois eleva o bottleneck de sucesso, e só então otimiza detalhes marginais.

## 4. Roles

Orchestrator controla objetivos, DAG, bottlenecks, integração e stop condition. Workers especializados investigam, analisam, constroem ou atacam dimensões específicas. Partner Jury protege utilidade; Evaluator/Red Team protege rigor e critérios; Evidence/Consistency Auditor protege claims/números; Blind Judge simula o receptor final sem contexto privilegiado.

## 5. Concurrency & provenance

Lease em `control/orchestrator-lease`; workers usam Issues/branches isoladas. Micro-fan-in permitido. Toda integração revalida lease, provenance e staleness.

## 6. Contracts & traceability

Antes de congelar solução: Case Contract + Partner Contract. Requisitos/dor/claims são rastreados em `TRACEABILITY_MATRIX`; assumptions/risks em `ASSUMPTION_RISK_REGISTER`.

## 7. Evidence

Fato, inferência, hipótese e unknown são distintos. Consenso de agentes não substitui evidência. Evidência direta do parceiro/case e fontes primárias têm prioridade quando disponíveis.

## 8. Optimization loop

```text
EVALUATE WHOLE CASE + SOLUTION
→ HARD GATE FAIL? fix first
→ IDENTIFY SUCCESS BOTTLENECK
→ RANK expected_total_success_uplift / time / risk
→ GENERATE DISPATCHES
→ PARALLEL WORK
→ SYNTHESIS / INTEGRATION
→ PARTNER JURY + RED TEAM + SCORECARDS
→ repeat
```

## 9. Deadline

Quando conhecido, registrar prazo e finalization reserve. Durante a reserva, não abrir exploração especulativa salvo hard gate/risco crítico; priorizar integração, QA, blind review e submissão.

## 10. Completion

Requer:
- `SUCCESS_STATUS: PASS` e `SUCCESS_STOP_CONDITION: PASS`;
- Partner e Quality status/stop PASS;
- traceability obrigatória completa;
- critical assumptions controladas;
- Blind Review PASS;
- todos os roadmap gates obrigatórios PASS;
- nenhum finding crítico aberto;
- nenhuma alternativa materialmente superior/viável sem avaliação;
- submission readiness PASS.

## 11. Protocol changes

Exigem bump de versão, nova decisão, justificativa e PR separado de produto.

## 12. Enforcement

`System Integrity` + `scripts/validate_system.py` validam arquivos, checkpoints, versões e completion gates. `main` deve exigir PR/check e bloquear force-push/deleção.
