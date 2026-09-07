#!/usr/bin/env python3
from pathlib import Path
import copy
import json
import re

ROOT = Path(__file__).resolve().parents[1]

AUDIT_SCRIPTS = [
    "scripts/audit_medievalorigins_upstream.py",
    "scripts/audit_ibarnorigins_upstream.py",
    "scripts/audit_origins_fantasy_upstream.py",
    "scripts/audit_origins_backgrounds_upstream.py",
    "scripts/audit_origins_more_backgrounds_upstream.py",
    "scripts/audit_origins_backgrounds_iss_upstream.py",
    "scripts/audit_origins_furries_upstream.py",
    "scripts/audit_origins_classes_extended_upstream.py",
    "scripts/audit_origins_classes_iss_upstream.py",
    "scripts/audit_origin_architect_upstream.py",
]

ADDON_COUNTS = {
    "Medieval Origins Revival": "401/401",
    "ibarn's quartet origins addon": "69/69",
    "Origins Fantasy for NeoOrigins": "240/240",
    "Origins: Backgrounds for NeoOrigins": "65/65",
    "Origins: More Backgrounds for NeoOrigins": "44/44",
    "Origins: Backgrounds ISS for NeoOrigins": "79/79",
    "Origins Furries for NeoOrigins": "117/117",
    "Origins: Classes Extended for NeoOrigins": "124/124",
    "Origins: Classes ISS for NeoOrigins": "99/99",
    "Origin Architect": "22/22",
}

FALLBACK_COUNTS = {
    "medievalorigins": 102,
    "ibarnorigins": 69,
    "origins_fantasy": 240,
    "origins_backgrounds": 65,
    "origins_backgrounds_two": 39,
    "origins_backgrounds_iss": 77,
    "origins_furries": 117,
    "origins_classes_ex": 124,
    "origins_classes_iss": 99,
    "originsmodernui": 22,
}


def update_audit_scripts():
    for rel in AUDIT_SCRIPTS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        match = re.search(r"LOCALES\s*=\s*\((.*?)\)", text, re.S)
        if not match:
            raise RuntimeError(f"LOCALES not found in {rel}")
        inner = match.group(1)
        if '"ko_kr"' not in inner:
            if '"ja_jp"' not in inner:
                raise RuntimeError(f"ja_jp not found in {rel}")
            new_inner = inner.replace('"ja_jp"', '"ja_jp", "ko_kr"', 1)
            text = text[:match.start(1)] + new_inner + text[match.end(1):]
            path.write_text(text, encoding="utf-8")


def update_readme():
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(\| (?:21|25) \| )13( \|)", r"\g<1>14\2", text)
    text = text.replace(
        "**Hongrois (`hu_hu`)** et **Japonais (`ja_jp`)**.",
        "**Hongrois (`hu_hu`)**, **Japonais (`ja_jp`)** et **Coréen (`ko_kr`)**.",
    )
    text = text.replace("Les treize langues", "Les quatorze langues")
    text = text.replace("Couverture CS / HU / JA", "Couverture CS / HU / JA / KO")

    out = []
    for line in text.splitlines():
        for project, count in ADDON_COUNTS.items():
            if line.startswith(f"| {project} |"):
                parts = line.split(" | ")
                if len(parts) >= 4 and parts[2].count(" · ") == 2:
                    parts[2] = parts[2] + f" · {count}"
                    line = " | ".join(parts)
                break
        out.append(line)
    text = "\n".join(out) + "\n"

    if "Pour le coréen :" not in text:
        korean = (
            "Pour le coréen :\n\n"
            "- **1.21.1 : 2 296/2 296 clés** couvertes ;\n"
            "- **26.1.x : 2 307/2 307 clés** couvertes ;\n"
            "- **26.2 : 2 307/2 307 clés** couvertes.\n\n"
        )
        text = text.replace("Sur 26.x, trois anciennes clés", korean + "Sur 26.x, trois anciennes clés")

    path.write_text(text, encoding="utf-8")


def update_catalog_md():
    path = ROOT / "CATALOG.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("日本語 (`ja_jp`) |", "日本語 (`ja_jp`) · 한국어 (`ko_kr`) |")
    text = text.replace("Les treize langues ciblées sont", "Les quatorze langues ciblées sont")
    text = text.replace("`hu_hu` et `ja_jp`.", "`hu_hu`, `ja_jp` et `ko_kr`.")
    if "NeoOrigins coréen couvre" not in text:
        anchor = "- NeoOrigins hongrois couvre **2 296/2 296** clés en 1.21.1, **2 307/2 307** en 26.1.x et **2 307/2 307** en 26.2. Les trois anciennes clés de récompense absentes des branches 26.x restent sans effet et sont signalées comme obsolètes par l'audit.\n"
        note = "- NeoOrigins coréen couvre **2 296/2 296** clés en 1.21.1, **2 307/2 307** en 26.1.x et **2 307/2 307** en 26.2.\n"
        text = text.replace(anchor, anchor + note)
    path.write_text(text, encoding="utf-8")


def replace_locale_strings(value):
    if isinstance(value, str):
        return value.replace("ja_jp", "ko_kr").replace("日本語", "한국어")
    if isinstance(value, list):
        return [replace_locale_strings(v) for v in value]
    if isinstance(value, dict):
        return {k: replace_locale_strings(v) for k, v in value.items()}
    return value


def update_catalog_json():
    path = ROOT / "catalog.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["project"]["supported_locale_count"] = 14

    for project in data["supported_projects"]:
        pid = project.get("id")
        langs = project.setdefault("languages", {})
        if "ko_kr" not in langs:
            if "ja_jp" not in langs:
                raise RuntimeError(f"ja_jp catalog template missing for {pid}")
            ko = replace_locale_strings(copy.deepcopy(langs["ja_jp"]))
            ko["name"] = "한국어"
            if pid == "medievalorigins":
                ko.pop("files_glob", None)
                ko["file"] = "src/main/resources/resourcepacks/fallback_localizations/assets/medievalorigins/lang/ko_kr.json"
                ko["official_keys"] = 305
                ko["fallback_keys"] = 102
            elif pid in FALLBACK_COUNTS:
                ko["fallback_keys"] = FALLBACK_COUNTS[pid]
            langs["ko_kr"] = ko

        compatibility = project.get("compatibility", {})
        for key, value in list(compatibility.items()):
            if isinstance(value, str):
                compatibility[key] = value.replace("treize", "quatorze")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_build_workflow():
    path = ROOT / ".github/workflows/build.yml"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "branches: [ main, release/0.8.0-japanese ]",
        "branches: [ main, release/0.8.0-japanese, release/0.8.0-korean ]",
    )
    text = re.sub(r"(audit_locales: '[^']*\bja_jp)(')", r"\1 ko_kr\2", text)

    if "Verify packaged Korean localizations" not in text:
        marker = "      - name: Upload JAR\n"
        korean_verify = r'''      - name: Verify packaged Korean localizations
        run: |
          JAR=$(find build/libs -type f -name '*.jar' ! -name '*-sources.jar' | head -n 1)
          test -n "$JAR"
          jar tf "$JAR" > build/jar-contents-ko-${{ matrix.target }}.txt
          KO_COUNT=$(grep -cE '(^|/)lang/ko_kr\.json$' build/jar-contents-ko-${{ matrix.target }}.txt || true)
          echo "Korean localization files in ${{ matrix.target }}: $KO_COUNT"
          test "$KO_COUNT" -gt 0

          ADDON_PATTERN='(^|/)assets/(medievalorigins|medievalorigins_[^/]*|ibarnorigins|origins_fantasy|origins_backgrounds|origins_backgrounds_two|origins_backgrounds_iss|origins_furries|origins_classes_ex|origins_classes_iss|originsmodernui)/'

          if [ "${{ matrix.include_addon_translations }}" = "true" ]; then
            grep -Eq '(^|/)assets/medievalorigins/lang/ko_kr\.json$' build/jar-contents-ko-${{ matrix.target }}.txt
            for ns in ibarnorigins origins_fantasy origins_backgrounds origins_backgrounds_two origins_backgrounds_iss origins_furries origins_classes_ex origins_classes_iss originsmodernui; do
              grep -Eq "(^|/)assets/$ns/lang/ko_kr.json$" build/jar-contents-ko-${{ matrix.target }}.txt
            done
            echo "Korean addon packaging verified for ${{ matrix.target }}."
          else
            if grep -Eq "$ADDON_PATTERN" build/jar-contents-ko-${{ matrix.target }}.txt; then
              echo "Unexpected 1.21.1 addon localization found in ${{ matrix.target }}"
              grep -E "$ADDON_PATTERN" build/jar-contents-ko-${{ matrix.target }}.txt | head -n 50
              exit 1
            fi
            echo "No 1.21.1 addon namespaces packaged in ${{ matrix.target }}."
          fi

'''
        if marker not in text:
            raise RuntimeError("Upload JAR marker not found in build.yml")
        text = text.replace(marker, korean_verify + marker, 1)

    path.write_text(text, encoding="utf-8")


def write_korean_audit_workflow():
    path = ROOT / ".github/workflows/audit-korean-bootstrap.yml"
    path.write_text(r'''name: Audit Korean NeoOrigins bootstrap

on:
  push:
    branches:
      - release/0.8.0-korean

jobs:
  audit:
    strategy:
      fail-fast: false
      matrix:
        include:
          - target: mc-1.21.1
            ref: '860ecdb24e723983e93004ea8ceb5de90ccf0d70'
            extra: 'neoorigins_121_batch1'
          - target: mc-26.1.x
            ref: '3c1c7365507679c836d3c14af5d4dd0654652e87'
            extra: 'neoorigins_26_1'
          - target: mc-26.2
            ref: '65864716a5a796fa1c51ec3e8a6d9640abebb4ca'
            extra: 'neoorigins_26_2'
    runs-on: ubuntu-latest
    name: Audit ${{ matrix.target }}
    steps:
      - uses: actions/checkout@v4
      - name: Audit Korean fallback coverage
        run: |
          python3 scripts/audit_neoorigins_upstream.py \
            --ref "${{ matrix.ref }}" \
            --output "build/ko-audit-${{ matrix.target }}" \
            --locale ko_kr \
            --extra-namespace neoorigins_226 \
            --extra-namespace "${{ matrix.extra }}" \
            --fail-on-overlap \
            --fail-on-missing
      - name: Print report
        run: cat "build/ko-audit-${{ matrix.target }}/report.json"
      - uses: actions/upload-artifact@v4
        with:
          name: korean-audit-${{ matrix.target }}
          path: build/ko-audit-${{ matrix.target }}
          if-no-files-found: error
''', encoding="utf-8")


def cleanup_temp_files():
    for rel in [
        "scripts/finish_korean_integration.py",
        ".github/workflows/finish-korean-integration.yml",
    ]:
        path = ROOT / rel
        if path.exists():
            path.unlink()


def main():
    update_audit_scripts()
    update_readme()
    update_catalog_md()
    update_catalog_json()
    update_build_workflow()
    write_korean_audit_workflow()
    cleanup_temp_files()
    print("Korean integration metadata prepared successfully.")


if __name__ == "__main__":
    main()
