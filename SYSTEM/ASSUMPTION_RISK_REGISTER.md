# ASSUMPTION & RISK REGISTER

## Assumptions

| ID | Assumption | Evidence | Impact if wrong | Uncertainty | Validation / mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| A-0001 | Para o vídeo final, a regra operacional deve ser <=5:00 apesar de o Entregável 5 mencionar “5 a 7 minutos” | E-0001: seção 7 fixa máximo de 5 min e associa critério eliminatório | CRITICAL | MEDIUM | planejar <=5:00; confirmar com organizador se houver canal | Orchestrator | CONTROLLED |
| A-0002 | O usuário interno provável é equipe de conteúdo/editorial/research, mas owner/decision maker não foram identificados | E-0002 + inferência | HIGH | HIGH | não projetar workflow final como fato; tratar persona interna como hipótese | Research | OPEN |
| A-0003 | O maior valor é `content transformation + trust layer`, não “resumidor” | E-0001,E-0002,W001 | HIGH | MEDIUM | comparar contra prompts simples/manual e medir valor incremental | Strategy | SUPPORTED_HYPOTHESIS |
| A-0004 | Níveis de sofisticação precisam de gold/calibração mensurável além de prompts | E-0001; W001-T002/T005/T009 | HIGH | LOW | criar eval dataset e labels independentes; validar separabilidade | Eval | SUPPORTED |
| A-0005 | LangGraph + Pydantic + UI leve pode ser bom trade-off inicial, mas stack final não está decidida | W001-T006/T010 | MEDIUM | MEDIUM | executar EXP-B e EXP-H; baseline plain async obrigatório | Architecture | PROVISIONAL |
| A-0006 | Não foi fornecido dataset gold/anotado pelo parceiro | briefing não contém dataset gold | HIGH | HIGH | construir pequeno golden set reproduzível e documentar limitações | Eval | OPEN |
| A-0007 | Imitação de “voz Suno” pode ser desejável, mas o briefing exige níveis, não style transfer de marca | E-0001,E-0002,W001-T001 | MEDIUM | HIGH | manter como calibração suave/opcional até evidência interna | Content | OPEN |
| A-0008 | Documentos públicos-alvo poderão ser obtidos e parseados de forma confiável suficiente para demo | E-0001,W001-T010 | HIGH | MEDIUM | executar EXP-A em 3 famílias e usar fallback/review | Data | OPEN |
| A-0009 | Flesch PT-BR requer implementação/teste controlado em vez de uso cego de biblioteca genérica | W001-T002/T009 | MEDIUM | LOW | implementar versão controlada + unit/adversarial tests | Eval | SUPPORTED |
| A-0010 | LLM/semantic judge deve ser sensor secundário e estruturado, não árbitro único | W001-T004/T009/T010 | HIGH | LOW | hard gates determinísticos/source-first; semantic ablation EXP-G | Eval | CONTROLLED_BY_DESIGN |
| A-0011 | Ganho operacional real do parceiro pode incluir tempo/retrabalho/reuso multicanal | E-0002 + inferência | HIGH | HIGH | apresentar como hipótese; não declarar ROI sem dados internos | Partner Research | OPEN |

## Risks

| ID | Risk | Likelihood | Impact | Trigger | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RISK-0001 | Alucinação ou drift factual em números, datas, entidades, direção/condicionais | HIGH | CRITICAL | claim sem source support ou anchor mismatch | deterministic anchors + claim grounding + hard fail | Eval | OPEN |
| RISK-0002 | “Gaming” das métricas: melhorar Flesch apagando conceito ou inflar densidade com jargão | HIGH | HIGH | métrica sobe enquanto cobertura/qualidade cai | métricas multidimensionais + floors + adversarial tests | Eval | OPEN |
| RISK-0003 | Avaliação circular: mesmo modelo gera e valida sem ground truth | MEDIUM | HIGH | judge concorda sistematicamente sem evidência externa | gold set + deterministic rules + source-based checks | Eval | OPEN |
| RISK-0004 | Dataset experimental pequeno/desbalanceado não generaliza | HIGH | HIGH | métricas instáveis por tipo de documento | slices por documento/audiência/formato + held-out set | Eval | OPEN |
| RISK-0005 | Retries aumentam custo/latência e podem não convergir | MEDIUM | MEDIUM | >MAX_RETRIES ou piora após repair | branch-local targeted repair + telemetry + stop criteria | Architecture | OPEN |
| RISK-0006 | Vídeo não prova funcionamento real dentro de 5 min e anula entrega técnica | MEDIUM | CRITICAL | demo roteirizada sem execução real ou duração >5 min | evidence cockpit cedo; target 4:40; fallback persistido transparente | Demo | OPEN |
| RISK-0007 | Overengineering consome tempo sem melhorar critérios | HIGH | HIGH | arquitetura sofisticada sem ganho medido | baseline plain async + EXP-B kill criterion | Orchestrator | OPEN |
| RISK-0008 | Conteúdo gerado cruza fronteira de adaptação e vira recomendação financeira nova | MEDIUM | HIGH | buy/sell/price target não presente na fonte | executable content policy + hard fail/review | Compliance | OPEN |
| RISK-0009 | Uma única função de qualidade é aplicada indevidamente a artigo/carrossel/vídeo | HIGH | MEDIUM | output passa métrica textual mas falha formato | schemas/evaluators por formato | Eval/UX | OPEN |
| RISK-0010 | Extração de PDF perde tabelas/números/rodapés e contamina todo pipeline | MEDIUM | HIGH | anchor coverage baixa | source trust + EXP-A + parser fallback/review | Data | OPEN |
| RISK-0011 | Owner/workflow interno desconhecido leva a proposta pouco adotável | MEDIUM | HIGH | solução depende de processo não evidenciado | modular adapters/configuração + partner jury | Strategy | OPEN |
| RISK-0012 | `main` permanece sem branch protection por decisão operacional do usuário | MEDIUM | MEDIUM | push direto acidental altera canônicos | CI, lease, PR discipline e checkpoints; risco aceito | Orchestrator | ACCEPTED |
| RISK-0013 | Reducer/estado paralelo perde outputs silenciosamente | MEDIUM | HIGH | fan-out/join sobrescreve branch | reducers keyed by job_id + concurrency smoke test | Architecture | OPEN |
| RISK-0014 | Formatos curtos/bullets inflam artificialmente métricas de legibilidade | HIGH | MEDIUM | Flesch melhora sem mudança cognitiva real | format slicing + ACV multidimensional | Eval | OPEN |
| RISK-0015 | Ontologia/policy envelhece e aliases/regras ficam inconsistentes | MEDIUM | MEDIUM | regressões por mudança de termo/regra | versionamento + fixtures/regression suite | Eval/Compliance | OPEN |
| RISK-0016 | Fallback persistido da demo parece conteúdo enlatado | MEDIUM | HIGH | geração live falha e provenance não é mostrado | label CACHED/PERSISTED RUN + run id/hash/timestamp + local re-eval | Demo | OPEN |
| RISK-0017 | Mudança de modelo/provider altera comportamento/custo | HIGH | MEDIUM | regressão após update/provider drift | provider abstraction + fingerprints + regression suite | Architecture | OPEN |

## Rules

- Assumptions usam `A-####`; risks usam `RISK-####`.
- Premissa de alto impacto + alta incerteza deve gerar task de validação/teste.
- Uma premissa crítica não pode desaparecer por consenso; ela só muda de status por evidência, mitigação ou decisão explícita.
- `PROJECT_STATUS: COMPLETE` exige nenhuma premissa crítica material `UNCONTROLLED`.