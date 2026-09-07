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


def main():
    update_audit_scripts()
    update_readme()
    update_catalog_md()
    update_catalog_json()
    Path(__file__).unlink()
    print("Non-workflow Korean metadata prepared successfully.")


if __name__ == "__main__":
    main()
