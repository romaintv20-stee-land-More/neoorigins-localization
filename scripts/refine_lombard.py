#!/usr/bin/env python3
"""Refine Lombard (`lmo`) fallbacks with direct English -> Lombard OPUS MT."""
from __future__ import annotations
from pathlib import Path
import json, re
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import bootstrap_lombard as base

ROOT=base.ROOT; ASSETS=base.ASSETS
MODEL_ID="Helsinki-NLP/opus-mt-en-roa"; TARGET_TOKEN=">>lmo<<"
PROTECT_RE=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b",re.IGNORECASE)
SUSPICIOUS_RE=re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]",re.MULTILINE)
TECHNICAL_CASEFOLD={"neoorigins","origin architect","hud","json","xp","hp","neoforge","minecraft","curseforge"}

def read_json(path:Path): return json.loads(path.read_text(encoding="utf-8"))
def write_json(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def protected_signature(text:str):
    return [token.casefold() if token.casefold() in TECHNICAL_CASEFOLD else token for token in PROTECT_RE.findall(text)]
def sanitize(source:str,value:str):
    if not base.placeholder_signature(source): value=base.PLACEHOLDER_RE.sub("",value)
    if "§" not in source: value=value.replace("§","")
    return re.sub(r"[ \t]{2,}"," ",value).strip()

def build_sources():
    n121=read_json(ROOT/"build/lmo-discovery-mc-1.21.1/lmo_missing_en.json"); n261=read_json(ROOT/"build/lmo-discovery-mc-26.1/lmo_missing_en.json"); n262=read_json(ROOT/"build/lmo-discovery-mc-26.2/lmo_missing_en.json")
    common={k:v for k,v in n121.items() if n261.get(k)==v and n262.get(k)==v}; d121={k:v for k,v in n121.items() if k not in common}; d261={k:v for k,v in n261.items() if k not in common}; d262={k:v for k,v in n262.items() if k not in common}
    folders={"medievalorigins":"medievalorigins-upstream-audit","ibarnorigins":"ibarnorigins-upstream-audit","origins_fantasy":"origins-fantasy-upstream-audit","origins_backgrounds":"origins-backgrounds-upstream-audit","origins_backgrounds_two":"origins-more-backgrounds-upstream-audit","origins_backgrounds_iss":"origins-backgrounds-iss-upstream-audit","origins_furries":"origins-furries-upstream-audit","origins_classes_ex":"origins-classes-extended-upstream-audit","origins_classes_iss":"origins-classes-iss-upstream-audit","originsmodernui":"origin-architect-upstream-audit"}
    addons={ns:read_json(ROOT/f"build/{folder}/upstream_en_us.json") for ns,folder in folders.items()}; shared=set(addons["origins_backgrounds"]); addons["origins_backgrounds_two"]={k:v for k,v in addons["origins_backgrounds_two"].items() if k not in shared}; addons["origins_backgrounds_iss"]={k:v for k,v in addons["origins_backgrounds_iss"].items() if k not in shared}
    return common,d121,d261,d262,addons

class Translator:
    def __init__(self):
        print(f"Loading direct Lombard OPUS model: {MODEL_ID} target={TARGET_TOKEN}",flush=True); self.tok=AutoTokenizer.from_pretrained(MODEL_ID); self.model=AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID); self.model.eval()
    def batch(self,texts:list[str]):
        if not texts:return []
        enc=self.tok([f"{TARGET_TOKEN} {text}" for text in texts],return_tensors="pt",padding=True,truncation=True,max_length=512)
        with torch.inference_mode(): gen=self.model.generate(**enc,num_beams=4,max_new_tokens=512,early_stopping=True)
        return [x.strip() for x in self.tok.batch_decode(gen,skip_special_tokens=True)]
    @staticmethod
    def affixes(piece:str):
        alpha=[i for i,c in enumerate(piece) if c.isalpha()]
        if not alpha:return piece,"",""
        a,b=alpha[0],alpha[-1]; return piece[:a],piece[a:b+1],piece[b+1:]
    def structural(self,source:str):
        pieces=PROTECT_RE.split(source); tokens=PROTECT_RE.findall(source); out=list(pieces); indexes=[]; cores=[]; aff={}
        for i,piece in enumerate(pieces):
            pre,core,suf=self.affixes(piece)
            if core:indexes.append(i);cores.append(core);aff[i]=(pre,suf)
        vals=self.batch(cores)
        if len(vals)!=len(indexes): raise RuntimeError("Lombard structural span mismatch")
        for i,core,val in zip(indexes,cores,vals): pre,suf=aff[i];out[i]=pre+sanitize(core,val)+suf
        result=[]
        for i,piece in enumerate(out):
            result.append(piece)
            if i<len(tokens):result.append(tokens[i])
        return "".join(result)

def main():
    before_files=sorted(ASSETS.glob("**/lang/lmo.json"))
    if len(before_files)!=29: raise SystemExit(f"Expected 29 Lombard files before refinement, found {len(before_files)}")
    before={p:read_json(p) for p in before_files}; common,d121,d261,d262,addons=build_sources(); payloads=[common,d121,d261,d262,*addons.values()]; unique=sorted({str(v) for p in payloads for v in p.values()}); exact=base.build_corpus_map(); translated={}; direct=[]
    for source in unique:
        if source == "": translated[source]=""
        elif source in base.MANUAL_VALUES: translated[source]=base.MANUAL_VALUES[source]
        elif source in exact: translated[source]=exact[source]
        else: direct.append(source)
    print(f"Lombard refinement pool: {len(unique)} unique; {len(unique)-len(direct)} corpus/manual/preserved; {len(direct)} direct OPUS",flush=True)
    mt=Translator()
    for start in range(0,len(direct),24):
        batch=direct[start:start+24]; outputs=mt.batch(batch)
        if len(outputs)!=len(batch):raise SystemExit("Lombard OPUS batch size mismatch")
        for source,value in zip(batch,outputs):
            value=sanitize(source,value);ok=bool(value) and base.placeholder_signature(source)==base.placeholder_signature(value) and protected_signature(source)==protected_signature(value)
            if not ok:value=sanitize(source,mt.structural(source))
            if not value:raise SystemExit(f"Empty Lombard translation: {source!r}")
            if base.placeholder_signature(source)!=base.placeholder_signature(value):raise SystemExit(f"Lombard placeholder mismatch: {source!r}->{value!r}")
            if protected_signature(source)!=protected_signature(value):raise SystemExit(f"Lombard protected-token mismatch: {source!r}->{value!r}")
            if SUSPICIOUS_RE.search(value):raise SystemExit(f"Suspicious Lombard output: {source!r}->{value!r}")
            translated[source]=value
        done=min(start+len(batch),len(direct))
        if done%240==0 or done==len(direct):print(f"Direct Lombard progress: {done}/{len(direct)}",flush=True)
    def pl(src):return {k:translated[str(v)] for k,v in src.items()}
    common_lmo=pl(common)
    for p in ASSETS.glob("neoorigins_lmo_common_*/lang/lmo.json"):p.unlink()
    items=list(common_lmo.items())
    for i in range((len(items)+149)//150):write_json(ASSETS/f"neoorigins_lmo_common_{i+1:02d}/lang/lmo.json",dict(items[i*150:(i+1)*150]))
    write_json(ASSETS/"neoorigins_lmo_121/lang/lmo.json",pl(d121));write_json(ASSETS/"neoorigins_26_1/lang/lmo.json",pl(d261));write_json(ASSETS/"neoorigins_26_2/lang/lmo.json",pl(d262))
    for ns,src in addons.items():write_json(ASSETS/ns/"lang/lmo.json",pl(src))
    after_files=sorted(ASSETS.glob("**/lang/lmo.json"));after={p:read_json(p) for p in after_files};seen={};changed=total=0
    if len(after_files)!=29:raise SystemExit("Lombard file count changed")
    for p,data in after.items():
        if set(before[p])!=set(data):raise SystemExit(f"Lombard key set changed: {p}")
        for k,v in data.items():total+=1;seen[k]=str(v);changed+=before[p][k]!=v
    source_changed=sum(1 for p in payloads for v in p.values() if translated[str(v)]!=str(v));text="\n".join(str(v) for d in after.values() for v in d.values())
    if TARGET_TOKEN in text or SUSPICIOUS_RE.search(text):raise SystemExit("Lombard target marker/artifact survived output")
    if source_changed<2500:raise SystemExit(f"Too many English values survived Lombard MT: {source_changed}")
    if seen.get("key.categories.originsmodernui")!="Origin Architect":raise SystemExit("Origin Architect changed")
    red=exact.get("Red");random=seen.get("button.neoorigins.random")
    if red and random and red.casefold()==random.casefold():raise SystemExit("Random translated as Red")
    if seen.get("neoorigins.night_vision.on")==seen.get("neoorigins.night_vision.off"):raise SystemExit("Night vision on/off identical")
    print(f"Lombard refinement passed: {total} values / 29 files; {changed} bootstrap changes; {source_changed} source values changed",flush=True)

if __name__=="__main__":main()
