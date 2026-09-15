# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.5.0`

`STATE_VERSION: 0008`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case + Partner Intake`

`LAST_COMMITTED_WAVE: BOOT-T002-INTAKE`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- briefing primário foi ingerido e transcrito em `docs/case/CASE_BRIEF_TRANSCRIPTION.md`;
- `SYSTEM/CASE_CONTRACT.md` e `SYSTEM/PARTNER_CONTRACT.md` existem e preservam unknowns sem preenchimento inventado;
- pesquisa pública de parceiro/competidores/IA está em `docs/research/partner-competitor-ai-benchmark-2026-09-14.md`;
- Traceability Matrix contém requisitos/pains do case;
- Assumption/Risk Register contém assumptions/riscos prioritários;
- Success/Partner/Quality scorecards estão calibrados, mas sem score numérico de solução inexistente;
- briefing exige 3 níveis × 3 formatos, Hybrid Evaluator, grounding, refinement loop, interface, experimentos e documentação;
- vídeo final é hard gate: deve provar código/interface reais; regra operacional <=5:00 por A-0001;
- pesos/escala formal de avaliação não foram fornecidos;
- deadline, método de submissão, owner/decision maker e workflow interno Suno permanecem UNKNOWN;
- repositório público é aceito pelo usuário; ausência de proteção de `main` não é blocker e está registrada como RISK-0012;
- `SUCCESS_MODEL_VERSION 1.0` continua sendo a função objetivo dominante.

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

Nenhum blocker impede W001. Unknowns internos e deadline/submission estão registrados e devem ser tratados sem inventar fatos.

## Active wave

`W001` — Discovery / Eval Foundations — preparada para fan-out inicial de oito workers e dois fan-ins.

## Ready tasks

- `W001-T001` — Suno content/voice + partner-use-case calibration.
- `W001-T002` — legibilidade PT-BR + audience calibration metrics.
- `W001-T003` — financial ontology + domain-term/context metrics.
- `W001-T004` — factuality/grounding + anchor/claim design.
- `W001-T005` — golden dataset + labels + confusion-matrix experiment design.
- `W001-T006` — architecture/state/retry + stack trade-off experiment.
- `W001-T007` — UX/demo + format-specific evaluator requirements.
- `W001-T008` — compliance/content-policy guardrails.

## Planned fan-ins

- `W001-T009` — Hybrid Evaluator synthesis, depende T002/T003/T004/T005.
- `W001-T010` — W001 technical synthesis/candidate architecture, depende T001/T006/T007/T008/T009.

## Current success bottleneck

`EVALUATION_CALIBRATION_AND_GROUND_TRUTH`

O diferencial do case só fica defensável quando audience calibration, factuality e experiment design forem reproduzíveis e não circulares.

## Pending decisions

- arquitetura/stack final após W001;
- thresholds/floors do evaluator após calibração experimental;
- composição do golden/held-out dataset;
- política final de content guardrails;
- deadline/submission quando informação existir;
- tratamento do workflow interno Suno se continuar indisponível.

## Next action

1. materializar `W001.json`, Issues e dispatches sobre `STATE 0008`;
2. despachar W001-T001…T008 em paralelo;
3. integrar resultados seguros e liberar micro-fan-in T009;
4. liberar T010 após dependências;
5. reavaliar Success/Partner/Quality e decidir avanço de fase/build.

## Recovery point

Retomar de `STATE_VERSION 0008` e `SYSTEM/CHECKPOINTS/STATE-v0008.md`. Os contratos, traceability, assumptions e scorecards são a base factual para W001.
