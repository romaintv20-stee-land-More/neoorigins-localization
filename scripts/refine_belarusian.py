#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive fixes for Origins/Minecraft terminology. Keep mod identity
# names stable and reuse current Minecraft Belarusian terms where available.
OVERRIDES = {
    "neoorigins.toggle.on": "Здольнасць уключана",
    "neoorigins.toggle.off": "Здольнасць выключана",
    "neoorigins.night_vision.on": "Начны зрок уключаны",
    "neoorigins.night_vision.off": "Начны зрок выключаны",
    "neoorigins.night_vision.disabled_by_server": "Начны зрок адключаны на гэтым серверы.",
    "neoorigins.night_vision.no_power": "Ваш Origin не мае здольнасці Начны зрок.",
    "neoorigins.ultimine.no_power": "Ваш Origin не мае здольнасці Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Клас",
    "screen.neoorigins.choose_origin": "Выбраць Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Выбраць Origin",
    "screen.neoorigins.choose.origins.layer.class": "Выбраць клас",
    "gui.neoorigins.search.label": "Пошук Origin",
    "gui.neoorigins.picker.no_results": "Няма Origin, якія адпавядаюць пошуку",
    "gui.neoorigins.hint.select": "Выберыце Origin, каб убачыць падрабязнасці",
    "gui.neoorigins.detail.powers_header": "Здольнасці",
    "gui.neoorigins.power.key_tag.toggle": "[%s] Укл./выкл.",
    "gui.neoorigins.sort.class": "Клас",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Класавая здольнасць",
    "key.neoorigins.view_info": "Паказаць інфармацыю пра Origin",
    "key.neoorigins.open_creator": "Адкрыць стваральнік Origin",
    "key.neoorigins.open_mob_creator": "Адкрыць стваральнік Mob Origin",
    "key.neoorigins.toggle_night_vision": "Уключыць/выключыць начны зрок",
    "key.category.neoorigins.hotkeys": "NeoOrigins (гарачыя клавішы)",
    "screen.neoorigins.origin_info": "Інфармацыя пра Origin",
    "screen.neoorigins.debug_powers": "Актыўныя здольнасці (debug)",
    "gui.neoorigins.info.no_origin": "Origin яшчэ не выбраны.",
    "gui.neoorigins.info.your_origin": "Ваш Origin",
    "screen.neoorigins.origin_editor": "Рэдактар Origin",
    "gui.neoorigins.editor.layers_header": "Слаі Origin",
    "gui.neoorigins.editor.powers_header": "Дадатковыя здольнасці",
    "screen.neoorigins.creator": "Стваральнік Origin",
    "gui.neoorigins.creator.tab.powers": "Здольнасці",
    "gui.neoorigins.creator.apply": "Прымяніць",
    "screen.neoorigins.mob_creator": "Стваральнік Mob Origin",
    "gui.neoorigins.mob_creator.tab.powers": "Здольнасці",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Правілы з'яўлення",
    "gui.neoorigins.mob_creator.tab.drops": "Здабыча",
    "gui.neoorigins.mob_creator.apply": "Прымяніць",
    "gui.neoorigins.debug.powers_header": "Прызначаныя здольнасці",

    "origins.neoorigins.human.name": "Чалавек",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    "power.neoorigins.merling_water_breathing.name": "Дыханне пад вадой",
    "power.neoorigins.merling_night_vision.name": "Глыбінны зрок",
    "power.neoorigins.merling_land_slowdown.name": "Запаволенне на сушы",
    "power.neoorigins.merling_dries_out.name": "Высыханне",
    "power.neoorigins.avian_no_fall_damage.name": "Лёгкая вага",
    "power.neoorigins.avian_hollow_bones.name": "Полыя косці",
    "power.neoorigins.blazeling_fire_immunity.name": "Вогненнае сэрца",
    "power.neoorigins.blazeling_blaze_scales.name": "Луска Blaze",
    "power.neoorigins.blazeling_nether_born.name": "Народжаны ў Нэдары",
    "power.neoorigins.blazeling_nether_born.description": "Вы рухаецеся хутчэй, калі знаходзіцеся ў Нэдары.",
    "power.neoorigins.blazeling_night_vision.name": "Цеплавы зрок",
    "power.neoorigins.caveborn_night_vision.name": "Адаптацыя да цемры",
    "power.neoorigins.caveborn_no_fall_damage.name": "Пячорны крок",
    "power.neoorigins.caveborn_stone_fists.name": "Каменныя кулакі",
    "power.neoorigins.nether_fungus_diet.name": "Рацыён з грыбоў Нэдара",
    "power.neoorigins.caveborn_eat_copper.name": "Смак да медзі",
    "power.neoorigins.caveborn_eat_iron.name": "Смак да жалеза",
    "power.neoorigins.caveborn_eat_gold.name": "Смак да золата",
    "power.neoorigins.caveborn_eat_diamond.name": "Смак да алмазаў",
    "power.neoorigins.caveborn_eat_emerald.name": "Смак да смарагдаў",
    "power.neoorigins.caveborn_eat_netherite.name": "Смак да нэдарыту",
    "power.neoorigins.caveborn_netherite_bonus.name": "Нэдарытавае ядро",
    "power.neoorigins.golem_natural_armor.name": "Жалезная скура",

    "origin.origins_furries.komodo.name": "Комадскі варан",
    "origin.origins_furries.otter.name": "Выдра",
    "origin.origins_furries.raccoon.name": "Янот",
    "power.origins_furries.charge.name": "Рывок",
    "power.origins_furries.chicken_xp.name": "Курыны досвед",
    "power.origins_furries.low_light_vision.name": "Зрок пры слабым святле",
    "power.origins_furries.low_light_vision.description": "Калі вы знаходзіцеся вышэй за ўзровень мора, вы атрымліваеце эфект Начны зрок.",
    "power.origins_furries.pavlov.name": "Рэфлекс Паўлава",
    "power.origins_furries.raccoon_jump.name": "Скачок янота",
    "power.origins_furries.night_vision.name": "Начны зрок",
    "power.origins_furries.night_vision.description": "Вы бачыце ў цемры.",
    "power.origins_furries.scales.name": "Луска",
    "power.origins_furries.scales.description": "Ваша луска дае +4 натуральнай брані.",
    "power.origins_furries.heavy_wool.description": "Ваша густая воўна дае +2 натуральнай брані.",
    "power.origins_furries.fragile.description": "Ваша максімальнае здароўе на 2 сэрцы меншае за чалавечае.",
    "power.origins_furries.soft.description": "Ваша максімальнае здароўе на 1 сэрца меншае за чалавечае.",
    "power.origins_furries.safe_meat.description": "Вы можаце бяспечна есці гнілую плоць і сырую бараніну.",
    "power.origins_furries.trash_regen.description": "Ужыванне гнілой плоці дае вам рэгенерацыю.",

    "screen.originsmodernui.title": "Выбраць Origin",
    "screen.originsmodernui.search_hint": "Пошук Origin...",
    "screen.originsmodernui.choose_prompt": "Выберыце Origin са спісу",
    "screen.originsmodernui.profile": "Профіль персанажа",
    "key.originsmodernui.open_profile": "Адкрыць профіль персанажа",
    "key.originsmodernui.toggle_hud": "Уключыць/выключыць HUD Origin Architect",
    "originsmodernui.config.hud.position": "Пазіцыя HUD",
    "originsmodernui.config.hud.style": "Стыль HUD",
    "originsmodernui.config.hud.scale": "Маштаб HUD",
    "originsmodernui.config.hud.opacity": "Непразрыстасць HUD",
    "originsmodernui.config.hud.x_offset": "Гарызантальны зрух",
    "originsmodernui.config.hud.y_offset": "Вертыкальны зрух",
    "originsmodernui.config.hud.show_level": "Паказваць узровень Origin Architect",
    "originsmodernui.config.hud.show_points": "Паказваць нявыкарыстаныя ачкі рыс",
    "originsmodernui.config.hud.show_xp_popup": "Паказваць атрыманы досвед",
    "originsmodernui.config.hud.show_level_popup": "Паказваць павышэнне ўзроўню",
}

VALUE_REPLACEMENTS = {
    "Night Vision": "Начны зрок",
    "Netherite": "нэдарыт",
    "Незерит": "нэдарыт",
    "Нетэрит": "нэдарыт",
    "Pavloved": "Рэфлекс Паўлава",
}

SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[А-Яа-яЁёІіЎў])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/be_by.json")):
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

print(f"Belarusian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
