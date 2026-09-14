#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re
import subprocess
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
    "SYSTEM/ORCHESTRATOR_LEASE.md",
    "SYSTEM/CHECKPOINTS/README.md",
    "SYSTEM/WAVES/README.md",
    "SYSTEM/WAVES/_TEMPLATE.json",
    "SYSTEM/RESULTS/README.md",
]

RUNTIME_CANONICAL = {
    "SYSTEM/STATE.md",
    "SYSTEM/ROADMAP.md",
    "SYSTEM/DECISIONS.md",
    "SYSTEM/TASK_LEDGER.md",
    "SYSTEM/KNOWLEDGE_INDEX.md",
}
PROTOCOL_FILES = {
    "AGENTS.md",
    "START_HERE.md",
    "SYSTEM/CONSTITUTION.md",
    "SYSTEM/ORCHESTRATOR_LEASE.md",
    "SYSTEM/TEMPLATES.md",
    "scripts/validate_system.py",
    ".github/workflows/system-integrity.yml",
    ".github/CODEOWNERS",
}
PRODUCT_PREFIXES = ("src/", "tests/", "data/", "docs/", "deliverables/", "app/", "web/")
ALLOWED_TASK_STATUS = {
    "PLANNED", "READY", "RUNNING", "BLOCKED", "RESULT_RECEIVED",
    "INTEGRATED", "CANCELLED", "STALE"
}

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


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if check and result.returncode != 0:
        fail(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return ""
    return result.stdout


def git_show(ref: str, path: str):
    result = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        return None
    return result.stdout


def parse_state_version(text: str):
    value = field(text, "STATE_VERSION")
    return int(value) if value and re.fullmatch(r"\d{4}", value) else None


def validate_wave(path: Path) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid wave JSON {path.relative_to(ROOT)}: {exc}")
        return

    wave_id = data.get("wave_id")
    if path.stem != wave_id:
        fail(f"wave filename/id mismatch: {path.name} vs {wave_id!r}")
    if not re.fullmatch(r"W\d{3}", str(wave_id or "")):
        fail(f"invalid wave_id in {path.name}: {wave_id!r}")
    if not re.fullmatch(r"\d{4}", str(data.get("base_state_version", ""))):
        fail(f"invalid base_state_version in {path.name}")
    if not re.fullmatch(r"[0-9a-f]{40}", str(data.get("base_commit_sha", ""))):
        fail(f"invalid base_commit_sha in {path.name}")

    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        fail(f"wave {path.name} must contain non-empty tasks")
        return

    ids = set()
    graph = {}
    for task in tasks:
        task_id = task.get("task_id")
        attempt = task.get("attempt_id")
        if not re.fullmatch(rf"{re.escape(wave_id or '')}-T\d{{3}}", str(task_id or "")):
            fail(f"invalid task_id {task_id!r} in {path.name}")
            continue
        if task_id in ids:
            fail(f"duplicate task_id {task_id} in {path.name}")
        ids.add(task_id)
        if not re.fullmatch(r"A\d{2,}", str(attempt or "")):
            fail(f"invalid attempt_id for {task_id}: {attempt!r}")
        if task.get("status") not in ALLOWED_TASK_STATUS:
            fail(f"invalid task status for {task_id}: {task.get('status')!r}")
        deps = task.get("dependencies", [])
        if not isinstance(deps, list):
            fail(f"dependencies for {task_id} must be a list")
            deps = []
        graph[task_id] = deps

    for task_id, deps in graph.items():
        for dep in deps:
            if dep not in ids:
                fail(f"{task_id} depends on unknown task {dep} in {path.name}")

    visiting, visited = set(), set()
    def dfs(node):
        if node in visiting:
            fail(f"dependency cycle detected in {path.name} at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, []):
            dfs(dep)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        dfs(node)


parser = argparse.ArgumentParser()
parser.add_argument("--base-ref", help="base commit/ref for differential validation")
args = parser.parse_args()

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
    fail(f"protocol version mismatch: constitution={protocol_constitution}, state={protocol_state}")
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

# Decisions referenced by STATE must exist; IDs cannot be reused.
state_decisions = sorted(set(re.findall(r"\bD-\d{4}\b", state)))
for decision_id in state_decisions:
    if f"## {decision_id} " not in decisions:
        fail(f"STATE.md references missing decision: {decision_id}")
decision_headings = re.findall(r"^## (D-\d{4})\b", decisions, flags=re.MULTILINE)
if len(decision_headings) != len(set(decision_headings)):
    fail("DECISIONS.md contains duplicate decision IDs")
next_id_match = re.search(r"## Próximo ID disponível\s+\n+`(D-\d{4})`", decisions)
if decision_headings and next_id_match:
    highest = max(int(x.split("-")[1]) for x in decision_headings)
    nxt = int(next_id_match.group(1).split("-")[1])
    if nxt != highest + 1:
        fail(f"next decision ID should be D-{highest + 1:04d}, got D-{nxt:04d}")

# Active tasks in STATE must exist in ledger.
task_ids = sorted(set(re.findall(r"\b(?:BOOT-T\d{3}|W\d{3}-T\d{3})\b", state)))
for task_id in task_ids:
    if task_id not in ledger:
        fail(f"STATE.md references task absent from TASK_LEDGER.md: {task_id}")

# Checkpoint must exactly mirror current state and be the highest state checkpoint.
if state_version and re.fullmatch(r"\d{4}", state_version):
    checkpoint = ROOT / f"SYSTEM/CHECKPOINTS/STATE-v{state_version}.md"
    if not checkpoint.exists():
        fail(f"missing checkpoint for current state: {checkpoint.relative_to(ROOT)}")
    elif checkpoint.read_text(encoding="utf-8") != state:
        fail(f"current checkpoint does not exactly match SYSTEM/STATE.md: {checkpoint.name}")
    checkpoints = []
    for p in (ROOT / "SYSTEM/CHECKPOINTS").glob("STATE-v[0-9][0-9][0-9][0-9].md"):
        checkpoints.append(int(p.stem.split("v")[1]))
    if checkpoints and max(checkpoints) != int(state_version):
        fail(f"highest checkpoint v{max(checkpoints):04d} != current state v{int(state_version):04d}")

# Validate executable wave manifests.
for path in sorted((ROOT / "SYSTEM/WAVES").glob("W[0-9][0-9][0-9].json")):
    validate_wave(path)

# Guard core invariants against accidental deletion.
for phrase in [
    "O GitHub é a fonte de verdade",
    "Somente o Orchestrator com lease ativo altera arquivos canônicos",
    "Toda tarefa tem `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION` e `BASE_COMMIT_SHA`",
    "Nenhuma fase avança sem satisfazer seu gate no roadmap",
    "Todo incremento de estado cria checkpoint imutável",
]:
    if phrase not in constitution:
        fail(f"constitutional invariant missing: {phrase}")

# Differential validation for PRs.
if args.base_ref:
    base = args.base_ref
    changed = {x.strip() for x in git("diff", "--name-only", f"{base}...HEAD").splitlines() if x.strip()}
    base_state = git_show(base, "SYSTEM/STATE.md")
    base_constitution = git_show(base, "SYSTEM/CONSTITUTION.md")
    base_decisions = git_show(base, "SYSTEM/DECISIONS.md")

    runtime_changed = bool(changed & RUNTIME_CANONICAL) or any(re.fullmatch(r"SYSTEM/WAVES/W\d{3}\.json", p) for p in changed)
    protocol_changed = bool(changed & PROTOCOL_FILES)
    product_changed = any(p.startswith(PRODUCT_PREFIXES) for p in changed)

    old_state_num = parse_state_version(base_state or "")
    new_state_num = parse_state_version(state)
    state_changed = "SYSTEM/STATE.md" in changed

    if runtime_changed and not state_changed:
        fail("runtime canonical files changed without SYSTEM/STATE.md change")
    if state_changed and old_state_num is not None and new_state_num != old_state_num + 1:
        fail(f"STATE_VERSION must increment exactly by 1: old={old_state_num:04d}, new={new_state_num}")
    if state_changed and state_version:
        expected_cp = f"SYSTEM/CHECKPOINTS/STATE-v{state_version}.md"
        if expected_cp not in changed:
            fail(f"state changed but new checkpoint is not part of diff: {expected_cp}")

    old_protocol = field(base_constitution or "", "PROTOCOL_VERSION")
    if protocol_changed:
        if protocol_constitution == old_protocol:
            fail("protocol/governance files changed without PROTOCOL_VERSION bump")
        if "SYSTEM/DECISIONS.md" not in changed:
            fail("protocol/governance change requires SYSTEM/DECISIONS.md update")
        if product_changed:
            fail("protocol/governance changes must not be mixed with product changes in the same PR")
        old_ids = set(re.findall(r"^## (D-\d{4})\b", base_decisions or "", flags=re.MULTILINE))
        new_ids = set(decision_headings)
        if not (new_ids - old_ids):
            fail("protocol/governance change requires at least one new decision ID")

    # Existing checkpoints are append-only.
    for p in changed:
        m = re.fullmatch(r"SYSTEM/CHECKPOINTS/STATE-v(\d{4})\.md", p)
        if m and old_state_num is not None and int(m.group(1)) <= old_state_num:
            if git_show(base, p) is not None:
                fail(f"existing checkpoint modified: {p}")

if errors:
    print("SYSTEM INTEGRITY CHECK: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("SYSTEM INTEGRITY CHECK: PASS")
print(f"protocol={protocol_state} state={state_version} phase={current_phase}")
