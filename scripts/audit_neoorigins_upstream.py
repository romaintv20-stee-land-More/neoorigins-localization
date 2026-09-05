#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "src/main/resources/resourcepacks/fallback_localizations"
PACK_ASSETS = PACK / "assets"
PACK_LANG = PACK_ASSETS / "neoorigins/lang"
DEFAULT_REF = "v2.2.25"
LOCALES = ("fr_fr", "nl_nl", "es_es", "de_de", "pt_br")
BASE = "https://raw.githubusercontent.com/CyberDay1/NeoOrigins/{ref}/src/main/resources/assets/neoorigins/lang/{locale}.json"


def fetch_json(url: str, allow_missing: bool = False):
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if allow_missing and exc.code == 404:
            return {}
        raise


def fallback_paths(locale: str):
    paths = [PACK_LANG / f"{locale}.json"]
    if locale == "nl_nl":
        paths.extend(sorted(PACK_ASSETS.glob("neoorigins_nl_*/lang/nl_nl.json")))
    return [path for path in paths if path.exists()]


def load_fallback(locale: str):
    merged = {}
    owners = {}
    duplicates = []
    for path in fallback_paths(locale):
        data = json.loads(path.read_text(encoding="utf-8"))
        for key, value in data.items():
            if key in merged:
                duplicates.append((key, owners[key], path))
                continue
            merged[key] = value
            owners[key] = path
    if duplicates:
        details = ", ".join(
            f"{key} ({first.relative_to(ROOT)} / {second.relative_to(ROOT)})"
            for key, first, second in duplicates[:10]
        )
        raise SystemExit(f"Duplicate fallback keys across split locale files: {details}")
    return merged


def prune_locale(locale: str, official: dict):
    for path in fallback_paths(locale):
        data = json.loads(path.read_text(encoding="utf-8"))
        pruned = {key: value for key, value in data.items() if key not in official}
        if pruned != data:
            path.write_text(json.dumps(pruned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Compare NeoOrigins fallback locales with upstream language files.")
    parser.add_argument("--ref", default=DEFAULT_REF, help="Upstream NeoOrigins tag/branch/commit")
    parser.add_argument("--output", default=str(ROOT / "build/upstream-audit"))
    parser.add_argument("--prune", action="store_true", help="Remove fallback keys that now exist upstream")
    parser.add_argument("--fail-on-overlap", action="store_true", help="Fail when fallback contains keys already translated upstream")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    en = fetch_json(BASE.format(ref=args.ref, locale="en_us"))
    report = {
        "upstream": "CyberDay1/NeoOrigins",
        "ref": args.ref,
        "english_keys": len(en),
        "locales": {},
    }
    has_overlap = False

    for locale in LOCALES:
        official = fetch_json(BASE.format(ref=args.ref, locale=locale), allow_missing=True)
        fallback = load_fallback(locale)

        missing = {key: value for key, value in en.items() if key not in official}
        overlap = sorted(set(fallback) & set(official))
        stale = sorted(set(fallback) - set(en))
        untranslated = sorted(set(missing) - set(fallback))
        has_overlap |= bool(overlap)

        (out_dir / f"{locale}_missing_en.json").write_text(
            json.dumps(missing, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (out_dir / f"{locale}_overlap.json").write_text(
            json.dumps(overlap, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (out_dir / f"{locale}_untranslated_keys.json").write_text(
            json.dumps(untranslated, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        if args.prune and overlap:
            prune_locale(locale, official)
            fallback = load_fallback(locale)
            overlap = sorted(set(fallback) & set(official))
            stale = sorted(set(fallback) - set(en))
            untranslated = sorted(set(missing) - set(fallback))

        report["locales"][locale] = {
            "official_exists": bool(official),
            "official_keys": len(official),
            "missing_upstream_keys": len(missing),
            "fallback_keys": len(fallback),
            "fallback_files": len(fallback_paths(locale)),
            "fallback_overlap_with_official": len(overlap),
            "fallback_stale_keys": len(stale),
            "missing_not_yet_in_fallback": len(untranslated),
        }

    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"NeoOrigins upstream audit ({args.ref})")
    print(f"English: {len(en)} keys")
    for locale, stats in report["locales"].items():
        print(
            f"{locale}: official={stats['official_keys']} | missing={stats['missing_upstream_keys']} | "
            f"fallback={stats['fallback_keys']} ({stats['fallback_files']} file(s)) | "
            f"overlap={stats['fallback_overlap_with_official']} | "
            f"not-yet-translated={stats['missing_not_yet_in_fallback']}"
        )

    if args.fail_on_overlap and has_overlap:
        raise SystemExit("Fallback overlap detected: run this script with --prune, review the diff, then commit.")


if __name__ == "__main__":
    main()
