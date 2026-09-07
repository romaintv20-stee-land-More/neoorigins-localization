#!/usr/bin/env python3
from pathlib import Path
import json
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
REF = "1.21.1-fabric"
BASE = f"https://raw.githubusercontent.com/muon-rw/Medieval-Origins-Revival/{REF}/src/main/resources/assets/medievalorigins/lang/{{locale}}.json"


def fetch(locale, allow_missing=False):
    try:
        with urllib.request.urlopen(BASE.format(locale=locale), timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if allow_missing and e.code == 404:
            return {}
        raise


en = fetch("en_us")
official = fetch("ja_jp", allow_missing=True)
merged = {}
for path in sorted(ASSETS.glob("medievalorigins_ja_*/lang/ja_jp.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    overlap = set(merged) & set(data)
    if overlap:
        raise SystemExit(f"duplicate keys in Japanese files: {sorted(overlap)[:10]}")
    merged.update(data)

missing = {k: v for k, v in en.items() if k not in official and k not in merged}
out = ROOT / "tmp_medieval_ja_missing_en.json"
out.write_text(json.dumps(missing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"EN={len(en)} OFFICIAL={len(official)} FALLBACK={len(merged)} MISSING={len(missing)}")
