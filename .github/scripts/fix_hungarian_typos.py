from pathlib import Path

replacements = {
    "src/main/resources/resourcepacks/fallback_localizations/assets/neoorigins_hu_01/lang/hu_hu.json": {
        "Az eredeted nem képes érércet bányászni.": "Az eredeted nem képes érctelepeket egyszerre kibányászni.",
    },
    "src/main/resources/resourcepacks/fallback_localizations/assets/neoorigins_hu_03/lang/hu_hu.json": {
        "nettherit törmeléket": "netherit törmeléket",
    },
    "src/main/resources/resourcepacks/fallback_localizations/assets/neoorigins_hu_06/lang/hu_hu.json": {
        "Magnafürdő": "Magmafürdő",
    },
    "src/main/resources/resourcepacks/fallback_localizations/assets/neoorigins_hu_08/lang/hu_hu.json": {
        "Varázslásmesterység": "Varázslásmesterség",
    },
}

for file_name, mapping in replacements.items():
    path = Path(file_name)
    text = path.read_text(encoding="utf-8")
    for old, new in mapping.items():
        if text.count(old) != 1:
            raise SystemExit(f"Expected one occurrence of {old!r} in {file_name}, found {text.count(old)}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
