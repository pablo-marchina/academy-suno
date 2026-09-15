# AGENTS.md — Academy Suno

Estas regras valem para qualquer agente/chat.

## Source of truth

GitHub, nesta ordem: `CONSTITUTION` → `STATE` → `SUCCESS_MODEL/SCORECARD` → Partner/Quality models/scorecards → `ROADMAP` → `DECISIONS` → `TASK_LEDGER/WAVES` → Issues/PRs/results → knowledge/evidence.

## Bootstrap

Antes de trabalhar, identifique `PROTOCOL_VERSION`, `STATE_VERSION`, main SHA, role/task/attempt e execute `CONTINUITY_CHECK`. Referência divergente = `STALE_INPUT`.

## Objective

Otimize o **sucesso total** definido em `SYSTEM/SUCCESS_MODEL.md`. Não optimize isoladamente velocidade, Partner Value, score da banca, tecnologia, estética ou volume de trabalho.

## Authority

Somente holder do lease ativo altera canônicos. Workers nunca integram estado.

## Task provenance

Toda tentativa declara `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION`, `BASE_COMMIT_SHA`, dependências, `SUCCESS_TARGETS`, requirement/pain refs, assumptions relevantes, objetivo e DoD.

## Worker lifecycle signals

Para tentativas despachadas em protocolo 1.6.0+, após `CONTINUITY_CHECK: PASS` e branch isolada, o worker comenta `TASK_STARTED` na Issue antes do trabalho substantivo. Pode emitir `TASK_PROGRESS` em marcos materiais e deve terminar com exatamente um `TASK_COMPLETE`, `TASK_BLOCKED` ou `TASK_STALE`, conforme `SYSTEM/TASK_SIGNALS.md`.

Sinais são telemetria; worker não altera `STATE`, `TASK_LEDGER` ou wave manifest.

## Worker result

Persistir resultado no GitHub e declarar: identidade/base, status/confidence, findings/evidence, `SUCCESS_IMPACT`, `TRACEABILITY_UPDATES`, assumptions/risks afetados, state/decision proposals, artifacts e next actions. `TASK_COMPLETE` só é válido após RESULT persistido.

## Parallelism

Paralelize tarefas independentes somente quando isso não reduz qualidade nem cria escrita concorrente. Branch por tentativa quando editar arquivos.

## Evidence & uncertainty

Separe fato, inferência, hipótese e unknown. Consenso não substitui evidência. Premissa crítica deve permanecer explícita até validação/controle.

## Completion

Nenhum agente declara projeto completo sem Success + Partner + Quality PASS e Final Review PASS.
