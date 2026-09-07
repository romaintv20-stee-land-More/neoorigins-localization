#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".github/workflows/build.yml"
README = ROOT / "README.md"
CATALOG_MD = ROOT / "CATALOG.md"
CATALOG_JSON = ROOT / "catalog.json"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"


def update_build():
    text = BUILD.read_text(encoding="utf-8")

    locale_lines = re.findall(r"audit_locales: '[^']+'", text)
    if len(locale_lines) != 3:
        raise SystemExit(f"Expected 3 audit_locales entries, found {len(locale_lines)}")
    text = re.sub(
        r"audit_locales: '([^']*\bcs_cz)'",
        lambda m: m.group(0) if "hu_hu" in m.group(1).split() else f"audit_locales: '{m.group(1)} hu_hu'",
        text,
    )

    if "audit_hungarian_namespace_glob:" not in text:
        needle = "            audit_czech_namespace_glob: 'neoorigins_cs_*'"
        if text.count(needle) != 3:
            raise SystemExit(f"Expected 3 Czech matrix glob entries, found {text.count(needle)}")
        text = text.replace(
            needle,
            needle + "\n            audit_hungarian_namespace_glob: 'neoorigins_hu_*'",
        )

    if "matrix.audit_hungarian_namespace_glob" not in text:
        czech_block = '''          if [ -n "${{ matrix.audit_czech_namespace_glob }}" ]; then
            EXTRA_ARGS+=(--fallback-namespace-glob "${{ matrix.audit_czech_namespace_glob }}")
          fi'''
        if text.count(czech_block) != 1:
            raise SystemExit(f"Expected Czech shell block once, found {text.count(czech_block)}")
        hungarian_block = '''          if [ -n "${{ matrix.audit_hungarian_namespace_glob }}" ]; then
            EXTRA_ARGS+=(--fallback-namespace-glob "${{ matrix.audit_hungarian_namespace_glob }}")
          fi'''
        text = text.replace(czech_block, czech_block + "\n" + hungarian_block)

    for line in re.findall(r"audit_locales: '[^']+'", text):
        if "hu_hu" not in line:
            raise SystemExit(f"Hungarian missing from build locale line: {line}")
    if text.count("audit_hungarian_namespace_glob: 'neoorigins_hu_*'") != 3:
        raise SystemExit("Hungarian namespace glob not present in all 3 matrix entries")
    if text.count("matrix.audit_hungarian_namespace_glob") != 2:
        raise SystemExit("Hungarian namespace glob shell handling malformed")

    BUILD.write_text(text, encoding="utf-8")


def update_readme():
    text = README.read_text(encoding="utf-8")

    text = text.replace("| 21 | 11 |", "| 21 | 12 |")
    text = text.replace("| 25 | 11 |", "| 25 | 12 |")

    old_languages = "Turc (`tr_tr`), Chinois simplifié (`zh_cn`) et **Tchèque (`cs_cz`)**."
    new_languages = "Turc (`tr_tr`), Chinois simplifié (`zh_cn`), **Tchèque (`cs_cz`)** et **Hongrois (`hu_hu`)**."
    if old_languages in text:
        text = text.replace(old_languages, new_languages)
    elif "Hongrois (`hu_hu`)" not in text:
        raise SystemExit("Could not find README language sentence to add Hungarian")

    text = text.replace("Les onze langues sont disponibles", "Les douze langues sont disponibles")

    czech_block = '''Pour le tchèque :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.'''
    hungarian_block = '''Pour le hongrois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.'''
    if hungarian_block not in text:
        if czech_block not in text:
            raise SystemExit("Could not find Czech coverage block in README")
        text = text.replace(czech_block, czech_block + "\n\n" + hungarian_block)

    text = text.replace("| Projet | Version/référence | Couverture tchèque | Couverture effective par langue |", "| Projet | Version/référence | Couverture CS / HU | Couverture effective par langue |")

    lines = text.splitlines()
    in_projects = False
    transformed = 0
    for i, line in enumerate(lines):
        if line == "## Projets pris en charge sur Minecraft 1.21.1":
            in_projects = True
            continue
        if in_projects and line.startswith("## "):
            in_projects = False
        if in_projects and line.startswith("| ") and not line.startswith("| Projet ") and not line.startswith("|---"):
            parts = line.split("|")
            # ['', project, version, coverage, effective, '']
            if len(parts) >= 6:
                coverage = parts[3].strip()
                if " · " not in coverage:
                    parts[3] = f" {coverage} · {coverage} "
                    lines[i] = "|".join(parts)
                    transformed += 1
    if transformed not in (0, 10):
        raise SystemExit(f"Expected to update 10 README project rows or 0 if already done, updated {transformed}")
    text = "\n".join(lines) + "\n"

    if "| 11 |" in text:
        raise SystemExit("README still contains a build language count of 11")
    if "Les onze langues" in text:
        raise SystemExit("README still says eleven languages")

    README.write_text(text, encoding="utf-8")


def update_catalog_md():
    text = CATALOG_MD.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed_rows = 0
    in_table = False
    for i, line in enumerate(lines):
        if line == "## Projets et langues":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            in_table = False
        if in_table and line.startswith("| [") and "`hu_hu`" not in line:
            if not line.endswith(" |"):
                raise SystemExit(f"Unexpected CATALOG row format: {line[:80]}")
            lines[i] = line[:-2] + " · Magyar (`hu_hu`) |"
            changed_rows += 1
    if changed_rows not in (0, 11):
        raise SystemExit(f"Expected to update 11 CATALOG project rows or 0 if already done, updated {changed_rows}")
    text = "\n".join(lines) + "\n"

    old_note = "- Les onze langues ciblées sont : `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr`, `zh_cn` et `cs_cz`."
    new_note = "- Les douze langues ciblées sont : `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr`, `zh_cn`, `cs_cz` et `hu_hu`."
    if old_note in text:
        text = text.replace(old_note, new_note)
    elif new_note not in text:
        raise SystemExit("Could not find CATALOG language count note")

    czech_note = "- NeoOrigins tchèque couvre **2 296/2 296** clés en 1.21.1, **2 307/2 307** en 26.1.x et **2 307/2 307** en 26.2. Les trois anciennes clés de récompense absentes des branches 26.x restent sans effet et sont signalées comme obsolètes par l'audit."
    hu_note = "- NeoOrigins hongrois couvre **2 296/2 296** clés en 1.21.1, **2 307/2 307** en 26.1.x et **2 307/2 307** en 26.2. Les trois anciennes clés de récompense absentes des branches 26.x restent sans effet et sont signalées comme obsolètes par l'audit."
    if hu_note not in text:
        if czech_note not in text:
            raise SystemExit("Could not find Czech CATALOG coverage note")
        text = text.replace(czech_note, czech_note + "\n" + hu_note)

    if "Les onze langues" in text:
        raise SystemExit("CATALOG.md still says eleven languages")
    CATALOG_MD.write_text(text, encoding="utf-8")


def replace_strings(value):
    if isinstance(value, str):
        return value.replace("onze langues", "douze langues")
    if isinstance(value, list):
        return [replace_strings(v) for v in value]
    if isinstance(value, dict):
        return {k: replace_strings(v) for k, v in value.items()}
    return value


def update_catalog_json():
    data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    data = replace_strings(data)
    data["project"]["supported_locale_count"] = 12

    projects = data.get("supported_projects", [])
    if len(projects) != 11:
        raise SystemExit(f"Expected 11 supported projects, found {len(projects)}")

    for project in projects:
        languages = project.setdefault("languages", {})
        if project["id"] == "neoorigins":
            languages["hu_hu"] = {
                "name": "Magyar",
                "status": "supported",
                "targets": ["1.21.1", "26.1.x", "26.2"],
            }
        else:
            entry = {"name": "Magyar", "status": "supported"}
            namespace = project.get("namespace")
            if namespace:
                rel = Path("src/main/resources/resourcepacks/fallback_localizations/assets") / namespace / "lang/hu_hu.json"
                if (ROOT / rel).exists():
                    entry["file"] = rel.as_posix()
            languages["hu_hu"] = entry

    for project in projects:
        if "hu_hu" not in project.get("languages", {}):
            raise SystemExit(f"Missing Hungarian catalog entry for {project['id']}")
        rel = project["languages"]["hu_hu"].get("file")
        if rel and not (ROOT / rel).exists():
            raise SystemExit(f"Catalog Hungarian file does not exist: {rel}")

    CATALOG_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    update_build()
    update_readme()
    update_catalog_md()
    update_catalog_json()
    print("Hungarian integration finalized in build.yml, README.md, CATALOG.md and catalog.json")


if __name__ == "__main__":
    main()
