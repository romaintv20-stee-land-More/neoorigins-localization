#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re
import time
import urllib.error
import urllib.request
import zipfile
import io

ROOT = Path(__file__).resolve().parents[1]
PACK_LANG = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets/origins_fantasy/lang"
LOCALES = ("fr_fr", "de_de", "es_es", "pt_br", "nl_nl", "it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn", "cs_cz")
DEFAULT_FILE_ID = "8816068"
DEFAULT_FILENAME = "Origins-Fantasy-1.21.1-NeoOrigins-1.1.3.jar"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sd]")


def placeholders(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def download_jar(file_id: str, filename: str, attempts: int = 4):
    a, b = file_id[:-3], file_id[-3:]
    urls = (
        f"https://edge.forgecdn.net/files/{a}/{b}/{filename}",
        f"https://mediafilez.forgecdn.net/files/{a}/{b}/{filename}",
        f"https://www.curseforge.com/minecraft/mc-mods/origins-fantsy-neoorigins/download/{file_id}/file",
    )
    last_error = None
    for attempt in range(1, attempts + 1):
        for url in urls:
            try:
                request = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "NeoOrigins-Localization-Audit",
                        "Referer": "https://www.curseforge.com/",
                        "Accept": "*/*",
                    },
                )
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = response.read()
                if data[:2] == b"PK":
                    return data, url
                last_error = RuntimeError(f"Downloaded content is not a JAR from {url}")
            except (urllib.error.URLError, urllib.error.HTTPError, ConnectionResetError, TimeoutError) as exc:
                last_error = exc
        if attempt != attempts:
            delay = 2 ** (attempt - 1)
            print(f"Transient Origins Fantasy download error ({attempt}/{attempts}): {last_error}; retrying in {delay}s")
            time.sleep(delay)
    raise last_error


def read_locale(jar: zipfile.ZipFile, locale: str):
    path = f"assets/origins_fantasy/lang/{locale}.json"
    try:
        return json.loads(jar.read(path).decode("utf-8"))
    except KeyError:
        return {}


def main():
    parser = argparse.ArgumentParser(description="Compare Origins Fantasy for NeoOrigins fallback locales with the pinned upstream CurseForge JAR.")
    parser.add_argument("--file-id", default=DEFAULT_FILE_ID, help="CurseForge file id")
    parser.add_argument("--filename", default=DEFAULT_FILENAME, help="Exact CurseForge JAR filename")
    parser.add_argument("--output", default=str(ROOT / "build/origins-fantasy-upstream-audit"))
    parser.add_argument("--prune", action="store_true", help="Remove fallback keys that now exist upstream")
    parser.add_argument("--fail-on-overlap", action="store_true")
    parser.add_argument("--fail-on-missing", action="store_true")
    parser.add_argument("--fail-on-placeholders", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    jar_data, source_url = download_jar(args.file_id, args.filename)

    with zipfile.ZipFile(io.BytesIO(jar_data)) as jar:
        en = read_locale(jar, "en_us")
        if not en:
            raise SystemExit("Origins Fantasy audit failed: upstream en_us.json is missing")
        official_locales = {locale: read_locale(jar, locale) for locale in LOCALES}

    report = {
        "upstream": "Origins Fantasy for NeoOrigins",
        "curseforge_project_id": 1587502,
        "curseforge_file_id": int(args.file_id),
        "filename": args.filename,
        "source_url": source_url,
        "english_keys": len(en),
        "locales": {},
    }
    any_overlap = any_missing = any_placeholder_error = False

    for locale in LOCALES:
        official = official_locales[locale]
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
                placeholder_errors.append({"key": key, "expected": expected, "actual": actual})

        if args.prune and path.exists() and overlap:
            fallback = {k: v for k, v in fallback.items() if k not in official}
            path.write_text(json.dumps(fallback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            overlap = []
            stale = sorted(set(fallback) - set(en))
            missing = sorted(set(missing_upstream) - set(fallback))

        any_overlap |= bool(overlap)
        any_missing |= bool(missing)
        any_placeholder_error |= bool(placeholder_errors)
        (out_dir / f"{locale}_missing_keys.json").write_text(json.dumps(missing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out_dir / f"{locale}_overlap.json").write_text(json.dumps(overlap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out_dir / f"{locale}_placeholder_errors.json").write_text(json.dumps(placeholder_errors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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

    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Origins Fantasy for NeoOrigins audit ({args.filename}, CurseForge file {args.file_id})")
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
        raise SystemExit("Origins Fantasy audit failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
