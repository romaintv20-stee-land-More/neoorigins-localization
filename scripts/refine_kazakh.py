#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive fixes. Keep mod identity names stable and prefer terminology
# already used by Minecraft's current Kazakh localization where available.
OVERRIDES = {
    "neoorigins.toggle.on": "Қабілет қосулы",
    "neoorigins.toggle.off": "Қабілет өшірілген",
    "neoorigins.night_vision.on": "Түнде көру қосулы",
    "neoorigins.night_vision.off": "Түнде көру өшірілген",
    "neoorigins.night_vision.disabled_by_server": "Бұл серверде түнде көру өшірілген.",
    "neoorigins.night_vision.no_power": "Сіздің Origin-іңізде түнде көру қабілеті жоқ.",
    "neoorigins.ultimine.no_power": "Сіздің Origin-іңізде Ultimine қабілеті жоқ.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Класс",
    "screen.neoorigins.choose_origin": "Origin таңдаңыз",
    "screen.neoorigins.choose.origins.layer.origin": "Origin таңдаңыз",
    "screen.neoorigins.choose.origins.layer.class": "Класс таңдаңыз",
    "gui.neoorigins.search.label": "Origin іздеу",
    "gui.neoorigins.picker.no_results": "Іздеуіңізге сәйкес Origin табылмады",
    "gui.neoorigins.hint.select": "Толық мәліметті көру үшін Origin таңдаңыз",
    "gui.neoorigins.detail.powers_header": "Қабілеттер",
    "gui.neoorigins.sort.class": "Класс",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Класс қабілеті",
    "key.neoorigins.view_info": "Origin мәліметін көру",
    "key.neoorigins.open_creator": "Origin жасаушысын ашу",
    "key.neoorigins.open_mob_creator": "Mob Origin жасаушысын ашу",
    "key.neoorigins.toggle_night_vision": "Түнде көруді қосу/өшіру",
    "key.category.neoorigins.hotkeys": "NeoOrigins (жылдам пернелер)",
    "screen.neoorigins.origin_info": "Origin мәліметі",
    "gui.neoorigins.info.no_origin": "Origin әлі таңдалмаған.",
    "gui.neoorigins.info.your_origin": "Сіздің Origin-іңіз",
    "screen.neoorigins.origin_editor": "Origin редакторы",
    "gui.neoorigins.editor.layers_header": "Origin қабаттары",
    "gui.neoorigins.editor.powers_header": "Қосымша қабілеттер",
    "screen.neoorigins.creator": "Origin жасаушысы",
    "gui.neoorigins.creator.tab.powers": "Қабілеттер",
    "gui.neoorigins.creator.apply": "Қолдану",
    "screen.neoorigins.mob_creator": "Mob Origin жасаушысы",
    "gui.neoorigins.mob_creator.tab.powers": "Қабілеттер",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Пайда болу ережелері",
    "gui.neoorigins.mob_creator.tab.drops": "Олжа",
    "gui.neoorigins.mob_creator.apply": "Қолдану",
    "gui.neoorigins.debug.powers_header": "Берілген қабілеттер",

    # Canonical Origin identity names: do not literal-translate the mod identities.
    "origins.neoorigins.human.name": "Адам",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    "power.neoorigins.merling_water_breathing.name": "Су астында тыныс алу",
    "power.neoorigins.merling_night_vision.name": "Тереңдікте көру",
    "power.neoorigins.merling_land_slowdown.name": "Құрлықтағы баяулық",
    "power.neoorigins.merling_dries_out.name": "Құрғау",
    "power.neoorigins.avian_no_fall_damage.name": "Жеңіл салмақ",
    "power.neoorigins.avian_hollow_bones.name": "Қуыс сүйектер",
    "power.neoorigins.blazeling_fire_immunity.name": "От жүрегі",
    "power.neoorigins.blazeling_blaze_scales.name": "Blaze қабыршақтары",
    "power.neoorigins.blazeling_nether_born.name": "Незерде туған",
    "power.neoorigins.blazeling_nether_born.description": "Незерде жүргенде жылдамырақ қозғаласыз.",
    "power.neoorigins.blazeling_night_vision.name": "Жылулық көру",
    "power.neoorigins.caveborn_night_vision.name": "Қараңғылыққа бейімделу",
    "power.neoorigins.caveborn_no_fall_damage.name": "Үңгір қадамы",
    "power.neoorigins.caveborn_stone_fists.name": "Тас жұдырықтар",
    "power.neoorigins.caveborn_mining_fortune.name": "Қазу Fortune-ы",
    "power.neoorigins.nether_fungus_diet.name": "Незер саңырауқұлақтарының диетасы",
    "power.neoorigins.nether_fungus_diet.description": "Незердегі warped және crimson саңырауқұлақтарын тағам ретінде жей аласыз; олар 5 аштық пен 0,6 қанығуды қалпына келтіреді. Тоқ кезде жей алмайсыз.",
    "power.neoorigins.caveborn_eat_copper.name": "Мыстың дәмі",
    "power.neoorigins.caveborn_eat_iron.name": "Темірдің дәмі",
    "power.neoorigins.caveborn_eat_gold.name": "Алтынның дәмі",
    "power.neoorigins.caveborn_eat_diamond.name": "Алмастың дәмі",
    "power.neoorigins.caveborn_eat_emerald.name": "Изумрудтың дәмі",
    "power.neoorigins.caveborn_eat_netherite.name": "Незериттің дәмі",
    "power.neoorigins.caveborn_netherite_bonus.name": "Незерит өзегі",
    "power.neoorigins.golem_natural_armor.name": "Темір тері",

    "origin.origins_furries.komodo.name": "Комодо айдаһары",
    "origin.origins_furries.otter.name": "Кәмшат",
    "origin.origins_furries.raccoon.name": "Енот",
    "power.origins_furries.charge.name": "Жүгіріп шабуылдау",
    "power.origins_furries.chicken_xp.name": "Тауық тәжірибесі",
    "power.origins_furries.low_light_vision.name": "Күңгірт жарықта көру",
    "power.origins_furries.low_light_vision.description": "Теңіз деңгейінен жоғары болғанда түнде көру әсерін аласыз.",
    "power.origins_furries.pavlov.name": "Павлов реакциясы",
    "power.origins_furries.raccoon_jump.name": "Енот секірісі",
    "power.origins_furries.night_vision.name": "Түнде көру",
    "power.origins_furries.night_vision.description": "Сізде түнде көру қабілеті бар.",
    "power.origins_furries.scales.name": "Қабыршақтар",
    "power.origins_furries.scales.description": "Қабыршақтарыңыз сізге +4 табиғи сауыт береді.",
    "power.origins_furries.heavy_wool.description": "Қалың жүніңіз сізге +2 табиғи сауыт береді.",
    "power.origins_furries.fragile.description": "Сіздің максималды саулығыңыз адамға қарағанда 2 жүрекке аз.",
    "power.origins_furries.soft.description": "Сіздің максималды саулығыңыз адамға қарағанда 1 жүрекке аз.",
    "power.origins_furries.safe_meat.description": "Шіріген ет пен шикі қой етін қауіпсіз жей аласыз.",
    "power.origins_furries.trash_regen.description": "Шіріген ет жегенде регенерация аласыз.",

    "screen.originsmodernui.title": "Origin таңдаңыз",
    "screen.originsmodernui.search_hint": "Origin іздеу...",
    "screen.originsmodernui.choose_prompt": "Тізімнен Origin таңдаңыз",
    "screen.originsmodernui.profile": "Кейіпкер профилі",
    "key.originsmodernui.open_profile": "Кейіпкер профилін ашу",
    "key.originsmodernui.toggle_hud": "Origin Architect HUD-ын қосу/өшіру",
    "originsmodernui.config.hud.position": "HUD орны",
    "originsmodernui.config.hud.style": "HUD стилі",
    "originsmodernui.config.hud.scale": "HUD масштабы",
    "originsmodernui.config.hud.opacity": "HUD мөлдірлігі",
    "originsmodernui.config.hud.x_offset": "Көлденең ығысу",
    "originsmodernui.config.hud.y_offset": "Тік ығысу",
    "originsmodernui.config.hud.show_level": "Origin Architect деңгейін көрсету",
    "originsmodernui.config.hud.show_points": "Жұмсалмаған сипаттама ұпайларын көрсету",
    "originsmodernui.config.hud.show_xp_popup": "Тәжірибе қосылғанын көрсету",
    "originsmodernui.config.hud.show_level_popup": "Деңгей көтерілгенін көрсету",
}

# High-confidence phrase replacements for recurrent machine-translation terminology.
VALUE_REPLACEMENTS = {
    "Түнгі көру": "Түнде көру",
    "Нетерит": "Незерит",
    "Netherite": "Незерит",
    "Павловед": "Павлов реакциясы",
}

# MT often concatenates sentences (e.g. "...жүреді.Су..."). Insert a space
# only when terminal punctuation is immediately followed by a Cyrillic/Kazakh letter.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүҺһІі])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/kk_kz.json")):
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

print(f"Kazakh refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
