#!/usr/bin/env python3
"""Targeted native terminology corrections and Serbian Latin-script parity."""
from pathlib import Path
import importlib.util,json
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
B=ROOT/"build/neoorigins-228"
PATHS={"common":"neoorigins_228_common","121":"neoorigins_228_121","261":"neoorigins_228_26_1"}
FR={
"entity.neoorigins.telegraph":"Signal d'avertissement",
"neoorigins.configuration.allow_mobs":"Autoriser les créatures",
"neoorigins.configuration.always_on":"Toujours actif",
"neoorigins.configuration.amount":"Quantité",
"neoorigins.configuration.caveborn_copper_tint":"Caveborn : teinte cuivrée",
"neoorigins.configuration.caveborn_diamond_tint":"Caveborn : teinte diamant",
"neoorigins.configuration.caveborn_emerald_tint":"Caveborn : teinte émeraude",
"neoorigins.configuration.caveborn_gold_tint":"Caveborn : teinte dorée",
"neoorigins.configuration.caveborn_iron_tint":"Caveborn : teinte fer",
"neoorigins.configuration.caveborn_netherite_tint":"Caveborn : teinte netherite",
"neoorigins.configuration.class_fisher_sea_legs":"Pêcheur : pied marin",
"neoorigins.configuration.class_fisher_swim_speed":"Pêcheur : vitesse de nage",
"neoorigins.configuration.class_fisher_waters_luck":"Pêcheur : chance aquatique",
"neoorigins.configuration.class_mason_block_reach":"Maçon : portée des blocs",
"neoorigins.configuration.class_mason_stone_speed":"Maçon : vitesse de minage de la pierre",
"neoorigins.configuration.class_mason_strong_grip":"Maçon : prise ferme",
"gui.neoorigins.picker.claimed":"Déjà choisie",
"gui.neoorigins.picker.claimed_by":"Déjà choisie par %s",
"origins.neoorigins.class_rogue.description":
 "Assassin furtif qui devient invisible en s'accroupissant et frappe plus fort lorsqu'il est accroupi.",
"power.neoorigins.class_rogue_stealth.description":
 "Après 10 secondes accroupi, tu deviens invisible. Tant que tu es invisible, les créatures ne peuvent plus te choisir comme nouvelle cible."
}
def rj(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def wj(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def main():
    src=rj(B/"source_splits.json")
    frcache=B/"translated/fr_fr.json";fc=rj(frcache)
    count=0
    for ver,folder in PATHS.items():
        p=A/folder/"lang/fr_fr.json";d=rj(p)
        for k in d:
            if k in FR:
                d[k]=FR[k];fc[src[ver][k]]=FR[k];count+=1
        wj(p,d)
    wj(frcache,fc)
    spec=importlib.util.spec_from_file_location("serb",ROOT/"scripts/bootstrap_serbian_latin.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    scp=B/"translated/sr_cs.json";sc=rj(scp)
    total=0
    for ver,folder in PATHS.items():
        source_path=A/folder/"lang/sr_sp.json"
        if not source_path.exists():raise SystemExit(f"Missing Serbian Cyrillic: {source_path}")
        src_data=rj(source_path)
        target={k:mod.transliterate(v) for k,v in src_data.items()}
        wj(A/folder/"lang/sr_cs.json",target)
        for k,v in target.items():sc[src[ver][k]]=v;total+=1
    wj(scp,sc)
    reportpath=B/"translation_report.json";report=rj(reportpath)
    for r in report:
        if r["locale"]=="sr_cs":r["mode"]="Cyrillic-to-Latin transliteration from sr_sp"
        if r["locale"]=="fr_fr":r["manual_reviewed_entries"]=count
    wj(reportpath,report)
    print(f"French terminology corrected: {count}; Serbian Latin transliterated: {total}")
if __name__=="__main__":main()
