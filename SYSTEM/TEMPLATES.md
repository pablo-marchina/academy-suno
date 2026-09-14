# OPERATIONAL TEMPLATES

## 1. Task / GitHub Issue

```text
TASK_ID: W###-T###
ATTEMPT_ID: A01
BASE_STATE_VERSION: ####
BASE_COMMIT_SHA: <40 hex do main no dispatch>
ROLE: ...
PRIORITY: CRITICAL | HIGH | MEDIUM | LOW
WORK_BRANCH: task/W###-T###-A01-<slug> | none

OBJECTIVE
<resultado específico esperado>

PARTNER_VALUE_LINK
- pain/hard gate/gap afetado: ...
- mecanismo de valor esperado: ...
- por que esta tarefa merece prioridade agora: ...

CONTEXT
<contexto mínimo necessário>

DEPENDENCIES
- <TASK_ID ou none>

INPUTS
- <arquivos, URLs, issues, evidências>

SCOPE
- IN: ...
- OUT: ...

DEFINITION_OF_DONE
- [ ] resultado verificável produzido
- [ ] impacto no parceiro/evidência ou redução de incerteza explicitados

OUTPUT_FORMAT
Use RESULT abaixo e persista no GitHub.
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

PARTNER_IMPACT
- pain addressed: ...
- expected value/uplift: ...
- evidence/confidence: ...
- adoption/implementation implication: ...
- does this dominate a simpler alternative? YES/NO/UNKNOWN — why

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

Arquivo: `SYSTEM/WAVES/W###.json`. Campos por task: identidade, role, status, required, dependencies, issue e branch. Cada task liberada deve ter vínculo com Partner/Quality gap, hard gate ou dependência crítica.

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
- ...

PARTNER_VALUE_DELTA
- partner gaps/hard gates improved: ...
- evidence accepted: ...
- alternatives invalidated/dominated: ...

QUALITY_DELTA
- ...

STALE_CHECK
- ...

DECISIONS
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
1. Read canonical files including Partner/Quality models.
2. Resolve main SHA.
3. Execute CONTINUITY_CHECK.
4. If Orchestrator, validate/claim lease.
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
partner_status: ...
quality_status: ...
status: PASS | FAIL
```

## 7. Audit

```text
AUDIT
STATE_VERSION: ####
STATUS: PASS | FAIL

CHECKS
- Partner objective alignment: PASS/FAIL
- Partner hard gates: PASS/FAIL/NOT_EVALUABLE
- Adoption/actionability: PASS/FAIL/NOT_EVALUABLE
- Quality gates: PASS/FAIL/NOT_EVALUABLE
- Lease/checkpoint/DAG/provenance: PASS/FAIL
- State/Roadmap/Decision/Ledger consistency: PASS/FAIL
- Stale/orphan results: PASS/FAIL

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
PARTNER_VALUE_IMPACT: ...
QUALITY_IMPACT: ...
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
