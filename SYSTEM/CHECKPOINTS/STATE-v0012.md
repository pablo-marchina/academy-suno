# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.6.0`

`STATE_VERSION: 0012`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 2 — Discovery & Evidence`

`LAST_COMMITTED_WAVE: W001-COMPLETE`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- W001 está COMPLETE; T001…T010 foram integradas com proveniência válida;
- lifecycle signal-aware funcionou em T009/T010 com STARTED/PROGRESS/COMPLETE observáveis no GitHub;
- arquitetura candidata: source-first, pequena, stateful, auditável e não-agentic por default;
- fluxo candidato: Parser/SourceTrust → FactualBackbone/PolicyContext → 3×3 structured generation → per-variant HybridEvaluator → targeted repair → persisted evidence cockpit;
- stack candidata provisória: Python tipado + LangGraph StateGraph + Pydantic + SQLite/JSONL + Streamlit;
- baseline/fallback obrigatório: plain async Python com os mesmos contratos;
- parser, provider/model, semantic backend, audience classifier e thresholds permanecem `PENDING_EXPERIMENT`;
- hard gates de source trust, factuality material, conceitos/labels obrigatórios e policy são não compensáveis;
- repair é branch-local por `job_id`; uma falha não regenera a matriz inteira;
- evidence cockpit é a narrativa principal da demo: source → 3×3 → FAIL → diagnostics → repair → PASS → trace;
- W001 definiu backlog B01…B14 e mandatory experiments EXP-A…EXP-I;
- os próximos riscos dominantes são correctness da fundação e prova experimental, não desenho conceitual adicional;
- deadline, método de submissão, owner/decision maker e workflow interno Suno permanecem UNKNOWN e não podem ser inventados;
- repositório público e ausência de proteção de `main` são escolhas aceitas pelo usuário.

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

Nenhum blocker impede foundation build/experiments. External unknowns impedem apenas claims de production readiness/ROI/internal-policy alignment.

## Completed wave

`W001` — Discovery / Eval Foundations.

Integrated outcome:
- audience/content calibration;
- PT-BR complexity model;
- finance ontology metrics;
- factuality/source-grounding architecture;
- gold/held-out benchmark design;
- architecture/state/retry tradeoffs;
- format-native UX/demo design;
- compliance/content policy;
- Hybrid Evaluator synthesis;
- candidate architecture + build plan.

## Current success bottleneck

`FOUNDATION_CORRECTNESS_AND_EXPERIMENTAL_PROOF`

A solução está bem especificada, mas ainda precisa provar em código que source parsing/trust, deterministic factual/policy gates, 3×3 contracts e orchestration baseline funcionam sem silent corruption ou overengineering.

## Candidate build order

P0:
1. B01 domain schemas + version/provenance spine;
2. B02 real-source fixtures + ParserAdapter/source trust;
3. B03 factual backbone/deterministic anchors;
4. B04 executable policy engine;
5. B05 structured 3×3 generators/format schemas.

Mandatory early experiments:
- EXP-A parser/source-trust bakeoff;
- EXP-B LangGraph vs plain-async baseline;
- EXP-C hard-gate adversarial suite.

## Pending decisions

- lock LangGraph vs simple fallback after EXP-B;
- parser/fallback after EXP-A;
- provider/model after quality/cost/latency comparison;
- semantic backend after ablation;
- audience classifier/thresholds after development-gold calibration;
- repair cap after convergence/economics experiment;
- final UI lock after demo rehearsal;
- internal Suno policy/workflow only if externally validated.

## Next action

1. merge W001-T010 integration / STATE 0012;
2. close Issue #19 and realign Orchestrator lease;
3. create W002 against exact post-merge main SHA;
4. use W002 to build/test P0 foundation with maximum safe parallelism and explicit ownership paths;
5. integrate results by micro-fan-in and run EXP-A/B/C before locking architecture choices.

## Recovery point

Retomar de `STATE_VERSION 0012` e `SYSTEM/CHECKPOINTS/STATE-v0012.md`. W001 está COMPLETE. A próxima operação canônica é materializar W002 sobre o SHA exato da main pós-integração.