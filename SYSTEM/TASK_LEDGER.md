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
| W002-T001 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder | INTEGRATED | none | Issue #33 | 0014 |
| W002-T002 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder/Analyst | INTEGRATED | none | Issue #34 | 0014 |
| W002-T003 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder/Critic | INTEGRATED | none | Issue #35 | 0014 |
| W002-T004 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder | INTEGRATED | none | Issue #36 | 0014 |
| W002-T005 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder/Analyst | INTEGRATED | none | Issue #37 | 0014 |
| W002-T006 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Critic/Builder | INTEGRATED | none | Issue #38 | 0014 |
| W002-T007 | A01 | 0014 | 988beae91aad40acbcdd3189bdf8f0d2e216c832 | Builder | INTEGRATED | W002-T001,W002-T002,W002-T006 | Issue #39 / PR #56 | 0015 |
| W002-T008 | A01 | 0014 | 988beae91aad40acbcdd3189bdf8f0d2e216c832 | Builder | INTEGRATED | W002-T001,W002-T003 | Issue #40 / PR #54 | 0015 |
| W002-T009 | A01 | 0014 | 988beae91aad40acbcdd3189bdf8f0d2e216c832 | Builder | INTEGRATED | W002-T001,W002-T004 | Issue #41 / PR #55 | 0015 |
| W002-T010 | A01 | 0015 | resolve-after-merge | Synthesizer/Builder | READY | W002-T005,W002-T007,W002-T008,W002-T009 | Issue #42 | — |

## W001 outcome

W001 COMPLETE: source-first candidate, Hybrid Evaluator, trust-layer differentiation, evidence cockpit, build backlog B01–B14 and mandatory experiments EXP-A–I.

## W002 integrated foundation outcome

- T001: canonical Pydantic domain/provenance spine.
- T002/EXP-A: source trust requires semantic table-role provenance; parser library remains unlocked.
- T003/T008: executable policy engine integrated to canonical domain; FAIL > REVIEW_REQUIRED > PASS; `HF-11` kept for untraceable source mixing.
- T004/T009: native Article/Carousel/ShortVideo contracts reconciled with canonical enums/provenance; deterministic 3×3 planner; format suite 14/14 and generation suite 4/4 passed.
- T005/EXP-B: plain async executed required semantics; LangGraph remains pending runtime recheck.
- T006/T007: factual-v001 oracle + executable factual backbone; 13/13 factual tests pass and oracle comparison passes; known CRITICAL mutations cannot auto-PASS.

## Rules

Toda task deve apontar para hard gate, Success dimension, requisito/pain, assumption/risk ou dependency crítica. Reexecução cria novo attempt. RESULT_RECEIVED não significa integrado. Wave manifest é fonte do DAG. Para protocolo 1.6.0+, runtime status é reconstruído por `SYSTEM/TASK_SIGNALS.md` antes de qualquer atualização canônica.

## Next

W002-T010 está READY após integração de T005/T007/T008/T009. Após o merge de STATE 0015, bindar o SHA exato de main na Issue #42/dispatch antes de iniciar o worker.