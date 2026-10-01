#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
FILES = sorted(ASSETS.glob('**/lang/lb_lu.json'))

KEY_OVERRIDES = {
    'neoorigins.toggle.on': 'Fäegkeet aktivéiert',
    'neoorigins.toggle.off': 'Fäegkeet deaktivéiert',
    'neoorigins.night_vision.on': 'Nuechtsiicht aktivéiert',
    'neoorigins.night_vision.off': 'Nuechtsiicht deaktivéiert',
    'neoorigins.night_vision.disabled_by_server': 'Nuechtsiicht ass op dësem Server deaktivéiert.',
    'neoorigins.night_vision.no_power': 'Deng Origin huet keng Nuechtsiicht-Fäegkeet.',
    'neoorigins.ultimine.no_power': 'Deng Origin huet keng Ultimine-Fäegkeet.',
    'origins.layer.origin': 'Origin',
    'origins.layer.class': 'Klass',
    'screen.neoorigins.choose_origin': 'Wiel deng Origin',
    'screen.neoorigins.choose.origins.layer.origin': 'Wiel deng Origin',
    'screen.neoorigins.choose.origins.layer.class': 'Wiel deng Klass',
    'gui.neoorigins.search.label': 'Origin sichen',
    'gui.neoorigins.picker.no_results': 'Keng Origin passt op deng Sich',
    'gui.neoorigins.hint.select': 'Wiel eng Origin fir d\'Detailer ze gesinn',
    'gui.neoorigins.detail.powers_header': 'Fäegkeeten',
    'key.neoorigins.view_info': 'Origin-Info weisen',
    'key.neoorigins.open_creator': 'Origin Creator opmaachen',
    'key.neoorigins.open_mob_creator': 'Mob Origin Creator opmaachen',
    'key.neoorigins.toggle_night_vision': 'Nuechtsiicht wiesselen',
    'key.category.neoorigins.hotkeys': 'NeoOrigins (Schnelltasten)',
    'screen.neoorigins.origin_info': 'Origin-Info',
    'screen.neoorigins.debug_powers': 'Aktiv Fäegkeeten (Debug)',
    'gui.neoorigins.info.no_origin': 'Nach keng Origin gewielt.',
    'gui.neoorigins.info.your_origin': 'Deng Origin',
    'screen.neoorigins.origin_editor': 'Origin-Editor',
    'gui.neoorigins.editor.layers_header': 'Origin-Schichten',
    'gui.neoorigins.editor.powers_header': 'Fäegkeete wiesselen',
    'screen.neoorigins.creator': 'Origin Creator',
    'gui.neoorigins.creator.tab.powers': 'Fäegkeeten',
    'gui.neoorigins.creator.apply': 'Uwenden',
    'screen.neoorigins.mob_creator': 'Mob Origin Creator',
    'gui.neoorigins.mob_creator.tab.powers': 'Fäegkeeten',
    'gui.neoorigins.mob_creator.tab.spawn_rules': 'Spawn-Reegelen',
    'gui.neoorigins.mob_creator.tab.drops': 'Drops',
    'gui.neoorigins.mob_creator.apply': 'Uwenden',
    'gui.neoorigins.debug.powers_header': 'Vergi Fäegkeeten',
    'origins.neoorigins.human.name': 'Human',
    'origins.neoorigins.merling.name': 'Merling',
    'origins.neoorigins.avian.name': 'Avian',
    'origins.neoorigins.blazeling.name': 'Blazeling',
    'origins.neoorigins.elytrian.name': 'Elytrian',
    'origins.neoorigins.enderian.name': 'Enderian',
    'origins.neoorigins.arachnid.name': 'Arachnid',
    'origins.neoorigins.shulk.name': 'Shulk',
    'origins.neoorigins.phantom.name': 'Phantom',
    'power.neoorigins.blazeling_blaze_scales.name': 'Blaze-Schuppen',
    'power.neoorigins.blazeling_nether_born.name': 'Am Nether gebuer',
    'origin.origins_furries.fox.description': 'Kleng, schlau Fuusse friesse gär Hénger a séiss Beeren.',
    'origin.origins_furries.komodo.description': 'Komodo-Draache gär Hëtzt a kënnen d\'Keelt net ausstoen.',
    'origin.origins_furries.raccoon.name': 'Wäschbier',
    'origin.origins_furries.raccoon.description': 'Wäschbiere si clever Déieren, déi gär no Iessen am Offall sichen.',
    'power.origins_furries.boing': 'Sprong',
    'power.origins_furries.charge.name': 'Sprintattack',
    'power.origins_furries.chicken_xp.name': 'Hénger-XP',
    'power.origins_furries.fragile.description': 'Du hues 2 Häerzer manner Gesondheet wéi e Mënsch.',
    'power.origins_furries.hates_skels.name': 'Skelett-Haass',
    'power.origins_furries.heavy_wool.name': 'Déck Woll',
    'power.origins_furries.heavy_wool.description': 'Deng déck Woll gëtt dir +2 natierlech Rüstung.',
    'power.origins_furries.low_light_vision.name': 'Siicht bei wéineg Liicht',
    'power.origins_furries.low_light_vision.description': 'Du kriss Nuechtsiicht iwwer dem Mieresspigel.',
    'power.origins_furries.pavlov.name': 'Pavlov-Reaktioun',
    'power.origins_furries.pavlov.description': 'Wann s du eng Duerfklack schells, heels du dech am Austausch géint Honger.',
    'power.origins_furries.raccoon_jump.name': 'Wäschbier-Sprong',
    'power.origins_furries.safe_magma.name': 'Magmaresistenz',
    'power.origins_furries.scales.name': 'Schuppen',
    'power.origins_furries.scales.description': 'Deng Schuppe ginn dir +4 natierlech Rüstung.',
    'power.origins_furries.shear_self.name': 'Deng Woll selwer schéieren',
    'power.origins_furries.milk_self.name': 'Dech selwer melken',
    'power.origins_furries.night_vision.name': 'Nuechtsiicht',
    'power.origins_furries.night_vision.description': 'Du hues Nuechtsiicht.',
    'power.origins_furries.speed_gain.name': 'Waassergeschwindegkeet',
    'power.origins_furries.starting_wool.description': 'Du fänks mat 3 Woll un. Genuch fir e Bett ze maachen!',
    'power.origins_furries.trash_regen.name': 'Regeneratioun duerch Offall',
    'power.origins_furries.water_vision.name': 'Ënnerwaassersiicht',
    'power.origins_furries.munch_grass.name': 'Gras friessen',
    'screen.originsmodernui.title': 'Wiel deng Origin',
    'screen.originsmodernui.search_hint': 'Origins sichen...',
    'screen.originsmodernui.choose_prompt': 'Wiel eng Origin aus der Lëscht',
    'screen.originsmodernui.profile': 'Charakterprofil',
    'key.originsmodernui.open_profile': 'Charakterprofil opmaachen',
    'key.originsmodernui.toggle_hud': 'Origin-Architect-HUD wiesselen',
    'originsmodernui.config.hud.show_level': 'Origin-Architect-Niveau weisen',
    'originsmodernui.config.hud.show_points': 'Onbenotzte Stat-Punkte weisen',
    'originsmodernui.config.hud.show_xp_popup': 'XP-Gewënn-Popup weisen',
    'originsmodernui.config.hud.show_level_popup': 'Niveau-Up-Popup weisen',
}

REPLACEMENTS = [
    (re.compile(r'\bNight Vision\b', re.I), 'Nuechtsiicht'),
    (re.compile(r'\bNuecht Visioun\b', re.I), 'Nuechtsiicht'),
    (re.compile(r'\bNuetsvisioun\b', re.I), 'Nuechtsiicht'),
    (re.compile(r'\bNetherite\b', re.I), 'Netherit'),
    (re.compile(r'\bMuechten\b', re.I), 'Fäegkeeten'),
    (re.compile(r'\bUrspronk\b', re.I), 'Origin'),
    (re.compile(r'\bHierkonft\b', re.I), 'Origin'),
    (re.compile(r'\bOrigine\b', re.I), 'Origins'),
    (re.compile(r'\bToggleable\b', re.I), 'Ëmschaltbar'),
    (re.compile(r'\bToggle\b', re.I), 'Wiesselen'),
    (re.compile(r'\bShow\b', re.I), 'Weisen'),
    (re.compile(r'\bDefault\b', re.I), 'Standard'),
]

if not FILES:
    raise SystemExit('No lb_lu.json files found')

seen = set()
changed_files = 0
changed_values = 0
for path in FILES:
    data = json.loads(path.read_text(encoding='utf-8'))
    changed = False
    for key, value in KEY_OVERRIDES.items():
        if key in data:
            seen.add(key)
            if data[key] != value:
                data[key] = value
                changed = True
                changed_values += 1
    for key, value in list(data.items()):
        if not isinstance(value, str):
            continue
        new = value
        for pattern, replacement in REPLACEMENTS:
            new = pattern.sub(replacement, new)
        new = re.sub(r'(?<=[.!?])(?=[A-ZÀ-ÖØ-Þ])', ' ', new)
        if new != value:
            data[key] = new
            changed = True
            changed_values += 1
    for i in range(1, 65):
        key = f'key.neoorigins.hotkey.{i}'
        if key in data:
            want = f'Schnelltast {i:02d}'
            if data[key] != want:
                data[key] = want
                changed = True
                changed_values += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changed_files += 1

missing = sorted(set(KEY_OVERRIDES) - seen)
if missing:
    raise SystemExit(f'Expected contextual keys not found: {missing}')

joined = '\n'.join(str(v) for path in FILES for v in json.loads(path.read_text(encoding='utf-8')).values() if isinstance(v, str))
for bad in ('Nuecht Visioun', 'Night Vision', 'Pavloved', 'Open Charakter Profil', 'Toggle Architekt HUD', 'Show Architekt Niveau', 'Muechten', 'Hierkonft', 'Urspronk'):
    if bad in joined:
        raise SystemExit(f'Known Luxembourgish contextual false friend remains: {bad}')

print(f'Refined Luxembourgish terminology in {changed_files} / {len(FILES)} files; {changed_values} values changed; {len(KEY_OVERRIDES)} guarded keys found.')
