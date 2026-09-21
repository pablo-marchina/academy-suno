# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0028`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 6 — Adversarial Optimization`

`LAST_COMMITTED_WAVE: W004-BLIND-VIDEO-REVIEW-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE;
- W004-T001/T002/T003/T009/T010/T011/T012/T013/T014/T015/T017/T018 estão INTEGRATED;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`; não existe run credenciado real de provider com quality/latency/usage/cost observados;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- T014 implementa app recipient-facing real de texto/PDF; T015 consolida relatório/submission packet; T017 prova captura técnica real em browser/CI com PDF público e MP4 `7.200s <= 300s`;
- T018 inspecionou diretamente o artifact T017 e manteve `BLIND_REVIEW: NOT_PASS`: o vídeo de 7,2s é real, hash-bound e dentro do limite, porém silencioso/rápido demais para uma demonstração final inteligível;
- T018 observou que o PDF BCB real aparece corretamente como `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` por `TABLE_ROLE_AMBIGUITY`; isso é comportamento fail-closed desejado e não deve ser relaxado para produzir uma demo verde;
- F-002 (ingestão real) e F-003 (interface interativa) estão tecnicamente corrigidos; F-007 (relatório consolidado) existe, mas README/submission packet estão temporalmente desatualizados em relação a T014/T017/T018;
- F-008, duração <=5:00, tem evidência concreta PASS para T017; F-001 permanece PARTIAL porque existência técnica de vídeo não equivale a demo evaluator-facing suficiente;
- W004-T019 está materializada como remediação final interna: produzir walkthrough deliberadamente paced, mostrar primeiro um caminho real `SOURCE_READY/PASS` com 9/9 3×3 + provenance + repair evidence, e depois usar o BCB bloqueado como negative-control explicitamente rotulado; também deve atualizar README/submission packet com o artifact final exato;
- W004-T020 está PLANNED como blind/adversarial review independente após T019;
- audience thresholds continuam `DIAGNOSTIC_ONLY`; target→human/human→evaluator matrices seguem indisponíveis; semantic backend e provider/model permanecem sem preferência baseada em evidência;
- W004-T006 permanece dependente de T005; W004-T007 depende de T004/T005; W004-T008 continua fan-in final dependente de human/provider evidence válida;
- deadline, submission mechanism, owner/decision maker e workflow interno Suno permanecem UNKNOWN.

## Locked decisions

- `D-0001` GitHub canônico.
- `D-0002` Workers não integram.
- `D-0003` Paralelismo versionado.
- `D-0004` Guardrails executáveis.
- `D-0005` Lease exclusivo.
- `D-0006` Proveniência por tentativa.
- `D-0007` Checkpoints/DAG.
- `D-0009` Loop até gates/stop.
- `D-0011` Partner Contract/Jury/Adoption.
- `D-0012` Balanced Total Success dominante.
- `D-0013` Traceability + assumptions gates.
- `D-0014` Blind Review + deadline reserve.
- `D-0015` Lifecycle de worker observável por sinais duráveis.
- `D-0016` Foundation invariants lockados; implementation identities permanecem evidence-driven.

## W004 lifecycle

### INTEGRATED
- `W004-T001` — evidence cockpit — Issue #81 / PR #93.
- `W004-T002` — corpus + blind human-calibration preparation — Issue #82 / PR #94.
- `W004-T003` — parser/source generalization bakeoff — Issue #83 / PR #91.
- `W004-T009` — blind annotation operator — Issue #95 / PR #100.
- `W004-T010` — credential-safe provider evidence path — Issue #96 / PR #101.
- `W004-T011` — README/demo/release hardening — Issue #97 / PR #99.
- `W004-T012` — clean release-smoke CI — Issue #102 / PR #105.
- `W004-T013` — first blind/adversarial review — Issue #103 / PR #106.
- `W004-T014` — recipient-facing PDF/text app — Issue #107 / PR #112.
- `W004-T015` — consolidated experimental report/submission packet — Issue #108 / PR #111.
- `W004-T017` — real CI browser demo capture — Issue #115 / PR #117 / Actions run `35625349017`.
- `W004-T018` — direct blind review of concrete T017 video — Issue #118 / PR #120 — `NOT_PASS` for evaluator usability.

### BLOCKED external/fallback evidence
- `W004-T004-A01` — real provider execution unavailable — Issue #84.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.
- `W004-T016-A01` — worker-local screen recording unavailable; deterministic manual fallback retained — Issue #109 / PR #114.

### READY after post-merge bind
- `W004-T019-A01` — paced final demo + evaluator-facing package refresh — Issue #121.

### PLANNED
- `W004-T020-A01` — independent blind review of T019 package + concrete final demo — Issue #122.
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires valid human evidence + observed provider runs.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007.

## Current success bottleneck

`EVALUATOR_USABLE_FINAL_DEMO_PLUS_EXTERNAL_HUMAN_PROVIDER_EVIDENCE`

A barreira técnica de captura foi superada, mas T018 demonstrou que o artifact atual não comunica o fluxo suficientemente bem. A próxima ação interna é T019: uma gravação real, deliberadamente paced, com success path primeiro e negative-control fail-closed depois, acompanhada de atualização do evaluator journey. Isso não substitui human gold nem provider execution.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- o final video só pode fechar F-001 se T020 confirmar que o artifact concreto é evaluator-usable; `<=5:00` isoladamente não basta;
- o PDF BCB deve permanecer fail-closed enquanto faltar cell-role provenance; no demo-only bypass;
- artifact final deve ter hash/duration/provenance e retenção explicitamente documentados;
- production/release readiness somente após human/provider prerequisites + W004-T008 + final review.

## Next action

1. mergear STATE 0028 e bindar W004-T019 à `main` exata;
2. executar T019;
3. se T019 produzir artifact evaluator-facing válido, integrar e liberar T020;
4. se T019 bloquear, manter F-001 aberto e usar o blocker para novo attempt sem relaxar source trust;
5. manter #84/#85 como blockers externos;
6. quando dois humanos concluírem exports válidos via T009, iniciar novo attempt de T005;
7. quando credential autorizado existir, executar T010 e reavaliar T004/T007.

## Recovery point

Retomar de `STATE_VERSION 0028` e `SYSTEM/CHECKPOINTS/STATE-v0028.md`. T018 está integrado; T019 é o próximo worker interno seguro; T004/T005 continuam external-blocked.
