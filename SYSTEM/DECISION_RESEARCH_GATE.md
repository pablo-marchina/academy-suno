# DECISION RESEARCH GATE — Academy Suno

`DRG_VERSION: 1.0`

## 1. Purpose

Nenhuma escolha material deve ser baseada apenas em preferência, fama, familiaridade ou opinião. Stack, arquitetura e políticas do produto são evidence-driven.

## 2. What requires DRG

O gate é obrigatório antes de `LOCKED`, produção/default ou migração material para:
- frontend framework/runtime;
- API framework/protocol;
- workflow/orchestrator/durability layer;
- database/run store/object storage/cache/queue;
- auth/identity/RBAC/tenancy;
- deploy/runtime/cloud/hosting/container strategy;
- observability/LLM observability;
- parser/OCR/extraction stack;
- provider/model/embedding/reranker/semantic backend;
- evaluator framework/metrics/thresholds;
- prompting/routing/repair policy;
- dataset/gold/calibration methodology;
- security controls com alternativas relevantes;
- qualquer decisão com custo, lock-in, reliability ou quality impact material.

## 3. Required research record

Cada decisão recebe um arquivo em `docs/decisions/research/DR-####-<slug>.md` durante a execução da task e deve conter:

1. **Decision question** — problema e contexto exato.
2. **Workload / constraints** — requisitos do Academy Suno que importam.
3. **Alternatives** — pelo menos 3 alternativas materialmente diferentes quando existirem; baseline atual sempre incluído se aplicável.
4. **Evaluation criteria** — critérios definidos antes do resultado; pesos apenas se houver base defensável.
5. **Systematic source search** — estratégia, queries/categorias, data da pesquisa e stopping rule.
6. **Source table** — fonte, tipo, data, autoridade, claim suportado, limitações.
7. **Primary evidence first** — docs oficiais/standards/papers antes de blogs/opiniões quando disponíveis.
8. **Security/reliability/cost/lock-in** — explicitamente cobertos quando relevantes.
9. **Reproducible benchmark/experiment** — workload representativo do projeto quando a escolha for testável.
10. **Raw results + uncertainty** — não apenas conclusão.
11. **Decision** — winner somente se evidência justificar; `NO_PREFERENCE` é resultado válido.
12. **Confidence** — HIGH/MEDIUM/LOW com justificativa.
13. **Reversal conditions** — que nova evidência reabre a decisão.
14. **Traceability** — requisitos/risks/metrics/artefatos afetados.

## 4. Source coverage

A pesquisa deve buscar cobertura máxima prática, não volume pelo volume. Sempre que relevantes, cobrir:
- documentação oficial/primary sources;
- standards/specifications;
- papers/benchmarks acadêmicos;
- security guidance;
- vendor pricing/limits/status/SLA docs;
- independent benchmark/review;
- community operational evidence para failure modes reais, marcada como evidência secundária.

Fontes recentes são obrigatórias para tecnologia/preço/limites mutáveis. Data e versões devem ser registradas.

## 5. Stopping rule — evidence saturation

A pesquisa pode parar quando:
- critérios relevantes já possuem evidência de alta qualidade;
- nova rodada de busca não introduz alternativa material, failure mode, restrição ou evidência capaz de alterar a decisão;
- fontes restantes são redundantes ou de autoridade inferior;
- benchmark do workload já diferencia as alternativas ou demonstra `NO_PREFERENCE`.

A justificativa de saturação deve ser registrada. “Pesquisei bastante” não é stopping rule.

## 6. Quantitative decision policy

Quando mensurável, comparar com dados: qualidade, factualidade, error rate, latency p50/p95/p99, throughput, cost, resource use, recovery behavior, developer complexity proxy, security controls e operational burden.

Não criar score único artificial para esconder trade-offs. Hard gates são não compensatórios. Pareto frontier e `NO_OVERALL_PREFERENCE` são resultados válidos.

## 7. Experiment hygiene

- mesmo dataset/workload/configuração comparável;
- seeds/temperature/config versionados quando aplicável;
- DEV/CALIBRATION/HELD-OUT preservados;
- baseline e candidates executados sob condições equivalentes;
- outputs/metrics persistidos;
- sample size e limitações declarados;
- múltiplas repetições quando variância importar;
- significance/CI/effect size quando apropriado.

## 8. Promotion gate

Uma escolha só pode virar `LOCKED`/production default se:
- DR record existe e está rastreado;
- hard requirements passam;
- benchmark relevante passa quando testável;
- riscos materiais têm controle;
- decisão declara confidence + reversal conditions;
- nenhum counterfactual materialmente superior ficou sem avaliação.

Caso contrário o estado permitido é `CANDIDATE`, `DIAGNOSTIC_ONLY`, `NO_PREFERENCE`, `PENDING_EVIDENCE` ou equivalente.

## 9. Autopilot behavior

Antes de implementar tecnologia ainda não decidida, o Orchestrator deve gerar research/bakeoff tasks. Workers podem construir spikes/benchmarks isolados, mas não promovem sua preferência. O Orchestrator integra apenas após DRG e reavalia o Success Model.
