#!/usr/bin/env python3
"""Generate Serbian Latin (sr_cs) fallback files from the audited Serbian Cyrillic locale.

Minecraft exposes Serbian Cyrillic (sr_sp) and Serbian Latin (sr_cs) as separate
script variants. Serbian Latin is therefore derived by deterministic Serbian
Cyrillic -> Latin transliteration, while upstream discovery reports decide which
keys still need fallback coverage on each NeoOrigins target.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

CYR_TO_LAT = {
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Ђ": "Đ",
    "Е": "E", "Ж": "Ž", "З": "Z", "И": "I", "Ј": "J", "К": "K",
    "Л": "L", "Љ": "Lj", "М": "M", "Н": "N", "Њ": "Nj", "О": "O",
    "П": "P", "Р": "R", "С": "S", "Т": "T", "Ћ": "Ć", "У": "U",
    "Ф": "F", "Х": "H", "Ц": "C", "Ч": "Č", "Џ": "Dž", "Ш": "Š",
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ђ": "đ",
    "е": "e", "ж": "ž", "з": "z", "и": "i", "ј": "j", "к": "k",
    "л": "l", "љ": "lj", "м": "m", "н": "n", "њ": "nj", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "ћ": "ć", "у": "u",
    "ф": "f", "х": "h", "ц": "c", "ч": "č", "џ": "dž", "ш": "š",
}

TARGETS = {
    "mc-1.21.1": {
        "discovery": ROOT / "build/sr-latn-discovery-mc-1.21.1/sr_cs_missing_en.json",
        "source_extra": ASSETS / "neoorigins_sr_121/lang/sr_sp.json",
        "output_extra": ASSETS / "neoorigins_sr_121/lang/sr_cs.json",
    },
    "mc-26.1": {
        "discovery": ROOT / "build/sr-latn-discovery-mc-26.1/sr_cs_missing_en.json",
        "source_extra": ASSETS / "neoorigins_26_1/lang/sr_sp.json",
        "output_extra": ASSETS / "neoorigins_26_1/lang/sr_cs.json",
    },
    "mc-26.2": {
        "discovery": ROOT / "build/sr-latn-discovery-mc-26.2/sr_cs_missing_en.json",
        "source_extra": ASSETS / "neoorigins_26_2/lang/sr_sp.json",
        "output_extra": ASSETS / "neoorigins_26_2/lang/sr_cs.json",
    },
}

ADDON_NAMESPACES = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]


def read_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Required source file missing: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def transliterate(text: str) -> str:
    return "".join(CYR_TO_LAT.get(char, char) for char in text)


def transliterate_dict(data: dict) -> dict:
    return {key: transliterate(str(value)) for key, value in data.items()}


def load_common_sources():
    paths = sorted(ASSETS.glob("neoorigins_sr_common_*/lang/sr_sp.json"))
    if len(paths) != 16:
        raise SystemExit(f"Expected 16 Serbian Cyrillic common chunks, found {len(paths)}")
    return paths


def merged_source(common_paths, extra_path):
    merged = {}
    for path in [*common_paths, extra_path]:
        for key, value in read_json(path).items():
            if key in merged:
                raise SystemExit(f"Duplicate Serbian source key {key} while reading {path.relative_to(ROOT)}")
            merged[key] = transliterate(str(value))
    return merged


def main():
    common_paths = load_common_sources()
    missing_sets = {}
    target_sources = {}

    for target, cfg in TARGETS.items():
        missing = read_json(cfg["discovery"])
        missing_sets[target] = set(missing)
        target_sources[target] = merged_source(common_paths, cfg["source_extra"])
        absent_source = sorted(missing_sets[target] - set(target_sources[target]))
        if absent_source:
            raise SystemExit(f"{target}: {len(absent_source)} upstream-missing keys absent from sr_sp source: {absent_source[:5]}")

    # A key may live in a shared namespace only when every target still needs it.
    common_missing = set.intersection(*(missing_sets[target] for target in TARGETS))
    written_common = set()
    for source_path in common_paths:
        source_data = read_json(source_path)
        out = {
            key: transliterate(str(value))
            for key, value in source_data.items()
            if key in common_missing
        }
        output_path = source_path.with_name("sr_cs.json")
        write_json(output_path, out)
        written_common.update(out)

    # Any target-only need (including a common key translated officially on a
    # different target) is kept in that target's delta namespace.
    for target, cfg in TARGETS.items():
        source = target_sources[target]
        needed = missing_sets[target] - written_common
        out = {key: source[key] for key in source if key in needed}
        write_json(cfg["output_extra"], out)
        if set(out) != needed:
            missing = sorted(needed - set(out))
            raise SystemExit(f"{target}: failed to write {len(missing)} needed keys: {missing[:5]}")
        print(f"{target}: {len(written_common)} shared + {len(out)} target-specific sr_cs fallback keys")

    # Add-ons share the same wording as the already audited Serbian Cyrillic
    # translation; upstream-priority pruning is performed by the workflow after
    # generation, so this step intentionally starts from the complete sr_sp file.
    addon_files = 0
    addon_keys = 0
    for namespace in ADDON_NAMESPACES:
        source_path = ASSETS / namespace / "lang/sr_sp.json"
        if not source_path.exists():
            print(f"{namespace}: no sr_sp fallback file; skipping sr_cs derivation")
            continue
        out = transliterate_dict(read_json(source_path))
        write_json(source_path.with_name("sr_cs.json"), out)
        addon_files += 1
        addon_keys += len(out)

    latin_values = []
    for path in ASSETS.glob("**/lang/sr_cs.json"):
        latin_values.extend(str(value) for value in read_json(path).values())
    leftover_serbian_cyrillic = sum(
        sum(1 for char in value if char in CYR_TO_LAT)
        for value in latin_values
    )
    if leftover_serbian_cyrillic:
        raise SystemExit(f"Serbian Latin transliteration left {leftover_serbian_cyrillic} Serbian Cyrillic letters")

    print(f"Serbian Latin generated from sr_sp: {addon_files} add-on files / {addon_keys} physical add-on strings")
    print(f"Serbian Latin script sanity: 0 Serbian Cyrillic letters left across generated sr_cs values")


if __name__ == "__main__":
    main()
