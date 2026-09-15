# TRACEABILITY MATRIX

## Purpose

Garantir que nada importante do briefing, parceiro ou solução se perca entre pesquisa e entrega final.

## Required chain

`requirement/pain → evidence → assumption → insight/mechanism → solution → outcome → metric → deliverable location → validation`

## Evidence shorthand

- `E-0001` — briefing primário `docs/case/CASE_BRIEF_TRANSCRIPTION.md`.
- `E-0002` — pesquisa pública `docs/research/partner-competitor-ai-benchmark-2026-09-14.md`.
- `E-0003` — resultados W001-T001…T010 integrados em `SYSTEM/RESULTS/`, incluindo Hybrid Evaluator e candidate architecture/build plan.

## Matrix

| ID | Type | Source / requirement / pain | Evidence refs | Assumption refs | Solution element | Outcome / metric | Deliverable location | Status |
|---|---|---|---|---|---|---|---|---|
| PAIN-001 | PAIN | Documentos financeiros densos criam barreira para iniciantes/intermediários | E-0001,E-0003 | — | audience contracts + ACV/calibrated decision | compreensão sem perda factual | app + relatório | DESIGNED |
| PAIN-002 | PAIN | LLM simplifica por encurtamento e perde nuances | E-0001,E-0003 | A-0003 | immutable factual backbone + concept floors | concept/anchor preservation | evaluator + relatório | DESIGNED |
| PAIN-003 | PAIN | LLM-as-a-judge genérico é subjetivo/enviesado | E-0001,E-0002,E-0003 | A-0010 | hybrid evaluator + gold/ablation | deterministic + calibrated evaluation | eval framework | DESIGNED |
| PAIN-004 | PAIN | Ambiente financeiro/profissional exige rigor e auditabilidade | E-0001,E-0002,E-0003 | — | claim/source lineage + policy/audit trail | auditabilidade | dashboard + docs | DESIGNED |
| REQ-001 | REQUIREMENT | Ingestão de documentos financeiros públicos reais em PDF/texto | E-0001,E-0003 | A-0008 | ParserAdapter + SourceTrust | parse/anchor validation | pipeline | DESIGNED_NOT_BUILT |
| REQ-002 | REQUIREMENT | Workflow baseado em grafo com estado | E-0001,E-0003 | A-0005 | minimal StateGraph + simple baseline | state transitions/retry/checkpoint proof | pipeline/architecture | DESIGNED_NOT_BUILT |
| REQ-003 | REQUIREMENT | Gerar 3 níveis × 3 formatos | E-0001,E-0003 | — | VariantSpec[9] fan-out | 9 outputs por documento | app/demo | DESIGNED_NOT_BUILT |
| REQ-004 | REQUIREMENT | Iniciante: sem jargão desacompanhado de analogia; foco prático | E-0001,E-0003 | — | beginner contract + concept/analogy checks | unexplained-jargon + audience fit | evaluator | DESIGNED_NOT_CALIBRATED |
| REQ-005 | REQUIREMENT | Intermediário: vocabulário padrão; foco em alocação/tendências | E-0001,E-0003 | — | intermediate contract + ACV | calibrated audience fit | evaluator | DESIGNED_NOT_CALIBRATED |
| REQ-006 | REQUIREMENT | Avançado: preservar jargão e foco analítico/metodológico | E-0001,E-0003 | — | advanced contract + required labels | technical-concept preservation | evaluator | DESIGNED_NOT_CALIBRATED |
| REQ-007 | REQUIREMENT | Texto/Artigo Analítico | E-0001,E-0003 | — | typed Article schema/evaluator | format contract pass | app | DESIGNED_NOT_BUILT |
| REQ-008 | REQUIREMENT | Carrossel com gancho, corpo e conclusão | E-0001,E-0003 | — | typed Carousel schema/evaluator | slide-structure pass | app | DESIGNED_NOT_BUILT |
| REQ-009 | REQUIREMENT | Roteiro de vídeo curto com tempo/ganchos e fala <=60s | E-0001,E-0003 | — | typed ShortVideo schema/evaluator | duration/structure pass | app | DESIGNED_NOT_BUILT |
| REQ-010 | REQUIREMENT | Legibilidade estatística adaptada ao português | E-0001,E-0002,E-0003 | A-0009 | versioned PT-BR readability | development-gold calibration | eval framework | DESIGNED_NOT_CALIBRATED |
| REQ-011 | REQUIREMENT | Domain Term Density + contextualização via glossário financeiro | E-0001,E-0003 | — | versioned concept ontology/features | density/context/recall | eval framework | DESIGNED_NOT_BUILT |
| REQ-012 | REQUIREMENT | Factuality & Grounding Checker contra fonte | E-0001,E-0002,E-0003 | — | anchors + atomic claim grounding + source trust | unsupported/contradicted findings | evaluator/dashboard | DESIGNED_NOT_BUILT |
| REQ-013 | REQUIREMENT | Refinement loop rejeita/reprocessa se limiar falhar | E-0001,E-0003 | — | job-local targeted repair | FAIL→repair→PASS evidence | pipeline/demo | DESIGNED_NOT_BUILT |
| REQ-014 | REQUIREMENT | Interface comparativa com métricas por nível | E-0001,E-0003 | A-0005 | 3×3 evidence cockpit | side-by-side + lineage + telemetry | app | DESIGNED_NOT_BUILT |
| REQ-015 | REQUIREMENT | GitHub com grafo funcional e contribuições consistentes | E-0001 | — | repository/process | reproducibility + history | GitHub | ACTIVE |
| REQ-016 | REQUIREMENT | Suíte automatizada/reprodutível de evals | E-0001,E-0003 | A-0004,A-0010 | pytest + deterministic/adversarial/regression suites | regression pass | tests + relatório | DESIGNED_NOT_BUILT |
| REQ-017 | REQUIREMENT | Demonstrar auto-correção baseada em feedback numérico | E-0001,E-0003 | — | RepairRequest + lineage + re-eval | before/after metrics | demo video + app | DESIGNED_NOT_BUILT |
| REQ-018 | REQUIREMENT | Dashboard deve exibir rastreabilidade das fontes | E-0001,E-0002,E-0003 | — | source-click evidence cockpit | source attribution coverage | app | DESIGNED_NOT_BUILT |
| REQ-019 | REQUIREMENT | Relatório: matriz de confusão de níveis | E-0001,E-0003 | A-0006 | development/held-out + dual matrices | confusion matrix + macro metrics | docs/report | DESIGNED_NOT_EXECUTED |
| REQ-020 | REQUIREMENT | Relatório: trade-offs de custo/latência | E-0001,E-0003 | — | TelemetryEvent + versioned pricing | cost/output + latency distributions | docs/report | DESIGNED_NOT_EXECUTED |
| REQ-021 | REQUIREMENT | README/instruções claras de reprodutibilidade | E-0001,E-0003 | — | clean-start release item | reproduction pass | README | OPEN |
| REQ-022 | REQUIREMENT | Vídeo deve comprovar código e interface reais; ausência/falha anula entrega | E-0001,E-0003 | A-0001 | evidence-cockpit demo protocol | real code/UI shown | video | DESIGNED_NOT_EXECUTED |
| REQ-023 | REQUIREMENT | Duração do vídeo: conflito 5–7 min vs máximo 5 min | E-0001,E-0003 | A-0001 | 4:40 target + reserve | runtime <=5:00 | video | CONTROLLED |
| REQ-024 | REQUIREMENT | Não publicar automaticamente em redes / não renderizar avatar / não streaming ms | E-0001,E-0003 | — | explicit scope guard | no scope creep | architecture/docs | CONTROLLED |
| PAIN-005 | PARTNER | Potencial necessidade de escalar conteúdo multi-audiência/multicanal com confiança | E-0002,E-0003 | A-0002,A-0003 | content transformation + trust layer | time/rework/reuse hypotheses | partner value section | SUPPORTED_HYPOTHESIS |
| CRIT-001 | CRITICAL | Nenhuma média pode compensar perda factual ou requisito eliminatório | E-0001,E-0003 | — | non-compensatory HybridDecision | zero critical violations | success scorecard | DESIGNED |

## Rules

- IDs podem ser `REQ-###`, `PAIN-###`, `CRIT-###`, `CLAIM-###`.
- Todo requisito obrigatório e critério explícito precisa de linha própria.
- Toda dor/outcome material do parceiro precisa de linha própria.
- Claim material da solução deve apontar para evidência e, se aplicável, assumption ID.
- Antes da finalização, nenhum requisito obrigatório pode estar `OPEN`, `MISSING` ou sem `Deliverable location`.
- Mudança no briefing/feedback do parceiro exige revalidar linhas afetadas.