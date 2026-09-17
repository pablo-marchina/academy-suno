# ASSUMPTION & RISK REGISTER

## Assumptions

| ID | Assumption | Evidence | Impact if wrong | Uncertainty | Validation / mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| A-0001 | Para o vídeo final, a regra operacional deve ser <=5:00 apesar de o Entregável 5 mencionar “5 a 7 minutos” | E-0001 | CRITICAL | MEDIUM | planejar <=5:00; confirmar com organizador se houver canal | Orchestrator | CONTROLLED |
| A-0002 | O usuário interno provável é equipe de conteúdo/editorial/research, mas owner/decision maker não foram identificados | E-0002 + inferência | HIGH | HIGH | não projetar workflow final como fato | Research | OPEN |
| A-0003 | O maior valor é `content transformation + trust layer`, não “resumidor” | E-0001,E-0002,W001,W002,W003 | HIGH | MEDIUM | medir incrementality contra prompt/simple/manual em representative runs | Strategy | SUPPORTED_HYPOTHESIS |
| A-0004 | Níveis de sofisticação precisam de gold/calibração mensurável além de prompts | W003-T001/T004/T008/T009 | HIGH | LOW | calibration gate existe; W004 busca human gold/agreement | Eval | SUPPORTED_GATE_PROVEN_THRESHOLD_OPEN |
| A-0005 | Pydantic é adequado às fronteiras persistidas; orchestration final deve ser evidence-driven | W002;W003-T003/T009 | MEDIUM | LOW | plain async executou E2E mechanics; LangGraph challenger é opcional/non-blocking | Architecture | PLAIN_ASYNC_PROVISIONAL_EVIDENCE_LEADER |
| A-0006 | Não foi fornecido dataset gold/anotado pelo parceiro | briefing; W003-T001/T008/T009 | HIGH | HIGH | W004-T002/T005 cria representative independent human evidence; held-out protegido | Eval | PARTIALLY_MITIGATED_HUMAN_GOLD_OPEN |
| A-0007 | Imitação de “voz Suno” pode ser desejável, mas briefing exige níveis, não style transfer de marca | E-0001,E-0002,W001-T001 | MEDIUM | HIGH | manter soft/opcional até evidência interna | Content | OPEN |
| A-0008 | Documentos públicos-alvo podem ser parseados de forma confiável suficiente para demo | W002-T002/T007/T010;W003-T009 | HIGH | MEDIUM | behavior contract + W004-T003 expanded parser/source bakeoff | Data | PARTIALLY_SUPPORTED_W004_VALIDATION |
| A-0009 | Flesch PT-BR requer implementação/teste controlado em vez de uso cego de biblioteca genérica | W003-T004/T008 | MEDIUM | LOW | `ptbr-readability-v001` + tests + anti-gaming gate; thresholds diagnósticos | Eval | SUPPORTED_IMPLEMENTED |
| A-0010 | LLM/semantic judge deve ser sensor secundário e estruturado, não árbitro único | W003-T002/T006/T008/T009 | HIGH | LOW | hard-gate non-compensation executável; W004-T006 mede valor incremental | Eval | CONTROLLED_BY_DESIGN |
| A-0011 | Ganho operacional real do parceiro pode incluir tempo/retrabalho/reuso multicanal | E-0002 + inferência; W003 telemetry/mechanics | HIGH | HIGH | real provider + cockpit + baseline comparison antes de ROI claim | Partner Research | OPEN_INSTRUMENTED |

## Risks

| ID | Risk | Likelihood | Impact | Trigger | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RISK-0001 | Alucinação/drift factual em números, datas, entidades, direção/condicionais | HIGH | CRITICAL | claim sem source support | factual backbone + claim grounding + fresh source/factual/policy re-eval after repair | Eval | STRONGLY_CONTROLLED_CORE |
| RISK-0002 | Gaming: melhorar readability apagando conceito ou inflar densidade com jargão | HIGH | HIGH | métrica sobe enquanto cobertura cai | mandatory anti-gaming gate + human calibration downstream | Eval | STRONGLY_REDUCED_GATE_PASS |
| RISK-0003 | Avaliação circular: mesmo modelo gera e valida sem ground truth | MEDIUM | HIGH | target/prediction vira gold | target≠human separation + held-out rejection + W004 human gold | Eval | STRONGLY_REDUCED_HUMAN_GOLD_OPEN |
| RISK-0004 | Dataset pequeno/desbalanceado não generaliza | HIGH | HIGH | métricas instáveis por slice | W004 representative corpus + source-level split + no threshold freeze | Eval | ACTIVE_W004_CRITICAL |
| RISK-0005 | Retries aumentam custo/latência e não convergem | MEDIUM | MEDIUM | >stop criteria ou piora após repair | targeted repair bounded stops + separate telemetry; real-model evidence W004 | Architecture | STRONGLY_REDUCED_CORE_REAL_MODEL_OPEN |
| RISK-0006 | Vídeo não prova funcionamento real <=5 min | MEDIUM | CRITICAL | demo sem execução real ou >5 min | W004 cockpit + release proof; target 4:40 | Demo | OPEN_W004_RELEASE |
| RISK-0007 | Overengineering consome tempo sem melhorar critérios | LOW | HIGH | framework sofisticado sem ganho | no framework rewrite; plain async evidence leader | Orchestrator | REDUCED |
| RISK-0008 | Conteúdo cruza adaptação e vira recomendação financeira nova | MEDIUM | HIGH | recommendation nova/personalização | canonical policy hard gates + post-repair re-eval | Compliance | CONTROLLED_CORE |
| RISK-0009 | Uma função de qualidade é aplicada indevidamente a todos os formatos | LOW-MEDIUM | MEDIUM | texto passa, mídia falha | native format contracts + format slicing + human calibration | Eval/UX | CONTROLLED_FOUNDATION |
| RISK-0010 | Extração PDF perde tabelas/números/rodapés | MEDIUM | HIGH | source-trust baixa | behavior gate + W004-T003 expanded source bakeoff | Data | ACTIVE_W004_BAKEOFF |
| RISK-0011 | Owner/workflow interno desconhecido leva a proposta pouco adotável | MEDIUM | HIGH | solução depende de processo não evidenciado | modular adapters + partner jury | Strategy | OPEN |
| RISK-0012 | `main` sem branch protection por decisão do usuário | MEDIUM | MEDIUM | push direto acidental | CI, lease, PR discipline, checkpoints | Orchestrator | ACCEPTED |
| RISK-0013 | Estado paralelo perde outputs silenciosamente | LOW | HIGH | join sobrescreve branch | keyed job identity + W003 E2E 9/9 lossless join + RunStore reopen/resume | Architecture | STRONGLY_CONTROLLED_E2E |
| RISK-0014 | Formatos curtos inflam readability artificialmente | HIGH | MEDIUM | readability sobe sem mudança cognitiva | ACV + anti-gaming + human calibration | Eval | STRONGLY_REDUCED_GATE_PASS |
| RISK-0015 | Ontologia/policy envelhece e aliases/regras divergem | MEDIUM | MEDIUM | regressão por mudança | versionamento + fixtures + clean regression | Eval/Compliance | CONTROLLED_PARTIAL |
| RISK-0016 | Fallback persistido da demo parece conteúdo enlatado | MEDIUM | HIGH | live generation falha sem provenance | cockpit labels persisted run + run/hash/timestamp + release packet | Demo | OPEN_W004_COCKPIT |
| RISK-0017 | Mudança de model/provider altera comportamento/custo | HIGH | MEDIUM | provider drift | provider-neutral telemetry + W004 real provider runs/comparison | Architecture | ACTIVE_W004_PROVIDER |
| RISK-0018 | Componentes passam isoladamente mas falham em clean combined checkout | LOW-MEDIUM | HIGH | task-specific integration não executa em release CI | Foundation/System Integrity pass; W004-T008 deve incluir W003/W004 E2E test em clean release gate | Auditor | CONTROLLED_CORE_RELEASE_GATE_PENDING |
| RISK-0019 | Custo sintético de demo ser confundido com custo real | MEDIUM | HIGH | synthetic pricing aparece sem provenance | real cost exige observed usage + versioned pricing; cockpit deve mostrar N/A | Orchestrator | STRONGLY_CONTROLLED |
| RISK-0020 | Ausência de human gold ser mascarada por confusion matrix circular | MEDIUM | HIGH | requested target usado como truth | T008 returns NOT_COMPUTABLE; W004-T005 requires independent labels/agreement | Eval | CONTROLLED_BY_GATE_W004_OPEN |
| RISK-0021 | Mechanics proof ser confundido com provider/model-quality ou production-readiness proof | MEDIUM | CRITICAL | deterministic stub usado em claim externo | explicit MECHANICS_ONLY classification + cockpit evidence states + W004-T008 release gate | Orchestrator | ACTIVE_W004_CRITICAL |

## Rules

- Assumptions usam `A-####`; risks usam `RISK-####`.
- Premissa de alto impacto + alta incerteza deve gerar task de validação/teste.
- Uma premissa crítica não pode desaparecer por consenso; só muda por evidência, mitigação ou decisão explícita.
- `PROJECT_STATUS: COMPLETE` exige nenhuma premissa crítica material `UNCONTROLLED`.
