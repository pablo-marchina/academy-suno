#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, html, io, json, re, shutil, subprocess, tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[2]
FIXTURES=ROOT/"data/fixtures/parser_bakeoff"
OBS=ROOT/"experiments/parser_bakeoff/observed_candidates.json"

def load():
    return {x["fixture_id"]:x for p in sorted(FIXTURES.glob("*.json"))
            for x in [json.loads(p.read_text(encoding="utf-8"))]}

def norm(v):
    s=str(v).strip().replace("\u2212","-")
    return re.sub(r"[.\s]","",s) if re.fullmatch(r"\d{1,3}(?:[.\s]\d{3})+",s) else s

def score(f,c):
    aexp={a["id"]:a for a in f["manual_checks"]["critical_anchors"]}
    aobs=c.get("anchor_observations",{}); aerr=[]; matched=0
    for aid,e in aexp.items():
        g=aobs.get(aid)
        if not g: aerr.append({"id":aid,"error":"missing"}); continue
        ok=(norm(g.get("value"))==norm(e.get("value")) and
            g.get("unit")==e.get("unit") and g.get("role")==e.get("role"))
        if ok: matched+=1
        else: aerr.append({"id":aid,"error":"mismatch","expected":{k:e.get(k) for k in ("value","unit","role")},
                           "observed":{k:g.get(k) for k in ("value","unit","role")}})
    texp={b["id"]:b for b in f["manual_checks"]["required_table_bindings"]}
    tobs=c.get("table_bindings",{}); terr=[]
    for bid,e in texp.items():
        if tobs.get(bid)!=e: terr.append({"id":bid,"error":"table_role_mismatch","expected":e,"observed":tobs.get(bid)})
    qexp={q["id"] for q in f["manual_checks"]["required_qualifiers"]}
    qmiss=sorted(qexp-set(c.get("qualifiers_present",[])))
    values_present=all(aid in aobs and norm(aobs[aid].get("value"))==norm(e["value"]) for aid,e in aexp.items())
    silent=values_present and bool(aerr or terr)
    decision="FAIL" if aerr else ("REVIEW_REQUIRED" if terr or qmiss else "PASS")
    return {"fixture_id":f["fixture_id"],"decision":decision,
            "critical_anchor_coverage":round(matched/len(aexp),4) if aexp else 1.0,
            "anchor_errors":aerr,"table_role_errors":terr,"missing_qualifiers":qmiss,
            "silent_corruption":silent,"warnings":c.get("warnings",[])}

def observed():
    fs=load(); raw=json.loads(OBS.read_text(encoding="utf-8")); out={"mode":"observed_behavior","candidates":{}}
    for name,byf in raw["candidates"].items():
        rows=[]
        for fid,f in fs.items():
            spec=byf[fid]; anchors={}
            for a in f["manual_checks"]["critical_anchors"]:
                if a["id"] in spec.get("anchors_present",[]):
                    anchors[a["id"]]={"value":a["value"],"unit":a.get("unit"),
                                      "role":spec.get("role_overrides",{}).get(a["id"],a["role"])}
            tables={}
            for b in f["manual_checks"]["required_table_bindings"]:
                if b["id"] in spec.get("table_bindings_present",[]):
                    item=dict(b)
                    if b["id"] in spec.get("table_row_overrides",{}): item["row"]=spec["table_row_overrides"][b["id"]]
                    tables[b["id"]]=item
            warnings=[]
            if name=="flat_text_baseline" and f["manual_checks"]["required_table_bindings"]:
                warnings=["flat_text_preserves_tokens_but_drops_table_role_structure"]
            if name=="wrong_role_corruption" and spec.get("role_overrides"):
                warnings=["adversarial role swap: all critical numeric tokens remain present"]
            rows.append(score(f,{"anchor_observations":anchors,"table_bindings":tables,
                                 "qualifiers_present":spec.get("qualifiers_present",[]),"warnings":warnings}))
        out["candidates"][name]=rows
    return out

class Visible(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.skip=0; self.parts=[]
    def handle_starttag(self,t,a):
        if t.lower() in {"script","style","noscript","svg"}: self.skip+=1
    def handle_endtag(self,t):
        if t.lower() in {"script","style","noscript","svg"} and self.skip: self.skip-=1
        if t.lower() in {"p","div","li","tr","h1","h2","h3","br"}: self.parts.append("\n")
    def handle_data(self,d):
        if not self.skip: self.parts.append(d)
    def text(self):
        s=html.unescape(" ".join(self.parts)); s=re.sub(r"[ \t]+"," ",s); return re.sub(r"\n\s*\n+","\n",s).strip()

def html_stdlib(raw):
    p=Visible(); p.feed(raw.decode("utf-8",errors="replace")); return p.text()
def html_regex(raw):
    s=raw.decode("utf-8",errors="replace"); s=re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>"," ",s)
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"(?s)<[^>]+>"," ",s))).strip()
def pypdf(raw):
    from pypdf import PdfReader
    return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages)
def pdftotext(raw):
    if not shutil.which("pdftotext"): raise RuntimeError("pdftotext not installed")
    with tempfile.TemporaryDirectory() as td:
        src=Path(td)/"s.pdf"; dst=Path(td)/"o.txt"; src.write_bytes(raw)
        subprocess.run(["pdftotext","-layout",str(src),str(dst)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return dst.read_text(encoding="utf-8",errors="replace")
def fetch(url):
    with urlopen(Request(url,headers={"User-Agent":"academy-suno-parser-bakeoff/1.0"}),timeout=30) as r: return r.read()

def live_obs(f,name,text):
    low=text.lower().replace("\xa0"," "); anchors={}
    for a in f["manual_checks"]["critical_anchors"]:
        raw=str(a["value"]); alts={raw,raw.replace(".",","),raw.replace(",",".")}
        if raw.isdigit() and len(raw)>3: alts|={f"{int(raw):,}".replace(",","."),f"{int(raw):,}".replace(","," ")}
        if any(x.lower() in low for x in alts):
            anchors[a["id"]]={"value":a["value"],"unit":a.get("unit"),
                              "role":a["role"] if not f["manual_checks"]["required_table_bindings"] else None}
    q=[]
    for x in f["manual_checks"]["required_qualifiers"]:
        i=x["id"]
        if i=="forward_looking_not_guarantee" and ("garantias" in low or "promessas" in low): q.append(i)
        elif i=="subject_to_risks" and "riscos" in low and "incertezas" in low: q.append(i)
        elif i=="calibration_preserves_restrictive_stance" and "restrictive stance" in low: q.append(i)
        elif i=="non_ifrs_metrics_disclaimer" and "ifrs" in low and "isolad" in low: q.append(i)
    return {"anchor_observations":anchors,"table_bindings":{},"qualifiers_present":q,
            "warnings":[f"live parser {name} is flat text; table roles require a layout/table adapter"]
                       if f["manual_checks"]["required_table_bindings"] else []}

def live():
    out={"mode":"live","fixtures":{}}
    for fid,f in load().items():
        raw=fetch(f["source"]["canonical_url"]); parsers={}
        cand={"html_stdlib_visible_text":html_stdlib,"html_regex_strip":html_regex} if f["source"]["content_type"]=="text/html" else {"pdf_pypdf":pypdf,"pdf_pdftotext_layout":pdftotext}
        for name,fn in cand.items():
            try:
                text=fn(raw); parsers[name]={"score":score(f,live_obs(f,name,text)),
                    "text_sha256":hashlib.sha256(text.encode()).hexdigest(),"chars":len(text)}
            except Exception as e: parsers[name]={"error":f"{type(e).__name__}: {e}"}
        out["fixtures"][fid]={"url":f["source"]["canonical_url"],"raw_source_sha256":hashlib.sha256(raw).hexdigest(),
                              "bytes":len(raw),"parsers":parsers}
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--live",action="store_true"); ap.add_argument("--output",type=Path)
    a=ap.parse_args(); result=live() if a.live else observed(); payload=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(payload,encoding="utf-8")
    else: print(payload,end="")
if __name__=="__main__": main()
