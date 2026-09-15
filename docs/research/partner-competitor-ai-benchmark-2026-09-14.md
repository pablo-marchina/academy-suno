# Partner + Competitor + AI Product Benchmark

Data da pesquisa: 2026-09-14

## Escopo

Este documento consolida pesquisa pública sobre: (1) Suno e seus padrões de conteúdo/canais; (2) concorrentes e referências brasileiras; (3) produtos globais de IA financeira comparáveis; (4) arquitetura/evals comparáveis; (5) pessoas/equipe publicamente identificáveis e limitações de inferência.

O objetivo é apoiar BOOT-T002 e a construção de W001 sem transformar inferência em fato.

---

## 1. Suno: o que a evidência pública sugere

### 1.1 Posicionamento e ecossistema

O Grupo Suno se apresenta como um ecossistema com Research, Asset, Consultoria, Notícias, conteúdos educacionais e mídia. A página institucional também organiza conteúdos por Relatórios (Morning Call, Radar do Mercado, Resumo da Semana, Fiikipedia), Análise de Empresas, Educação Financeira e produtos gratuitos/pagos.

Fonte: https://www.suno.com.br/sobre/

A home atual da Suno mostra convivência de Notícias, Artigos, Guias, Cursos, Podcasts, YouTube, Suno One e assinaturas. Isso reforça que a dor do case é plausível como problema de distribuição multiformato, não apenas de sumarização.

Fonte: https://www.suno.com.br/

### 1.2 Diferentes profundidades editoriais já existem

A Suno publica conteúdo educacional de baixa barreira, como guias para iniciantes, com estrutura didática, perguntas frequentes, definições e passos práticos.

Exemplos:
- https://www.suno.com.br/artigos/tipos-de-investimentos-guia-completo-gss/
- https://www.suno.com.br/artigos/investimentos-para-iniciantes/

Também mantém conteúdo mais técnico sobre curva de juros, EV/EBITDA, valuation e outros conceitos avançados.

Exemplos:
- https://www.suno.com.br/artigos/curva-de-juros/
- https://www.suno.com.br/artigos/evebitda/comment-page-1/
- https://www.suno.com.br/artigos/reflexoes-tipos-de-valuation/

Isso significa que o eixo Beginner → Intermediate → Advanced não é artificial: já há sinais públicos de uma jornada de sofisticação do conteúdo. O case pode ser entendido como tentativa de tornar essa adaptação sistemática, mensurável e reproduzível.

### 1.3 Notícias têm padrão factual e temporal diferente

Suno Notícias opera com textos mais factuais, headline-driven, com números, entidades, atribuição de fontes e atualização temporal. Exemplo atual de mercado:

https://www.suno.com.br/noticias/ibovespa-cai-petrobras-petr4-focus-radar-mt/

Isso sugere que o sistema precisa distinguir `CONTENT_TYPE`: adaptar uma notícia ou fato relevante exige preservação de entidades, números, datas e grau de certeza muito mais estrita do que um artigo educacional.

### 1.4 Suno Minuto é um benchmark interno relevante

A central de ajuda descreve o Suno Minuto como ferramenta de atualizações diárias “curtas e diretas” sobre ativos, para decisões rápidas e menor esforço de leitura.

Fonte: https://www.suno.com.br/central-de-ajuda/

Isso reforça a hipótese de que a empresa já valoriza compressão editorial, mas o case pede elevar isso para uma transformação controlada por nível de sofisticação, formato e evals.

### 1.5 Vídeo possui linguagem e objetivo próprios

O canal verificado da Suno no YouTube tem cerca de 519 mil seguidores/inscritos no momento da pesquisa. Um episódio recente do Valor em Pauta tem mais de 50 minutos, com capítulos, tópicos macroeconômicos, materiais gratuitos e disclaimer educacional. A descrição estrutura explicitamente o que o espectador “vai entender”.

Exemplo: https://www.youtube.com/watch?v=QB_HZCwBY08

A própria página de autor da Suno Research mostra Shorts recentes. Isso indica coexistência de long-form e short-form e reforça que “roteiro de até 60s” precisa ser tratado como adaptação de mídia, não mero truncamento de artigo.

Fonte: https://www.suno.com.br/autor/suno-research/

### 1.6 Padrões editoriais e compliance

A home e páginas de conteúdo carregam disclaimer de que o material não deve ser interpretado como aconselhamento ou consultoria de valores mobiliários e mencionam segregação de atividades conforme regras de entidades reguladoras/autorreguladoras.

Fonte: https://www.suno.com.br/

Implicação: o pipeline deve preservar a fronteira entre EXPLICAR/ADAPTAR FONTE e CRIAR RECOMENDAÇÃO NOVA. Regras de conteúdo deveriam poder variar por `SOURCE_TYPE`, `CONTENT_TYPE` e, se aplicável, contexto/unidade de negócio.

### 1.7 Pessoas/equipe: o que é possível afirmar

Páginas públicas identificam Tiago Reis como Presidente do Conselho do Grupo Suno e mostram autores/editores históricos e atuais de conteúdos. A página pública de Felipe Areia o apresenta como editor-chefe do Suno Notícias; páginas antigas também citam Carlo Cauti em função editorial e Gian Kojikovski como diretor de conteúdo em 2020.

Fontes:
- https://www.suno.com.br/artigos/curva-de-juros/
- https://www.suno.com.br/noticias/author/felipe-areia/page/6/
- https://www.suno.com.br/noticias/suno-noticias-jornalismo/

Não há evidência pública encontrada que ligue qualquer uma dessas pessoas diretamente ao case “Suno Content / Academy x Finance”. Portanto, não atribuir ownership do desafio a nomes específicos sem material interno.

---

## 2. Benchmark competitivo brasileiro

### 2.1 Empiricus

A Empiricus se define como editora/casa de análise com linguagem simples e didática para pessoa física. Diferencia informativos gratuitos (newsletters/site) de publicações pagas/assinaturas. Sua página institucional enfatiza “linguagem acessível”, conteúdo profundo e direto ao ponto, jornada completa do investidor e histórico de copywriting persuasivo.

Fontes:
- https://www.empiricus.com.br/faq/quem-somos/
- https://www.empiricus.com.br/sobre/

Lições para o case:
- forte benchmark em simplificação e didática;
- separação free vs paid e conteúdo vs recomendação;
- risco de confundir “acessível” com copy persuasiva: nosso sistema deve medir rigor e factualidade separadamente de engajamento.

### 2.2 Nord Investimentos

A Nord organiza sua oferta explicitamente pela jornada do investidor e por tiers Start, Plus, Advanced e Supreme. Os produtos combinam conteúdos, cursos, podcasts, e em planos/verticais específicos email, monitorias e Telegram.

Fontes:
- https://www.nordinvestimentos.com.br/research/produtos-e-assinaturas/
- https://www.nordinvestimentos.com.br/research/produtos-e-assinaturas/caminhos-do-investidor/

Lições:
- benchmark muito forte para segmentação por estágio de sofisticação;
- a segmentação hoje parece principalmente por produto/assinatura, não uma transformação auditável da mesma fonte em 3 níveis;
- nosso 3×3 pode ser diferenciado se provar que uma mesma verdade factual é adaptada sem circularidade de avaliação.

### 2.3 XP Research

A XP organiza conteúdo por cadência e intenção: Morning Call diário, relatórios mensais de macro/renda fixa/alocação, resumos semanais, resultados de empresas, relatórios setoriais, trilhas de aprendizado, podcasts e vídeos. A newsletter Expert Drops sintetiza temas da semana em blocos curtos que apontam para análises profundas.

Fontes:
- https://conteudos.xpi.com.br/conteudos-gerais/researchxp-menu-relatorios/
- https://conteudos.xpi.com.br/conteudos-gerais/25-anos-de-investimentos-qual-o-proximo-passo-expert-drops/

Lições:
- benchmark de “content ladder”: sinal diário → resumo semanal → deep dive;
- bom exemplo de reutilização editorial entre texto, relatórios, podcasts e vídeos;
- a oportunidade do case é adicionar adaptação de sofisticação e controle quantitativo de qualidade.

### 2.4 BTG Pactual

O Research BTG publica taxonomia ampla por classe de ativo e estratégia, com conteúdo técnico aprofundado, incluindo Macro Strategy, Ações, Renda Fixa, Commodities, Cripto, FII/FIP-IE e carteiras recomendadas. Há também conteúdo de Morning Call e podcast Radar do Investidor.

Fontes:
- https://content.btgpactual.com/research/home/acoes/ativo/
- https://content.btgpactual.com/blog/autor/jerson-zanlorenzi
- https://cloud.btgpactual.com/ (Morning Call)

Relatórios públicos exibem linguagem institucional sofisticada, com termos como duration, high yield, spreads, taxa terminal, carry, curvas e benchmarks.

Exemplo: https://content.btgpactual.com/research/files/file/pt-BR/2025-04-01T110303.824_Global_Asset_Strategy___BTG_Pactual_Abr25.pdf

Lições:
- benchmark de nível avançado/institucional;
- preservação de jargão e método é parte da utilidade, não erro de legibilidade;
- nosso evaluator precisa evitar punir o nível avançado apenas por baixa facilidade de leitura.

### 2.5 Síntese competitiva

Evidência pública mostra que os grandes players já segmentam por jornada, canal, frequência e profundidade. Não foi encontrada, nesta pesquisa, evidência pública de um produto brasileiro que demonstre de forma central o seguinte conjunto ao mesmo tempo:

`mesma fonte financeira → 3 níveis de sofisticação × 3 formatos → métricas determinísticas + grounding → auto-repair → confusion matrix/benchmark experimental`.

Essa combinação é um potencial espaço de diferenciação do case.

---

## 3. Produtos globais de IA financeira comparáveis

### 3.1 AlphaSense

AlphaSense posiciona seu produto como plataforma de insights de IA sobre centenas de milhões de documentos financeiros/empresariais. Destaca citações em nível de sentença, outputs rastreáveis, integração do fluxo de pesquisa até relatórios/decks e conexão entre conclusões, premissas e fontes.

Fonte: https://www.alpha-sense.com/

Princípios que devemos absorver:
- source-first;
- citation-first;
- rastreabilidade de cada output;
- não separar geração de auditabilidade.

### 3.2 Quartr

Quartr constrói IA sobre material de RI de primeira parte: calls, transcripts, filings e slides. A mensagem de confiança é explícita: todo finding deve ser rastreável à fonte, e o produto explora também mudanças de linguagem/KPIs ao longo do tempo.

Fonte: https://quartr.com/

Princípios:
- first-party data como camada de confiança;
- traceabilidade como UX, não apenas log interno;
- estruturar documentos financeiros para IA antes de gerar narrativa.

### 3.3 FactSet Transcript Assistant

FactSet lançou Transcript Assistant com GenAI para extrair resumos, high/low takeaways, guidance atualizado e temas-chave de earnings calls.

Fontes:
- https://investor.factset.com/
- https://www.factset.com/

Princípio: a unidade de valor não é “texto resumido”, mas `insight type` estruturado.

### 3.4 Morningstar

Morningstar introduziu news summaries e outros recursos de IA e comunica explicitamente ao usuário o uso de IA.

Fonte: https://www.morningstar.com/

Princípio: transparência operacional sobre IA deve ser considerada parte do trust layer.

### 3.5 LSEG

LSEG enfatiza AI-ready financial data, trusted data pipelines e integração de dados/IA. Sua comunicação atual trata confiança e qualidade de dados como pré-condição para IA financeira.

Fonte: https://www.lseg.com/

Princípio: avaliação do output não substitui qualidade/linhagem do input.

---

## 4. Arquitetura e evals comparáveis

### 4.1 Financial Narrative Summarization

O Financial Narrative Summarisation (FNS) é uma linha acadêmica consolidada de sumarização de relatórios financeiros longos. Em FinNLP 2025, um estudo aplicando GraphRAG ao FNS encontrou que uma abordagem RAG simples superou GraphRAG em várias dimensões antes de otimizações específicas de domínio.

Fontes:
- https://aclanthology.org/events/ranlp-2019/
- https://aclanthology.org/events/finnlp-2025/

Implicação: não usar GraphRAG por efeito de arquitetura. O case pede “grafos com estado”; isso não significa que o knowledge substrate precisa ser GraphRAG.

### 4.2 AveniBench e avaliação financeira realista

AveniBench foi proposto como benchmark financeiro com habilidades como raciocínio tabular, raciocínio numérico, QA, long context, summarisation e diálogo, com modos de dificuldade.

Fonte: https://aclanthology.org/events/finnlp-2025/

Implicação: nosso golden set deveria ter slices por habilidade, não apenas uma nota geral de “qualidade”.

### 4.3 NLI/factualidade

FinNLP 2025 inclui trabalho sobre Natural Language Inference como judge para detectar problemas de factualidade e causalidade em análises financeiras. Isso reforça uso de entailment/contradiction como camada semântica separada do LLM judge editorial.

Fonte: https://aclanthology.org/events/finnlp-2025/

### 4.4 LLM-as-a-Judge: cuidado com multi-agent debate

Pesquisa de EMNLP 2025 encontrou que frameworks de debate multiagente podem amplificar vieses como position, verbosity, chain-of-thought e bandwagon, enquanto meta-judge tende a ser mais resistente em certos cenários.

Fonte: https://aclanthology.org/2025.findings-emnlp.941/

Implicação direta: o evaluator do case não deve ser “vários agentes discutindo até concordar”. Melhor usar métricas determinísticas + probes controlados + judge estruturado + human/gold calibration.

### 4.5 Regra-grounded audience adaptation

Trabalho de 2026 em outro domínio mostrou que rule grounding melhorou confiabilidade e adaptação de audiência comparado à geração direta a partir de dados crus.

Fonte: https://aclanthology.org/2026.bea-1.34/

É evidência cross-domain, não prova financeira, mas sustenta o desenho `validated facts/rules → audience adapter` em vez de `raw document → free-form rewrite`.

---

## 5. Content benchmark: padrões observados na Suno

Amostra pública representativa, não estatística:

### Beginner / educational

Características observadas:
- começa por definição do conceito;
- linguagem explicativa e direta;
- perguntas frequentes;
- passos práticos;
- exemplos cotidianos/operacionais;
- introdução de jargão seguida de explicação.

### News / factual

Características:
- headline orientada ao evento;
- prioridade para nomes, números, datas e movimento de mercado;
- atribuição de fontes/opiniões;
- baixo espaço para analogias;
- disclaimer de não recomendação.

### Advanced / analysis

Características:
- mantém múltiplos como EV/EBITDA, WACC, duration, spreads, curvas e termos macro;
- explica método quando a peça é educacional;
- em research institucional, profundidade e precisão superam facilidade de leitura.

### Short-form / Minuto / Shorts

Características:
- compressão de leitura/tempo;
- foco em sinal/actionable context;
- necessidade de preservar contexto mínimo para não transformar compressão em trivialização.

### Long-form video/podcast

Características:
- autoridade de especialista;
- construção de contexto;
- capítulos/temas;
- perguntas e tese narrativa;
- disclaimers e CTA.

Implicação: cada FORMAT deve ter evaluator próprio. Um “bom artigo” e um “bom roteiro de 60s” não compartilham a mesma função de qualidade.

---

## 6. Hipóteses de produto após benchmark

Hipótese H1: o produto de maior valor não é um resumidor; é uma `content transformation + trust layer`.

Hipótese H2: a ontologia/anchor layer deve produzir uma verdade factual comum antes do fan-out 3×3.

Hipótese H3: `audience level` e `media format` são dimensões ortogonais e devem ser avaliadas separadamente.

Hipótese H4: a principal diferenciação não está em LangGraph/Streamlit, mas em calibração, evidência, rastreabilidade e auto-repair mensurável.

Hipótese H5: para Suno, o produto pode reduzir tempo de produção/retrabalho e aumentar reutilização multicanal sem destruir rigor editorial.

Hipótese H6: uma demo de FAIL → diagnostics → targeted repair → PASS tende a comunicar mais valor do que apenas mostrar 9 outputs prontos.

Todas são hipóteses e devem ser validadas contra briefing, parceiro e experimentos.

---

## 7. Gaps que continuam UNKNOWN

- workflow editorial interno real da Suno;
- volume diário/semanal de documentos processados pela equipe;
- tempo médio de produção por tipo de peça;
- taxa/causas de retrabalho;
- quais canais são prioritários no desafio;
- quem é o usuário interno primário do produto;
- qual unidade/equipe é dona do problema;
- quais LLMs/provedores podem ou não ser usados;
- custo/latência aceitáveis;
- requisitos internos de compliance/editorial;
- se outputs devem imitar voz Suno ou apenas atender níveis do case;
- se o benchmark de avaliação será analisado manualmente pela banca;
- disponibilidade de material gold anotado.

Esses unknowns não impedem prototipagem, mas devem entrar no Assumption/Risk Register.

---

## 8. Recomendação para W001

W001 deve separar, em paralelo, pelo menos os seguintes workstreams: benchmark/voice da Suno por canal; ontology + domain-term calibration; factuality/grounding; readability PT-BR; dataset/gold labels + confusion matrix; architecture/state/retry; UX/demo; compliance/content policy; cost/latency; final-demo design.

O Orchestrator deve priorizar hard gates do briefing e os assumptions de maior impacto/incerteza, evitando decidir stack final antes dos experimentos mínimos.

---

## 9. Conclusão

A pesquisa pública sustenta uma tese forte: o mercado já possui conteúdo financeiro segmentado, multi-canal e produtos de IA que resumem/analisam fontes. A oportunidade específica do case é combinar tudo em um sistema que transforma uma verdade financeira comum em múltiplos níveis e formatos **com prova quantitativa de calibração, fidelidade e autocorreção**.

A vantagem competitiva do projeto não deve ser “usar agentes”, mas demonstrar que o sistema sabe quando sua própria transformação está errada e consegue corrigir o erro com rastreabilidade.
