#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALE = "kab_kab"
NATIVE_NAME = "Taqbaylit"
FRENCH_NAME = "Kabyle"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_kabyle_catalog_entries(data: dict) -> int:
    ensured = 0

    def visit(node):
        nonlocal ensured
        if isinstance(node, dict):
            if "isv" in node and isinstance(node["isv"], dict):
                template = copy.deepcopy(node["isv"])
                if template.get("status") == "supported" and ("targets" in template or "file" in template):
                    if LOCALE not in node:
                        node[LOCALE] = template

                    entry = node[LOCALE]
                    if not isinstance(entry, dict):
                        raise SystemExit("Existing Kabyle catalog entry is not a JSON object")

                    entry["name"] = NATIVE_NAME
                    if "file" in template:
                        expected_file = template["file"].replace("/isv.json", f"/{LOCALE}.json")
                        entry["file"] = expected_file
                        source = ROOT / expected_file
                        if not source.is_file():
                            raise SystemExit(f"Missing Kabyle source file for catalog metadata: {source}")
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
    data["project"]["supported_locale_count"] = 89

    neo = next(project for project in data["supported_projects"] if project["id"] == "neoorigins")
    namespaces = neo["compatibility"]["fallback_namespaces"]
    namespaces["kabyle_common_glob"] = "neoorigins_kab_common_*"
    namespaces["kabyle_mc_1_21_1"] = "neoorigins_kab_121"

    ensured = ensure_kabyle_catalog_entries(data)
    if ensured != 11:
        raise SystemExit(f"Expected Kabyle metadata in 11 projects, ensured {ensured}")

    write_json(path, data)


def finalize_catalog_md() -> None:
    path = ROOT / "CATALOG.md"
    text = path.read_text(encoding="utf-8")
    marker = "Medžuslovjansky (`isv`)"
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
            raise SystemExit(f"Expected 11 CATALOG.md rows to gain Kabyle, changed {changed}")
        text = "\n".join(lines) + "\n"
    elif present != 11:
        raise SystemExit(f"Expected Kabyle in 11 CATALOG.md rows, found {present}")

    path.write_text(text, encoding="utf-8")


def finalize_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")

    text = text.replace("| Minecraft 1.21.1 | `0.9.0-beta+1.21.1` | 21 | 88 |", "| Minecraft 1.21.1 | `0.9.0-beta+1.21.1` | 21 | 89 |")
    text = text.replace("| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.9.0-beta+26.1` | 25 | 88 |", "| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.9.0-beta+26.1` | 25 | 89 |")
    text = text.replace("| Minecraft 26.2 | `0.9.0-beta+26.2` | 25 | 88 |", "| Minecraft 26.2 | `0.9.0-beta+26.2` | 25 | 89 |")

    if f"{FRENCH_NAME} (`{LOCALE}`)" not in text:
        old = " et **Interslave (`isv`)**."
        new = f" et **Interslave (`isv`)** et **{FRENCH_NAME} (`{LOCALE}`)**."
        if old not in text:
            raise SystemExit("Could not locate the end of the README language list")
        text = text.replace(old, new, 1)

    text = text.replace("Les quatre-vingt-huit langues sont disponibles", "Les quatre-vingt-neuf langues sont disponibles")

    if "Pour le kabyle :" not in text:
        interslavic_block = "Pour l'interslave :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes."
        if interslavic_block not in text:
            raise SystemExit("Could not locate the Interslavic coverage block")
        kabyle_block = interslavic_block + "\n\nPour le kabyle :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes."
        text = text.replace(interslavic_block, kabyle_block, 1)

    path.write_text(text, encoding="utf-8")


def main() -> None:
    finalize_catalog_json()
    finalize_catalog_md()
    finalize_readme()
    print("Kabyle metadata finalized: locale 89 / kab_kab / Taqbaylit")


if __name__ == "__main__":
    main()
