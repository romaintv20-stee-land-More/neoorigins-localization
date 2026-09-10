#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive cleanup for highly visible UI, power/class names and config
# terminology. Origin / NeoOrigins remain canonical project/product terms.
OVERRIDES = {
    # Core NeoOrigins UI.
    "neoorigins.toggle.on": "Sposobnost uključena",
    "neoorigins.toggle.off": "Sposobnost isključena",
    "neoorigins.night_vision.on": "Noćni vid uključen",
    "neoorigins.night_vision.off": "Noćni vid isključen",
    "neoorigins.night_vision.disabled_by_server": "Noćni vid je onemogućen na ovom serveru.",
    "neoorigins.night_vision.no_power": "Tvoj Origin nema sposobnost noćnog vida.",
    "neoorigins.ultimine.no_power": "Tvoj Origin nema sposobnost Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Klasa",
    "screen.neoorigins.choose_origin": "Odaberi Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Odaberi Origin",
    "screen.neoorigins.choose.origins.layer.class": "Odaberi klasu",
    "gui.neoorigins.search.label": "Pretraži Origine",
    "gui.neoorigins.picker.no_results": "Nijedan Origin ne odgovara tvojoj pretrazi",
    "gui.neoorigins.hint.select": "Odaberi Origin za prikaz detalja",
    "gui.neoorigins.detail.powers_header": "Moći",
    "gui.neoorigins.sort.class": "Klasa",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Vještina klase",
    "key.neoorigins.view_info": "Prikaži informacije o Originu",
    "key.neoorigins.open_creator": "Otvori kreator Origina",
    "key.neoorigins.open_mob_creator": "Otvori kreator Mob Origina",
    "key.neoorigins.toggle_night_vision": "Uključi/isključi noćni vid",
    "key.category.neoorigins.hotkeys": "NeoOrigins (prečice)",
    "screen.neoorigins.origin_info": "Informacije o Originu",
    "gui.neoorigins.info.no_origin": "Origin još nije odabran.",
    "gui.neoorigins.info.your_origin": "Tvoj Origin",
    "screen.neoorigins.origin_editor": "Uređivač Origina",
    "gui.neoorigins.editor.layers_header": "Slojevi Origina",
    "gui.neoorigins.editor.powers_header": "Dodatne moći",
    "screen.neoorigins.creator": "Kreator Origina",
    "gui.neoorigins.creator.tab.powers": "Moći",
    "gui.neoorigins.creator.apply": "Primijeni",
    "screen.neoorigins.mob_creator": "Kreator Mob Origina",
    "gui.neoorigins.mob_creator.tab.powers": "Moći",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Pravila pojavljivanja",
    "gui.neoorigins.mob_creator.tab.drops": "Plijen",
    "gui.neoorigins.mob_creator.apply": "Primijeni",
    "gui.neoorigins.debug.powers_header": "Dodijeljene moći",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fae",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "Na noge",
    "power.medievalorigins.banshee.hexed.name": "Proklet",
    "power.medievalorigins.pixie.pixie_properties.name": "Sićušno tijelo",
    "origin.medievalorigins.high_elf.cryomancer.name": "Kriomant",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "Teška vuna",
    "entity.ibarnorigins.homing_wither_skull": "Navodeća Wither lobanja",
    "power.ibarnorigins.witherskull.name": "Navodeća Wither lobanja",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "Uzdignuta snaga",
    "power.neoorigins.class_merchant_silver_tongue.name": "Srebrni jezik",
    "power.neoorigins.class_cleric_turn_undead.name": "Otjerivanje nemrtvih",
    "power.neoorigins.class_paladin_turn_undead.name": "Otjerivanje nemrtvih",
    "power.neoorigins.sporeling_daylight_damage.name": "Sunčeva opekotina",
    "power.neoorigins.frostborn_freeze_aura.name": "Ledeni val",
    "power.neoorigins.strider_fire_immunity.name": "Rođen u lavi",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Odjekujuća odbrana",
    "power.neoorigins.enderite_slow_fall.name": "Ender lebdenje",
    "power.neoorigins.enderite_water_damage.name": "Ender slabost",
    "power.neoorigins.enderian_teleport.name": "Ender teleportacija",
    "power.neoorigins.feline_no_fall_damage.name": "Devet života",
    "power.neoorigins.draconic_fire_immunity.name": "Zmajeva krv",
    "power.neoorigins.cave_dragon_apex_hp.name": "Vrhunski zmaj",
    "power.neoorigins.automaton_ascended_overclock.name": "Preopterećenje",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Usklađivanje gravitacije",
    "power.neoorigins.necromancer_irons_attunement.name": "Nekrotično usklađivanje",
    "power.neoorigins.class_rogue_backstab.name": "Udarac s leđa",
    "power.neoorigins.dwarf_darkvision.name": "Vid u mraku",
    "power.neoorigins.dwarf_stonecunning.name": "Poznavanje kamena",
    "power.neoorigins.earth_mage_stonecunning.name": "Poznavanje kamena",
    "power.neoorigins.stoneguard_stone_mining.name": "Razbijač kamena",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Trk kroz sjene",
    "power.neoorigins.air_mage_zephyr.name": "Povjetarac",
    "power.neoorigins.gravity_mage_unmoored.name": "Nevezan",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Drvosječa",
    "neoorigins.configuration.class_lumberjack": "Drvosječa",
    "neoorigins.configuration.cinderborn_fireball": "Vatrena kugla Cinderborna",
    "neoorigins.configuration.elytrian_elytra_boost": "Pojačanje Elytre Elytriana",
    "neoorigins.configuration.golem_fire_weakness": "Vatrena slabost Golema",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Okamenjujući pogled Gorgone",
    "neoorigins.configuration.sculkborn_knockback_resist": "Otpornost na odbacivanje Sculkborna",
    "neoorigins.configuration.verdant_nether_damage": "Nether šteta Verdanta",
    "neoorigins.configuration.warden_sonic_boom": "Zvučni udar Wardena",

    # Origins Fantasy / classes / backgrounds.
    "origins.origins_fantasy.fae.name": "Fae",
    "origins.origins_fantasy.fae_two.name": "Fae",
    "origins.origins_fantasy.orc.name": "Ork",
    "power.origins_fantasy.fae_spryness.name": "Okretnost Fae",
    "power.origins_fantasy.ascended_na.name": "Uzdignuti oklop",
    "origins.origins_classes_iss.shadowcaster.name": "Čarobnjak sjene",
    "power.origins_classes_iss.mystic_turn_undead.name": "Otjerivanje nemrtvih",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Hrastova koža",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Noćni vid",
    "Rotten Flesh": "Trulo meso",
}

# Repair missing spaces between sentences without touching placeholders.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[A-ZČĆĐŠŽ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/bs_ba.json")):
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

print(f"Bosnian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
