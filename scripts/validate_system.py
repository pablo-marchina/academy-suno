#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
 'AGENTS.md','START_HERE.md','SYSTEM/CONSTITUTION.md','SYSTEM/STATE.md','SYSTEM/ROADMAP.md','SYSTEM/DECISIONS.md','SYSTEM/TASK_LEDGER.md','SYSTEM/KNOWLEDGE_INDEX.md','SYSTEM/AGENT_ROLES.md','SYSTEM/TEMPLATES.md','SYSTEM/ORCHESTRATOR_LEASE.md','SYSTEM/QUALITY_MODEL.md','SYSTEM/QUALITY_SCORECARD.md','SYSTEM/AUTOPILOT.md','SYSTEM/DISPATCH/README.md','SYSTEM/CHECKPOINTS/README.md','SYSTEM/WAVES/README.md','SYSTEM/WAVES/_TEMPLATE.json','SYSTEM/RESULTS/README.md']
RUNTIME_CANONICAL={'SYSTEM/STATE.md','SYSTEM/ROADMAP.md','SYSTEM/DECISIONS.md','SYSTEM/TASK_LEDGER.md','SYSTEM/KNOWLEDGE_INDEX.md','SYSTEM/QUALITY_SCORECARD.md'}
PROTOCOL_FILES={'AGENTS.md','START_HERE.md','SYSTEM/CONSTITUTION.md','SYSTEM/ORCHESTRATOR_LEASE.md','SYSTEM/TEMPLATES.md','SYSTEM/QUALITY_MODEL.md','SYSTEM/AUTOPILOT.md','SYSTEM/DISPATCH/README.md','scripts/validate_system.py','.github/workflows/system-integrity.yml','.github/CODEOWNERS'}
PRODUCT_PREFIXES=('src/','tests/','data/','docs/','deliverables/','app/','web/')
ALLOWED_TASK_STATUS={'PLANNED','READY','RUNNING','BLOCKED','RESULT_RECEIVED','INTEGRATED','CANCELLED','STALE'}
errors=[]
def fail(x): errors.append(x)
def read(p):
 f=ROOT/p
 if not f.exists(): fail(f'missing required file: {p}'); return ''
 return f.read_text(encoding='utf-8')
def field(t,n):
 m=re.search(rf'`{re.escape(n)}:\s*([^`]+)`',t); return m.group(1).strip() if m else None
def git(*a):
 r=subprocess.run(['git',*a],cwd=ROOT,text=True,capture_output=True)
 if r.returncode: fail(f"git {' '.join(a)} failed: {r.stderr.strip()}"); return ''
 return r.stdout
def show(ref,p):
 r=subprocess.run(['git','show',f'{ref}:{p}'],cwd=ROOT,text=True,capture_output=True); return r.stdout if r.returncode==0 else None
def state_num(t):
 v=field(t,'STATE_VERSION'); return int(v) if v and re.fullmatch(r'\d{4}',v) else None

def validate_wave(p):
 try: d=json.loads(p.read_text(encoding='utf-8'))
 except Exception as e: fail(f'invalid wave JSON {p}: {e}'); return
 wid=d.get('wave_id'); tasks=d.get('tasks')
 if p.stem!=wid or not re.fullmatch(r'W\d{3}',str(wid or '')): fail(f'invalid wave id/file: {p.name}')
 if not re.fullmatch(r'\d{4}',str(d.get('base_state_version',''))): fail(f'invalid base state in {p.name}')
 if not re.fullmatch(r'[0-9a-f]{40}',str(d.get('base_commit_sha',''))): fail(f'invalid base sha in {p.name}')
 if not isinstance(tasks,list) or not tasks: fail(f'wave {p.name} must contain tasks'); return
 ids=set(); graph={}
 for t in tasks:
  tid=t.get('task_id'); att=t.get('attempt_id')
  if not re.fullmatch(rf'{re.escape(wid or "")}-T\d{{3}}',str(tid or '')): fail(f'invalid task {tid} in {p.name}'); continue
  if tid in ids: fail(f'duplicate task {tid} in {p.name}')
  ids.add(tid)
  if not re.fullmatch(r'A\d{2,}',str(att or '')): fail(f'invalid attempt for {tid}')
  if t.get('status') not in ALLOWED_TASK_STATUS: fail(f'invalid status for {tid}')
  deps=t.get('dependencies',[]); graph[tid]=deps if isinstance(deps,list) else []
 for tid,deps in graph.items():
  for dep in deps:
   if dep not in ids: fail(f'{tid} depends on unknown {dep}')
 visiting=set(); visited=set()
 def dfs(n):
  if n in visiting: fail(f'dependency cycle in {p.name} at {n}'); return
  if n in visited: return
  visiting.add(n)
  for x in graph.get(n,[]): dfs(x)
  visiting.remove(n); visited.add(n)
 for n in graph: dfs(n)

ap=argparse.ArgumentParser(); ap.add_argument('--base-ref'); args=ap.parse_args()
for p in REQUIRED:
 if not (ROOT/p).exists(): fail(f'missing required file: {p}')
constitution=read('SYSTEM/CONSTITUTION.md'); state=read('SYSTEM/STATE.md'); roadmap=read('SYSTEM/ROADMAP.md'); decisions=read('SYSTEM/DECISIONS.md'); ledger=read('SYSTEM/TASK_LEDGER.md'); qm=read('SYSTEM/QUALITY_MODEL.md'); qs=read('SYSTEM/QUALITY_SCORECARD.md')
pc=field(constitution,'PROTOCOL_VERSION'); ps=field(state,'PROTOCOL_VERSION'); sv=field(state,'STATE_VERSION'); phase=field(state,'CURRENT_PHASE'); status=field(state,'PROJECT_STATUS'); qstatus=field(qs,'QUALITY_STATUS'); stop=field(qs,'STOP_CONDITION')
if not pc or not ps or pc!=ps: fail(f'protocol version mismatch: constitution={pc}, state={ps}')
if not sv or not re.fullmatch(r'\d{4}',sv): fail(f'invalid STATE_VERSION {sv!r}')
if status not in {'ACTIVE','PAUSED','COMPLETE'}: fail(f'invalid PROJECT_STATUS {status!r}')
pm=re.fullmatch(r'(\d+)\s+—\s+(.+)',phase or '')
if not pm or f'## Phase {pm.group(1)} — {pm.group(2)}' not in roadmap: fail(f'CURRENT_PHASE not found in roadmap: {phase!r}')
for phrase in ['MAXIMIZE expected_evaluator_quality','Hard gates','Quality loop','Anti-gaming']:
 if phrase not in qm: fail(f'quality model invariant missing: {phrase}')
for phrase in ['A função objetivo dominante é maximizar a qualidade esperada do case final','Todo incremento de estado cria checkpoint imutável','Somente o Orchestrator com lease ativo altera arquivos canônicos']:
 if phrase not in constitution: fail(f'constitutional invariant missing: {phrase}')
if status=='COMPLETE' and (qstatus!='PASS' or stop!='PASS'): fail('PROJECT_STATUS COMPLETE requires QUALITY_STATUS PASS and STOP_CONDITION PASS')
ids=re.findall(r'^## (D-\d{4})\b',decisions,flags=re.M)
if len(ids)!=len(set(ids)): fail('duplicate decision IDs')
for did in set(re.findall(r'\bD-\d{4}\b',state)):
 if f'## {did} ' not in decisions: fail(f'state references missing decision {did}')
nxt=re.search(r'## Próximo ID disponível\s+\n+`(D-\d{4})`',decisions)
if ids and nxt and int(nxt.group(1).split('-')[1])!=max(int(x.split('-')[1]) for x in ids)+1: fail('invalid next decision id')
for tid in set(re.findall(r'\b(?:BOOT-T\d{3}|W\d{3}-T\d{3})\b',state)):
 if tid not in ledger: fail(f'state task missing in ledger: {tid}')
if sv:
 cp=ROOT/f'SYSTEM/CHECKPOINTS/STATE-v{sv}.md'
 if not cp.exists(): fail(f'missing checkpoint v{sv}')
 elif cp.read_text(encoding='utf-8')!=state: fail(f'checkpoint v{sv} != STATE.md')
 cps=[int(p.stem.split('v')[1]) for p in (ROOT/'SYSTEM/CHECKPOINTS').glob('STATE-v[0-9][0-9][0-9][0-9].md')]
 if cps and max(cps)!=int(sv): fail('highest checkpoint != current state')
for p in sorted((ROOT/'SYSTEM/WAVES').glob('W[0-9][0-9][0-9].json')): validate_wave(p)

if args.base_ref:
 base=args.base_ref; changed={x for x in git('diff','--name-only',f'{base}...HEAD').splitlines() if x}; bs=show(base,'SYSTEM/STATE.md') or ''; bc=show(base,'SYSTEM/CONSTITUTION.md') or ''; bd=show(base,'SYSTEM/DECISIONS.md') or ''
 runtime=bool(changed & RUNTIME_CANONICAL) or any(re.fullmatch(r'SYSTEM/WAVES/W\d{3}\.json',p) for p in changed)
 proto=bool(changed & PROTOCOL_FILES); product=any(p.startswith(PRODUCT_PREFIXES) for p in changed); state_changed='SYSTEM/STATE.md' in changed
 old=state_num(bs); new=state_num(state)
 if runtime and not state_changed: fail('runtime canonical changed without STATE.md')
 if state_changed and old is not None and new!=old+1: fail(f'STATE_VERSION must increment exactly by 1: {old}->{new}')
 if state_changed and f'SYSTEM/CHECKPOINTS/STATE-v{sv}.md' not in changed: fail('state changed without matching new checkpoint')
 oldp=field(bc,'PROTOCOL_VERSION')
 if proto:
  if pc==oldp: fail('protocol files changed without protocol bump')
  if 'SYSTEM/DECISIONS.md' not in changed: fail('protocol change requires decisions update')
  if product: fail('protocol change mixed with product change')
  oldids=set(re.findall(r'^## (D-\d{4})\b',bd,flags=re.M))
  if not (set(ids)-oldids): fail('protocol change requires new decision ID')
 for p in changed:
  m=re.fullmatch(r'SYSTEM/CHECKPOINTS/STATE-v(\d{4})\.md',p)
  if m and old is not None and int(m.group(1))<=old and show(base,p) is not None: fail(f'existing checkpoint modified: {p}')

if errors:
 print('SYSTEM INTEGRITY CHECK: FAIL'); [print('-',e) for e in errors]; sys.exit(1)
print('SYSTEM INTEGRITY CHECK: PASS'); print(f'protocol={ps} state={sv} phase={phase} quality={qstatus} stop={stop}')
