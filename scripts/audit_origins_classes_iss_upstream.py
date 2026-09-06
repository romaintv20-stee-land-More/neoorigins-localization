#!/usr/bin/env python3
from pathlib import Path
import argparse
import io
import json
import re
import time
import urllib.error
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
LOCALES = ("fr_fr", "de_de", "es_es", "pt_br", "nl_nl", "it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn")
DEFAULT_FILE_ID = "8592095"
DEFAULT_FILENAME = "Origins-Classes-ISS-1.21.1-NeoOrigins-1.0.1.jar"
DEFAULT_NAMESPACE = "origins_classes_iss"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sd]")


def placeholders(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def download_jar(file_id: str, filename: str, attempts: int = 4):
    a, b = file_id[:-3], file_id[-3:]
    urls = (
        f"https://edge.forgecdn.net/files/{a}/{b}/{filename}",
        f"https://mediafilez.forgecdn.net/files/{a}/{b}/{filename}",
        f"https://www.curseforge.com/minecraft/mc-mods/origins-classes-iss-for-neoorigins/download/{file_id}/file",
    )
    last_error = None
    for attempt in range(1, attempts + 1):
        for url in urls:
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Localization-Audit", "Referer": "https://www.curseforge.com/", "Accept": "*/*"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = response.read()
                if data[:2] == b"PK":
                    return data, url
                last_error = RuntimeError(f"Downloaded content is not a JAR from {url}")
            except (urllib.error.URLError, urllib.error.HTTPError, ConnectionResetError, TimeoutError) as exc:
                last_error = exc
        if attempt != attempts:
            delay = 2 ** (attempt - 1)
            print(f"Transient Origins Classes ISS download error ({attempt}/{attempts}): {last_error}; retrying in {delay}s")
            time.sleep(delay)
    raise last_error


def detect_namespace(jar: zipfile.ZipFile, preferred: str):
    names = set(jar.namelist())
    if f"assets/{preferred}/lang/en_us.json" in names:
        return preferred
    candidates = sorted(name.split("/")[1] for name in names if name.startswith("assets/") and name.endswith("/lang/en_us.json") and len(name.split("/")) == 4)
    if len(candidates) == 1:
        return candidates[0]
    raise SystemExit(f"Origins Classes ISS audit failed: could not uniquely detect localization namespace; candidates={candidates}")


def read_locale(jar: zipfile.ZipFile, namespace: str, locale: str):
    try:
        return json.loads(jar.read(f"assets/{namespace}/lang/{locale}.json").decode("utf-8"))
    except KeyError:
        return {}


def escape_annotation(value: str):
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def main():
    parser = argparse.ArgumentParser(description="Compare Origins: Classes ISS for NeoOrigins fallback locales with the pinned upstream CurseForge JAR.")
    parser.add_argument("--file-id", default=DEFAULT_FILE_ID)
    parser.add_argument("--filename", default=DEFAULT_FILENAME)
    parser.add_argument("--namespace", default=DEFAULT_NAMESPACE)
    parser.add_argument("--output", default=str(ROOT / "build/origins-classes-iss-upstream-audit"))
    parser.add_argument("--prune", action="store_true")
    parser.add_argument("--fail-on-overlap", action="store_true")
    parser.add_argument("--fail-on-missing", action="store_true")
    parser.add_argument("--fail-on-placeholders", action="store_true")
    parser.add_argument("--annotate-missing", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    jar_data, source_url = download_jar(args.file_id, args.filename)
    with zipfile.ZipFile(io.BytesIO(jar_data)) as jar:
        namespace = detect_namespace(jar, args.namespace)
        en = read_locale(jar, namespace, "en_us")
        if not en:
            raise SystemExit("Origins Classes ISS audit failed: upstream en_us.json is missing")
        official_locales = {locale: read_locale(jar, namespace, locale) for locale in LOCALES}

    (out_dir / "upstream_en_us.json").write_text(json.dumps(en, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pack_lang = PACK_ROOT / namespace / "lang"
    report = {
        "upstream": "Origins: Classes ISS for NeoOrigins",
        "curseforge_project_id": 1622039,
        "curseforge_file_id": int(args.file_id),
        "filename": args.filename,
        "namespace": namespace,
        "source_url": source_url,
        "english_keys": len(en),
        "locales": {},
    }
    any_overlap = any_missing = any_placeholder_error = False
    annotation_keys = set()

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
        if args.annotate_missing:
            for key in missing:
                if key not in annotation_keys:
                    annotation_keys.add(key)
                    print(f"::error title=Missing Origins Classes ISS translation::{escape_annotation(key + ' = ' + str(en.get(key, '')))}")

    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Origins: Classes ISS for NeoOrigins audit ({args.filename}, CurseForge file {args.file_id})")
    print(f"Namespace: {namespace} | English: {len(en)} keys")
    for locale, stats in report["locales"].items():
        print(f"{locale}: official={stats['official_keys']} | fallback={stats['fallback_keys']} | overlap={stats['fallback_overlap_with_official']} | missing={stats['missing_not_yet_in_fallback']} | placeholders={stats['placeholder_errors']}")

    failures = []
    if args.fail_on_overlap and any_overlap:
        failures.append("fallback overlap with upstream translations")
    if args.fail_on_missing and any_missing:
        failures.append("missing fallback translations")
    if args.fail_on_placeholders and any_placeholder_error:
        failures.append("placeholder mismatch")
    if failures:
        raise SystemExit("Origins Classes ISS audit failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
