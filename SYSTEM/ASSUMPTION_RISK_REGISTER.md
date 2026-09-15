# ASSUMPTION & RISK REGISTER

## Assumptions

| ID | Assumption | Evidence | Impact if wrong | Uncertainty | Validation / mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| A-0001 | Para o vídeo final, a regra operacional deve ser <=5:00 apesar de o Entregável 5 mencionar “5 a 7 minutos” | E-0001 | CRITICAL | MEDIUM | planejar <=5:00; confirmar com organizador se houver canal | Orchestrator | CONTROLLED |
| A-0002 | O usuário interno provável é equipe de conteúdo/editorial/research, mas owner/decision maker não foram identificados | E-0002 + inferência | HIGH | HIGH | não projetar workflow final como fato | Research | OPEN |
| A-0003 | O maior valor é `content transformation + trust layer`, não “resumidor” | E-0001,E-0002,W001,W002 | HIGH | MEDIUM | medir incrementality contra prompt/simple/manual | Strategy | SUPPORTED_HYPOTHESIS |
| A-0004 | Níveis de sofisticação precisam de gold/calibração mensurável além de prompts | E-0001,W001,W002-T010 | HIGH | LOW | W003-T001/T004/T008: gold independente + ACV + calibration | Eval | SUPPORTED_ACTIVE_VALIDATION |
| A-0005 | Pydantic é adequado às fronteiras persistidas; orchestration final deve ser evidence-driven | W001-T006/T010; W002-T001/T005/T010 | MEDIUM | LOW-MEDIUM | plain async lidera provisoriamente; W003-T003 explicit graph/state + challenger recheck | Architecture | PLAIN_ASYNC_PROVISIONAL_LANGGRAPH_PENDING_RECHECK |
| A-0006 | Não foi fornecido dataset gold/anotado pelo parceiro | briefing não contém dataset gold | HIGH | HIGH | W003-T001 constrói benchmark independente e documenta limitações | Eval | ACTIVE_MITIGATION |
| A-0007 | Imitação de “voz Suno” pode ser desejável, mas briefing exige níveis, não style transfer de marca | E-0001,E-0002,W001-T001 | MEDIUM | HIGH | manter soft/opcional até evidência interna | Content | OPEN |
| A-0008 | Documentos públicos-alvo podem ser parseados de forma confiável suficiente para demo | W002-T002/T007/T010 | HIGH | MEDIUM | source/table-role behavior lockado; parser library só após expanded raw-byte bakeoff | Data | PARTIALLY_SUPPORTED |
| A-0009 | Flesch PT-BR requer implementação/teste controlado em vez de uso cego de biblioteca genérica | W001-T002/T009; W002-T010 | MEDIUM | LOW | W003-T004 implementação/versionamento + anti-gaming | Eval | SUPPORTED_ACTIVE_BUILD |
| A-0010 | LLM/semantic judge deve ser sensor secundário e estruturado, não árbitro único | W001-T004/T009/T010; W002-T006/T007/T010 | HIGH | LOW | hard gates determinísticos/source-first; W003-T002/T008 ablation | Eval | CONTROLLED_BY_DESIGN |
| A-0011 | Ganho operacional real do parceiro pode incluir tempo/retrabalho/reuso multicanal | E-0002 + inferência | HIGH | HIGH | telemetry/incrementality antes de declarar ROI | Partner Research | OPEN |

## Risks

| ID | Risk | Likelihood | Impact | Trigger | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RISK-0001 | Alucinação/drift factual em números, datas, entidades, direção/condicionais | HIGH | CRITICAL | claim sem source support ou anchor mismatch | factual-v001 + T007 backbone; W003-T002 claim grounding + T006 repair | Eval | CONTROLLED_FOUNDATION_CLAIM_LAYER_ACTIVE |
| RISK-0002 | Gaming: melhorar readability apagando conceito ou inflar densidade com jargão | HIGH | HIGH | métrica sobe enquanto cobertura cai | W003-T004 anti-gaming + T001 gold + T008 release gate | Eval | ACTIVE_MITIGATION |
| RISK-0003 | Avaliação circular: mesmo modelo gera e valida sem ground truth | MEDIUM | HIGH | judge concorda sem evidência externa | W003-T001 independent gold + deterministic/source checks + T008 ablation | Eval | ACTIVE_MITIGATION |
| RISK-0004 | Dataset pequeno/desbalanceado não generaliza | HIGH | HIGH | métricas instáveis por slice | source-level dev/held-out, agreement + no false threshold freeze | Eval | ACTIVE_MITIGATION |
| RISK-0005 | Retries aumentam custo/latência e não convergem | MEDIUM | MEDIUM | >stop criteria ou piora após repair | W003-T006 targeted repair + T007 telemetry | Architecture | ACTIVE_MITIGATION |
| RISK-0006 | Vídeo não prova funcionamento real <=5 min | MEDIUM | CRITICAL | demo sem execução real ou >5 min | evidence cockpit após W003; target 4:40 | Demo | OPEN |
| RISK-0007 | Overengineering consome tempo sem melhorar critérios | LOW-MEDIUM | HIGH | framework sofisticado sem ganho | D-0016; plain async leader; challenger evidence only | Orchestrator | REDUCED |
| RISK-0008 | Conteúdo cruza adaptação e vira recomendação financeira nova | MEDIUM | HIGH | recommendation nova/personalização | canonical policy hard gates + provenance; revalidar end-to-end | Compliance | CONTROLLED_FOUNDATION |
| RISK-0009 | Uma função de qualidade é aplicada indevidamente a todos os formatos | LOW-MEDIUM | MEDIUM | texto passa, mídia falha | native format contracts + format slicing/calibration | Eval/UX | CONTROLLED_FOUNDATION |
| RISK-0010 | Extração PDF perde tabelas/números/rodapés | MEDIUM | HIGH | source-trust baixa | source/table-role behavior gate; parser lock pending expanded replay | Data | CONTROLLED_PARTIAL |
| RISK-0011 | Owner/workflow interno desconhecido leva a proposta pouco adotável | MEDIUM | HIGH | solução depende de processo não evidenciado | modular adapters + partner jury | Strategy | OPEN |
| RISK-0012 | `main` sem branch protection por decisão do usuário | MEDIUM | MEDIUM | push direto acidental | CI, lease, PR discipline, checkpoints | Orchestrator | ACCEPTED |
| RISK-0013 | Estado paralelo perde outputs silenciosamente | MEDIUM | HIGH | join sobrescreve branch | keyed job identity + W003-T003 RunStore/graph tests | Architecture | ACTIVE_MITIGATION |
| RISK-0014 | Formatos curtos inflam readability artificialmente | HIGH | MEDIUM | Flesch sobe sem mudança cognitiva | W003-T004 format-aware features + T008 anti-gaming | Eval | ACTIVE_MITIGATION |
| RISK-0015 | Ontologia/policy envelhece e aliases/regras divergem | MEDIUM | MEDIUM | regressão por mudança | versionamento + fixtures/regression | Eval/Compliance | OPEN |
| RISK-0016 | Fallback persistido da demo parece conteúdo enlatado | MEDIUM | HIGH | live generation falha sem provenance | label persisted run + run/hash/timestamp + local re-eval | Demo | OPEN |
| RISK-0017 | Mudança de model/provider altera comportamento/custo | HIGH | MEDIUM | provider drift | provider abstraction + fingerprints + regression; no provider lock yet | Architecture | OPEN |
| RISK-0018 | Componentes W002 passam isoladamente mas falham em clean combined checkout | MEDIUM | HIGH | import/schema/CI integration failure | W003-T005 clean-checkout foundation CI | Auditor | ACTIVE_MITIGATION |

## Rules

- Assumptions usam `A-####`; risks usam `RISK-####`.
- Premissa de alto impacto + alta incerteza deve gerar task de validação/teste.
- Uma premissa crítica não pode desaparecer por consenso; só muda por evidência, mitigação ou decisão explícita.
- `PROJECT_STATUS: COMPLETE` exige nenhuma premissa crítica material `UNCONTROLLED`.
