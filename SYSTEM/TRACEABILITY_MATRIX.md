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
- `E-0010` — W003-T009: end-to-end mechanics proof; exact 9 jobs, one local quality repair, one independent transport retry, persistent RunStore reopen/resume, hard-gate non-compensation, telemetry lineage; deterministic stub é mechanics-only.
- `E-0011` — W004-T001…T004: evidence cockpit; 6-source/36-output corpus + annotation prep; parser/source-trust bakeoff; provider-neutral harness com external provider blocker explícito.
- `E-0012` — W004-T009/T010/T011: blind annotation operator; manual credential-safe provider workflow; README/evidence packet/demo storyboard/release-smoke runner, preservando external blockers.
- `E-0013` — W004-T012/T013: clean task-specific release smoke com 9/9 mechanics + persisted FAIL→PASS; primeiro blind review `NOT_PASS` separando gaps internos de blockers externos.
- `E-0014` — W004-T014/T015: app HTTP recipient-facing real aceita texto/PDF path/PDF upload com raw SHA/provenance/source trust/fail-closed ambiguity; relatório experimental + submission packet consolidados sem fabricar human/provider evidence.
- `E-0015` — W004-T016/T017: deterministic manual capture fallback + real GitHub Actions Playwright/Chromium recording. T017 run `35625349017` usou PDF BCB real SHA `4ac6a958cbff7571aad3f0125042f4b71890a70ec36e9ad9009b537e6458ce68`, gravou MP4 SHA `f04852fb11183e4e6bc8690d80c5ef26d6993edc6aa7ec71660b9e3b670c3bc4`, duração `7.200s`, DOM/content assertions e artifacts `10652146281`/`10652031268`.
- `E-0016` — W004-T018: revisão cega direta do artifact T017. F-008 duration PASS; F-001 PARTIAL porque o vídeo real de 7,2s é silencioso/rápido demais para cold-evaluator comprehension; F-002/F-003 tecnicamente remediados; F-007 artifact existe mas packet/README estão stale; BCB `SOURCE_BLOCKED/REVIEW_REQUIRED/LOW` confirmado como fail-closed correto por table-role ambiguity.

## Matrix

| ID | Type | Source / requirement / pain | Evidence refs | Assumption refs | Solution element | Outcome / metric | Deliverable location | Status |
|---|---|---|---|---|---|---|---|---|
| PAIN-001 | PAIN | Documentos financeiros densos criam barreira para iniciantes/intermediários | E-0001,E-0003,E-0007,E-0009,E-0010,E-0011,E-0014 | — | audience contracts + 3×3 + frozen corpus + gold/ACV + calibration gate | compreensão sem perda factual | app + relatório | FROZEN_CORPUS_READY_HUMAN_CALIBRATION_PENDING |
| PAIN-002 | PAIN | LLM simplifica por encurtamento e perde nuances | E-0001,E-0003,E-0005,E-0007,E-0008,E-0010,E-0013,E-0014 | A-0003 | factual backbone + claim grounding + concept floors + targeted repair | concept/anchor preservation + local repair | evaluator + relatório | CLEAN_E2E_CONTROLLED_PROOF_PASS |
| PAIN-003 | PAIN | LLM-as-a-judge genérico é subjetivo/enviesado | E-0001,E-0002,E-0003,E-0007,E-0009,E-0011 | A-0010 | hard gates + independent blind gold protocol + semantic ablation gate | calibrated hybrid evaluation | eval framework | ANTI_CIRCULAR_PREP_PASS_HUMAN_GOLD_PENDING |
| PAIN-004 | PAIN | Ambiente financeiro/profissional exige rigor/auditabilidade | E-0001,E-0002,E-0005,E-0007,E-0008,E-0010,E-0013,E-0014,E-0015,E-0016 | — | provenance + RunStore + repair lineage + telemetry + recipient app + recorded evidence | reconstructible audit trail | app + demo + docs | REAL_BROWSER_AUDIT_PROOF_PASS_FINAL_DEMO_REMEDIATION_OPEN |
| REQ-001 | REQUIREMENT | Ingestão de documentos financeiros públicos reais em PDF/texto | E-0001,E-0004,E-0006,E-0011,E-0014,E-0015,E-0016 | A-0008 | source-trust contract + role-aware parser gate + recipient ingest adapter | safe parse/source readiness + real PDF negative-control | pipeline/app/demo | RECIPIENT_RAW_INGEST_PASS_FAIL_CLOSED_TABLE_ROLE_CONFIRMED |
| REQ-002 | REQUIREMENT | Workflow baseado em grafo com estado | E-0001,E-0004,E-0006,E-0007,E-0008,E-0010,E-0013 | A-0005 | explicit graph/state + persistent RunStore | exact 9-job run, checkpoint/reopen/resume, lossless join | pipeline/architecture | CLEAN_E2E_MECHANICS_PASS |
| REQ-003 | REQUIREMENT | Gerar 3 níveis × 3 formatos | E-0001,E-0005,E-0007,E-0010,E-0011,E-0015 | — | VariantSpec + deterministic 3×3 planner + provider-neutral execution harness | 9/9 mechanics; real provider quality absent | app/demo | CLEAN_MECHANICS_PASS_REAL_PROVIDER_QUALITY_BLOCKED_EXTERNAL |
| REQ-004 | REQUIREMENT | Iniciante: sem jargão desacompanhado; foco prático | E-0001,E-0003,E-0007,E-0009,E-0011 | A-0004,A-0006 | frozen blind corpus + ontology/ACV + calibration gate | audience fit | evaluator | FROZEN_EVIDENCE_READY_HUMAN_LABELS_PENDING |
| REQ-005 | REQUIREMENT | Intermediário: vocabulário padrão; alocação/tendências | E-0001,E-0003,E-0007,E-0009,E-0011 | A-0004,A-0006 | frozen blind corpus + ontology/ACV + calibration gate | audience fit | evaluator | FROZEN_EVIDENCE_READY_HUMAN_LABELS_PENDING |
| REQ-006 | REQUIREMENT | Avançado: preservar jargão e profundidade analítica | E-0001,E-0003,E-0007,E-0009,E-0011 | A-0004,A-0006 | frozen blind corpus + ontology/ACV + calibration gate | audience fit | evaluator | FROZEN_EVIDENCE_READY_HUMAN_LABELS_PENDING |
| REQ-007 | REQUIREMENT | Texto/Artigo Analítico | E-0001,E-0005,E-0010,E-0011,E-0015 | — | typed Article + provenance | format validation | app/demo | E2E_MECHANICS_PASS |
| REQ-008 | REQUIREMENT | Carrossel com gancho/corpo/conclusão | E-0001,E-0005,E-0010,E-0011,E-0015 | — | typed Carousel | structure pass | app/demo | E2E_MECHANICS_PASS |
| REQ-009 | REQUIREMENT | Vídeo curto com tempo/ganchos e fala <=60s | E-0001,E-0005,E-0010,E-0011,E-0015 | — | typed ShortVideo | duration/structure pass | app/demo | E2E_MECHANICS_PASS |
| REQ-010 | REQUIREMENT | Legibilidade estatística adaptada ao português | E-0001,E-0002,E-0003,E-0007,E-0009,E-0011 | A-0009 | `ptbr-readability-v001` + frozen human-calibration set | controlled readability diagnostics | eval framework | IMPLEMENTED_DIAGNOSTIC_ONLY_HUMAN_CAL_PENDING |
| REQ-011 | REQUIREMENT | Domain Term Density + contextualização via glossário | E-0001,E-0003,E-0007,E-0009,E-0011 | — | `finance-ptbr-v001` + ACV + frozen human-calibration set | density/context/recall | eval framework | IMPLEMENTED_DIAGNOSTIC_ONLY_HUMAN_CAL_PENDING |
| REQ-012 | REQUIREMENT | Factuality & Grounding Checker contra fonte | E-0001,E-0003,E-0005,E-0007,E-0008,E-0010,E-0013,E-0014,E-0016 | — | deterministic backbone + claim HybridDecision + role-aware source gate | wrong value/role/unit cannot become PASS; ambiguous table role blocks | evaluator/cockpit | CLEAN_E2E_HARD_GATE_PASS_FAIL_CLOSED_DEMO_CONFIRMED |
| REQ-013 | REQUIREMENT | Refinement loop rejeita/reprocessa se limiar falhar | E-0001,E-0004,E-0007,E-0008,E-0010,E-0013,E-0015 | — | targeted branch repair | persisted branch-local FAIL→repair→fresh re-eval | pipeline/demo | CLEAN_E2E_CONTROLLED_PROOF_PASS |
| REQ-014 | REQUIREMENT | Interface comparativa com métricas por nível | E-0001,E-0003,E-0006,E-0010,E-0011,E-0014,E-0015,E-0016 | — | evidence cockpit + recipient app | 3×3 side-by-side + states + provenance | app/demo | INTERACTIVE_RECIPIENT_APP_TECHNICAL_PASS_FINAL_DEMO_PACKAGING_T019 |
| REQ-015 | REQUIREMENT | GitHub com grafo funcional e contribuições consistentes | E-0001,E-0004,E-0005,E-0007,E-0008,E-0010,E-0013,E-0015 | — | signal-aware DAG + graph/runstore + CI | reproducibility/history | GitHub | STRONG_PASS_CORE |
| REQ-016 | REQUIREMENT | Suíte automatizada/reprodutível de evals | E-0001,E-0003,E-0005,E-0007,E-0008,E-0009,E-0010,E-0011,E-0012,E-0013,E-0015 | A-0004,A-0010 | clean CI + release/video capture tests | regression pass | tests + relatório | CLEAN_TASK_SPECIFIC_CI_PASS |
| REQ-017 | REQUIREMENT | Auto-correção baseada em feedback numérico | E-0001,E-0003,E-0007,E-0008,E-0010,E-0013,E-0015 | — | TargetedRepairLoop + recipient evidence lineage | FAIL→repair→fresh re-eval recorded | demo + app | CLEAN_E2E_CONTROLLED_PROOF_PASS |
| REQ-018 | REQUIREMENT | Dashboard exibe rastreabilidade das fontes | E-0001,E-0002,E-0005,E-0007,E-0008,E-0010,E-0011,E-0014,E-0015,E-0016 | — | cockpit + recipient provenance view | source/run/job/attempt/repair lineage | app/demo | INTERACTIVE_TRACEABILITY_TECHNICAL_PASS_FINAL_DEMO_PACKAGING_T019 |
| REQ-019 | REQUIREMENT | Relatório: matriz de confusão de níveis | E-0001,E-0003,E-0007,E-0009,E-0011,E-0012,E-0014 | A-0006 | frozen blind set + agreement/adjudication tooling | target→human + human→evaluator matrices | docs/report | OPERATOR_READY_OBSERVED_MATRIX_PENDING_TWO_HUMANS |
| REQ-020 | REQUIREMENT | Relatório: trade-offs custo/latência | E-0001,E-0003,E-0007,E-0008,E-0010,E-0011,E-0012,E-0014 | — | telemetry + provider-neutral harness + official-pricing guard | observed latency/usage/cost only | docs/report | MANUAL_PATH_READY_REAL_PROVIDER_RUN_BLOCKED_EXTERNAL |
| REQ-021 | REQUIREMENT | README/instruções claras de reprodutibilidade | E-0001,E-0006,E-0007,E-0010,E-0011,E-0012,E-0013,E-0014,E-0016 | — | README + evidence packet + consolidated report + capture provenance | clean reproduction + obvious evaluator start | README + docs/report | REPRODUCIBILITY_PASS_EVALUATOR_JOURNEY_REFRESH_T019 |
| REQ-022 | REQUIREMENT | Vídeo comprova código/interface reais | E-0001,E-0003,E-0006,E-0008,E-0010,E-0013,E-0014,E-0015,E-0016 | A-0001 | recipient app + real browser capture + final paced walkthrough | real code/UI technical proof exists; communication quality pending | video artifact | TECHNICAL_PASS_T017_EVALUATOR_USABILITY_NOT_PASS_T018_T019_REQUIRED |
| REQ-023 | REQUIREMENT | Duração vídeo: máximo seguro 5 min | E-0001,E-0003,E-0013,E-0015,E-0016 | A-0001 | measured MP4 + hard duration gate | observed `7.200s <= 300s`; final T019 must also pass | video artifact | ACTUAL_DURATION_PASS_T017_FINAL_ARTIFACT_REMEASURE_T019 |
| REQ-024 | REQUIREMENT | Não publicar em redes/renderizar avatar/streaming ms | E-0001,E-0003 | — | scope guard | no scope creep | architecture/docs | CONTROLLED |
| PAIN-005 | PARTNER | Escalar conteúdo multi-audiência/multicanal com confiança | E-0002,E-0003,E-0005,E-0007,E-0008,E-0010,E-0011,E-0014,E-0015,E-0016 | A-0002,A-0003,A-0011 | transformation + trust + repair + telemetry + recipient evidence UX | quality/time/rework/reuse proxies | partner value section | TECHNICAL_PROOF_STRONG_HUMAN_PROVIDER_PROOF_PENDING |
| CRIT-001 | CRITICAL | Nenhuma média compensa perda factual/requisito eliminatório | E-0001,E-0003,E-0005,E-0007,E-0008,E-0009,E-0010,E-0013,E-0015,E-0016 | — | hard-gate precedence + explicit blind review | hard failures/gaps remain terminal/non-hidden | success scorecard | CORE_PASS_FINAL_DEMO_AND_EXTERNAL_GATES_OPEN |

## Rules

- IDs podem ser `REQ-###`, `PAIN-###`, `CRIT-###`, `CLAIM-###`.
- Todo requisito obrigatório e critério explícito precisa de linha própria.
- Toda dor/outcome material do parceiro precisa de linha própria.
- Claim material deve apontar para evidência e, se aplicável, assumption ID.
- Antes da finalização, nenhum requisito obrigatório pode estar `OPEN`, `MISSING` ou sem `Deliverable location`.
- Mudança no briefing/feedback do parceiro exige revalidar linhas afetadas.
