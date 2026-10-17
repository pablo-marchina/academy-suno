# W008-T001 — Questionário e workflow editorial propostos

**Identidade:** W008-T001-A01 / Issue #252 • **Data:** 2026-10-15 • **Classificação:** PROPOSED_NOT_VALIDATED.

Este instrumento complementa [a descoberta do parceiro](W008_T001_PARTNER_DISCOVERY.md). **Nenhuma pergunta foi enviada, respondida ou validada pela Suno.** Não há entrevistas, participantes, avaliadores humanos ou aprovações fictícias. Respostas geradas por IA não contam como resposta do parceiro nem como HUMAN_GOLD. A licença/uso de fontes, autoridade profissional e retenção seguem UNKNOWN até prova autêntica.

## 1. Protocolo de coleta e proveniência

Quando autorizado, registrar para cada resposta: question_id; respondent_role; authority_scope; evidence_document_ref; answered_at; applicable_business_line; policy_version; allowed_use; redaction_status. Não colocar nomes, contatos privados ou respostas sensíveis no GitHub público. Uma afirmação do portal público da Suno é PUBLIC_SIGNAL_ONLY, não valida política interna.

Estados possíveis por resposta: UNKNOWN (atual em todas as perguntas); PUBLIC_SIGNAL_ONLY; PARTNER_ANSWERED_UNVERIFIED; PARTNER_CONFIRMED_WITH_SCOPE; CONFLICTING; NOT_APPLICABLE. “Não sei”, ausência de contato e “não autorizado” não se convertem em “sim”.

## 2. Perguntas de descoberta ordenadas por risco/decisão

| ID | Pergunta a um representante com competência | Artefato mínimo para confirmar | Sem resposta |
|---|---|---|---|
| Q01 Produto | Notícias, Research assinada, material educativo e comunicações comerciais têm quais fluxos independentes? | escopo por business line autorizado | manter lanes separadas |
| Q02 Responsabilidades | Que função inicia pauta, valida fonte, revisa, aprova rascunho, autoriza publicação e corrige? | matriz de papéis e poderes por tipo de conteúdo | não habilitar workflow de aprovação |
| Q03 Contrafactual | Quais etapas, ferramentas, filas, fontes e checkpoints compõem uma pauta manual atual? | mapa do processo com exemplos anonimizados | baseline manual UNKNOWN |
| Q04 Escala | Qual o volume e a distribuição de pautas, revisões, urgências e entregáveis por janela observada? | contagens brutas e período | sem SLA e ROI |
| Q05 Independência | Como notícias mantêm independência de Research, Asset, patrocínios e recomendações? | política/autoridade por lane | bloquear transferência entre linhas |
| Q06 Formatos | São realmente necessários artigos, carrosséis e roteiros curtos, com três públicos para toda fonte? | canais, frequência e entregáveis aprovados | grade 3×3 apenas contrato técnico |
| Q07 Público | Como definem iniciante, intermediário e avançado, conceitos obrigatórios e linguagem? | taxonomia editorial versionada | audiência apenas diagnóstica |
| Q08 Fontes | Quais filings oficiais, releases, fontes próprias, assinaturas e terceiros são permitidos? | allowlist com classe/licença | fontes não confirmadas em HOLD |
| Q09 Direitos | Quais operações são permitidas por fonte: consultar, armazenar, resumir, enviar a LLM, adaptar, redistribuir? | base contratual/licença e finalidade | não presumir reprodução |
| Q10 Embargos | Quem marca fonte embargada, qual controle de revisão e correção de origem? | regra de embargo/retificação | não ativar revision watch |
| Q11 Finanças | Quem valida unidade, período, linha de tabela, denominadores, guidance, estimativas e ressalvas? | checklist e autoridade técnica | conflito vira REVIEW_REQUIRED |
| Q12 Regulação | Como distinguem notícia/opinião/relatório de analista/promoção e divulgam riscos/conflitos? | política de conteúdo por gênero | não automatizar recomendação |
| Q13 Voz | Qual estilo e terminologia aprovados e quais claims jamais podem ser omitidos? | guia editorial versionado | não alegar imitar estilo Suno |
| Q14 Aceite | Quais evidências tornam texto apto a exportar e quais motivos impedem aprovação? | critérios e registro de decisão | estado DRAFT_ONLY |
| Q15 Retificação | Quem invalida uma peça, pede retratação e determina reavaliação derivada? | política de correção e exemplos permitidos | não afirmar rollback operacional |
| Q16 CMS | Quais canais, schemas de export, permissões, sandbox e roundtrip necessários? | contrato técnico com autorização | apenas draft offline |
| Q17 Privacidade | Qual finalidade, base legal, classe de dados, fornecedor e retenção de cada input, comentário e telemetria? | registro de tratamento/política de retenção | nenhum input confidencial |
| Q18 Isolamento | Que roles/workspaces podem ver fontes, drafts, números, eventos e artefatos? | matriz autorizativa com casos negativos | não habilitar acesso multiusuário público |
| Q19 Economia | Quais custos reais de revisão, licenças, geração, retrabalho e manutenção existem? | registro com unidades/períodos | ROI NOT_COMPUTABLE |
| Q20 Métricas | Qual melhoria tem valor para o parceiro e qual condição faria abandonar ou reduzir o piloto? | objetivos, denominadores e gatilhos acordados | não definir pesos/targets |
| Q21 Custódia | Quem guarda source-original e versões de aprovação; quando exclui o que não deve persistir? | política por classe/finalidade | retenção UNKNOWN |
| Q22 IA | Que decisões jamais podem ser delegadas ao assistente, inclusive revisão jurídica/editorial? | declaração/política por lane | IA só prepara, nunca assina/publica |

As perguntas não devem ser apresentadas como entrevista realizada. Fonte pública: [Suno Notícias — Sobre](https://www.suno.com.br/noticias/sobre/) declara autonomia editorial; [Linha editorial](https://www.suno.com.br/noticias/linha-editorial/) declara verificação prévia, diferenciação entre opinião e notícia e correção. A [CVM](https://www.gov.br/cvm/pt-br/assuntos/regulados/consultas-por-participante/analistas-de-valores-mobiliarios) trata da atividade regulamentada de analistas. Essas fontes não determinam o organograma real.

## 3. Papéis propostos, não atribuídos a colaboradores reais

Papéis abstratos: SOURCE_CURATOR, DRAFT_AUTHOR, FACT_REVIEWER, EDITORIAL_REVIEWER, REGULATED_ANALYST_IF_APPLICABLE, COMPLIANCE_IF_APPLICABLE, EXPORT_APPROVER, PUBLISHER, AUDITOR.

| Decisão | Executor proposto | Autoridade necessária | Hard gate |
|---|---|---|---|
| fonte e pauta | SOURCE_CURATOR | editoria de origem | rights/embargo/workspace |
| ancoragem numérica | FACT_REVIEWER + diagnóstico automático | responsável factual | hash, trecho/tabela/célula e período |
| geração de rascunho | AI_AGENT | nenhuma aprovação implícita | source/policy/schema/9 identity |
| revisão de conteúdo | EDITORIAL_REVIEWER | papel real validado | fonte, policy, factualidade sem compensação |
| aprovação para exportar | EXPORT_APPROVER | autorização e auditoria futuras | role+policy+version+CAS |
| publicação | PUBLISHER fora da integração | autorização externa do CMS | nenhum auto-publish |
| revogação/correção | responsável de retratação | editoria/lane aplicável | versionamento e lineage |

Uma equipe pode combinar papéis apenas quando a política futura autorizar. **IA não é aprovador**, e D-0019 trata somente da decisão do operador de não contratar avaliadores humanos para calibração; não cria a autoridade de publicar conteúdo por IA.

## 4. Sequência mínima de estados (desenho, não motor implementado)

1. **SOURCE_PROPOSED** — identificar fonte/versão/source_group, classe editorial e candidato a uso.
2. **RIGHTS_CHECK** — classificar licença, embargo, conteúdo privado, finalidade e autorização por business line. Falha ou desconhecido → HOLD, sem upload a provider.
3. **SOURCE_ACCEPTED** — preservar bytes/hash e proveniência da fonte. Ambiguidade de role em tabela/célula → REVIEW_REQUIRED, sem promover fato.
4. **FACTS_ANCHORED** — manter número, sinal, unidade, período, modalidade, condição e ponte a page/span/table/cell.
5. **DRAFT_GENERATED** — executar uma saída solicitada ou **exatamente 9 saídas** quando modo 3×3; todos os jobs têm identidade única.
6. **CHECKED** — aplicar hard gates source/factual/policy/schema/provenance, comparações estruturadas e alerta de ausência de evidência. FAIL/REVIEW domina scores.
7. **REVIEW_PENDING** — rascunhos e referências em visualização; editor aprova/rejeita/solicita correção no futuro, quando papéis/autorização existirem.
8. **APPROVED_FOR_EXPORT** — somente após signoff autorizado real, sem fonte/policy stale. **Não implementado por esta task**.
9. **EXPORTED_DRAFT** — export versionado para uso externo, não postagem. Nenhum workflow CMS autorizado por este estudo.
10. **REVOKED / REWORK** — mudança de source hash, política ou erro material invalida versões afetadas e retorna à checagem.

**Rotas de negócio:** NEWS_EDITORIAL (informar; independência e verificação), RESEARCH_ANALYST (relatório técnico regulado quando aplicável), MARKETING_EDUCATION (distinguir publicidade e afirmações). UNKNOWN não deve ser classificado automaticamente como notícia ou como recomendação.

**Invariantes:** nenhum artefato em SOURCE_BLOCKED, RIGHTS_HOLD, REVIEW_REQUIRED ou sem autorização evolui para aprovado/publicado; aprovação de uma variante não aprova as demais oito; revisão de versão não sobrescreve prova antiga; nenhum source hash divergente pode validar afirmação antiga; publicação automática continua fora do escopo.

## 5. Classes de fonte, condições e limites

| Classe proposta | Exemplo | Elegibilidade atual |
|---|---|---|
| PRIMARY_DISCLOSURE | arquivos de companhias na [CVM](https://www.gov.br/cvm/pt-br/assuntos/regulados/consultas-por-participante/companhias) | leitura pública possível; licenças/termos de reutilização por fonte a confirmar |
| PUBLIC_MACRO_DATA | dados oficiais macroeconômicos | uso e periodicidade por endpoint/licença a confirmar |
| SUNO_PUBLISHED_NEWS | notícia publicada no site | público para leitura; rodapé da [linha editorial](https://www.suno.com.br/noticias/linha-editorial/) restringe reprodução/distribuição não autorizada |
| SUNO_RESEARCH_PAID | relatório de assinante | não usar sem autorização específica |
| THIRD_PARTY_LICENSED | datasets/feeds comerciais | não usar sem contrato/escopo explícitos |
| EMBARGOED | release ainda não liberado | HOLD até embargo e direitos resolvidos |
| PRIVATE_PERSONAL | material interno ou pessoal | HOLD; avaliação da finalidade, necessidade, base legal e fornecedor |
| UNKNOWN | licença ou procedência desconhecida | HOLD |

**Bases normativas de triagem:** [Lei 9.610/1998, art. 29](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm) sobre reprodução/adaptação; [LGPD compilada arts. 4, 6, 7, 15–16](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm) sobre finalidade, hipóteses e término; [ANPD](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-para-definicoes-dos-agentes-de-tratamento-de-dados-pessoais-e-do-encarregado) sobre responsabilidades. A exceção para tratamento *exclusivamente jornalístico* **não** é licença geral para SaaS, analytics, logs e fornecedores. O worker não emite parecer jurídico nem supõe permissão.

## 6. Contrato mínimo de dados proposto (não implementado)

Um pacote auditável incluiria: document_id, source_group_id, source_hash, source_version, source_uri, rights_class, allowed_uses_ref, editorial_lane, policy_version, run_id, attempt_id, audience, format, job_id, prompt_version, schema_version, model_version, claim_refs, source_span_refs/table_cell_refs, numeric_assertions, hard_gates, unresolved_findings, repair_history, draft_content_digest, editorial_status, reviewer_decision_ref **quando existir de verdade**, export_permission_ref e retention_class.

Missing critical: rights, source_hash ou provenance ⇒ HOLD/REVIEW. Falta de reviewer/permission ⇒ não há APPROVED_FOR_EXPORT. Não incluir dados pessoais/segredos em repositório. Correspondência entre claim_id e uma asserção fornecida não comprova que o PDF realmente sustenta a frase; a ponte M05 é limitada à verificação contratual estruturada (ver docs/product/research/W010_T002_NATIVE_BRIDGE.md).

## 7. Counterfactuals e protocolo quantitativo

**A0:** fluxo manual real (UNKNOWN); **A1:** prompting direto com revisão; **A2:** rascunho único + fonte/claims ancorados + gates; **A3:** 3×3 + M05 + eval/repair/revisão; **A4:** checklist no editor/CMS sem geração. Todas são alternativas candidatas; **nenhuma executada** nesta task. A3 só é comparável a outras no mesmo conjunto de entregáveis; não alegar que nove variantes equivalem a um artigo.

**Workload para teste futuro:** fonte autorizada por source_group, tipo de peça/complexidade definidos antes da análise, mesma versão/hash dos documentos e configuração pareada, sem leakage entre DEV/CAL/HELD_OUT de uma mesma fonte. Registros brutos por tentativa e formato incluem tempos wall e ativo quando medidos, contagem de edições, source/policy failures e suas evidências, status crítico, tokens/infra/licença completos e perdas/duplicações em 9/9.

**Métricas com denominador explícito:** active_editor_minutes (soma de sessões ativas reais), time_to_approved_draft (diferença entre timestamps reais, não presumir aprovação), rework_rounds (revisões substantivas), critical_fact_errors (auditadas), false_alarm_rate (alertas falsos/alertas auditados), provenance_coverage (claims materiais ancorados/claims avaliáveis), editorial_rejections_by_reason, cost_per_approved_draft (custo total real/rascunhos aprovados), rights_incidents, source_revision_detection_delay e adoption_by_eligible_user. Todas **NOT_MEASURED** aqui. Para eventos censurados, reportar separadamente não aprovados/abandono; nunca dividir por zero nem converter falta de logs em sucesso.

**Uncertainty:** dados agrupados por documento/fonte, intervalos de confiança e efeito somente quando amostras e independência permitirem; hard gates prevalecem sobre custo/tempo. Nenhum tamanho de amostra, p95, SLA, ROI, preferência Suno, benchmark ou threshold foi inventado. IA-only pode executar testes sintéticos e diagnósticos (human_gold_eligible=false), mas não fingir revisão humana.

## 8. Aceite, riscos e pontos de decisão

| Tema | Critério para saída do UNKNOWN | Situação nesta entrega |
|---|---|---|
| Partner workflow | autoridade, mapa real e respostas com escopo | UNKNOWN |
| Canais e audiência | formatos/canais/taxonomia aprovados | UNKNOWN |
| Direitos e privacy | classes/autorizações/retention e fornecedores | UNKNOWN |
| Hard gates financeiros | verificação com fonte original e aceites independentes | REFERENCE_PARTIAL |
| Aprovação editorial | signoff auditável de pessoa autorizada e authz real | NOT_IMPLEMENTED |
| 3×3 | nove contratos e join consistente em escopo real solicitado | REFERENCE_SCOPED |
| Economia | baseline e custos completos de workload real | NOT_MEASURED |
| Release/produção | exigências PROD-001..017 e evidência operacional | NOT_AUTHORIZED |

**Condições de reversão/pivot:** se uma fonte não tiver uso permitido, manter manual; se nove variantes não forem usadas, priorizar uma saída sem alterar obrigação 3×3 do case; se checagem de claims for mais onerosa e não reduzir erro observado, reavaliar A2; se aprovação/legal não puder ser provada, manter tudo como DRAFT. Aplicar Decision Research Gate antes de travar arquitetura/políticas/workflow e solicitar ao Orchestrator somente integração da **pesquisa**, não aprovação da Suno.

**Traceability:** PAIN-005; A-0002; A-0011; RISK-0011; PROD-011; PROD-014; M01/M02/M05/M06/M07/M08/M11/M12. A-0002/A-0011/RISK-0011 permanecem OPEN_EXTERNAL, por design.
