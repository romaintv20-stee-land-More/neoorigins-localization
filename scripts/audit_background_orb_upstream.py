#!/usr/bin/env python3
from pathlib import Path
import io
import json
import re
import time
import urllib.error
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "localization/background_orb_translations.json"
BACKGROUND_LANG = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets/origins_backgrounds/lang"
CONTEXT_PATH = "assets/neoorigins/lang/en_us.json"
JARS = (
    ("8875601", "Origins-Backgrounds-1.21.1-NeoOrigins-1.0.3.jar"),
    ("8875590", "Origins-More-Backgrounds-1.21.1-NeoOrigins-1.0.4.jar"),
)
EXPECTED_KEYS = {
    "item.neoorigins.purple_orb",
    "item.neoorigins.purple_orb.not_enough_xp",
    "jei.neoorigins.purple_orb.info",
    "emi.neoorigins.purple_orb.info",
}
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sd]")


def placeholders(value: str):
    return sorted(PLACEHOLDER_RE.findall(value))

def download_jar(file_id: str, filename: str, attempts: int = 4):
    a, b = file_id[:-3], file_id[-3:]
    urls = (
        f"https://edge.forgecdn.net/files/{a}/{b}/{filename}",
        f"https://mediafilez.forgecdn.net/files/{a}/{b}/{filename}",
    )
    last_error = None
    for attempt in range(1, attempts + 1):
        for url in urls:
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Localization-Audit"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = response.read()
                if data[:2] == b"PK":
                    return data
                last_error = RuntimeError(f"Downloaded content is not a JAR: {url}")
            except (urllib.error.URLError, urllib.error.HTTPError, ConnectionResetError, TimeoutError) as exc:
                last_error = exc
        if attempt != attempts:
            time.sleep(2 ** (attempt - 1))
    raise last_error


def read_context(jar_data: bytes):
    with zipfile.ZipFile(io.BytesIO(jar_data)) as jar:
        try:
            return json.loads(jar.read(CONTEXT_PATH).decode("utf-8"))
        except KeyError as exc:
            raise SystemExit(f"Missing {CONTEXT_PATH} in upstream JAR") from exc

def main():
    table = json.loads(TABLE.read_text(encoding="utf-8"))
    expected_locales = sorted(path.stem for path in BACKGROUND_LANG.glob("*.json"))
    if sorted(table) != expected_locales:
        missing = sorted(set(expected_locales) - set(table))
        extra = sorted(set(table) - set(expected_locales))
        raise SystemExit(f"Background Orb locale mismatch: missing={missing}, extra={extra}")
    if len(table) != 92:
        raise SystemExit(f"Expected 92 Background Orb locales, found {len(table)}")

    upstream = None
    for file_id, filename in JARS:
        current = read_context(download_jar(file_id, filename))
        if set(current) != EXPECTED_KEYS:
            raise SystemExit(f"Unexpected contextual keys in {filename}: {sorted(current)}")
        if upstream is None:
            upstream = current
        elif current != upstream:
            raise SystemExit("Backgrounds and More Backgrounds do not ship the same contextual English strings")

    errors = []
    for locale, values in sorted(table.items()):
        if set(values) != EXPECTED_KEYS:
            errors.append(f"{locale}: wrong key set")
            continue
        for key in EXPECTED_KEYS:
            value = values.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{locale}: empty {key}")
                continue
            if placeholders(value) != placeholders(upstream[key]):
                errors.append(f"{locale}: placeholder mismatch for {key}")
        if values["jei.neoorigins.purple_orb.info"] != values["emi.neoorigins.purple_orb.info"]:
            errors.append(f"{locale}: JEI/EMI descriptions differ")
        if re.search(r"(?<!\d)2(?!\d)", values["jei.neoorigins.purple_orb.info"]):
            errors.append(f"{locale}: stale cost 2 in contextual description")

    if errors:
        raise SystemExit("Background Orb audit failed:\n" + "\n".join(errors[:30]))
    print(f"Background Orb upstream audit passed: {len(table)} locales, {len(EXPECTED_KEYS)} keys each")


if __name__ == "__main__":
    main()
