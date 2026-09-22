---
name: Agent task
author: ''
about: Tarefa versionada para execução paralela por worker/chat
labels: ''
assignees: ''
---

TASK_ID: W###-T###
ATTEMPT_ID: A01
BASE_STATE_VERSION: ####
BASE_COMMIT_SHA: <40 hex do main no dispatch>
ROLE: <role from SYSTEM/AGENT_ROLES.md>
PRIORITY: CRITICAL | HIGH | MEDIUM | LOW
STATUS: READY | PLANNED | BLOCKED
WORKER_BRANCH: worker/W###-T###-A01
SUCCESS_TARGETS: <Success/Partner/Quality/Production dimensions or gates>
REQUIREMENT_REFS: REQ-... | none
PAIN_REFS: PAIN-... | none
PRODUCTION_REFS: PROD-... | none
ASSUMPTION_REFS: A-... | none
RISK_REFS: RISK-... | none
DRG_APPLICABILITY: REQUIRED | NOT_REQUIRED | ALREADY_SATISFIED_BY_INPUTS
DEPENDENCIES: none | W###-T###,...

## Objective

...

## Context / current evidence boundary

- ...

## Scope

**IN**
- ...

**OUT**
- ...

## Evidence required

- ...
- para decisão material: cumprir `SYSTEM/DECISION_RESEARCH_GATE.md`, incluindo baseline/counterfactual, alternativas, fontes adequadas e benchmark representativo quando testável;
- não promover consenso de agentes, preferência estética ou popularidade de framework a evidência.

## Definition of done

- [ ] `CONTINUITY_CHECK: PASS` contra base válida
- [ ] branch isolada `worker/<TASK_ID>-<ATTEMPT_ID>`
- [ ] `TASK_STARTED` emitido na Issue antes do trabalho substantivo
- [ ] objetivo/escopo/DoD específicos concluídos ou blocker explicitamente provado
- [ ] findings distinguem fato, inferência, hipótese e unknown
- [ ] decisões materiais terminam como `LOCK | NO_PREFERENCE | PENDING_EVIDENCE` quando DRG aplicável
- [ ] RESULT persistido em `SYSTEM/RESULTS/<TASK_ID>-<ATTEMPT_ID>.md`
- [ ] exatamente um terminal `TASK_COMPLETE | TASK_BLOCKED | TASK_STALE` emitido após persistência

## Result contract

Use o contrato `RESULT` de `SYSTEM/TEMPLATES.md`. Inclua obrigatoriamente:

- `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION`, `BASE_COMMIT_SHA`;
- `STATUS` e `CONFIDENCE`;
- findings/evidence e limitações;
- `SUCCESS_IMPACT`;
- `TRACEABILITY_UPDATES`;
- assumptions/risks afetados;
- state/decision proposals;
- artifact refs;
- next actions.

Workers não alteram arquivos canônicos. Sinais de lifecycle seguem `SYSTEM/TASK_SIGNALS.md`; somente o Orchestrator com lease ativo integra `STATE`, ledger, wave, scorecards, traceability e demais canônicos.
