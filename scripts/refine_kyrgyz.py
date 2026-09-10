#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

OVERRIDES = {
    "neoorigins.toggle.on": "Жөндөм күйгүзүлдү",
    "neoorigins.toggle.off": "Жөндөм өчүрүлдү",
    "neoorigins.night_vision.on": "Түнкү көрүү күйгүзүлдү",
    "neoorigins.night_vision.off": "Түнкү көрүү өчүрүлдү",
    "neoorigins.night_vision.disabled_by_server": "Бул серверде түнкү көрүү өчүрүлгөн.",
    "neoorigins.night_vision.no_power": "Сиздин Origin'иңизде түнкү көрүү жөндөмү жок.",
    "neoorigins.ultimine.no_power": "Сиздин Origin'иңизде Ultimine жөндөмү жок.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Класс",
    "screen.neoorigins.choose_origin": "Origin тандаңыз",
    "screen.neoorigins.choose.origins.layer.origin": "Origin тандаңыз",
    "screen.neoorigins.choose.origins.layer.class": "Класс тандаңыз",
    "gui.neoorigins.search.label": "Origin издөө",
    "gui.neoorigins.picker.no_results": "Издөөңүзгө туура келген Origin табылган жок",
    "gui.neoorigins.hint.select": "Толук маалыматты көрүү үчүн Origin тандаңыз",
    "gui.neoorigins.detail.powers_header": "Жөндөмдөр",
    "gui.neoorigins.sort.class": "Класс",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Класс жөндөмү",
    "key.neoorigins.view_info": "Origin маалыматын көрүү",
    "key.neoorigins.open_creator": "Origin түзүүчүсүн ачуу",
    "key.neoorigins.open_mob_creator": "Mob Origin түзүүчүсүн ачуу",
    "key.neoorigins.toggle_night_vision": "Түнкү көрүүнү күйгүзүү/өчүрүү",
    "key.category.neoorigins.hotkeys": "NeoOrigins (ыкчам баскычтар)",
    "screen.neoorigins.origin_info": "Origin маалыматы",
    "gui.neoorigins.info.no_origin": "Origin азырынча тандала элек.",
    "gui.neoorigins.info.your_origin": "Сиздин Origin'иңиз",
    "screen.neoorigins.origin_editor": "Origin редактору",
    "gui.neoorigins.editor.layers_header": "Origin катмарлары",
    "gui.neoorigins.editor.powers_header": "Кошумча жөндөмдөр",
    "screen.neoorigins.creator": "Origin түзүүчүсү",
    "gui.neoorigins.creator.tab.powers": "Жөндөмдөр",
    "gui.neoorigins.creator.apply": "Колдонуу",
    "screen.neoorigins.mob_creator": "Mob Origin түзүүчүсү",
    "gui.neoorigins.mob_creator.tab.powers": "Жөндөмдөр",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Пайда болуу эрежелери",
    "gui.neoorigins.mob_creator.tab.drops": "Түшүмдөр",
    "gui.neoorigins.mob_creator.apply": "Колдонуу",
    "gui.neoorigins.debug.powers_header": "Берилген жөндөмдөр",

    # Medieval Origins: repair untranslated / malformed title values.
    "origin.medievalorigins.fae.name": "Фей",
    "origin.medievalorigins.yeti.name": "Йети",
    "power.medievalorigins.alfiq.on_your_feet.name": "Бутка туруу",
    "power.medievalorigins.banshee.hexed.name": "Каргыш тийген",
    "power.medievalorigins.pixie.pixie_properties.name": "Кыпкычтай кичинекей",
    "origin.medievalorigins.high_elf.cryomancer.name": "Криомант",

    # Origins Furries.
    "power.origins_furries.heavy_wool.name": "Калың жүн",

    # ibarn quartet add-on.
    "entity.ibarnorigins.homing_wither_skull": "Бутага багытталган Wither баш сөөгү",
    "power.ibarnorigins.witherskull.name": "Бутага багытталган Wither баш сөөгү",

    # NeoOrigins powers/classes where machine translation left English or mangled it.
    "power.neoorigins.draconic_ascended_attack.name": "Жогорулатылган күч",
    "power.neoorigins.class_merchant_silver_tongue.name": "Күмүш тил",
    "power.neoorigins.class_cleric_turn_undead.name": "Өлбөстөрдү кайтаруу",
    "power.neoorigins.class_paladin_turn_undead.name": "Өлбөстөрдү кайтаруу",
    "power.neoorigins.sporeling_daylight_damage.name": "Күн күйдүрүүсү",
    "power.neoorigins.frostborn_freeze_aura.name": "Аяз жарылуусу",
    "power.neoorigins.strider_fire_immunity.name": "Лавада төрөлгөн",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Үн толкунун кайтаруу",
    "power.neoorigins.enderite_slow_fall.name": "Эндер сүзүүсү",
    "power.neoorigins.enderite_water_damage.name": "Эндер алсыздыгы",
    "power.neoorigins.enderian_teleport.name": "Эндер телепортациясы",
    "power.neoorigins.feline_no_fall_damage.name": "Тогуз өмүр",
    "power.neoorigins.draconic_fire_immunity.name": "Ажыдаар каны",
    "power.neoorigins.cave_dragon_apex_hp.name": "Чоку ажыдаар",
    "power.neoorigins.automaton_ascended_overclock.name": "Ашыкча ылдамдатуу",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Гравитургиялык шайкештик",
    "power.neoorigins.necromancer_irons_attunement.name": "Өлүмгө байланышкан шайкештик",
    "power.neoorigins.class_rogue_backstab.name": "Аркадан сокку",
    "power.neoorigins.dwarf_darkvision.name": "Караңгыда көрүү",
    "power.neoorigins.dwarf_stonecunning.name": "Таш билгичтик",
    "power.neoorigins.earth_mage_stonecunning.name": "Таш билгичтик",
    "power.neoorigins.stoneguard_stone_mining.name": "Таш талкалоочу",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Көлөкө чуркоо",
    "power.neoorigins.air_mage_zephyr.name": "Зефир",
    "power.neoorigins.gravity_mage_unmoored.name": "Байланбаган",
    "origins.neoorigins.darkness_mage.description": "Көлөкө токуган сыйкырчы, айланып жүргөн көлөкө шарларын чакырып, караңгылык көлмөлөрүнүн арасында кадам таштайт. Түнкүсүн жашыруун жана кооптуу, бирок күн нуру күчүңүздү күйгүзүп жок кылат.",

    # Configuration labels should be readable Kyrgyz while keeping canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Токойчу",
    "neoorigins.configuration.class_lumberjack": "Токойчу",
    "neoorigins.configuration.cinderborn_fireball": "Cinderborn от шары",
    "neoorigins.configuration.elytrian_elytra_boost": "Elytrian Elytra күчөтүүсү",
    "neoorigins.configuration.golem_fire_weakness": "Големдин отко алсыздыгы",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Горгондун ташка айлантуучу көз карашы",
    "neoorigins.configuration.sculkborn_knockback_resist": "Sculkborn түртүлүүгө каршылыгы",
    "neoorigins.configuration.verdant_nether_damage": "Verdant Незер зыяны",
    "neoorigins.configuration.warden_sonic_boom": "Warden үн жарылуусу",

    # Origins Fantasy.
    "origins.origins_fantasy.fae.name": "Фей",
    "origins.origins_fantasy.fae_two.name": "Фей",
    "origins.origins_fantasy.orc.name": "Орк",
    "power.origins_fantasy.fae_spryness.name": "Фей шамдагайлыгы",
    "power.origins_fantasy.ascended_na.name": "Жогорулатылган соот",

    # Classes / backgrounds add-ons.
    "origins.origins_classes_iss.shadowcaster.name": "Көлөкө сыйкырчысы",
    "power.origins_classes_iss.mystic_turn_undead.name": "Өлбөстөрдү кайтаруу",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Эмен тери коргонуусу",
    "origin.origins_backgrounds_two.disenchanter.name": "Сыйкырсыздандыруучу",
    "origins.origins_classes_ex.duskblade.name": "Күүгүм кылычы",
    "power.origins_classes_ex.heavy_armor_nerf.name": "Ыңгайсыз соот",
    "power.origins_classes_ex.offhand_defense.name": "Кошумча кол коргонуусу",
    "power.origins_classes_ex.armor_weakness.name": "Соот — оор",
    "power.origins_classes_ex.void_gaze.name": "Боштук көрүнүшү",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Түнкү көрүнүш": "Түнкү көрүү",
    "Нетерит": "Незерит",
    "Netherite": "Незерит",
}

SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[А-Яа-яЁёҢңӨөҮү])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/ky_kg.json")):
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
print(f"Kyrgyz refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
