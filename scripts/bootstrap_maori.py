#!/usr/bin/env python3
"""Bootstrap Māori (`mi_nz`) fallbacks from English.

Exact whole-string Minecraft corpus matches are reused first. Remaining English is
left for direct NLLB `eng_Latn -> mri_Latn` refinement. No pivot or word projection.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
import json, re, urllib.request

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
PLACEHOLDER_RE=re.compile(r"%(?:\d+\$)?[sdif]")
MC_REF="83af272f5a618b287781ee9ce2a48cfc8f47dd61"
MC_BASE=f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{MC_REF}/java"
MANUAL_VALUES={"Origin Architect":"Origin Architect"}

def read_json(path:Path):return json.loads(path.read_text(encoding="utf-8"))
def write_json(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def fetch_json(url:str):
    req=urllib.request.Request(url,headers={"User-Agent":"NeoOrigins-Maori-Bootstrap"})
    with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
def placeholder_signature(text:str):return sorted(PLACEHOLDER_RE.findall(text))

def build_corpus_map()->dict[str,str]:
    en=fetch_json(f"{MC_BASE}/en_us.json");mi=fetch_json(f"{MC_BASE}/mi_nz.json");votes:dict[str,Counter[str]]=defaultdict(Counter);rejected=unchanged=0;shared=sorted(set(en)&set(mi))
    for key in shared:
        source,target=str(en[key]),str(mi[key])
        if source.casefold()==target.casefold():unchanged+=1;continue
        if not source.strip() or not target.strip() or placeholder_signature(source)!=placeholder_signature(target):rejected+=1;continue
        votes[source][target]+=1
    exact={};ambiguous=0
    for source,counter in votes.items():
        target,top=counter.most_common(1)[0];total=sum(counter.values())
        if top/total>=.80:exact[source]=target
        else:ambiguous+=1
    print(f"Minecraft Māori corpus: {len(shared)} aligned; {rejected} rejected; {unchanged} unchanged; {len(exact)} exact; {ambiguous} ambiguous")
    return exact

def payload(source:dict[str,str],exact:dict[str,str]):
    out={}
    for key,raw in source.items():
        value=str(raw);translated=MANUAL_VALUES.get(value,exact.get(value,value))
        if placeholder_signature(value)!=placeholder_signature(translated):raise RuntimeError(f"Māori placeholder mismatch: {value!r}->{translated!r}")
        out[key]=translated
    return out

def main():
    n121=read_json(ROOT/"build/mi-discovery-mc-1.21.1/mi_nz_missing_en.json");n261=read_json(ROOT/"build/mi-discovery-mc-26.1/mi_nz_missing_en.json");n262=read_json(ROOT/"build/mi-discovery-mc-26.2/mi_nz_missing_en.json")
    common={k:v for k,v in n121.items() if n261.get(k)==v and n262.get(k)==v};d121={k:v for k,v in n121.items() if k not in common};d261={k:v for k,v in n261.items() if k not in common};d262={k:v for k,v in n262.items() if k not in common}
    print(f"NeoOrigins Māori split: common={len(common)}, 1.21.1={len(d121)}, 26.1={len(d261)}, 26.2={len(d262)}")
    folders={"medievalorigins":"medievalorigins-upstream-audit","ibarnorigins":"ibarnorigins-upstream-audit","origins_fantasy":"origins-fantasy-upstream-audit","origins_backgrounds":"origins-backgrounds-upstream-audit","origins_backgrounds_two":"origins-more-backgrounds-upstream-audit","origins_backgrounds_iss":"origins-backgrounds-iss-upstream-audit","origins_furries":"origins-furries-upstream-audit","origins_classes_ex":"origins-classes-extended-upstream-audit","origins_classes_iss":"origins-classes-iss-upstream-audit","originsmodernui":"origin-architect-upstream-audit"}
    addons={ns:read_json(ROOT/f"build/{folder}/upstream_en_us.json") for ns,folder in folders.items()};shared_bg=set(addons["origins_backgrounds"]);addons["origins_backgrounds_two"]={k:v for k,v in addons["origins_backgrounds_two"].items() if k not in shared_bg};addons["origins_backgrounds_iss"]={k:v for k,v in addons["origins_backgrounds_iss"].items() if k not in shared_bg}
    exact=build_corpus_map();common_mi=payload(common,exact)
    for path in ASSETS.glob("neoorigins_mi_common_*/lang/mi_nz.json"):path.unlink()
    items=list(common_mi.items())
    for i in range((len(items)+149)//150):write_json(ASSETS/f"neoorigins_mi_common_{i+1:02d}/lang/mi_nz.json",dict(items[i*150:(i+1)*150]))
    write_json(ASSETS/"neoorigins_mi_121/lang/mi_nz.json",payload(d121,exact));write_json(ASSETS/"neoorigins_26_1/lang/mi_nz.json",payload(d261,exact));write_json(ASSETS/"neoorigins_26_2/lang/mi_nz.json",payload(d262,exact))
    for ns,src in addons.items():write_json(ASSETS/ns/"lang/mi_nz.json",payload(src,exact))
    files=sorted(ASSETS.glob("**/lang/mi_nz.json"))
    if len(files)!=29:raise RuntimeError(f"Expected 29 Māori files, found {len(files)}")
    sources=[common,d121,d261,d262,*addons.values()];total=sum(len(x) for x in sources);hits=sum(1 for x in sources for v in x.values() if str(v) in exact or str(v) in MANUAL_VALUES)
    print(f"Māori bootstrap: 29 files; exact/manual {hits}/{total}; {total-hits} remain for NLLB")
if __name__=="__main__":main()
