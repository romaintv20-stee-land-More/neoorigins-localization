#!/usr/bin/env python3
"""Offline QA for pinned NeoOrigins 2.2.28 translations across all 92 locales."""
from pathlib import Path
import collections,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
SOURCE=ROOT/"localization/neoorigins_228_source.json"
PATHS={"common":"neoorigins_228_common","121":"neoorigins_228_121",
       "261":"neoorigins_228_26_1","262":"neoorigins_228_26_2"}
PH=re.compile(r"%(?:\d+\$)?[sdif]")
def rj(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def main():
    src=rj(SOURCE)
    langs=next(x for x in rj(ROOT/"catalog.json")["supported_projects"] if x["id"]=="neoorigins")["languages"]
    if len(langs)!=92:raise SystemExit(f"Expected 92 locales, got {len(langs)}")
    errors=[];stats=collections.Counter()
    expected={"common":230,"121":8,"261":1,"262":0}
    for version,keys in src.items():
        if len(keys)!=expected[version]:errors.append(f"{version}: expected {expected[version]}, found {len(keys)}")
    for locale in langs:
        for ver,namespace in PATHS.items():
            p=A/namespace/"lang"/f"{locale}.json"
            if not src[ver]:
                if p.exists():errors.append(f"{locale} {ver}: unexpected file")
                continue
            if not p.exists():
                errors.append(f"{locale} {ver}: missing file");continue
            data=rj(p)
            if set(data)!=set(src[ver]):
                missing=set(src[ver])-set(data);stale=set(data)-set(src[ver])
                errors.append(f"{locale} {ver}: missing {len(missing)}, stale {len(stale)}")
            for k,s in src[ver].items():
                t=data.get(k)
                if not isinstance(t,str) or not t.strip():errors.append(f"{locale}: empty {k}")
                elif sorted(PH.findall(s))!=sorted(PH.findall(t)):errors.append(f"{locale}: placeholder {k}")
            stats[ver]+=len(data)
        # Changed descriptions must not remain in older, higher-sorted fallback namespaces.
        for p in A.glob(f"neoorigins*/lang/{locale}.json"):
            if p.parent.parent.name.startswith("neoorigins_228_"):continue
            d=rj(p)
            duplicates=set(src["common"]) & set(d)
            if duplicates:errors.append(f"{locale} duplicate in {p.parent.parent.name}: {len(duplicates)}")
    report={"locales":len(langs),"per_locale":expected,"total_new_entries":sum(stats.values()),
            "errors":errors}
    (ROOT/"build/neoorigins-228").mkdir(parents=True,exist_ok=True)
    (ROOT/"build/neoorigins-228/offline_audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="errors"},ensure_ascii=False))
    if errors:
        print("\n".join(errors[:30]));raise SystemExit(f"FAIL: {len(errors)} audit errors")
    print("PASS: 92 locales; version-specific key sets and placeholders valid")
if __name__=="__main__":main()
