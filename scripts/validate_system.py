#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
REQ=['AGENTS.md','START_HERE.md','SYSTEM/CONSTITUTION.md','SYSTEM/STATE.md','SYSTEM/ROADMAP.md','SYSTEM/DECISIONS.md','SYSTEM/TASK_LEDGER.md','SYSTEM/KNOWLEDGE_INDEX.md','SYSTEM/AGENT_ROLES.md','SYSTEM/TEMPLATES.md','SYSTEM/ORCHESTRATOR_LEASE.md','SYSTEM/SUCCESS_MODEL.md','SYSTEM/SUCCESS_SCORECARD.md','SYSTEM/PARTNER_OUTCOME_MODEL.md','SYSTEM/PARTNER_SCORECARD.md','SYSTEM/QUALITY_MODEL.md','SYSTEM/QUALITY_SCORECARD.md','SYSTEM/TRACEABILITY_MATRIX.md','SYSTEM/ASSUMPTION_RISK_REGISTER.md','SYSTEM/FINAL_REVIEW_PROTOCOL.md','SYSTEM/AUTOPILOT.md','SYSTEM/DISPATCH/README.md','SYSTEM/CHECKPOINTS/README.md','SYSTEM/WAVES/README.md','SYSTEM/WAVES/_TEMPLATE.json','SYSTEM/RESULTS/README.md']
RUNTIME={'SYSTEM/STATE.md','SYSTEM/ROADMAP.md','SYSTEM/DECISIONS.md','SYSTEM/TASK_LEDGER.md','SYSTEM/KNOWLEDGE_INDEX.md','SYSTEM/SUCCESS_SCORECARD.md','SYSTEM/PARTNER_SCORECARD.md','SYSTEM/QUALITY_SCORECARD.md','SYSTEM/TRACEABILITY_MATRIX.md','SYSTEM/ASSUMPTION_RISK_REGISTER.md'}
PROTO={'AGENTS.md','START_HERE.md','SYSTEM/CONSTITUTION.md','SYSTEM/ORCHESTRATOR_LEASE.md','SYSTEM/TEMPLATES.md','SYSTEM/SUCCESS_MODEL.md','SYSTEM/PARTNER_OUTCOME_MODEL.md','SYSTEM/QUALITY_MODEL.md','SYSTEM/FINAL_REVIEW_PROTOCOL.md','SYSTEM/AUTOPILOT.md','SYSTEM/DISPATCH/README.md','SYSTEM/AGENT_ROLES.md','scripts/validate_system.py','.github/workflows/system-integrity.yml','.github/CODEOWNERS'}
PRODUCT=('src/','tests/','data/','docs/','deliverables/','app/','web/')
ALLOWED={'PLANNED','READY','RUNNING','BLOCKED','RESULT_RECEIVED','INTEGRATED','CANCELLED','STALE'}; errors=[]
def fail(x): errors.append(x)
def read(p):
 f=ROOT/p
 if not f.exists(): fail('missing required file: '+p); return ''
 return f.read_text(encoding='utf-8')
def field(t,n):
 m=re.search(rf'`{re.escape(n)}:\s*([^`]+)`',t); return m.group(1).strip() if m else None
def show(ref,p):
 r=subprocess.run(['git','show',f'{ref}:{p}'],cwd=ROOT,text=True,capture_output=True); return r.stdout if r.returncode==0 else None
def git(*a):
 r=subprocess.run(['git',*a],cwd=ROOT,text=True,capture_output=True)
 if r.returncode: fail('git failed: '+r.stderr.strip()); return ''
 return r.stdout
def state_num(t):
 v=field(t,'STATE_VERSION'); return int(v) if v and re.fullmatch(r'\d{4}',v) else None
def wave(p):
 try:d=json.loads(p.read_text())
 except Exception as e: fail(f'invalid wave {p}: {e}'); return
 wid=d.get('wave_id'); ts=d.get('tasks')
 if p.stem!=wid or not re.fullmatch(r'W\d{3}',str(wid or '')): fail('invalid wave id '+p.name)
 if not re.fullmatch(r'\d{4}',str(d.get('base_state_version',''))): fail('invalid wave base state')
 if not re.fullmatch(r'[0-9a-f]{40}',str(d.get('base_commit_sha',''))): fail('invalid wave base sha')
 if not isinstance(ts,list) or not ts: fail('wave has no tasks'); return
 ids=set(); g={}
 for t in ts:
  tid=t.get('task_id'); att=t.get('attempt_id')
  if not re.fullmatch(rf'{re.escape(wid or "")}-T\d{{3}}',str(tid or '')): fail('bad task '+str(tid)); continue
  if tid in ids: fail('duplicate '+tid)
  ids.add(tid); g[tid]=t.get('dependencies',[]) if isinstance(t.get('dependencies',[]),list) else []
  if not re.fullmatch(r'A\d{2,}',str(att or '')): fail('bad attempt '+tid)
  if t.get('status') not in ALLOWED: fail('bad status '+tid)
 for t,ds in g.items():
  for d in ds:
   if d not in ids: fail(f'{t} depends unknown {d}')
 visiting=set(); visited=set()
 def dfs(n):
  if n in visiting: fail('dependency cycle '+n); return
  if n in visited:return
  visiting.add(n)
  for x in g.get(n,[]):dfs(x)
  visiting.remove(n); visited.add(n)
 for n in g:dfs(n)
ap=argparse.ArgumentParser(); ap.add_argument('--base-ref'); args=ap.parse_args()
for p in REQ:
 if not (ROOT/p).exists():fail('missing required file: '+p)
con=read('SYSTEM/CONSTITUTION.md'); state=read('SYSTEM/STATE.md'); roadmap=read('SYSTEM/ROADMAP.md'); dec=read('SYSTEM/DECISIONS.md'); ledger=read('SYSTEM/TASK_LEDGER.md'); success=read('SYSTEM/SUCCESS_MODEL.md'); ss=read('SYSTEM/SUCCESS_SCORECARD.md'); ps=read('SYSTEM/PARTNER_SCORECARD.md'); qs=read('SYSTEM/QUALITY_SCORECARD.md')
pc=field(con,'PROTOCOL_VERSION'); pv=field(state,'PROTOCOL_VERSION'); sv=field(state,'STATE_VERSION'); phase=field(state,'CURRENT_PHASE'); project=field(state,'PROJECT_STATUS'); sst=field(ss,'SUCCESS_STATUS'); ssstop=field(ss,'SUCCESS_STOP_CONDITION'); pst=field(ps,'PARTNER_STATUS'); pstop=field(ps,'PARTNER_STOP_CONDITION'); qst=field(qs,'QUALITY_STATUS'); qstop=field(qs,'STOP_CONDITION'); blind=field(ss,'BLIND_REVIEW'); trace=field(ss,'TRACEABILITY_STATUS'); assumptions=field(ss,'CRITICAL_ASSUMPTIONS_STATUS')
if not pc or pc!=pv:fail(f'protocol mismatch {pc}/{pv}')
if not sv or not re.fullmatch(r'\d{4}',sv):fail('invalid state version')
if project not in {'ACTIVE','PAUSED','COMPLETE'}:fail('invalid project status')
ph=re.fullmatch(r'(\d+)\s+—\s+(.+)',phase or '')
if not ph or f'## Phase {ph.group(1)} — {ph.group(2)}' not in roadmap:fail('phase not in roadmap')
for x in ['MAXIMIZE expected_total_success','Hard gates globais','Traceability chain','Independent final validation']:
 if x not in success:fail('success invariant missing: '+x)
for x in ['A função objetivo dominante é maximizar sucesso total balanceado','Nenhuma média/score agregado pode compensar falha de hard gate crítico','Finalização exige blind review independente']:
 if x not in con:fail('constitution invariant missing: '+x)
if project=='COMPLETE':
 if (sst,ssstop,pst,pstop,qst,qstop,blind,trace,assumptions)!=('PASS','PASS','PASS','PASS','PASS','PASS','PASS','COMPLETE','CONTROLLED'): fail('COMPLETE requires success/partner/quality/blind/traceability/assumptions PASS')
ids=re.findall(r'^## (D-\d{4})\b',dec,flags=re.M)
if len(ids)!=len(set(ids)):fail('duplicate decision ids')
for did in set(re.findall(r'\bD-\d{4}\b',state)):
 if f'## {did} ' not in dec:fail('missing decision '+did)
nxt=re.search(r'## Próximo ID disponível\s+\n+`(D-\d{4})`',dec)
if ids and nxt and int(nxt.group(1).split('-')[1])!=max(int(x.split('-')[1]) for x in ids)+1:fail('bad next decision')
for tid in set(re.findall(r'\b(?:BOOT-T\d{3}|W\d{3}-T\d{3})\b',state)):
 if tid not in ledger:fail('task missing ledger '+tid)
if sv:
 cp=ROOT/f'SYSTEM/CHECKPOINTS/STATE-v{sv}.md'
 if not cp.exists():fail('missing checkpoint')
 elif cp.read_text()!=state:fail('checkpoint != state')
 cps=[int(p.stem.split('v')[1]) for p in (ROOT/'SYSTEM/CHECKPOINTS').glob('STATE-v[0-9][0-9][0-9][0-9].md')]
 if cps and max(cps)!=int(sv):fail('highest checkpoint mismatch')
for p in (ROOT/'SYSTEM/WAVES').glob('W[0-9][0-9][0-9].json'):wave(p)
if args.base_ref:
 base=args.base_ref; changed={x for x in git('diff','--name-only',f'{base}...HEAD').splitlines() if x}; bs=show(base,'SYSTEM/STATE.md') or ''; bc=show(base,'SYSTEM/CONSTITUTION.md') or ''; bd=show(base,'SYSTEM/DECISIONS.md') or ''
 runtime=bool(changed&RUNTIME) or any(re.fullmatch(r'SYSTEM/WAVES/W\d{3}\.json',p) for p in changed); proto=bool(changed&PROTO); product=any(p.startswith(PRODUCT) for p in changed); state_changed='SYSTEM/STATE.md' in changed; old=state_num(bs); new=state_num(state)
 if runtime and not state_changed:fail('runtime canonical changed without state')
 if state_changed and old is not None and new!=old+1:fail(f'state must +1 {old}->{new}')
 if state_changed and f'SYSTEM/CHECKPOINTS/STATE-v{sv}.md' not in changed:fail('state changed without checkpoint')
 if proto:
  if field(bc,'PROTOCOL_VERSION')==pc:fail('protocol changed without bump')
  if 'SYSTEM/DECISIONS.md' not in changed:fail('protocol change requires decisions')
  if product:fail('protocol mixed with product')
  oldids=set(re.findall(r'^## (D-\d{4})\b',bd,flags=re.M))
  if not(set(ids)-oldids):fail('protocol change requires new decision')
 for p in changed:
  m=re.fullmatch(r'SYSTEM/CHECKPOINTS/STATE-v(\d{4})\.md',p)
  if m and old is not None and int(m.group(1))<=old and show(base,p) is not None:fail('existing checkpoint modified '+p)
if errors:
 print('SYSTEM INTEGRITY CHECK: FAIL'); [print('-',e) for e in errors]; sys.exit(1)
print('SYSTEM INTEGRITY CHECK: PASS'); print(f'protocol={pv} state={sv} phase={phase} success={sst}/{ssstop} partner={pst}/{pstop} quality={qst}/{qstop}')
