# TRACEABILITY MATRIX

## Purpose

Garantir que nada importante do briefing, parceiro ou solução se perca entre pesquisa e entrega final.

## Required chain

`requirement/pain → evidence → assumption → insight/mechanism → solution → outcome → metric → deliverable location → validation`

## Evidence shorthand

- `E-0001` — briefing primário `docs/case/CASE_BRIEF_TRANSCRIPTION.md`.
- `E-0002` — pesquisa pública `docs/research/partner-competitor-ai-benchmark-2026-09-14.md`.
- `E-0003` — resultados W001-T001…T010 integrados, incluindo Hybrid Evaluator e candidate architecture/build plan.
- `E-0004` — W002-T001…T006: domain/provenance, parser/source-trust EXP-A, policy slice, format contracts, orchestration EXP-B, factual adversarial oracle.
- `E-0005` — W002-T007…T009: factual backbone/oracle runtime pass, canonical policy engine e 3×3 native-format generation core.
- `E-0006` — W002-T010: foundation synthesis e evidence-backed invariants.
- `E-0007` — W003-T001…T005: gold protocol, claim-level grounding, explicit graph/state + RunStore, PT-BR/ontology/ACV anti-gaming e clean-checkout Foundation Regression CI.

## Matrix

| ID | Type | Source / requirement / pain | Evidence refs | Assumption refs | Solution element | Outcome / metric | Deliverable location | Status |
|---|---|---|---|---|---|---|---|---|
| PAIN-001 | PAIN | Documentos financeiros densos criam barreira para iniciantes/intermediários | E-0001,E-0003,E-0007 | — | audience contracts + 3×3 planning + gold/ACV | compreensão sem perda factual | app + relatório | CORE_FEATURES_DIAGNOSTIC_CALIBRATION_PENDING |
| PAIN-002 | PAIN | LLM simplifica por encurtamento e perde nuances | E-0001,E-0003,E-0005,E-0007 | A-0003 | factual backbone + claim grounding + concept floors + repair | concept/anchor preservation | evaluator + relatório | CORE_PASS_REPAIR_PENDING |
| PAIN-003 | PAIN | LLM-as-a-judge genérico é subjetivo/enviesado | E-0001,E-0002,E-0003,E-0007 | A-0010 | hard gates + independent gold protocol + semantic ablation | calibrated hybrid evaluation | eval framework | CORE_PASS_CALIBRATION_PENDING |
| PAIN-004 | PAIN | Ambiente financeiro/profissional exige rigor/auditabilidade | E-0001,E-0002,E-0005,E-0007 | — | provenance + findings + RunStore + clean CI | audit trail reconstructível | dashboard + docs | CORE_AUDITABLE_UI_PENDING |
| REQ-001 | REQUIREMENT | Ingestão de documentos financeiros públicos reais em PDF/texto | E-0001,E-0004,E-0006 | A-0008 | source-trust contract + real fixtures + parser adapters | safe parse/source readiness | pipeline | FOUNDATION_PARTIAL_LIBRARY_UNLOCKED |
| REQ-002 | REQUIREMENT | Workflow baseado em grafo com estado | E-0001,E-0004,E-0006,E-0007 | A-0005 | explicit graph/state + persistent RunStore | 9/9 join, repair, checkpoint/resume, history | pipeline/architecture | CORE_PASS |
| REQ-003 | REQUIREMENT | Gerar 3 níveis × 3 formatos | E-0001,E-0005,E-0007 | — | VariantSpec + deterministic 3×3 planner | 9 unique jobs/source | app/demo | FOUNDATION_PASS_PROVIDER_PENDING |
| REQ-004 | REQUIREMENT | Iniciante: sem jargão desacompanhado; foco prático | E-0001,E-0003,E-0007 | A-0004,A-0006 | gold rubric + ontology/ACV | audience fit / unexplained jargon | evaluator | FEATURES_PASS_THRESHOLDS_PENDING |
| REQ-005 | REQUIREMENT | Intermediário: vocabulário padrão; alocação/tendências | E-0001,E-0003,E-0007 | A-0004,A-0006 | gold rubric + ontology/ACV | calibrated audience fit | evaluator | FEATURES_PASS_THRESHOLDS_PENDING |
| REQ-006 | REQUIREMENT | Avançado: preservar jargão e profundidade analítica | E-0001,E-0003,E-0007 | A-0004,A-0006 | gold rubric + ontology/ACV | technical concept preservation | evaluator | FEATURES_PASS_THRESHOLDS_PENDING |
| REQ-007 | REQUIREMENT | Texto/Artigo Analítico | E-0001,E-0005 | — | typed Article + provenance | format validation | app | FOUNDATION_PASS |
| REQ-008 | REQUIREMENT | Carrossel com gancho/corpo/conclusão | E-0001,E-0005 | — | typed Carousel HOOK/BODY/CONCLUSION | structure pass | app | FOUNDATION_PASS |
| REQ-009 | REQUIREMENT | Vídeo curto com tempo/ganchos e fala <=60s | E-0001,E-0005 | — | typed ShortVideo/timecodes/visual cues | duration/structure pass | app | FOUNDATION_PASS |
| REQ-010 | REQUIREMENT | Legibilidade estatística adaptada ao português | E-0001,E-0002,E-0003,E-0007 | A-0009 | `ptbr-readability-v001` + T008 calibration | controlled readability + coverage diagnostics | eval framework | IMPLEMENTED_DIAGNOSTIC_ONLY |
| REQ-011 | REQUIREMENT | Domain Term Density + contextualização via glossário | E-0001,E-0003,E-0007 | — | `finance-ptbr-v001` + ACV multidimensional | density/context/recall | eval framework | IMPLEMENTED_DIAGNOSTIC_ONLY |
| REQ-012 | REQUIREMENT | Factuality & Grounding Checker contra fonte | E-0001,E-0003,E-0005,E-0007 | — | deterministic backbone + claim-level HybridDecision | support/contradiction/unverifiable + provenance | evaluator/dashboard | CORE_PASS_PARTIAL_SCOPE |
| REQ-013 | REQUIREMENT | Refinement loop rejeita/reprocessa se limiar falhar | E-0001,E-0004,E-0007 | — | graph repair hook + T006 targeted repair | FAIL→feedback→repair→re-eval | pipeline/demo | GRAPH_HOOK_PASS_TARGETED_REPAIR_READY |
| REQ-014 | REQUIREMENT | Interface comparativa com métricas por nível | E-0001,E-0003,E-0006 | — | B13 evidence cockpit após W003 | side-by-side + lineage + telemetry | app | BLOCKED_BY_W003_PROOF |
| REQ-015 | REQUIREMENT | GitHub com grafo funcional e contribuições consistentes | E-0001,E-0004,E-0005,E-0007 | — | signal-aware DAG + graph/runstore + application CI | reproducibility/history | GitHub | STRONG_PASS_CORE |
| REQ-016 | REQUIREMENT | Suíte automatizada/reprodutível de evals | E-0001,E-0003,E-0005,E-0007 | A-0004,A-0010 | combined clean CI + focused suites | regression pass | tests + relatório | STRONG_PASS_CORE |
| REQ-017 | REQUIREMENT | Auto-correção baseada em feedback numérico | E-0001,E-0003,E-0007 | — | W003-T006 targeted repair | before/after metrics | demo + app | READY |
| REQ-018 | REQUIREMENT | Dashboard exibe rastreabilidade das fontes | E-0001,E-0002,E-0005,E-0007 | — | provenance + RunStore + future B13 cockpit | source attribution coverage | app | CORE_PASS_UI_PENDING |
| REQ-019 | REQUIREMENT | Relatório: matriz de confusão de níveis | E-0001,E-0003,E-0007 | A-0006 | gold protocol + T008 calibration | confusion matrix + macro/per-level metrics | docs/report | GOLD_PROTOCOL_PASS_CALIBRATION_PENDING |
| REQ-020 | REQUIREMENT | Relatório: trade-offs custo/latência | E-0001,E-0003,E-0007 | — | W003-T007 telemetry + later provider evidence | cost/output + latency distributions | docs/report | READY |
| REQ-021 | REQUIREMENT | README/instruções claras de reprodutibilidade | E-0001,E-0006,E-0007 | — | clean-start release / B14 | reproduction pass | README | OPEN |
| REQ-022 | REQUIREMENT | Vídeo comprova código/interface reais | E-0001,E-0003,E-0006 | A-0001 | evidence cockpit + B14 demo protocol | real code/UI shown | video | BLOCKED_BY_PRODUCT_PROOF |
| REQ-023 | REQUIREMENT | Duração vídeo: máximo seguro 5 min | E-0001,E-0003 | A-0001 | target 4:40 + reserve | runtime <=5:00 | video | CONTROLLED |
| REQ-024 | REQUIREMENT | Não publicar em redes/renderizar avatar/streaming ms | E-0001,E-0003 | — | scope guard | no scope creep | architecture/docs | CONTROLLED |
| PAIN-005 | PARTNER | Escalar conteúdo multi-audiência/multicanal com confiança | E-0002,E-0003,E-0005,E-0007 | A-0002,A-0003,A-0011 | transformation + trust + repair + telemetry | quality/time/rework/reuse proxies | partner value section | SUPPORTED_CORE_REPAIR_TELEMETRY_PENDING |
| CRIT-001 | CRITICAL | Nenhuma média compensa perda factual/requisito eliminatório | E-0001,E-0003,E-0005,E-0007 | — | hard-gate precedence + HybridDecision | zero critical violations | success scorecard | CORE_PASS_MUST_PRESERVE |

## Rules

- IDs podem ser `REQ-###`, `PAIN-###`, `CRIT-###`, `CLAIM-###`.
- Todo requisito obrigatório e critério explícito precisa de linha própria.
- Toda dor/outcome material do parceiro precisa de linha própria.
- Claim material deve apontar para evidência e, se aplicável, assumption ID.
- Antes da finalização, nenhum requisito obrigatório pode estar `OPEN`, `MISSING` ou sem `Deliverable location`.
- Mudança no briefing/feedback do parceiro exige revalidar linhas afetadas.
