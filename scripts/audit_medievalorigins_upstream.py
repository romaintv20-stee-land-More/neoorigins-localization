#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PACK_ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
PACK_LANG = PACK_ASSETS / "medievalorigins/lang"
DEFAULT_REF = "1.21.1-fabric"
LOCALES = ("fr_fr", "de_de", "es_es", "pt_br", "nl_nl", "it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn", "cs_cz")
BASE = "https://raw.githubusercontent.com/muon-rw/Medieval-Origins-Revival/{ref}/src/main/resources/assets/medievalorigins/lang/{locale}.json"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sd]")


def fetch_json(url: str, allow_missing: bool = False, attempts: int = 4):
    request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Localization-Audit"})
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if allow_missing and exc.code == 404:
                return {}
            last_error = exc
            if exc.code not in (408, 429, 500, 502, 503, 504) or attempt == attempts:
                raise
        except (urllib.error.URLError, ConnectionResetError, TimeoutError) as exc:
            last_error = exc
            if attempt == attempts:
                raise
        delay = 2 ** (attempt - 1)
        print(f"Transient upstream fetch error ({attempt}/{attempts}) for {url}: {last_error}; retrying in {delay}s")
        time.sleep(delay)
    raise last_error


def placeholders(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def fallback_paths(locale: str):
    paths = [PACK_LANG / f"{locale}.json"]
    paths.extend(sorted(PACK_ASSETS.glob(f"medievalorigins_*/lang/{locale}.json")))
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
            else:
                merged[key] = value
                owners[key] = path
    if duplicates:
        details = ", ".join(
            f"{key} ({first.relative_to(ROOT)} / {second.relative_to(ROOT)})"
            for key, first, second in duplicates[:10]
        )
        raise SystemExit(f"Duplicate Medieval Origins fallback keys: {details}")
    return merged


def prune_locale(locale: str, official: dict):
    for path in fallback_paths(locale):
        data = json.loads(path.read_text(encoding="utf-8"))
        pruned = {k: v for k, v in data.items() if k not in official}
        if pruned != data:
            path.write_text(json.dumps(pruned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Compare Medieval Origins Revival fallback locales with upstream language files.")
    parser.add_argument("--ref", default=DEFAULT_REF, help="Upstream branch/tag/commit")
    parser.add_argument("--output", default=str(ROOT / "build/medievalorigins-upstream-audit"))
    parser.add_argument("--prune", action="store_true", help="Remove fallback keys that now exist upstream")
    parser.add_argument("--fail-on-overlap", action="store_true")
    parser.add_argument("--fail-on-missing", action="store_true")
    parser.add_argument("--fail-on-placeholders", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    en = fetch_json(BASE.format(ref=args.ref, locale="en_us"))
    report = {
        "upstream": "muon-rw/Medieval-Origins-Revival",
        "ref": args.ref,
        "english_keys": len(en),
        "locales": {},
    }

    any_overlap = False
    any_missing = False
    any_placeholder_error = False

    for locale in LOCALES:
        official = fetch_json(BASE.format(ref=args.ref, locale=locale), allow_missing=True)
        fallback = load_fallback(locale)

        missing_upstream = {k: v for k, v in en.items() if k not in official}
        overlap = sorted(set(fallback) & set(official))
        stale = sorted(set(fallback) - set(en))
        missing = sorted(set(missing_upstream) - set(fallback))
        missing_en = {key: missing_upstream[key] for key in missing}

        placeholder_errors = []
        for key in sorted(set(fallback) & set(en)):
            expected = placeholders(en[key])
            actual = placeholders(fallback[key])
            if expected != actual:
                placeholder_errors.append({"key": key, "expected": expected, "actual": actual})

        if args.prune and overlap:
            prune_locale(locale, official)
            fallback = load_fallback(locale)
            overlap = sorted(set(fallback) & set(official))
            stale = sorted(set(fallback) - set(en))
            missing = sorted(set(missing_upstream) - set(fallback))
            missing_en = {key: missing_upstream[key] for key in missing}

        any_overlap |= bool(overlap)
        any_missing |= bool(missing)
        any_placeholder_error |= bool(placeholder_errors)

        (out_dir / f"{locale}_missing_keys.json").write_text(json.dumps(missing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out_dir / f"{locale}_missing_en.json").write_text(json.dumps(missing_en, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out_dir / f"{locale}_overlap.json").write_text(json.dumps(overlap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out_dir / f"{locale}_placeholder_errors.json").write_text(json.dumps(placeholder_errors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        report["locales"][locale] = {
            "official_exists": bool(official),
            "official_keys": len(official),
            "missing_upstream_keys": len(missing_upstream),
            "fallback_keys": len(fallback),
            "fallback_files": len(fallback_paths(locale)),
            "fallback_overlap_with_official": len(overlap),
            "fallback_stale_keys": len(stale),
            "missing_not_yet_in_fallback": len(missing),
            "placeholder_errors": len(placeholder_errors),
        }

    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Medieval Origins Revival upstream audit ({args.ref})")
    print(f"English: {len(en)} keys")
    for locale, stats in report["locales"].items():
        print(
            f"{locale}: official={stats['official_keys']} | missing-upstream={stats['missing_upstream_keys']} | "
            f"fallback={stats['fallback_keys']} ({stats['fallback_files']} file(s)) | overlap={stats['fallback_overlap_with_official']} | "
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
        raise SystemExit("Medieval Origins audit failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
