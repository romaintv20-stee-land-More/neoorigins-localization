#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
FILES = sorted(ASSETS.glob('**/lang/uz_uz.json'))

KEY_OVERRIDES = {
    'neoorigins.toggle.on': 'Qobiliyat yoqildi',
    'neoorigins.toggle.off': "Qobiliyat o'chirildi",
    'neoorigins.night_vision.on': "Tunda ko'rish yoqildi",
    'neoorigins.night_vision.off': "Tunda ko'rish o'chirildi",
    'neoorigins.night_vision.disabled_by_server': "Bu serverda Tunda ko'rish o'chirilgan.",
    'neoorigins.night_vision.no_power': "Sizning Origin'ingizda Tunda ko'rish qobiliyati yo'q.",
    'neoorigins.ultimine.no_power': "Sizning Origin'ingizda Ultimine qobiliyati yo'q.",
    'origins.layer.origin': 'Origin',
    'origins.layer.class': 'Klass',
    'screen.neoorigins.choose_origin': 'Origin tanlang',
    'screen.neoorigins.choose.origins.layer.origin': 'Origin tanlang',
    'screen.neoorigins.choose.origins.layer.class': 'Klass tanlang',
    'gui.neoorigins.search.label': 'Origin qidirish',
    'gui.neoorigins.picker.no_results': 'Qidiruvga mos Origin topilmadi',
    'gui.neoorigins.hint.select': "Batafsil ko'rish uchun Origin tanlang",
    'gui.neoorigins.detail.powers_header': 'Qobiliyatlar',
    'key.neoorigins.view_info': "Origin ma'lumotlarini ko'rish",
    'key.neoorigins.open_creator': 'Origin Creator-ni ochish',
    'key.neoorigins.open_mob_creator': 'Mob Origin Creator-ni ochish',
    'key.neoorigins.toggle_night_vision': "Tunda ko'rishni almashtirish",
    'key.category.neoorigins.hotkeys': 'NeoOrigins (tezkor tugmalar)',
    'screen.neoorigins.origin_info': "Origin ma'lumotlari",
    'gui.neoorigins.info.no_origin': 'Hali Origin tanlanmagan.',
    'gui.neoorigins.info.your_origin': "Sizning Origin'ingiz",
    'screen.neoorigins.origin_editor': 'Origin muharriri',
    'gui.neoorigins.editor.layers_header': 'Origin qatlamlari',
    'gui.neoorigins.editor.powers_header': 'Qobiliyatlarni tahrirlash',
    'screen.neoorigins.creator': 'Origin Creator',
    'gui.neoorigins.creator.tab.powers': 'Qobiliyatlar',
    'gui.neoorigins.creator.apply': "Qo'llash",
    'screen.neoorigins.mob_creator': 'Mob Origin Creator',
    'gui.neoorigins.mob_creator.tab.powers': 'Qobiliyatlar',
    'gui.neoorigins.mob_creator.tab.spawn_rules': "Paydo bo'lish qoidalari",
    'gui.neoorigins.mob_creator.tab.drops': 'Tushadigan buyumlar',
    'gui.neoorigins.mob_creator.apply': "Qo'llash",
    'gui.neoorigins.debug.powers_header': 'Berilgan qobiliyatlar',
    'origins.neoorigins.human.name': 'Human',
    'origins.neoorigins.merling.name': 'Merling',
    'origins.neoorigins.avian.name': 'Avian',
    'origins.neoorigins.blazeling.name': 'Blazeling',
    'origins.neoorigins.elytrian.name': 'Elytrian',
    'origins.neoorigins.enderian.name': 'Enderian',
    'origins.neoorigins.arachnid.name': 'Arachnid',
    'origins.neoorigins.shulk.name': 'Shulk',
    'origins.neoorigins.phantom.name': 'Phantom',
    'power.neoorigins.blazeling_blaze_scales.name': 'Blaze tangachalari',
    'power.neoorigins.blazeling_nether_born.name': "Netherda tug'ilgan",
    'power.neoorigins.blazeling_nether_born.description': "Netherda bo'lganingizda tezroq harakatlanasiz (ko'rinadigan effekt belgisi yo'q).",
    'power.origins_furries.boing': 'Sapchish',
    'power.origins_furries.charge.name': 'Zaryadli yugurish',
    'power.origins_furries.charge.description': "Sprint qilayotganda ko'proq zarar yetkazasiz.",
    'power.origins_furries.chicken_xp.name': 'Tovuq tajribasi',
    'power.origins_furries.chicken_xp.description': "Tovuqlarni o'ldirganingizda ikki baravar ko'p tajriba olasiz.",
    'power.origins_furries.fragile.description': "Sog'lig'ingiz odatdagi insonnikidan 2 yurakka kam.",
    'power.origins_furries.heavy_wool.name': "Og'ir jun",
    'power.origins_furries.heavy_wool.description': "Qalin juningiz sizga +2 tabiiy zirh beradi.",
    'power.origins_furries.low_light_vision.name': "Kam yorug'likda ko'rish",
    'power.origins_furries.low_light_vision.description': "Dengiz sathidan yuqorida bo'lsangiz, Tunda ko'rish effektiga ega bo'lasiz.",
    'power.origins_furries.pavlov.name': 'Pavlov reaksiyasi',
    'power.origins_furries.pavlov.description': "Qishloq qo'ng'irog'i chalinganda ochlik hisobiga sog'lig'ingiz tiklanadi.",
    'power.origins_furries.raccoon_jump.name': 'Rakun sakrashi',
    'origin.origins_furries.raccoon.name': 'Rakun',
    'origin.origins_furries.raccoon.description': "Rakunlar chaqqon va zukko oziq izlovchilar bo'lib, ko'pincha axlat orasidan ovqat qidiradi.",
    'power.origins_furries.scales.name': 'Tangachalar',
    'power.origins_furries.scales.description': 'Tangachalaringiz sizga +4 tabiiy zirh beradi.',
    'power.origins_furries.night_vision.name': "Tunda ko'rish",
    'power.origins_furries.night_vision.description': "Siz Tunda ko'rish qobiliyatiga egasiz.",
    'power.origins_furries.soft.description': "Sog'lig'ingiz odatdagi insonnikidan 1 yurakka kam.",
    'power.origins_furries.starting_wool.description': "Siz 3 ta jun bilan boshlaysiz. To'shak yasashga yetadi!",
    'power.origins_furries.munch_grass.name': "O't yeyish",
    'screen.originsmodernui.title': 'Origin tanlang',
    'screen.originsmodernui.search_hint': 'Origin qidirish...',
    'screen.originsmodernui.choose_prompt': "Ro'yxatdan Origin tanlang",
    'key.originsmodernui.toggle_hud': 'Origin Architect HUD-ni almashtirish',
    'originsmodernui.config.hud.show_level': 'Origin Architect darajasini ko\'rsatish',
    'originsmodernui.config.hud.show_points': "Ishlatilmagan ochkolarni ko'rsatish",
    'originsmodernui.config.hud.show_xp_popup': "Tajriba olinganda qalqib chiquvchi oynani ko'rsatish",
    'originsmodernui.config.hud.show_level_popup': "Daraja oshganda qalqib chiquvchi oynani ko'rsatish",
}

# Minecraft 26.2 Uzbek terminology is used for game terms; branded project names stay canonical.
REPLACEMENTS = [
    (re.compile(r'\bTungi ko[\'’]rish\b', re.I), "Tunda ko'rish"),
    (re.compile(r'\bNight Vision\b', re.I), "Tunda ko'rish"),
    (re.compile(r'\bNetherite\b', re.I), 'Netherit'),
]

if not FILES:
    raise SystemExit('No uz_uz.json files found')

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
            want = f'Tezkor tugma {i:02d}'
            if data[key] != want:
                data[key] = want
                changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changed_files += 1

missing = sorted(set(KEY_OVERRIDES) - seen)
if missing:
    raise SystemExit(f'Expected contextual keys not found: {missing}')

# Contextual assertions against machine-translation false friends found during review.
joined = '\n'.join(
    str(v)
    for path in FILES
    for v in json.loads(path.read_text(encoding='utf-8')).values()
    if isinstance(v, str)
)
for bad in (
    "O'zingizning kelib chiqishini tanlang",
    'Manbalarni qidirish...',
    'Pavloved',
    'Tarozilar',
    'Zerikarli',
    "Sprint paytida siz ko'proq zarar ko'rasiz.",
):
    if bad in joined:
        raise SystemExit(f'Known Uzbek contextual false friend remains: {bad}')

print(f'Refined Uzbek terminology in {changed_files} / {len(FILES)} files; {len(KEY_OVERRIDES)} guarded keys found.')
