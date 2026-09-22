# QUALITY SCORECARD

`QUALITY_MODEL_VERSION: 1.3`

`SCORECARD_VERSION: 0023`

`QUALITY_STATUS: W004_CASE_QUALITY_PASS_PRODUCTION_QUALITY_ACTIVE`

`STOP_CONDITION: FAIL`

## Contract status

- Case objective/deliverables: `KNOWN / W004 INTERNAL PACKAGE PRESENT`
- Production Contract: `ACTIVE / PROD-001..017 OPEN`
- Explicit evaluation criteria: `CASE + PRODUCTION HARD GATES IDENTIFIED`
- Evaluation weights/scale: `NOT PROVIDED`
- Output audiences: `3 KNOWN / FINAL EVALUATOR UNKNOWN`
- Constraints/deadline: `SCOPE + VIDEO HARD GATE KNOWN / DATE UNKNOWN`
- Decision Research Gate: `ACTIVE`

## Current evaluation

W004 remains a strong case-quality baseline: functional graph, exact 3×3, hybrid evaluator, fail-closed grounding, repair, clean CI, observed provider trade-offs and independently reviewed real-browser video. D-0018 intentionally reopens quality because the target is now a production-grade multi-user product rather than only a bounded case proof.

No production stack is locked by this scorecard. Material choices require DRG evidence.

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

15. authenticated multi-user product — `OPEN`;
16. tenant/workspace isolation + authz tests — `OPEN`;
17. production API + secure upload boundary — `OPEN`;
18. shared durable persistence/object storage — `OPEN`;
19. real provider path in final UI — `OPEN`;
20. Eval-Driven CI/offline experiments — `OPEN`;
21. human-calibrated audience production evidence — `OPEN`;
22. adaptive policy with deterministic safety invariants — `OPEN`;
23. live architecture/output/eval/trace/cost/health cockpit — `OPEN`;
24. observability coverage — `OPEN`;
25. load/recovery/backup/restore evidence — `OPEN`;
26. threat model/security evidence — `OPEN`;
27. reproducible deployment — `OPEN`;
28. DRG records for all material production choices — `OPEN`;
29. final production blind review/video — `OPEN`;
30. submission logistics/deadline/final reserve — `UNKNOWN_EXTERNAL`.

## Evidence boundaries

- D-0017 does not authorize human/production calibration claims.
- `PRODUCTION_READY` remains false until Production Contract hard gates pass.
- W004 demo is preserved evidence, not final production evidence after material implementation changes.
- No framework/provider/database/frontend winner exists until DRG evidence supports one.

## Current quality bottleneck

`SYSTEMATIC_PRODUCTION_RESEARCH_AND_ARCHITECTURE_SELECTION`

## Next quality action

Execute W005 research/bakeoff tasks, then synthesize candidate architecture with explicit `LOCK | NO_PREFERENCE | PENDING_EVIDENCE` outcomes. Only afterward start production implementation waves.
