#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative context fixes for machine-translation false friends and
# Minecraft/mod terminology. Keep proper game/mod terms when clearer.
OVERRIDES = {
    "neoorigins.night_vision.no_power": "Nid oes gan eich Tarddiad y gallu Gweledigaeth Nos.",
    "neoorigins.ultimine.no_power": "Nid oes gan eich Tarddiad y gallu Ultimine.",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.category.neoorigins.hotkeys": "NeoOrigins (bysellau poeth)",
    "key.neoorigins.toggle_night_vision": "Toglo Gweledigaeth Nos",
    "gui.neoorigins.button.back": "< Yn ôl",
    "gui.neoorigins.picker.back_to_grid": "< Yn ôl i'r grid",
    "gui.neoorigins.editor.powers_header": "Pwerau Togladwy",
    "gui.neoorigins.creator.save": "Cadw",
    "gui.neoorigins.creator.apply": "Cymhwyso",
    "gui.neoorigins.mob_creator.apply": "Cymhwyso",
    "gui.neoorigins.mob_creator.tab.drops": "Eitemau wedi'u Gollwng",

    "origins.neoorigins.blazeling.name": "Blazeling",
    "power.neoorigins.blazeling_nether_born.name": "Wedi'i Eni yn y Nether",
    "power.neoorigins.blazeling_nether_born.description": "Rydych chi'n symud yn gyflymach tra yn y Nether.",
    "power.neoorigins.caveborn_night_vision.name": "Cyfarwydd â'r Tywyllwch",
    "power.neoorigins.caveborn_no_fall_damage.name": "Cam y Ceudwll",
    "power.neoorigins.caveborn_stone_fists.name": "Dyrnau Cerrig",
    "power.neoorigins.caveborn_mining_fortune.name": "Mining Fortune",
    "power.neoorigins.nether_fungus_diet.name": "Deiet Ffwng y Nether",
    "power.neoorigins.caveborn_eat_netherite.name": "Blas am Netherite",
    "power.neoorigins.caveborn_netherite_bonus.name": "Craidd Netherite",
    "power.neoorigins.enderian_ender_eyes.name": "Ender Eyes",
    "power.neoorigins.golem_natural_armor.name": "Croen Haearn",

    "power.origins_furries.charge.name": "Ymosodiad Gwib",
    "power.origins_furries.chicken_xp.name": "XP Cyw Iâr",
    "power.origins_furries.low_light_vision.name": "Golwg mewn Golau Isel",
    "power.origins_furries.pavlov.name": "Ymateb Pavlov",
    "power.origins_furries.scales.name": "Cennau",
    "power.origins_furries.scales.description": "Mae eich cennau yn rhoi +4 Arfwisg Naturiol i chi.",
    "power.origins_furries.raccoon_jump.name": "Naid Racŵn",
    "power.origins_furries.safe_meat.description": "Mae Cnawd Pydredig a Chig Dafad Amrwd yn ddiogel i'w bwyta.",
    "power.origins_furries.trash_regen.description": "Rydych chi'n ennill Adfywio o fwyta Cnawd Pydredig.",
    "power.origins_furries.night_vision.name": "Gweledigaeth Nos",

    "key.originsmodernui.open_profile": "Agor Proffil Cymeriad",
    "key.originsmodernui.toggle_hud": "Toglo HUD",
    "originsmodernui.config.hud.position": "Safle HUD",
    "originsmodernui.config.hud.opacity": "Didreiddedd HUD",
    "originsmodernui.config.hud.show_level": "Dangos lefel",
}

# Google occasionally joins translated sentences without a space. Fix only
# punctuation immediately followed by an uppercase Latin/Welsh letter.
SENTENCE_JOIN = re.compile(r"(?<=[.!?])(?=[A-ZÀ-ÖØ-Ý])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/cy_gb.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = OVERRIDES.get(key, value)
        spaced = SENTENCE_JOIN.sub(" ", new_value)
        if spaced != new_value:
            spacing_fixes += 1
        new_value = spaced
        if new_value != value:
            data[key] = new_value
            changed = True
            changed_values += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(f"Welsh refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
