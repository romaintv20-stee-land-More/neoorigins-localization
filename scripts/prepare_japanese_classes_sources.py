#!/usr/bin/env python3
from pathlib import Path
import io, json, urllib.request, zipfile

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ("8393343", "Origins-Classes-Ex-1.21.1-NeoOrigins-1.0.1.jar", "origins_classes_extended", "tmp_origins_classes_extended_ja_missing_en.json"),
    ("8592095", "Origins-Classes-ISS-1.21.1-NeoOrigins-1.0.1.jar", "origins_classes_iss", "tmp_origins_classes_iss_ja_missing_en.json"),
]
for file_id, filename, namespace, output in TARGETS:
    a, b = file_id[:-3], file_id[-3:]
    url = f"https://edge.forgecdn.net/files/{a}/{b}/{filename}"
    req = urllib.request.Request(url, headers={"User-Agent":"NeoOrigins-Localization-Audit","Referer":"https://www.curseforge.com/"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = set(z.namelist())
        if f"assets/{namespace}/lang/en_us.json" not in names:
            candidates = sorted(name.split("/")[1] for name in names if name.startswith("assets/") and name.endswith("/lang/en_us.json") and len(name.split("/")) == 4)
            if len(candidates) != 1:
                raise SystemExit(f"Could not detect namespace for {filename}: {candidates}")
            namespace = candidates[0]
        en = json.loads(z.read(f"assets/{namespace}/lang/en_us.json").decode("utf-8"))
        try:
            ja = json.loads(z.read(f"assets/{namespace}/lang/ja_jp.json").decode("utf-8"))
        except KeyError:
            ja = {}
    missing = {k:v for k,v in en.items() if k not in ja}
    (ROOT / output).write_text(json.dumps(missing, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"{namespace}: EN={len(en)} OFFICIAL_JA={len(ja)} MISSING={len(missing)}")
