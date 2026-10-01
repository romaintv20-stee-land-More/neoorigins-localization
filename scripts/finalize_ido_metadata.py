#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALE = "io_en"
NATIVE_NAME = "Ido"
FRENCH_NAME = "Ido"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_ido_catalog_entries(data: dict) -> int:
    added = 0

    def visit(node):
        nonlocal added
        if isinstance(node, dict):
            if "haw_us" in node and LOCALE not in node and isinstance(node["haw_us"], dict):
                template = copy.deepcopy(node["haw_us"])
                if template.get("status") == "supported" and ("targets" in template or "file" in template):
                    template["name"] = NATIVE_NAME
                    if "file" in template:
                        template["file"] = template["file"].replace("/haw_us.json", f"/{LOCALE}.json")
                        source = ROOT / template["file"]
                        if not source.is_file():
                            raise SystemExit(f"Missing Ido source file for catalog metadata: {source}")
                        payload = load_json(source)
                        if not isinstance(payload, dict):
                            raise SystemExit(f"Expected JSON object in {source}")
                        template["fallback_keys"] = len(payload)
                    node[LOCALE] = template
                    added += 1
            for value in list(node.values()):
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(data)
    return added


def finalize_catalog_json() -> None:
    path = ROOT / "catalog.json"
    data = load_json(path)
    data["project"]["supported_locale_count"] = 87

    neo = next(project for project in data["supported_projects"] if project["id"] == "neoorigins")
    namespaces = neo["compatibility"]["fallback_namespaces"]
    namespaces["ido_common_glob"] = "neoorigins_io_common_*"
    namespaces["ido_mc_1_21_1"] = "neoorigins_io_121"

    added = add_ido_catalog_entries(data)
    if added != 11:
        raise SystemExit(f"Expected to add Ido metadata to 11 projects, added {added}")

    write_json(path, data)


def finalize_catalog_md() -> None:
    path = ROOT / "CATALOG.md"
    text = path.read_text(encoding="utf-8")
    marker = "ʻŌlelo Hawaiʻi (`haw_us`)"
    ido = f"{NATIVE_NAME} (`{LOCALE}`)"
    changed = 0
    lines = []
    for line in text.splitlines():
        if line.startswith("|") and marker in line and ido not in line:
            line = line.replace(f"{marker} |", f"{marker} · {ido} |")
            changed += 1
        lines.append(line)
    if changed != 11:
        raise SystemExit(f"Expected 11 CATALOG.md rows to gain Ido, changed {changed}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def finalize_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")

    text = text.replace("| Minecraft 1.21.1 | `0.9.0-beta+1.21.1` | 21 | 86 |", "| Minecraft 1.21.1 | `0.9.0-beta+1.21.1` | 21 | 87 |")
    text = text.replace("| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.9.0-beta+26.1` | 25 | 86 |", "| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.9.0-beta+26.1` | 25 | 87 |")
    text = text.replace("| Minecraft 26.2 | `0.9.0-beta+26.2` | 25 | 86 |", "| Minecraft 26.2 | `0.9.0-beta+26.2` | 25 | 87 |")

    if f"{FRENCH_NAME} (`{LOCALE}`)" not in text:
        old = " et **Hawaïen (`haw_us`)**."
        new = f" et **Hawaïen (`haw_us`)** et **{FRENCH_NAME} (`{LOCALE}`)**."
        if old not in text:
            raise SystemExit("Could not locate the end of the README language list")
        text = text.replace(old, new, 1)

    text = text.replace("Les quatre-vingt-six langues sont disponibles", "Les quatre-vingt-sept langues sont disponibles")

    if "Pour l'ido :" not in text:
        hawaiian_block = "Pour l'hawaïen :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes."
        if hawaiian_block not in text:
            raise SystemExit("Could not locate the Hawaiian coverage block")
        ido_block = hawaiian_block + "\n\nPour l'ido :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes."
        text = text.replace(hawaiian_block, ido_block, 1)

    path.write_text(text, encoding="utf-8")


def main() -> None:
    finalize_catalog_json()
    finalize_catalog_md()
    finalize_readme()
    print("Ido metadata finalized: locale 87 / io_en / Ido")


if __name__ == "__main__":
    main()
