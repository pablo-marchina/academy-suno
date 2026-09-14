# OPERATIONAL TEMPLATES

## 1. Task / GitHub Issue

```text
TASK_ID: W###-T###
ATTEMPT_ID: A01
BASE_STATE_VERSION: ####
BASE_COMMIT_SHA: <40 hex do main no dispatch>
ROLE: Researcher | Analyst | Synthesizer | Critic | Auditor | Builder
PRIORITY: CRITICAL | HIGH | MEDIUM | LOW
WORK_BRANCH: task/W###-T###-A01-<slug> | none

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

OUTPUT_FORMAT
Use o template RESULT abaixo e persista o resultado no GitHub.
```

## 2. Worker Result

```text
RESULT
TASK_ID: W###-T###
ATTEMPT_ID: A##
BASE_STATE_VERSION: ####
BASE_COMMIT_SHA: <40 hex>
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
- ...

DECISIONS_PROPOSED
- ...

OPEN_RISKS
- ...

CONFLICTS_WITH_CURRENT_STATE
- none | ...

ARTIFACT_REFS
- Issue/PR/path: ...

NEXT_ACTIONS
- ...
```

## 3. Wave Manifest

Arquivo: `SYSTEM/WAVES/W###.json`. Use `SYSTEM/WAVES/_TEMPLATE.json` como base.

Campos obrigatórios por task: `task_id`, `attempt_id`, `role`, `status`, `required`, `dependencies`, `issue`, `branch`.

## 4. Integration / Commit

```text
INTEGRATION
ORCHESTRATOR_SESSION_ID: ORCH-G###-S###
LEASE_REVALIDATED: YES
WAVE: W### | SYSTEM
FROM_STATE: ####
FROM_MAIN_SHA: <40 hex>
TO_STATE: ####

RESULTS_RECEIVED
- W###-T001/A01: COMPLETE / integrated

STALE_CHECK
- ...

DECISIONS
- D-#### ...

EVIDENCE_ACCEPTED
- E-#### ...

ROADMAP_GATE_CHANGE
- ...

CHECKPOINT
- SYSTEM/CHECKPOINTS/STATE-v####.md

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
MAIN_COMMIT_SHA: ...
ORCHESTRATOR_LEASE: ... | N/A
CURRENT_PHASE: ...
LAST_COMMITTED_WAVE: ...

WHAT_THIS_CHAT_DID
- ...

UNCOMMITTED_WORK
- none | ...

OPEN_THREADS
- ...

NEXT_CHAT_STARTS_BY
1. Read canonical files.
2. Resolve main SHA.
3. Execute CONTINUITY_CHECK independently.
4. If Orchestrator, claim/transfer lease atomically.
5. Trust canonical files if handoff conflicts.
```

## 6. Continuity Check

```text
CONTINUITY_CHECK
protocol_version: ...
state_version: ...
main_commit_sha: ...
current_phase: ...
last_committed_wave: ...
role: ...
task_id: ...
attempt_id: ...
orchestrator_lease: ...
locked_decisions_seen: ...
open_blockers_seen: ...
status: PASS | FAIL
```

## 7. Audit

```text
AUDIT
STATE_VERSION: ####
MAIN_COMMIT_SHA: ...
STATUS: PASS | FAIL

CHECKS
- Lease consistency: PASS/FAIL
- Checkpoint consistency: PASS/FAIL
- Wave/DAG consistency: PASS/FAIL
- Provenance/attempt consistency: PASS/FAIL
- Constitution compliance: PASS/FAIL
- State/Roadmap/Decision/Ledger consistency: PASS/FAIL
- Stale/orphan results: PASS/FAIL
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

## 9. Lease claim

```text
LEASE_CLAIM
observed_lease_blob_sha: ...
requested_session_id: ORCH-G###-S###
state_version: ####
main_commit_sha: ...
result: ACQUIRED | CONFLICT | DENIED
```
