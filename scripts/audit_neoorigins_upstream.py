#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PACK_LANG = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets/neoorigins/lang"
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
        fallback_path = PACK_LANG / f"{locale}.json"
        fallback = json.loads(fallback_path.read_text(encoding="utf-8")) if fallback_path.exists() else {}

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

        if args.prune and fallback_path.exists() and overlap:
            pruned = {key: value for key, value in fallback.items() if key not in official}
            fallback_path.write_text(json.dumps(pruned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            fallback = pruned
            overlap = []

        report["locales"][locale] = {
            "official_exists": bool(official),
            "official_keys": len(official),
            "missing_upstream_keys": len(missing),
            "fallback_keys": len(fallback),
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
            f"fallback={stats['fallback_keys']} | overlap={stats['fallback_overlap_with_official']} | "
            f"not-yet-translated={stats['missing_not_yet_in_fallback']}"
        )

    if args.fail_on_overlap and has_overlap:
        raise SystemExit("Fallback overlap detected: run this script with --prune, review the diff, then commit.")


if __name__ == "__main__":
    main()
