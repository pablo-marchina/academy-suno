# TASK LEDGER

Somente Orchestrator com lease ativo altera este arquivo.

## Status
`PLANNED | READY | RUNNING | BLOCKED | RESULT_RECEIVED | INTEGRATED | CANCELLED | STALE`

| Task ID | Attempt | Base State | Base Commit | Role | Status | Dependencies | Issue / PR | Integrated State |
|---|---|---:|---|---|---|---|---|---|
| BOOT-T001 | A01 | 0001 | legacy | Orchestrator | INTEGRATED | none | PR #1 | 0002 |
| BOOT-T002 | A01 | 0007 | 434123de90e2cebb8d60bb4020a90c09ec48bcab | Orchestrator | INTEGRATED | BOOT-T001 | Issue #2 | 0008 |
| W001-T001 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Researcher | INTEGRATED | none | Issue #10 | 0009 |
| W001-T002 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #11 | 0009 |
| W001-T003 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #12 | 0009 |
| W001-T004 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #13 | 0009 |
| W001-T005 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #14 | 0009 |
| W001-T006 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #15 | 0009 |
| W001-T007 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Builder/Writer | INTEGRATED | none | Issue #16 | 0009 |
| W001-T008 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Critic/Researcher | INTEGRATED | none | Issue #17 | 0009 |
| W001-T009 | A01 | 0010 | resolve-at-dispatch | Synthesizer | READY | W001-T002,W001-T003,W001-T004,W001-T005 | Issue #18 | — |
| W001-T010 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Synthesizer | PLANNED | W001-T001,W001-T006,W001-T007,W001-T008,W001-T009 | Issue #19 | — |

## W001 purpose

Validar os componentes de maior risco/impacto antes de build amplo: calibração de audiência, ontologia financeira, factuality/grounding, benchmark experimental, arquitetura, UX/demo e guardrails; depois sintetizar Hybrid Evaluator e arquitetura candidata.

## Integrated fan-out findings

- T001: tratar voz Suno como calibração suave; separar audiência, formato e source/content type.
- T002: Flesch PT-BR é sensor, não classificador único; usar vetor multidimensional calibrado.
- T003: métricas devem operar sobre conceitos normalizados, aliases e anti-jargon-stuffing.
- T004: factuality deve ser claim-centric, source-first, com veto determinístico para erros materiais.
- T005: golden/held-out independente, split por documento e duas matrizes de confusão evitam circularidade.
- T006: candidato mínimo é grafo explícito pequeno com backbone factual, fan-out 3x3 e targeted repair.
- T007: demo deve ser evidence cockpit com format-specific evaluators e FAIL→repair→PASS.
- T008: source-first content policy, hard fail para recomendação nova/drift e human-review triggers.

## Rules

Toda task deve apontar para hard gate, Success dimension, requisito/pain, assumption/risk ou dependency crítica. Reexecução cria novo attempt. RESULT_RECEIVED não significa integrado. Wave manifest é fonte do DAG. Para protocolo 1.6.0+, runtime status é reconstruído por `SYSTEM/TASK_SIGNALS.md` antes de qualquer atualização canônica.

## Next

Executar W001-T009 sobre os RESULTs integrados de T002–T005 com lifecycle signals. Depois liberar W001-T010 quando T009 estiver integrado.