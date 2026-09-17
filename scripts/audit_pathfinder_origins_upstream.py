#!/usr/bin/env python3
from pathlib import Path
import argparse
import io
import json
import re
import urllib.error
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACK_LANG = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets/pathfinder_origins/lang"
LOCALES = (
    "fr_fr", "de_de", "es_es", "pt_br", "nl_nl", "it_it",
    "pl_pl", "ru_ru", "tr_tr", "zh_cn", "cs_cz", "hu_hu",
)
DEFAULT_VERSION_ID = "AePOxNR3"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sd]")


def placeholders(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def fetch_json(url: str):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "NeoOrigins-Localization/1.1.0 (GitHub audit)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def download_archive(version_id: str):
    metadata = fetch_json(f"https://api.modrinth.com/v2/version/{version_id}")
    files = metadata.get("files", [])
    if not files:
        raise SystemExit("Pathfinder Origins audit failed: Modrinth version has no files")
    selected = next((item for item in files if item.get("primary")), files[0])
    request = urllib.request.Request(
        selected["url"],
        headers={"User-Agent": "NeoOrigins-Localization/1.1.0 (GitHub audit)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = response.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        raise SystemExit(f"Pathfinder Origins download failed: {exc}") from exc
    if data[:2] != b"PK":
        raise SystemExit("Pathfinder Origins audit failed: downloaded file is not a ZIP/JAR")
    return data, metadata, selected


def collect_display_strings(archive: zipfile.ZipFile):
    values = set()
    occurrences = 0

    def walk(current):
        nonlocal occurrences
        if isinstance(current, dict):
            for key, value in current.items():
                if key in {"name", "description"} and isinstance(value, str):
                    values.add(value)
                    occurrences += 1
                else:
                    walk(value)
        elif isinstance(current, list):
            for value in current:
                walk(value)

    for name in archive.namelist():
        if not name.startswith("data/") or not name.endswith(".json"):
            continue
        try:
            payload = json.loads(archive.read(name).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        walk(payload)
    return values, occurrences


def load_locale(locale: str):
    path = PACK_LANG / f"{locale}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Audit Pathfinder Origins fallback locales against the pinned Modrinth archive.")
    parser.add_argument("--version-id", default=DEFAULT_VERSION_ID)
    parser.add_argument("--output", default=str(ROOT / "build/pathfinder-origins-upstream-audit"))
    parser.add_argument("--fail-on-missing", action="store_true")
    parser.add_argument("--fail-on-stale", action="store_true")
    parser.add_argument("--fail-on-placeholders", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    data, metadata, selected = download_archive(args.version_id)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        source_strings, occurrences = collect_display_strings(archive)

    report = {
        "project": "Pathfinder Origins",
        "version_id": args.version_id,
        "version_number": metadata.get("version_number"),
        "filename": selected.get("filename"),
        "unique_strings": len(source_strings),
        "occurrences": occurrences,
        "locales": {},
    }

    any_missing = any_stale = any_placeholder_error = False
    for locale in LOCALES:
        fallback = load_locale(locale)
        missing = sorted(source_strings - set(fallback))
        stale = sorted(set(fallback) - source_strings)
        placeholder_errors = []
        for key in sorted(source_strings & set(fallback)):
            expected = placeholders(key)
            actual = placeholders(fallback[key])
            if expected != actual:
                placeholder_errors.append({"key": key, "expected": expected, "actual": actual})

        any_missing |= bool(missing)
        any_stale |= bool(stale)
        any_placeholder_error |= bool(placeholder_errors)
        report["locales"][locale] = {
            "fallback_keys": len(fallback),
            "missing": len(missing),
            "stale": len(stale),
            "placeholder_errors": len(placeholder_errors),
        }
        (out_dir / f"{locale}_missing.json").write_text(json.dumps(missing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out_dir / f"{locale}_stale.json").write_text(json.dumps(stale, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out_dir / f"{locale}_placeholder_errors.json").write_text(json.dumps(placeholder_errors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Pathfinder Origins {report['version_number']}: {len(source_strings)} unique strings / {occurrences} occurrences")
    for locale, stats in report["locales"].items():
        print(f"{locale}: fallback={stats['fallback_keys']} missing={stats['missing']} stale={stats['stale']} placeholders={stats['placeholder_errors']}")

    failures = []
    if args.fail_on_missing and any_missing:
        failures.append("missing fallback translations")
    if args.fail_on_stale and any_stale:
        failures.append("stale fallback keys")
    if args.fail_on_placeholders and any_placeholder_error:
        failures.append("placeholder mismatch")
    if failures:
        raise SystemExit("Pathfinder Origins audit failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
