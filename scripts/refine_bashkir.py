#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Deterministic context pass. Product names such as Origin/NeoOrigins stay canonical;
# Minecraft terms follow the current official ba_ru localization where useful.
OVERRIDES = {
    "neoorigins.toggle.on": "Һәләт ҡабыҙылды",
    "neoorigins.toggle.off": "Һәләт һүндерелде",
    "neoorigins.night_vision.on": "Төнгө күренеслек ҡабыҙылды",
    "neoorigins.night_vision.off": "Төнгө күренеслек һүндерелде",
    "neoorigins.night_vision.disabled_by_server": "Был серверҙа Төнгө күренеслек һүндерелгән.",
    "neoorigins.night_vision.no_power": "Һеҙҙең Origin-да Төнгө күренеслек һәләте юҡ.",
    "neoorigins.ultimine.no_power": "Һеҙҙең Origin-да Ultimine һәләте юҡ.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Класс",
    "screen.neoorigins.choose_origin": "Origin һайлағыҙ",
    "screen.neoorigins.choose.origins.layer.origin": "Origin һайлағыҙ",
    "screen.neoorigins.choose.origins.layer.class": "Класс һайлағыҙ",
    "gui.neoorigins.search.label": "Origin эҙләү",
    "gui.neoorigins.picker.no_results": "Эҙләүегеҙгә тап килгән Origin табылманы",
    "gui.neoorigins.hint.select": "Тулы мәғлүмәтте ҡарау өсөн Origin һайлағыҙ",
    "gui.neoorigins.detail.powers_header": "Һәләттәр",
    "gui.neoorigins.sort.class": "Класс",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Класс һәләте",
    "key.neoorigins.view_info": "Origin тураһында мәғлүмәтте ҡарау",
    "key.neoorigins.open_creator": "Origin булдырыусыны асыу",
    "key.neoorigins.open_mob_creator": "Mob Origin булдырыусыны асыу",
    "key.neoorigins.toggle_night_vision": "Төнгө күренеслекте ҡабыҙыу/һүндереү",
    "key.category.neoorigins.hotkeys": "NeoOrigins (тиҙ төймәләр)",
    "screen.neoorigins.origin_info": "Origin тураһында мәғлүмәт",
    "gui.neoorigins.info.no_origin": "Origin әлегә һайланмаған.",
    "gui.neoorigins.info.your_origin": "Һеҙҙең Origin",
    "screen.neoorigins.origin_editor": "Origin мөхәррире",
    "gui.neoorigins.editor.layers_header": "Origin ҡатламдары",
    "gui.neoorigins.editor.powers_header": "Өҫтәмә һәләттәр",
    "screen.neoorigins.creator": "Origin булдырыусы",
    "gui.neoorigins.creator.tab.powers": "Һәләттәр",
    "gui.neoorigins.creator.apply": "Ҡулланыу",
    "screen.neoorigins.mob_creator": "Mob Origin булдырыусы",
    "gui.neoorigins.mob_creator.tab.powers": "Һәләттәр",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Пәйҙә булыу ҡағиҙәләре",
    "gui.neoorigins.mob_creator.tab.drops": "Табыш",
    "gui.neoorigins.mob_creator.apply": "Ҡулланыу",
    "gui.neoorigins.debug.powers_header": "Бирелгән һәләттәр",

    # Medieval Origins / add-ons: fix short visible names that machine translation
    # commonly leaves English or translates too literally.
    "origin.medievalorigins.fae.name": "Фея",
    "origin.medievalorigins.yeti.name": "Йети",
    "power.medievalorigins.alfiq.on_your_feet.name": "Аяҡҡа баҫыу",
    "power.medievalorigins.banshee.hexed.name": "Ҡәһәрләнгән",
    "power.medievalorigins.pixie.pixie_properties.name": "Бик бәләкәй",
    "origin.medievalorigins.high_elf.cryomancer.name": "Криомант",
    "power.origins_furries.heavy_wool.name": "Ҡуйы йөн",
    "entity.ibarnorigins.homing_wither_skull": "Маҡсатҡа йүнәлгән Wither баш һөйәге",
    "power.ibarnorigins.witherskull.name": "Маҡсатҡа йүнәлгән Wither баш һөйәге",

    # NeoOrigins powers/classes.
    "power.neoorigins.draconic_ascended_attack.name": "Көсәйтелгән көс",
    "power.neoorigins.class_merchant_silver_tongue.name": "Көмөш тел",
    "power.neoorigins.class_cleric_turn_undead.name": "Үлеләрҙе кире ҡағыу",
    "power.neoorigins.class_paladin_turn_undead.name": "Үлеләрҙе кире ҡағыу",
    "power.neoorigins.sporeling_daylight_damage.name": "Ҡояш яндырыуы",
    "power.neoorigins.frostborn_freeze_aura.name": "Һалҡынлыҡ тулҡыны",
    "power.neoorigins.strider_fire_immunity.name": "Лавала тыуған",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Тауыш тулҡынын кире ҡағыу",
    "power.neoorigins.enderite_slow_fall.name": "Эндер йөҙөүе",
    "power.neoorigins.enderite_water_damage.name": "Эндер көсһөҙлөгө",
    "power.neoorigins.enderian_teleport.name": "Эндер телепортацияһы",
    "power.neoorigins.feline_no_fall_damage.name": "Туғыҙ ғүмер",
    "power.neoorigins.draconic_fire_immunity.name": "Аждаһа ҡаны",
    "power.neoorigins.cave_dragon_apex_hp.name": "Юғары аждаһа",
    "power.neoorigins.automaton_ascended_overclock.name": "Үтә тиҙләтеү",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Гравитургик көйләнеш",
    "power.neoorigins.necromancer_irons_attunement.name": "Үлем көйләнеше",
    "power.neoorigins.class_rogue_backstab.name": "Арҡанан һуғыу",
    "power.neoorigins.dwarf_darkvision.name": "Ҡараңғыла күреү",
    "power.neoorigins.dwarf_stonecunning.name": "Таш белеме",
    "power.neoorigins.earth_mage_stonecunning.name": "Таш белеме",
    "power.neoorigins.stoneguard_stone_mining.name": "Таш емереүсе",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Күләгә йүгереүе",
    "power.neoorigins.air_mage_zephyr.name": "Зефир",
    "power.neoorigins.gravity_mage_unmoored.name": "Бәйләнмәгән",

    # Configuration labels: readable Bashkir while keeping canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Урмансы",
    "neoorigins.configuration.class_lumberjack": "Урмансы",
    "neoorigins.configuration.cinderborn_fireball": "Cinderborn ут шары",
    "neoorigins.configuration.elytrian_elytra_boost": "Elytrian Elytra көсәйтеүе",
    "neoorigins.configuration.golem_fire_weakness": "Големдың утҡа көсһөҙлөгө",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Горгонаның ташҡа әйләндереүсе ҡарашы",
    "neoorigins.configuration.sculkborn_knockback_resist": "Sculkborn этәреүгә ҡаршылығы",
    "neoorigins.configuration.verdant_nether_damage": "Verdant Незер зыяны",
    "neoorigins.configuration.warden_sonic_boom": "Warden тауыш тулҡыны",

    # Origins Fantasy / classes / backgrounds.
    "origins.origins_fantasy.fae.name": "Фея",
    "origins.origins_fantasy.fae_two.name": "Фея",
    "origins.origins_fantasy.orc.name": "Орк",
    "power.origins_fantasy.fae_spryness.name": "Фея етеҙлеге",
    "power.origins_fantasy.ascended_na.name": "Көсәйтелгән жәбә",
    "origins.origins_classes_iss.shadowcaster.name": "Күләгә тылсымсыһы",
    "power.origins_classes_iss.mystic_turn_undead.name": "Үлеләрҙе кире ҡағыу",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Имән тире һаҡлауы",
    "origin.origins_backgrounds_two.disenchanter.name": "Тылсымды бөтөрөүсе",
    "origins.origins_classes_ex.duskblade.name": "Эңер ҡылысы",
    "power.origins_classes_ex.heavy_armor_nerf.name": "Ауыр жәбә",
    "power.origins_classes_ex.offhand_defense.name": "Икенсе ҡул һаҡлауы",
    "power.origins_classes_ex.armor_weakness.name": "Жәбә — ауыр",
    "power.origins_classes_ex.void_gaze.name": "Бушлыҡ ҡарашы",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Төнгө күренеслек",
    "Rotten Flesh": "Серек ит",
    "Netherite": "Неҙерит",
    "Нетерит": "Неҙерит",
    "Незерит": "Неҙерит",
}

SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[А-Яа-яЁёӘәӨөҮүҒғҠҡҢңҘҙҪҫҺһ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/ba_ru.json")):
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
print(f"Bashkir refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
