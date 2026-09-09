#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
FILES = sorted(ASSETS.glob('**/lang/kn_in.json'))

KEY_OVERRIDES = {
    'neoorigins.toggle.on': 'ಸಾಮರ್ಥ್ಯ ಸಕ್ರಿಯವಾಗಿದೆ',
    'neoorigins.toggle.off': 'ಸಾಮರ್ಥ್ಯ ನಿಷ್ಕ್ರಿಯವಾಗಿದೆ',
    'neoorigins.night_vision.on': 'ರಾತ್ರಿ ದೃಷ್ಟಿ ಸಕ್ರಿಯವಾಗಿದೆ',
    'neoorigins.night_vision.off': 'ರಾತ್ರಿ ದೃಷ್ಟಿ ನಿಷ್ಕ್ರಿಯವಾಗಿದೆ',
    'neoorigins.night_vision.disabled_by_server': 'ಈ ಸರ್ವರ್‌ನಲ್ಲಿ ರಾತ್ರಿ ದೃಷ್ಟಿಯನ್ನು ನಿಷ್ಕ್ರಿಯಗೊಳಿಸಲಾಗಿದೆ.',
    'neoorigins.night_vision.no_power': 'ನಿಮ್ಮ Origin‌ಗೆ ರಾತ್ರಿ ದೃಷ್ಟಿ ಸಾಮರ್ಥ್ಯ ಇಲ್ಲ.',
    'neoorigins.ultimine.no_power': 'ನಿಮ್ಮ Origin‌ಗೆ Ultimine ಸಾಮರ್ಥ್ಯ ಇಲ್ಲ.',
    'origins.layer.origin': 'Origin',
    'origins.layer.class': 'ವರ್ಗ',
    'screen.neoorigins.choose_origin': 'ನಿಮ್ಮ Origin ಆಯ್ಕೆಮಾಡಿ',
    'screen.neoorigins.choose.origins.layer.origin': 'ನಿಮ್ಮ Origin ಆಯ್ಕೆಮಾಡಿ',
    'screen.neoorigins.choose.origins.layer.class': 'ನಿಮ್ಮ ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
    'gui.neoorigins.search.label': 'Origin ಹುಡುಕಿ',
    'gui.neoorigins.picker.no_results': 'ನಿಮ್ಮ ಹುಡುಕಾಟಕ್ಕೆ ಹೊಂದುವ Origin ಕಂಡುಬಂದಿಲ್ಲ',
    'gui.neoorigins.hint.select': 'ವಿವರಗಳನ್ನು ನೋಡಲು Origin ಆಯ್ಕೆಮಾಡಿ',
    'gui.neoorigins.detail.powers_header': 'ಸಾಮರ್ಥ್ಯಗಳು',
    'key.neoorigins.view_info': 'Origin ಮಾಹಿತಿಯನ್ನು ನೋಡಿ',
    'key.neoorigins.open_creator': 'Origin Creator ತೆರೆಯಿರಿ',
    'key.neoorigins.open_mob_creator': 'Mob Origin Creator ತೆರೆಯಿರಿ',
    'key.neoorigins.toggle_night_vision': 'ರಾತ್ರಿ ದೃಷ್ಟಿಯನ್ನು ಬದಲಿಸಿ',
    'key.category.neoorigins.hotkeys': 'NeoOrigins (ಹಾಟ್‌ಕೀಗಳು)',
    'screen.neoorigins.origin_info': 'Origin ಮಾಹಿತಿ',
    'gui.neoorigins.info.no_origin': 'ಇನ್ನೂ ಯಾವುದೇ Origin ಆಯ್ಕೆ ಮಾಡಿಲ್ಲ.',
    'gui.neoorigins.info.your_origin': 'ನಿಮ್ಮ Origin',
    'screen.neoorigins.origin_editor': 'Origin ಸಂಪಾದಕ',
    'gui.neoorigins.editor.layers_header': 'Origin ಪದರಗಳು',
    'gui.neoorigins.editor.powers_header': 'ಸಾಮರ್ಥ್ಯಗಳನ್ನು ಬದಲಿಸಿ',
    'screen.neoorigins.creator': 'Origin Creator',
    'gui.neoorigins.creator.tab.powers': 'ಸಾಮರ್ಥ್ಯಗಳು',
    'gui.neoorigins.creator.apply': 'ಅನ್ವಯಿಸಿ',
    'screen.neoorigins.mob_creator': 'Mob Origin Creator',
    'gui.neoorigins.mob_creator.tab.powers': 'ಸಾಮರ್ಥ್ಯಗಳು',
    'gui.neoorigins.mob_creator.tab.spawn_rules': 'ಸ್ಪಾನ್ ನಿಯಮಗಳು',
    'gui.neoorigins.mob_creator.tab.drops': 'ಲೂಟ್',
    'gui.neoorigins.mob_creator.apply': 'ಅನ್ವಯಿಸಿ',
    'gui.neoorigins.debug.powers_header': 'ನೀಡಲಾದ ಸಾಮರ್ಥ್ಯಗಳು',
    'origins.neoorigins.human.name': 'Human',
    'origins.neoorigins.merling.name': 'Merling',
    'origins.neoorigins.avian.name': 'Avian',
    'origins.neoorigins.blazeling.name': 'Blazeling',
    'origins.neoorigins.elytrian.name': 'Elytrian',
    'origins.neoorigins.enderian.name': 'Enderian',
    'origins.neoorigins.arachnid.name': 'Arachnid',
    'origins.neoorigins.shulk.name': 'Shulk',
    'origins.neoorigins.phantom.name': 'Phantom',
    'power.neoorigins.blazeling_blaze_scales.name': 'Blaze ಶಲ್ಕಗಳು',
    'power.neoorigins.blazeling_nether_born.name': 'Nether‌ನಲ್ಲಿ ಜನಿಸಿದ',
    'power.neoorigins.blazeling_nether_born.description': 'Nether‌ನಲ್ಲಿ ಇರುವಾಗ ನೀವು ಹೆಚ್ಚು ವೇಗವಾಗಿ ಚಲಿಸುತ್ತೀರಿ (ಗೋಚರ ಪರಿಣಾಮ ಐಕಾನ್ ಇಲ್ಲ).',
    'power.origins_furries.boing': 'ಜಿಗಿತ',
    'power.origins_furries.charge.name': 'ದೌಡು ದಾಳಿ',
    'power.origins_furries.chicken_xp.name': 'ಕೋಳಿ XP',
    'power.origins_furries.chicken_xp.description': 'ಕೋಳಿಗಳನ್ನು ಕೊಂದಾಗ ನೀವು ಎರಡು ಪಟ್ಟು XP ಪಡೆಯುತ್ತೀರಿ.',
    'power.origins_furries.fragile.description': 'ಮಾನವನಿಗಿಂತ ನಿಮಗೆ 2 ಹೃದಯ ಕಡಿಮೆ ಆರೋಗ್ಯವಿದೆ.',
    'power.origins_furries.heavy_wool.name': 'ದಪ್ಪ ಉಣ್ಣೆ',
    'power.origins_furries.heavy_wool.description': 'ನಿಮ್ಮ ದಪ್ಪ ಉಣ್ಣೆ ನಿಮಗೆ +2 ನೈಸರ್ಗಿಕ ಕವಚ ನೀಡುತ್ತದೆ.',
    'power.origins_furries.low_light_vision.name': 'ಕಡಿಮೆ ಬೆಳಕಿನ ದೃಷ್ಟಿ',
    'power.origins_furries.low_light_vision.description': 'ಸಮುದ್ರಮಟ್ಟದ ಮೇಲಿರುವಾಗ ನೀವು ರಾತ್ರಿ ದೃಷ್ಟಿ ಪಡೆಯುತ್ತೀರಿ.',
    'power.origins_furries.pavlov.name': 'ಪಾವ್ಲೋವ್ ಪ್ರತಿಕ್ರಿಯೆ',
    'power.origins_furries.pavlov.description': 'ಹಳ್ಳಿಯ ಗಂಟೆ ಬಾರಿಸಿದಾಗ ಹಸಿವಿನ ಬೆಲೆಗೆ ನೀವು ಗುಣಮುಖರಾಗುತ್ತೀರಿ.',
    'power.origins_furries.raccoon_jump.name': 'ರಕೂನ್ ಜಿಗಿತ',
    'origin.origins_furries.raccoon.name': 'ರಕೂನ್',
    'origin.origins_furries.raccoon.description': 'ರಕೂನ್‌ಗಳು ಚುರುಕು ಮತ್ತು ಕುತೂಹಲದ ಆಹಾರ ಹುಡುಕುವ ಪ್ರಾಣಿಗಳು; ಅವು ಕಸದೊಳಗೆ ಹುಡುಕಾಡುವುದು ಸಾಮಾನ್ಯ.',
    'power.origins_furries.scales.name': 'ಶಲ್ಕಗಳು',
    'power.origins_furries.scales.description': 'ನಿಮ್ಮ ಶಲ್ಕಗಳು ನಿಮಗೆ +4 ನೈಸರ್ಗಿಕ ಕವಚ ನೀಡುತ್ತವೆ.',
    'power.origins_furries.night_vision.name': 'ರಾತ್ರಿ ದೃಷ್ಟಿ',
    'power.origins_furries.night_vision.description': 'ನಿಮಗೆ ರಾತ್ರಿ ದೃಷ್ಟಿ ಇದೆ.',
    'power.origins_furries.soft.description': 'ಮಾನವನಿಗಿಂತ ನಿಮಗೆ 1 ಹೃದಯ ಕಡಿಮೆ ಆರೋಗ್ಯವಿದೆ.',
    'power.origins_furries.starting_wool.description': 'ನೀವು 3 ಉಣ್ಣೆಯೊಂದಿಗೆ ಆರಂಭಿಸುತ್ತೀರಿ. ಹಾಸಿಗೆ ಮಾಡಲು ಸಾಕಷ್ಟು!',
    'power.origins_furries.munch_grass.name': 'ಹುಲ್ಲು ತಿನ್ನುವುದು',
    'screen.originsmodernui.title': 'ನಿಮ್ಮ Origin ಆಯ್ಕೆಮಾಡಿ',
    'screen.originsmodernui.search_hint': 'Origin ಹುಡುಕಿ...',
    'screen.originsmodernui.choose_prompt': 'ಪಟ್ಟಿಯಿಂದ Origin ಆಯ್ಕೆಮಾಡಿ',
    'key.originsmodernui.toggle_hud': 'Origin Architect HUD ಅನ್ನು ಬದಲಿಸಿ',
    'originsmodernui.config.hud.show_level': 'Origin Architect ಮಟ್ಟವನ್ನು ತೋರಿಸಿ',
    'originsmodernui.config.hud.show_points': 'ಖರ್ಚಾಗದ ಅಂಕಗಳನ್ನು ತೋರಿಸಿ',
    'originsmodernui.config.hud.show_xp_popup': 'XP ಗಳಿಕೆಯನ್ನು ತೋರಿಸಿ',
    'originsmodernui.config.hud.show_level_popup': 'ಮಟ್ಟ ಏರಿಕೆಯನ್ನು ತೋರಿಸಿ',
}

REPLACEMENTS = [
    (re.compile(r'\bNight Vision\b', re.I), 'ರಾತ್ರಿ ದೃಷ್ಟಿ'),
    (re.compile(r'\bNetherite\b', re.I), 'Netherite'),
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
                new = f'ಹಾಟ್‌ಕೀ {n:02d}'
        if isinstance(new, str):
            for pattern, replacement in REPLACEMENTS:
                new = pattern.sub(replacement, new)
            new = re.sub(r'(?<=[.!?])(?=[^\W\d_])', ' ', new, flags=re.UNICODE)
        if new != value:
            data[key] = new
            changes += 1
            file_changes += 1
    if file_changes:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changed_files += 1

print(f'Kannada contextual refinement: {changes} values changed across {changed_files} files')
