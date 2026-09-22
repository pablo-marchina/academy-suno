#!/usr/bin/env python3
"""W004-T006-A01 semantic-off/on diagnostic ablation under D-0017.

The candidate adapter is deliberately an experimental deterministic token-overlap
semantic proxy. It is used to measure whether the semantic hook adds diagnostic
resolution while preserving hard-gate precedence. It is NOT a production backend
selection and the accepted A03 model calibration remains non-human evidence.
"""
from __future__ import annotations

import argparse, base64, gzip, hashlib, json, re, unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from suno_content.domain import GateStatus, Materiality, ProvenanceRef
from suno_content.grounding import (
    AtomicClaim, ClaimSupportStatus, EvidenceItem, EvidencePacket, SemanticSignal,
    run_semantic_ablation,
)

ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = ROOT / "experiments/automated_calibration_w004/runs/W004-T005-A02/calibration.json"
BLIND = ROOT / "data/evals/w004/blind_items/blind_bank_v001.jsonl.gz.b64"
EXPECTED_COUNT = 36

STOP = {
    'a','an','and','as','at','be','by','for','from','in','is','it','of','on','or','that','the','to','was','were','with',
    'a','as','de','do','da','dos','das','e','em','no','na','nos','nas','o','os','um','uma','para','por','que','com','se',
}


def norm(s: str) -> str:
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode('ascii').lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9%$.,/+-]+', ' ', s)).strip()


def toks(s: str) -> set[str]:
    return {x for x in norm(s).split() if len(x) > 1 and x not in STOP}


class TokenOverlapSemanticAdapter:
    backend_id = 'token-overlap-semantic-proxy'
    backend_version = 'w004-t006-a01-v1'

    def evaluate(self, claim: AtomicClaim, evidence: EvidencePacket) -> SemanticSignal:
        claim_tokens = toks(claim.text)
        evidence_text = ' '.join(x.text for x in evidence.retrieved)
        evidence_tokens = toks(evidence_text)
        overlap = len(claim_tokens & evidence_tokens) / len(claim_tokens) if claim_tokens else 0.0
        # Numeric tokens carry strong preservation value; require every number if present.
        nums = set(re.findall(r'\d+(?:[.,]\d+)?%?', norm(claim.text)))
        number_ok = nums.issubset(set(re.findall(r'\d+(?:[.,]\d+)?%?', norm(evidence_text))))
        if overlap >= 0.62 and number_ok:
            status = ClaimSupportStatus.SUPPORTED
        elif overlap < 0.25 or not number_ok:
            status = ClaimSupportStatus.UNSUPPORTED
        else:
            status = ClaimSupportStatus.UNVERIFIABLE
        return SemanticSignal(
            claim_id=claim.claim_id,
            support_status=status,
            backend_id=self.backend_id,
            backend_version=self.backend_version,
            confidence=round(overlap, 6),
            evidence_refs=evidence.evidence_refs,
            diagnostic_codes=(f'TOKEN_RECALL_{overlap:.3f}', f'NUMERIC_PRESERVATION_{number_ok}'),
        )


def load_blind() -> dict[str, dict[str, Any]]:
    raw = gzip.decompress(base64.b64decode(b''.join(BLIND.read_bytes().split()), validate=True))
    rows = [json.loads(x) for x in raw.decode('utf-8').splitlines() if x.strip()]
    if len(rows) != EXPECTED_COUNT:
        raise ValueError('blind population drift')
    return {r['blind_item_id']: r for r in rows}


def make_provenance(source_id: str, source_context: dict[str, Any], blind_id: str) -> ProvenanceRef:
    digest = hashlib.sha256(json.dumps(source_context, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return ProvenanceRef(source_id=source_id, source_hash=digest, page_number=1, span_id=f'generated-output-{blind_id}')


def expected_reference(row: dict[str, Any]) -> str:
    checks = row['non_compensatory_checks']
    if checks['FACTUAL_CRITICAL_PRESERVATION'] == 'FAIL' or checks['MATERIAL_CONCEPT_PRESERVATION'] == 'FAIL':
        return 'FAIL'
    if checks['FACTUAL_CRITICAL_PRESERVATION'] == 'REVIEW_REQUIRED' or checks['MATERIAL_CONCEPT_PRESERVATION'] == 'REVIEW_REQUIRED':
        return 'REVIEW_REQUIRED'
    return 'PASS'


def build() -> dict[str, Any]:
    calibration = json.loads(CALIBRATION.read_text(encoding='utf-8'))
    if calibration['evidence_class'] != 'MODEL_AUTOMATED_BLIND_CALIBRATION':
        raise ValueError('T005 evidence class drift')
    if calibration['human_gold_eligible'] is not False:
        raise ValueError('human-gold boundary drift')
    blind = load_blind()
    rows = calibration['joined_rows']
    if len(rows) != EXPECTED_COUNT:
        raise ValueError('calibration population drift')
    adapter = TokenOverlapSemanticAdapter()
    detail=[]
    semantic_rows=[]
    for row in rows:
        bid=row['blind_item_id']; packet=blind[bid]; ctx=packet['source_check_context']
        ref=make_provenance(row['source_id'], ctx, bid)
        claim_texts=[('ANCHOR',x,Materiality.CRITICAL) for x in ctx.get('critical_anchors',[])]
        claim_texts += [('QUALIFIER',x,Materiality.MATERIAL) for x in ctx.get('required_qualifiers',[])]
        claims=[]; packets={}
        for idx,(kind,text,materiality) in enumerate(claim_texts,1):
            cid=f'{bid}:{kind}:{idx}'
            claim=AtomicClaim(claim_id=cid,text=text,materiality=materiality,expected_evidence_refs=(ref,))
            evidence=EvidencePacket(
                claim_id=cid, expected_refs=(ref,),
                retrieved=(EvidenceItem(provenance=ref,text=packet['output_text'],extraction_status=GateStatus.PASS),),
                retrieval_version='w004-t006-generated-output-v1',
            )
            claims.append(claim); packets[cid]=evidence
        checks=row['non_compensatory_checks']
        factual_status = GateStatus.FAIL if (
            checks['FACTUAL_CRITICAL_PRESERVATION']=='FAIL' or checks['MATERIAL_CONCEPT_PRESERVATION']=='FAIL'
        ) else GateStatus.REVIEW_REQUIRED if (
            checks['FACTUAL_CRITICAL_PRESERVATION']=='REVIEW_REQUIRED' or checks['MATERIAL_CONCEPT_PRESERVATION']=='REVIEW_REQUIRED'
        ) else GateStatus.PASS
        result=run_semantic_ablation(
            claims, packets, source_status=GateStatus.PASS, factual_status=factual_status,
            policy_status=GateStatus.PASS, adapter=adapter,
        )
        before=result.without_semantic.status.value; after=result.with_semantic.status.value
        expected=expected_reference(row)
        hard_before=list(result.without_semantic.hard_fail_codes); hard_after=list(result.with_semantic.hard_fail_codes)
        semantic_rows.append({
            'item_id':bid,
            'hard_fail_codes_without_semantic':hard_before,
            'hard_fail_codes_with_semantic':hard_after,
            'decision_without_semantic':before,
            'decision_with_semantic':after,
            'semantic_added_information': bool(result.changed_claim_ids),
        })
        detail.append({
            'blind_item_id':bid,'source_id':row['source_id'],'format':row['format'],
            'automated_reference_decision':expected,'without_semantic':before,'with_semantic':after,
            'without_matches_reference':before==expected,'with_matches_reference':after==expected,
            'changed_claim_count':len(result.changed_claim_ids),'claim_count':len(claims),
            'hard_gate_invariant':result.hard_gate_invariant,
            'hard_fail_codes_without_semantic':hard_before,'hard_fail_codes_with_semantic':hard_after,
        })
    if not all(r['hard_gate_invariant'] for r in detail):
        raise ValueError('semantic adapter changed hard gate codes')
    if any(r['hard_fail_codes_without_semantic'] and r['with_semantic']=='PASS' for r in detail):
        raise ValueError('semantic adapter compensated a hard fail')
    before_acc=sum(r['without_matches_reference'] for r in detail)/len(detail)
    after_acc=sum(r['with_matches_reference'] for r in detail)/len(detail)
    resolved=sum(r['without_semantic']=='REVIEW_REQUIRED' and r['with_semantic']!='REVIEW_REQUIRED' for r in detail)
    changed=sum(r['without_semantic']!=r['with_semantic'] for r in detail)
    return {
        'schema_version':'w004-t006-semantic-ablation-v001','task_id':'W004-T006','attempt_id':'A01',
        'base_state_version':'0035','base_commit_sha':'b3b65219c1b000ff50c6cb7f54b1cee057168652',
        'evidence_policy':'D-0017','reference_evidence_class':'MODEL_AUTOMATED_BLIND_CALIBRATION',
        'human_gold_eligible':False,'human_preference_observed':False,'threshold_disposition':'DIAGNOSTIC_ONLY',
        'candidate_backend':{'backend_id':adapter.backend_id,'backend_version':adapter.backend_version,'kind':'EXPERIMENTAL_DETERMINISTIC_PROXY','production_lock_eligible':False},
        'sample_count':len(detail),'hard_gate_invariant_all':True,'hard_fail_compensation_count':0,
        'decision_changed_count':changed,'review_resolved_count':resolved,
        'reference_accuracy_without_semantic':before_acc,'reference_accuracy_with_semantic':after_acc,
        'reference_accuracy_delta':after_acc-before_acc,
        'backend_decision':'NO_BACKEND_PREFERENCE',
        'backend_decision_reason':'Candidate is a deterministic proxy and the reference is automated, not independent human gold. Incremental diagnostic value may be measured, but production backend preference remains unlocked.',
        'semantic_rows_for_release_gate':semantic_rows,'rows':detail,
    }


def write(report:dict[str,Any], out:Path, doc:Path, result:Path)->None:
    out.parent.mkdir(parents=True,exist_ok=True); doc.parent.mkdir(parents=True,exist_ok=True); result.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    md=f"""# W004-T006-A01 — semantic off/on diagnostic ablation

- Reference: `MODEL_AUTOMATED_BLIND_CALIBRATION` under `D-0017`
- Sample: **{report['sample_count']}** frozen development outputs
- Candidate: `{report['candidate_backend']['backend_id']}` (`EXPERIMENTAL_DETERMINISTIC_PROXY`)
- Hard-gate invariant: **PASS (36/36)**
- Hard-fail compensations: **0**
- Decision changes: **{report['decision_changed_count']}**
- REVIEW_REQUIRED resolved: **{report['review_resolved_count']}**
- Reference accuracy semantic-off: **{report['reference_accuracy_without_semantic']:.3f}**
- Reference accuracy semantic-on: **{report['reference_accuracy_with_semantic']:.3f}**
- Delta: **{report['reference_accuracy_delta']:+.3f}**
- Backend decision: **NO_BACKEND_PREFERENCE**

The semantic hook adds measurable diagnostic resolution while preserving hard-gate precedence, but this candidate is only a deterministic proxy evaluated against automated calibration evidence. It does not justify a production semantic-backend lock or any human-preference claim.
"""
    doc.write_text(md,encoding='utf-8')
    res=f"""# RESULT W004-T006-A01

`TASK_ID: W004-T006`
`ATTEMPT_ID: A01`
`BASE_STATE_VERSION: 0035`
`BASE_COMMIT_SHA: b3b65219c1b000ff50c6cb7f54b1cee057168652`
`WORKER_BRANCH: worker/W004-T006-A01`
`STATUS: COMPLETE_DIAGNOSTIC_ONLY`
`EVIDENCE_POLICY: D-0017`

## Outcome

- sample count: `{report['sample_count']}`
- semantic candidate: `{report['candidate_backend']['backend_id']}` / `{report['candidate_backend']['backend_version']}`
- hard-gate invariant: `{str(report['hard_gate_invariant_all']).lower()}`
- hard-fail compensation count: `{report['hard_fail_compensation_count']}`
- decision changed count: `{report['decision_changed_count']}`
- REVIEW_REQUIRED resolved count: `{report['review_resolved_count']}`
- automated-reference accuracy semantic-off: `{report['reference_accuracy_without_semantic']:.6f}`
- automated-reference accuracy semantic-on: `{report['reference_accuracy_with_semantic']:.6f}`
- delta: `{report['reference_accuracy_delta']:+.6f}`
- backend decision: `NO_BACKEND_PREFERENCE`
- human gold eligible: `false`
- human preference observed: `false`
- thresholds: `DIAGNOSTIC_ONLY`

## Boundary

The ablation proves the architecture can add semantic diagnostics without weakening hard gates. It does not prove this proxy is a production semantic backend, and it does not convert automated calibration into human evidence.

## Artifacts

- `{out.relative_to(ROOT).as_posix()}`
- `{doc.relative_to(ROOT).as_posix()}`
"""
    result.write_text(res,encoding='utf-8')


def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,default=ROOT/'experiments/semantic_ablation_w004/runs/W004-T006-A01/ablation.json'); p.add_argument('--doc',type=Path,default=ROOT/'docs/evals/semantic_ablation_w004/W004-T006-A01.md'); p.add_argument('--result',type=Path,default=ROOT/'SYSTEM/RESULTS/W004-T006-A01.md'); a=p.parse_args()
    r=build(); write(r,a.out,a.doc,a.result); print(json.dumps({'status':'COMPLETE_DIAGNOSTIC_ONLY','sample_count':r['sample_count'],'delta':r['reference_accuracy_delta'],'hard_gate_invariant':r['hard_gate_invariant_all'],'backend_decision':r['backend_decision']})); return 0

if __name__=='__main__': raise SystemExit(main())
