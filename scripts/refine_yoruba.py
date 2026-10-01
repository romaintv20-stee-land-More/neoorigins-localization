#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive cleanup for highly visible UI, power/class names and config
# terminology. Origin / NeoOrigins remain canonical project/product terms. Core
# Minecraft wording follows the current Yoruba client where practical.
OVERRIDES = {
    # Core NeoOrigins UI.
    "neoorigins.toggle.on": "TAN",
    "neoorigins.toggle.off": "PA",
    "neoorigins.night_vision.on": "Alẹ Iran TAN",
    "neoorigins.night_vision.off": "Alẹ Iran PA",
    "neoorigins.night_vision.disabled_by_server": "Alẹ Iran ti wa ni PA lori olupin yii.",
    "neoorigins.night_vision.no_power": "Origin rẹ ko ni agbara Alẹ Iran.",
    "neoorigins.ultimine.no_power": "Origin rẹ ko ni agbara Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Kilasi",
    "screen.neoorigins.choose_origin": "Yan Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Yan Origin",
    "screen.neoorigins.choose.origins.layer.class": "Yan kilasi",
    "gui.neoorigins.search.label": "Wa Origins",
    "gui.neoorigins.picker.no_results": "Ko si Origin ti o ba wiwa mu",
    "gui.neoorigins.hint.select": "Yan Origin lati wo alaye",
    "gui.neoorigins.detail.powers_header": "Agbara",
    "gui.neoorigins.sort.class": "Kilasi",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Ọgbọn kilasi",
    "key.neoorigins.view_info": "Wo alaye Origin",
    "key.neoorigins.open_creator": "Ṣí Olùdá Origin",
    "key.neoorigins.open_mob_creator": "Ṣí Olùdá Mob Origin",
    "key.neoorigins.toggle_night_vision": "TAN/PA Alẹ Iran",
    "key.category.neoorigins.hotkeys": "NeoOrigins (awọn bọtini ọna abuja)",
    "screen.neoorigins.origin_info": "Alaye Origin",
    "gui.neoorigins.info.no_origin": "Ko si Origin ti a yan.",
    "gui.neoorigins.info.your_origin": "Origin rẹ",
    "screen.neoorigins.origin_editor": "Olootu Origin",
    "gui.neoorigins.editor.layers_header": "Awọn ipele Origin",
    "gui.neoorigins.editor.powers_header": "Awọn agbara afikun",
    "screen.neoorigins.creator": "Olùdá Origin",
    "gui.neoorigins.creator.tab.powers": "Agbara",
    "gui.neoorigins.creator.apply": "Waye",
    "screen.neoorigins.mob_creator": "Olùdá Mob Origin",
    "gui.neoorigins.mob_creator.tab.powers": "Agbara",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Awọn ofin spawn",
    "gui.neoorigins.mob_creator.tab.drops": "Awọn nkan ti o ṣubu",
    "gui.neoorigins.mob_creator.apply": "Waye",
    "gui.neoorigins.debug.powers_header": "Awọn agbara ti a fun",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fae",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "Duro lori ẹsẹ rẹ",
    "power.medievalorigins.banshee.hexed.name": "Eegun",
    "power.medievalorigins.pixie.pixie_properties.name": "Ara kekere",
    "origin.medievalorigins.high_elf.cryomancer.name": "Cryomancer",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "Irun-agutan wuwo",
    "entity.ibarnorigins.homing_wither_skull": "Agbari Wither ti n lepa",
    "power.ibarnorigins.witherskull.name": "Agbari Wither ti n lepa",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "Ikọlu ti o ga",
    "power.neoorigins.class_merchant_silver_tongue.name": "Ahọn fadaka",
    "power.neoorigins.class_cleric_turn_undead.name": "Lé awọn undead kuro",
    "power.neoorigins.class_paladin_turn_undead.name": "Lé awọn undead kuro",
    "power.neoorigins.sporeling_daylight_damage.name": "Ibajẹ imọlẹ ọjọ",
    "power.neoorigins.frostborn_freeze_aura.name": "Aura didi",
    "power.neoorigins.strider_fire_immunity.name": "Aabo ina",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Aabo projectile",
    "power.neoorigins.enderite_slow_fall.name": "Isubu Ender lọra",
    "power.neoorigins.enderite_water_damage.name": "Ailera Ender ninu omi",
    "power.neoorigins.enderian_teleport.name": "Teleport Ender",
    "power.neoorigins.feline_no_fall_damage.name": "Igbesi aye mẹsan",
    "power.neoorigins.draconic_fire_immunity.name": "Ẹjẹ dragoni",
    "power.neoorigins.cave_dragon_apex_hp.name": "Dragoni apex",
    "power.neoorigins.automaton_ascended_overclock.name": "Overclock",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Isopọ walẹ",
    "power.neoorigins.necromancer_irons_attunement.name": "Isopọ necrotic",
    "power.neoorigins.class_rogue_backstab.name": "Ikọlu lati ẹhin",
    "power.neoorigins.dwarf_darkvision.name": "Iran okunkun",
    "power.neoorigins.earth_mage_stonecunning.name": "Ọgbọn okuta",
    "power.neoorigins.dwarf_stonecunning.name": "Ọgbọn okuta",
    "power.neoorigins.stoneguard_stone_mining.name": "Iwakusa okuta",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Ṣiṣe ninu okunkun",
    "power.neoorigins.air_mage_zephyr.name": "Zephyr",
    "power.neoorigins.gravity_mage_unmoored.name": "Laisi oran",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Onigi",
    "neoorigins.configuration.class_lumberjack": "Onigi",
    "neoorigins.configuration.cinderborn_fireball": "Bọọlu ina Cinderborn",
    "neoorigins.configuration.elytrian_elytra_boost": "Ìgbéga Elytra ti Elytrian",
    "neoorigins.configuration.golem_fire_weakness": "Ailera Golem si ina",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Wiwo okuta Gorgon",
    "neoorigins.configuration.sculkborn_knockback_resist": "Atako knockback Sculkborn",
    "neoorigins.configuration.verdant_nether_damage": "Ibajẹ Nether Verdant",
    "neoorigins.configuration.warden_sonic_boom": "Ìbúgbàù Ohùn Warden",

    # Origins Fantasy / classes.
    "origins.origins_fantasy.fae.name": "Fae",
    "origins.origins_fantasy.fae_two.name": "Fae",
    "origins.origins_fantasy.orc.name": "Orc",
    "power.origins_fantasy.fae_spryness.name": "Iyara Fae",
    "power.origins_fantasy.ascended_na.name": "Ihamọra ti o ga",
    "origins.origins_classes_iss.shadowcaster.name": "Olupilẹṣẹ ojiji",
    "power.origins_classes_iss.mystic_turn_undead.name": "Lé awọn undead kuro",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Awọ oaku",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Alẹ Iran",
    "Rotten Flesh": "Eran run",
}

SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[A-ZÀ-ÖØ-ÞẸỌṢ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/yo_ng.json")):
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

print(f"Yoruba refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
