# ASSUMPTION & RISK REGISTER

## Assumptions

| ID | Assumption | Evidence | Impact if wrong | Uncertainty | Validation / mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| A-0001 | Para o vídeo final, a regra operacional deve ser <=5:00 apesar de o Entregável 5 mencionar “5 a 7 minutos” | E-0001 | CRITICAL | MEDIUM | planejar <=5:00; confirmar com organizador se houver canal | Orchestrator | CONTROLLED |
| A-0002 | O usuário interno provável é equipe de conteúdo/editorial/research, mas owner/decision maker não foram identificados | E-0002 + inferência | HIGH | HIGH | não projetar workflow final como fato | Research | OPEN |
| A-0003 | O maior valor é `content transformation + trust layer`, não “resumidor” | E-0001,E-0002,W001,W002,W003-T002/T003 | HIGH | MEDIUM | medir incrementality contra prompt/simple/manual | Strategy | SUPPORTED_HYPOTHESIS |
| A-0004 | Níveis de sofisticação precisam de gold/calibração mensurável além de prompts | W003-T001/T004 | HIGH | LOW | gold protocol + ACV existem; T008 calibra sem usar held-out | Eval | SUPPORTED_DIAGNOSTIC_ONLY |
| A-0005 | Pydantic é adequado às fronteiras persistidas; orchestration final deve ser evidence-driven | W002;W003-T003 | MEDIUM | LOW | plain async lidera com explicit graph/state proof; LangGraph challenger ainda runtime-unavailable | Architecture | PLAIN_ASYNC_PROVISIONAL_LANGGRAPH_PENDING_RECHECK |
| A-0006 | Não foi fornecido dataset gold/anotado pelo parceiro | briefing; W003-T001 | HIGH | HIGH | gold-v001 criado, mas n=3/sem independent human agreement impede threshold freeze | Eval | PARTIALLY_MITIGATED |
| A-0007 | Imitação de “voz Suno” pode ser desejável, mas briefing exige níveis, não style transfer de marca | E-0001,E-0002,W001-T001 | MEDIUM | HIGH | manter soft/opcional até evidência interna | Content | OPEN |
| A-0008 | Documentos públicos-alvo podem ser parseados de forma confiável suficiente para demo | W002-T002/T007/T010 | HIGH | MEDIUM | source/table-role behavior lockado; parser library só após expanded raw-byte bakeoff | Data | PARTIALLY_SUPPORTED |
| A-0009 | Flesch PT-BR requer implementação/teste controlado em vez de uso cego de biblioteca genérica | W003-T004 | MEDIUM | LOW | `ptbr-readability-v001` + tests; thresholds permanecem diagnósticos | Eval | SUPPORTED_IMPLEMENTED |
| A-0010 | LLM/semantic judge deve ser sensor secundário e estruturado, não árbitro único | W003-T002 | HIGH | LOW | HybridDecision preserva hard-gate precedence; T008 mede valor incremental | Eval | CONTROLLED_BY_DESIGN |
| A-0011 | Ganho operacional real do parceiro pode incluir tempo/retrabalho/reuso multicanal | E-0002 + inferência | HIGH | HIGH | T007 telemetry/incrementality antes de declarar ROI | Partner Research | OPEN |

## Risks

| ID | Risk | Likelihood | Impact | Trigger | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RISK-0001 | Alucinação/drift factual em números, datas, entidades, direção/condicionais | HIGH | CRITICAL | claim sem source support | factual backbone + W003 claim grounding; T006 re-eval após repair | Eval | CONTROLLED_CORE_REPAIR_PENDING |
| RISK-0002 | Gaming: melhorar readability apagando conceito ou inflar densidade com jargão | HIGH | HIGH | métrica sobe enquanto cobertura cai | W003-T004 anti-gaming + T001 gold + T008 release gate | Eval | REDUCED_CALIBRATION_PENDING |
| RISK-0003 | Avaliação circular: mesmo modelo gera e valida sem ground truth | MEDIUM | HIGH | judge concorda sem evidência externa | independent gold protocol + deterministic/source checks + T008 ablation | Eval | REDUCED_AGREEMENT_PENDING |
| RISK-0004 | Dataset pequeno/desbalanceado não generaliza | HIGH | HIGH | métricas instáveis por slice | source-level split; explicit n=3 limitation; no threshold freeze | Eval | OPEN_CONTROLLED_NO_OVERCLAIM |
| RISK-0005 | Retries aumentam custo/latência e não convergem | MEDIUM | MEDIUM | >stop criteria ou piora após repair | graph separates transport retry/quality repair; T006/T007 next | Architecture | CONTROLLED_PARTIAL |
| RISK-0006 | Vídeo não prova funcionamento real <=5 min | MEDIUM | CRITICAL | demo sem execução real ou >5 min | evidence cockpit após W003; target 4:40 | Demo | OPEN |
| RISK-0007 | Overengineering consome tempo sem melhorar critérios | LOW | HIGH | framework sofisticado sem ganho | plain async explicit graph/state proof; no LangGraph lock | Orchestrator | REDUCED |
| RISK-0008 | Conteúdo cruza adaptação e vira recomendação financeira nova | MEDIUM | HIGH | recommendation nova/personalização | canonical policy hard gates + HybridDecision | Compliance | CONTROLLED_CORE |
| RISK-0009 | Uma função de qualidade é aplicada indevidamente a todos os formatos | LOW-MEDIUM | MEDIUM | texto passa, mídia falha | native format contracts + format slicing/calibration | Eval/UX | CONTROLLED_FOUNDATION |
| RISK-0010 | Extração PDF perde tabelas/números/rodapés | MEDIUM | HIGH | source-trust baixa | source/table-role behavior gate; parser lock pending expanded replay | Data | CONTROLLED_PARTIAL |
| RISK-0011 | Owner/workflow interno desconhecido leva a proposta pouco adotável | MEDIUM | HIGH | solução depende de processo não evidenciado | modular adapters + partner jury | Strategy | OPEN |
| RISK-0012 | `main` sem branch protection por decisão do usuário | MEDIUM | MEDIUM | push direto acidental | CI, lease, PR discipline, checkpoints | Orchestrator | ACCEPTED |
| RISK-0013 | Estado paralelo perde outputs silenciosamente | LOW-MEDIUM | HIGH | join sobrescreve branch | keyed job identity + explicit graph/RunStore proof 9/9 | Architecture | STRONGLY_REDUCED |
| RISK-0014 | Formatos curtos inflam readability artificialmente | HIGH | MEDIUM | readability sobe sem mudança cognitiva | multidimensional ACV + anti-gaming; T008 calibration | Eval | REDUCED_CALIBRATION_PENDING |
| RISK-0015 | Ontologia/policy envelhece e aliases/regras divergem | MEDIUM | MEDIUM | regressão por mudança | versionamento + fixtures + clean regression | Eval/Compliance | CONTROLLED_PARTIAL |
| RISK-0016 | Fallback persistido da demo parece conteúdo enlatado | MEDIUM | HIGH | live generation falha sem provenance | label persisted run + run/hash/timestamp + local re-eval | Demo | OPEN |
| RISK-0017 | Mudança de model/provider altera comportamento/custo | HIGH | MEDIUM | provider drift | provider abstraction + fingerprints + regression; no provider lock yet | Architecture | OPEN |
| RISK-0018 | Componentes passam isoladamente mas falham em clean combined checkout | LOW | HIGH | import/schema/CI integration failure | W003-T005 clean-checkout Foundation Regression + System Integrity PASS | Auditor | CONTROLLED_CORE |

## Rules

- Assumptions usam `A-####`; risks usam `RISK-####`.
- Premissa de alto impacto + alta incerteza deve gerar task de validação/teste.
- Uma premissa crítica não pode desaparecer por consenso; só muda por evidência, mitigação ou decisão explícita.
- `PROJECT_STATUS: COMPLETE` exige nenhuma premissa crítica material `UNCONTROLLED`.
