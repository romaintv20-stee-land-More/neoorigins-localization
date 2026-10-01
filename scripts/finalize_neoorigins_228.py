#!/usr/bin/env python3
"""Finalize the 2.2.28 update after all 92 locales have been generated."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"build/neoorigins-228"
ASSETS=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
def rj(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def wj(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def replace(p,needle,replacement):
    p=ROOT/p;body=p.read_text(encoding="utf-8")
    if needle not in body:raise RuntimeError(f"Expected source not found in {p}: {needle[:65]}")
    p.write_text(body.replace(needle,replacement),encoding="utf-8")
def main():
    reports=rj(CACHE/"translation_report.json")
    locales=set(next(x for x in rj(ROOT/"catalog.json")["supported_projects"] if x["id"]=="neoorigins")["languages"])
    done={x["locale"] for x in reports if x["status"]=="ok"}
    if done!=locales:raise SystemExit(f"Translation incomplete: {sorted(locales-done)}; failed={len(reports)-len(done)}")
    source=rj(CACHE/"source_splits.json")
    wj(ROOT/"localization/neoorigins_228_source.json",source)
    changed={"origins.neoorigins.class_rogue.description","power.neoorigins.class_rogue_stealth.description"}
    clean_count=0
    for p in ASSETS.glob("neoorigins*/lang/*.json"):
        if p.parts[-3].startswith("neoorigins_228_"):continue
        obj=rj(p)
        if not changed.intersection(obj):continue
        for key in changed:
            if key in obj:del obj[key];clean_count+=1
        wj(p,obj)
    print(f"Pruned {clean_count} superseded Rogue description values.",flush=True)
    catalog=rj(ROOT/"catalog.json")
    for target,new_count in [("1.21.1",2532),("26.1.x",2536),("26.2",2535)]:
        build=catalog["project"]["builds"][target]
        build["version"]=("1.1.1+26.1" if target=="26.1.x" else "1.1.1+"+target)
    neo=next(x for x in catalog["supported_projects"] if x["id"]=="neoorigins")
    comp=neo["compatibility"];comp["version"]="2.2.28"
    comp["audit_refs"]={"1.21.1":"87860513d5947fa0407a4dd1868126c9489e56cd",
                        "26.1.x":"4f11c58362a7b3c76d5475ed072b79f49ceb537d",
                        "26.2":"d2d7c0b6d5439e11e3ed3e981dcdd25642f0b417"}
    comp["delta_2_2_28"]={"common":228,"mc_1_21_1_only":8,"mc_26_1_only":1,
                            "mc_26_2_only":0,"changed_descriptions":2,
                            "fallback_namespaces":{"common":"neoorigins_228_common","1.21.1":"neoorigins_228_121",
                                                   "26.1.x":"neoorigins_228_26_1"}}
    for target,n in [("1.21.1",2532),("26.1.x",2536),("26.2",2535)]:
        comp["coverage"][target]["english_keys"]=n
        comp["coverage"][target]["covered_keys"]=n
    wj(ROOT/"catalog.json",catalog)
    replace("gradle.properties","mod_version=1.1.0","mod_version=1.1.1")
    for doc in ["README.md","CATALOG.md"]:
        p=ROOT/doc
        body=p.read_text(encoding="utf-8").replace("1.1.0+1.21.1","1.1.1+1.21.1").replace(
           "1.1.0+26.1","1.1.1+26.1").replace("1.1.0+26.2","1.1.1+26.2")
        if doc=="README.md":
            marker="## Langues\n"
            note=("## NeoOrigins 2.2.28 (mise à jour 1.1.1)\n\n"
                "Les trois builds intègrent les nouvelles clés anglaises de NeoOrigins 2.2.28. "
                "Les **92 locales** reçoivent un fallback pour les **228 nouvelles clés communes**, "
                "plus **8 clés 1.21.1** ou **1 clé 26.1.x** ; les **deux descriptions du Voleur** "
                "sont actualisées. Le code et les JAR amont restent ceux de NeoOrigins.\n\n"
                "Les nouveaux textes ont été générés avec réutilisation de traductions existantes "
                "et traduction automatique vérifiée structurellement. Une révision native est "
                "encore souhaitable, notamment pour les variantes régionales et dialectales.\n\n")
            body=body.replace(marker,note+marker,1)
        else:
            marker="## Notes\n"
            body=body.replace(marker,("## Mise à jour 2.2.28\n\n"
                "La 1.1.1 intègre 236 nouvelles clés distinctes pour les 92 langues "
                "(228 communes aux trois versions, 8 propres à 1.21.1 et 1 propre à 26.1.x) "
                "et deux descriptions modifiées. Les nouvelles traductions nécessitent encore une "
                "relecture linguistique, sans modification du nombre de langues.\n\n")+marker,1)
        p.write_text(body,encoding="utf-8")
    gradle=ROOT/"build.gradle";g=gradle.read_text(encoding="utf-8")
    pos="    if (!include26_1Translations) {"
    extra=("    if (!include121BatchTranslations) {\n"
           "        exclude 'resourcepacks/fallback_localizations/assets/neoorigins_228_121/**'\n"
           "    }\n"
           "    if (!include26_1Translations) {\n"
           "        exclude 'resourcepacks/fallback_localizations/assets/neoorigins_228_26_1/**'\n"
           "    }\n"
           "    if (!include26_2Translations) {\n"
           "        exclude 'resourcepacks/fallback_localizations/assets/neoorigins_228_26_2/**'\n"
           "    }\n")
    if "neoorigins_228_121" not in g:
        assert pos in g;gradle.write_text(g.replace(pos,extra+pos,1),encoding="utf-8")
    print("Updated metadata, documentation and Gradle packaging.",flush=True)
if __name__=="__main__":main()
