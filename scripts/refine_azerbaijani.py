#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
FILES = sorted(ASSETS.glob('**/lang/az_az.json'))

KEY_OVERRIDES = {
    'neoorigins.toggle.on': 'Qabiliyyət aktivdir',
    'neoorigins.toggle.off': 'Qabiliyyət deaktivdir',
    'neoorigins.night_vision.on': 'Gecə Görüşü aktivdir',
    'neoorigins.night_vision.off': 'Gecə Görüşü deaktivdir',
    'neoorigins.night_vision.disabled_by_server': 'Gecə Görüşü bu serverdə deaktiv edilib.',
    'neoorigins.night_vision.no_power': 'Origin-inin Gecə Görüşü qabiliyyəti yoxdur.',
    'neoorigins.ultimine.no_power': 'Origin-inin Ultimine qabiliyyəti yoxdur.',
    'origins.layer.origin': 'Origin',
    'origins.layer.class': 'Sinif',
    'screen.neoorigins.choose_origin': 'Origin-ini seç',
    'screen.neoorigins.choose.origins.layer.origin': 'Origin-ini seç',
    'screen.neoorigins.choose.origins.layer.class': 'Sinifini seç',
    'gui.neoorigins.search.label': 'Origin axtar',
    'gui.neoorigins.picker.no_results': 'Axtarışına uyğun Origin tapılmadı',
    'gui.neoorigins.hint.select': 'Təfərrüatlara baxmaq üçün Origin seç',
    'gui.neoorigins.detail.powers_header': 'Qabiliyyətlər',
    'key.neoorigins.view_info': 'Origin məlumatına bax',
    'key.neoorigins.open_creator': 'Origin Creator-i aç',
    'key.neoorigins.open_mob_creator': 'Mob Origin Creator-i aç',
    'key.neoorigins.toggle_night_vision': 'Gecə Görüşünü dəyiş',
    'key.category.neoorigins.hotkeys': 'NeoOrigins (qısayollar)',
    'screen.neoorigins.origin_info': 'Origin məlumatı',
    'gui.neoorigins.info.no_origin': 'Hələ Origin seçilməyib.',
    'gui.neoorigins.info.your_origin': 'Sənin Origin-in',
    'screen.neoorigins.origin_editor': 'Origin redaktoru',
    'gui.neoorigins.editor.layers_header': 'Origin qatları',
    'gui.neoorigins.editor.powers_header': 'Qabiliyyətləri dəyiş',
    'screen.neoorigins.creator': 'Origin Creator',
    'gui.neoorigins.creator.tab.powers': 'Qabiliyyətlər',
    'gui.neoorigins.creator.apply': 'Tətbiq et',
    'screen.neoorigins.mob_creator': 'Mob Origin Creator',
    'gui.neoorigins.mob_creator.tab.powers': 'Qabiliyyətlər',
    'gui.neoorigins.mob_creator.tab.spawn_rules': 'Yaranma qaydaları',
    'gui.neoorigins.mob_creator.tab.drops': 'Qənimət',
    'gui.neoorigins.mob_creator.apply': 'Tətbiq et',
    'gui.neoorigins.debug.powers_header': 'Verilmiş qabiliyyətlər',
    'origins.neoorigins.human.name': 'Human',
    'origins.neoorigins.merling.name': 'Merling',
    'origins.neoorigins.avian.name': 'Avian',
    'origins.neoorigins.blazeling.name': 'Blazeling',
    'origins.neoorigins.elytrian.name': 'Elytrian',
    'origins.neoorigins.enderian.name': 'Enderian',
    'origins.neoorigins.arachnid.name': 'Arachnid',
    'origins.neoorigins.shulk.name': 'Shulk',
    'origins.neoorigins.phantom.name': 'Phantom',
    'power.neoorigins.blazeling_blaze_scales.name': 'Blaze pulcuqları',
    'power.neoorigins.blazeling_nether_born.name': 'Nether-də doğulmuş',
    'power.neoorigins.blazeling_nether_born.description': 'Nether-də olarkən daha sürətli hərəkət edirsən (görünən effekt işarəsi yoxdur).',
    'power.origins_furries.boing': 'Sıçrayış',
    'power.origins_furries.charge.name': 'Atılma',
    'power.origins_furries.chicken_xp.name': 'Toyuq təcrübəsi',
    'power.origins_furries.chicken_xp.description': 'Toyuqları öldürəndə ikiqat təcrübə qazanırsan.',
    'power.origins_furries.fragile.description': 'İnsandan 2 ürək az sağlamlığın var.',
    'power.origins_furries.heavy_wool.name': 'Qalın yun',
    'power.origins_furries.heavy_wool.description': 'Qalın yunun sənə +2 təbii zireh verir.',
    'power.origins_furries.low_light_vision.name': 'Zəif işıqda görmə',
    'power.origins_furries.low_light_vision.description': 'Dəniz səviyyəsindən yuxarıda Gecə Görüşü əldə edirsən.',
    'power.origins_furries.pavlov.name': 'Pavlov refleksi',
    'power.origins_furries.pavlov.description': 'Kənd zəngini çalmaq aclıq müqabilində səni sağaldır.',
    'power.origins_furries.raccoon_jump.name': 'Yenot sıçrayışı',
    'origin.origins_furries.raccoon.name': 'Yenot',
    'origin.origins_furries.raccoon.description': 'Yenotlar çevik və maraqlı yem axtaranlardır, tez-tez zibilləri eşələyirlər.',
    'power.origins_furries.scales.name': 'Pulcuqlar',
    'power.origins_furries.scales.description': 'Pulcuqların sənə +4 təbii zireh verir.',
    'power.origins_furries.night_vision.name': 'Gecə Görüşü',
    'power.origins_furries.night_vision.description': 'Sənin Gecə Görüşün var.',
    'power.origins_furries.soft.description': 'İnsandan 1 ürək az sağlamlığın var.',
    'power.origins_furries.starting_wool.description': '3 yunla başlayırsan. Yataq düzəltməyə kifayətdir!',
    'power.origins_furries.munch_grass.name': 'Ot yemək',
    'screen.originsmodernui.title': 'Origin-ini seç',
    'screen.originsmodernui.search_hint': 'Origin axtar...',
    'screen.originsmodernui.choose_prompt': 'Siyahıdan Origin seç',
    'key.originsmodernui.toggle_hud': 'Origin Architect HUD-unu dəyiş',
    'originsmodernui.config.hud.show_level': 'Origin Architect səviyyəsini göstər',
    'originsmodernui.config.hud.show_points': 'Xərclənməmiş statistika xallarını göstər',
    'originsmodernui.config.hud.show_xp_popup': 'XP qazancını göstər',
    'originsmodernui.config.hud.show_level_popup': 'Səviyyə artımını göstər',
}

# Contextual replacements are deliberately conservative: preserve product names and
# repair well-observed machine-translation false friends without rewriting arbitrary prose.
REPLACEMENTS = [
    (re.compile(r'\bHollandiyada\b', re.I), 'Nether-də'),
    (re.compile(r'\bHollandiya\b', re.I), 'Nether'),
    (re.compile(r'\bNight Vision\b', re.I), 'Gecə Görüşü'),
    (re.compile(r'\bNetherite\b', re.I), 'Nezerit'),
    (re.compile(r'\bnetherit\b', re.I), 'Nezerit'),
]

changes = 0
changed_files = 0
for path in FILES:
    data = json.loads(path.read_text(encoding='utf-8'))
    file_changes = 0
    for key, value in list(data.items()):
        new = KEY_OVERRIDES.get(key, value)
        if key.startswith('key.neoorigins.hotkey.'):
            try:
                n = int(key.rsplit('.', 1)[1])
            except ValueError:
                pass
            else:
                new = f'Qısayol {n:02d}'
        if isinstance(new, str):
            for pattern, replacement in REPLACEMENTS:
                new = pattern.sub(replacement, new)
            # Repair joined sentence boundaries such as "...gəzirlər.Su..." while
            # leaving decimals and version numbers untouched.
            new = re.sub(r'(?<=[.!?])(?=[^\W\d_])', ' ', new, flags=re.UNICODE)
        if new != value:
            data[key] = new
            changes += 1
            file_changes += 1
    if file_changes:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changed_files += 1

print(f'Azerbaijani contextual refinement: {changes} values changed across {changed_files} files')
