#!/usr/bin/env python3
"""Verify the official Anti Magick: NeoOrigins 0.1.2 language delta and fallbacks."""
from pathlib import Path
import json
import re
import io
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
URL="https://cdn.modrinth.com/data/Ef2BIfFi/versions/PkvY4hbS/antimagick_neoorigins-0.1.2.jar"
NAMESPACE="antimagick_neoorigins"
LANG=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"/NAMESPACE/"lang"
EXPECTED={
 "category.antimagick_neoorigins.active_powers": "NeoOrigins active powers",
 "category.antimagick_neoorigins.summons": "NeoOrigins summons"
}
PLACEHOLDER=re.compile(r"%(?:\d+\$)?[sd]")
def read_zip_locale(jar,name):
    return json.loads(jar.read("assets/"+NAMESPACE+"/lang/"+name+".json").decode("utf-8"))
def main():
    req=urllib.request.Request(URL,headers={"User-Agent":"NeoOrigins-Localization-Audit/1.2.0"})
    with urllib.request.urlopen(req,timeout=45) as response:
        source=response.read()
    assert source[:2]==b"PK","Upstream JAR unavailable or invalid"
    with zipfile.ZipFile(io.BytesIO(source)) as jar:
        en=read_zip_locale(jar,"en_us")
        assert en==EXPECTED,f"Anti Magick English keys changed: {en!r}"
        ru=read_zip_locale(jar,"ru_ru")
        assert set(ru)==set(EXPECTED),"Russian coverage changed"
    catalog=json.loads((ROOT/"catalog.json").read_text(encoding="utf-8"))
    meta=next(p for p in catalog["supported_projects"] if p["id"]==NAMESPACE)
    assert set(meta["languages"])==set(p.stem for p in (ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets/origins_furries/lang").glob("*.json"))
    expected_locales=set(meta["languages"])-{"ru_ru"}
    existing={p.stem for p in LANG.glob("*.json")}
    assert existing==expected_locales,("Missing locales", sorted(expected_locales-existing),sorted(existing-expected_locales))
    assert len(existing)==92
    for loc in sorted(existing):
        labels=json.loads((LANG/(loc+".json")).read_text(encoding="utf-8"))
        assert set(labels)==set(EXPECTED),loc
        for key,val in labels.items():
            assert isinstance(val,str) and val.strip() and "NeoOrigins" in val,(loc,key)
            assert PLACEHOLDER.findall(val)==PLACEHOLDER.findall(EXPECTED[key]),(loc,key)
    assert not (LANG/"ru_ru.json").exists(),"Never override upstream Russian"
    print("Anti Magick upstream audit OK: 2 keys, 92 complete fallback locales, Russian handled upstream")
if __name__=="__main__":
    main()
