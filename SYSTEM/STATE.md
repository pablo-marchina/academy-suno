# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0033`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 7 — Blind Review, Final Deliverable & Defense`

`LAST_COMMITTED_WAVE: W004-PROVIDER-MECHANICS-ACCEPTED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE;
- W004-T001/T002/T003/T004/T009/T010/T011/T012/T013/T014/T015/T017/T018/T019/T020/T021 estão INTEGRATED;
- W004-T004 foi fechado por tentativa aceita `A08`: Actions run `35664987180` usou o cliente OpenAI Python `2.11.0` no modo compatível oficialmente documentado pela Groq, fez Models preflight HTTP `200`, observou `13` modelos ativos e selecionou `openai/gpt-oss-120b`;
- a geração A08 retornou HTTP `200`, latência observada `349.694 ms`, usage `84` input / `61` output / `145` total tokens e custo derivado `4.92e-05 USD` a partir de snapshot oficial versionado de pricing Groq; provider-returned model foi `openai/gpt-oss-120b` e o response fingerprint SHA-256 foi `5a3466faf9d179f5da92cde5ad5de9e2227e9821c7260976040db466e7b8d3fc`;
- o envelope de mechanics A08 passou strict T007 import (`exit 0`) e fresh-clone remoto com byte verification; artifact Actions `10668547182`; secret material e raw generated text não foram persistidos;
- A04-A07 permanecem diagnósticos não aceitos. A06 ainda reproduziu HTTP 403 via raw `urllib`; A07 isolou resposta Cloudflare `error code: 1010`/`text/plain` sem Groq request-id; A08 resolveu o path usando o cliente compatível documentado, sem spoofing de browser headers;
- A08 satisfaz evidência de provider **mechanics** (auth/runtime/latency/usage/cost/provenance), mas não autoriza preferência de provider/model nem claim de content quality; comparação de qualidade continua dependente de human gold/T007;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- T019 produziu a demo final real da app recipient-facing: Actions run `35636285651`, MP4 SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, duração observada `69.12s <= 300s`, H.264 1280×720 a 25 fps, success path `SOURCE_READY/PASS` primeiro, 9/9 mechanics, persisted `FAIL → repair → PASS`, evidence boundaries e BCB fail-closed safety negative-control sem bypass;
- T020 baixou e verificou diretamente os artifacts aceitos, mediu novamente o MP4 em `69.120000s`, inspecionou frames independentes e concluiu `VIDEO_PACKAGE_REVIEW: PASS` com `NEW_CRITICAL_FINDINGS: 0` e `NEW_HIGH_FINDINGS: 0`;
- T021 A02 preservou byte-identically o MP4 aceito em `artifacts/submission/final-demo.mp4`, com source SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, `1388430` bytes e fresh-clone/read-back SHA/size + `cmp` PASS no Actions run `35651949452`;
- F-001/F-002/F-003/F-007/F-008 passam no escopo de video/package review; provider mechanics agora também têm evidence observada, mas isso não equivale a project/release/production readiness;
- audience thresholds continuam `DIAGNOSTIC_ONLY`; target→human/human→evaluator matrices seguem indisponíveis; semantic backend e provider/model preference permanecem sem lock baseado em evidência;
- W004-T006 permanece dependente de T005; W004-T007 tinha dependências T004/T005 e agora aguarda somente T005 na prática; W004-T008 continua fan-in final dependente de T005/T006/T007;
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
- `W004-T004` — accepted Groq provider mechanics — Issue #84 / accepted attempt A08 / PR #133 / Actions run `35664987180`.
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
- `W004-T020` — independent final blind/adversarial review — Issue #122 / PR #126 — `VIDEO_PACKAGE_REVIEW: PASS`.
- `W004-T021` — durable byte-identical accepted-video preservation — Issue #127 / accepted attempt A02 / PR #130 / Actions run `35651949452`.

### BLOCKED external/fallback evidence
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.
- `W004-T016-A01` — worker-local screen recording unavailable; deterministic manual fallback retained — Issue #109 / PR #114.

### PLANNED
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — T004 provider-mechanics prerequisite is satisfied; still requires valid T005 human evidence for quality comparison.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007.

## Current success bottleneck

`EXTERNAL_HUMAN_CALIBRATION_EVIDENCE`

Todos os gaps internos materiais conhecidos do vídeo/pacote, retenção do MP4 e provider mechanics foram fechados no escopo aplicável. T004 A08 provou runtime real Groq com auth, model discovery, generation, latency, usage, official-pricing-derived cost e downstream import. O blocker material restante é humano: duas anotações primárias genuinamente independentes sobre o frozen 36-item DEVELOPMENT blind bank. Esse evidence é prerequisite para T005 e, por consequência, T006/T007/T008.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model preference somente após comparação T007 sobre quality evidence humana válida; A08 sozinho prova mechanics, não preferência;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- `VIDEO_PACKAGE_REVIEW: PASS` + durable artifact + provider mechanics PASS não autorizam project/release/production PASS;
- o PDF BCB deve permanecer fail-closed enquanto faltar cell-role provenance; no demo-only bypass;
- production/release readiness somente após T005/T006/T007/T008 + final applicable reviews.

## Next action

1. manter #85 como blocker externo explícito até existirem `PRIMARY_A` e `PRIMARY_B` completos, independentes e com provenance suficiente;
2. quando os dois humanos concluírem exports válidos via T009, iniciar novo attempt de T005 sem reutilizar A01;
3. após T005 aceito, liberar T006 e T007 em paralelo quando seguro — T004 provider prerequisite já está satisfeita;
4. integrar T006/T007 e executar T008 clean-E2E final;
5. depois executar reviews finais aplicáveis e reavaliar Success + Partner + Quality stop conditions.

## Recovery point

Retomar de `STATE_VERSION 0033` e `SYSTEM/CHECKPOINTS/STATE-v0033.md`. T004 A08 está integrado com provider mechanics real observada; T005 é o único blocker externo material restante para o fan-in T006/T007/T008. Nenhum human evidence foi fabricado.
