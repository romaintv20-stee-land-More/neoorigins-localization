#!/usr/bin/env python3
"""Build Marathi from Beyond & More's Minecraft translations and pinned add-on English."""
from __future__ import annotations
from collections import Counter,defaultdict
from pathlib import Path
import argparse,hashlib,json,re,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import sync_neoorigins_228 as translation
ASSETS=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
BNM=Path(r"D:\ssd\Autres\Mcreator\Mods\Steel_and_More\src\main\resources\assets")
CACHED=ROOT/"build/marathi-sources"
CACHE=ROOT/"build/marathi-cache/mr_translations.json"
LOCALE="mr_in"
REFS={"121":"87860513d5947fa0407a4dd1868126c9489e56cd",
      "261":"4f11c58362a7b3c76d5475ed072b79f49ceb537d",
      "262":"d2d7c0b6d5439e11e3ed3e981dcdd25642f0b417"}
VANILLA={"121":"1.21.1","261":"26.1.2","262":"26.2"}
ADDONS={
 "medievalorigins":"medievalorigins-upstream-audit",
 "ibarnorigins":"ibarnorigins-upstream-audit",
 "origins_fantasy":"origins-fantasy-upstream-audit",
 "origins_backgrounds":"origins-backgrounds-upstream-audit",
 "origins_backgrounds_two":"origins-more-backgrounds-upstream-audit",
 "origins_backgrounds_iss":"origins-backgrounds-iss-upstream-audit",
 "origins_furries":"origins-furries-upstream-audit",
 "origins_classes_ex":"origins-classes-extended-upstream-audit",
 "origins_classes_iss":"origins-classes-iss-upstream-audit",
 "originsmodernui":"origin-architect-upstream-audit"}
PH=re.compile(r"%(?:\d+\$)?[sdif]")
def rj(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def wj(p,data):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
def sha(keys):
    return hashlib.sha256("\n".join(sorted(keys)).encode("utf-8")).hexdigest()
def sig(t):return sorted(PH.findall(t))
def build_corpus(bn_en,bn_mr,van_en,van_mr):
    votes=defaultdict(Counter)
    for english,marathi in ((bn_en,bn_mr),(van_en,van_mr)):
        for k in english.keys() & marathi.keys():
            e=english[k];m=marathi[k]
            if isinstance(e,str) and isinstance(m,str) and m.strip() and sig(e)==sig(m):
                votes[e][m]+=2 if english is van_en else 1
    return {src:freq.most_common(1)[0][0] for src,freq in votes.items()}
def load_sources():
    old_en=rj(CACHED/"minecraft_26.1.2_en_us.json")
    old_mr=rj(BNM/"minecraft/lang/mr_in.json")
    mod_en=rj(BNM/"steel_and_more/lang/en_us.json")
    mod_mr=rj(BNM/"steel_and_more/lang/mr_in.json")
    assert len(old_mr)==7886,len(old_mr)
    assert set(old_mr)==set(rj(CACHED/"minecraft_26.1.2_en_us.json"))
    corpus=build_corpus(mod_en,mod_mr,old_en,old_mr)
    core={t:rj(ROOT/"build/neoorigins-228"/f"{ref}_en_us.json") for t,ref in REFS.items()}
    assert {v:len(d) for v,d in core.items()}=={"121":2532,"261":2536,"262":2535}
    common={k:v for k,v in core["121"].items() if all(core[x].get(k)==v for x in ("261","262"))}
    sections={"common":dict(sorted(common.items()))}
    for target in ("121","261","262"):
        sections[target]={k:v for k,v in sorted(core[target].items()) if k not in common}
    for target in ("121","261","262"):
        assert {**sections["common"],**sections[target]}==core[target]
    addons={name:rj(ROOT/"build"/folder/"upstream_en_us.json") for name,folder in ADDONS.items()}
    backgrounds=set(addons["origins_backgrounds"])
    for name in ("origins_backgrounds_two","origins_backgrounds_iss"):
        addons[name]={k:v for k,v in addons[name].items() if k not in backgrounds}
    pathfinder=rj(ASSETS/"pathfinder_origins/lang/fr_fr.json")
    assert len(pathfinder)==406,len(pathfinder)
    addons["pathfinder_origins"]={k:k for k in pathfinder}
    vanilla={target:rj(CACHED/f"minecraft_{ver}_en_us.json") for target,ver in VANILLA.items()}
    return old_en,old_mr,corpus,sections,addons,vanilla
def valid(src,tr):
    return isinstance(tr,str) and (src==tr=="" or bool(tr.strip())) and sig(src)==sig(tr)
def fill_cache(corpus,sections,addons,vanilla,old_en,old_mr):
    cache=dict(corpus);cache[""]=""
    if CACHE.exists():cache.update(rj(CACHE))
    all_sources={v for group in [*sections.values(),*addons.values()] for v in group.values() if v}
    for target,en in vanilla.items():
        for k,value in en.items():
            if k in old_mr and old_en.get(k)==value and valid(value,old_mr[k]):
                cache[value]=old_mr[k]
            elif value:all_sources.add(value)
    # Preserve brand names and project-specific names for consistent UI display.
    for name in ("NeoOrigins","Minecraft","Beyond & More","Origin Architect","Elytra","Pathfinder Origins"):
        cache[name]=name
    todo=[v for v in sorted(all_sources) if v not in cache or not valid(v,cache[v])]
    print(f"Marathi corpus: {len(corpus)} reusable source strings; {len(todo)} new unique sources",flush=True)
    if todo:
        total=len(translation.chunks(todo,n=18,limit=1350))
        for i,batch in enumerate(translation.chunks(todo,n=18,limit=1350),1):
            try:
                result=translation.machine_batch(batch,"mr")
            except Exception as ex:
                print("Batch",i,"requires direct placeholder-safe translation:",repr(ex),flush=True)
                result=[]
                for src in batch:
                    translated=translation.google(src,"mr")
                    if not valid(src,translated):
                        protected=[];index=0
                        def protect(m):
                            nonlocal index
                            token="⟦"+str(index).zfill(4)+"⟧"
                            protected.append((token,m.group(0)))
                            index+=1
                            return token
                        masked=re.sub(r"%(?:\\d+\\$)?[sdif]|§.|\\\\n",protect,src)
                        translated=translation.google(masked,"mr")
                        for token,original in protected:translated=translated.replace(token,original)
                    if not valid(src,translated):
                        raise ValueError(f"Marathi placeholder mismatch in direct translation: {src!r} -> {translated!r}")
                    result.append(translated)
            for src,target in zip(batch,result):
                if not valid(src,target):raise ValueError(f"Marathi placeholder mismatch: {src!r} -> {target!r}")
                cache[src]=target
            wj(CACHE,{k:cache[k] for k in cache if k not in corpus})
            if i%8==0 or i==total:
                print("TRANSLATED",i,"/",total,"batches",flush=True)
            time.sleep(.12)
    return cache
def materialize(old_en,old_mr,cache,sections,addons,vanilla):
    output=ROOT/"localization/minecraft_marathi"
    core_source=ROOT/"localization/marathi_core_source.json"
    addon_source=ROOT/"localization/marathi_addons_source.json"
    wj(core_source,sections);wj(addon_source,addons)
    common=list(sorted(sections["common"].items()))
    for index in range((len(common)+149)//150):
        chunk=dict(common[index*150:(index+1)*150])
        wj(ASSETS/f"neoorigins_mr_common_{index+1:02d}/lang/mr_in.json",
           {k:cache[v] for k,v in chunk.items()})
    for target,folder in (("121","neoorigins_mr_121"),("261","neoorigins_mr_26_1"),("262","neoorigins_mr_26_2")):
        wj(ASSETS/folder/"lang/mr_in.json",{k:cache[v] for k,v in sections[target].items()})
    for namespace,source in addons.items():
        wj(ASSETS/namespace/"lang/mr_in.json",{k:cache[v] for k,v in source.items()})
    summary={"source":"Beyond & More 26.1.2 mr_in and pinned source strings",
             "locale":"mr_in","review_status":"machine_translation_pending_native_review",
             "core_sections":{k:len(v) for k,v in sections.items()},
             "addon_keys":{k:len(v) for k,v in addons.items()},"minecraft":{}}
    for target,english in vanilla.items():
        localized={}
        for key,source in english.items():
            if key in old_mr and old_en.get(key)==source and valid(source,old_mr[key]):
                value=old_mr[key]
            else:value=cache[source]
            if not valid(source,value):raise RuntimeError(f"Invalid vanilla {target} {key}")
            localized[key]=value
        path=output/VANILLA[target]/"mr_in.json"
        wj(path,localized)
        summary["minecraft"][VANILLA[target]]={
            "keys":len(localized),"key_sha256":sha(localized),
            "reused_from_bnm":sum(1 for k,v in english.items() if old_en.get(k)==v)}
        print("MINECRAFT",VANILLA[target],len(localized),"keys",flush=True)
    wj(ROOT/"localization/marathi_coverage.json",summary)
    print("MARATHI GENERATED",{k:len(v) for k,v in sections.items()},
          "addons",{k:len(v) for k,v in addons.items()},flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument("--prepare-only",action="store_true");p.add_argument("--build-only",action="store_true")
    args=p.parse_args()
    inputs=load_sources()
    old_en,old_mr,corpus,sections,addons,vanilla=inputs
    if args.prepare_only:
        CACHE.parent.mkdir(parents=True,exist_ok=True)
        wj(ROOT/"build/marathi-cache/source_counts.json",
           {"core":{k:len(v) for k,v in sections.items()},
            "addons":{k:len(v) for k,v in addons.items()},
            "vanilla":{k:len(v) for k,v in vanilla.items()} })
        print("Source split and counts prepared.",flush=True);return
    if args.build_only:
        if not CACHE.exists():raise RuntimeError("Translate cache missing")
        cache=build_corpus(rj(BNM/"steel_and_more/lang/en_us.json"),
            rj(BNM/"steel_and_more/lang/mr_in.json"),old_en,old_mr)
        cache.update(rj(CACHE))
    else:cache=fill_cache(corpus,sections,addons,vanilla,old_en,old_mr)
    materialize(old_en,old_mr,cache,sections,addons,vanilla)
if __name__=="__main__":main()
