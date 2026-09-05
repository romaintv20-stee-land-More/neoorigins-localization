#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PACK_LANG = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets/ibarnorigins/lang"
DEFAULT_REF = "multiloader-1.21.1-new-pack-format"
LOCALES = ("fr_fr", "de_de", "es_es", "pt_br", "nl_nl")
BASE = "https://raw.githubusercontent.com/ibarn-Recreational/ibarn-origins-addon/{ref}/common/src/main/resources/assets/ibarnorigins/lang/{locale}.json"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sd]")


def fetch_json(url: str, allow_missing: bool = False):
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if allow_missing and exc.code == 404:
            return {}
        raise


def placeholders(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def main():
    parser = argparse.ArgumentParser(description="Compare ibarn's quartet origins addon fallback locales with upstream language files.")
    parser.add_argument("--ref", default=DEFAULT_REF, help="Upstream branch/tag/commit")
    parser.add_argument("--output", default=str(ROOT / "build/ibarnorigins-upstream-audit"))
    parser.add_argument("--prune", action="store_true", help="Remove fallback keys that now exist upstream")
    parser.add_argument("--fail-on-overlap", action="store_true")
    parser.add_argument("--fail-on-missing", action="store_true")
    parser.add_argument("--fail-on-placeholders", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    en = fetch_json(BASE.format(ref=args.ref, locale="en_us"))
    report = {
        "upstream": "ibarn-Recreational/ibarn-origins-addon",
        "ref": args.ref,
        "english_keys": len(en),
        "locales": {},
    }

    any_overlap = False
    any_missing = False
    any_placeholder_error = False

    for locale in LOCALES:
        official = fetch_json(BASE.format(ref=args.ref, locale=locale), allow_missing=True)
        path = PACK_LANG / f"{locale}.json"
        fallback = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

        missing_upstream = {k: v for k, v in en.items() if k not in official}
        overlap = sorted(set(fallback) & set(official))
        stale = sorted(set(fallback) - set(en))
        missing = sorted(set(missing_upstream) - set(fallback))

        placeholder_errors = []
        for key in sorted(set(fallback) & set(en)):
            expected = placeholders(en[key])
            actual = placeholders(fallback[key])
            if expected != actual:
                placeholder_errors.append({
                    "key": key,
                    "expected": expected,
                    "actual": actual,
                })

        if args.prune and path.exists() and overlap:
            fallback = {k: v for k, v in fallback.items() if k not in official}
            path.write_text(json.dumps(fallback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            overlap = []
            stale = sorted(set(fallback) - set(en))
            missing = sorted(set(missing_upstream) - set(fallback))

        any_overlap |= bool(overlap)
        any_missing |= bool(missing)
        any_placeholder_error |= bool(placeholder_errors)

        (out_dir / f"{locale}_missing_keys.json").write_text(
            json.dumps(missing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_dir / f"{locale}_overlap.json").write_text(
            json.dumps(overlap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_dir / f"{locale}_placeholder_errors.json").write_text(
            json.dumps(placeholder_errors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        report["locales"][locale] = {
            "official_exists": bool(official),
            "official_keys": len(official),
            "missing_upstream_keys": len(missing_upstream),
            "fallback_keys": len(fallback),
            "fallback_overlap_with_official": len(overlap),
            "fallback_stale_keys": len(stale),
            "missing_not_yet_in_fallback": len(missing),
            "placeholder_errors": len(placeholder_errors),
        }

    (out_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"ibarn's quartet origins addon upstream audit ({args.ref})")
    print(f"English: {len(en)} keys")
    for locale, stats in report["locales"].items():
        print(
            f"{locale}: official={stats['official_keys']} | missing-upstream={stats['missing_upstream_keys']} | "
            f"fallback={stats['fallback_keys']} | overlap={stats['fallback_overlap_with_official']} | "
            f"not-yet-translated={stats['missing_not_yet_in_fallback']} | placeholders={stats['placeholder_errors']}"
        )

    failures = []
    if args.fail_on_overlap and any_overlap:
        failures.append("fallback overlap with upstream translations")
    if args.fail_on_missing and any_missing:
        failures.append("missing fallback translations")
    if args.fail_on_placeholders and any_placeholder_error:
        failures.append("placeholder mismatch")
    if failures:
        raise SystemExit("ibarn origins audit failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
