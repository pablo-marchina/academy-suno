# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0011`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case + Partner Intake`

`LAST_COMMITTED_WAVE: W001-T009-INTEGRATED`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- briefing primário, Case Contract, Partner Contract, Traceability Matrix e Assumption/Risk Register estão materializados;
- W001 está ACTIVE; W001-T001…T009 estão integradas;
- lifecycle signal-aware foi validado em execução real: T009 emitiu `TASK_STARTED` e `TASK_COMPLETE` válidos na Issue #18, com RESULT persistido e proveniência consistente;
- o Hybrid Evaluator sintetizado em T009 é hierárquico, evidence-first e não compensatório;
- pipeline lógico do evaluator: source trust → deterministic factual anchors → atomic claim grounding → concept/terminology layer → Audience Complexity Vector → calibrated audience decision → hybrid decision → targeted repair → re-evaluation;
- `CRITICAL` factual contradiction é hard fail; `ERROR` material não resolvido bloqueia auto-PASS; conceitos materiais obrigatórios e labels técnicos explicitamente requeridos não podem ser compensados por estilo/legibilidade;
- Flesch PT-BR, lexical/syntactic/cohesion signals, concept density/contextualization e audience classifier são sinais calibráveis; diagnostics não aprovam output isoladamente;
- `required_concepts`, `authorized_concepts` e `required_technical_labels` devem ser definidos a partir da fonte/rubrica/policy antes de avaliar o output;
- golden/held-out calibration continua separando generation target, human gold e evaluator prediction, com split por documento e thresholds congelados antes do held-out;
- a arquitetura candidata ainda não está locked; T010 deve reconciliar evaluator, partner/content fit, compliance, UX/demo, stack e backlog de build;
- thresholds finais, stack final, parser/fallback final e arquitetura final continuam dependentes de experimentos e síntese T010;
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

Nenhum blocker impede W001-T010. Unknowns internos e deadline/submission continuam registrados e não devem ser inventados.

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
- `W001-T009` — Hybrid Evaluator synthesis.

## Ready task

`W001-T010` — candidate architecture + build plan. Todas as dependências estão integradas. Base exata será fixada na Issue #19 após merge deste estado; lifecycle signals obrigatórios.

## Current success bottleneck

`TECHNICAL_SYNTHESIS_AND_BUILD_PLAN`

O evaluator está especificado; o próximo risco é converter os componentes validados em uma arquitetura mínima coerente e um backlog que maximize hard-gate coverage sem overengineering.

## Pending decisions

- arquitetura/stack final após T010 e experimentos obrigatórios;
- thresholds/floors do evaluator após implementação/calibração no development gold;
- composição final e disponibilidade prática do golden/held-out dataset;
- política final de content guardrails e human review;
- parser/fallback após testes reais com Copom, fato relevante e release;
- deadline/submission quando informação existir;
- tratamento do workflow interno Suno se continuar indisponível.

## Next action

1. mergear integração de T009 e `STATE 0011`;
2. alinhar lease e Issue #19 ao SHA exato da nova `main`;
3. despachar W001-T010, que deve emitir lifecycle signals autonomamente;
4. integrar T010 se seguro;
5. reavaliar Success/Partner/Quality, assumptions, traceability e roadmap; então encerrar W001 e abrir build wave priorizada.

## Recovery point

Retomar de `STATE_VERSION 0011` e `SYSTEM/CHECKPOINTS/STATE-v0011.md`. W001-T001…T009 são evidência integrada; W001-T010 é a única task READY do critical path.