# CASE SETEMBRO: SUNO CONTENT — Transcrição canônica

Fonte: PDF fornecido pelo usuário nesta conversa, 4 páginas.

## 1. Contextualização do Problema

O mercado financeiro produz um volume diário de comunicados cruciais para a tomada de decisão: atas do Copom, fatos relevantes, relatórios de inflação e releases de resultados trimestrais. No entanto, esses documentos são redigidos em linguagem técnica, densa e formal, criando uma barreira de compreensão para investidores iniciantes e intermediários.

A prática comum de usar modelos de linguagem (LLMs) para resumir esses documentos enfrenta dois problemas graves:

1. **Resumo por Encurtamento (Trivialização):** a IA frequentemente apenas corta frases ou simplifica o vocabulário de forma ingênua, perdendo nuances macroeconômicas críticas ou infantilizando a comunicação.
2. **Avaliação Subjetiva (Falta de Rigor Técnico):** a validação da qualidade dos resumos costuma depender apenas de outro prompt genérico (LLM-as-a-judge), que sofre de viés de complacência, viés de extensão (textos mais longos recebem notas maiores) e incapacidade de quantificar densidade conceitual.

Para que um sistema de IA seja viável em ambientes regulados e profissionais, ele não pode ser apenas um gerador cego: ele precisa de uma camada de avaliação quantitativa, determinística e baseada em dados (Eval-Driven Development), capaz de aferir a adequação do tom, a fidelidade factual e a densidade de terminologia técnica.

## 2. Objetivo do Projeto

Desenvolver um sistema inteligente baseado em grafos com estado capaz de receber documentos financeiros públicos densos e gerar conteúdos adaptados para 3 níveis de sofisticação (Iniciante, Intermediário e Avançado) em 3 formatos de mídia (Texto Analítico, Carrossel Informativo e Roteiro de Vídeo Curto).

O principal diferencial e núcleo de aprendizado do projeto é a construção de um Avaliador Híbrido de Calibração e Rigor: uma suíte automatizada de testes e métricas que combina algoritmos linguísticos determinísticos, extração de entidades financeiras e julgamento estruturado para medir se os níveis de sofisticação foram genuinamente respeitados, sem recorrer a simples encurtamento textual.

## 3. Pergunta Norteadora

Como desenhar e avaliar um pipeline de IA capaz de adaptar documentos regulatórios e financeiros complexos para diferentes públicos e formatos, garantindo rigor conceitual, adequação de vocabulário e fidelidade factual por meio de métricas objetivas e determinísticas?

## 4. Escopo da Solução

### No Escopo

- **Ingestão e Processamento:** leitura e estruturação de documentos financeiros públicos reais em PDF/texto (ex.: Atas do Copom, Fatos Relevantes da CVM, Releases de Resultados da B3).
- **Matriz de Adaptação:**
  - **Audiências:**
    1. Iniciante: zero jargão financeiro desacompanhado de analogia cotidiana; foco no impacto prático no bolso.
    2. Intermediário: vocabulário de mercado padrão (CDI, Selic, IPCA, dividendos); foco em alocação e tendências.
    3. Avançado/Institucional: jargão pleno preservado (curva de juros, forward guidance, hiato do produto, EBITDA ajustado, covenants); foco analítico e metodológico.
  - **Formatos:**
    1. Texto/Artigo Analítico (para web/newsletter).
    2. Estrutura de Carrossel (slides com gancho, corpo e conclusão).
    3. Roteiro de Vídeo Curto (marcações de tempo, ganchos visuais e roteiro de fala em até 60s).
- **Framework Híbrido de Avaliação (Núcleo Diferencial):**
  - cálculo de legibilidade estatística (Flesch-Kincaid adaptado ao português);
  - Domain Term Density Score: densidade e contextualização de termos técnicos contra glossário financeiro pré-estabelecido;
  - Factuality & Grounding Checker: fidelidade factual das afirmações geradas em relação ao documento fonte;
  - Refinement Loop: rejeita e reprocessa o texto caso as métricas do nível não sejam atendidas.
- **Interface:** visualização comparativa da matriz de saídas e exibição do relatório de métricas de avaliação por nível.

### Fora do Escopo

- publicação automática nas redes sociais (APIs de Instagram/TikTok/LinkedIn);
- renderização direta de vídeo com avatares sintéticos (foco no roteiro e estrutura);
- análise de mercado em tempo real com streaming de cotações em milissegundos.

## 5. Arquitetura da Solução e Tecnologias Sugeridas

### 5.1 Pipeline Multi-Agente / Workflow com Estado (LangGraph ou Pydantic AI)

1. Document Extractor & Anchor: extrai pontos centrais, números-chave e declarações factuais do documento original.
2. Audience Adapters (Executores Paralelos): nós especializados em adaptar o conteúdo para cada persona.
3. Format Synthesizers: nós responsáveis por estruturar as saídas nos formatos finais (artigo, carrossel, roteiro).
4. Hybrid Evaluator Node: executa a bateria de métricas determinísticas e LLM Judge estruturado.
5. Conditional Routing / Retry: se a pontuação do avaliador for inferior ao limiar do nível, o grafo faz nova iteração injetando o relatório de falha no contexto (Reflection Pattern).

### 5.2 Camada de Avaliação Técnica (Diferencial Prático)

- Algoritmos Léxicos: textstat ou implementações customizadas de Flesch Reading Ease adaptadas ao português brasileiro.
- Glossário & NER: spaCy ou extração baseada em Pydantic para monitorar termos técnicos sem analogia prévia no nível iniciante.
- Métricas de Avaliação de IA: DeepEval, Ragas ou suíte de testes com pytest para asserções automatizadas sobre outputs.

### 5.3 Interface e Visualização

- Streamlit, FastAPI + React ou Gradio: upload do PDF da ata/release, inspeção lado a lado das versões e auditoria da telemetria das métricas.

## 6. Entregáveis Esperados

1. **Entregável 1 — Pipeline de Adaptação Estruturada + GitHub com contribuições consistentes:** grafo funcional capaz de processar os documentos e cobrir as variações de nível e formato.
2. **Entregável 2 — Suíte de Avaliação Híbrida (Eval Framework):** código reprodutível com métricas determinísticas (legibilidade + densidade de termos técnicos) e testes automatizados.
3. **Entregável 3 — Mecanismo de Auto-Correção (Reflection Loop):** demonstração do agente detectando um desvio de nível e reescrevendo com base no feedback numérico.
4. **Entregável 4 — Interface de Demonstração e Dashboard:** aplicação web interativa exibindo o conteúdo gerado, a rastreabilidade das fontes e as pontuações do avaliador.
5. **Entregável 5 — Vídeo Demonstrativo e Apresentação Técnica:** vídeo de até 5 a 7 minutos apresentando arquitetura, aplicação web funcionando ao vivo, suíte de avaliação em ação e decisões técnicas de engenharia.
6. **Entregável 6 — Relatório Experimental e Documentação:** repositório no GitHub com README detalhado cobrindo metodologia de avaliação, matriz de confusão de níveis, trade-offs de custo/latência e instruções claras de reprodutibilidade.

## 7. Diretrizes do Vídeo Demonstrativo

- **Duração:** máximo de 5 minutos.
- **Critério Eliminatório:** a ausência do vídeo ou a entrega de um vídeo que não comprove o funcionamento real do código e da interface anula a entrega técnica.

## Nota de transcrição

Há uma inconsistência interna preservada acima: o Entregável 5 menciona “até 5 a 7 minutos”, enquanto a seção 7 fixa “Máximo de 5 minutos” e associa a diretriz a critério eliminatório. Nenhuma correção silenciosa foi feita nesta transcrição.
