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
