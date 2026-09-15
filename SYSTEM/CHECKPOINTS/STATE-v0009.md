# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.5.0`

`STATE_VERSION: 0009`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case + Partner Intake`

`LAST_COMMITTED_WAVE: W001-FANOUT-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- briefing primário, Case Contract, Partner Contract, Traceability Matrix e Assumption/Risk Register estão materializados;
- W001 está ACTIVE;
- W001-T001…T008 foram executadas em branches isoladas, classificadas `SAFE_TO_INTEGRATE` e persistidas em `SYSTEM/RESULTS/`;
- os RESULTs aceitos convergem para uma arquitetura source-first com uma verdade factual comum antes do fan-out 3×3;
- audiência, formato e source/content type devem ser dimensões separadas;
- Flesch PT-BR é sensor de legibilidade superficial, não classificador único de nível;
- sofisticação deve ser multidimensional e calibrada contra golden set independente;
- terminologia deve operar sobre conceitos financeiros normalizados, aliases, contextualização e anti-gaming;
- factuality deve ser claim-centric/source-first, com anchors determinísticos e veto para erros materiais;
- benchmark experimental deve separar target de geração, human gold e predicted level, com split por documento e held-out protegido;
- arquitetura candidata de trabalho é grafo explícito pequeno, backbone factual, fan-out 3×3, avaliação por variante e targeted repair;
- UX candidata é evidence cockpit com format-specific evaluators, source lineage e demonstração FAIL→diagnostics→repair→PASS;
- content policy deve bloquear recomendação nova/personalizada, drift material, perda de atribuição e elevação indevida de certeza;
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

## Open blockers

Nenhum blocker impede o fan-in W001-T009. Unknowns internos e deadline/submission continuam registrados e não devem ser inventados.

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

`W001-T009` — Hybrid Evaluator synthesis. Dependências T002–T005 satisfeitas e aceitas.

## Planned task

`W001-T010` — candidate architecture + build plan. Continua bloqueada até T009 ser integrada.

## Current success bottleneck

`HYBRID_EVALUATOR_SYNTHESIS_AND_CALIBRATION_PLAN`

Os componentes necessários existem separadamente; o próximo risco é integrá-los sem criar score compensatório, thresholds arbitrários ou circularidade.

## Pending decisions

- arquitetura/stack final após T009/T010;
- thresholds/floors do evaluator após calibração experimental;
- composição final e disponibilidade prática do golden/held-out dataset;
- política final de content guardrails;
- parser/fallback após testes reais com Copom, fato relevante e release;
- deadline/submission quando informação existir;
- tratamento do workflow interno Suno se continuar indisponível.

## Next action

1. despachar W001-T009 em `STATE 0009` contra SHA exato da `main` pós-integração;
2. integrar T009 se seguro;
3. liberar T010 via micro-fan-in;
4. sintetizar arquitetura candidata/plano de build;
5. reavaliar Success/Partner/Quality, assumptions e traceability antes de build amplo.

## Recovery point

Retomar de `STATE_VERSION 0009` e `SYSTEM/CHECKPOINTS/STATE-v0009.md`. Os RESULTs W001-T001…T008 são evidência integrada e W001-T009 é a única task READY do critical path.
