#!/usr/bin/env python3
from pathlib import Path
import json
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
OUT = ASSETS / "neoorigins_26_2/lang"
TMP = ROOT / "tmp/26_2_translation_needed"
REF = "26.2"
BASE = "https://raw.githubusercontent.com/CyberDay1/NeoOrigins/{ref}/src/main/resources/assets/neoorigins/lang/{locale}.json"
LOCALES = ("it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn")


def fetch(locale: str, allow_missing=False):
    url = BASE.format(ref=REF, locale=locale)
    req = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Localization-Prepare"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as exc:
        if allow_missing and exc.code == 404:
            return {}
        raise


def load_existing(locale: str):
    merged = {}
    batch = ASSETS / "neoorigins_121_batch1/lang" / f"{locale}.json"
    if batch.exists():
        merged.update(json.loads(batch.read_text(encoding="utf-8")))
    if locale == "tr_tr":
        for p in sorted(ASSETS.glob("neoorigins_tr_*/lang/tr_tr.json")):
            merged.update(json.loads(p.read_text(encoding="utf-8")))
    return merged


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    en = fetch("en_us")
    summary = {"english_keys": len(en), "locales": {}}

    for locale in LOCALES:
        official = fetch(locale, allow_missing=True)
        existing = load_existing(locale)
        missing = {k: v for k, v in en.items() if k not in official}
        needed = {k: v for k, v in missing.items() if k not in existing}

        if locale == "tr_tr":
            # Turkish has no official 26.2 locale. The existing split fallback already
            # covers the 26.1-era keys; this delta contains only genuinely new 26.2 keys.
            delta = needed
        else:
            # Other new locales are official upstream on 26.2 but omit a subset of keys.
            # Reuse our audited 1.21.1 translations where possible and leave only the
            # newly missing entries for translation.
            delta = {k: existing.get(k, v) for k, v in missing.items()}

        (OUT / f"{locale}.json").write_text(
            json.dumps(delta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (TMP / f"{locale}.json").write_text(
            json.dumps(needed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        summary["locales"][locale] = {
            "official_keys": len(official),
            "missing_upstream_keys": len(missing),
            "existing_reused": len(set(missing) & set(existing)),
            "translation_needed": len(needed),
            "delta_keys": len(delta),
        }

    (TMP / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
