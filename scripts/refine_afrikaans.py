#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
FILES = sorted(ASSETS.glob("**/lang/af_za.json"))
if not FILES:
    raise SystemExit("No Afrikaans af_za files found")

KEY_OVERRIDES = {
    # Core NeoOrigins UI / canonical product terminology.
    "neoorigins.toggle.on": "Vermoë aangeskakel",
    "neoorigins.toggle.off": "Vermoë afgeskakel",
    "neoorigins.night_vision.on": "Nagsig aan",
    "neoorigins.night_vision.off": "Nagsig af",
    "neoorigins.night_vision.disabled_by_server": "Nagsig is op hierdie bediener gedeaktiveer.",
    "neoorigins.night_vision.no_power": "Jou Origin het nie die nagsig-vermoë nie.",
    "neoorigins.ultimine.no_power": "Jou Origin het nie die Ultimine-vermoë nie.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Klas",
    "screen.neoorigins.choose_origin": "Kies jou Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Kies jou Origin",
    "screen.neoorigins.choose.origins.layer.class": "Kies jou klas",
    "gui.neoorigins.search.label": "Soek Origin",
    "gui.neoorigins.picker.no_results": "Geen Origin pas by jou soektog nie",
    "gui.neoorigins.hint.select": "Kies 'n Origin om besonderhede te sien",
    "gui.neoorigins.detail.powers_header": "Vermoëns",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.view_info": "Bekyk Origin-inligting",
    "key.neoorigins.open_creator": "Maak Origin Creator oop",
    "key.neoorigins.open_mob_creator": "Maak Mob Origin Creator oop",
    "key.neoorigins.toggle_night_vision": "Wissel nagsig",
    "key.category.neoorigins.hotkeys": "NeoOrigins (sneltoetse)",
    "screen.neoorigins.origin_info": "Origin-inligting",
    "gui.neoorigins.info.no_origin": "Nog geen Origin gekies nie.",
    "gui.neoorigins.info.your_origin": "Jou Origin",
    "screen.neoorigins.origin_editor": "Origin-redigeerder",
    "gui.neoorigins.editor.layers_header": "Origin-lae",
    "gui.neoorigins.editor.powers_header": "Wissel vermoëns",
    "screen.neoorigins.creator": "Origin Creator",
    "gui.neoorigins.creator.tab.powers": "Vermoëns",
    "gui.neoorigins.creator.apply": "Pas toe",
    "screen.neoorigins.mob_creator": "Mob Origin Creator",
    "gui.neoorigins.mob_creator.tab.powers": "Vermoëns",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Verskyningsreëls",
    "gui.neoorigins.mob_creator.tab.drops": "Buit",
    "gui.neoorigins.mob_creator.apply": "Pas toe",
    "gui.neoorigins.debug.powers_header": "Toegekende vermoëns",

    # Canonical Origin identities / proper names.
    "origins.neoorigins.human.name": "Human",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    # Minecraft / gameplay terminology and common MT false friends.
    "power.neoorigins.blazeling_nether_born.name": "Nether-gebore",
    "power.origins_furries.charge.name": "Stormloop",
    "power.origins_furries.chicken_xp.name": "Ervaring van hoenders",
    "power.origins_furries.pavlov.name": "Pavlov se refleks",
    "power.origins_furries.raccoon.name": "Wasbeer",
    "power.origins_furries.scales.name": "Skubbe",
    "power.origins_furries.night_vision.name": "Nagsig",
    "power.origins_furries.low_light_vision.name": "Laelig-nagsig",
    "power.origins_furries.heavy_wool.name": "Swaar wol",

    # Origin Architect is a product name, not generic architecture.
    "screen.originsmodernui.title": "Kies jou Origin",
    "screen.originsmodernui.search_hint": "Soek Origin...",
    "screen.originsmodernui.choose_prompt": "Kies 'n Origin uit die lys",
    "key.originsmodernui.toggle_hud": "Wissel Origin Architect-HUD",
    "originsmodernui.config.hud.show_level": "Wys Origin Architect-vlak",
    "originsmodernui.config.hud.show_points": "Wys onbestede statistiekpunte",
    "originsmodernui.config.hud.show_xp_popup": "Wys XP-wins",
    "originsmodernui.config.hud.show_level_popup": "Wys vlakverhoging",
}

# Exact-value mistranslations which are unambiguously wrong in these resources.
VALUE_REPLACEMENTS = {
    "Geplavei": "Pavlov se refleks",
    "Skale": "Skubbe",
    "Oorsprong Skepper": "Origin Creator",
    "Doen aansoek": "Pas toe",
}

# Targeted terminology replacements. Keep Minecraft proper names recognizable.
TEXT_REPLACEMENTS = [
    (re.compile(r"\bGeplavei\b"), "Pavlov se refleks"),
    (re.compile(r"\bOnderland\b"), "Nether"),
    (re.compile(r"\bOnder-gebore\b"), "Nether-gebore"),
    (re.compile(r"\bnetheriet\b", re.I), lambda m: "Netherite" if m.group(0)[0].isupper() else "netherite"),
    (re.compile(r"\bnetherrak\b", re.I), lambda m: "Netherrack" if m.group(0)[0].isupper() else "netherrack"),
]

LETTER = r"A-Za-zÀ-ÖØ-öø-ÿ"

def fix_sentence_spacing(value: str) -> str:
    # MT frequently joins sentences as "...woord.Volgende". Digits are excluded,
    # so decimal values such as 1.5 remain intact.
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

        # Normalize all generated hotkey labels consistently.
        m = re.fullmatch(r"key\.neoorigins\.hotkey\.(\d+)", key)
        if m:
            new = f"Sneltoets {int(m.group(1)):02d}"

        # Targeted contextual descriptions that MT rendered incorrectly.
        if key == "power.origins_furries.scales.description":
            new = "Jou skubbe gee jou +4 natuurlike pantser."
        elif key == "origin.origins_furries.raccoon.description":
            new = "Wasbere is rats en nuuskierige kossoekers wat dikwels in afval rondkrap."
        elif key == "power.origins_furries.chicken_xp.description":
            new = "Jy kry twee keer soveel ervaring wanneer jy hoenders doodmaak."
        elif key == "power.origins_furries.pavlov.description":
            new = "Om 'n dorpsklok te lui, genees jou in ruil vir honger."
        elif key == "power.neoorigins.blazeling_nether_born.description":
            new = "Jy beweeg vinniger terwyl jy in die Nether is (geen sigbare effekikoon nie)."
        elif key == "power.origins_furries.heavy_wool.description":
            new = "Jou dik wol gee jou +2 natuurlike pantser."
        elif key == "power.origins_furries.night_vision.description":
            new = "Jy het nagsig."
        elif key == "power.origins_furries.low_light_vision.description":
            new = "Jy kry nagsig bo seevlak."

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

print(f"Afrikaans contextual refinement: {changed} values changed across {changed_files} files")
