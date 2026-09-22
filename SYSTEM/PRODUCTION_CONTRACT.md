# PRODUCTION CONTRACT — Academy Suno

`PRODUCTION_CONTRACT_VERSION: 1.0`

## 1. Purpose

Transformar o case comprovado em um produto real, multiusuário e defendível para produção, preservando integralmente os requisitos do briefing Suno. O vídeo obrigatório continua existindo, mas demonstra o mesmo sistema real; não existe arquitetura paralela/fake exclusiva para demo.

## 2. Non-negotiable product principles

1. **Single real product path** — frontend, API, workflow, providers, evals, repair, storage e observability usados na defesa são os mesmos componentes do produto.
2. **Multi-user / multi-tenant** — identidade, organização/workspace, autorização e isolamento devem ser propriedades de primeira classe.
3. **Quantitative-first** — propriedades mensuráveis usam métricas, datasets, thresholds e uncertainty; qualitativo entra apenas onde não houver substituto válido e deve ser estruturado.
4. **Eval-Driven Development** — mudanças materiais de geração/eval/prompt/model/parser/runtime passam por regressão/experimento antes de promoção.
5. **Adaptive where useful, deterministic where safety-critical** — invariantes de source trust, factualidade crítica, schema, compliance, tenant isolation e provenance permanecem fail-closed; routing/model/prompt/retrieval/repair/budget/concurrency podem adaptar sob políticas observáveis.
6. **Maximum live visibility** — arquitetura, execução, outputs, evidência, evals, repair, traces, custo, latência e saúde do sistema devem ser inspecionáveis no frontend quando tecnicamente seguro.
7. **Evidence-driven choices** — nenhuma escolha material de stack/arquitetura é congelada sem `DECISION_RESEARCH_GATE`.
8. **Production claims require production evidence** — local smoke/demo/fixture não é production readiness.

## 3. Product requirements

### PROD-001 — Identity and tenant isolation
- usuários autenticados;
- `organization/workspace/user/run` como dimensões explícitas;
- RBAC/authorization definido e testado;
- cross-tenant unauthorized access observado = 0 nos testes;
- tenant binding obrigatório em dados persistidos e artifacts privados.

### PROD-002 — Production API boundary
- API tipada/versionada;
- validação de payloads e limites de upload;
- idempotency para operações relevantes;
- tratamento de timeouts/retries/backpressure;
- sem input de path arbitrário no filesystem do servidor para usuários não confiáveis.

### PROD-003 — Durable shared persistence
- estado de runs deve sobreviver restart/redeploy;
- storage compartilhado apropriado a múltiplas réplicas;
- histórico/audit trail imutável ou append-only onde aplicável;
- backup/restore demonstrado.

### PROD-004 — Secure document/object storage
- uploads em área controlada/object store;
- allowlist de formatos necessários;
- size limits, content validation e filename/path sanitization;
- source hash, provenance e retention policy explícitos.

### PROD-005 — Real provider path
- o fluxo recipient-facing final executa providers reais quando configurado;
- nenhuma tela final substitui output real por preview `MECHANICS_ONLY` sem identificação explícita;
- provider/model abstraídos e mensurados por qualidade/custo/latência/reliability.

### PROD-006 — Stateful 3×3 AI workflow
- documento real → anchor/provenance → 3 audiências × 3 formatos → eval → repair/review → aggregate;
- branch identity estável;
- lossless join;
- resume após interrupção;
- hard gates não compensatórios.

### PROD-007 — Hybrid evaluation system
- factual/source/policy hard gates;
- legibilidade PT-BR;
- term density/contextualization;
- concept/numeric/entity/date preservation;
- structured semantic/judge sensors secundários;
- versioned evaluator configuration.

### PROD-008 — Human-calibrated audience evidence
Para claims fortes de audience calibration/production thresholds:
- dataset cego versionado;
- pelo menos duas streams humanas independentes por item ou protocolo equivalente justificado;
- agreement/adjudication reportados;
- DEV/CALIBRATION/HELD-OUT separados;
- confusion matrix e uncertainty;
- thresholds congelados somente com evidência suficiente.

Até lá, thresholds continuam `DIAGNOSTIC_ONLY`.

### PROD-009 — Eval-driven CI/CD
- regressão determinística em PRs materiais;
- offline eval/experiments para mudanças probabilísticas;
- baseline vs candidate no mesmo dataset/configuração;
- release block quando hard gate regressa;
- artifacts de experimento persistidos.

### PROD-010 — Adaptive runtime policy
- routing/model/prompt/retrieval/repair/budget podem adaptar;
- objetivo multiobjetivo explícito: qualidade + factualidade + latência + custo + reliability;
- policy versionada e auditável;
- nenhuma adaptação pode relaxar hard gates críticos.

### PROD-011 — Live Evidence Cockpit
O frontend final deve permitir, no mínimo:
- workspace/document/run status;
- grafo live e eventos por node;
- matriz 3×3 real;
- source explorer/citations;
- metric breakdown;
- before/after repair;
- experiment comparison;
- trace explorer;
- custo/latência/tokens/retries;
- health/reliability;
- audit/provenance;
- research/decision records.

### PROD-012 — Observability
- traces, metrics e structured logs correlacionados por request/run/job/tenant;
- provider/eval spans;
- p50/p95/p99, error/retry/queue rates e cost;
- telemetry exportável e inspecionável.

### PROD-013 — Reliability and capacity evidence
Antes de `production-ready`:
- load curve em níveis crescentes de concorrência;
- failure/retry tests;
- restart/resume tests;
- backup/restore test;
- defined SLO/SLA targets ou explicitamente `UNKNOWN` até dados suficientes;
- saturation point documentado, não inventado.

### PROD-014 — Security and privacy evidence
- threat model;
- authz tests;
- tenant isolation tests;
- upload/input abuse controls;
- secrets management;
- dependency/security scanning;
- least privilege;
- logging sem vazamento indevido de conteúdo/credentials.

### PROD-015 — Research-gated architecture
Toda decisão material segue `SYSTEM/DECISION_RESEARCH_GATE.md` e registra alternativas, fontes, critérios, benchmark, decisão, incerteza e reversal conditions.

### PROD-016 — Reproducible deployment
- ambiente declarativo/containerizado quando adequado;
- health checks e startup/restart behavior;
- migrations reproduzíveis;
- configuração/secrets fora do código;
- clean deployment/runbook reproduzível.

### PROD-017 — Production-grade final evidence
A entrega final deve mostrar o sistema real ao vivo. O vídeo obrigatório do briefing permanece <=5:00 e funciona como evidência do produto, não como substituto dele.

## 4. Quantitative release gates

Os valores abaixo são invariantes hard quando aplicáveis; demais targets devem ser definidos por pesquisa/benchmark antes do freeze:

- critical factual/source/policy hard-gate compensation: `0`;
- cross-tenant unauthorized access in defined tests: `0`;
- runs/jobs without provenance binding: `0`;
- required 3×3 branch coverage: `9/9`;
- accepted join losing/duplicating branches: `0`;
- critical schema violations promoted as PASS: `0`;
- backup/restore and restart/resume defined scenarios: `100% PASS` before production claim;
- final technical video: `<= 5:00`.

Quality/audience/latency/cost/capacity thresholds may not be invented. They require dataset/benchmark evidence and confidence bounds where relevant.

## 5. Out of scope remains out of scope

Preservar o briefing: publicação automática em redes sociais, avatar/renderização sintética de vídeo e streaming de cotações em milissegundos não entram salvo nova decisão explícita baseada em valor e impacto no case.

## 6. Definition of production-ready

`PRODUCTION_READY` só pode ser alegado quando PROD-001..017 aplicáveis estiverem rastreados e seus hard gates estiverem `PASS`, com security/reliability/deployment evidence real. Qualquer lacuna vira `PRODUCTION_UNKNOWN`, `DIAGNOSTIC_ONLY` ou blocker explícito; nunca é promovida por inferência.
