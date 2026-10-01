#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive fixes. Keep Origins identity/product names stable and prefer
# terminology already used by Minecraft's current Mongolian localization.
OVERRIDES = {
    "neoorigins.toggle.on": "Чадвар асаалттай",
    "neoorigins.toggle.off": "Чадвар унтраалттай",
    "neoorigins.night_vision.on": "Харанхуйд харах асаалттай",
    "neoorigins.night_vision.off": "Харанхуйд харах унтраалттай",
    "neoorigins.night_vision.disabled_by_server": "Энэ сервер дээр харанхуйд харах чадварыг идэвхгүй болгосон.",
    "neoorigins.night_vision.no_power": "Таны Origin-д харанхуйд харах чадвар байхгүй.",
    "neoorigins.ultimine.no_power": "Таны Origin-д Ultimine чадвар байхгүй.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Анги",
    "screen.neoorigins.choose_origin": "Origin-оо сонгоно уу",
    "screen.neoorigins.choose.origins.layer.origin": "Origin-оо сонгоно уу",
    "screen.neoorigins.choose.origins.layer.class": "Ангиа сонгоно уу",
    "gui.neoorigins.search.label": "Origin хайх",
    "gui.neoorigins.picker.no_results": "Таны хайлтад тохирох Origin олдсонгүй",
    "gui.neoorigins.hint.select": "Дэлгэрэнгүйг харахын тулд Origin сонгоно уу",
    "gui.neoorigins.detail.powers_header": "Чадварууд",
    "gui.neoorigins.power.key_tag.toggle": "[%s] Асаах/унтраах",
    "gui.neoorigins.sort.class": "Анги",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Ангийн чадвар",
    "key.neoorigins.view_info": "Origin мэдээллийг харах",
    "key.neoorigins.open_creator": "Origin бүтээгчийг нээх",
    "key.neoorigins.open_mob_creator": "Mob Origin бүтээгчийг нээх",
    "key.neoorigins.toggle_night_vision": "Харанхуйд харахыг асаах/унтраах",
    "key.category.neoorigins.hotkeys": "NeoOrigins (түргэн товчнууд)",
    "screen.neoorigins.origin_info": "Origin мэдээлэл",
    "screen.neoorigins.debug_powers": "Идэвхтэй чадварууд (debug)",
    "gui.neoorigins.info.no_origin": "Origin хараахан сонгоогүй байна.",
    "gui.neoorigins.info.your_origin": "Таны Origin",
    "screen.neoorigins.origin_editor": "Origin засварлагч",
    "gui.neoorigins.editor.layers_header": "Origin давхаргууд",
    "gui.neoorigins.editor.powers_header": "Нэмэлт чадварууд",
    "screen.neoorigins.creator": "Origin бүтээгч",
    "gui.neoorigins.creator.tab.powers": "Чадварууд",
    "gui.neoorigins.creator.apply": "Хэрэглэх",
    "screen.neoorigins.mob_creator": "Mob Origin бүтээгч",
    "gui.neoorigins.mob_creator.tab.powers": "Чадварууд",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Үүсэх дүрэм",
    "gui.neoorigins.mob_creator.tab.drops": "Олз",
    "gui.neoorigins.mob_creator.apply": "Хэрэглэх",
    "gui.neoorigins.debug.powers_header": "Олгосон чадварууд",

    # Canonical Origin identity names: do not literal-translate the mod identities.
    "origins.neoorigins.human.name": "Хүн",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    "power.neoorigins.merling_water_breathing.name": "Усан дор амьсгалах",
    "power.neoorigins.merling_night_vision.name": "Гүний хараа",
    "power.neoorigins.merling_land_slowdown.name": "Газарт удаашрах",
    "power.neoorigins.merling_dries_out.name": "Хатах",
    "power.neoorigins.avian_no_fall_damage.name": "Хөнгөн жин",
    "power.neoorigins.avian_hollow_bones.name": "Хөндий яс",
    "power.neoorigins.blazeling_fire_immunity.name": "Галын зүрх",
    "power.neoorigins.blazeling_blaze_scales.name": "Blaze хайрс",
    "power.neoorigins.blazeling_nether_born.name": "Тамд төрсөн",
    "power.neoorigins.blazeling_nether_born.description": "Тамд байхдаа илүү хурдан хөдөлнө.",
    "power.neoorigins.blazeling_night_vision.name": "Дулааны хараа",
    "power.neoorigins.caveborn_night_vision.name": "Харанхуйд дасах",
    "power.neoorigins.caveborn_no_fall_damage.name": "Агуйн алхаа",
    "power.neoorigins.caveborn_stone_fists.name": "Чулуун нударга",
    "power.neoorigins.nether_fungus_diet.name": "Тамын мөөгний хооллолт",
    "power.neoorigins.caveborn_eat_copper.name": "Зэсний амт",
    "power.neoorigins.caveborn_eat_iron.name": "Төмрийн амт",
    "power.neoorigins.caveborn_eat_gold.name": "Алтны амт",
    "power.neoorigins.caveborn_eat_diamond.name": "Алмазын амт",
    "power.neoorigins.caveborn_eat_emerald.name": "Маргадын амт",
    "power.neoorigins.caveborn_eat_netherite.name": "Недеритийн амт",
    "power.neoorigins.caveborn_netherite_bonus.name": "Недерит цөм",
    "power.neoorigins.golem_natural_armor.name": "Төмөр арьс",

    "origin.origins_furries.komodo.name": "Комодо луу",
    "origin.origins_furries.otter.name": "Халиу",
    "origin.origins_furries.raccoon.name": "Элбэнх",
    "power.origins_furries.charge.name": "Давшилт",
    "power.origins_furries.chicken_xp.name": "Тахианы туршлага",
    "power.origins_furries.low_light_vision.name": "Бүдэг гэрэлд харах",
    "power.origins_furries.low_light_vision.description": "Далайн түвшнээс дээш байхдаа харанхуйд харах нөлөө авна.",
    "power.origins_furries.pavlov.name": "Павловын урвал",
    "power.origins_furries.raccoon_jump.name": "Элбэнхийн үсрэлт",
    "power.origins_furries.night_vision.name": "Харанхуйд харах",
    "power.origins_furries.night_vision.description": "Та харанхуйд харах чадвартай.",
    "power.origins_furries.scales.name": "Хайрс",
    "power.origins_furries.scales.description": "Таны хайрс +4 төрөлхийн хуяг өгнө.",
    "power.origins_furries.heavy_wool.description": "Таны өтгөн ноос +2 төрөлхийн хуяг өгнө.",
    "power.origins_furries.fragile.description": "Таны амины дээд хэмжээ хүнийхээс 2 зүрхээр бага.",
    "power.origins_furries.soft.description": "Таны амины дээд хэмжээ хүнийхээс 1 зүрхээр бага.",
    "power.origins_furries.safe_meat.description": "Муудсан мах болон түүхий хонины махыг аюулгүй идэж чадна.",
    "power.origins_furries.trash_regen.description": "Муудсан мах идэхэд нөхөн төлжих нөлөө авна.",

    "screen.originsmodernui.title": "Origin-оо сонгоно уу",
    "screen.originsmodernui.search_hint": "Origin хайх...",
    "screen.originsmodernui.choose_prompt": "Жагсаалтаас Origin сонгоно уу",
    "screen.originsmodernui.profile": "Дүрийн профайл",
    "key.originsmodernui.open_profile": "Дүрийн профайлыг нээх",
    "key.originsmodernui.toggle_hud": "Origin Architect HUD-г асаах/унтраах",
    "originsmodernui.config.hud.position": "HUD байрлал",
    "originsmodernui.config.hud.style": "HUD загвар",
    "originsmodernui.config.hud.scale": "HUD хэмжээ",
    "originsmodernui.config.hud.opacity": "HUD тунгалагшил",
    "originsmodernui.config.hud.x_offset": "Хэвтээ шилжилт",
    "originsmodernui.config.hud.y_offset": "Босоо шилжилт",
    "originsmodernui.config.hud.show_level": "Origin Architect түвшнийг харуулах",
    "originsmodernui.config.hud.show_points": "Зарцуулаагүй шинж чанарын оноог харуулах",
    "originsmodernui.config.hud.show_xp_popup": "Туршлага нэмэгдсэнийг харуулах",
    "originsmodernui.config.hud.show_level_popup": "Түвшин ахисныг харуулах",
}

VALUE_REPLACEMENTS = {
    "Шөнийн хараа": "Харанхуйд харах",
    "Netherite": "Недерит",
    "Нетерит": "Недерит",
    "Павловед": "Павловын урвал",
}

# MT often joins sentences without a space. Fix only terminal punctuation directly
# followed by a Mongolian/Cyrillic letter.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[А-Яа-яЁёӨөҮү])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/mn_mn.json")):
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

print(f"Mongolian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
