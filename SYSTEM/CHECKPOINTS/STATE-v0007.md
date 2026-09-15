# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.5.0`

`STATE_VERSION: 0007`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case + Partner Intake`

`LAST_COMMITTED_WAVE: SYSTEM-SUCCESS-ARCHITECTURE-V1.5`

## Objective

Entregar a melhor solução e o melhor case possíveis como combinação balanceada de valor para o parceiro, aderência ao briefing/avaliação, rigor/evidência, qualidade/diferenciação da solução, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução.

## Current truth

- `SUCCESS_MODEL_VERSION 1.0` é a função objetivo dominante.
- Partner Outcome e Quality são componentes/hard gates, não objetivos isolados suficientes.
- Traceability Matrix, Assumption/Risk Register e Final Review Protocol são obrigatórios.
- Success/Partner/Quality scorecards aguardam briefing/contratos; não é válido pontuar ainda.
- Autopilot deve fechar hard gates, depois elevar o bottleneck de sucesso total.
- Orchestrator gera prompts/dispatches automaticamente.
- Phase 1 aberta; Issue #2 é o intake/framing canônico.

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

- `B-0001` — falta briefing/material para contratos e scorecards.
- `B-0002` — proteção administrativa do main ainda deve ser ativada.
- `B-0003` — repo público: confirmar confidencialidade antes de material sensível.

## Active tasks

- `BOOT-T002` — `READY` — Issue #2 — ingerir briefing, construir contracts, traceability/assumptions, calibrar scorecards e preparar W001.

## Pending decisions

- deadline/formato/submission conforme briefing;
- visibilidade público/privado;
- critérios/pesos/floors conforme case;
- success metrics do parceiro;
- finalization reserve após conhecer prazo.

## Next action

1. resolver blockers administrativos aplicáveis;
2. revalidar lease;
3. executar BOOT-T002 sobre STATE 0007;
4. construir Case + Partner Contracts;
5. inicializar Traceability + Assumption/Risk Register;
6. calibrar Success/Partner/Quality scorecards;
7. criar W001 a partir dos hard gates/unknowns/bottlenecks de maior impacto;
8. gerar dispatches e iniciar Autopilot.

## Recovery point

Retomar de `STATE_VERSION 0007` e `SYSTEM/CHECKPOINTS/STATE-v0007.md`.
