#!/usr/bin/env python3
"""Inspect 2.2.28 localized deltas in each target-specific built JAR."""
from pathlib import Path
import argparse,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument("--jar",required=True);p.add_argument("--target",required=True)
args=p.parse_args()
mapping={"mc-1.21.1":"121","mc-26.1.x":"261","mc-26.2":"262"}
if args.target not in mapping:raise SystemExit(f"Unknown target: {args.target}")
src=json.loads((ROOT/"localization/neoorigins_228_source.json").read_text(encoding="utf-8"))
locales=list(next(x for x in json.loads((ROOT/"catalog.json").read_text(encoding="utf-8"))["supported_projects"] if x["id"]=="neoorigins")["languages"])
paths={"common":"neoorigins_228_common","121":"neoorigins_228_121",
       "261":"neoorigins_228_26_1","262":"neoorigins_228_26_2"}
with zipfile.ZipFile(args.jar) as f:
    names=set(f.namelist())
    for loc in locales:
        for v,ns in paths.items():
            name=f"resourcepacks/fallback_localizations/assets/{ns}/lang/{loc}.json"
            required=(v=="common" or v==mapping[args.target]) and bool(src[v])
            if (name in names)!=required:raise SystemExit(f"BAD {args.target} {loc}: {name} presence={name in names}, expected={required}")
            if required:
                data=json.loads(f.read(name))
                if set(data)!=set(src[v]):raise SystemExit(f"BAD key inventory: {args.target} {loc} {v}")
print(f"PASS {args.target}: 92 common locale files plus target-specific 2.2.28 deltas.")
