#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import openai
from openai import OpenAI

NA = "N/A"
BASE_URL = "https://api.groq.com/openai/v1"
CANDIDATES = ("openai/gpt-oss-120b", "openai/gpt-oss-20b")

def now(): return datetime.now(timezone.utc).isoformat()
def redact(text: str, secret: str) -> str:
    safe = text.replace(secret, "[REDACTED_GROQ_KEY]") if secret else text
    return re.sub(r"gsk_[A-Za-z0-9._-]+", "[REDACTED_GROQ_KEY]", safe)
def load_snapshot(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def choose(active, snap):
    models=snap.get("models") or {}
    return next((m for m in CANDIDATES if m in active and m in models), None)
def pricing(snap, model):
    m=(snap.get("models") or {}).get(model) or {}
    return {"status":"OBSERVED_SNAPSHOT","kind":snap.get("kind",NA),"source_url":m.get("source_url",NA),"retrieved_at":snap.get("retrieved_at",NA),"effective_at":snap.get("effective_at",NA),"currency":snap.get("currency",NA),"commercial_evidence_eligible":snap.get("kind")=="official_provider_pricing","reason":f"Official Groq pricing snapshot for {model}."}
def derive_cost(snap, model, usage):
    p=((snap.get("models") or {}).get(model) or {}).get("prices_per_million_tokens") or {}
    i,o=usage.get("input_tokens"),usage.get("output_tokens")
    if not all(isinstance(v,(int,float)) for v in (i,o,p.get("input"),p.get("output"))): return {"value":NA,"currency":snap.get("currency",NA),"observed":False,"derived":False}
    return {"value":round((i*p["input"]+o*p["output"])/1_000_000,10),"currency":snap.get("currency","USD"),"observed":False,"derived":True}
def diag_error(exc: Exception, secret: str) -> dict[str, Any]:
    status=getattr(exc,"status_code",NA); request_id=getattr(exc,"request_id",NA)
    response=getattr(exc,"response",None); headers={}
    if response is not None:
        for k in ("content-type","server","cf-ray","x-request-id"):
            try:
                v=response.headers.get(k)
                if v: headers[k]=v
            except Exception: pass
    body=getattr(exc,"body",None)
    body_text=json.dumps(body,ensure_ascii=False) if isinstance(body,(dict,list)) else str(body) if body not in (None,"") else NA
    return {"http_status":status,"type":type(exc).__name__,"message":redact(str(exc),secret)[:1000],"request_id":request_id or NA,"body_snippet":redact(body_text,secret)[:1000],"headers":headers}
def base(attempt, model, snap):
    return {"schema_version":"provider-probe-v1","task_id":"W004-T004","attempt_id":attempt,"captured_at":now(),"evidence_class":"MECHANICS_ONLY","provider":"Groq","provider_protocol":"openai_responses","model":model,"model_version":model,"endpoint":BASE_URL+"/responses","pricing_provenance":pricing(snap,model),"content_quality_evidence":False,"transport":{"client":"openai-python","version":openai.__version__,"base_url":BASE_URL}}
def blocked(attempt,status,preflight,error=None,model=NA,snap=None):
    out=base(attempt,model,snap) if snap and model!=NA else {"schema_version":"provider-probe-v1","task_id":"W004-T004","attempt_id":attempt,"captured_at":now(),"evidence_class":"MECHANICS_ONLY","provider":"Groq","provider_protocol":"openai_responses","model":model,"model_version":model,"endpoint":BASE_URL+"/responses","pricing_provenance":{"status":"UNOBSERVED","kind":NA,"source_url":NA,"retrieved_at":NA,"effective_at":NA,"currency":NA,"commercial_evidence_eligible":False,"reason":"No active model selected."},"content_quality_evidence":False,"transport":{"client":"openai-python","version":openai.__version__,"base_url":BASE_URL}}
    out.update({"status":status,"latency_ms":NA,"usage":{"input_tokens":NA,"output_tokens":NA,"total_tokens":NA,"observed":False},"cost":{"value":NA,"currency":"USD" if snap else NA,"observed":False,"derived":False},"response":{"sha256":NA,"bytes":NA,"provider_model":NA},"preflight":preflight})
    if error: out["error"]=error
    return out

def execute(attempt, env, prompt_file, pricing_file, timeout):
    secret=os.getenv(env,"").strip()
    if not secret: return blocked(attempt,"BLOCKED_NO_CREDENTIAL",{"status":"NOT_RUN"})
    if not secret.startswith("gsk_"): return blocked(attempt,"BLOCKED_PROVIDER_CLASSIFICATION",{"status":"NOT_RUN"},{"http_status":NA,"type":"credential_classification","message":"Not a Groq gsk_ credential."})
    snap=load_snapshot(pricing_file)
    client=OpenAI(api_key=secret,base_url=BASE_URL,timeout=timeout,max_retries=0)
    start=time.perf_counter()
    try:
        models=client.models.list(); pre_ms=round((time.perf_counter()-start)*1000,3)
        ids=sorted({m.id for m in models.data if getattr(m,"id",None)})
        pf={"http_status":200,"latency_ms":pre_ms,"active_model_count":len(ids),"selected_model":NA,"transport_client":"openai-python","transport_version":openai.__version__}
    except Exception as exc:
        pre_ms=round((time.perf_counter()-start)*1000,3); err=diag_error(exc,secret)
        pf={"http_status":err.get("http_status",NA),"latency_ms":pre_ms,"active_model_count":0,"selected_model":NA,"transport_client":"openai-python","transport_version":openai.__version__,"error":err}
        return blocked(attempt,"PREFLIGHT_ERROR",pf,err)
    selected=choose(ids,snap); pf["selected_model"]=selected or NA; pf["candidate_availability"]={m:m in ids for m in CANDIDATES}
    if not selected: return blocked(attempt,"BLOCKED_MODEL_NOT_ACTIVE",pf,{"http_status":200,"type":"model_availability","message":"No priced GPT-OSS candidate active."})
    prompt=Path(prompt_file).read_text(encoding="utf-8")
    start=time.perf_counter()
    try:
        response=client.responses.create(model=selected,input=prompt,max_output_tokens=128); latency=round((time.perf_counter()-start)*1000,3)
    except Exception as exc:
        latency=round((time.perf_counter()-start)*1000,3); err=diag_error(exc,secret); out=blocked(attempt,"TRANSPORT_ERROR",pf,err,selected,snap); out["latency_ms"]=latency; out["http_status"]=err.get("http_status",NA); return out
    usage_obj=getattr(response,"usage",None); i=getattr(usage_obj,"input_tokens",NA); o=getattr(usage_obj,"output_tokens",NA); t=getattr(usage_obj,"total_tokens",NA)
    usage={"input_tokens":i,"output_tokens":o,"total_tokens":t,"observed":all(isinstance(v,int) for v in (i,o,t))}
    raw=response.model_dump_json().encode("utf-8")
    return {**base(attempt,selected,snap),"status":"OBSERVED_RUN","http_status":200,"latency_ms":latency,"usage":usage,"cost":derive_cost(snap,selected,usage),"response":{"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"provider_model":getattr(response,"model",NA)},"preflight":pf}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--attempt-id",required=True); p.add_argument("--secret-env",default="PROVIDER_API_KEY"); p.add_argument("--prompt-file",required=True); p.add_argument("--pricing-snapshot",required=True); p.add_argument("--timeout",type=float,default=60); p.add_argument("--output",required=True); a=p.parse_args()
    r=execute(a.attempt_id,a.secret_env,a.prompt_file,a.pricing_snapshot,a.timeout); Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"attempt_id":r.get("attempt_id"),"status":r.get("status"),"transport":r.get("transport"),"preflight_http_status":(r.get("preflight") or {}).get("http_status",NA),"model":r.get("model"),"provider_http_status":r.get("http_status",(r.get("error") or {}).get("http_status",NA))},ensure_ascii=False))
    return 0 if r.get("status")=="OBSERVED_RUN" else 3
if __name__=="__main__": raise SystemExit(main())
