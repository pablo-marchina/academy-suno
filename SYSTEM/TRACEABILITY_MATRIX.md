# TRACEABILITY MATRIX

## Purpose

Garantir que nada importante do briefing, parceiro ou solução se perca entre pesquisa e entrega final.

## Required chain

`requirement/pain → evidence → assumption → insight/mechanism → solution → outcome → metric → deliverable location → validation`

## Evidence shorthand

- `E-0001` — briefing primário `docs/case/CASE_BRIEF_TRANSCRIPTION.md`.
- `E-0002` — pesquisa pública `docs/research/partner-competitor-ai-benchmark-2026-09-14.md`.

## Matrix

| ID | Type | Source / requirement / pain | Evidence refs | Assumption refs | Solution element | Outcome / metric | Deliverable location | Status |
|---|---|---|---|---|---|---|---|---|
| PAIN-001 | PAIN | Documentos financeiros densos criam barreira para iniciantes/intermediários | E-0001 | — | audience adaptation | compreensão sem perda factual | app + relatório | OPEN |
| PAIN-002 | PAIN | LLM simplifica por encurtamento e perde nuances | E-0001 | A-0003 | factual backbone + calibration | concept/anchor preservation | evaluator + relatório | OPEN |
| PAIN-003 | PAIN | LLM-as-a-judge genérico é subjetivo/enviesado | E-0001,E-0002 | A-0010 | hybrid evaluator | deterministic + calibrated judge metrics | eval framework | OPEN |
| PAIN-004 | PAIN | Ambiente financeiro/profissional exige rigor e auditabilidade | E-0001,E-0002 | — | grounding + traceability | claim/source lineage | dashboard + docs | OPEN |
| REQ-001 | REQUIREMENT | Ingestão de documentos financeiros públicos reais em PDF/texto | E-0001 | A-0008 | parser/extractor | parse success + anchor coverage | pipeline | OPEN |
| REQ-002 | REQUIREMENT | Workflow baseado em grafo com estado | E-0001 | A-0005 | state graph | state transitions/retry reproduzíveis | pipeline/architecture | OPEN |
| REQ-003 | REQUIREMENT | Gerar 3 níveis × 3 formatos | E-0001 | — | fan-out audience × format | 9 outputs por documento | app/demo | OPEN |
| REQ-004 | REQUIREMENT | Iniciante: sem jargão desacompanhado de analogia; foco prático | E-0001 | — | beginner adapter | unexplained-jargon rate + readability | evaluator | OPEN |
| REQ-005 | REQUIREMENT | Intermediário: vocabulário padrão; foco em alocação/tendências | E-0001 | — | intermediate adapter | calibrated term coverage | evaluator | OPEN |
| REQ-006 | REQUIREMENT | Avançado: preservar jargão e foco analítico/metodológico | E-0001 | — | advanced adapter | technical-concept preservation | evaluator | OPEN |
| REQ-007 | REQUIREMENT | Texto/Artigo Analítico | E-0001 | — | article synthesizer | format contract pass | app | OPEN |
| REQ-008 | REQUIREMENT | Carrossel com gancho, corpo e conclusão | E-0001 | — | carousel synthesizer | slide-structure pass | app | OPEN |
| REQ-009 | REQUIREMENT | Roteiro de vídeo curto com tempo/ganchos e fala <=60s | E-0001 | — | short-video synthesizer | estimated duration <=60s | app | OPEN |
| REQ-010 | REQUIREMENT | Legibilidade estatística adaptada ao português | E-0001,E-0002 | A-0009 | PT-BR readability metric | threshold calibration | eval framework | OPEN |
| REQ-011 | REQUIREMENT | Domain Term Density + contextualização via glossário financeiro | E-0001 | — | ontology/glossary evaluator | density/contextualization metrics | eval framework | OPEN |
| REQ-012 | REQUIREMENT | Factuality & Grounding Checker contra fonte | E-0001,E-0002 | — | anchor/claim grounding | unsupported-claim + numeric mismatch rate | eval framework/dashboard | OPEN |
| REQ-013 | REQUIREMENT | Refinement loop rejeita/reprocessa se limiar falhar | E-0001 | — | conditional retry | FAIL→repair→PASS evidence | pipeline/demo | OPEN |
| REQ-014 | REQUIREMENT | Interface comparativa com métricas por nível | E-0001 | A-0005 | web UI | side-by-side + telemetry | app | OPEN |
| REQ-015 | REQUIREMENT | GitHub com grafo funcional e contribuições consistentes | E-0001 | — | repository/process | reproducibility + history | GitHub | OPEN |
| REQ-016 | REQUIREMENT | Suíte automatizada/reprodutível de evals | E-0001 | A-0004,A-0010 | pytest/custom evals/semantic layer | regression suite pass | tests + relatório | OPEN |
| REQ-017 | REQUIREMENT | Demonstrar auto-correção baseada em feedback numérico | E-0001 | — | targeted repair | before/after metrics | demo video + app | OPEN |
| REQ-018 | REQUIREMENT | Dashboard deve exibir rastreabilidade das fontes | E-0001,E-0002 | — | source lineage UX | source attribution coverage | app | OPEN |
| REQ-019 | REQUIREMENT | Relatório: matriz de confusão de níveis | E-0001 | A-0006 | gold/eval dataset | confusion matrix + macro metrics | docs/report | OPEN |
| REQ-020 | REQUIREMENT | Relatório: trade-offs de custo/latência | E-0001 | — | telemetry/experiment | cost/output + latency distributions | docs/report | OPEN |
| REQ-021 | REQUIREMENT | README/instruções claras de reprodutibilidade | E-0001 | — | documentation | clean-start reproduction pass | README | OPEN |
| REQ-022 | REQUIREMENT | Vídeo deve comprovar código e interface reais; ausência/falha anula entrega | E-0001 | A-0001 | final demo protocol | real live demo shown | video | OPEN |
| REQ-023 | REQUIREMENT | Duração do vídeo: conflito 5–7 min vs máximo 5 min | E-0001 | A-0001 | finalization rule | planned runtime <=5:00 | video | CONTROLLED |
| REQ-024 | REQUIREMENT | Não publicar automaticamente em redes / não renderizar avatar / não streaming ms | E-0001 | — | scope guard | no scope creep | architecture/docs | OPEN |
| PAIN-005 | PARTNER | Potencial necessidade de escalar conteúdo multi-audiência/multicanal com confiança | E-0002 | A-0002,A-0003 | content transformation + trust layer | time/rework/reuse hypotheses | partner value section | HYPOTHESIS |
| CRIT-001 | CRITICAL | Nenhuma média pode compensar perda factual ou requisito eliminatório | E-0001 | — | hard-gate evaluator | zero critical violations | success scorecard | OPEN |

## Rules

- IDs podem ser `REQ-###`, `PAIN-###`, `CRIT-###`, `CLAIM-###`.
- Todo requisito obrigatório e critério explícito precisa de linha própria.
- Toda dor/outcome material do parceiro precisa de linha própria.
- Claim material da solução deve apontar para evidência e, se aplicável, assumption ID.
- Antes da finalização, nenhum requisito obrigatório pode estar `OPEN`, `MISSING` ou sem `Deliverable location`.
- Mudança no briefing/feedback do parceiro exige revalidar linhas afetadas.
