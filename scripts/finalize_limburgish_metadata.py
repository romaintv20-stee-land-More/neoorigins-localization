#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALE = "li_li"
NATIVE_NAME = "Limburgs"
FRENCH_NAME = "Limbourgeois"
TEMPLATE_LOCALE = "ksh"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_limburgish_catalog_entries(data: dict) -> int:
    ensured = 0

    def visit(node):
        nonlocal ensured
        if isinstance(node, dict):
            if TEMPLATE_LOCALE in node and isinstance(node[TEMPLATE_LOCALE], dict):
                template = copy.deepcopy(node[TEMPLATE_LOCALE])
                if template.get("status") == "supported" and ("targets" in template or "file" in template):
                    if LOCALE not in node:
                        node[LOCALE] = template

                    entry = node[LOCALE]
                    if not isinstance(entry, dict):
                        raise SystemExit("Existing Limburgish catalog entry is not a JSON object")

                    entry["name"] = NATIVE_NAME
                    if "file" in template:
                        expected_file = template["file"].replace(f"/{TEMPLATE_LOCALE}.json", f"/{LOCALE}.json")
                        entry["file"] = expected_file
                        source = ROOT / expected_file
                        if not source.is_file():
                            raise SystemExit(f"Missing Limburgish source file for catalog metadata: {source}")
                        payload = load_json(source)
                        if not isinstance(payload, dict):
                            raise SystemExit(f"Expected JSON object in {source}")
                        entry["fallback_keys"] = len(payload)

                    ensured += 1

            for value in list(node.values()):
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(data)
    return ensured


def finalize_catalog_json() -> None:
    path = ROOT / "catalog.json"
    data = load_json(path)
    if data["project"].get("supported_locale_count") != 90:
        raise SystemExit("Limburgish metadata finalization requires merged Kölsch locale 90 first")
    data["project"]["supported_locale_count"] = 91

    neo = next(project for project in data["supported_projects"] if project["id"] == "neoorigins")
    namespaces = neo["compatibility"]["fallback_namespaces"]
    namespaces["limburgish_common_glob"] = "neoorigins_li_common_*"
    namespaces["limburgish_mc_1_21_1"] = "neoorigins_li_121"

    ensured = ensure_limburgish_catalog_entries(data)
    if ensured != 11:
        raise SystemExit(f"Expected Limburgish metadata in 11 projects, ensured {ensured}")

    write_json(path, data)


def finalize_catalog_md() -> None:
    path = ROOT / "CATALOG.md"
    text = path.read_text(encoding="utf-8")
    marker = "Kölsch/Ripoarisch (`ksh`)"
    new_locale = f"{NATIVE_NAME} (`{LOCALE}`)"
    present = sum(1 for line in text.splitlines() if line.startswith("|") and new_locale in line)
    if present == 0:
        changed = 0
        lines = []
        for line in text.splitlines():
            if line.startswith("|") and marker in line:
                line = line.replace(f"{marker} |", f"{marker} · {new_locale} |")
                changed += 1
            lines.append(line)
        if changed != 11:
            raise SystemExit(f"Expected 11 CATALOG.md rows to gain Limburgish, changed {changed}")
        text = "\n".join(lines) + "\n"
    elif present != 11:
        raise SystemExit(f"Expected Limburgish in 11 CATALOG.md rows, found {present}")

    path.write_text(text, encoding="utf-8")


def finalize_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")

    text = text.replace("| Minecraft 1.21.1 | `0.9.0-beta+1.21.1` | 21 | 90 |", "| Minecraft 1.21.1 | `0.9.0-beta+1.21.1` | 21 | 91 |")
    text = text.replace("| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.9.0-beta+26.1` | 25 | 90 |", "| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.9.0-beta+26.1` | 25 | 91 |")
    text = text.replace("| Minecraft 26.2 | `0.9.0-beta+26.2` | 25 | 90 |", "| Minecraft 26.2 | `0.9.0-beta+26.2` | 25 | 91 |")

    if f"{FRENCH_NAME} (`{LOCALE}`)" not in text:
        old = " et **Kölsch (`ksh`)**."
        new = f" et **Kölsch (`ksh`)** et **{FRENCH_NAME} (`{LOCALE}`)**."
        if old not in text:
            raise SystemExit("Could not locate the end of the README language list after Kölsch")
        text = text.replace(old, new, 1)

    text = text.replace("Les quatre-vingt-dix langues sont disponibles", "Les quatre-vingt-onze langues sont disponibles")

    if "pour le limbourgeois :" not in text.casefold():
        kolsch_block = "Pour le kölsch :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes."
        if kolsch_block not in text:
            raise SystemExit("Could not locate the Kölsch coverage block")
        limburgish_block = kolsch_block + "\n\nPour le limbourgeois :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes."
        text = text.replace(kolsch_block, limburgish_block, 1)

    path.write_text(text, encoding="utf-8")


def main() -> None:
    finalize_catalog_json()
    finalize_catalog_md()
    finalize_readme()
    print("Limburgish metadata finalized: locale 91 / li_li / Limburgs")


if __name__ == "__main__":
    main()
