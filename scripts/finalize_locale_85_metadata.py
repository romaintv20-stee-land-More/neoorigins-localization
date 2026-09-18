#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_JSON = ROOT / "catalog.json"
README = ROOT / "README.md"
CATALOG_MD = ROOT / "CATALOG.md"

LOCALE = "gv_im"
DISPLAY_NAME = "Gaelg"
SOURCE_LOCALE = "go_fr"


def rewrite_locale_strings(value):
    """Clone Gallo metadata while changing only locale paths/namespaces."""
    if isinstance(value, dict):
        return {key: rewrite_locale_strings(item) for key, item in value.items()}
    if isinstance(value, list):
        return [rewrite_locale_strings(item) for item in value]
    if isinstance(value, str):
        if value == SOURCE_LOCALE:
            return LOCALE
        value = value.replace("neoorigins_go_", "neoorigins_gv_")
        value = re.sub(r"(?<=/)go_fr(?=\.json(?:$|[?#]))", LOCALE, value)
        value = re.sub(r"(?<=\\)go_fr(?=\.json(?:$|[?#]))", LOCALE, value)
        return value
    return value


def add_manx_from_gallo(node) -> int:
    added = 0

    def walk(value):
        nonlocal added
        if isinstance(value, dict):
            if SOURCE_LOCALE in value and isinstance(value[SOURCE_LOCALE], dict):
                if LOCALE in value:
                    raise SystemExit("Manx metadata already exists before locale 85 finalization")
                entry = rewrite_locale_strings(copy.deepcopy(value[SOURCE_LOCALE]))
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
            if key == "supported_locale_count" and value == 84:
                node[key] = 85
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


def assert_manx_entry_clean(value, project_id: str) -> None:
    if isinstance(value, dict):
        for item in value.values():
            assert_manx_entry_clean(item, project_id)
    elif isinstance(value, list):
        for item in value:
            assert_manx_entry_clean(item, project_id)
    elif isinstance(value, str):
        if "/go_fr.json" in value or "neoorigins_go_" in value:
            raise SystemExit(
                f"{project_id}: Gallo path/namespace leaked into Manx metadata: {value!r}"
            )


def main() -> None:
    catalog = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    project = catalog.get("project", {})
    if project.get("supported_locale_count") != 84:
        raise SystemExit(
            "Expected catalog supported_locale_count=84 before Manx finalization, "
            f"got {project.get('supported_locale_count')!r}"
        )

    added = add_manx_from_gallo(catalog)
    if added != 11:
        raise SystemExit(f"Expected 11 Manx catalog entries, got {added}")

    count_changes = update_supported_counts(catalog)
    if count_changes < 1:
        raise SystemExit("No supported_locale_count values were updated")

    neoorigins = next(
        item for item in catalog["supported_projects"] if item.get("id") == "neoorigins"
    )
    compatibility = neoorigins["compatibility"]
    fallbacks = compatibility["fallback_namespaces"]
    additions = {
        "manx_common_glob": "neoorigins_gv_common_*",
        "manx_mc_1_21_1": "neoorigins_gv_121",
    }
    for key, value in additions.items():
        if key in fallbacks:
            raise SystemExit(f"Fallback namespace key already exists: {key}")
        fallbacks[key] = value

    old_note = compatibility["coverage_note"]
    if "All 84 currently supported locales" not in old_note:
        raise SystemExit("Unexpected NeoOrigins coverage_note before locale 85 finalization")
    compatibility["coverage_note"] = old_note.replace(
        "All 84 currently supported locales",
        "All 85 currently supported locales",
    )

    CATALOG_JSON.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme = README.read_text(encoding="utf-8")
    readme = replace_exact(readme, "| 84 |", "| 85 |", expected=3)
    readme = replace_exact(
        readme,
        "**Gallo (`go_fr`)**.",
        "**Gallo (`go_fr`)** et **Mannois (`gv_im`)**.",
        expected=1,
    )
    readme = replace_exact(
        readme,
        "Les quatre-vingt-quatre langues sont disponibles",
        "Les quatre-vingt-cinq langues sont disponibles",
        expected=1,
    )
    gallo_block = (
        "Pour le gallo :\n\n"
        "- **1.21.1 : 2 296/2 296 clés** couvertes ;\n"
        "- **26.1.x : 2 307/2 307 clés** couvertes ;\n"
        "- **26.2 : 2 307/2 307 clés** couvertes."
    )
    manx_block = gallo_block + (
        "\n\nPour le mannois :\n\n"
        "- **1.21.1 : 2 296/2 296 clés** couvertes ;\n"
        "- **26.1.x : 2 307/2 307 clés** couvertes ;\n"
        "- **26.2 : 2 307/2 307 clés** couvertes."
    )
    readme = replace_exact(readme, gallo_block, manx_block, expected=1)
    README.write_text(readme, encoding="utf-8")

    catalog_md = CATALOG_MD.read_text(encoding="utf-8")
    catalog_md = replace_exact(
        catalog_md,
        "Galo (`go_fr`)",
        "Galo (`go_fr`) · Gaelg (`gv_im`)",
        expected=11,
    )
    CATALOG_MD.write_text(catalog_md, encoding="utf-8")

    final_catalog = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    if final_catalog["project"]["supported_locale_count"] != 85:
        raise SystemExit("Final supported_locale_count is not 85")
    for supported_project in final_catalog["supported_projects"]:
        languages = supported_project.get("languages")
        if languages is None:
            continue
        project_id = supported_project.get("id", "unknown")
        if LOCALE not in languages:
            raise SystemExit(f"{project_id}: missing {LOCALE} after metadata finalization")
        if languages[LOCALE].get("name") != DISPLAY_NAME:
            raise SystemExit(
                f"{project_id}: unexpected Manx display name {languages[LOCALE].get('name')!r}"
            )
        assert_manx_entry_clean(languages[LOCALE], project_id)

    print("Metadata finalization passed: 84 -> 85 locales; gv_im added to all 11 projects.")


if __name__ == "__main__":
    main()
