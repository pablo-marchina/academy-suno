# CASE CONTRACT — Suno Content

`CASE_CONTRACT_VERSION: 0001`

`SOURCE_STATUS: PRIMARY_BRIEF_INGESTED`

## Source

Documento primário fornecido pelo usuário: **CASE SETEMBRO: SUNO CONTENT**, 4 páginas. Transcrição canônica em `docs/case/CASE_BRIEF_TRANSCRIPTION.md`.

Pesquisa pública complementar: `docs/research/partner-competitor-ai-benchmark-2026-09-14.md`.

## Pergunta norteadora

Como desenhar e avaliar um pipeline de IA capaz de adaptar documentos regulatórios e financeiros complexos para diferentes públicos e formatos, garantindo rigor conceitual, adequação de vocabulário e fidelidade factual por meio de métricas objetivas e determinísticas?

## Objetivo explícito do projeto

Desenvolver um sistema inteligente baseado em grafos com estado capaz de receber documentos financeiros públicos densos e gerar conteúdos adaptados para **3 níveis de sofisticação** (Iniciante, Intermediário e Avançado) em **3 formatos** (Texto/Artigo Analítico, Carrossel Informativo e Roteiro de Vídeo Curto).

O núcleo diferencial exigido é um **Avaliador Híbrido de Calibração e Rigor** que combine algoritmos linguísticos determinísticos, extração/monitoramento de entidades e termos financeiros, grounding/factuality e julgamento estruturado para comprovar que a adaptação por nível é real e não simples encurtamento.

## Problema explícito

1. **Resumo por encurtamento / trivialização** — LLMs podem cortar ou simplificar ingenuamente e perder nuances financeiras/macroeconômicas.
2. **Avaliação subjetiva** — LLM-as-a-judge genérico pode sofrer complacência, viés de extensão e incapacidade de quantificar densidade conceitual.
3. **Necessidade profissional/regulada** — o sistema precisa de avaliação quantitativa, determinística e baseada em dados para tom, fidelidade factual e terminologia.

## Entradas no escopo

Documentos financeiros públicos reais em PDF/texto, incluindo exemplos dados no briefing:
- Atas do Copom;
- Fatos Relevantes da CVM;
- releases de resultados / documentos de companhias listadas/B3;
- relatórios de inflação/política monetária são citados na contextualização.

## Matriz obrigatória de adaptação

### Audiência 1 — Iniciante
- zero jargão financeiro desacompanhado de analogia cotidiana;
- foco no impacto prático no bolso.

### Audiência 2 — Intermediário
- vocabulário de mercado padrão (ex.: CDI, Selic, IPCA, dividendos);
- foco em alocação e tendências.

### Audiência 3 — Avançado/Institucional
- preservação de jargão pleno (ex.: curva de juros, forward guidance, hiato do produto, EBITDA ajustado, covenants);
- foco analítico e metodológico.

### Formatos obrigatórios
1. Texto/Artigo Analítico para web/newsletter.
2. Estrutura de Carrossel com gancho, corpo e conclusão.
3. Roteiro de Vídeo Curto com marcações de tempo, ganchos visuais e fala em até 60 segundos.

Total nominal por documento: **9 combinações audiência × formato**.

## Framework Híbrido de Avaliação — obrigatório

- legibilidade estatística / Flesch adaptado ao português;
- Domain Term Density Score ou equivalente operacional para densidade/contextualização de termos técnicos contra glossário financeiro;
- Factuality & Grounding Checker contra o documento fonte;
- Refinement Loop que rejeita/reprocessa quando métricas do nível não são atendidas;
- LLM Judge apenas de forma estruturada dentro do framework híbrido, não como única fonte de verdade.

## Interface — obrigatório

Visualização comparativa da matriz de saídas e relatório/telemetria das métricas de avaliação por nível. O Entregável 4 adiciona rastreabilidade das fontes.

## Fora do escopo explícito

- publicação automática em Instagram/TikTok/LinkedIn;
- renderização direta de vídeo com avatares sintéticos;
- análise de mercado em tempo real com streaming de cotações em milissegundos.

## Tecnologias sugeridas — não tratadas como obrigatórias

- workflow: LangGraph ou Pydantic AI;
- léxico/legibilidade: textstat ou implementação customizada;
- glossário/NER: spaCy ou extração baseada em Pydantic;
- evals: DeepEval, Ragas ou pytest;
- interface: Streamlit, FastAPI + React ou Gradio.

A escolha final de stack deve ser justificada por qualidade, reprodutibilidade, tempo de implementação, auditabilidade, custo/latência e clareza da demo.

## Entregáveis obrigatórios

### DEL-001 — Pipeline de Adaptação Estruturada + GitHub
Grafo funcional que processe documentos e cubra variações de nível e formato, com contribuições consistentes no GitHub.

### DEL-002 — Suíte de Avaliação Híbrida
Código reprodutível com métricas determinísticas de legibilidade e densidade de termos técnicos, complementadas por factuality/grounding e julgamento estruturado conforme o escopo.

### DEL-003 — Mecanismo de Auto-Correção
Demonstração de desvio detectado (ex.: nível básico difícil demais) e reescrita baseada em feedback numérico.

### DEL-004 — Interface de Demonstração / Dashboard
Aplicação web exibindo conteúdo, comparação, rastreabilidade de fontes e pontuações do avaliador.

### DEL-005 — Vídeo Demonstrativo + Apresentação Técnica
Deve apresentar arquitetura, aplicação funcionando ao vivo, suíte de avaliação em ação e decisões de engenharia.

### DEL-006 — Relatório Experimental + Documentação
README/repositório com metodologia de avaliação, matriz de confusão de níveis, trade-offs de custo/latência e instruções de reprodutibilidade.

## Restrição crítica de vídeo e conflito de fonte

O briefing contém uma inconsistência que deve permanecer explícita:
- seção de Entregável 5: “vídeo de até 5 a 7 minutos”;
- seção 7, Diretrizes do Vídeo: **“Duração: Máximo de 5 minutos.”**

A seção 7 também declara como **critério eliminatório** a ausência do vídeo ou vídeo que não comprove funcionamento real do código e da interface.

Regra operacional provisória: **planejar vídeo <= 5:00**, por ser a instrução mais específica e associada ao critério eliminatório. Essa interpretação está registrada como `A-0001` até eventual confirmação do organizador.

## Critérios de avaliação explícitos / inferíveis do próprio enunciado

O documento não fornece pesos, escala numérica ou rubrica formal. Não inventar pesos.

Hard gates/requisitos verificáveis extraídos do briefing:
- funcionamento real do pipeline;
- cobertura da matriz 3×3;
- fidelidade factual/grounding;
- calibração de sofisticação sem mero encurtamento;
- métricas determinísticas reproduzíveis;
- refinement loop demonstrável;
- interface comparativa com telemetria/rastreabilidade;
- testes automatizados;
- matriz de confusão de níveis;
- trade-offs de custo/latência;
- documentação reprodutível;
- vídeo real <=5 min como regra operacional e com prova de código/interface.

## Audiência da entrega

- parceiro/desafio: Suno / “Suno Content” no briefing;
- contexto visual do documento: Academy x Finance;
- banca, avaliadores específicos e decision maker interno: `UNKNOWN`.

## Prazo e submissão

- mês indicado no título: Setembro;
- data/hora limite: `UNKNOWN`;
- método de submissão: `UNKNOWN`;
- formato obrigatório além dos entregáveis acima: `UNKNOWN`.

## Definition of success para o case

A entrega deve passar o `SYSTEM/SUCCESS_MODEL.md`: valor real para o parceiro + aderência integral ao briefing + rigor/evidência + solução forte/diferenciada + viabilidade/adoção + excelência do artefato + comunicação/defesa + robustez de execução, sem permitir que média alta compense hard gate crítico.
