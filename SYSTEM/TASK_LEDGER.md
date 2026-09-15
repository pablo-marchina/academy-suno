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
| W001-T009 | A01 | 0010 | 762598b64216ce4ec272a50dd49ecbea08e8ae59 | Synthesizer | INTEGRATED | W001-T002,W001-T003,W001-T004,W001-T005 | Issue #18 | 0011 |
| W001-T010 | A01 | 0011 | d6d7519f0e119d58509cbabdb5f636cac0698ff0 | Synthesizer | INTEGRATED | W001-T001,W001-T006,W001-T007,W001-T008,W001-T009 | Issue #19 | 0012 |
| W002-T001 | A01 | 0013 | resolve-at-dispatch | Builder | READY | none | Issue #33 | — |
| W002-T002 | A01 | 0013 | resolve-at-dispatch | Builder/Analyst | READY | none | Issue #34 | — |
| W002-T003 | A01 | 0013 | resolve-at-dispatch | Builder/Critic | READY | none | Issue #35 | — |
| W002-T004 | A01 | 0013 | resolve-at-dispatch | Builder | READY | none | Issue #36 | — |
| W002-T005 | A01 | 0013 | resolve-at-dispatch | Builder/Analyst | READY | none | Issue #37 | — |
| W002-T006 | A01 | 0013 | resolve-at-dispatch | Critic/Builder | READY | none | Issue #38 | — |
| W002-T007 | A01 | 0013 | resolve-after-fanin | Builder | PLANNED | W002-T001,W002-T002,W002-T006 | Issue #39 | — |
| W002-T008 | A01 | 0013 | resolve-after-fanin | Builder | PLANNED | W002-T001,W002-T003 | Issue #40 | — |
| W002-T009 | A01 | 0013 | resolve-after-fanin | Builder | PLANNED | W002-T001,W002-T004 | Issue #41 | — |
| W002-T010 | A01 | 0013 | resolve-after-fanin | Synthesizer/Builder | PLANNED | W002-T005,W002-T007,W002-T008,W002-T009 | Issue #42 | — |

## W001 outcome

W001 COMPLETE: source-first candidate, Hybrid Evaluator, trust-layer differentiation, evidence cockpit, build backlog B01–B14 and mandatory experiments EXP-A–I.

## W002 purpose

Atacar `FOUNDATION_CORRECTNESS_AND_EXPERIMENTAL_PROOF` com máximo paralelismo seguro. O fan-out inicial possui ownership paths disjuntos: domain contracts, parser fixtures/bakeoff, policy gates, format contracts, orchestration smoke test e factual adversarial fixtures. Micro-fan-in posterior libera B03/B04/B05 core integrations e síntese final.

## Rules

Toda task deve apontar para hard gate, Success dimension, requisito/pain, assumption/risk ou dependency crítica. Reexecução cria novo attempt. RESULT_RECEIVED não significa integrado. Wave manifest é fonte do DAG. Para protocolo 1.6.0+, runtime status é reconstruído por `SYSTEM/TASK_SIGNALS.md` antes de qualquer atualização canônica.

## Next

Despachar W002-T001…T006 após merge de STATE 0013 e bind de SHA exato nas Issues. Não executar T007…T010 antes das dependências.