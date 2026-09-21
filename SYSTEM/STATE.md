# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0032`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 7 — Blind Review, Final Deliverable & Defense`

`LAST_COMMITTED_WAVE: W004-GROQ-ACCESS-BLOCKER-CHARACTERIZED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001, W002 e W003 estão COMPLETE; W004 permanece ACTIVE;
- W004-T001/T002/T003/T009/T010/T011/T012/T013/T014/T015/T017/T018/T019/T020/T021 estão INTEGRATED;
- W004-T004 continua BLOCKED, agora com blocker externo caracterizado: a credencial fornecida foi identificada defensavelmente como Groq (`gsk_`), mas ainda não existe run de provider aceito com usage/cost/model response observados;
- T004 A02/A03 falharam closed antes de qualquer request por classificação ambígua do secret; nenhum segredo foi exposto;
- T004 A04 identificou Groq e realizou o primeiro request real autorizado ao endpoint oficial Responses para `openai/gpt-oss-20b`; Actions run `35661547702` retornou HTTP `403 Forbidden` após `74.928 ms`, sem usage/model response;
- T004 A05 executou preflight read-only autenticado `GET https://api.groq.com/openai/v1/models`; Actions run `35661903374` retornou HTTP `403` após `83.516 ms`. Como o próprio preflight foi recusado, A05 não realizou geração. Isso desloca o blocker de “credencial ausente” para acesso/permissão Groq de organização/projeto/key;
- os artifacts/resultados A04/A05 são auditáveis em branches de worker, mas nenhuma tentativa foi aceita/integrada como evidência observada de provider; o próximo retry deve usar novo ATTEMPT_ID após correção externa das permissões Groq;
- W004-T005 A01 permanece BLOCKED por falta de duas streams primárias humanas genuinamente independentes; nenhum pseudo-human/model gold é permitido;
- T019 produziu a demo final real da app recipient-facing: Actions run `35636285651`, MP4 SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`, duração observada `69.12s <= 300s`, H.264 1280×720 a 25 fps, success path `SOURCE_READY/PASS` primeiro, 9/9 mechanics, persisted `FAIL → repair → PASS`, evidence boundaries e BCB fail-closed safety negative-control sem bypass;
- T020 baixou e verificou diretamente os artifacts aceitos, mediu novamente o MP4 em `69.120000s`, inspecionou frames independentes e concluiu `VIDEO_PACKAGE_REVIEW: PASS` com `NEW_CRITICAL_FINDINGS: 0` e `NEW_HIGH_FINDINGS: 0`;
- T021 A01 foi classificada `LIVENESS_UNCERTAIN` sem commit/result após start válido; o retry A02 foi executado sobre a mesma base canônica e é a tentativa aceita;
- T021 A02 baixou novamente o artifact aceito `10656720873`, verificou o source MP4 com SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5` e `1388430` bytes, persistiu os mesmos bytes em `artifacts/submission/final-demo.mp4`, fez fresh-clone/read-back remoto e confirmou SHA/size + `cmp` byte-a-byte PASS no Actions run `35651949452`;
- o binary durável está no histórico do repositório desde persistence commit `8216b56edef7a666e08aab7c6dc37ea1a6ec3781`; portanto a expiração dos Actions artifacts em `2026-12-20T18:06:45Z` deixou de ser dependência de disponibilidade do MP4 aceito;
- F-001/F-002/F-003/F-007/F-008 passam no escopo de video/package review para o artifact exato T019/T021; isso não equivale a project/release/production readiness;
- root README e `docs/submission/SUBMISSION_PACKET.md` estão atuais e apontam para a preservação durável do artifact final;
- o BCB real permanece corretamente `SOURCE_BLOCKED / REVIEW_REQUIRED / LOW` quando table-role provenance é ambígua; isso é safety behavior, não falha a ser ocultada;
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
- `W004-T020` — independent final blind/adversarial review — Issue #122 / PR #126 — `VIDEO_PACKAGE_REVIEW: PASS`.
- `W004-T021` — durable byte-identical accepted-video preservation — Issue #127 / accepted attempt A02 / PR #130 / Actions run `35651949452`.

### BLOCKED external/fallback evidence
- `W004-T004-A05` — Groq credential identified, but read-only `/openai/v1/models` preflight returns HTTP 403; external Groq access/permission correction required — Issue #84 / Actions run `35661903374`.
- `W004-T005-A01` — two independent human primary annotations unavailable — Issue #85.
- `W004-T016-A01` — worker-local screen recording unavailable; deterministic manual fallback retained — Issue #109 / PR #114.

### PLANNED
- `W004-T006` — semantic backend ablation — requires valid T005 human gold.
- `W004-T007` — provider/model comparison — requires accepted T004 provider mechanics + valid human evidence.
- `W004-T008` — final clean-E2E release proof — requires T001,T003,T005,T006,T007.

## Current success bottleneck

`EXTERNAL_HUMAN_GROQ_PERMISSION_EVIDENCE`

Todos os gaps internos materiais conhecidos do vídeo/pacote e de retenção do MP4 aceito foram fechados em escopo: T020 aprovou independentemente o pacote/vídeo T019 e T021 preservou os bytes aceitos em storage controlado pelo repositório com read-back byte-identical. O provider path também foi reduzido a um blocker externo específico: a credencial é Groq, chega à API, porém o endpoint read-only `/models` retorna 403 antes de qualquer geração aceita. Os blockers materiais restantes são, portanto, duas anotações humanas independentes e correção de acesso/permissões Groq seguida de novo attempt T004.

## Pending decisions

- audience thresholds somente após human gold + agreement/adjudication suficiente; caso contrário `DIAGNOSTIC_ONLY`;
- semantic backend somente após ablation no mesmo development gold válido;
- provider/model somente após runs observáveis comparáveis + quality evidence válida;
- parser implementation continua `UNLOCKED` até same-raw-byte cross-parser/OCR evidence;
- `VIDEO_PACKAGE_REVIEW: PASS` + durable artifact não autorizam project/release/production PASS;
- o PDF BCB deve permanecer fail-closed enquanto faltar cell-role provenance; no demo-only bypass;
- production/release readiness somente após human/provider prerequisites + W004-T008 + final applicable reviews.

## Next action

1. manter #84/#85 como blockers externos explícitos;
2. no Groq Console, corrigir/confirmar acesso da credencial ao projeto e permissões de organização/projeto para API/modelos; depois iniciar T004 em novo attempt (A06 ou próximo ID livre), sem reutilizar A05;
3. quando dois humanos concluírem exports válidos via T009, iniciar novo attempt de T005;
4. liberar T006/T007/T008 somente quando seus prerequisites reais forem satisfeitos;
5. após esses fan-ins, executar os reviews finais aplicáveis e reavaliar Success + Partner + Quality stop conditions.

## Recovery point

Retomar de `STATE_VERSION 0032` e `SYSTEM/CHECKPOINTS/STATE-v0032.md`. T021 permanece integrado e o MP4 final aceito está preservado byte-identical. T004 está external-blocked por Groq HTTP 403 já reproduzido no próprio `/models`; T005 permanece external-blocked por duas streams humanas independentes. Nenhum provider/human evidence foi fabricado.
