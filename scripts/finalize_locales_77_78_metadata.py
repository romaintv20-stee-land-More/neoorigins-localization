#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_JSON = ROOT / "catalog.json"
README = ROOT / "README.md"
CATALOG_MD = ROOT / "CATALOG.md"

LOCALES = {
    "zh_tw": "繁體中文",
    "se_no": "Davvisámegiella",
}


def rewrite_locale_strings(value, source_locale: str, target_locale: str):
    if isinstance(value, dict):
        return {
            key: rewrite_locale_strings(item, source_locale, target_locale)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [rewrite_locale_strings(item, source_locale, target_locale) for item in value]
    if isinstance(value, str):
        return value.replace(source_locale, target_locale)
    return value


def add_locales_from_tatar(node) -> dict[str, int]:
    added = {locale: 0 for locale in LOCALES}

    def walk(value):
        if isinstance(value, dict):
            if "tt_ru" in value and isinstance(value["tt_ru"], dict):
                template = value["tt_ru"]
                for locale, name in LOCALES.items():
                    if locale in value:
                        continue
                    entry = rewrite_locale_strings(copy.deepcopy(template), "tt_ru", locale)
                    entry["name"] = name
                    value[locale] = entry
                    added[locale] += 1
            for item in list(value.values()):
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(node)
    return added


def update_supported_counts(node) -> int:
    changed = 0
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "supported_locale_count" and value == 76:
                node[key] = 78
                changed += 1
            else:
                changed += update_supported_counts(value)
    elif isinstance(node, list):
        for item in node:
            changed += update_supported_counts(item)
    return changed


def replace_exact(text: str, old: str, new: str, expected: int | None = None) -> str:
    count = text.count(old)
    if expected is not None and count != expected:
        raise SystemExit(f"Expected {expected} occurrences of {old!r}, found {count}")
    if expected is None and count == 0:
        raise SystemExit(f"Missing expected text: {old!r}")
    return text.replace(old, new)


def main() -> None:
    catalog = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    project = catalog.get("project", {})
    if project.get("supported_locale_count") != 76:
        raise SystemExit(
            f"Expected catalog supported_locale_count=76 before finalization, got {project.get('supported_locale_count')!r}"
        )

    added = add_locales_from_tatar(catalog)
    if added != {"zh_tw": 11, "se_no": 11}:
        raise SystemExit(f"Expected 11 catalog entries for each new locale, got {added}")

    count_changes = update_supported_counts(catalog)
    if count_changes < 1:
        raise SystemExit("No supported_locale_count values were updated")

    neoorigins = next(
        project for project in catalog["supported_projects"] if project.get("id") == "neoorigins"
    )
    compatibility = neoorigins["compatibility"]
    fallbacks = compatibility["fallback_namespaces"]
    additions = {
        "traditional_chinese_common_glob": "neoorigins_zhtw_common_*",
        "traditional_chinese_mc_1_21_1": "neoorigins_zhtw_121",
        "northern_sami_common_glob": "neoorigins_se_common_*",
        "northern_sami_mc_1_21_1": "neoorigins_se_121",
    }
    for key, value in additions.items():
        if key in fallbacks:
            raise SystemExit(f"Fallback namespace key already exists: {key}")
        fallbacks[key] = value

    old_note = compatibility["coverage_note"]
    if "All 76 currently supported locales" not in old_note:
        raise SystemExit("Unexpected NeoOrigins coverage_note before locale 77/78 finalization")
    compatibility["coverage_note"] = old_note.replace(
        "All 76 currently supported locales",
        "All 78 currently supported locales",
    )

    CATALOG_JSON.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme = README.read_text(encoding="utf-8")
    readme = replace_exact(readme, "| 76 |", "| 78 |", expected=3)
    readme = replace_exact(
        readme,
        "**Tatar (`tt_ru`)**.",
        "**Tatar (`tt_ru`)**, **Chinois traditionnel (`zh_tw`)** et **Same du Nord (`se_no`)**.",
        expected=1,
    )
    readme = replace_exact(
        readme,
        "Les soixante-seize langues sont disponibles",
        "Les soixante-dix-huit langues sont disponibles",
        expected=1,
    )
    tatar_block = (
        "Pour le tatar :\n\n"
        "- **1.21.1 : 2 296/2 296 clés** couvertes ;\n"
        "- **26.1.x : 2 307/2 307 clés** couvertes ;\n"
        "- **26.2 : 2 307/2 307 clés** couvertes."
    )
    extra_blocks = tatar_block + (
        "\n\nPour le chinois traditionnel :\n\n"
        "- **1.21.1 : 2 296/2 296 clés** couvertes ;\n"
        "- **26.1.x : 2 307/2 307 clés** couvertes ;\n"
        "- **26.2 : 2 307/2 307 clés** couvertes.\n\n"
        "Pour le same du Nord :\n\n"
        "- **1.21.1 : 2 296/2 296 clés** couvertes ;\n"
        "- **26.1.x : 2 307/2 307 clés** couvertes ;\n"
        "- **26.2 : 2 307/2 307 clés** couvertes."
    )
    readme = replace_exact(readme, tatar_block, extra_blocks, expected=1)
    README.write_text(readme, encoding="utf-8")

    catalog_md = CATALOG_MD.read_text(encoding="utf-8")
    catalog_md = replace_exact(
        catalog_md,
        "Tatar (`tt_ru`)",
        "Tatar (`tt_ru`) · 繁體中文 (`zh_tw`) · Davvisámegiella (`se_no`)",
        expected=11,
    )
    CATALOG_MD.write_text(catalog_md, encoding="utf-8")

    # Final metadata sanity checks.
    final_catalog = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    if final_catalog["project"]["supported_locale_count"] != 78:
        raise SystemExit("Final supported_locale_count is not 78")
    for project in final_catalog["supported_projects"]:
        languages = project.get("languages")
        if languages is None:
            continue
        for locale in LOCALES:
            if locale not in languages:
                raise SystemExit(f"{project.get('id')}: missing {locale} after metadata finalization")

    print("Metadata finalization passed: 76 -> 78 locales; zh_tw and se_no added to all 11 projects.")


if __name__ == "__main__":
    main()
