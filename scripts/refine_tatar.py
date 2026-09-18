#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Deterministic contextual pass. Product names such as Origin/NeoOrigins remain
# canonical; common Minecraft terminology follows the current tt_ru vocabulary.
OVERRIDES = {
    "neoorigins.toggle.on": "Сәләт кабызылды",
    "neoorigins.toggle.off": "Сәләт сүндерелде",
    "neoorigins.night_vision.on": "Төн күрү кабызылды",
    "neoorigins.night_vision.off": "Төн күрү сүндерелде",
    "neoorigins.night_vision.disabled_by_server": "Бу серверда Төн күрү сүндерелгән.",
    "neoorigins.night_vision.no_power": "Сезнең Origin-да Төн күрү сәләте юк.",
    "neoorigins.ultimine.no_power": "Сезнең Origin-да Ultimine сәләте юк.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Класс",
    "screen.neoorigins.choose_origin": "Origin сайлагыз",
    "screen.neoorigins.choose.origins.layer.origin": "Origin сайлагыз",
    "screen.neoorigins.choose.origins.layer.class": "Класс сайлагыз",
    "gui.neoorigins.search.label": "Origin эзләү",
    "gui.neoorigins.picker.no_results": "Эзләвегезгә туры килгән Origin табылмады",
    "gui.neoorigins.hint.select": "Тулы мәгълүматны карау өчен Origin сайлагыз",
    "gui.neoorigins.detail.powers_header": "Сәләтләр",
    "gui.neoorigins.sort.class": "Класс",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Класс сәләте",
    "key.neoorigins.view_info": "Origin турында мәгълүматны карау",
    "key.neoorigins.open_creator": "Origin төзүчесен ачу",
    "key.neoorigins.open_mob_creator": "Mob Origin төзүчесен ачу",
    "key.neoorigins.toggle_night_vision": "Төн күрүне кабызу/сүндерү",
    "key.category.neoorigins.hotkeys": "NeoOrigins (тиз төймәләр)",
    "screen.neoorigins.origin_info": "Origin турында мәгълүмат",
    "gui.neoorigins.info.no_origin": "Origin әле сайланмаган.",
    "gui.neoorigins.info.your_origin": "Сезнең Origin",
    "screen.neoorigins.origin_editor": "Origin мөхәррире",
    "gui.neoorigins.editor.layers_header": "Origin катламнары",
    "gui.neoorigins.editor.powers_header": "Өстәмә сәләтләр",
    "screen.neoorigins.creator": "Origin төзүчесе",
    "gui.neoorigins.creator.tab.powers": "Сәләтләр",
    "gui.neoorigins.creator.apply": "Куллану",
    "screen.neoorigins.mob_creator": "Mob Origin төзүчесе",
    "gui.neoorigins.mob_creator.tab.powers": "Сәләтләр",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Барлыкка килү кагыйдәләре",
    "gui.neoorigins.mob_creator.tab.drops": "Табыш",
    "gui.neoorigins.mob_creator.apply": "Куллану",
    "gui.neoorigins.debug.powers_header": "Бирелгән сәләтләр",

    # High-visibility add-on names.
    "origin.medievalorigins.fae.name": "Фея",
    "origin.medievalorigins.yeti.name": "Йети",
    "power.medievalorigins.alfiq.on_your_feet.name": "Аякка басу",
    "power.medievalorigins.banshee.hexed.name": "Каргалган",
    "power.medievalorigins.pixie.pixie_properties.name": "Бик кечкенә",
    "origin.medievalorigins.high_elf.cryomancer.name": "Криомант",
    "power.origins_furries.heavy_wool.name": "Куе йон",
    "entity.ibarnorigins.homing_wither_skull": "Максатка юнәлгән Wither баш сөяге",
    "power.ibarnorigins.witherskull.name": "Максатка юнәлгән Wither баш сөяге",

    # NeoOrigins powers/classes.
    "power.neoorigins.draconic_ascended_attack.name": "Көчәйтелгән көч",
    "power.neoorigins.class_merchant_silver_tongue.name": "Көмеш тел",
    "power.neoorigins.class_cleric_turn_undead.name": "Үлеләрне кире кагу",
    "power.neoorigins.class_paladin_turn_undead.name": "Үлеләрне кире кагу",
    "power.neoorigins.sporeling_daylight_damage.name": "Кояш яндыруы",
    "power.neoorigins.frostborn_freeze_aura.name": "Салкынлык дулкыны",
    "power.neoorigins.strider_fire_immunity.name": "Лавада туган",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Тавыш дулкынын кире кагу",
    "power.neoorigins.enderite_slow_fall.name": "Эндер йөзүе",
    "power.neoorigins.enderite_water_damage.name": "Эндер көчсезлеге",
    "power.neoorigins.enderian_teleport.name": "Эндер телепортациясе",
    "power.neoorigins.feline_no_fall_damage.name": "Тугыз гомер",
    "power.neoorigins.draconic_fire_immunity.name": "Аждаһа каны",
    "power.neoorigins.class_rogue_backstab.name": "Аркадан сугу",
    "power.neoorigins.dwarf_darkvision.name": "Караңгыда күрү",
    "power.neoorigins.dwarf_stonecunning.name": "Таш белеме",
    "power.neoorigins.earth_mage_stonecunning.name": "Таш белеме",
    "power.neoorigins.stoneguard_stone_mining.name": "Таш җимерүче",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Күләгә йөгерүе",
    "power.neoorigins.air_mage_zephyr.name": "Зефир",

    # Configuration labels.
    "neoorigins.configuration.classes.class_lumberjack": "Урманчы",
    "neoorigins.configuration.class_lumberjack": "Урманчы",
    "neoorigins.configuration.cinderborn_fireball": "Cinderborn ут шары",
    "neoorigins.configuration.elytrian_elytra_boost": "Elytrian Elytra көчәйтүе",
    "neoorigins.configuration.golem_fire_weakness": "Големның утка көчсезлеге",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Горгонаның ташка әйләндерүче карашы",
    "neoorigins.configuration.sculkborn_knockback_resist": "Sculkborn кире кагуга каршылыгы",
    "neoorigins.configuration.verdant_nether_damage": "Verdant Незер зыяны",
    "neoorigins.configuration.warden_sonic_boom": "Warden тавыш дулкыны",

    # Origins Fantasy / classes / backgrounds.
    "origins.origins_fantasy.fae.name": "Фея",
    "origins.origins_fantasy.fae_two.name": "Фея",
    "origins.origins_fantasy.orc.name": "Орк",
    "power.origins_fantasy.fae_spryness.name": "Фея җитезлеге",
    "origins.origins_classes_iss.shadowcaster.name": "Күләгә тылсымчысы",
    "power.origins_classes_iss.mystic_turn_undead.name": "Үлеләрне кире кагу",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Имән тире саклавы",
    "origin.origins_backgrounds_two.disenchanter.name": "Тылсымны бетерүче",
    "origins.origins_classes_ex.duskblade.name": "Эңгер кылычы",
    "power.origins_classes_ex.heavy_armor_nerf.name": "Авыр җиһаз",
    "power.origins_classes_ex.offhand_defense.name": "Икенче кул саклавы",
    "power.origins_classes_ex.armor_weakness.name": "Җиһаз — авыр",
    "power.origins_classes_ex.void_gaze.name": "Бушлык карашы",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Төн күрү",
    "Rotten Flesh": "Черек ит",
}

SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[А-Яа-яЁёӘәӨөҮүҖҗҢңҺһ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/tt_ru.json")):
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
print(f"Tatar refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
