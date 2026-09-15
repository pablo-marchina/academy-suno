# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0010`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case + Partner Intake`

`LAST_COMMITTED_WAVE: W001-FANOUT-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- briefing primário, Case Contract, Partner Contract, Traceability Matrix e Assumption/Risk Register estão materializados;
- W001 está ACTIVE; W001-T001…T008 estão integradas;
- os RESULTs aceitos convergem para uma arquitetura source-first com verdade factual comum antes do fan-out 3×3;
- audiência, formato e source/content type são dimensões separadas;
- Flesch PT-BR é sensor, sofisticação é multidimensional, terminologia opera sobre conceitos normalizados e factuality é claim-centric/source-first;
- benchmark separa generation target, human gold e evaluator prediction com held-out por documento;
- arquitetura candidata de trabalho é grafo explícito pequeno + backbone factual + fan-out 3×3 + avaliação por variante + targeted repair;
- UX candidata é evidence cockpit com evaluators por formato, source lineage e FAIL→diagnostics→repair→PASS;
- content policy bloqueia recomendação nova/personalizada, drift material, perda de atribuição e modality escalation;
- `SYSTEM/TASK_SIGNALS.md` passa a governar lifecycle de attempts futuros: worker registra `TASK_STARTED`, progress material opcional e terminal obrigatório na Issue;
- Orchestrator reconstrói `READY/RUNNING/RESULT_RECEIVED/BLOCKED/STALE` dos sinais + artefatos; usuário não precisa transportar status entre chats;
- não existe heartbeat periódico/TTL como prova de liveness; liveness incerta pode gerar novo attempt sem reutilização de ID;
- `W001-T009` é a primeira task a operar sob protocolo 1.6.0 / lifecycle signals;
- thresholds finais, stack final e arquitetura final ainda não estão locked; dependem de T009/T010 e experimentos;
- deadline, método de submissão, owner/decision maker e workflow interno Suno permanecem UNKNOWN;
- repositório público e ausência de proteção de `main` são escolhas aceitas pelo usuário; risco permanece documentado.

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

## Open blockers

Nenhum blocker impede W001-T009. Unknowns internos e deadline/submission continuam registrados e não devem ser inventados.

## Active wave

`W001` — Discovery / Eval Foundations.

## Integrated tasks

- `W001-T001` — Suno content/partner calibration.
- `W001-T002` — legibilidade PT-BR / audience complexity.
- `W001-T003` — financial ontology / terminology metrics.
- `W001-T004` — factuality / grounding / anchors.
- `W001-T005` — golden dataset / confusion-matrix design.
- `W001-T006` — architecture / state / retry / stack tradeoffs.
- `W001-T007` — UX/demo / format-specific evaluators.
- `W001-T008` — compliance / content-policy guardrails.

## Ready task

`W001-T009` — Hybrid Evaluator synthesis. Base exata será fixada na Issue #18 após merge deste protocolo; lifecycle signals obrigatórios.

## Planned task

`W001-T010` — candidate architecture + build plan. Continua bloqueada até T009 ser integrada.

## Current success bottleneck

`HYBRID_EVALUATOR_SYNTHESIS_AND_CALIBRATION_PLAN`

Os componentes existem separadamente; o próximo risco é integrá-los sem score compensatório, thresholds arbitrários ou circularidade.

## Pending decisions

- arquitetura/stack final após T009/T010;
- thresholds/floors do evaluator após calibração experimental;
- composição final/disponibilidade prática do golden/held-out dataset;
- política final de content guardrails;
- parser/fallback após testes reais com Copom, fato relevante e release;
- deadline/submission quando informação existir;
- tratamento do workflow interno Suno se continuar indisponível.

## Next action

1. mergear protocolo 1.6.0 / lifecycle signals;
2. alinhar lease e Issue #18 ao SHA exato da nova `main`;
3. despachar W001-T009, que deve emitir `TASK_STARTED` autonomamente;
4. em próximo Autopilot, reconstruir status pela Issue/result e integrar T009 quando completo;
5. liberar T010 via micro-fan-in.

## Recovery point

Retomar de `STATE_VERSION 0010` e `SYSTEM/CHECKPOINTS/STATE-v0010.md`. Os RESULTs W001-T001…T008 são evidência integrada; W001-T009 é READY e passa a ser observável por task signals.
