#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
FILES = sorted(ASSETS.glob('**/lang/cv_cu.json'))

KEY_OVERRIDES = {
    'neoorigins.toggle.on': 'Пултарулӑх вӑй кӗртнӗ',
    'neoorigins.toggle.off': 'Пултарулӑх сӳнтернӗ',
    'neoorigins.night_vision.on': 'Ҫӗрлехи куҫ вӑй кӗртнӗ',
    'neoorigins.night_vision.off': 'Ҫӗрлехи куҫ сӳнтернӗ',
    'neoorigins.night_vision.disabled_by_server': 'Ку сервер ҫинче Ҫӗрлехи куҫ сӳнтернӗ.',
    'neoorigins.night_vision.no_power': 'Сирӗн Originӑрӑн Ҫӗрлехи куҫ пултарулӑхӗ ҫук.',
    'neoorigins.ultimine.no_power': 'Сирӗн Originӑрӑн Ultimine пултарулӑхӗ ҫук.',
    'origins.layer.origin': 'Origin',
    'origins.layer.class': 'Класс',
    'screen.neoorigins.choose_origin': 'Origin суйласа илӗр',
    'screen.neoorigins.choose.origins.layer.origin': 'Origin суйласа илӗр',
    'screen.neoorigins.choose.origins.layer.class': 'Класс суйласа илӗр',
    'gui.neoorigins.search.label': 'Origin шыравӗ',
    'gui.neoorigins.picker.no_results': 'Шыравпа килӗшекен Origin тупӑнмарӗ',
    'gui.neoorigins.hint.select': 'Тӗплӗнрех курма Origin суйласа илӗр',
    'gui.neoorigins.detail.powers_header': 'Пултарулӑхсем',
    'key.neoorigins.view_info': 'Origin информацине пӑхӑр',
    'key.neoorigins.open_creator': 'Origin Creator уҫ',
    'key.neoorigins.open_mob_creator': 'Mob Origin Creator уҫ',
    'key.neoorigins.toggle_night_vision': 'Ҫӗрлехи куҫа улӑштар',
    'key.category.neoorigins.hotkeys': 'NeoOrigins (хоткейсем)',
    'screen.neoorigins.origin_info': 'Origin информацийӗ',
    'gui.neoorigins.info.no_origin': 'Хальлӗхе Origin суйласа илмен.',
    'gui.neoorigins.info.your_origin': 'Сирӗн Origin',
    'screen.neoorigins.origin_editor': 'Origin редакторӗ',
    'gui.neoorigins.editor.layers_header': 'Origin сийӗсем',
    'gui.neoorigins.editor.powers_header': 'Пултарулӑхсене улӑштар',
    'screen.neoorigins.creator': 'Origin Creator',
    'gui.neoorigins.creator.tab.powers': 'Пултарулӑхсем',
    'gui.neoorigins.creator.apply': 'Йышӑнтар',
    'screen.neoorigins.mob_creator': 'Mob Origin Creator',
    'gui.neoorigins.mob_creator.tab.powers': 'Пултарулӑхсем',
    'gui.neoorigins.mob_creator.tab.spawn_rules': 'Спавн правилӗсем',
    'gui.neoorigins.mob_creator.tab.drops': 'Лут',
    'gui.neoorigins.mob_creator.apply': 'Йышӑнтар',
    'gui.neoorigins.debug.powers_header': 'Панӑ пултарулӑхсем',
    'origins.neoorigins.human.name': 'Human',
    'origins.neoorigins.merling.name': 'Merling',
    'origins.neoorigins.avian.name': 'Avian',
    'origins.neoorigins.blazeling.name': 'Blazeling',
    'origins.neoorigins.elytrian.name': 'Elytrian',
    'origins.neoorigins.enderian.name': 'Enderian',
    'origins.neoorigins.arachnid.name': 'Arachnid',
    'origins.neoorigins.shulk.name': 'Shulk',
    'origins.neoorigins.phantom.name': 'Phantom',
    'power.neoorigins.blazeling_blaze_scales.name': 'Blaze хупӑсем',
    'power.neoorigins.blazeling_nether_born.name': 'Незерте ҫуралнӑ',
    'power.neoorigins.blazeling_nether_born.description': 'Незерте пулнӑ чух эсир хӑвӑртрах хускалатӑр (курӑнакан эффект значокӗ ҫук).',
    'power.origins_furries.boing': 'Сикни',
    'power.origins_furries.charge.name': 'Атака',
    'power.origins_furries.chicken_xp.name': 'Чӑх XP',
    'power.origins_furries.chicken_xp.description': 'Чӑхсене вӗлернӗ чух икӗ хут ытларах XP илетӗр.',
    'power.origins_furries.fragile.description': 'Сирӗн сывлӑхӑр ҫыннинчен 2 чӗре сахалтарах.',
    'power.origins_furries.heavy_wool.name': 'Йывӑр ҫӑм',
    'power.origins_furries.heavy_wool.description': 'Йывӑр ҫӑм сире +2 тӗп бронь парать.',
    'power.origins_furries.low_light_vision.name': 'Пӑчӑ ҫутӑра курни',
    'power.origins_furries.low_light_vision.description': 'Тинӗс шайӗнчен ҫӳлерех пулсан эсир Ҫӗрлехи куҫ илетӗр.',
    'power.origins_furries.pavlov.name': 'Павлов реакцийӗ',
    'power.origins_furries.pavlov.description': 'Ял хӑнкӑравӗ янӑранӑ чух выҫлӑх хисепӗпе сывалатӑр.',
    'power.origins_furries.raccoon_jump.name': 'Енот сикни',
    'origin.origins_furries.raccoon.name': 'Енот',
    'origin.origins_furries.raccoon.description': 'Енотсем хускануҫӑ тата ӑсчах апат шыравҫисем; вӗсем час-часах пӑрахӑҫра апат шыраҫҫӗ.',
    'power.origins_furries.scales.name': 'Хупӑсем',
    'power.origins_furries.scales.description': 'Сирӗн хупӑрсем сире +4 тӗп бронь параҫҫӗ.',
    'power.origins_furries.night_vision.name': 'Ҫӗрлехи куҫ',
    'power.origins_furries.night_vision.description': 'Сирӗн Ҫӗрлехи куҫ пур.',
    'power.origins_furries.soft.description': 'Сирӗн сывлӑхӑр ҫыннинчен 1 чӗре сахалтарах.',
    'power.origins_furries.starting_wool.description': 'Эсир 3 ҫӑмпа пуҫлатӑр. Вырӑн тунӑшӑн ҫитет!',
    'power.origins_furries.munch_grass.name': 'Курӑк ҫини',
    'screen.originsmodernui.title': 'Origin суйласа илӗр',
    'screen.originsmodernui.search_hint': 'Origin шыра...',
    'screen.originsmodernui.choose_prompt': 'Списӑкран Origin суйласа илӗр',
    'key.originsmodernui.toggle_hud': 'Origin Architect HUD-не улӑштар',
    'originsmodernui.config.hud.show_level': 'Origin Architect шайне кӑтарт',
    'originsmodernui.config.hud.show_points': 'Усӑ курман очкӑсене кӑтарт',
    'originsmodernui.config.hud.show_xp_popup': 'XP илнине кӑтарт',
    'originsmodernui.config.hud.show_level_popup': 'Шай ӳснине кӑтарт',
}

REPLACEMENTS = [
    (re.compile(r'\bNight Vision\b', re.I), 'Ҫӗрлехи куҫ'),
    (re.compile(r'\bNetherite\b', re.I), 'Незерит'),
    (re.compile(r'\bNether\b', re.I), 'Незер'),
    (re.compile('Ҫӗрлехи курӑм'), 'Ҫӗрлехи куҫ'),
    (re.compile('Ҫӗрлехи курӑну'), 'Ҫӗрлехи куҫ'),
]

if not FILES:
    raise SystemExit('No cv_cu.json files found')

seen = set()
changed_files = 0
for path in FILES:
    data = json.loads(path.read_text(encoding='utf-8'))
    changed = False
    for key, value in KEY_OVERRIDES.items():
        if key in data:
            seen.add(key)
            if data[key] != value:
                data[key] = value
                changed = True
    for key, value in list(data.items()):
        if not isinstance(value, str):
            continue
        new = value
        for pattern, replacement in REPLACEMENTS:
            new = pattern.sub(replacement, new)
        if new != value:
            data[key] = new
            changed = True
    for i in range(1, 65):
        key = f'key.neoorigins.hotkey.{i}'
        if key in data:
            want = f'Хоткей {i:02d}'
            if data[key] != want:
                data[key] = want
                changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changed_files += 1

missing = sorted(set(KEY_OVERRIDES) - seen)
if missing:
    raise SystemExit(f'Expected contextual keys not found: {missing}')

print(f'Refined Chuvash terminology in {changed_files} / {len(FILES)} files; {len(KEY_OVERRIDES)} guarded keys found.')
