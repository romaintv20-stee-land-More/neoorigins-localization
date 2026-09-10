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
    "neoorigins.toggle.on": "Galloud gweredekaet",
    "neoorigins.toggle.off": "Galloud diweredekaet",
    "neoorigins.night_vision.on": "Gwelet en noz gweredekaet",
    "neoorigins.night_vision.off": "Gwelet en noz diweredekaet",
    "neoorigins.night_vision.disabled_by_server": "Diweredekaet eo gwelet en noz gant ar servijer-mañ.",
    "neoorigins.night_vision.no_power": "N'eus ket ar galloud Gwelet en noz gant hoc'h Origin.",
    "neoorigins.ultimine.no_power": "N'eus ket ar galloud Ultimine gant hoc'h Origin.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Klas",
    "screen.neoorigins.choose_origin": "Dibabit un Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Dibabit un Origin",
    "screen.neoorigins.choose.origins.layer.class": "Dibabit ur c'hlas",
    "gui.neoorigins.search.label": "Klask Origins",
    "gui.neoorigins.picker.no_results": "N'eus Origin ebet o klotañ gant ho klask",
    "gui.neoorigins.hint.select": "Dibabit un Origin evit diskouez ar munudoù",
    "gui.neoorigins.detail.powers_header": "Galloudoù",
    "gui.neoorigins.sort.class": "Klas",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Barregezh ar c'hlas",
    "key.neoorigins.view_info": "Gwelet titouroù an Origin",
    "key.neoorigins.open_creator": "Digeriñ krouer an Origin",
    "key.neoorigins.open_mob_creator": "Digeriñ krouer Mob Origin",
    "key.neoorigins.toggle_night_vision": "Gweredekaat/diweredekaat gwelet en noz",
    "key.category.neoorigins.hotkeys": "NeoOrigins (berradurioù)",
    "screen.neoorigins.origin_info": "Titouroù an Origin",
    "gui.neoorigins.info.no_origin": "N'eus Origin ebet dibabet c'hoazh.",
    "gui.neoorigins.info.your_origin": "Hoc'h Origin",
    "screen.neoorigins.origin_editor": "Embanner an Origin",
    "gui.neoorigins.editor.layers_header": "Gwiskadoù an Origin",
    "gui.neoorigins.editor.powers_header": "Galloudoù ouzhpenn",
    "screen.neoorigins.creator": "Krouer an Origin",
    "gui.neoorigins.creator.tab.powers": "Galloudoù",
    "gui.neoorigins.creator.apply": "Arloañ",
    "screen.neoorigins.mob_creator": "Krouer Mob Origin",
    "gui.neoorigins.mob_creator.tab.powers": "Galloudoù",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Reolennoù genel",
    "gui.neoorigins.mob_creator.tab.drops": "Preizh",
    "gui.neoorigins.mob_creator.apply": "Arloañ",
    "gui.neoorigins.debug.powers_header": "Galloudoù roet",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fae",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "War ho treid",
    "power.medievalorigins.banshee.hexed.name": "Milliget",
    "power.medievalorigins.pixie.pixie_properties.name": "Korf bihan-tre",
    "origin.medievalorigins.high_elf.cryomancer.name": "Kriomant",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "Gloan pounner",
    "entity.ibarnorigins.homing_wither_skull": "Klopennoù Wither heñchet",
    "power.ibarnorigins.witherskull.name": "Klopennoù Wither heñchet",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "Kreñvder uhelaet",
    "power.neoorigins.class_merchant_silver_tongue.name": "Teod arc'hant",
    "power.neoorigins.class_cleric_turn_undead.name": "Argas an divarvelien",
    "power.neoorigins.class_paladin_turn_undead.name": "Argas an divarvelien",
    "power.neoorigins.sporeling_daylight_damage.name": "Deviñ gant an heol",
    "power.neoorigins.frostborn_freeze_aura.name": "Gwagenn skorn",
    "power.neoorigins.strider_fire_immunity.name": "Ganet er lava",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Difenn dasson",
    "power.neoorigins.enderite_slow_fall.name": "Nijell Ender",
    "power.neoorigins.enderite_water_damage.name": "Gwander Ender",
    "power.neoorigins.enderian_teleport.name": "Treuzkas Ender",
    "power.neoorigins.feline_no_fall_damage.name": "Nav buhez",
    "power.neoorigins.draconic_fire_immunity.name": "Gwad aerouant",
    "power.neoorigins.cave_dragon_apex_hp.name": "Aerouant uhelañ",
    "power.neoorigins.automaton_ascended_overclock.name": "Dreist-tizh",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Emglev gant ar graviter",
    "power.neoorigins.necromancer_irons_attunement.name": "Emglev nekrotek",
    "power.neoorigins.class_rogue_backstab.name": "Taol en kein",
    "power.neoorigins.dwarf_darkvision.name": "Gwelet en deñvalijenn",
    "power.neoorigins.dwarf_stonecunning.name": "Anaoudegezh ar maen",
    "power.neoorigins.earth_mage_stonecunning.name": "Anaoudegezh ar maen",
    "power.neoorigins.stoneguard_stone_mining.name": "Torrer maen",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Redadeg dre ar skeudoù",
    "power.neoorigins.air_mage_zephyr.name": "Avelig",
    "power.neoorigins.gravity_mage_unmoored.name": "Distag",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Koadour",
    "neoorigins.configuration.class_lumberjack": "Koadour",
    "neoorigins.configuration.cinderborn_fireball": "Boul-tan Cinderborn",
    "neoorigins.configuration.elytrian_elytra_boost": "Kreñvaat adeskell Elytrian",
    "neoorigins.configuration.golem_fire_weakness": "Gwander ouzh an tan Golem",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Sell maenaat Gorgon",
    "neoorigins.configuration.sculkborn_knockback_resist": "Dalc'husted ouzh an argil Sculkborn",
    "neoorigins.configuration.verdant_nether_damage": "Freuzioù Nether Verdant",
    "neoorigins.configuration.warden_sonic_boom": "Tarzhadenn son Warden",

    # Origins Fantasy / classes / backgrounds.
    "origins.origins_fantasy.fae.name": "Fae",
    "origins.origins_fantasy.fae_two.name": "Fae",
    "origins.origins_fantasy.orc.name": "Ork",
    "power.origins_fantasy.fae_spryness.name": "Primded Fae",
    "power.origins_fantasy.ascended_na.name": "Houarnwisk uhelaet",
    "origins.origins_classes_iss.shadowcaster.name": "Hudour ar skeud",
    "power.origins_classes_iss.mystic_turn_undead.name": "Argas an divarvelien",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Kroc'hen derv",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Gwelet en noz",
    "Rotten Flesh": "Kig brein",
}

# Repair missing spaces between sentences without touching placeholders.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[A-ZÀ-ÖØ-Þ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/br_fr.json")):
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

print(f"Breton refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
