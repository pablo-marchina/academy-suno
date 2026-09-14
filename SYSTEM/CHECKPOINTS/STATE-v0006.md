# CANONICAL PROJECT STATE

`PROTOCOL_VERSION: 1.4.0`

`STATE_VERSION: 0006`

`PROJECT_STATUS: ACTIVE`

`CURRENT_PHASE: 1 — Case + Partner Intake`

`LAST_COMMITTED_WAVE: SYSTEM-PARTNER-VALUE-V1.4`

## Objective

Entregar a solução que mais ajuda o parceiro na dor real e prioritária, dentro das restrições do case, e construir o melhor case possível para demonstrar e defender essa solução.

## Current truth

- GitHub é a fonte canônica.
- O sistema opera com lease, provenance por tentativa, checkpoints, DAG e dispatches.
- `PARTNER_MODEL_VERSION 1.0` define Partner Value como função objetivo primária.
- `QUALITY_MODEL_VERSION 1.1` trata excelência do case como constraint/secondary objective da solução partner-first.
- `PARTNER_SCORECARD` e `QUALITY_SCORECARD` aguardam briefing/contratos; ainda não é válido pontuar.
- Orchestrator gera prompts/dispatches automaticamente.
- Phase 1 está aberta; Issue #2 continua sendo a tarefa de ingestão/framing.

## Locked decisions

- `D-0001` — GitHub é fonte canônica.
- `D-0002` — Workers não integram estado.
- `D-0003` — Tarefas independentes são paralelizadas.
- `D-0004` — Guardrails executáveis.
- `D-0005` — Lease exclusivo.
- `D-0006` — Proveniência/idempotência por tentativa.
- `D-0007` — Checkpoints e DAG.
- `D-0009` — Loop obrigatório até hard gates/stop.
- `D-0010` — Partner Value é função objetivo primária.
- `D-0011` — Partner Contract/Jury/Adoption Gate obrigatórios.

## Open blockers

- `B-0001` — Falta briefing/material para construir Case Contract e Partner Contract.
- `B-0002` — Proteção administrativa do `main` ainda deve ser ativada.
- `B-0003` — Repositório público: confirmar confidencialidade antes de versionar materiais.

## Active tasks

- `BOOT-T002` — `READY` — Issue #2 — ingerir briefing, construir Case Contract + Partner Contract, calibrar scorecards e preparar W001.

## Pending decisions

- prazo/formato conforme briefing;
- visibilidade público/privado;
- stack técnica se aplicável;
- critérios/pesos finais conforme case;
- Partner success metrics e pain priority após evidência.

## Next action

1. Resolver blockers administrativos aplicáveis.
2. Revalidar lease.
3. Executar `BOOT-T002` sobre `STATE 0006`.
4. Construir Case Contract + Partner Contract sem inventar fatos.
5. Calibrar Partner/Quality Scorecards.
6. Criar W001 priorizando unknowns e gaps com maior impacto esperado no parceiro.
7. Gerar dispatches e iniciar partner-first autopilot loop.

## Recovery point

Retomar de `STATE_VERSION 0006` e `SYSTEM/CHECKPOINTS/STATE-v0006.md`. Nenhuma conclusão fora do main é canônica.
