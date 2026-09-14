#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "AGENTS.md",
    "START_HERE.md",
    "SYSTEM/CONSTITUTION.md",
    "SYSTEM/STATE.md",
    "SYSTEM/ROADMAP.md",
    "SYSTEM/DECISIONS.md",
    "SYSTEM/TASK_LEDGER.md",
    "SYSTEM/KNOWLEDGE_INDEX.md",
    "SYSTEM/AGENT_ROLES.md",
    "SYSTEM/TEMPLATES.md",
]

errors = []


def fail(msg: str) -> None:
    errors.append(msg)


def read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        fail(f"missing required file: {path}")
        return ""
    return p.read_text(encoding="utf-8")


def field(text: str, name: str):
    m = re.search(rf"`{re.escape(name)}:\s*([^`]+)`", text)
    return m.group(1).strip() if m else None


for path in REQUIRED:
    if not (ROOT / path).exists():
        fail(f"missing required file: {path}")

constitution = read("SYSTEM/CONSTITUTION.md")
state = read("SYSTEM/STATE.md")
roadmap = read("SYSTEM/ROADMAP.md")
decisions = read("SYSTEM/DECISIONS.md")
ledger = read("SYSTEM/TASK_LEDGER.md")

protocol_constitution = field(constitution, "PROTOCOL_VERSION")
protocol_state = field(state, "PROTOCOL_VERSION")
state_version = field(state, "STATE_VERSION")
current_phase = field(state, "CURRENT_PHASE")
project_status = field(state, "PROJECT_STATUS")

if not protocol_constitution:
    fail("CONSTITUTION.md has no PROTOCOL_VERSION")
if not protocol_state:
    fail("STATE.md has no PROTOCOL_VERSION")
if protocol_constitution and protocol_state and protocol_constitution != protocol_state:
    fail(
        f"protocol version mismatch: constitution={protocol_constitution}, state={protocol_state}"
    )

if not state_version or not re.fullmatch(r"\d{4}", state_version):
    fail(f"STATE_VERSION must be exactly four digits; got {state_version!r}")

if project_status not in {"ACTIVE", "PAUSED", "COMPLETE"}:
    fail(f"invalid PROJECT_STATUS: {project_status!r}")

phase_match = re.fullmatch(r"(\d+)\s+—\s+(.+)", current_phase or "")
if not phase_match:
    fail(f"invalid CURRENT_PHASE format: {current_phase!r}")
else:
    phase_number, phase_name = phase_match.groups()
    heading = f"## Phase {phase_number} — {phase_name}"
    if heading not in roadmap:
        fail(f"CURRENT_PHASE not found in ROADMAP.md: {heading}")

# Every decision referenced by STATE must exist in the decision log.
state_decisions = sorted(set(re.findall(r"\bD-\d{4}\b", state)))
for decision_id in state_decisions:
    if f"## {decision_id} " not in decisions:
        fail(f"STATE.md references missing decision: {decision_id}")

# Decision IDs may not be reused.
decision_headings = re.findall(r"^## (D-\d{4})\b", decisions, flags=re.MULTILINE)
if len(decision_headings) != len(set(decision_headings)):
    fail("DECISIONS.md contains duplicate decision IDs")

# Next decision ID must be greater than the highest registered ID.
next_id_match = re.search(r"## Próximo ID disponível\s+\n+`(D-\d{4})`", decisions)
if decision_headings and next_id_match:
    highest = max(int(x.split("-")[1]) for x in decision_headings)
    nxt = int(next_id_match.group(1).split("-")[1])
    if nxt != highest + 1:
        fail(f"next decision ID should be D-{highest + 1:04d}, got D-{nxt:04d}")

# Active tasks in STATE must be registered in the canonical ledger.
task_ids = sorted(set(re.findall(r"\b(?:BOOT-T\d{3}|W\d{3}-T\d{3})\b", state)))
for task_id in task_ids:
    if task_id not in ledger:
        fail(f"STATE.md references task absent from TASK_LEDGER.md: {task_id}")

# Guard against accidental deletion of core invariants.
for phrase in [
    "O GitHub é a fonte de verdade",
    "Somente o Orchestrator altera arquivos canônicos",
    "Toda tarefa tem `TASK_ID` e `BASE_STATE_VERSION`",
    "Nenhuma fase avança sem satisfazer seu gate no roadmap",
]:
    if phrase not in constitution:
        fail(f"constitutional invariant missing: {phrase}")

if errors:
    print("SYSTEM INTEGRITY CHECK: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("SYSTEM INTEGRITY CHECK: PASS")
print(f"protocol={protocol_state} state={state_version} phase={current_phase}")
