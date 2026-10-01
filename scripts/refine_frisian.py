#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive cleanup for highly visible UI, power/class names and config
# terminology. Origin / NeoOrigins remain canonical project/product terms. Core
# Minecraft wording follows the current West Frisian client where practical.
OVERRIDES = {
    # Core NeoOrigins UI.
    "neoorigins.toggle.on": "Krêft ynskeakele",
    "neoorigins.toggle.off": "Krêft útskeakele",
    "neoorigins.night_vision.on": "Nachtsicht ynskeakele",
    "neoorigins.night_vision.off": "Nachtsicht útskeakele",
    "neoorigins.night_vision.disabled_by_server": "Nachtsicht is útskeakele op dizze server.",
    "neoorigins.night_vision.no_power": "Dyn Origin hat de krêft Nachtsicht net.",
    "neoorigins.ultimine.no_power": "Dyn Origin hat de krêft Ultimine net.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Klasse",
    "screen.neoorigins.choose_origin": "Kies in Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Kies in Origin",
    "screen.neoorigins.choose.origins.layer.class": "Kies in klasse",
    "gui.neoorigins.search.label": "Origins sykje",
    "gui.neoorigins.picker.no_results": "Gjin Origins komme oerien mei de sykterm",
    "gui.neoorigins.hint.select": "Kies in Origin om de details te besjen",
    "gui.neoorigins.detail.powers_header": "Krêften",
    "gui.neoorigins.sort.class": "Klasse",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Klassefeardigens",
    "key.neoorigins.view_info": "Origin-ynformaasje besjen",
    "key.neoorigins.open_creator": "Origin-makker iepenje",
    "key.neoorigins.open_mob_creator": "Mob Origin-makker iepenje",
    "key.neoorigins.toggle_night_vision": "Nachtsicht oan/út sette",
    "key.category.neoorigins.hotkeys": "NeoOrigins (fluchtoetsen)",
    "screen.neoorigins.origin_info": "Origin-ynformaasje",
    "gui.neoorigins.info.no_origin": "Der is noch gjin Origin keazen.",
    "gui.neoorigins.info.your_origin": "Dyn Origin",
    "screen.neoorigins.origin_editor": "Origin-bewurker",
    "gui.neoorigins.editor.layers_header": "Origin-lagen",
    "gui.neoorigins.editor.powers_header": "Oanfoljende krêften",
    "screen.neoorigins.creator": "Origin-makker",
    "gui.neoorigins.creator.tab.powers": "Krêften",
    "gui.neoorigins.creator.apply": "Tapasse",
    "screen.neoorigins.mob_creator": "Mob Origin-makker",
    "gui.neoorigins.mob_creator.tab.powers": "Krêften",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Spawnregels",
    "gui.neoorigins.mob_creator.tab.drops": "Bút",
    "gui.neoorigins.mob_creator.apply": "Tapasse",
    "gui.neoorigins.debug.powers_header": "Tawiisde krêften",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fae",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "Op dyn fuotten",
    "power.medievalorigins.banshee.hexed.name": "Betsjoend",
    "power.medievalorigins.pixie.pixie_properties.name": "Lyts lichem",
    "origin.medievalorigins.high_elf.cryomancer.name": "Kryomant",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "Swiere wol",
    "entity.ibarnorigins.homing_wither_skull": "Sykjende Wither-schedels",
    "power.ibarnorigins.witherskull.name": "Sykjende Wither-schedels",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "Ferheven krêft",
    "power.neoorigins.class_merchant_silver_tongue.name": "Sulveren tonge",
    "power.neoorigins.class_cleric_turn_undead.name": "Untsjerren ôfwarje",
    "power.neoorigins.class_paladin_turn_undead.name": "Untsjerren ôfwarje",
    "power.neoorigins.sporeling_daylight_damage.name": "Baarnend deiljocht",
    "power.neoorigins.frostborn_freeze_aura.name": "Froastweach",
    "power.neoorigins.strider_fire_immunity.name": "Berne yn lava",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Echoferdigening",
    "power.neoorigins.enderite_slow_fall.name": "Ender-glydzje",
    "power.neoorigins.enderite_water_damage.name": "Ender-swakte",
    "power.neoorigins.enderian_teleport.name": "Ender-teleportaasje",
    "power.neoorigins.feline_no_fall_damage.name": "Njoggen libbens",
    "power.neoorigins.draconic_fire_immunity.name": "Drakebloed",
    "power.neoorigins.cave_dragon_apex_hp.name": "Topdraak",
    "power.neoorigins.automaton_ascended_overclock.name": "Oerklok",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Swiertekrêftôfstimming",
    "power.neoorigins.necromancer_irons_attunement.name": "Nekrotyske ôfstimming",
    "power.neoorigins.class_rogue_backstab.name": "Rêchstek",
    "power.neoorigins.dwarf_darkvision.name": "Tsjustersicht",
    "power.neoorigins.earth_mage_stonecunning.name": "Stienkennis",
    "power.neoorigins.dwarf_stonecunning.name": "Stienkennis",
    "power.neoorigins.stoneguard_stone_mining.name": "Stienmynjen",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Rinne yn 'e skaden",
    "power.neoorigins.air_mage_zephyr.name": "Sefyr",
    "power.neoorigins.gravity_mage_unmoored.name": "Losmakke",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Houthakker",
    "neoorigins.configuration.class_lumberjack": "Houthakker",
    "neoorigins.configuration.cinderborn_fireball": "Cinderborn-fjoerbal",
    "neoorigins.configuration.elytrian_elytra_boost": "Elytrian Elytra-fersnelling",
    "neoorigins.configuration.golem_fire_weakness": "Golem-fjoerswakte",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Gorgon-ferstienjende blik",
    "neoorigins.configuration.sculkborn_knockback_resist": "Sculkborn-weromslachwjerstân",
    "neoorigins.configuration.verdant_nether_damage": "Verdant-Nether-skea",
    "neoorigins.configuration.warden_sonic_boom": "Warden-sonyske knal",

    # Origins Fantasy / classes.
    "origins.origins_fantasy.fae.name": "Fae",
    "origins.origins_fantasy.fae_two.name": "Fae",
    "origins.origins_fantasy.orc.name": "Ork",
    "power.origins_fantasy.fae_spryness.name": "Fae-behendigens",
    "power.origins_fantasy.ascended_na.name": "Ferheven harnas",
    "origins.origins_classes_iss.shadowcaster.name": "Skaadsmiter",
    "power.origins_classes_iss.mystic_turn_undead.name": "Untsjerren ôfwarje",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Ikehûd",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Nachtsicht",
    "Rotten Flesh": "Bedoarn fleis",
    "Netherite": "Netheryt",
}

SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[A-ZÀ-ÖØ-Þ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/fy_nl.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = OVERRIDES.get(key, value)
        for old, new in VALUE_REPLACEMENTS.items():
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

print(f"Frisian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
