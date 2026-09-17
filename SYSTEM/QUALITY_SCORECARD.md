# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.1`

`SCORECARD_VERSION: 0012`

`QUALITY_STATUS: W004_COCKPIT_CORPUS_PARSER_READY_HUMAN_PROVIDER_EVIDENCE_PENDING`

`STOP_CONDITION: FAIL`

## Case Contract status

- Objective: `KNOWN`
- Mandatory deliverables: `6 DELIVERABLES IDENTIFIED`
- Explicit evaluation criteria: `REQUIREMENTS/HARD GATES IDENTIFIED`
- Evaluation weights/scale: `NOT PROVIDED`
- Audience: `3 OUTPUT AUDIENCES KNOWN / FINAL EVALUATOR UNKNOWN`
- Constraints/deadline: `SCOPE + VIDEO HARD GATE KNOWN / DATE UNKNOWN`
- Partner Outcome linkage: `VALUE_HYPOTHESIS_SUPPORTED_EXECUTION_ADVANCED`

## Current evaluation

W004 initial fanout moved the project from mechanics-only toward partner-visible evidence: the comparative cockpit exists, the development corpus is broader and frozen, and parser/source-trust hard gates generalize across three primary-source families. Human calibration is still unobserved and provider execution is externally blocked; therefore no audience threshold/provider preference/release readiness is promoted.

## Hard gates

Status: `ACTIVE_HUMAN_CALIBRATION_AND_RELEASE_PROOF`

1. pipeline funcional baseado em estado/grafo — `CORE_PASS`;
2. cobertura 3 níveis × 3 formatos — `MECHANICS_PASS / REAL_PROVIDER_QUALITY_PENDING`;
3. framework híbrido determinístico — `CORE_PASS_PARTIAL_SCOPE`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `CORE_PASS_PARTIAL_SCOPE`; parser role hard gates strengthened;
7. auto-correção mensurável — `E2E_CONTROLLED_PROOF_PASS`;
8. interface comparativa com métricas/rastreabilidade — `IMPLEMENTED_W004_T001 / RELEASE_VALIDATION_PENDING`;
9. testes automatizados/reprodutíveis — `STRONG_PASS_CORE_AND_WORKER_CI`; task-specific release E2E CI ainda pendente;
10. matriz de confusão dos níveis — `PREPARATION_READY / OBSERVED_HUMAN_MATRIX_PENDING_T005`;
11. análise custo/latência — `HARNESS_PASS / REAL_PROVIDER_RUN_BLOCKED_EXTERNAL`;
12. README/documentação reproduzível — `PARTIAL`; cockpit/parser/provider docs exist, release README pending;
13. vídeo real comprovando código/interface — `PENDING`;
14. vídeo <=5:00 — `CONTROLLED_BY_PLAN`.

## W004 initial evidence

- T001 cockpit preserves explicit evidence states, provenance, 3×3 comparison, repair lineage and telemetry; no aggregate score hides FAIL/REVIEW/N/A;
- T002 freezes 36 development outputs from 4 development sources within a 6-source manifest, keeps 2 sources held-out and prepares blind double annotation/adjudication/agreement tooling;
- T003 demonstrates 100% value coverage can still be source-unsafe when table/row/column/unit/period roles are wrong; 8/8 focused tests PASS; parser identity remains unlocked;
- T004 provider harness preserves N/A when unobserved, rejects synthetic pricing as commercial evidence and returns explicit blocker without credential; real provider quality/latency/usage/cost remain unknown;
- T001/T002 worker heads and T003/T004 staging evidence passed clean GitHub CI gates before final combined fan-in validation.

## Open quality gaps

1. two genuinely independent human annotation streams + agreement/adjudication over frozen development set;
2. observed target→human and human→evaluator matrices and any evidence-supported threshold decision;
3. semantic-on/off ablation on the same independent development gold;
4. credentialed comparable provider/model runs with observed quality/latency/usage/cost;
5. same-raw-byte parser comparison/OCR coverage if parser implementation lock is required;
6. task-specific clean-E2E release proof, final README/report, video and adversarial final reviews.

## Next quality action

Execute W004-T005. If independent human annotations cannot be obtained, return BLOCKED rather than pseudo-labeling. After T005, release T006; T007 remains blocked until T004 receives real provider-run evidence.