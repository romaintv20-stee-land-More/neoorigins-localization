#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
FILES = sorted(ASSETS.glob('**/lang/eo_uy.json'))

# Context-sensitive corrections. Branded Origins terms deliberately stay canonical
# while gameplay/UI terminology follows natural Esperanto and current Minecraft usage.
KEY_OVERRIDES = {
    'neoorigins.toggle.on': 'Povo ŝaltita',
    'neoorigins.toggle.off': 'Povo malŝaltita',
    'neoorigins.night_vision.on': 'Noktvido ŝaltita',
    'neoorigins.night_vision.off': 'Noktvido malŝaltita',
    'neoorigins.night_vision.disabled_by_server': 'Noktvido estas malŝaltita de ĉi tiu servilo.',
    'neoorigins.night_vision.no_power': 'Via Origin ne havas la povon Noktvido.',
    'neoorigins.ultimine.no_power': 'Via Origin ne havas la povon Ultimine.',
    'origins.layer.origin': 'Origin',
    'origins.layer.class': 'Klaso',
    'screen.neoorigins.choose_origin': 'Elektu vian Origin',
    'screen.neoorigins.choose_prompt': 'Elektu: %s',
    'screen.neoorigins.choose.origins.layer.origin': 'Elektu vian Origin',
    'screen.neoorigins.choose.origins.layer.class': 'Elektu vian klason',
    'button.neoorigins.random': 'Hazarda',
    'gui.neoorigins.search.label': 'Serĉi Origin',
    'gui.neoorigins.picker.back_to_grid': '< Krado',
    'gui.neoorigins.picker.no_results': 'Neniu Origin kongruas kun via serĉo',
    'gui.neoorigins.hint.select': 'Elektu Origin por vidi detalojn',
    'gui.neoorigins.detail.powers_header': 'Povoj',
    'gui.neoorigins.sort.manual': 'Permane',
    'key.category.neoorigins.neoorigins': 'NeoOrigins',
    'key.neoorigins.class_skill': 'Klasa Kapablo',
    'key.neoorigins.view_info': 'Montri Origin-informojn',
    'key.neoorigins.open_creator': 'Malfermi Origin Creator',
    'key.neoorigins.open_mob_creator': 'Malfermi Mob Origin Creator',
    'key.neoorigins.toggle_night_vision': 'Ŝalti/malŝalti Noktvidon',
    'key.category.neoorigins.hotkeys': 'NeoOrigins (Fulmoklavoj)',
    'screen.neoorigins.origin_info': 'Origin-informoj',
    'screen.neoorigins.debug_powers': 'Aktivaj Povoj (Sencimigo)',
    'gui.neoorigins.info.no_origin': 'Neniu Origin ankoraŭ elektita.',
    'gui.neoorigins.info.your_origin': 'Via Origin',
    'gui.neoorigins.info.debug': 'Sencimigo',
    'screen.neoorigins.origin_editor': 'Origin-redaktilo',
    'gui.neoorigins.editor.layers_header': 'Origin-tavoloj',
    'gui.neoorigins.editor.powers_header': 'Redakti Povojn',
    'screen.neoorigins.creator': 'Origin Creator',
    'gui.neoorigins.creator.tab.powers': 'Povoj',
    'gui.neoorigins.creator.save': 'Konservi',
    'gui.neoorigins.creator.apply': 'Apliki',
    'screen.neoorigins.mob_creator': 'Mob Origin Creator',
    'gui.neoorigins.mob_creator.tab.powers': 'Povoj',
    'gui.neoorigins.mob_creator.tab.spawn_rules': 'Generaj Reguloj',
    'gui.neoorigins.mob_creator.tab.drops': 'Faligaĵoj',
    'gui.neoorigins.mob_creator.save': 'Konservi',
    'gui.neoorigins.mob_creator.apply': 'Apliki',
    'gui.neoorigins.debug.capabilities_header': 'Aktivaj Kapabloj',
    'gui.neoorigins.debug.powers_header': 'Donitaj Povoj',
    'origins.neoorigins.human.name': 'Homo',
    'origins.neoorigins.merling.name': 'Merling',
    'origins.neoorigins.avian.name': 'Avian',
    'origins.neoorigins.blazeling.name': 'Blazeling',
    'origins.neoorigins.elytrian.name': 'Elytrian',
    'origins.neoorigins.enderian.name': 'Enderian',
    'origins.neoorigins.arachnid.name': 'Arachnid',
    'origins.neoorigins.shulk.name': 'Shulk',
    'origins.neoorigins.phantom.name': 'Phantom',
    'power.neoorigins.merling_water_breathing.name': 'Submarspirado',
    'power.neoorigins.merling_aquatic_speed.name': 'Akva Rapideco',
    'power.neoorigins.merling_land_slowdown.name': 'Tera Malrapidiĝo',
    'power.neoorigins.merling_dries_out.name': 'Sekiĝo',
    'power.neoorigins.avian_slow_fall.name': 'Malrapida Falo',
    'power.neoorigins.blazeling_fire_immunity.name': 'Fajroimuneco',
    'power.neoorigins.blazeling_blaze_scales.name': 'Blaze-skvamoj',
    'power.neoorigins.blazeling_nether_born.name': 'Naskita en Nether',
    'power.neoorigins.blazeling_firebolt.name': 'Fajrobulo',
    'power.neoorigins.strider_stampede.name': 'Amaskuro',
    'power.neoorigins.golem_ground_slam.name': 'Terfrapo',
    'power.neoorigins.enderian_projectile_dodge.name': 'Evito de Pafaĵoj',
    'power.neoorigins.enderian_water_damage.name': 'Akva Malforteco',
    'power.neoorigins.enderian_teleport.name': 'Teletransporto',
    'power.neoorigins.arachnid_spiders_fang.name': 'Aranea Dentego',
    'origin.origins_furries.fox.description': 'Vulpoj estas malgrandaj ruzaj bestoj, kiuj amas kokidojn kaj dolĉajn berojn.',
    'origin.origins_furries.komodo.description': 'Komodaj varanoj amas varmon kaj ne toleras malvarmon.',
    'origin.origins_furries.raccoon.name': 'Lavurso',
    'origin.origins_furries.raccoon.description': 'Lavurso estas lerta besto, kiu amas serĉi manĝaĵon en rubo.',
    'power.origins_furries.boing': 'Salto',
    'power.origins_furries.charge.name': 'Sturma Kuro',
    'power.origins_furries.chicken_xp.name': 'Kokida Sperto',
    'power.origins_furries.fragile.description': 'Vi havas 2 sanajn korojn malpli ol homo.',
    'power.origins_furries.hates_skels.name': 'Malamo al Skeletoj',
    'power.origins_furries.heavy_wool.name': 'Peza Lano',
    'power.origins_furries.heavy_wool.description': 'Via peza lano donas al vi +2 naturan armaĵon.',
    'power.origins_furries.low_light_vision.name': 'Malfortluma Vido',
    'power.origins_furries.low_light_vision.description': 'Vi ricevas Noktvidon kiam vi estas super marnivelo.',
    'power.origins_furries.pavlov.name': 'Pavlova Reflekso',
    'power.origins_furries.pavlov.description': 'Kiam vi sonorigas vilaĝan sonorilon, vi resaniĝas kontraŭ malsato.',
    'power.origins_furries.raccoon_jump.name': 'Lavursa Salto',
    'power.origins_furries.safe_magma.name': 'Magma Rezisto',
    'power.origins_furries.scales.name': 'Skvamoj',
    'power.origins_furries.scales.description': 'Viaj skvamoj donas al vi +4 naturan armaĵon.',
    'power.origins_furries.shear_self.name': 'Tondi Vian Lanon',
    'power.origins_furries.milk_self.name': 'Melki Vin',
    'power.origins_furries.night_vision.name': 'Noktvido',
    'power.origins_furries.night_vision.description': 'Vi havas Noktvidon.',
    'power.origins_furries.speed_gain.name': 'Akva Rapideco',
    'power.origins_furries.starting_wool.description': 'Vi komencas kun 3 lanoj. Sufiĉas por lito!',
    'power.origins_furries.trash_regen.name': 'Ruba Resaniĝo',
    'power.origins_furries.water_vision.name': 'Subakva Vido',
    'power.origins_furries.munch_grass.name': 'Manĝi Herbon',
    'screen.originsmodernui.title': 'Elektu vian Origin',
    'screen.originsmodernui.search_hint': 'Serĉi Origins...',
    'screen.originsmodernui.choose_prompt': 'Elektu Origin el la listo',
    'screen.originsmodernui.profile': 'Rolula Profilo',
    'key.originsmodernui.open_profile': 'Malfermi Rolulan Profilon',
    'key.originsmodernui.toggle_hud': 'Ŝalti/malŝalti la Origin Architect HUD',
    'originsmodernui.config.hud.show_level': 'Montri Origin Architect-nivelon',
    'originsmodernui.config.hud.show_points': 'Montri neuzitajn statistikajn poentojn',
    'originsmodernui.config.hud.show_xp_popup': 'Montri ŝprucfenestron de akirita sperto',
    'originsmodernui.config.hud.show_level_popup': 'Montri ŝprucfenestron de niveliĝo',
}

REPLACEMENTS = [
    (re.compile(r'\bNight Vision\b', re.I), 'Noktvido'),
    (re.compile(r'\bHotkey\b', re.I), 'Fulmoklavo'),
    (re.compile(r'\bToggle\b'), 'Ŝalti/malŝalti'),
    (re.compile(r'\bOpen\b'), 'Malfermi'),
    (re.compile(r'\bShow\b'), 'Montri'),
    (re.compile(r'\bDefault\b'), 'Defaŭlta'),
    (re.compile(r'\bPowers\b'), 'Povoj'),
    (re.compile(r'\bPower\b'), 'Povo'),
]

if not FILES:
    raise SystemExit('No eo_uy.json files found')

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
        new = re.sub(r'(?<=[.!?])(?=[A-ZÀ-ÖØ-ÞĈĜĤĴŜŬ])', ' ', new)
        if new != value:
            data[key] = new
            changed = True
            changed_values += 1
    for i in range(1, 65):
        key = f'key.neoorigins.hotkey.{i}'
        if key in data:
            want = f'Fulmoklavo {i:02d}'
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
for bad in ('Night Vision', 'Hotkey 30', 'Hotkey 33', 'Hotkey 34', 'Hotkey 37', 'Hotkey 38', 'Hotkey 39', 'Hotkey 47', 'Hotkey 48', 'Hotkey 49'):
    if bad in joined:
        raise SystemExit(f'Known Esperanto contextual English remnant remains: {bad}')

print(f'Refined Esperanto terminology in {changed_files} / {len(FILES)} files; {changed_values} values changed; {len(KEY_OVERRIDES)} guarded keys found.')
