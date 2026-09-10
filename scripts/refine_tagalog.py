#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive UI wording and highly visible labels. Origin / NeoOrigins and
# well-known mod terms remain canonical where translating them would be less clear.
OVERRIDES = {
    "neoorigins.toggle.on": "Pinagana ang kakayahan",
    "neoorigins.toggle.off": "Hindi pinagana ang kakayahan",
    "neoorigins.night_vision.on": "Pinagana ang Pagkakita sa Dilim",
    "neoorigins.night_vision.off": "Hindi pinagana ang Pagkakita sa Dilim",
    "neoorigins.night_vision.disabled_by_server": "Hindi pinagana ang Pagkakita sa Dilim sa server na ito.",
    "neoorigins.night_vision.no_power": "Walang kakayahang Pagkakita sa Dilim ang iyong Origin.",
    "neoorigins.ultimine.no_power": "Walang kakayahang Ultimine ang iyong Origin.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Klase",
    "screen.neoorigins.choose_origin": "Pumili ng Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Pumili ng Origin",
    "screen.neoorigins.choose.origins.layer.class": "Pumili ng klase",
    "gui.neoorigins.search.label": "Maghanap ng Origin",
    "gui.neoorigins.picker.no_results": "Walang Origin na tumutugma sa iyong paghahanap",
    "gui.neoorigins.hint.select": "Pumili ng Origin upang makita ang mga detalye",
    "gui.neoorigins.detail.powers_header": "Mga Kakayahan",
    "gui.neoorigins.sort.class": "Klase",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Kakayahan ng Klase",
    "key.neoorigins.view_info": "Tingnan ang impormasyon ng Origin",
    "key.neoorigins.open_creator": "Buksan ang Origin Creator",
    "key.neoorigins.open_mob_creator": "Buksan ang Mob Origin Creator",
    "key.neoorigins.toggle_night_vision": "I-toggle ang Pagkakita sa Dilim",
    "key.category.neoorigins.hotkeys": "NeoOrigins (Mga Hotkey)",
    "screen.neoorigins.origin_info": "Impormasyon ng Origin",
    "gui.neoorigins.info.no_origin": "Wala pang napipiling Origin.",
    "gui.neoorigins.info.your_origin": "Iyong Origin",
    "screen.neoorigins.origin_editor": "Editor ng Origin",
    "gui.neoorigins.editor.layers_header": "Mga Layer ng Origin",
    "gui.neoorigins.editor.powers_header": "Karagdagang Mga Kakayahan",
    "screen.neoorigins.creator": "Origin Creator",
    "gui.neoorigins.creator.tab.powers": "Mga Kakayahan",
    "gui.neoorigins.creator.apply": "Ilapat",
    "screen.neoorigins.mob_creator": "Mob Origin Creator",
    "gui.neoorigins.mob_creator.tab.powers": "Mga Kakayahan",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Mga Panuntunan sa Pag-spawn",
    "gui.neoorigins.mob_creator.tab.drops": "Mga Nahuhulog na Item",
    "gui.neoorigins.mob_creator.apply": "Ilapat",
    "gui.neoorigins.debug.powers_header": "Mga Ibinigay na Kakayahan",

    # A small manual pass over highly visible add-on names/titles.
    "origin.medievalorigins.high_elf.cryomancer.name": "Mangkukulam ng Yelo",
    "power.medievalorigins.alfiq.on_your_feet.name": "Tumayo Ka",
    "power.medievalorigins.banshee.hexed.name": "Isinumpa",
    "power.medievalorigins.pixie.pixie_properties.name": "Munting Katawan",
    "power.origins_furries.heavy_wool.name": "Mabigat na Lana",
    "entity.ibarnorigins.homing_wither_skull": "Humahabol na Wither Skull",
    "power.ibarnorigins.witherskull.name": "Humahabol na Wither Skull",
    "power.neoorigins.class_merchant_silver_tongue.name": "Mahusay Magsalita",
    "power.neoorigins.class_cleric_turn_undead.name": "Itaboy ang Undead",
    "power.neoorigins.class_paladin_turn_undead.name": "Itaboy ang Undead",
    "power.neoorigins.sporeling_daylight_damage.name": "Paso sa Araw",
    "power.neoorigins.frostborn_freeze_aura.name": "Bugso ng Lamig",
    "power.neoorigins.feline_no_fall_damage.name": "Siyam na Buhay",
    "power.neoorigins.class_rogue_backstab.name": "Saksak sa Likod",
    "power.neoorigins.dwarf_darkvision.name": "Paningin sa Dilim",
    "power.neoorigins.dwarf_stonecunning.name": "Kaalaman sa Bato",
    "power.neoorigins.earth_mage_stonecunning.name": "Kaalaman sa Bato",
    "power.neoorigins.stoneguard_stone_mining.name": "Tagabasag ng Bato",
    "power.neoorigins.air_mage_zephyr.name": "Banayad na Hangin",
    "neoorigins.configuration.classes.class_lumberjack": "Magtotroso",
    "neoorigins.configuration.class_lumberjack": "Magtotroso",
}

# Official/current Minecraft Tagalog terminology where applicable, plus branding.
VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Pagkakita sa Dilim",
    "Rotten Flesh": "Bulok na Laman",
}

changed_files = 0
changed_values = 0
found_keys = set()
for path in sorted(ASSETS.glob("**/lang/tl_ph.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, wanted in OVERRIDES.items():
        if key in data:
            found_keys.add(key)
            if data[key] != wanted:
                data[key] = wanted
                changed = True
                changed_values += 1
    for key, value in list(data.items()):
        new_value = value
        for old, new in VALUE_REPLACEMENTS.items():
            new_value = new_value.replace(old, new)
        if new_value != value:
            data[key] = new_value
            changed = True
            changed_values += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

required = {
    "neoorigins.toggle.on",
    "neoorigins.night_vision.on",
    "origins.layer.origin",
    "screen.neoorigins.choose_origin",
    "key.category.neoorigins.neoorigins",
    "key.neoorigins.open_mob_creator",
    "gui.neoorigins.mob_creator.tab.spawn_rules",
    "screen.neoorigins.origin_editor",
}
missing = sorted(required - found_keys)
if missing:
    raise SystemExit(f"Required Tagalog UI keys not found: {missing}")
print(f"Refined {changed_values} Tagalog values across {changed_files} files; matched {len(found_keys)} explicit keys")
