#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NA = "N/A"
MODELS_ENDPOINT = "https://api.groq.com/openai/v1/models"
RESPONSES_ENDPOINT = "https://api.groq.com/openai/v1/responses"
CANDIDATES = ("openai/gpt-oss-120b", "openai/gpt-oss-20b")

def now(): return datetime.now(timezone.utc).isoformat()
def redact(text, secret):
    safe = text.replace(secret, "[REDACTED_GROQ_KEY]") if secret else text
    return re.sub(r"gsk_[A-Za-z0-9._-]+", "[REDACTED_GROQ_KEY]", safe)

def safe_headers(headers):
    keep = ("content-type", "server", "x-request-id", "cf-ray", "via", "x-groq-region")
    return {k: headers.get(k) for k in keep if headers.get(k)}

def parse_http_error(exc, secret):
    raw = b""
    try: raw = exc.read(65536)
    except Exception: pass
    decoded = redact(raw.decode("utf-8", errors="replace"), secret)
    msg, typ, code = str(exc), NA, NA
    body_kind = "empty"
    if raw:
        body_kind = "text"
        try:
            payload = json.loads(decoded)
            body_kind = "json"
            err = payload.get("error") if isinstance(payload, dict) else None
            if isinstance(err, dict):
                msg = str(err.get("message", msg)); typ = str(err.get("type", NA)); code = str(err.get("code", NA))
        except Exception:
            pass
    snippet = re.sub(r"\s+", " ", decoded).strip()[:1000] if decoded else NA
    return {"http_status": int(exc.code), "type": redact(typ, secret), "code": redact(code, secret), "message": redact(msg, secret)[:1000], "body_kind": body_kind, "body_snippet": snippet, "headers": safe_headers(exc.headers)}

def request_json(req, secret, timeout):
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(); elapsed = round((time.perf_counter()-start)*1000, 3)
            return int(r.status), raw, json.loads(raw.decode()), None, elapsed, safe_headers(r.headers)
    except urllib.error.HTTPError as exc:
        elapsed = round((time.perf_counter()-start)*1000, 3)
        return int(exc.code), b"", None, parse_http_error(exc, secret), elapsed, safe_headers(exc.headers)
    except (urllib.error.URLError, TimeoutError) as exc:
        elapsed = round((time.perf_counter()-start)*1000, 3)
        err = {"http_status": NA, "type": type(exc).__name__, "code": NA, "message": redact(str(exc), secret)[:1000], "body_kind": "none", "body_snippet": NA, "headers": {}}
        return None, b"", None, err, elapsed, {}

def load_snapshot(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def choose(active, snap):
    models = snap.get("models") or {}
    return next((m for m in CANDIDATES if m in active and m in models), None)
def pricing(snap, model):
    m=(snap.get("models") or {}).get(model) or {}
    return {"status":"OBSERVED_SNAPSHOT","kind":snap.get("kind",NA),"source_url":m.get("source_url",NA),"retrieved_at":snap.get("retrieved_at",NA),"effective_at":snap.get("effective_at",NA),"currency":snap.get("currency",NA),"commercial_evidence_eligible":snap.get("kind")=="official_provider_pricing","reason":f"Official Groq pricing snapshot for {model}."}
def cost(snap, model, usage):
    p=((snap.get("models") or {}).get(model) or {}).get("prices_per_million_tokens") or {}
    i,o=usage.get("input_tokens"),usage.get("output_tokens")
    if not all(isinstance(v,(int,float)) for v in (i,o,p.get("input"),p.get("output"))): return {"value":NA,"currency":snap.get("currency",NA),"observed":False,"derived":False}
    return {"value":round((i*p["input"]+o*p["output"])/1_000_000,10),"currency":snap.get("currency","USD"),"observed":False,"derived":True}
def base(attempt, model, snap):
    return {"schema_version":"provider-probe-v1","task_id":"W004-T004","attempt_id":attempt,"captured_at":now(),"evidence_class":"MECHANICS_ONLY","provider":"Groq","provider_protocol":"openai_responses","model":model,"model_version":model,"endpoint":RESPONSES_ENDPOINT,"pricing_provenance":pricing(snap,model),"content_quality_evidence":False}
def blocked(attempt,status,preflight,error=None,model=NA,snap=None):
    out = base(attempt,model,snap) if snap and model!=NA else {"schema_version":"provider-probe-v1","task_id":"W004-T004","attempt_id":attempt,"captured_at":now(),"evidence_class":"MECHANICS_ONLY","provider":"Groq","provider_protocol":"openai_responses","model":model,"model_version":model,"endpoint":RESPONSES_ENDPOINT,"pricing_provenance":{"status":"UNOBSERVED","kind":NA,"source_url":NA,"retrieved_at":NA,"effective_at":NA,"currency":NA,"commercial_evidence_eligible":False,"reason":"No active model selected."},"content_quality_evidence":False}
    out.update({"status":status,"latency_ms":NA,"usage":{"input_tokens":NA,"output_tokens":NA,"total_tokens":NA,"observed":False},"cost":{"value":NA,"currency":"USD" if snap else NA,"observed":False,"derived":False},"response":{"sha256":NA,"bytes":NA,"provider_model":NA},"preflight":preflight})
    if error: out["error"]=error
    return out

def execute(attempt, env, prompt_file, pricing_file, timeout):
    secret=os.getenv(env,"").strip()
    if not secret: return blocked(attempt,"BLOCKED_NO_CREDENTIAL",{"status":"NOT_RUN","endpoint":MODELS_ENDPOINT})
    if not secret.startswith("gsk_"): return blocked(attempt,"BLOCKED_PROVIDER_CLASSIFICATION",{"status":"NOT_RUN","endpoint":MODELS_ENDPOINT},{"http_status":NA,"type":"credential_classification","code":"not_groq_gsk","message":"Not a Groq gsk_ credential."})
    snap=load_snapshot(pricing_file)
    headers={"Authorization":f"Bearer {secret}","Content-Type":"application/json"}
    s,raw,payload,err,ms,rh=request_json(urllib.request.Request(MODELS_ENDPOINT,headers=headers,method="GET"),secret,timeout)
    pf={"endpoint":MODELS_ENDPOINT,"http_status":s if s is not None else NA,"latency_ms":ms,"response_sha256":hashlib.sha256(raw).hexdigest() if raw else NA,"response_bytes":len(raw) if raw else NA,"response_headers":rh,"active_model_count":0,"selected_model":NA}
    if err: pf["error"]=err
    if s!=200 or not isinstance(payload,dict): return blocked(attempt,"PREFLIGHT_ERROR",pf,err)
    ids=sorted({str(x.get("id")) for x in (payload.get("data") or []) if isinstance(x,dict) and x.get("id")})
    pf["active_model_count"]=len(ids); selected=choose(ids,snap); pf["selected_model"]=selected or NA; pf["candidate_availability"]={m:m in ids for m in CANDIDATES}
    if not selected: return blocked(attempt,"BLOCKED_MODEL_NOT_ACTIVE",pf,{"http_status":200,"type":"model_availability","code":"no_priced_candidate_active","message":"No A07 priced GPT-OSS candidate is active."})
    prompt=Path(prompt_file).read_text(encoding="utf-8")
    body=json.dumps({"model":selected,"input":prompt,"max_output_tokens":128}).encode()
    s2,raw2,p2,err2,ms2,rh2=request_json(urllib.request.Request(RESPONSES_ENDPOINT,data=body,headers=headers,method="POST"),secret,timeout)
    if s2!=200 or not isinstance(p2,dict):
        out=blocked(attempt,"TRANSPORT_ERROR",pf,err2,selected,snap); out["latency_ms"]=ms2; out["http_status"]=s2 if s2 is not None else NA; out["response_headers"]=rh2; return out
    u=p2.get("usage") or {}; i=u.get("input_tokens",NA); o=u.get("output_tokens",NA); t=u.get("total_tokens",NA); usage={"input_tokens":i,"output_tokens":o,"total_tokens":t,"observed":all(isinstance(v,int) for v in (i,o,t))}
    return {**base(attempt,selected,snap),"status":"OBSERVED_RUN","http_status":s2,"latency_ms":ms2,"usage":usage,"cost":cost(snap,selected,usage),"response":{"sha256":hashlib.sha256(raw2).hexdigest(),"bytes":len(raw2),"provider_model":p2.get("model",NA)},"preflight":pf,"response_headers":rh2}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--attempt-id",required=True); p.add_argument("--secret-env",default="PROVIDER_API_KEY"); p.add_argument("--prompt-file",required=True); p.add_argument("--pricing-snapshot",required=True); p.add_argument("--timeout",type=float,default=60); p.add_argument("--output",required=True); a=p.parse_args()
    r=execute(a.attempt_id,a.secret_env,a.prompt_file,a.pricing_snapshot,a.timeout); Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"attempt_id":r.get("attempt_id"),"status":r.get("status"),"preflight_http_status":(r.get("preflight") or {}).get("http_status",NA),"error_body_kind":((r.get("preflight") or {}).get("error") or {}).get("body_kind",NA),"error_server":(((r.get("preflight") or {}).get("error") or {}).get("headers") or {}).get("server",NA)},ensure_ascii=False))
    return 0 if r.get("status")=="OBSERVED_RUN" else 3
if __name__=="__main__": raise SystemExit(main())
