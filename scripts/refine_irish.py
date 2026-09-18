#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative corrections for machine-translation false friends and
# Minecraft/Origins terminology. Proper mod/game terms are intentionally kept
# where translating them literally would change their meaning.
OVERRIDES = {
    "neoorigins.night_vision.on": "Amharc Oíche ar siúl",
    "neoorigins.night_vision.off": "Amharc Oíche múchta",
    "neoorigins.night_vision.disabled_by_server": "Tá Amharc Oíche díchumasaithe ar an bhfreastalaí seo.",
    "neoorigins.night_vision.no_power": "Níl cumhacht Amharc Oíche ag do Origin.",
    "neoorigins.ultimine.no_power": "Níl cumhacht Ultimine ag do Origin.",
    "origins.layer.origin": "Origin",
    "screen.neoorigins.choose_origin": "Roghnaigh d'Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Roghnaigh d'Origin",
    "gui.neoorigins.search.label": "Cuardaigh Origins",
    "gui.neoorigins.picker.back_to_grid": "< Ar Ais chuig an eangach",
    "gui.neoorigins.picker.no_results": "Níl aon Origin ag teacht le do chuardach",
    "gui.neoorigins.hint.select": "Roghnaigh Origin chun sonraí a fheiceáil",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.category.neoorigins.hotkeys": "NeoOrigins (aicearraí méarchláir)",
    "key.neoorigins.view_info": "Féach ar Fhaisnéis Origin",
    "key.neoorigins.open_mob_creator": "Oscail Cruthaitheoir Mob Origin",
    "key.neoorigins.toggle_night_vision": "Malartaigh Amharc Oíche",
    "screen.neoorigins.origin_info": "Eolas Origin",
    "gui.neoorigins.info.no_origin": "Níl aon Origin roghnaithe fós.",
    "gui.neoorigins.info.your_origin": "D'Origin",
    "screen.neoorigins.origin_editor": "Eagarthóir Origin",
    "gui.neoorigins.editor.layers_header": "Sraitheanna Origin",
    "gui.neoorigins.editor.powers_header": "Cumhachtaí Inmhalartaithe",
    "screen.neoorigins.creator": "Cruthaitheoir Origin",
    "gui.neoorigins.creator.apply": "Cuir i bhfeidhm",
    "gui.neoorigins.mob_creator.apply": "Cuir i bhfeidhm",
    "gui.neoorigins.mob_creator.tab.drops": "Earraí a Thiteann",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Rialacha Sceite",

    "origins.neoorigins.blazeling.name": "Blazeling",
    "power.neoorigins.blazeling_nether_born.name": "Rugadh sa Nether",
    "power.neoorigins.blazeling_nether_born.description": "Bogann tú níos tapúla agus tú sa Nether.",
    "power.neoorigins.blazeling_night_vision.name": "Amharc Teasa",
    "power.neoorigins.merling_night_vision.name": "Amharc na Doimhneachta",
    "power.neoorigins.merling_land_slowdown.name": "Mall ar Thalamh",
    "power.neoorigins.merling_dries_out.name": "Triomú Amach",
    "power.neoorigins.avian_no_fall_damage.name": "Meáchan Cleite",
    "power.neoorigins.caveborn_night_vision.name": "Cleachtaithe leis an Dorchadas",
    "power.neoorigins.caveborn_no_fall_damage.name": "Céim Uaimhe",
    "power.neoorigins.caveborn_stone_fists.name": "Dorn Cloiche",
    "power.neoorigins.caveborn_mining_fortune.name": "Mining Fortune",
    "power.neoorigins.nether_fungus_diet.name": "Aiste Bia Fungais an Nether",
    "power.neoorigins.caveborn_eat_netherite.name": "Blas ar Netheríte",
    "power.neoorigins.caveborn_netherite_bonus.name": "Croí Netheríte",
    "power.neoorigins.enderian_ender_eyes.name": "Ender Eyes",
    "power.neoorigins.golem_natural_armor.name": "Craiceann Iarainn",

    "origin.origins_furries.komodo.name": "Dragún Komodo",
    "power.origins_furries.charge.name": "Ionsaí Luais",
    "power.origins_furries.chicken_xp.name": "XP Sicín",
    "power.origins_furries.low_light_vision.name": "Amharc i Solas Íseal",
    "power.origins_furries.low_light_vision.description": "Faigheann tú Amharc Oíche os cionn leibhéal na farraige.",
    "power.origins_furries.pavlov.name": "Freagairt Pavlov",
    "power.origins_furries.raccoon_jump.name": "Léim Racúin",
    "power.origins_furries.night_vision.name": "Amharc Oíche",
    "power.origins_furries.night_vision.description": "Tá Amharc Oíche agat.",
    "power.origins_furries.scales.name": "Scálaí",
    "power.origins_furries.scales.description": "Tugann do scálaí +4 Armúr Nádúrtha duit.",
    "power.origins_furries.safe_meat.description": "Tá Feoil Lofa agus Caoireoil Amh sábháilte le hithe.",
    "power.origins_furries.trash_regen.description": "Faigheann tú Athghiniúint as Feoil Lofa a ithe.",

    "screen.originsmodernui.title": "Roghnaigh d'Origin",
    "screen.originsmodernui.search_hint": "Cuardaigh Origins...",
    "screen.originsmodernui.choose_prompt": "Roghnaigh Origin ón liosta",
    "key.originsmodernui.open_profile": "Oscail Próifíl an Charachtair",
    "key.originsmodernui.toggle_hud": "Malartaigh HUD",
    "originsmodernui.config.hud.position": "Suíomh HUD",
    "originsmodernui.config.hud.opacity": "Teimhneacht HUD",
    "originsmodernui.config.hud.show_level": "Taispeáin leibhéal",
    "originsmodernui.config.hud.show_points": "Taispeáin pointí stait nár úsáideadh",
    "originsmodernui.config.hud.show_xp_popup": "Taispeáin preabfhuinneog gnóthachain XP",
    "originsmodernui.config.hud.show_level_popup": "Taispeáin preabfhuinneog ardaithe leibhéil",
}

# Common MT artefacts that are safe to normalize regardless of key.
EXACT_VALUE_REPLACEMENTS = {
    "Fís Oíche": "Amharc Oíche",
    "Oíche Fís": "Amharc Oíche",
}

# Google translation sometimes joins sentence boundaries. Only insert spaces
# after sentence punctuation when the following character is an uppercase Latin
# letter, which avoids touching placeholders or formatting codes.
SENTENCE_JOIN = re.compile(r"(?<=[.!?])(?=[A-ZÀ-ÖØ-Ý])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/ga_ie.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = OVERRIDES.get(key, value)
        for old, new in EXACT_VALUE_REPLACEMENTS.items():
            new_value = new_value.replace(old, new)
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

print(f"Irish refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
