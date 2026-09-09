#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
FILES = sorted(ASSETS.glob("**/lang/fo_fo.json"))
if not FILES:
    raise SystemExit("No Faroese fo_fo files found")

KEY_OVERRIDES = {
    # Core NeoOrigins UI / canonical product terminology.
    "neoorigins.toggle.on": "Førleiki virkin",
    "neoorigins.toggle.off": "Førleiki óvirkin",
    "neoorigins.ultimine.no_power": "Tín Origin hevur ikki Ultimine-førleikan.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Flokkur",
    "screen.neoorigins.choose_origin": "Vel tín Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Vel tín Origin",
    "gui.neoorigins.search.label": "Leita eftir Origin",
    "gui.neoorigins.detail.powers_header": "Førleikar",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.view_info": "Vís Origin-upplýsingar",
    "key.neoorigins.open_creator": "Opna Origin Creator",
    "key.neoorigins.open_mob_creator": "Opna Mob Origin Creator",
    "key.category.neoorigins.hotkeys": "NeoOrigins (Snarlyklar)",
    "screen.neoorigins.origin_info": "Origin-upplýsingar",
    "gui.neoorigins.info.no_origin": "Eingin Origin er valdur enn.",
    "gui.neoorigins.info.your_origin": "Tín Origin",
    "screen.neoorigins.origin_editor": "Origin-ritstjóri",
    "gui.neoorigins.editor.layers_header": "Origin-løg",
    "gui.neoorigins.editor.powers_header": "Førleikar",
    "screen.neoorigins.creator": "Origin Creator",
    "gui.neoorigins.creator.tab.powers": "Førleikar",
    "gui.neoorigins.creator.apply": "Nýt",
    "screen.neoorigins.mob_creator": "Mob Origin Creator",
    "gui.neoorigins.mob_creator.tab.powers": "Førleikar",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Reglur fyri framkalling",
    "gui.neoorigins.mob_creator.tab.drops": "Úrtøka",
    "gui.neoorigins.mob_creator.apply": "Nýt",

    # Canonical Origin names: these are identities/proper names, not prose.
    "origins.neoorigins.human.name": "Human",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    # Minecraft terminology / contextual false friends.
    "power.neoorigins.blazeling_nether_born.name": "Nether-føddur",
    "power.origins_furries.charge.name": "Skundálop",
    "power.origins_furries.chicken_xp.name": "Royndarstig frá høsnum",
    "power.origins_furries.pavlov.name": "Pavlovs refleks",
    "power.origins_furries.raccoon.name": "Vaskabjørn",
    "power.origins_furries.scales.name": "Skøl",
    "power.origins_furries.night_vision.name": "Náttarsjón",

    # Origin Architect is a product name and should not become generic architecture.
    "screen.originsmodernui.title": "Vel tín Origin",
    "screen.originsmodernui.search_hint": "Leita eftir Origin...",
    "screen.originsmodernui.choose_prompt": "Vel ein Origin á listanum",
    "key.originsmodernui.toggle_hud": "Skift Origin Architect HUD",
    "originsmodernui.config.hud.show_level": "Vís Origin Architect-stig",
    "originsmodernui.config.hud.show_points": "Vís óbrúkt stat-stig",
    "originsmodernui.config.hud.show_xp_popup": "Vís XP-vinning",
    "originsmodernui.config.hud.show_level_popup": "Vís stig-upp fráboðan",
}

# Exact value replacements for repeated machine-translation false friends.
VALUE_REPLACEMENTS = {
    "Vald": "Førleikar",
    "Pavlað": "Pavlovs refleks",
    "Vektir": "Skøl",
}

# Known terminology replacements. Use word-aware patterns where possible so normal
# Faroese prose is not damaged. Minecraft's current Faroese locale uses Nether- and
# Netheritt- terminology.
TEXT_REPLACEMENTS = [
    (re.compile(r"\bNeteritt\b"), "Netheritt"),
    (re.compile(r"\bNeterit\b"), "Netheritt"),
    (re.compile(r"\bnetherit\b", re.I), lambda m: "Netheritt" if m.group(0)[0].isupper() else "netheritt"),
    (re.compile(r"\bNiðurlondum\b"), "Nether"),
    (re.compile(r"\bNiðurlond\b"), "Nether"),
    (re.compile(r"\bneðra eldum\b", re.I), "Nether-eldi"),
]

LETTER = r"A-ZÁÐÍÓÚÝÆØa-záðíóúýæø"

def fix_sentence_spacing(value: str) -> str:
    # MT frequently joins sentences as "...word.Next". Digits are excluded so
    # decimal values such as 1.5 are untouched.
    return re.sub(rf"(?<=[.!?])(?=[{LETTER}])", " ", value)

changed = 0
changed_files = 0
for path in FILES:
    data = json.loads(path.read_text(encoding="utf-8"))
    file_changed = 0
    for key, old in list(data.items()):
        new = old
        if key in KEY_OVERRIDES:
            new = KEY_OVERRIDES[key]
        elif new in VALUE_REPLACEMENTS:
            new = VALUE_REPLACEMENTS[new]

        # Normalize the 64 generated hotkey labels, many of which were mistranslated.
        m = re.fullmatch(r"key\.neoorigins\.hotkey\.(\d+)", key)
        if m:
            new = f"Snarlykil {int(m.group(1)):02d}"

        # Targeted contextual replacements.
        if key == "power.origins_furries.scales.description":
            new = "Tíni skøl geva tær +4 natúrliga brynju."
        elif key == "origin.origins_furries.raccoon.description":
            new = "Vaskabjørnar eru smidligir og forvitnir matleitarar, sum ofta leita í ruski."
        elif key == "power.origins_furries.chicken_xp.description":
            new = "Tú fært tvær ferðir so nógv royndarstig av at drepa høsn."
        elif key == "power.origins_furries.pavlov.description":
            new = "At ringja við einari bygdaklokku grøðir teg í staðin fyri at geva tær mat."
        elif key == "power.neoorigins.blazeling_nether_born.description":
            new = "Tú flytur teg skjótari, meðan tú ert í Nether (einki sjónligt effektikon)."

        for pattern, replacement in TEXT_REPLACEMENTS:
            new = pattern.sub(replacement, new)
        new = fix_sentence_spacing(new)

        if new != old:
            data[key] = new
            changed += 1
            file_changed += 1
    if file_changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(f"Faroese contextual refinement: {changed} values changed across {changed_files} files")
