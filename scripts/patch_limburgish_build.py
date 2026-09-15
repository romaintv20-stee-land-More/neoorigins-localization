#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "build.gradle"


def insert_after_once(text: str, anchor: str, addition: str) -> str:
    if addition.strip() in text:
        return text
    if text.count(anchor) != 1:
        raise SystemExit(f"Expected exactly one Gradle anchor, found {text.count(anchor)}: {anchor!r}")
    return text.replace(anchor, anchor + addition, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    text = insert_after_once(
        text,
        "def includeKabyle121Translations = (project.findProperty('include_kabyle_121_translations') ?: defaultInclude121Translations.toString()).toBoolean()\n",
        "def includeLimburgish121Translations = (project.findProperty('include_limburgish_121_translations') ?: defaultInclude121Translations.toString()).toBoolean()\n",
    )
    text = insert_after_once(
        text,
        "    inputs.property 'include_kabyle_121_translations', includeKabyle121Translations\n",
        "    inputs.property 'include_limburgish_121_translations', includeLimburgish121Translations\n",
    )
    text = insert_after_once(
        text,
        "    if (!includeKabyle121Translations) {\n        exclude 'resourcepacks/fallback_localizations/assets/neoorigins_kab_121/**'\n    }\n",
        "\n    if (!includeLimburgish121Translations) {\n        exclude 'resourcepacks/fallback_localizations/assets/neoorigins_li_121/**'\n    }\n",
    )

    checks = [
        "include_limburgish_121_translations",
        "includeLimburgish121Translations",
        "neoorigins_li_121/**",
    ]
    for needle in checks:
        if needle not in text:
            raise SystemExit(f"Limburgish Gradle patch missing {needle!r}")

    PATH.write_text(text, encoding="utf-8")
    print("Limburgish Gradle packaging selector installed")


if __name__ == "__main__":
    main()
