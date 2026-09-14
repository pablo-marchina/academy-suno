# OPERATIONAL TEMPLATES

## 1. Task / GitHub Issue

```text
TASK_ID: W###-T###
BASE_STATE_VERSION: ####
ROLE: Researcher | Analyst | Synthesizer | Critic | Auditor | Builder
PRIORITY: CRITICAL | HIGH | MEDIUM | LOW

OBJECTIVE
<resultado específico esperado>

CONTEXT
<contexto mínimo necessário; não copie histórico inteiro>

DEPENDENCIES
- <TASK_ID ou none>

INPUTS
- <arquivos, URLs, issues, evidências>

SCOPE
- IN: ...
- OUT: ...

DEFINITION_OF_DONE
- [ ] ...
- [ ] ...

OUTPUT_FORMAT
Use o template RESULT abaixo.
```

## 2. Worker Result

```text
RESULT
TASK_ID: W###-T###
BASE_STATE_VERSION: ####
STATUS: COMPLETE | PARTIAL | BLOCKED | STALE
CONFIDENCE: 0-100

EXECUTIVE_SUMMARY
...

FINDINGS
1. ...

EVIDENCE
- E-candidate: <claim> — <source/data>

ASSUMPTIONS
- ...

STATE_DELTA_PROPOSED
- add/change/remove: ...

DECISIONS_PROPOSED
- ...

OPEN_RISKS
- ...

CONFLICTS_WITH_CURRENT_STATE
- none | ...

NEXT_ACTIONS
- ...
```

## 3. Wave Plan

```text
WAVE: W###
BASE_STATE_VERSION: ####
OBJECTIVE: ...

CRITICAL_PATH
...

PARALLEL_TASKS
- W###-T001 — role — objective — deps
- W###-T002 — role — objective — deps
- W###-T003 — role — objective — deps

FAN_IN_REQUIREMENTS
- required tasks: ...
- optional tasks: ...

EXIT_CONDITION
...
```

## 4. Integration / Commit

```text
INTEGRATION
WAVE: W###
FROM_STATE: ####
TO_STATE: ####

RESULTS_RECEIVED
- W###-T001: COMPLETE / integrated
- ...

STALE_CHECK
- ...

DECISIONS
- D-#### ...

EVIDENCE_ACCEPTED
- E-#### ...

RISKS_OPENED/CLOSED
- ...

ROADMAP_GATE_CHANGE
- ...

NEXT_CRITICAL_PATH
- ...
```

## 5. Chat Handoff

```text
HANDOFF
ROLE: ...
OUTGOING_CHAT: ...
PROTOCOL_VERSION: ...
STATE_VERSION: ...
CURRENT_PHASE: ...
LAST_COMMITTED_WAVE: ...

WHAT_THIS_CHAT_DID
- ...

UNCOMMITTED_WORK
- none | ...

OPEN_THREADS
- ...

IMPORTANT_WARNINGS
- ...

NEXT_CHAT_STARTS_BY
1. Read AGENTS.md + canonical SYSTEM files.
2. Execute CONTINUITY_CHECK independently.
3. Compare with this handoff.
4. Trust canonical files if there is any conflict.
```

## 6. Continuity Check

```text
CONTINUITY_CHECK
protocol_version: ...
state_version: ...
current_phase: ...
last_committed_wave: ...
role: ...
task_id: ...
locked_decisions_seen: ...
open_blockers_seen: ...
status: PASS | FAIL
```

## 7. Audit

```text
AUDIT
STATE_VERSION: ####
STATUS: PASS | FAIL

CHECKS
- Constitution compliance: PASS/FAIL
- State consistency: PASS/FAIL
- Roadmap consistency: PASS/FAIL
- Decision consistency: PASS/FAIL
- Task ledger consistency: PASS/FAIL
- Open Issues consistency: PASS/FAIL
- Stale results: PASS/FAIL
- Orphan results/tasks: PASS/FAIL
- Skipped gates: PASS/FAIL

FINDINGS
1. severity — finding — corrective action

SAFE_TO_CONTINUE: YES | NO
```

## 8. Decision Review

```text
DECISION_REVIEW
DECISION_ID: D-####
CURRENT_STATUS: LOCKED
TRIGGER: ...
NEW_EVIDENCE: ...
IMPACT_IF_KEPT: ...
IMPACT_IF_CHANGED: ...
RECOMMENDATION: KEEP | REOPEN
```
