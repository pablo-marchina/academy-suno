# W008-T001 — Descoberta editorial e contrato de adoção (EP-01)

**Data da pesquisa:** 2026-10-15 (America/Sao_Paulo)  
**Task/attempt:** `W008-T001-A01` / Issue [#252](https://github.com/pablo-marchina/academy-suno/issues/252)  
**Procedência imutável:** STATE `0064`, base `b8e22eca2affc0b9696087bca88603f8285c6940`  
**Continuidade observada:** STATE `0075`, `main=c150d10e1c72eb0652ffd1c55af5695fd8d104b0`; tarefa READY, comparação base→main ahead 16/behind 0, sem sobreposição com arquivos desta task.  
**Classe da evidência:** `PUBLIC_PRIMARY` + `REPOSITORY_INSPECTION` + `DESIGN_HYPOTHESIS`. **Não há** entrevistas, questionários respondidos, acesso às operações do parceiro, pilotos, validação humana, autorização de uso de conteúdo de terceiros, medições de ROI ou decisão de produção.  
**Decisão:** `NO_PREFERENCE / PENDING_PARTNER_EVIDENCE` para workflow editorial, priorização e adoção. Este documento **não é** pesquisa de satisfação nem especificação aprovada pela Suno.

## 1. Problema e pergunta de decisão

Pergunta: em quais jornadas editoriais/research/compliance uma transformação de documento financeiro em **três audiências × três formatos nativos** gera economia de esforço e qualidade defensável, sem violar independência editorial, direitos, verificação de fontes, políticas ou controles de publicação?

O case do projeto pede 9 variantes e gates factuais; isso **não comprova** que a Suno já opera 9 variantes por pauta, que usa os três formatos em todos os canais, ou que qualquer colaborador aprovou o produto.

**Unidades organizacionais não intercambiáveis (evidência externa):**

- O [Suno Notícias — Sobre](https://www.suno.com.br/noticias/sobre/) declara portal gratuito de informação financeira, equipe editorial e decisões independentes das atividades comerciais do Grupo Suno, incluindo Suno Research e Suno Asset. Isso sustenta **segregação editorial declarada publicamente**, não papéis detalhados de aprovação no CMS.
- A [linha editorial do Suno Notícias](https://www.suno.com.br/noticias/linha-editorial/) estabelece verificação prévia, distinção entre notícia e opinião e correção de erros. São princípios públicos da marca, **não** SLAs medidos ou contrato fornecido ao Academy Suno.
- A [Suno Research](https://www.suno.com.br/research/) divulga oferta de relatórios e carteiras a assinantes; conteúdo de análise/investimento é um ramo diferente de jornalismo aberto. Não presumir transferência de relatórios pagos para este projeto.
- A [CVM explica a atividade de analista](https://www.gov.br/cvm/pt-br/assuntos/regulados/consultas-por-participante/analistas-de-valores-mobiliarios): relatórios de análise sobre valores mobiliários/emissores, inclusive distribuídos a clientes, têm enquadramento profissional regulado. **A classificação jurídica de cada peça concreta requer avaliação apropriada; não classificá-la pela mera existência de IA.**

### 1.1 Matriz de evidência verificável

| ID | Classe | Fonte e afirmação limitada | Implicação / limite |
|---|---|---|---|
| P01 | PUBLIC_PRIMARY — publicação institucional | [Suno Notícias / Sobre](https://www.suno.com.br/noticias/sobre/), consultado 2026-10-15: objetivos de informação e autonomia editorial declarada | Não misturar aprovação jornalística com aprovação da casa de análise; não prova organograma vigente |
| P02 | PUBLIC_PRIMARY — política editorial pública | [Linha editorial](https://www.suno.com.br/noticias/linha-editorial/), consultado 2026-10-15: verificação, diferenciação opinião/notícia, correções | Projetar checagem/correção; não inferir workflow real ou prazos |
| P03 | PUBLIC_PRIMARY — oferta pública de produto | [Suno Research](https://www.suno.com.br/research/), consultado 2026-10-15: relatórios e carteiras de assinatura | Direitos/revisão do fluxo research são independentes e ainda desconhecidos |
| P04 | PUBLIC_PRIMARY — site editorial | [Editorias Suno Notícias](https://www.suno.com.br/noticias/), consultado 2026-10-15: matérias e categorias abertas | Evidencia saídas jornalísticas públicas; **não** evidencia carrossel/vídeo curto como entregáveis operacionais do parceiro |
| P05 | GOVERNMENT_PRIMARY — regulação | [CVM / Analistas](https://www.gov.br/cvm/pt-br/assuntos/regulados/consultas-por-participante/analistas-de-valores-mobiliarios), [orientações sobre publicidade de analistas](https://www.gov.br/cvm/pt-br/assuntos/noticias/2019-1/orientacoes-para-analistas-de-valores-mobiliarios-4773d2705983437eab40f7a0e3c45579) | Verificar caso a caso responsabilidade profissional, conflitos, comunicação de riscos, projeção/opinião |
| P06 | GOVERNMENT_PRIMARY — fontes possíveis | [CVM / Companhias](https://www.gov.br/cvm/pt-br/assuntos/regulados/consultas-por-participante/companhias) e [Portal Dados Abertos](https://www.gov.br/cvm/pt-br/acesso-a-informacao-cvm/dados-abertos) | Há documentos/dados públicos consultáveis; **acesso público não substitui licença, correção, atribuição nem aprovação de uso** |
| P07 | LEGAL_PRIMARY — texto de lei | [Lei 9.610/1998, arts. 28-29](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm) | Reutilização/adaptação/reprodução de obras exige análise de direitos/exceções; sem permissão presumida |
| P08 | LEGAL_PRIMARY — texto de lei | [LGPD compilada, arts. 4, 6, 7, 15-16](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm) | Dados pessoais exigem avaliação de finalidade, base legal e retenção; art. 4º tem hipótese para finalidade exclusivamente jornalística, **não autorização geral** para qualquer SaaS/log analítico |
| P09 | REGULATOR_GUIDANCE | [ANPD / agentes de tratamento](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-para-definicoes-dos-agentes-de-tratamento-de-dados-pessoais-e-do-encarregado) | Atribuição de controlador/operador depende do arranjo factual; não assumir que a Suno autorizou suboperadores |
| R01 | REPOSITORY_INSPECTION | `src/suno_content/domain/models.py`: `SourceProvenance`, `ProvenanceRef`, `TableCellProvenance`, `VariantSpec`, `EvalReport.protect_non_compensatory_pass` | Spine tipada e fail-closed existem no domínio de referência; não implicam processo editorial real |
| R02 | REPOSITORY_INSPECTION | `src/suno_content/ingest/adapters.py:PdfExtraction` e `src/suno_content/ingest/service.py:IngestResult,_ready_cells` | Transporte usa texto plano; células 3×3 de ingest são `MECHANICS_ONLY` — não produto/publicação |
| R03 | REPOSITORY_INSPECTION | `src/suno_content/consistency/native_bridge.py:NativeVariant,_units` + `docs/product/research/W010_T002_NATIVE_BRIDGE.md` | M05 tem verificador de ligações nativas→asserções fornecidas offline; não verifica independentemente prosa nem PDF original |
| R04 | ACCEPTED_SCOPED_RECORD | `SYSTEM/RESULTS/W007-T004-A01.md` e `docs/product/research/W008_T002_CONTRACT_INVENTORY.md` | Parser estrutural foi testado em fatia limitada; source-original ≠ produção/OCR winner |
| R05 | GOVERNANCE | `SYSTEM/PRODUCTION_CONTRACT.md`, `SYSTEM/DECISION_RESEARCH_GATE.md`, `docs/product/EVOLUTION_MASTER_PLAN.md` | Exigem 9/9, hard gates, auditoria, DRG e NÃO autorizam production-ready |

### 1.2 Busca sistemática e escopo da saturação

**Data:** 2026-10-15. Categorias pesquisadas: (a) páginas oficiais Suno `/noticias/sobre`, `/noticias/linha-editorial`, `/research`, editorias; (b) páginas oficiais CVM sobre analistas e dados de companhias; (c) legislação primária Planalto LGPD/direitos autorais; (d) ANPD sobre agentes; (e) repositório e artefatos W006/W007/W008/W010. Consultadas buscas pelas expressões “Suno Notícias linha editorial independência”, “Suno Research relatórios assinatura”, “CVM analistas relatórios Resolução 20”, “CVM dados abertos companhias”, “LGPD art. 4 6 15 16”, “Lei 9610 art 29” e “ANPD agentes tratamento”. Foram abertas fontes oficiais para confirmar escopo; material mercadológico e cobertura secundária não substituíram fonte primária.

**Stopping rule aplicado somente à fotografia documental pública:** fontes adicionais nessas categorias não esclareceriam o *real* processo interno de pauta, ferramentas, contratos e aceites; novas buscas genéricas seriam redundantes para este escopo. **Não** há saturação empírica de necessidades de usuários, mercado, política interna ou benchmarking. Reabrir com políticas/fluxos aprovados, documentos autorizados, amostra de pautas reais ou regra regulatória atualizada. Não usar informação pública para “validar” entrevistas inexistentes.

## 2. O que se observa no repositório vs. o que é desconhecido na Suno

| Dimensão | Fato atual do Academy Suno | Desconhecido externo que bloqueia contrato definitivo |
|---|---|---|
| Destinatário | Protótipo prevê `BEGINNER/INTERMEDIATE/ADVANCED × ARTICLE/CAROUSEL/SHORT_VIDEO` | Segmentos reais, gêneros, distribuição, acessibilidade e formatos aprovados |
| Pauta e seleção | Source→anchor→geração→eval/repair foi concebido | Quem cria/atribui pauta, quem define fatos primários, tolerância a urgência |
| Fontes | Há source hash, estruturas de provenance e quarantine fail-closed | Fontes licenciadas/autorizadas, acesso a documentos pagos, embargo, terceiros |
| Validação factual | Gates e checagens estruturadas offline por escopo | Quem tem dever de verificar números, projeções, citações e correções em produção |
| Aprovação | M06 é candidato no plano EP-01/EP-12 | Quem pode aprovar notícia vs análise vs publicidade e separar funções |
| Publicação | Formatos nativos são contratos internos; postagem automática está fora | CMS, canal, metadados, taxonomia, atribuição, publicação manual e rollback |
| Privacidade | Isolamento/retention são requisitos de contrato, não validação operacional | Finalidades/bases legais, retenção por classe, titulares, fornecedores permitidos |
| Valor | M12 mede esforço/retrabalho quando houver eventos | Volumes, custo interno, horas, taxa de correção, incentivos, adoção real |

### 2.1 Hipóteses de dor, **não** achados de entrevista

- **H01, A-0002 / RISK-0011:** editores podem gastar tempo substancial conferindo relações entre número, unidade, período e fonte enquanto adaptam texto; severidade/frequência **UNKNOWN**.
- **H02, A-0011:** coordenação de múltiplas variantes pode gerar repetição, divergências e retrabalho; frequência/custo **UNKNOWN**, especialmente porque saída 3×3 simultânea não está demonstrada como necessidade operacional.
- **H03, PAIN-005:** um source explorer e registro de correções podem reduzir esforço de auditoria/revisão; efeito incremental **NOT_MEASURED**.
- **H04:** riscos mais caros podem ser publicação de número/projeção incorreto, fonte desatualizada e transposição indevida de recomendação entre jornalismo e análise; ocorrência na Suno **UNKNOWN**.
- **H05:** início com “uma fonte → um artigo” pode oferecer menor custo de adoção que nove saídas; requer comparação no mesmo workload.

## 3. Contrato preliminar do parceiro (todos os campos externos ainda PENDING)

| Campo | Contrato candidato / estado |
|---|---|
| Problema operacional | Reuso editorial com verificabilidade financeira; `HYPOTHESIS_ONLY` |
| Usuários/decisores | Jornalismo (pauta/redação/edição), pesquisa/analista responsável quando aplicável, revisão jurídica/compliance conforme classe; **papéis propostos**, não proprietários confirmados |
| Organização | Separação entre editorial jornalístico e research indicada por P01; integração organizacional `UNVERIFIED` |
| Material de entrada | Documentos oficiais/dados públicos licenciados/aprovados; report proprietário/embargado somente com autorização |
| Produtos-alvo | `ARTICLE`, `CAROUSEL`, `SHORT_VIDEO` × 3 níveis = grade técnica; seleção operacional por canal `UNKNOWN` |
| Responsabilidade | Ferramenta prepara rascunhos/evidência; **responsável editorial humano externo ao sistema decide publicação**, sem alegar processo já implementado |
| Critério de sucesso | Menor tempo/ações de revisão sem regressão factual/editorial/compliance e com direitos respeitados; metas numéricas `NOT_DEFINED` |
| Volume/frequência | `NOT_OBSERVED`; evitar assumir pautas/dia, minutos por matéria ou audiência |
| Canais/dados/retention | `UNCONFIRMED`; autorização específica e tabela de retenção indispensáveis antes de tráfego real |
| Adoção/ROI | `NOT_MEASURED`; efeito a ser estimado somente sobre eventos reais pareados e custo completo |

**Condição transversal:** conteúdo “aprovado por IA” não deve ser tratado como **autorizado para publicação**. A decisão humana editorial é um gate de responsabilidade/operacional futuro, distinto do waiver do projeto que dispensa avaliadores humanos de *calibração de audiência*. A decisão D-0019 não fabrica aprovações reais.

## 4. Jornada editorial mínima proposta (MVP investigável)

`SOURCE_PROPOSED → RIGHTS_CLASSIFIED → SOURCE_ACCEPTED → FACTS_ANCHORED → DRAFTS_GENERATED → CHECKED → REVIEW_PENDING → APPROVED_FOR_EXPORT → EXPORTED_DRAFT`; eventuais correções `REJECTED/REWORK` voltam a avaliação; `REVOKED` invalida pacote/exportações pendentes. **Estados apenas desenhados, não implementados nem homologados.**

1. **Intake autorizado:** origem, URL/versão, licença/embargo, finalidade, workspace, hash, editoria, data de coleta e expiração. Sem base documental/uso permitido: `HOLD`.
2. **Verificação da fonte:** texto/trecho/página/tabela/célula vinculados; se linha/coluna/unidade/periodicidade forem ambíguas: `REVIEW_REQUIRED`, sem interpolar número.
3. **Contrato da peça:** notícia factual, opinião, conteúdo educacional, análise/recomendação ou marketing devem ter rotas/políticas diferentes; classificador só sugere e **não determina obrigação legal**.
4. **Geração delimitada:** grade 3×3 como invariante técnico quando a execução 3×3 for solicitada; permitir **visualização/seleção editorial** de subconjunto, sem fingir que 9 outputs foram aprovados ou publicados.
5. **Avaliação:** fact/source/policy/schema/provenance críticos não compensatórios; conflito entre variantes reabre a peça; IA avaliadora é diagnóstica, `human_gold_eligible=false`.
6. **Revisão de responsabilidade:** revisor autorizado confere trechos/projeções/atribuições, documenta motivo, decide recusar/aprovar **somente para exportar rascunho**. Autorização/SSO real não está sendo implementada aqui (D-0023).
7. **Export seguro:** Markdown/HTML/JSON de artigo/carrossel/roteiro, com status rascunho, fonte, revisões e policy version; CMS sandbox somente após aprovação concreta. **Sem auto-publicação**.
8. **Correção/revisão da origem:** atualização de source hash → invalida afetados, aponta claim diff e exige nova checagem/decisão humana antes de exportar versão corrigida.

**Lanes sugeridas:** `NEWS_EDITORIAL` com independência jornalística e verificação; `RESEARCH_ANALYST` com responsabilidade e restrições de relatórios de análise quando pertinentes; `MARKETING_EDUCATION` com revisão de direitos/claims. A escolha de lane é uma decisão do parceiro não inferível de P01–P09.

## 5. Portfólio M01–M12 — valor hipotético, não aprovação de features

| Cap. | Ganho/risco plausível | Recomendação de pesquisa / dependência | Evidência faltante |
|---|---|---|---|
| M01 Financial Truth | rastreio de números/periodicidade | investigar cedo; bridge a provenance existente, evitar modelo duplicado | extração fonte-original tabela/célula e custo |
| M02 Verifier | reduzir erros objetivos de fórmula/unidade | experimento offline com injeções verificáveis | taxas real de alarme/omissão por grupo |
| M03 Revision Watch | evitar republicação desatualizada | condicionar a fontes permitidas e workflow de correção | feed rights, cadence, owner |
| M04 Audience | adaptar sem apagar conceitos | IA diagnóstica sob D-0019; sem “preferência humana” | dados do destinatário, calibração externa ausente |
| M05 Consistency | evitar contradição entre variantes | usar ponte estruturada W010 como baseline bounded | 9 saídas reais originais e checagem textual |
| M06 Workspace | aprovações/comentários/citações | prototipar navegação read-only antes de workflow autorizativo | papéis reais, authz, teste com usuários |
| M07 Policy as Code | política por gênero/canal | mapear normas, não definir automaticamente política editorial | signoff de compliance/jurídico |
| M08 Evidence Passport | reprodutibilidade de revisão/correção | ensaiar manifest com redaction/rights, sem “verdade absoluta” | permissões de exportação/retention |
| M09 Benchmark Lab | comprovar incrementalidade | protocolo já preregistrado W008-T003 | execuções fonte-original e custos observados |
| M10 Adaptive Quality/Cost | economizar recursos sob gates | **adiar** decisão de roteamento até métricas e rollback | provider/quality/custo sob workload |
| M11 Editorial Exports | facilitar uso do CMS | definir arquivos draft e roundtrip, sem publicação | CMS/canal/política de integração |
| M12 Value Analytics | atribuir esforço e retrabalho | definir schema de eventos privado/consentido | baseline real, custo completo e piloto |

**Prioridade provisória de aprendizagem:** caracterizar **gênero e direitos → fonte verificável → revisão do artigo → métricas do processo → variantes adicionais se houver demanda**. É prioridade *de pesquisa*, não `LOCK` de produto; o case ainda exige 9/9 quando o fluxo 3×3 for invocado.

## 6. Alternativas ao desenho editorial (DRG preliminar, sem lock)

**Workload comparável pré-registrado, ainda não executado:** mesma seleção autorizada de documentos financeiros por source group, mesmo briefing/público/formato quando compatível, itens de complexidade variada, execução com versões/inputs/logs congelados, revisor com responsabilidade legítima se futuramente disponível; só medir sobre pares elegíveis. Resguardar `DEV/CAL/HELD_OUT`, sem vazamento entre versões de mesma fonte.

| Opção | Mecanismo | Custo/esforço | Riscos/controles | Reversibilidade |
|---|---|---|---|---|
| A0 — manual atual (counterfactual; como ocorre **UNKNOWN**) | leitura, verificação, redação, aprovação em ferramentas existentes | medição exigida; não tratar como “tempo zero” | erros manuais não estimados, auditabilidade variável | nenhuma migração |
| A1 — prompt direto + revisão | documento autorizado → único prompt → edição externa | implantação simples; tokens/turnos a medir | citações/números sem verificação estruturada; bloquear publicação automática | desligar gerador |
| A2 — anchors + checagem determinística + rascunho | source trust, claim links, saída única, gates, revisão | mais curadoria inicial; menos fricção 3×3 hipotética | falha de parser/célula; `REVIEW_REQUIRED` para lacuna | manter A0/manual ou A1 apenas fora da produção |
| A3 — 3×3 com eval, consistency e repair + revisão | grade 9/9 e evidência de ligações, sem aprovação automática | custo/latência/retrabalho 9 variantes a medir | maior complexidade, risco de falsa certeza de IA; fail-closed | desativar grade e preservar artefatos/versão |
| A4 — CMS/editor atual + checklist de fontes/contrato | sem nova geração; adicionar checklist e audit trail | baixo custo técnico, alta operação manual potencial | disciplina humana e integração; processo vigente desconhecido | remover checklist |

**Critérios antes de seleção:** 9/9 quando requerido, 0 compensação de gate crítico, licensing/retention, latência total por pauta, minutos ativos de revisão, erros críticos detectados/escapados, false positives, rounds de edição, source links completos, export válido, custo total por item aprovado, retrabalho em correções, aprendizado por usuário, manutenção e auditabilidade. **Sem pesos sintéticos, custo estimado ou winner.** A fronteira de Pareto só pode ser derivada de valores brutos comparáveis; quando ausentes, `PARETO_NOT_COMPUTABLE`.

**Reversal conditions:** se usuários operam só uma saída por pauta, reavaliar A3; se custo de ancorar excede revisão manual sem ganho de erro/retrabalho, reavaliar A2; se source rights não permitem processamento, retornar ao manual; se dados reais provarem ganho consistente sob gates, propor DRG formal e piloto limitado. Nenhuma alternativa foi rodada ou avaliada contra a Suno.

## 7. Fronteiras de direitos, compliance e retenção (triagem, não parecer jurídico)

- **Fonte:** armazenar categoria `PUBLIC_OFFICIAL`, `PUBLIC_THIRD_PARTY`, `OWNED_APPROVED`, `LICENSED`, `EMBARGOED`, `PRIVATE`, `UNKNOWN`; autorização de transformação/distribuição independente da visibilidade. A lei de direitos autorais e aviso do rodapé do site Suno exigem cautela ao reproduzir matéria alheia/P01–P08.
- **Política por gênero:** notícia verificada/opinião distinguível conforme P02; relatório de análise ou publicidade relacionada a analista requer revisão de enquadramento e comunicação de riscos/conflitos com base na CVM/P05. Não adaptar automaticamente análise para “compre agora” nem transferir recomendação comercial à redação independente.
- **Pessoais/retention:** mapear dados pessoais em fontes, prompts, comentários, eventos, export e analytics. Determinar finalidade/base legal/retention e quem decide tratamento por fluxo; verificar a exceção de finalidade *exclusivamente jornalística* da LGPD art. 4º **individualmente**; não assumir aplicabilidade/isenção universal do produto.
- **Acesso e fluxo:** não habilitar uploads públicos, não enviar documento privado a provedor não aprovado, não habilitar export/publicação não autorizados. D-0023 posterga **novas features de auth**, não altera hard gates existentes `PROD-001/014` ou bloqueio de exposição.
- **Correção:** preservar histórico de versões e motivos em registro autorizado, permitir invalidação/revisão conforme direitos/política; retenção exata, expurgo e base legal são `UNKNOWN`, não configurar “guardar para sempre”.

## 8. Métricas verificáveis e protocolo de contrafactual

**Unidade:** `approved_source_group × editorial_case × format_request × policy_version`; distinguir modo um formato de modo 3×3 completo. Evento ideal (não coletado): `source_received,source_rejected,claims_reviewed,draft_generated,gate_failed,review_opened,correction_requested,revision_submitted,approved_for_export,exported_draft,revoked`, com IDs e tempos monotônicos, sem conteúdo sensível indiscriminado. Uso futuro requer autorização, redaction e instrumentação versionada.

| Métrica raw | Definição reproduzível | Estado |
|---|---|---|
| `lead_time_to_approved_draft` | timestamp de aprovação de export − receipt da fonte, com censura de não aprovados | NOT_MEASURED |
| `active_editor_minutes` | soma de intervalos ativos de revisão com sessão válida; sem inferir a partir de tempo de parede | NOT_MEASURED |
| `rework_rounds` | número de rodadas de revisão com mudança substantiva por artefato; deduplicar retries | NOT_MEASURED |
| `critical_source_policy_errors` | ocorrências confirmadas por protocolo de auditoria de fatos, com severidade e grupo de fonte | NOT_MEASURED |
| `false_alarm_rate` | alertas refutados/alertas auditados; nunca calcular com denominador zero | NOT_MEASURED |
| `provenance_coverage` | claims materiais com vínculo resolvível de hash+trecho/tabela/célula / claims materiais avaliáveis | NOT_MEASURED |
| `editorial_rejection_rate` | rejeitados por revisão / avaliados (por gênero/lane), com motivo | NOT_MEASURED |
| `gross_tool_cost_per_approved` | soma provider + compute + armazenamento + revisões atribuíveis / rascunhos aprovados | NOT_MEASURED |
| `adoption` | usuários elegíveis que concluem jornadas reais / elegíveis com acesso, com segmentação | NOT_MEASURED |
| `revision_propagation_delay` | ciência de atualização verificada → rascunhos afetados sinalizados e reavaliados | NOT_MEASURED |

**Comparação:** atribuir documentos a opções com desenho pareado/contrabalançado que não reutilize a mesma peça de forma a contaminar julgamentos; fixar fonte, gênero, prompt, população de destino e direitos; separar grupos de origem em treino/calibração/held-out; observar contagens/medianas/p95/variabilidade, intervalos quando o tamanho permitir. **Não** estabelecer `n`, thresholds, minutos economizados ou ROI antes de elegibilidade real. Resultado de `AI-only` é `MODEL_AUTOMATED`, não satisfação humana.

**ROI somente futuro:** `benefício_líquido = (minutos_ativos_manuais − minutos_ativos_assistidos) × custo_hora_real + retrabalho_evitable_validado − (infra + licenças + revisão + integração + manutenção)`. Não atribuir causalidade sem piloto/desenho; preços, salários, volumes, taxa de falha e ROI atual são `UNKNOWN`.

## 9. Decisões pendentes, prioridades de descoberta e rastreabilidade

| Ref | Questão a resolver | Evidência necessária | Estado |
|---|---|---|---|
| `PAIN-005` | dor é quantitativamente material? | observação de tarefas, baseline, frequência e revisão | PENDING_EXTERNAL |
| `A-0002` | quem realmente usa/decide? | mapeamento de áreas e owner autorizado | OPEN_EXTERNAL |
| `A-0011` | reuso 3×3 reduz esforço? | canal real, baseline A0, piloto A2 vs A3 | OPEN_EXTERNAL |
| `RISK-0011` | como não impor processo estranho à Suno? | jornada real, gatekeepers, teste de adoção | OPEN_EXTERNAL |
| `PROD-011` | source explorer útil e seguro? | UX da fonte e revisão no caminho real | PENDING_IMPLEMENTATION/EVIDENCE |
| `PROD-014` | direitos/retention/isolamento? | autorizações e controles testados; não inferir de docs | OPEN_HARD_GATE |
| `M01/M05/M06/M07/M11/M12` | ordem e investimento? | DRG + workload editorial e compliance validados | CANDIDATES_ONLY |

**Pedidos de aprovação explicitamente não obtidos:** identificação de patrocinador, editor responsável por cada lane e consultor de compliance; lista de fontes e direitos de processamento; política de embargo/correção/arquivamento; escolha de canais/CMS e se 3×3 completo agrega valor; política de revisão/assinatura; dados mínimos de baseline e autorização para piloto. A resposta de cada área só será considerada obtida com artefato e permissão verificáveis.

**Propostas ao Orchestrator, não mudanças canônicas:** (1) registrar `EP-01 Research Discovery = documented / partner validation pending`, nunca `PARTNER_PASS`; (2) propor M06 como UX de leitura/compare apenas até papéis e autorização validarem aprovações; (3) manter A-0002, A-0011 e RISK-0011 `OPEN_EXTERNAL`; (4) abrir DRG próprio quando houver escolha material de política de revisão/CMS/workflow; (5) nenhum PRODUCTION_READY ou RELEASE com base neste estudo.

**Documento complementar:** [`W008_T001_QUESTIONNAIRE_AND_WORKFLOW.md`](W008_T001_QUESTIONNAIRE_AND_WORKFLOW.md).  
**Terminal evidence:** `SYSTEM/RESULTS/W008-T001-A01.md` após criação dos artefatos.
