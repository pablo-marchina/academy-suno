# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0029`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 6 — Adversarial Optimization`

`LAST_COMMITTED_WAVE: W004-PACED-FINAL-DEMO-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE;
- W004-T001/T002/T003/T009/T010/T011/T012/T013/T014/T015/T017/T018/T019 estão INTEGRATED;
- W004-T004 A01 permanece `BLOCKED_EXTERNAL_PROVIDER_ACCESS`: não existe run credenciado real de provider com quality/latency/usage/cost observados;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- T018 manteve `BLIND_REVIEW: NOT_PASS` para o artifact T017 de 7,2s por insuficiência de comunicação evaluator-facing, embora existência/duração técnicas tenham passado;
- T019 remediou esse gap em task scope sem autoaprovação: GitHub Actions run `35636285651` produziu demo real deliberadamente paced da app recipient-facing, com success path `SOURCE_READY/PASS` primeiro e BCB fail-closed safety negative-control depois;
- o MP4 final T019 tem SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, duração observada `69.12s <= 300s`, H.264 1280×720 a 25 fps, sem áudio, com captions/hold-times visíveis para tornar a jornada compreensível sem contexto oculto;
- primary Actions artifact T019: `10656720873`, digest `sha256:7b7435c4d7c64428da12e6bd8ba973fc57010b74f941dcf9f7099bf169c64982`; provenance artifact `10656775849`, digest `sha256:0f8e8e786afca176a19b9d0c70c18b9134a37ee91d234dc53a87286b38c692b0`; ambos reportam expiração em `2026-12-20T18:06:45Z`;
- T019 mostrou text source real/controlada em `SOURCE_READY/PASS`, hash exato, 9/9 audience×format mechanics cells, persisted `FAIL → repair → PASS`, evidence boundaries, e em seguida PDF público real do BCB permanecendo corretamente `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` por `TABLE_ROLE_AMBIGUITY`, sem bypass;
- nove frames representativos foram decodificados do MP4 final pós-conversão e validados contra screenshots do mesmo estado; todos PASS;
- README raiz e `docs/submission/SUBMISSION_PACKET.md` foram atualizados para a verdade pós-T019 e apontam o recipient app/evidence path;
- `BLIND_REVIEW` permanece `NOT_PASS` até T020 inspecionar independentemente o artifact T019; T019 não pode aprovar a própria demo;
- W004-T020 está READY após post-merge bind para blind/adversarial review final do pacote + concrete T019 demo;
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
- `W004-T018` — direct blind review of T017 — Issue #118 / PR #120 — `NOT_PASS` for evaluator usability.
- `W004-T019` — paced final demo + evaluator-facing package refresh — Issue #121 / PR #124 / Actions run `35636285651`.

### BLOCKED external/fallback evidence
- `W004-T004-A01` — real provider execution unavailable — Issue #84.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.
- `W004-T016-A01` — worker-local screen recording unavailable; deterministic manual fallback retained — Issue #109 / PR #114.

### READY after post-merge bind
- `W004-T020-A01` — independent blind/adversarial review of current package + concrete T019 final demo — Issue #122.

### PLANNED
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires valid human evidence + observed provider runs.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007.

## Current success bottleneck

`INDEPENDENT_FINAL_DEMO_REVIEW_PLUS_EXTERNAL_HUMAN_PROVIDER_EVIDENCE`

T019 materially remediou o gap interno de comunicação: existe agora um walkthrough real de 69.12s, success-path-first, com captions/hold-times, 9/9 mechanics, repair lineage, provenance e BCB fail-closed negative-control. O próximo gate interno é T020 julgar cegamente o artifact concreto e o pacote atualizado. Em paralelo, human gold independente e provider execution real continuam blockers externos irredutíveis.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- F-001/video evaluator usability só pode ser promovido se T020 confirmar o artifact T019 concreto; task-scope PASS de T019 não substitui revisão independente;
- o PDF BCB deve permanecer fail-closed enquanto faltar cell-role provenance; no demo-only bypass;
- artifact final deve ser copiado para storage de submissão durável se o horizonte puder ultrapassar `2026-12-20T18:06:45Z`, preservando SHA/digest/provenance;
- production/release readiness somente após human/provider prerequisites + W004-T008 + final reviews.

## Next action

1. mergear STATE 0029 e bindar W004-T020 à `main` exata;
2. executar T020 sobre README/submission packet + concrete T019 MP4/artifacts;
3. se T020 aprovar o video/package scope, encerrar o gap interno de demo sem converter isso em overall release PASS;
4. se T020 encontrar novo gap crítico/high interno, remediar antes do final fan-in;
5. manter #84/#85 como blockers externos;
6. quando dois humanos concluírem exports válidos via T009, iniciar novo attempt de T005;
7. quando credential autorizado existir, executar T010 e reavaliar T004/T007.

## Recovery point

Retomar de `STATE_VERSION 0029` e `SYSTEM/CHECKPOINTS/STATE-v0029.md`. T019 está integrado com demo final paced concreta; T020 é o próximo worker interno seguro; T004/T005 continuam external-blocked.
