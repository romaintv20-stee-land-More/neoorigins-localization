#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive fixes for Origins/Minecraft terminology. Keep mod identity
# names stable and reuse current Minecraft Macedonian terms where available.
OVERRIDES = {
    "neoorigins.toggle.on": "Способноста е вклучена",
    "neoorigins.toggle.off": "Способноста е исклучена",
    "neoorigins.night_vision.on": "Ноќното гледање е вклучено",
    "neoorigins.night_vision.off": "Ноќното гледање е исклучено",
    "neoorigins.night_vision.disabled_by_server": "Ноќното гледање е оневозможено на овој сервер.",
    "neoorigins.night_vision.no_power": "Твојот Origin ја нема способноста Ноќно гледање.",
    "neoorigins.ultimine.no_power": "Твојот Origin ја нема способноста Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Класа",
    "screen.neoorigins.choose_origin": "Избери Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Избери Origin",
    "screen.neoorigins.choose.origins.layer.class": "Избери класа",
    "gui.neoorigins.search.label": "Пребарај Origin",
    "gui.neoorigins.picker.no_results": "Нема Origin што одговара на пребарувањето",
    "gui.neoorigins.hint.select": "Избери Origin за да ги видиш деталите",
    "gui.neoorigins.detail.powers_header": "Способности",
    "gui.neoorigins.power.key_tag.toggle": "[%s] Вклучи/исклучи",
    "gui.neoorigins.sort.class": "Класа",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Класна способност",
    "key.neoorigins.view_info": "Прикажи информации за Origin",
    "key.neoorigins.open_creator": "Отвори го создавачот на Origin",
    "key.neoorigins.open_mob_creator": "Отвори го создавачот на Mob Origin",
    "key.neoorigins.toggle_night_vision": "Вклучи/исклучи ноќно гледање",
    "key.category.neoorigins.hotkeys": "NeoOrigins (кратенки)",
    "screen.neoorigins.origin_info": "Информации за Origin",
    "screen.neoorigins.debug_powers": "Активни способности (debug)",
    "gui.neoorigins.info.no_origin": "Сè уште не е избран Origin.",
    "gui.neoorigins.info.your_origin": "Твојот Origin",
    "screen.neoorigins.origin_editor": "Уредувач на Origin",
    "gui.neoorigins.editor.layers_header": "Слоеви на Origin",
    "gui.neoorigins.editor.powers_header": "Дополнителни способности",
    "screen.neoorigins.creator": "Создавач на Origin",
    "gui.neoorigins.creator.tab.powers": "Способности",
    "gui.neoorigins.creator.apply": "Примени",
    "screen.neoorigins.mob_creator": "Создавач на Mob Origin",
    "gui.neoorigins.mob_creator.tab.powers": "Способности",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Правила за создавање",
    "gui.neoorigins.mob_creator.tab.drops": "Плен",
    "gui.neoorigins.mob_creator.apply": "Примени",
    "gui.neoorigins.debug.powers_header": "Доделени способности",

    # Canonical Origin identity names.
    "origins.neoorigins.human.name": "Човек",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    "power.neoorigins.merling_water_breathing.name": "Дишење под вода",
    "power.neoorigins.merling_night_vision.name": "Длабински вид",
    "power.neoorigins.merling_land_slowdown.name": "Забавување на копно",
    "power.neoorigins.merling_dries_out.name": "Исушување",
    "power.neoorigins.avian_no_fall_damage.name": "Лесна тежина",
    "power.neoorigins.avian_hollow_bones.name": "Шупливи коски",
    "power.neoorigins.blazeling_fire_immunity.name": "Огнено срце",
    "power.neoorigins.blazeling_blaze_scales.name": "Blaze лушпи",
    "power.neoorigins.blazeling_nether_born.name": "Роден во Недерот",
    "power.neoorigins.blazeling_nether_born.description": "Се движиш побрзо додека си во Недерот.",
    "power.neoorigins.blazeling_night_vision.name": "Термален вид",
    "power.neoorigins.caveborn_night_vision.name": "Приспособување на темнината",
    "power.neoorigins.caveborn_no_fall_damage.name": "Пештерски чекор",
    "power.neoorigins.caveborn_stone_fists.name": "Камени тупаници",
    "power.neoorigins.nether_fungus_diet.name": "Исхрана со габи од Недерот",
    "power.neoorigins.caveborn_eat_copper.name": "Вкус за бакар",
    "power.neoorigins.caveborn_eat_iron.name": "Вкус за железо",
    "power.neoorigins.caveborn_eat_gold.name": "Вкус за злато",
    "power.neoorigins.caveborn_eat_diamond.name": "Вкус за дијамант",
    "power.neoorigins.caveborn_eat_emerald.name": "Вкус за смарагд",
    "power.neoorigins.caveborn_eat_netherite.name": "Вкус за недерит",
    "power.neoorigins.caveborn_netherite_bonus.name": "Недеритно јадро",
    "power.neoorigins.golem_natural_armor.name": "Железна кожа",

    "origin.origins_furries.komodo.name": "Комодски змеј",
    "origin.origins_furries.otter.name": "Видра",
    "origin.origins_furries.raccoon.name": "Ракун",
    "power.origins_furries.charge.name": "Налет",
    "power.origins_furries.chicken_xp.name": "Пилешко искуство",
    "power.origins_furries.low_light_vision.name": "Гледање при слаба светлина",
    "power.origins_furries.low_light_vision.description": "Додека си над морското ниво, добиваш ефект Ноќно гледање.",
    "power.origins_furries.pavlov.name": "Павлов рефлекс",
    "power.origins_furries.raccoon_jump.name": "Скок на ракун",
    "power.origins_furries.night_vision.name": "Ноќно гледање",
    "power.origins_furries.night_vision.description": "Можеш да гледаш во темнина.",
    "power.origins_furries.scales.name": "Лушпи",
    "power.origins_furries.scales.description": "Твоите лушпи даваат +4 природен оклоп.",
    "power.origins_furries.heavy_wool.description": "Твојата густа волна дава +2 природен оклоп.",
    "power.origins_furries.fragile.description": "Твоето максимално здравје е за 2 срца помало од човечкото.",
    "power.origins_furries.soft.description": "Твоето максимално здравје е за 1 срце помало од човечкото.",
    "power.origins_furries.safe_meat.description": "Можеш безбедно да јадеш расипано месо и сурово овчо месо.",
    "power.origins_furries.trash_regen.description": "Јадењето расипано месо ти дава регенерација.",

    "screen.originsmodernui.title": "Избери Origin",
    "screen.originsmodernui.search_hint": "Пребарај Origin...",
    "screen.originsmodernui.choose_prompt": "Избери Origin од списокот",
    "screen.originsmodernui.profile": "Профил на ликот",
    "key.originsmodernui.open_profile": "Отвори го профилот на ликот",
    "key.originsmodernui.toggle_hud": "Вклучи/исклучи Origin Architect HUD",
    "originsmodernui.config.hud.position": "Позиција на HUD",
    "originsmodernui.config.hud.style": "Стил на HUD",
    "originsmodernui.config.hud.scale": "Големина на HUD",
    "originsmodernui.config.hud.opacity": "Проѕирност на HUD",
    "originsmodernui.config.hud.x_offset": "Хоризонтално поместување",
    "originsmodernui.config.hud.y_offset": "Вертикално поместување",
    "originsmodernui.config.hud.show_level": "Прикажи го нивото на Origin Architect",
    "originsmodernui.config.hud.show_points": "Прикажи непотрошени поени за особини",
    "originsmodernui.config.hud.show_xp_popup": "Прикажи добиено искуство",
    "originsmodernui.config.hud.show_level_popup": "Прикажи зголемување на нивото",
}

VALUE_REPLACEMENTS = {
    "Night Vision": "Ноќно гледање",
    "Netherite": "недерит",
    "Нетерајт": "недерит",
    "Нетерит": "недерит",
    "Pavloved": "Павлов рефлекс",
}

# MT sometimes joins sentences without a space. Only split terminal punctuation
# directly followed by a Cyrillic letter.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[А-Яа-яЀ-ӿ])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/mk_mk.json")):
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

print(f"Macedonian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
