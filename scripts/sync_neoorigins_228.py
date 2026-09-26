#!/usr/bin/env python3
"""Prepare and translate NeoOrigins 2.2.28 fallback deltas, per pinned Git refs."""
from __future__ import annotations
import argparse, collections, concurrent.futures, json, re, threading, time
import urllib.error, urllib.parse, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
CACHE=ROOT/"build/neoorigins-228"
CACHE.mkdir(parents=True,exist_ok=True)
REVS={"121":("af467a3bc118f6bbc0970d68f7e03fa631d7e6f2","87860513d5947fa0407a4dd1868126c9489e56cd"),
      "261":("aa207ef14cf3b938e28b4081162701953957c1d5","4f11c58362a7b3c76d5475ed072b79f49ceb537d"),
      "262":("511cadcafe3027d2a56b4448652ec9b74e2f3b07","d2d7c0b6d5439e11e3ed3e981dcdd25642f0b417")}
EXPECTED={"121":236,"261":229,"262":228}
BASE="https://raw.githubusercontent.com/CyberDay1/NeoOrigins/{}/src/main/resources/assets/neoorigins/lang/{}.json"
TOKEN=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n|\{[^{}]+\}|<[^<>]+>")
PH=re.compile(r"%(?:\d+\$)?[sdif]")
SEP=re.compile(r"\s*ZZQSEP\d{4}ZZQ\s*")
LANGS={"fil_ph":"tl","he_il":"iw","zh_cn":"zh-CN","zh_tw":"zh-TW","no_no":"no","nn_no":"no",
       "sr_sp":"sr","sr_cs":"sr","se_no":"se","fra_de":"de","bar":"de","brb":"nl",
       "esan":"es","go_fr":"fr","ksh":"de","nds_de":"nds","fur_it":"fur","isv":"isv",
       "kab_kab":"kab","haw_us":"haw","io_en":"io","li_li":"li","gv_im":"gv",
       "ast_es":"ast","cv_cu":"cv","ba_ru":"ba","fo_fo":"fo","mt_mt":"mt"}
PROXY={"se_no":"no","bar":"de","brb":"nl","esan":"es","fra_de":"de","go_fr":"fr",
       "ksh":"de","fur_it":"it","isv":"ru","li_li":"nl","nds_de":"de","gv_im":"ga",
       "ast_es":"es","cv_cu":"ru","ba_ru":"ru","fo_fo":"da","io_en":"eo",
       "kab_kab":"fr","haw_us":"en"}
FR_FIX={"Activation time (ticks)":"Temps d'activation (ticks)",
        "Cooldown (ticks)":"Temps de recharge (ticks)",
        "Despawn time (ticks)":"Délai de disparition (ticks)",
        "Duration (ticks)":"Durée (ticks)",
        "Recovery time (ticks)":"Temps de récupération (ticks)"}
def readj(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def writej(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+".tmp")
    tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for attempt in range(12):
        try:
            tmp.replace(p)
            break
        except PermissionError:
            if attempt==11: raise
            time.sleep(0.25)
def get(url,missing=False):
    last=None
    for i in range(4):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"NeoOrigins-Localization-2.2.28"})
            with urllib.request.urlopen(req,timeout=35) as res: return json.load(res)
        except urllib.error.HTTPError as e:
            if missing and e.code==404: return {}
            last=e
            if e.code not in (408,429,500,502,503,504): break
        except Exception as e: last=e
        time.sleep(min(8,2**i))
    raise RuntimeError(f"Fetch {url}: {last}")
def upstream(ref,locale="en_us"):
    p=CACHE/f"{ref}_{locale}.json"
    if not p.exists():writej(p,get(BASE.format(ref,locale),missing=locale!="en_us"))
    return readj(p)
def prepare():
    old={v:upstream(a) for v,(a,b) in REVS.items()}
    new={v:upstream(b) for v,(a,b) in REVS.items()}
    added={v:{k:s for k,s in new[v].items() if k not in old[v]} for v in REVS}
    changed={v:{k:s for k,s in new[v].items() if k in old[v] and s!=old[v][k]} for v in REVS}
    for v in REVS:
        assert len(added[v])==EXPECTED[v],(v,len(added[v]))
        assert len(changed[v])==2,(v,changed[v])
        assert not (old[v].keys()-new[v].keys()),v
    common={k:s for k,s in added["121"].items() if all(added[v].get(k)==s for v in ("261","262"))}
    assert len(common)==228,len(common)
    assert changed["121"]==changed["261"]==changed["262"]
    splits={"common":dict(sorted({**common,**changed["121"]}.items()))}
    splits.update({v:dict(sorted({k:s for k,s in data.items() if k not in common}.items())) for v,data in added.items()})
    writej(CACHE/"source_splits.json",splits)
    writej(CACHE/"pinned_refs.json",{"old":{v:a for v,(a,b) in REVS.items()},
        "new":{v:b for v,(a,b) in REVS.items()},"old_count":{v:len(x) for v,x in old.items()},
        "new_count":{v:len(x) for v,x in new.items()},"new_keys":{v:len(x) for v,x in added.items()},
        "changed_keys":list(changed["121"])})
    print("Prepared:",{k:len(v) for k,v in splits.items()},flush=True)
    return old,splits
def corpus(locale,old):
    votes=collections.defaultdict(collections.Counter)
    for path in ASSETS.glob(f"neoorigins*/lang/{locale}.json"):
        if "228_" in path.parts[-3]:continue
        obj=readj(path)
        for key,target in obj.items():
            for en in old.values():
                src=en.get(key)
                if src is not None and target.strip() and target!=src and sorted(PH.findall(src))==sorted(PH.findall(target)):
                    votes[src][target]+=1
    if locale in ("fr_fr","de_de","es_es","pt_br","nl_nl","it_it","pl_pl","ru_ru","ja_jp","ko_kr","uk_ua","zh_cn"):
        for v,(ref,_) in REVS.items():
            official=upstream(ref,locale)
            for key,target in official.items():
                src=old[v].get(key)
                if src and target and src!=target and sorted(PH.findall(src))==sorted(PH.findall(target)):
                    votes[src][target]+=3
    return {src:count.most_common(1)[0][0] for src,count in votes.items()}
def google(text,target,attempts=3):
    if target=="en":return text
    p=urllib.parse.urlencode({"client":"gtx","sl":"en","tl":target,"dt":"t","q":text})
    url="https://translate.googleapis.com/translate_a/single?"+p
    last=None
    for i in range(attempts):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=40) as r:
                o=json.load(r)
            result="".join(x[0] for x in o[0] if x and isinstance(x[0],str))
            if result.strip():return result
            last="empty translation"
        except Exception as e:last=e
        time.sleep(1.5*(i+1))
    # Official Google Translate web UI transport used by the project's earlier bootstrap scripts.
    # Its endpoint is separate from the public gtx transport and provides a conservative 429 fallback.
    inner=json.dumps([[text,"en",target,True],[None]],ensure_ascii=False)
    data=urllib.parse.urlencode({"f.req":json.dumps([[["MkEWBc",inner,None,"generic"]]],ensure_ascii=False)}).encode("utf-8")
    request=urllib.request.Request("https://translate.google.com/_/TranslateWebserverUi/data/batchexecute",
        data=data,headers={"User-Agent":"Mozilla/5.0","Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request,timeout=50) as response:
                payload=response.read().decode("utf-8")
            outer=json.loads(payload.split(chr(10),2)[2])
            parsed=json.loads(outer[0][2])
            result="".join(part[0] for part in parsed[1][0][0][5])
            if result.strip():return result
        except Exception as exc:
            last=exc
            time.sleep((attempt+1)*2)
    raise RuntimeError(f"{target}: {last}")
legacy_google=google
def google(text,target,attempts=2):
    if target=="en":return text
    inner=json.dumps([[text,"en",target,True],[None]],ensure_ascii=False)
    data=urllib.parse.urlencode({"f.req":json.dumps([[["MkEWBc",inner,None,"generic"]]],ensure_ascii=False)}).encode("utf-8")
    request=urllib.request.Request("https://translate.google.com/_/TranslateWebserverUi/data/batchexecute",
        data=data,headers={"User-Agent":"Mozilla/5.0","Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"})
    try:
        with urllib.request.urlopen(request,timeout=25) as response:
            payload=response.read().decode("utf-8")
        outer=json.loads(payload.split(chr(10),2)[2]);parsed=json.loads(outer[0][2])
        result="".join(part[0] for part in parsed[1][0][0][5])
        if result.strip():return result
    except Exception:
        pass
    return legacy_google(text,target,attempts=1)
def mask(src):
    tokens=[]
    def repl(m):
        tokens.append(m.group(0));return f"ZXQPH{len(tokens)-1:04d}ZXQ"
    return TOKEN.sub(repl,src),tokens
def unmask(result,tokens):
    for i,t in enumerate(tokens):
        result=re.sub(r"ZXQPH\s*"+str(i).zfill(4)+r"\s*ZXQ",lambda m,v=t:v,result,flags=re.I)
    return result.strip()
def machine_batch(sources,target):
    masked=[mask(s) for s in sources]
    joined="\n".join(v if i==0 else f"ZZQSEP{i:04d}ZZQ\n{v}" for i,(v,_) in enumerate(masked))
    answer=google(joined,target)
    parts=SEP.split(answer)
    if len(parts)!=len(sources):
        parts=[google(v,target) for v,t in masked]
    out=[]
    for src,part,(v,tokens) in zip(sources,parts,masked):
        res=unmask(part,tokens)
        if not res or sorted(PH.findall(src))!=sorted(PH.findall(res)):
            raise ValueError(f"Failed placeholder/empty {target}: {src!r} => {res!r}")
        out.append(res)
    return out
def chunks(values,n=20,limit=1700):
    result=[];cur=[];size=0
    for x in values:
        if cur and (len(cur)>=n or size+len(x)>limit):
            result.append(cur);cur=[];size=0
        cur.append(x);size+=len(x)
    if cur:result.append(cur)
    return result
def one(locale,old,splits):
    cp=CACHE/"translated"/f"{locale}.json"
    pre=readj(cp) if cp.exists() else {}
    lang=LANGS.get(locale,locale.split("_")[0])
    known=corpus(locale,old)
    vals=dict.fromkeys(v for section in splits.values() for v in section.values())
    for src in vals:
        if src not in pre and src in known:pre[src]=known[src]
    if locale=="fr_fr":pre.update(FR_FIX)
    if locale in ("sr_sp","sr_cs"):pre["Claimed by %s"]="Preuzeto od %s"
    pending=[s for s in vals if s not in pre]
    mode="direct"
    batches=chunks(pending)
    try:
        if batches: machine_batch(batches[0],lang)
    except Exception:
        if locale in PROXY and PROXY[locale]!=lang:
            mode="proxy:"+PROXY[locale];lang=PROXY[locale]
        else: mode="retry:"+lang
    for i,batch in enumerate(batches):
        try: answers=machine_batch(batch,lang)
        except Exception as e:
            try:answers=[google(mask(s)[0],lang) for s in batch];answers=[unmask(t,mask(s)[1]) for s,t in zip(batch,answers)]
            except Exception as e2:
                print(f"FAILED {locale} batch {i+1}/{len(batches)}: {e2}",flush=True)
                writej(cp,pre)
                return {"locale":locale,"status":"failed","reason":str(e2),"done":len(pre),"target":lang}
        for s,t in zip(batch,answers):
            if not t or sorted(PH.findall(s))!=sorted(PH.findall(t)):
                print(f"FAILED {locale} placeholders {s!r}=>{t!r}",flush=True)
                writej(cp,pre);return {"locale":locale,"status":"failed","reason":"placeholder","done":len(pre)}
            pre[s]=t
        writej(cp,pre)
    assert all(v in pre for v in vals)
    folders={"common":"neoorigins_228_common","121":"neoorigins_228_121",
             "261":"neoorigins_228_26_1","262":"neoorigins_228_26_2"}
    for version,source in splits.items():
        if source:
            dest=ASSETS/folders[version]/"lang"/f"{locale}.json"
            payload={k:pre[v] for k,v in source.items()}
            if dest.exists() and readj(dest)==payload:continue
            writej(dest,payload)
    return {"locale":locale,"status":"ok","mode":mode,"baseline_reuse":len(vals)-len(pending),
            "machine":len(pending),"total":len(vals)}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--locale",action="append");p.add_argument("--workers",type=int,default=4)
    a=p.parse_args();old,splits=prepare()
    catalog=readj(ROOT/"catalog.json")
    locales=a.locale or list(next(p for p in catalog["supported_projects"] if p["id"]=="neoorigins")["languages"])
    reports=[r for r in (readj(CACHE/"translation_report.json") if (CACHE/"translation_report.json").exists() else [])
             if r["locale"] not in set(locales)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        futures={pool.submit(one,loc,old,splits):loc for loc in locales}
        for f in concurrent.futures.as_completed(futures):
            try:r=f.result()
            except Exception as e:r={"locale":futures[f],"status":"failed","reason":str(e)}
            reports.append(r);writej(CACHE/"translation_report.json",sorted(reports,key=lambda x:x["locale"]))
            print("LOCALE",json.dumps(r,ensure_ascii=False),flush=True)
    if any(x["status"]!="ok" for x in reports):raise SystemExit("Some locales are incomplete")
    print(f"ALL {len(reports)} locales translated.",flush=True)
if __name__=="__main__":main()
