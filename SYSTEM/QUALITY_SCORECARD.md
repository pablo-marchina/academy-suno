# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.3`

`SCORECARD_VERSION: 0025`

`QUALITY_STATUS: W004_CASE_QUALITY_PASS_W005_PRODUCTION_RESEARCH_READY`

`STOP_CONDITION: FAIL`

## Contract status

- Case objective/deliverables: `KNOWN / W004 INTERNAL PACKAGE PRESENT`
- Production Contract: `ACTIVE / PROD-001..017 OPEN`
- Explicit evaluation criteria: `CASE + PRODUCTION HARD GATES IDENTIFIED`
- Evaluation weights/scale: `NOT PROVIDED`
- Output audiences: `3 KNOWN / FINAL EVALUATOR UNKNOWN`
- Constraints/deadline: `SCOPE + VIDEO HARD GATE KNOWN / DATE UNKNOWN`
- Decision Research Gate: `ACTIVE / W005 COVERAGE RECONCILED AND READY`

## Current evaluation

W004 remains a strong case-quality baseline: functional graph, exact 3×3, hybrid evaluator, fail-closed grounding, repair, clean CI, observed provider trade-offs and independently reviewed real-browser video. D-0018 intentionally reopened quality because the target is now a production-grade multi-user product rather than only a bounded case proof.

The readiness review expanded W005 before any worker started. Eleven parallel research/bakeoff inputs now cover the production architecture decision surface, including two material areas absent from the original fan-out: developer platform/repository/package/build/test/CI-CD (`T013`) and financial document parsing/extraction/source-grounding (`T014`). T010–T012 remain gated synthesis/red-team/final-fan-in. No production stack is locked by this scorecard or by wave creation.

## Preserved W004 hard gates

1. pipeline funcional baseado em estado/grafo — `PASS_BASELINE`;
2. cobertura 3 níveis × 3 formatos — `PASS_MECHANICS / CALIBRATION_DIAGNOSTIC`;
3. framework híbrido — `PASS_EVIDENCE_BOUNDED`;
4. legibilidade PT-BR — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
5. densidade/contextualização financeira — `IMPLEMENTED_DIAGNOSTIC_ONLY`;
6. factuality/grounding — `PASS_TESTED_SCOPE_FAIL_CLOSED`;
7. auto-correção — `PASS_FAIL_TO_REPAIR_TO_PASS`;
8. interface comparativa/rastreabilidade — `PASS_W004_SCOPE`;
9. testes/reprodutibilidade — `PASS_CLEAN_CI`;
10. audience calibration — `MODEL_AUTOMATED_ONLY / NO_HUMAN_GOLD`;
11. custo/latência — `PASS_BOUNDED_OBSERVED`;
12. README/report — `PASS_W004_INTERNAL_PACKAGE`;
13. vídeo real <=5:00 — `PASS_69_120S_W004`;
14. final clean-E2E — `PASS_T008_A02`.

## New production hard gates

15. authenticated multi-user product — `OPEN / W005-T001,T004`;
16. tenant/workspace isolation + authz tests — `OPEN / W005-T004`;
17. production API + secure upload boundary — `OPEN / W005-T002,T004`;
18. shared durable persistence/object storage — `OPEN / W005-T003,T004`;
19. financial parser/source-grounding production evidence — `OPEN / W005-T014`;
20. real provider path in final UI — `OPEN / W005-T002,T006`;
21. Eval-Driven offline/CI/online experiments — `OPEN / W005-T005,T009,T013`;
22. human-calibrated audience production evidence — `OPEN / W005-T005`;
23. adaptive policy with deterministic safety invariants — `OPEN / W005-T006`;
24. live architecture/output/eval/trace/cost/health cockpit — `OPEN / W005-T002,T007`;
25. observability coverage — `OPEN / W005-T007`;
26. load/recovery/backup/restore evidence — `OPEN / W005-T008,T009`;
27. threat model/security evidence — `OPEN / W005-T004,T007,T014,T011`;
28. reproducible developer platform/dependency/build/test/CI-CD path — `OPEN / W005-T013`;
29. reproducible deployment — `OPEN / W005-T008,T013`;
30. DRG records for all material production choices — `ACTIVE / W005-T001..T010,T013,T014`;
31. final production blind review/video — `OPEN AFTER BUILD`;
32. submission logistics/deadline/final reserve — `UNKNOWN_EXTERNAL`.

## Evidence boundaries

- D-0017 does not authorize human/production calibration claims.
- `PRODUCTION_READY` remains false until Production Contract hard gates pass.
- W004 demo is preserved evidence, not final production evidence after material implementation changes.
- No framework/provider/database/parser/frontend/toolchain winner exists until W005 DRG evidence supports one.

## Current quality bottleneck

`W005_SYSTEMATIC_RESEARCH_EXECUTION_AND_EVIDENCE_FANIN`

## Next quality action

Run W005-T001..T009 plus T013/T014 in parallel. Accept only results with valid task provenance, systematic research coverage, quantitative benchmark/method evidence where testable and explicit uncertainty. Then T010 must synthesize all eleven inputs; T011 must independently red-team; T012 must close findings and produce the Phase 9 implementation DAG.
