# PARTNER CONTRACT — Suno Content

`PARTNER_CONTRACT_VERSION: 0001`

`STATUS: SUFFICIENT_FOR_DISCOVERY_WITH_EXPLICIT_UNKNOWNS`

## Partner/context

Parceiro do desafio: **Suno**, identificado no briefing como “Suno Content”. Evidência pública consolidada em `docs/research/partner-competitor-ai-benchmark-2026-09-14.md` indica um ecossistema de Research, Notícias, educação, mídia, Asset e Consultoria, com conteúdos em múltiplas profundidades e canais.

Não há evidência pública suficiente para afirmar que “Suno Content” seja uma unidade formal específica ou identificar o owner interno do desafio.

## Dor primária sustentada pelo briefing

Documentos financeiros públicos relevantes para decisão são densos, técnicos e formais. Investidores iniciantes/intermediários encontram barreira de compreensão. Ao usar LLMs para adaptação, surgem duas falhas críticas:

1. simplificação/trivialização que perde nuances;
2. avaliação subjetiva e pouco auditável baseada apenas em LLM-as-a-judge.

A dor pode ser expressa como:

> Como escalar transformação editorial de documentos financeiros para diferentes públicos e formatos sem sacrificar rigor factual/conceitual e com prova objetiva de que a adaptação respeitou o nível esperado?

## Quem sente a dor

### Evidência explícita
- investidores iniciantes e intermediários sofrem barreira de compreensão;
- usuários avançados/institucionais precisam preservar jargão e profundidade.

### Hipótese/inferência apoiada por contexto público
- equipes de conteúdo/editorial/research podem se beneficiar de automação de transformação, avaliação e rastreabilidade.

### UNKNOWN
- usuário interno primário do produto;
- owner operacional;
- decision maker;
- equipe que implementaria/manteria o sistema.

## Contexto público relevante do parceiro

Pesquisa pública sugere:
- a Suno opera conteúdo educacional, notícias, research, podcasts, YouTube e produtos em diferentes profundidades;
- o ecossistema declara atender públicos “do iniciante ao profissional”;
- há sinais públicos de valorização de IA, agilidade e excelência;
- Notícias/Research/Asset possuem contextos editoriais e regulatórios distintos;
- conteúdo público da Suno usa disclaimers e fronteiras de não-recomendação.

Esses pontos são contexto, não prova de workflow interno.

## Workflow/status quo

### Sustentado pelo briefing
- uso comum de LLMs para resumir/adaptar documentos;
- validação frequentemente feita por prompt genérico/LLM judge;
- isso pode gerar trivialização e avaliação complacente/enviesada.

### UNKNOWN
- workflow editorial interno atual da Suno;
- ferramentas atuais;
- volume de documentos/conteúdos;
- tempo de produção/revisão;
- causas e taxa de retrabalho;
- processo de aprovação/compliance;
- modelos/provedores permitidos.

## Sintomas vs. causas

### Sintomas
- resumo curto porém raso;
- nível iniciante ainda difícil ou infantilizado;
- nível avançado diluído;
- perda de números, entidades, condicionais ou nuances;
- confiança excessiva em uma nota subjetiva de judge.

### Causas candidatas a validar
- transformação direta `documento cru → texto livre` sem backbone factual;
- ausência de rubrica mensurável por audiência/formato;
- ausência de grounding/anchors por claim;
- judge não calibrado e circular;
- falta de dataset/gold labels para validar os níveis;
- ausência de feedback numérico estruturado para repair.

## Outcome desejado explícito

Sistema que:
- recebe documentos financeiros públicos densos;
- gera 3 níveis × 3 formatos;
- preserva fidelidade factual e rigor conceitual;
- mede adequação de nível e terminologia;
- detecta falhas;
- corrige automaticamente com base em relatório estruturado;
- exibe saídas, métricas e rastreabilidade de fontes.

## Outcomes de valor para o parceiro — hipóteses, não requisitos do briefing

A validar em W001/fases seguintes:
- reduzir tempo de transformação editorial;
- reduzir retrabalho de revisão de nível/factualidade;
- aumentar reutilização multicanal da mesma fonte;
- aumentar consistência entre canais/audiências;
- aumentar auditabilidade e confiança do processo de IA.

## Alternativas/counterfactuals que a solução deve superar

- processo manual puro;
- prompt único de resumo;
- três prompts por audiência sem evals;
- LLM-as-a-judge genérico;
- fluxo sem state/retry;
- soluções comerciais de summarization/research sem calibração 3×3 específica;
- solução mais simples com templates/regras determinísticas onde LLM não agrega valor.

## Restrições relevantes

### Explícitas
- documentos públicos;
- ambiente financeiro/profissional;
- 3 níveis × 3 formatos;
- vídeo curto de até 60s na saída;
- requisitos de eval híbrido e auto-correção;
- itens fora do escopo definidos no Case Contract.

### Contexto público / risco
- preservar fronteira entre explicar/adaptar a fonte e inventar recomendação de investimento;
- source lineage e transparência aumentam confiança;
- diferentes tipos de conteúdo podem exigir regras diferentes.

## Barreiras de adoção candidatas

- baixa confiança em factualidade;
- métricas fáceis de “gamear”;
- baixa qualidade de extração de PDF;
- latência/custo de múltiplas gerações e retries;
- ausência de gold set;
- inconsistência de voz/formato;
- integração com workflow editorial real desconhecida;
- necessidade de revisão humana em conteúdos sensíveis.

## Métricas de sucesso do parceiro

### Diretamente alinhadas ao briefing
- factuality/grounding;
- legibilidade calibrada por nível;
- densidade/contextualização de termos;
- capacidade de distinguir níveis (incluindo matriz de confusão no relatório experimental);
- taxa de outputs que passam sem retry e após repair;
- cobertura 3×3;
- rastreabilidade de fontes;
- custo/latência.

### Métricas operacionais futuras — hipóteses
- tempo por peça;
- retrabalho editorial;
- time-to-publish;
- número de formatos reaproveitados por fonte;
- taxa de correção humana pós-pipeline.

## Partner hard gates para este estágio

1. Não escolher solução final assumindo workflow interno inexistente na evidência.
2. Não confundir facilidade de leitura com qualidade para o nível avançado.
3. Não permitir que factualidade seja compensada por estilo/engajamento.
4. Comparar a solução com alternativas mais simples.
5. Manter unknowns internos explícitos e controlados.
6. Antes da finalização, possuir caminho plausível de implementação, uso e medição mesmo sem acesso interno completo.

## Unknowns prioritários

- owner/decision maker/implementer internos;
- workflow editorial real;
- volume e SLA;
- canais prioritários;
- voice/style guide interno;
- requisitos de compliance internos;
- orçamento/limites de custo e latência;
- modelo/provedor permitido;
- existência de dataset anotado;
- data final e método de submissão.
