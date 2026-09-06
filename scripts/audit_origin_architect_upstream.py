#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
LOCALES = ("fr_fr", "de_de", "es_es", "pt_br", "nl_nl", "it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn")
DEFAULT_REF = "f58a6261292942d4123c46ff221fbdade138a329"
DEFAULT_NAMESPACE = "originsmodernui"
RAW_BASE = "https://raw.githubusercontent.com/ReoTpak/origin-architect-modern-uI/{ref}/src/main/resources/assets/originsmodernui/lang/{locale}.json"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sd]")


def placeholders(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def fetch_locale(ref: str, locale: str):
    url = RAW_BASE.format(ref=ref, locale=locale)
    request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Localization-Audit"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8")), url
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {}, url
        raise


def main():
    parser = argparse.ArgumentParser(description="Audit Origin Architect fallback locales against the pinned upstream source.")
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--namespace", default=DEFAULT_NAMESPACE)
    parser.add_argument("--output", default=str(ROOT / "build/origin-architect-upstream-audit"))
    parser.add_argument("--fail-on-overlap", action="store_true")
    parser.add_argument("--fail-on-missing", action="store_true")
    parser.add_argument("--fail-on-placeholders", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    en, source_url = fetch_locale(args.ref, "en_us")
    if not en:
        raise SystemExit("Origin Architect audit failed: upstream en_us.json is missing")

    official_locales = {locale: fetch_locale(args.ref, locale)[0] for locale in LOCALES}
    pack_lang = PACK_ROOT / args.namespace / "lang"
    report = {"upstream": "Origin Architect", "source_ref": args.ref, "namespace": args.namespace, "source_url": source_url, "english_keys": len(en), "locales": {}}
    any_overlap = any_missing = any_placeholder_error = False

    for locale in LOCALES:
        official = official_locales[locale]
        path = pack_lang / f"{locale}.json"
        fallback = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        missing_upstream = {k: v for k, v in en.items() if k not in official}
        overlap = sorted(set(fallback) & set(official))
        stale = sorted(set(fallback) - set(en))
        missing = sorted(set(missing_upstream) - set(fallback))
        placeholder_errors = []
        for key in sorted(set(fallback) & set(en)):
            if placeholders(en[key]) != placeholders(fallback[key]):
                placeholder_errors.append(key)
        any_overlap |= bool(overlap)
        any_missing |= bool(missing)
        any_placeholder_error |= bool(placeholder_errors)
        report["locales"][locale] = {"official_keys": len(official), "fallback_keys": len(fallback), "overlap": len(overlap), "stale": len(stale), "missing": len(missing), "placeholder_errors": len(placeholder_errors)}

    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "upstream_en_us.json").write_text(json.dumps(en, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Origin Architect audit | English: {len(en)} keys | ref: {args.ref}")
    for locale, stats in report["locales"].items():
        print(f"{locale}: official={stats['official_keys']} fallback={stats['fallback_keys']} overlap={stats['overlap']} stale={stats['stale']} missing={stats['missing']} placeholders={stats['placeholder_errors']}")

    failures = []
    if args.fail_on_overlap and any_overlap:
        failures.append("fallback overlap with upstream translations")
    if args.fail_on_missing and any_missing:
        failures.append("missing fallback translations")
    if args.fail_on_placeholders and any_placeholder_error:
        failures.append("placeholder mismatch")
    if failures:
        raise SystemExit("Origin Architect audit failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
