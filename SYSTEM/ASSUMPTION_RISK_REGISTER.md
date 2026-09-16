# ASSUMPTION & RISK REGISTER

## Assumptions

| ID | Assumption | Evidence | Impact if wrong | Uncertainty | Validation / mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| A-0001 | Para o vídeo final, a regra operacional deve ser <=5:00 apesar de o Entregável 5 mencionar “5 a 7 minutos” | E-0001 | CRITICAL | MEDIUM | planejar <=5:00; confirmar com organizador se houver canal | Orchestrator | CONTROLLED |
| A-0002 | O usuário interno provável é equipe de conteúdo/editorial/research, mas owner/decision maker não foram identificados | E-0002 + inferência | HIGH | HIGH | não projetar workflow final como fato | Research | OPEN |
| A-0003 | O maior valor é `content transformation + trust layer`, não “resumidor” | E-0001,E-0002,W001,W002,W003-T002/T003/T006/T007/T008 | HIGH | MEDIUM | medir incrementality contra prompt/simple/manual | Strategy | SUPPORTED_HYPOTHESIS |
| A-0004 | Níveis de sofisticação precisam de gold/calibração mensurável além de prompts | W003-T001/T004/T008 | HIGH | LOW | calibration gate existe; thresholds permanecem DIAGNOSTIC_ONLY até human gold/agreement suficientes | Eval | SUPPORTED_GATE_PROVEN_THRESHOLD_OPEN |
| A-0005 | Pydantic é adequado às fronteiras persistidas; orchestration final deve ser evidence-driven | W002;W003-T003 | MEDIUM | LOW | plain async lidera com explicit graph/state proof; LangGraph challenger ainda runtime-unavailable | Architecture | PLAIN_ASYNC_PROVISIONAL_LANGGRAPH_PENDING_RECHECK |
| A-0006 | Não foi fornecido dataset gold/anotado pelo parceiro | briefing; W003-T001/T008 | HIGH | HIGH | gold-v001 n=3 e sem independent human labels/agreement; não congelar thresholds nem usar target como gold | Eval | PARTIALLY_MITIGATED_HUMAN_GOLD_OPEN |
| A-0007 | Imitação de “voz Suno” pode ser desejável, mas briefing exige níveis, não style transfer de marca | E-0001,E-0002,W001-T001 | MEDIUM | HIGH | manter soft/opcional até evidência interna | Content | OPEN |
| A-0008 | Documentos públicos-alvo podem ser parseados de forma confiável suficiente para demo | W002-T002/T007/T010 | HIGH | MEDIUM | source/table-role behavior lockado; parser library só após expanded raw-byte bakeoff | Data | PARTIALLY_SUPPORTED |
| A-0009 | Flesch PT-BR requer implementação/teste controlado em vez de uso cego de biblioteca genérica | W003-T004/T008 | MEDIUM | LOW | `ptbr-readability-v001` + tests + anti-gaming gate; thresholds permanecem diagnósticos | Eval | SUPPORTED_IMPLEMENTED |
| A-0010 | LLM/semantic judge deve ser sensor secundário e estruturado, não árbitro único | W003-T002/T006/T008 | HIGH | LOW | hard-gate non-compensation executável; semantic value segue NOT_RUN até development gold válido | Eval | CONTROLLED_BY_DESIGN |
| A-0011 | Ganho operacional real do parceiro pode incluir tempo/retrabalho/reuso multicanal | E-0002 + inferência; W003-T007 instrumentação | HIGH | HIGH | telemetry real/incrementality antes de declarar ROI; synthetic pricing não conta | Partner Research | OPEN_INSTRUMENTED |

## Risks

| ID | Risk | Likelihood | Impact | Trigger | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RISK-0001 | Alucinação/drift factual em números, datas, entidades, direção/condicionais | HIGH | CRITICAL | claim sem source support | factual backbone + claim grounding + fresh source/factual/policy re-eval after repair | Eval | STRONGLY_CONTROLLED_CORE |
| RISK-0002 | Gaming: melhorar readability apagando conceito ou inflar densidade com jargão | HIGH | HIGH | métrica sobe enquanto cobertura cai | mandatory anti-gaming gate em T008 + T004 fixtures | Eval | STRONGLY_REDUCED_GATE_PASS |
| RISK-0003 | Avaliação circular: mesmo modelo gera e valida sem ground truth | MEDIUM | HIGH | target/prediction vira gold | target≠human gold separation + held-out rejection + deterministic/source checks | Eval | STRONGLY_REDUCED_HUMAN_GOLD_OPEN |
| RISK-0004 | Dataset pequeno/desbalanceado não generaliza | HIGH | HIGH | métricas instáveis por slice | source-level split; n=3 explícito; NOT_COMPUTABLE semantics; no threshold freeze | Eval | OPEN_CONTROLLED_NO_OVERCLAIM |
| RISK-0005 | Retries aumentam custo/latência e não convergem | MEDIUM | MEDIUM | >stop criteria ou piora após repair | targeted repair bounded stops + separate retry/repair telemetry | Architecture | STRONGLY_REDUCED_CORE |
| RISK-0006 | Vídeo não prova funcionamento real <=5 min | MEDIUM | CRITICAL | demo sem execução real ou >5 min | evidence cockpit após W003; target 4:40 | Demo | OPEN |
| RISK-0007 | Overengineering consome tempo sem melhorar critérios | LOW | HIGH | framework sofisticado sem ganho | plain async explicit graph/state proof; no LangGraph lock | Orchestrator | REDUCED |
| RISK-0008 | Conteúdo cruza adaptação e vira recomendação financeira nova | MEDIUM | HIGH | recommendation nova/personalização | canonical policy hard gates + HybridDecision + post-repair re-eval | Compliance | CONTROLLED_CORE |
| RISK-0009 | Uma função de qualidade é aplicada indevidamente a todos os formatos | LOW-MEDIUM | MEDIUM | texto passa, mídia falha | native format contracts + format slicing/calibration gate | Eval/UX | CONTROLLED_FOUNDATION |
| RISK-0010 | Extração PDF perde tabelas/números/rodapés | MEDIUM | HIGH | source-trust baixa | source/table-role behavior gate; parser lock pending expanded replay | Data | CONTROLLED_PARTIAL |
| RISK-0011 | Owner/workflow interno desconhecido leva a proposta pouco adotável | MEDIUM | HIGH | solução depende de processo não evidenciado | modular adapters + partner jury | Strategy | OPEN |
| RISK-0012 | `main` sem branch protection por decisão do usuário | MEDIUM | MEDIUM | push direto acidental | CI, lease, PR discipline, checkpoints | Orchestrator | ACCEPTED |
| RISK-0013 | Estado paralelo perde outputs silenciosamente | LOW-MEDIUM | HIGH | join sobrescreve branch | keyed job identity + explicit graph/RunStore proof 9/9 | Architecture | STRONGLY_REDUCED |
| RISK-0014 | Formatos curtos inflam readability artificialmente | HIGH | MEDIUM | readability sobe sem mudança cognitiva | multidimensional ACV + mandatory sentence-chopping/acronym/concept-deletion anti-gaming gate | Eval | STRONGLY_REDUCED_GATE_PASS |
| RISK-0015 | Ontologia/policy envelhece e aliases/regras divergem | MEDIUM | MEDIUM | regressão por mudança | versionamento + fixtures + clean regression | Eval/Compliance | CONTROLLED_PARTIAL |
| RISK-0016 | Fallback persistido da demo parece conteúdo enlatado | MEDIUM | HIGH | live generation falha sem provenance | label persisted run + run/hash/timestamp + local re-eval | Demo | OPEN |
| RISK-0017 | Mudança de model/provider altera comportamento/custo | HIGH | MEDIUM | provider drift | provider-neutral telemetry + explicit N/A + no-preference release gate until measured evidence | Architecture | REDUCED_OBSERVABILITY_OPEN_PROVIDER |
| RISK-0018 | Componentes passam isoladamente mas falham em clean combined checkout | LOW | HIGH | import/schema/CI integration failure | Foundation Regression + System Integrity gates | Auditor | CONTROLLED_CORE |
| RISK-0019 | Custo sintético de demo ser confundido com custo real | MEDIUM | HIGH | synthetic pricing aparece sem provenance | T008 kill criterion `SYNTHETIC_PRICING_PRESENTED_AS_PROVIDER_COST`; real cost exige usage completo + pricing versionado | Orchestrator | STRONGLY_CONTROLLED |
| RISK-0020 | Ausência de human gold ser mascarada por confusion matrix circular | MEDIUM | HIGH | requested target usado como truth | T008 separa target→human de human→evaluator e retorna NOT_COMPUTABLE sem labels válidos | Eval | CONTROLLED_BY_GATE |

## Rules

- Assumptions usam `A-####`; risks usam `RISK-####`.
- Premissa de alto impacto + alta incerteza deve gerar task de validação/teste.
- Uma premissa crítica não pode desaparecer por consenso; só muda por evidência, mitigação ou decisão explícita.
- `PROJECT_STATUS: COMPLETE` exige nenhuma premissa crítica material `UNCONTROLLED`.
