#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_JSON = ROOT / "catalog.json"
README = ROOT / "README.md"
CATALOG_MD = ROOT / "CATALOG.md"

LOCALE = "bar"
DISPLAY_NAME = "Boarisch"
SOURCE_LOCALE = "se_no"


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


def add_bavarian_from_northern_sami(node) -> int:
    added = 0

    def walk(value):
        nonlocal added
        if isinstance(value, dict):
            if SOURCE_LOCALE in value and isinstance(value[SOURCE_LOCALE], dict):
                if LOCALE in value:
                    raise SystemExit("Bavarian metadata already exists before locale 79 finalization")
                entry = rewrite_locale_strings(
                    copy.deepcopy(value[SOURCE_LOCALE]), SOURCE_LOCALE, LOCALE
                )
                entry["name"] = DISPLAY_NAME
                value[LOCALE] = entry
                added += 1
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
            if key == "supported_locale_count" and value == 78:
                node[key] = 79
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
    if project.get("supported_locale_count") != 78:
        raise SystemExit(
            "Expected catalog supported_locale_count=78 before Bavarian finalization, "
            f"got {project.get('supported_locale_count')!r}"
        )

    added = add_bavarian_from_northern_sami(catalog)
    if added != 11:
        raise SystemExit(f"Expected 11 Bavarian catalog entries, got {added}")

    count_changes = update_supported_counts(catalog)
    if count_changes < 1:
        raise SystemExit("No supported_locale_count values were updated")

    neoorigins = next(
        item for item in catalog["supported_projects"] if item.get("id") == "neoorigins"
    )
    compatibility = neoorigins["compatibility"]
    fallbacks = compatibility["fallback_namespaces"]
    additions = {
        "bavarian_common_glob": "neoorigins_bar_common_*",
        "bavarian_mc_1_21_1": "neoorigins_bar_121",
    }
    for key, value in additions.items():
        if key in fallbacks:
            raise SystemExit(f"Fallback namespace key already exists: {key}")
        fallbacks[key] = value

    old_note = compatibility["coverage_note"]
    if "All 78 currently supported locales" not in old_note:
        raise SystemExit("Unexpected NeoOrigins coverage_note before locale 79 finalization")
    compatibility["coverage_note"] = old_note.replace(
        "All 78 currently supported locales",
        "All 79 currently supported locales",
    )

    CATALOG_JSON.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme = README.read_text(encoding="utf-8")
    readme = replace_exact(readme, "| 78 |", "| 79 |", expected=3)
    readme = replace_exact(
        readme,
        "**Same du Nord (`se_no`)**.",
        "**Same du Nord (`se_no`)** et **Bavarois (`bar`)**.",
        expected=1,
    )
    readme = replace_exact(
        readme,
        "Les soixante-dix-huit langues sont disponibles",
        "Les soixante-dix-neuf langues sont disponibles",
        expected=1,
    )
    sami_block = (
        "Pour le same du Nord :\n\n"
        "- **1.21.1 : 2 296/2 296 clés** couvertes ;\n"
        "- **26.1.x : 2 307/2 307 clés** couvertes ;\n"
        "- **26.2 : 2 307/2 307 clés** couvertes."
    )
    bavarian_block = sami_block + (
        "\n\nPour le bavarois :\n\n"
        "- **1.21.1 : 2 296/2 296 clés** couvertes ;\n"
        "- **26.1.x : 2 307/2 307 clés** couvertes ;\n"
        "- **26.2 : 2 307/2 307 clés** couvertes."
    )
    readme = replace_exact(readme, sami_block, bavarian_block, expected=1)
    README.write_text(readme, encoding="utf-8")

    catalog_md = CATALOG_MD.read_text(encoding="utf-8")
    catalog_md = replace_exact(
        catalog_md,
        "Davvisámegiella (`se_no`)",
        "Davvisámegiella (`se_no`) · Boarisch (`bar`)",
        expected=11,
    )
    CATALOG_MD.write_text(catalog_md, encoding="utf-8")

    final_catalog = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    if final_catalog["project"]["supported_locale_count"] != 79:
        raise SystemExit("Final supported_locale_count is not 79")
    for supported_project in final_catalog["supported_projects"]:
        languages = supported_project.get("languages")
        if languages is None:
            continue
        if LOCALE not in languages:
            raise SystemExit(
                f"{supported_project.get('id')}: missing {LOCALE} after metadata finalization"
            )
        if languages[LOCALE].get("name") != DISPLAY_NAME:
            raise SystemExit(
                f"{supported_project.get('id')}: unexpected Bavarian display name "
                f"{languages[LOCALE].get('name')!r}"
            )

    print("Metadata finalization passed: 78 -> 79 locales; bar added to all 11 projects.")


if __name__ == "__main__":
    main()
