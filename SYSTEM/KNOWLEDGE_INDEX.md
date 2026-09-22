# KNOWLEDGE INDEX

Este arquivo indexa conhecimento consolidado. Ele não substitui `SYSTEM/STATE.md`; serve para evitar inflar o estado canônico com detalhes de pesquisa e para impedir que workers usem conclusões históricas stale como se fossem verdade corrente.

## Camadas de informação

```text
RAW RESULTS / ISSUES / EXPERIMENTS
        ↓
KNOWLEDGE INDEX + evidence artifacts
        ↓
TRACEABILITY / SCORECARDS / DECISIONS
        ↓
CANONICAL STATE
```

## Evidence registry aceito

| Evidence ID | Claim / Topic | Source / Artifact | Evidence class / boundary | Status |
|---|---|---|---|---|
| E-0001 | Briefing primário: problema, 3×3, Hybrid Evaluator, refinement, interface, relatório e vídeo | `docs/case/CASE_BRIEF_TRANSCRIPTION.md`, `SYSTEM/CASE_CONTRACT.md` | primary case evidence | VERIFIED |
| E-0002 | Suno/competidores/AI-finance/content benchmark e unknowns internos | `docs/research/partner-competitor-ai-benchmark-2026-09-14.md` | public research; internal workflow remains inferred/unknown | VERIFIED_BOUNDED |
| E-0003 | Case Contract consolidado sem inventar pesos/deadline | `SYSTEM/CASE_CONTRACT.md` | canonical contract | VERIFIED |
| E-0004 | Partner Contract com dor, contexto, hipóteses e unknowns explícitos | `SYSTEM/PARTNER_CONTRACT.md` | canonical contract | VERIFIED |
| E-0007 | Eval/readability/ontology/golden foundation W003 | accepted W003 results/artifacts | development/eval foundation | VERIFIED_BOUNDED |
| E-0010 | Exact 9-job E2E mechanics + repair + RunStore | accepted W003 mechanics/e2e artifacts | controlled mechanics, not production readiness | VERIFIED_BOUNDED |
| E-0014 | Recipient app/report package | W004-T014/T015 artifacts | recipient-case scope | VERIFIED_BOUNDED |
| E-0017 | Final paced real-browser demo 69.12 s | W004-T019 artifacts | real browser/demo scope | VERIFIED_BOUNDED |
| E-0018 | Independent final video/package review | W004-T020 | review scope; zero new CRITICAL/HIGH in that package | VERIFIED_BOUNDED |
| E-0019 | Durable exact repository copy + byte identity | W004-T021 | artifact durability scope | VERIFIED |
| E-0020 | Observed Groq mechanics, latency/usage and official-pricing-derived cost | W004-T004-A08 | `PROVIDER_MECHANICS`; not quality winner | VERIFIED_BOUNDED |
| E-0021 | 36/36 automated blind audience calibration | W004-T005-A02 + D-0017 | `MODEL_AUTOMATED_BLIND_CALIBRATION`; `human_gold=false` | VERIFIED_BOUNDED |
| E-0022 | Semantic-off/on ablation delta +0.000000 | W004-T006-A01 | diagnostic ablation; hard gates invariant | VERIFIED_BOUNDED |
| E-0023 | Observed Groq 120B/20B bounded comparison, 8/8 calls | W004-T007-A05 | same-task bounded comparison; `NO_OVERALL_MODEL_PREFERENCE` | VERIFIED_BOUNDED |
| E-0024 | Clean-checkout release proof, 9/9 | W004-T008-A02 / Actions `35672891477` | clean-E2E W004 release scope | VERIFIED_BOUNDED |
| E-0025 | Explicit operator scope expansion to real production-grade multi-user product | D-0018 + `SYSTEM/PRODUCTION_CONTRACT.md` | operator requirement; does not itself prove production | VERIFIED_REQUIREMENT |

`TRACEABILITY_MATRIX.md` é a fonte canônica para a aplicação desses IDs a requisitos/claims. Um worker não cria um Evidence ID definitivo por conta própria; ele propõe evidência e o Orchestrator integra/numera quando aceito.

## Case / briefing truth

- problema: transformar conteúdo financeiro denso para diferentes públicos e formatos sem perder rigor;
- saída obrigatória: 3 audiências × 3 formatos;
- evaluator híbrido, métricas, factual grounding e refinement loop são centrais;
- interface comparativa, relatório técnico/experimental, GitHub/reprodutibilidade e vídeo real fazem parte do deliverable;
- vídeo continua hard gate de submissão; regra operacional segura preservada: `<=5:00`;
- publicação automática em social/avatar/streaming de cotação permanecem fora do escopo do briefing;
- deadline e mecanismo de submissão continuam `UNKNOWN_EXTERNAL`.

## Partner / users / value

Fatos suportados:
- audiences externas: Iniciante, Intermediário e Avançado/Institucional;
- trust/factual preservation é central ao problema;
- conteúdo multicanal é parte explícita do case.

Ainda não observado diretamente:
- owner/decision maker/workflow interno Suno;
- baseline real de tempo/retrabalho/custo editorial;
- ROI operacional do produto.

Portanto, tempo economizado, ROI e adoção interna são hipóteses a medir, não claims atuais.

## W004 — baseline aceito, não target final

W004 provou no escopo declarado:

- exact 9-job fan-out e lossless join;
- state/checkpoint/repair lineage;
- source/factual/policy hard-gate non-compensation;
- targeted repair com fresh re-evaluation;
- recipient-facing text/PDF ingest e fail-closed source trust;
- provider mechanics reais e comparação bounded;
- automated blind calibration com provenance explícita;
- clean-checkout release proof;
- browser-real final demo e artifact durability.

Limites que **não podem ser promovidos**:

- D-0017 não é human gold e não calibra thresholds de produção;
- comparação de provider/model não selecionou winner global;
- SQLite/local RunStore não é shared production persistence;
- recipient app W004 não é multi-user production frontend;
- W004 não prova tenant isolation, secure untrusted uploads, deployment, capacity, recovery ou produção real multi-replica;
- mechanics/demo evidence não equivale a `PRODUCTION_READY`.

## Production scope — D-0018

O target passa a obedecer `PROD-001..017` em `SYSTEM/PRODUCTION_CONTRACT.md`:

1. real multi-user identity/tenancy/authz;
2. typed production API;
3. shared durable persistence;
4. secure document/object ingestion;
5. real provider path no produto;
6. durable exact 3×3 workflow + repair/resume;
7. hybrid eval com deterministic/source-grounded hard gates;
8. stronger human-calibrated audience evidence para claims de produção quando disponível;
9. Eval-Driven Development offline/CI/online;
10. adaptive-safe runtime para escolhas suaves;
11. live Evidence Cockpit;
12. arquitetura/runtime visualizáveis no frontend;
13. capacidade/reliability medidas quantitativamente;
14. security/privacy/secrets/audit;
15. systematic Decision Research Gate;
16. deploy/migrate/rollback/backup/recovery;
17. frontend real consumindo runtime real.

Produção só pode ser alegada no escopo que possuir evidência para todos os hard gates aplicáveis.

## Decision Research Gate

Toda escolha material permanece desbloqueada até passar por `SYSTEM/DECISION_RESEARCH_GATE.md`.

### Regras consolidadas

- incluir baseline atual como counterfactual quando houver;
- cobrir >=3 alternativas materialmente diferentes quando existirem;
- usar documentação primária/standards/papers/advisories e fontes independentes pertinentes;
- definir critérios antes de observar resultados;
- executar benchmark reproduzível em workload representativo quando testável;
- medir dimensões relevantes — qualidade, factualidade, p50/p95/p99, throughput, errors, queue, cost, resource use, operational burden;
- reportar slices, variance/uncertainty e raw observations quando o desenho permitir;
- terminar em `LOCK`, `NO_PREFERENCE` ou `PENDING_EVIDENCE` com reversal conditions;
- parar pesquisa por evidence saturation, não por preferência/volume de links.

## W005 — production decision research

Estado inicial da wave: T001–T009 `READY` em paralelo; T010–T012 são fan-in gated.

| Task | Pergunta principal |
|---|---|
| W005-T001 | transformar Production Contract em requisitos/aceitação mensuráveis sem selecionar stack |
| W005-T002 | frontend/API/event streaming/live Evidence Cockpit |
| W005-T003 | orchestration/durability/concurrency/crash recovery/multi-replica |
| W005-T004 | identity/tenant/authz/database/storage/upload/security |
| W005-T005 | eval science, corpus, human calibration, offline/CI/online EDD |
| W005-T006 | adaptive provider/model/prompt/retrieval/repair routing sob hard gates |
| W005-T007 | traces/metrics/logs/live evidence/redaction/LLM observability |
| W005-T008 | deployment/reliability/capacity/recovery/operational burden |
| W005-T009 | benchmark harness e metodologia quantitativa cross-cutting |
| W005-T010 | synthesis de arquitetura e decisões a partir de T001–T009 |
| W005-T011 | red-team independente da arquitetura sintetizada |
| W005-T012 | fan-in final + DAG das waves de implementação |

Nenhum worker deve antecipar T010/T012 com uma stack escolhida por gosto, popularidade ou familiaridade.

## Technology posture corrente

### Foundation invariants preservados

Conforme D-0016 e D-0018:
- typed Python + Pydantic v2 nas fronteiras persistidas é baseline comprovado, não licença para congelar toda a stack de produção;
- canonical source/provenance spine;
- source trust antes de generation;
- semantic table-role provenance para fatos de tabela;
- factual/policy/source hard gates não compensatórios;
- exact 3×3 com branch/job identities estáveis;
- repair local;
- semantic/LLM judge apenas como sensor secundário.

### Identidades ainda desbloqueadas

Precisam de W005/DRG antes de produção:
- frontend framework e rendering/deployment model;
- API framework/boundary;
- auth/identity provider;
- database/RLS ou alternativa;
- object storage;
- orchestration/durable workflow runtime;
- parser implementation;
- model/provider/routing policy;
- semantic eval/LLM observability stack;
- telemetry backend;
- deployment topology/cloud/runtime;
- dependency/package/toolchain do produto final.

O repositório ainda não possui um manifest/toolchain definitivo do produto de produção por desenho: criar um agora seria lock prematuro antes do DRG. O baseline W004 continua reproduzível pelos workflows/instruções atuais.

## Evaluation posture

- audience thresholds atuais: `DIAGNOSTIC_ONLY`;
- human gold/agreement/preference: **not observed**;
- W004 automated blind calibration: válida somente no escopo D-0017;
- factual/source/policy hard gates: preservados fora de qualquer optimizer;
- W005-T005 deve definir corpus ampliado, DEV/CALIBRATION/HELD-OUT, human annotation/adjudication, uncertainty e online eval;
- W005-T009 deve fornecer metodologia quantitativa reutilizável para as demais decisões.

## Reliability / security posture

P0/P1 ativos antes de qualquer production claim incluem:
- cross-tenant leakage;
- arbitrary filesystem path / unsafe upload;
- SQLite/local source of truth sob multi-replica;
- synthetic/stale cockpit evidence;
- observability data leakage;
- adaptive routing bypassando hard gates;
- untested capacity/recovery/deployment.

Fonte canônica: `SYSTEM/ASSUMPTION_RISK_REGISTER.md`.

## Economics / metrics

Já existe evidence bounded de provider usage/latency/cost em W004, mas isso não é workload de produção nem ROI do parceiro.

W005 deve estabelecer como medir, conforme decisão:
- quality/eval slices;
- latency p50/p95/p99;
- throughput/error/queue/resource saturation;
- provider/model/token cost;
- retry/repair rate;
- recovery/restart behavior;
- operational burden;
- eventual user approval/edit/rework signals quando houver produto e usuários reais.

## Estratégia de diferenciação

A diferenciação defendida permanece: não “usar agentes”, mas construir uma transformação editorial financeira verificável que:

- sabe de qual fonte/trecho/fato veio cada saída;
- distingue invariantes determinísticos de escolhas adaptativas;
- detecta falhas quantitativamente;
- repara localmente e reavalia;
- preserva auditabilidade;
- compara alternativas/stack por evidência;
- mostra tudo isso live no produto real sem expor dados indevidos.

## Prioridade corrente

`PRODUCTION_DECISION_RESEARCH_EXECUTION`.

A próxima ação correta é executar W005-T001..T009 em paralelo, integrar evidência válida, então liberar T010→T011→T012. Phase 9 product implementation permanece gated até esse fan-in produzir arquitetura e DAG evidence-backed.
