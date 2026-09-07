#!/usr/bin/env python3
from pathlib import Path
import io, json, urllib.request, zipfile

ROOT = Path(__file__).resolve().parents[1]
FILE_ID = "8397352"
FILENAME = "Origins-Furries-1.21.1-NeoOrigins-1.0.0.jar"
a, b = FILE_ID[:-3], FILE_ID[-3:]
url = f"https://edge.forgecdn.net/files/{a}/{b}/{FILENAME}"
req = urllib.request.Request(url, headers={"User-Agent":"NeoOrigins-Localization-Audit","Referer":"https://www.curseforge.com/"})
with urllib.request.urlopen(req, timeout=60) as r:
    data = r.read()
with zipfile.ZipFile(io.BytesIO(data)) as z:
    en = json.loads(z.read("assets/origins_furries/lang/en_us.json").decode("utf-8"))
    try:
        ja = json.loads(z.read("assets/origins_furries/lang/ja_jp.json").decode("utf-8"))
    except KeyError:
        ja = {}
missing = {k:v for k,v in en.items() if k not in ja}
(ROOT / "tmp_origins_furries_ja_missing_en.json").write_text(json.dumps(missing, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(f"EN={len(en)} OFFICIAL_JA={len(ja)} MISSING={len(missing)}")
