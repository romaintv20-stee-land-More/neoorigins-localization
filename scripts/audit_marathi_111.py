#!/usr/bin/env python3
"""Strict structural/packaging audit for Marathi added to 1.1.1."""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
PH=re.compile(r"%(?:\d+\$)?[sdif]")
PACK="resourcepacks/fallback_localizations/"
VER={"mc-1.21.1":("121","1.21.1"),"mc-26.1.x":("261","26.1.2"),
     "mc-26.2":("262","26.2")}
TARGET_NS={"121":"neoorigins_mr_121","261":"neoorigins_mr_26_1",
           "262":"neoorigins_mr_26_2"}
def rj(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(keys):return hashlib.sha256("\n".join(sorted(keys)).encode("utf-8")).hexdigest()
def check(src,localized,label):
    assert isinstance(localized,dict),label
    missing=set(src)-set(localized);stale=set(localized)-set(src)
    if missing or stale:raise RuntimeError(f"{label} missing={len(missing)} stale={len(stale)}")
    for key,source in src.items():
        target=localized[key]
        if not isinstance(target,str) or (source!="" and not target.strip()):
            raise RuntimeError(f"{label}: empty/non-text value {key}")
        if sorted(PH.findall(source))!=sorted(PH.findall(target)):
            raise RuntimeError(f"{label}: placeholder mismatch {key}")
def source_audit():
    c=rj(ROOT/"catalog.json")
    assert c["project"]["supported_locale_count"]==93
    assert len(c["supported_projects"])==12
    assert all("mr_in" in p["languages"] for p in c["supported_projects"])
    assert all(len(p["languages"])==93 for p in c["supported_projects"] if p["id"]!="pathfinder_origins")
    assert len(next(p for p in c["supported_projects"] if p["id"]=="pathfinder_origins")["languages"])==14
    core=rj(ROOT/"localization/marathi_core_source.json")
    addons=rj(ROOT/"localization/marathi_addons_source.json")
    coverage=rj(ROOT/"localization/marathi_coverage.json")
    chunks=sorted(ASSETS.glob("neoorigins_mr_common_*/lang/mr_in.json"))
    common={}
    assert len(chunks)==(len(core["common"])+149)//150
    for file in chunks:
        payload=rj(file)
        if set(common)&set(payload):raise RuntimeError(f"Duplicate Marathi core keys in {file}")
        common.update(payload)
    check(core["common"],common,"core common")
    for target,ns in TARGET_NS.items():
        delta=rj(ASSETS/ns/"lang/mr_in.json")
        check(core[target],delta,f"core {target}")
        full={**common,**delta}
        expected={"121":2532,"261":2536,"262":2535}[target]
        assert len(full)==expected
        assert len(set(common)&set(delta))==0
    for ns,english in addons.items():
        p=ASSETS/ns/"lang/mr_in.json"
        check(english,rj(p),f"addon {ns}")
        assert c["supported_projects"][[p["id"] for p in c["supported_projects"]].index(ns)]["languages"]["mr_in"]["fallback_keys"]==len(english)
    ctx=rj(ROOT/"localization/background_orb_translations.json")
    registered=set(next(p for p in c["supported_projects"] if p["id"]=="neoorigins")["languages"])
    assert set(ctx)==registered
    src_ctx={key:addons["origins_backgrounds"][key] for key in ctx["mr_in"]}
    check(src_ctx,ctx["mr_in"],"Marathi Background Orb contextual override")
    mr_bg=rj(ASSETS/"origins_backgrounds/lang/mr_in.json")
    assert all(mr_bg[k]==v for k,v in ctx["mr_in"].items())
    for target,version in (("121","1.21.1"),("261","26.1.2"),("262","26.2")):
        localized=rj(ROOT/"localization/minecraft_marathi"/version/"mr_in.json")
        manifest=coverage["minecraft"][version]
        assert len(localized)==manifest["keys"]
        assert sha(localized)==manifest["key_sha256"]
    mcmeta=(ROOT/"src/main/resources"/PACK/"pack.mcmeta").read_text(encoding="utf-8")
    mcmeta=mcmeta.replace("$"+"{resource_pack_format}","34")
    language=json.loads(mcmeta)["language"]["mr_in"]
    assert language=={"region":"भारत","name":"मराठी","bidirectional":False}
    print("PASS Marathi: 93 registered locales; 3 core inventories; 11 add-ons; 3 Minecraft inventories.")
    return core,addons,coverage
def jar_audit(jar,target,core,addons,coverage):
    key,version=VER[target]
    with zipfile.ZipFile(jar) as archive:
        files=set(archive.namelist())
        def get(path):
            if path not in files:raise RuntimeError(f"{target}: missing {path}")
            return json.loads(archive.read(path))
        metadata=get(PACK+"pack.mcmeta")
        assert metadata["language"]["mr_in"]["name"]=="मराठी"
        vanilla_path=PACK+"assets/minecraft/lang/mr_in.json"
        vanilla=get(vanilla_path)
        assert len(vanilla)==coverage["minecraft"][version]["keys"]
        assert sha(vanilla)==coverage["minecraft"][version]["key_sha256"]
        coremap={}
        common=sorted(f for f in files if re.fullmatch(PACK+r"assets/neoorigins_mr_common_\d+/lang/mr_in\.json",f))
        assert len(common)==(len(core["common"])+149)//150,(target,len(common))
        for path in common:
            for k,v in get(path).items():
                if k in coremap:raise RuntimeError(f"{target}: duplicated core key {k}")
                coremap[k]=v
        for t,ns in TARGET_NS.items():
            name=PACK+f"assets/{ns}/lang/mr_in.json"
            if t==key:
                for k,v in get(name).items():
                    if k in coremap:raise RuntimeError(f"{target}: shared & delta overlap {k}")
                    coremap[k]=v
            elif name in files:raise RuntimeError(f"{target}: wrong target namespace {ns}")
        expected={**core["common"],**core[key]}
        check(expected,coremap,f"{target} core")
        for ns,src in addons.items():
            name=PACK+f"assets/{ns}/lang/mr_in.json"
            if key=="121":check(src,get(name),f"{target} {ns}")
            elif name in files:raise RuntimeError(f"{target}: 1.21.1 addon leaked: {ns}")
        ctx=rj(ROOT/"localization/background_orb_translations.json")["mr_in"]
        contextual_path="resourcepacks/background_orb_localizations/assets/neoorigins/lang/mr_in.json"
        if key=="121":
            check({k:addons["origins_backgrounds"][k] for k in ctx},get(contextual_path),"Background Orb contextual pack")
        elif contextual_path in files:raise RuntimeError(f"{target}: 1.21.1 contextual pack leaked")
    print(f"PASS JAR {target}: {len(coremap)} NeoOrigins keys, {len(vanilla)} Minecraft keys")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar");p.add_argument("--target",choices=list(VER))
    args=p.parse_args()
    core,addons,coverage=source_audit()
    if bool(args.jar)!=bool(args.target):p.error("Specify both --jar and --target")
    if args.jar:jar_audit(args.jar,args.target,core,addons,coverage)
if __name__=="__main__":main()
