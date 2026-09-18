#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative contextual corrections for machine-translation false friends and
# Minecraft/Origins terminology. Canonical mod/game names are intentionally kept
# where a literal translation changes the identity or meaning of the term.
OVERRIDES = {
    "neoorigins.night_vision.on": "Sealladh Oidhche air",
    "neoorigins.night_vision.off": "Sealladh Oidhche dheth",
    "neoorigins.night_vision.disabled_by_server": "Tha Sealladh Oidhche à comas air an fhrithealaiche seo.",
    "neoorigins.night_vision.no_power": "Chan eil cumhachd Sealladh Oidhche aig an Origin agad.",
    "neoorigins.ultimine.no_power": "Chan eil cumhachd Ultimine aig an Origin agad.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Clas",
    "screen.neoorigins.choose_origin": "Tagh an Origin agad",
    "screen.neoorigins.choose.origins.layer.origin": "Tagh an Origin agad",
    "gui.neoorigins.search.label": "Lorg Origins",
    "gui.neoorigins.picker.back_to_grid": "< Air ais dhan ghriod",
    "gui.neoorigins.picker.no_results": "Chan eil Origin sam bith a' freagairt ris an rannsachadh agad",
    "gui.neoorigins.hint.select": "Tagh Origin gus am mion-fhiosrachadh fhaicinn",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.category.neoorigins.hotkeys": "NeoOrigins (hotkeys)",
    "key.neoorigins.view_info": "Seall fiosrachadh Origin",
    "key.neoorigins.open_creator": "Fosgail Cruthadair Origin",
    "key.neoorigins.open_mob_creator": "Fosgail Cruthadair Mob Origin",
    "key.neoorigins.toggle_night_vision": "Toglaich Sealladh Oidhche",
    "screen.neoorigins.origin_info": "Fiosrachadh Origin",
    "gui.neoorigins.info.no_origin": "Cha deach Origin a thaghadh fhathast.",
    "gui.neoorigins.info.your_origin": "An Origin agad",
    "screen.neoorigins.origin_editor": "Deasaiche Origin",
    "gui.neoorigins.editor.layers_header": "Sreathan Origin",
    "gui.neoorigins.editor.powers_header": "Cumhachdan roghnach",
    "screen.neoorigins.creator": "Cruthadair Origin",
    "gui.neoorigins.creator.apply": "Cuir an sàs",
    "screen.neoorigins.mob_creator": "Cruthadair Mob Origin",
    "gui.neoorigins.mob_creator.apply": "Cuir an sàs",
    "gui.neoorigins.mob_creator.tab.drops": "Nitchean a thuiteas",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Riaghailtean Spawn",

    # Canonical Origin identities: translating these names literally creates
    # unrelated Scottish Gaelic words or even another nationality.
    "origins.neoorigins.human.name": "Duine",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    "power.neoorigins.merling_water_breathing.name": "Anail Uisge",
    "power.neoorigins.merling_night_vision.name": "Sealladh na Doimhneachd",
    "power.neoorigins.merling_land_slowdown.name": "Nas Slaodaiche air Tìr",
    "power.neoorigins.merling_dries_out.name": "A' Tiormachadh",
    "power.neoorigins.avian_no_fall_damage.name": "Cuideam Ite",
    "power.neoorigins.avian_hollow_bones.name": "Cnàmhan Falamh",
    "power.neoorigins.blazeling_fire_immunity.name": "Cridhe nan Èibhlean",
    "power.neoorigins.blazeling_nether_born.name": "Rugadh san Nether",
    "power.neoorigins.blazeling_nether_born.description": "Gluaisidh tu nas luaithe fhad 's a tha thu san Nether.",
    "power.neoorigins.blazeling_night_vision.name": "Sealladh Teas",
    "power.neoorigins.caveborn_night_vision.name": "Cleachdte ris an Dorchadas",
    "power.neoorigins.caveborn_no_fall_damage.name": "Ceum Uaimhe",
    "power.neoorigins.caveborn_stone_fists.name": "Dòrnan Cloiche",
    "power.neoorigins.caveborn_mining_fortune.name": "Mining Fortune",
    "power.neoorigins.nether_fungus_diet.name": "Daithead Fungais Nether",
    "power.neoorigins.caveborn_eat_netherite.name": "Blas Netherite",
    "power.neoorigins.caveborn_netherite_bonus.name": "Cridhe Netherite",
    "power.neoorigins.enderian_ender_eyes.name": "Ender Eyes",
    "power.neoorigins.golem_natural_armor.name": "Craiceann Iarainn",

    "origin.origins_furries.komodo.name": "Dràgon Komodo",
    "origin.origins_furries.raccoon.name": "Raccoon",
    "power.origins_furries.charge.name": "Ionnsaigh Luais",
    "power.origins_furries.chicken_xp.name": "XP Cearc",
    "power.origins_furries.low_light_vision.name": "Sealladh ann an Solas Ìosal",
    "power.origins_furries.low_light_vision.description": "Gheibh thu Sealladh Oidhche os cionn ìre na mara.",
    "power.origins_furries.pavlov.name": "Freagairt Pavlov",
    "power.origins_furries.raccoon_jump.name": "Leum Raccoon",
    "power.origins_furries.night_vision.name": "Sealladh Oidhche",
    "power.origins_furries.night_vision.description": "Tha Sealladh Oidhche agad.",
    "power.origins_furries.scales.name": "Lannan",
    "power.origins_furries.scales.description": "Bheir na lannan agad +4 Armachd Nàdarra dhut.",
    "power.origins_furries.safe_meat.description": "Tha Rotten Flesh agus Raw Mutton sàbhailte ri ithe.",
    "power.origins_furries.trash_regen.description": "Gheibh thu Regeneration bho bhith ag ithe Rotten Flesh.",
    "power.origins_furries.submersion.name": "Bogadh",

    "screen.originsmodernui.title": "Tagh an Origin agad",
    "screen.originsmodernui.search_hint": "Lorg Origins...",
    "screen.originsmodernui.choose_prompt": "Tagh Origin bhon liosta",
    "key.originsmodernui.open_profile": "Fosgail Pròifil a' Charactair",
    "key.originsmodernui.toggle_hud": "Toglaich HUD",
    "originsmodernui.config.hud.position": "Suidheachadh HUD",
    "originsmodernui.config.hud.style": "Stoidhle HUD",
    "originsmodernui.config.hud.opacity": "Neo-shoilleireachd HUD",
    "originsmodernui.config.hud.show_level": "Seall ìre",
    "originsmodernui.config.hud.show_points": "Seall puingean stat nach deach a chleachdadh",
    "originsmodernui.config.hud.show_xp_popup": "Seall pop-up XP",
    "originsmodernui.config.hud.show_level_popup": "Seall pop-up ìre-suas",
}

EXACT_VALUE_REPLACEMENTS = {
    "Neo-Thùs": "NeoOrigins",
    "Neo Origins": "NeoOrigins",
    "Sealladh na h-oidhche": "Sealladh Oidhche",
    "Sealladh oidhche": "Sealladh Oidhche",
}

# Machine translation occasionally joins sentence boundaries. Only insert a
# space when punctuation is immediately followed by an uppercase Latin letter.
SENTENCE_JOIN = re.compile(r"(?<=[.!?])(?=[A-ZÀ-ÖØ-Ý])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/gd_gb.json")):
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

print(f"Scottish Gaelic refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
