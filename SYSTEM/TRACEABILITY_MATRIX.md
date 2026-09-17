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
- `E-0008` — W003-T006/T007: targeted repair + fresh hard-gate re-evaluation + telemetry auditável.
- `E-0009` — W003-T008: calibration/ablation/anti-gaming release gate; 8/8 focused tests PASS; held-out rejection, target≠gold, hard-gate non-compensation, anti-gaming PASS e `DIAGNOSTIC_ONLY` posture.
- `E-0010` — W003-T009: end-to-end mechanics proof; exact 9 jobs, one local quality repair, one independent transport retry, persistent RunStore reopen/resume, hard-gate non-compensation, telemetry lineage; worker head System Integrity + Foundation Regression PASS. Deterministic stub é mechanics-only.

## Matrix

| ID | Type | Source / requirement / pain | Evidence refs | Assumption refs | Solution element | Outcome / metric | Deliverable location | Status |
|---|---|---|---|---|---|---|---|---|
| PAIN-001 | PAIN | Documentos financeiros densos criam barreira para iniciantes/intermediários | E-0001,E-0003,E-0007,E-0009,E-0010 | — | audience contracts + 3×3 + gold/ACV + calibration gate | compreensão sem perda factual | app + relatório | MECHANICS_PASS_HUMAN_CALIBRATION_PENDING |
| PAIN-002 | PAIN | LLM simplifica por encurtamento e perde nuances | E-0001,E-0003,E-0005,E-0007,E-0008,E-0010 | A-0003 | factual backbone + claim grounding + concept floors + targeted repair | concept/anchor preservation + local repair | evaluator + relatório | E2E_CONTROLLED_PROOF_PASS |
| PAIN-003 | PAIN | LLM-as-a-judge genérico é subjetivo/enviesado | E-0001,E-0002,E-0003,E-0007,E-0009 | A-0010 | hard gates + independent gold protocol + semantic ablation gate | calibrated hybrid evaluation | eval framework | ANTI_CIRCULAR_GATE_PASS_ABLATION_PENDING |
| PAIN-004 | PAIN | Ambiente financeiro/profissional exige rigor/auditabilidade | E-0001,E-0002,E-0005,E-0007,E-0008,E-0009,E-0010 | — | provenance + RunStore + repair lineage + telemetry + release gate | reconstructible audit trail | cockpit + docs | E2E_AUDITABLE_COCKPIT_PENDING |
| REQ-001 | REQUIREMENT | Ingestão de documentos financeiros públicos reais em PDF/texto | E-0001,E-0004,E-0006 | A-0008 | source-trust contract + parser adapters | safe parse/source readiness | pipeline | FOUNDATION_PARTIAL_W004_BAKEOFF_READY |
| REQ-002 | REQUIREMENT | Workflow baseado em grafo com estado | E-0001,E-0004,E-0006,E-0007,E-0008,E-0010 | A-0005 | explicit graph/state + persistent RunStore | exact 9-job run, checkpoint/reopen/resume, lossless join | pipeline/architecture | E2E_MECHANICS_PASS |
| REQ-003 | REQUIREMENT | Gerar 3 níveis × 3 formatos | E-0001,E-0005,E-0007,E-0010 | — | VariantSpec + deterministic 3×3 planner | 9/9 jobs/source | app/demo | E2E_MECHANICS_PASS_REAL_PROVIDER_QUALITY_PENDING |
| REQ-004 | REQUIREMENT | Iniciante: sem jargão desacompanhado; foco prático | E-0001,E-0003,E-0007,E-0009 | A-0004,A-0006 | gold rubric + ontology/ACV + calibration gate | audience fit | evaluator | FEATURES_PASS_THRESHOLD_FREEZE_BLOCKED |
| REQ-005 | REQUIREMENT | Intermediário: vocabulário padrão; alocação/tendências | E-0001,E-0003,E-0007,E-0009 | A-0004,A-0006 | gold rubric + ontology/ACV + calibration gate | audience fit | evaluator | FEATURES_PASS_THRESHOLD_FREEZE_BLOCKED |
| REQ-006 | REQUIREMENT | Avançado: preservar jargão e profundidade analítica | E-0001,E-0003,E-0007,E-0009 | A-0004,A-0006 | gold rubric + ontology/ACV + calibration gate | audience fit | evaluator | FEATURES_PASS_THRESHOLD_FREEZE_BLOCKED |
| REQ-007 | REQUIREMENT | Texto/Artigo Analítico | E-0001,E-0005,E-0010 | — | typed Article + provenance | format validation | app | E2E_MECHANICS_PASS |
| REQ-008 | REQUIREMENT | Carrossel com gancho/corpo/conclusão | E-0001,E-0005,E-0010 | — | typed Carousel | structure pass | app | E2E_MECHANICS_PASS |
| REQ-009 | REQUIREMENT | Vídeo curto com tempo/ganchos e fala <=60s | E-0001,E-0005,E-0010 | — | typed ShortVideo | duration/structure pass | app | E2E_MECHANICS_PASS |
| REQ-010 | REQUIREMENT | Legibilidade estatística adaptada ao português | E-0001,E-0002,E-0003,E-0007,E-0009 | A-0009 | `ptbr-readability-v001` + anti-gaming/calibration gate | controlled readability diagnostics | eval framework | IMPLEMENTED_DIAGNOSTIC_ONLY |
| REQ-011 | REQUIREMENT | Domain Term Density + contextualização via glossário | E-0001,E-0003,E-0007,E-0009 | — | `finance-ptbr-v001` + ACV | density/context/recall | eval framework | IMPLEMENTED_DIAGNOSTIC_ONLY |
| REQ-012 | REQUIREMENT | Factuality & Grounding Checker contra fonte | E-0001,E-0003,E-0005,E-0007,E-0008,E-0009,E-0010 | — | deterministic backbone + claim HybridDecision | wrong value remains hard FAIL despite clean soft signals | evaluator/cockpit | E2E_HARD_GATE_PASS_PARTIAL_SCOPE |
| REQ-013 | REQUIREMENT | Refinement loop rejeita/reprocessa se limiar falhar | E-0001,E-0004,E-0007,E-0008,E-0010 | — | targeted branch repair | one controlled branch repair + fresh gate IDs | pipeline/demo | E2E_CONTROLLED_PROOF_PASS |
| REQ-014 | REQUIREMENT | Interface comparativa com métricas por nível | E-0001,E-0003,E-0006,E-0008,E-0009,E-0010 | — | W004-T001 evidence cockpit | side-by-side + provenance + telemetry + explicit unknowns | app | W004_T001_READY |
| REQ-015 | REQUIREMENT | GitHub com grafo funcional e contribuições consistentes | E-0001,E-0004,E-0005,E-0007,E-0008,E-0009,E-0010 | — | signal-aware DAG + graph/runstore + CI | reproducibility/history | GitHub | STRONG_PASS_CORE |
| REQ-016 | REQUIREMENT | Suíte automatizada/reprodutível de evals | E-0001,E-0003,E-0005,E-0007,E-0008,E-0009,E-0010 | A-0004,A-0010 | clean CI + focused suites | regression pass | tests + relatório | STRONG_PASS_CORE_RELEASE_E2E_CI_PENDING |
| REQ-017 | REQUIREMENT | Auto-correção baseada em feedback numérico | E-0001,E-0003,E-0007,E-0008,E-0010 | — | TargetedRepairLoop | branch-local FAIL→repair→fresh re-eval; siblings unchanged | demo + app | E2E_CONTROLLED_PROOF_PASS |
| REQ-018 | REQUIREMENT | Dashboard exibe rastreabilidade das fontes | E-0001,E-0002,E-0005,E-0007,E-0008,E-0010 | — | provenance + RunStore + telemetry + W004 cockpit | source/run/repair lineage | app | CORE_PASS_COCKPIT_READY |
| REQ-019 | REQUIREMENT | Relatório: matriz de confusão de níveis | E-0001,E-0003,E-0007,E-0009 | A-0006 | executable confusion harness + W004 human calibration | target→human + human→evaluator matrices | docs/report | HARNESS_PASS_OBSERVED_MATRIX_NOT_COMPUTABLE |
| REQ-020 | REQUIREMENT | Relatório: trade-offs custo/latência | E-0001,E-0003,E-0007,E-0008,E-0009,E-0010 | — | telemetry + W004 provider runs | latency + observed usage/cost only | docs/report | TELEMETRY_PASS_REAL_PROVIDER_EVIDENCE_PENDING |
| REQ-021 | REQUIREMENT | README/instruções claras de reprodutibilidade | E-0001,E-0006,E-0007,E-0010 | — | W004-T008 release packet | clean reproduction pass | README | W004_RELEASE_FANIN_PENDING |
| REQ-022 | REQUIREMENT | Vídeo comprova código/interface reais | E-0001,E-0003,E-0006,E-0008,E-0010 | A-0001 | cockpit + release proof | real code/UI shown | video | W004_RELEASE_PROOF_PENDING |
| REQ-023 | REQUIREMENT | Duração vídeo: máximo seguro 5 min | E-0001,E-0003 | A-0001 | target 4:40 + reserve | runtime <=5:00 | video | CONTROLLED |
| REQ-024 | REQUIREMENT | Não publicar em redes/renderizar avatar/streaming ms | E-0001,E-0003 | — | scope guard | no scope creep | architecture/docs | CONTROLLED |
| PAIN-005 | PARTNER | Escalar conteúdo multi-audiência/multicanal com confiança | E-0002,E-0003,E-0005,E-0007,E-0008,E-0009,E-0010 | A-0002,A-0003,A-0011 | transformation + trust + repair + telemetry + cockpit | quality/time/rework/reuse proxies | partner value section | MECHANICS_SUPPORTED_REPRESENTATIVE_VALUE_EVIDENCE_PENDING |
| CRIT-001 | CRITICAL | Nenhuma média compensa perda factual/requisito eliminatório | E-0001,E-0003,E-0005,E-0007,E-0008,E-0009,E-0010 | — | hard-gate precedence + HybridDecision | wrong factual value remains terminal non-PASS | success scorecard | E2E_CORE_PASS_MUST_PRESERVE |

## Rules

- IDs podem ser `REQ-###`, `PAIN-###`, `CRIT-###`, `CLAIM-###`.
- Todo requisito obrigatório e critério explícito precisa de linha própria.
- Toda dor/outcome material do parceiro precisa de linha própria.
- Claim material deve apontar para evidência e, se aplicável, assumption ID.
- Antes da finalização, nenhum requisito obrigatório pode estar `OPEN`, `MISSING` ou sem `Deliverable location`.
- Mudança no briefing/feedback do parceiro exige revalidar linhas afetadas.
