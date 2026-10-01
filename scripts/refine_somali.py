#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
FILES = sorted(ASSETS.glob('**/lang/so_so.json'))

# Context-sensitive corrections. Branded Origins terms deliberately stay canonical
# while gameplay/UI terminology is rendered naturally in Somali.
KEY_OVERRIDES = {
    'neoorigins.toggle.on': 'Awoodda waa daaran',
    'neoorigins.toggle.off': 'Awoodda waa dansan',
    'neoorigins.night_vision.on': 'Aragtida Habeenka waa daaran',
    'neoorigins.night_vision.off': 'Aragtida Habeenka waa dansan',
    'neoorigins.night_vision.disabled_by_server': 'Aragtida Habeenka waa laga damiyey server-kan.',
    'neoorigins.night_vision.no_power': 'Origin-kaagu ma laha awoodda Aragtida Habeenka.',
    'neoorigins.ultimine.no_power': 'Origin-kaagu ma laha awoodda Ultimine.',
    'origins.layer.origin': 'Origin',
    'origins.layer.class': 'Fasal',
    'screen.neoorigins.choose_origin': 'Dooro Origin-kaaga',
    'screen.neoorigins.choose_prompt': 'Dooro %s-kaaga',
    'screen.neoorigins.choose.origins.layer.origin': 'Dooro Origin-kaaga',
    'screen.neoorigins.choose.origins.layer.class': 'Dooro Fasalkaaga',
    'button.neoorigins.random': 'Nasiib',
    'gui.neoorigins.search.label': 'Raadi Origin',
    'gui.neoorigins.picker.back_to_grid': '< Shabakad',
    'gui.neoorigins.picker.no_results': 'Ma jiro Origin ku habboon raadintaada',
    'gui.neoorigins.hint.select': 'Dooro Origin si aad faahfaahinta u aragto',
    'gui.neoorigins.detail.powers_header': 'Awoodaha',
    'gui.neoorigins.sort.manual': 'Gacanta',
    'key.category.neoorigins.neoorigins': 'NeoOrigins',
    'key.neoorigins.class_skill': 'Xirfadda Fasalka',
    'key.neoorigins.view_info': 'Muuji Macluumaadka Origin',
    'key.neoorigins.open_creator': 'Fur Origin Creator',
    'key.neoorigins.open_mob_creator': 'Fur Mob Origin Creator',
    'key.neoorigins.toggle_night_vision': 'Beddel Aragtida Habeenka',
    'key.category.neoorigins.hotkeys': 'NeoOrigins (Furayaasha Degdegga ah)',
    'screen.neoorigins.origin_info': 'Macluumaadka Origin',
    'screen.neoorigins.debug_powers': 'Awoodaha Firfircoon (Debug)',
    'gui.neoorigins.info.no_origin': 'Weli Origin lama dooran.',
    'gui.neoorigins.info.your_origin': 'Origin-kaaga',
    'gui.neoorigins.info.debug': 'Debug',
    'screen.neoorigins.origin_editor': 'Tafatiraha Origin',
    'gui.neoorigins.editor.layers_header': 'Lakabyada Origin',
    'gui.neoorigins.editor.powers_header': 'Beddel Awoodaha',
    'screen.neoorigins.creator': 'Origin Creator',
    'gui.neoorigins.creator.tab.powers': 'Awoodaha',
    'gui.neoorigins.creator.save': 'Kaydi',
    'gui.neoorigins.creator.apply': 'Dhaqan geli',
    'screen.neoorigins.mob_creator': 'Mob Origin Creator',
    'gui.neoorigins.mob_creator.tab.powers': 'Awoodaha',
    'gui.neoorigins.mob_creator.tab.spawn_rules': 'Xeerarka Dhalashada',
    'gui.neoorigins.mob_creator.tab.drops': 'Waxyaabaha Dhaca',
    'gui.neoorigins.mob_creator.save': 'Kaydi',
    'gui.neoorigins.mob_creator.apply': 'Dhaqan geli',
    'gui.neoorigins.debug.capabilities_header': 'Awoodaha Firfircoon',
    'gui.neoorigins.debug.powers_header': 'Awoodaha La Siiyey',
    'origins.neoorigins.human.name': 'Aadanaha',
    'origins.neoorigins.merling.name': 'Merling',
    'origins.neoorigins.avian.name': 'Avian',
    'origins.neoorigins.blazeling.name': 'Blazeling',
    'origins.neoorigins.elytrian.name': 'Elytrian',
    'origins.neoorigins.enderian.name': 'Enderian',
    'origins.neoorigins.arachnid.name': 'Arachnid',
    'origins.neoorigins.shulk.name': 'Shulk',
    'origins.neoorigins.phantom.name': 'Phantom',
    'power.neoorigins.merling_water_breathing.name': 'Neefsashada Biyaha',
    'power.neoorigins.merling_aquatic_speed.name': 'Xawaaraha Biyaha',
    'power.neoorigins.merling_land_slowdown.name': 'Gaabis Dhulka',
    'power.neoorigins.merling_dries_out.name': 'Qallayl',
    'power.neoorigins.avian_slow_fall.name': 'Dhicis Gaabis ah',
    'power.neoorigins.blazeling_fire_immunity.name': 'Difaaca Dabka',
    'power.neoorigins.blazeling_blaze_scales.name': 'Qolofyada Blaze',
    'power.neoorigins.blazeling_nether_born.name': 'Ku Dhashay Nether',
    'power.neoorigins.blazeling_firebolt.name': 'Kubadda Dabka',
    'power.neoorigins.strider_stampede.name': 'Duullaan',
    'power.neoorigins.golem_ground_slam.name': 'Garaaca Dhulka',
    'power.neoorigins.enderian_projectile_dodge.name': 'Ka Fogaanshaha Madfaca',
    'power.neoorigins.enderian_water_damage.name': 'Daciifnimada Biyaha',
    'power.neoorigins.enderian_teleport.name': 'Teleport',
    'power.neoorigins.arachnid_spiders_fang.name': 'Iligga Caarada',
    'origin.origins_furries.fox.description': 'Dawacooyin yaryar oo dhagar badan waxay jecel yihiin digaag iyo berry macaan.',
    'origin.origins_furries.komodo.description': 'Masduulaayaasha Komodo waxay jecel yihiin kulaylka mana adkaysan karaan qabowga.',
    'origin.origins_furries.raccoon.name': 'Raccoon',
    'origin.origins_furries.raccoon.description': 'Raccoon-ku waa xayawaan xeel badan oo jecel inuu cunto ka raadiyo qashinka.',
    'power.origins_furries.boing': 'Boodid',
    'power.origins_furries.charge.name': 'Weerar Orod',
    'power.origins_furries.chicken_xp.name': 'XP Digaag',
    'power.origins_furries.fragile.description': 'Waxaad leedahay 2 wadne caafimaad ka yar aadanaha.',
    'power.origins_furries.hates_skels.name': 'Nacaybka Qalfoofyada',
    'power.origins_furries.heavy_wool.name': 'Dhogor Culus',
    'power.origins_furries.heavy_wool.description': 'Dhogortaada culus waxay ku siinaysaa +2 gaashaan dabiici ah.',
    'power.origins_furries.low_light_vision.name': 'Aragti Iftiin Yar',
    'power.origins_furries.low_light_vision.description': 'Waxaad helaysaa Aragtida Habeenka markaad ka sarrayso heerka badda.',
    'power.origins_furries.pavlov.name': 'Falcelinta Pavlov',
    'power.origins_furries.pavlov.description': 'Markaad gambaleel tuulo garaacdo, waad bogsanaysaa adigoo gaajo ku bixinaya.',
    'power.origins_furries.raccoon_jump.name': 'Boodka Raccoon',
    'power.origins_furries.safe_magma.name': 'Difaaca Magma',
    'power.origins_furries.scales.name': 'Qolofyo',
    'power.origins_furries.scales.description': 'Qolofyadaadu waxay ku siinayaan +4 gaashaan dabiici ah.',
    'power.origins_furries.shear_self.name': 'Iska Xiir Dhogortaada',
    'power.origins_furries.milk_self.name': 'Iska Lis',
    'power.origins_furries.night_vision.name': 'Aragtida Habeenka',
    'power.origins_furries.night_vision.description': 'Waxaad leedahay Aragtida Habeenka.',
    'power.origins_furries.speed_gain.name': 'Xawaaraha Biyaha',
    'power.origins_furries.starting_wool.description': 'Waxaad ku bilaabaysaa 3 dhogor. Waa ku filan tahay sariir!',
    'power.origins_furries.trash_regen.name': 'Dib-u-soo-kabasho Qashin',
    'power.origins_furries.water_vision.name': 'Aragtida Biyaha Hoostooda',
    'power.origins_furries.munch_grass.name': 'Cun Cawska',
    'screen.originsmodernui.title': 'Dooro Origin-kaaga',
    'screen.originsmodernui.search_hint': 'Raadi Origins...',
    'screen.originsmodernui.choose_prompt': 'Dooro Origin liiska',
    'screen.originsmodernui.profile': 'Muuqaalka Dabeecadda',
    'key.originsmodernui.open_profile': 'Fur Muuqaalka Dabeecadda',
    'key.originsmodernui.toggle_hud': 'Beddel HUD-ka Origin Architect',
    'originsmodernui.config.hud.show_level': 'Muuji Heerka Origin Architect',
    'originsmodernui.config.hud.show_points': 'Muuji Dhibcaha Stat-ka aan la isticmaalin',
    'originsmodernui.config.hud.show_xp_popup': 'Muuji soo-boodka XP-ga la helay',
    'originsmodernui.config.hud.show_level_popup': 'Muuji soo-boodka kororka heerka',
}

REPLACEMENTS = [
    (re.compile(r'\bNight Vision\b', re.I), 'Aragtida Habeenka'),
    (re.compile(r'\bAragga Habeenka\b', re.I), 'Aragtida Habeenka'),
    (re.compile(r'\bOpen\b'), 'Fur'),
    (re.compile(r'\bToggle\b'), 'Beddel'),
    (re.compile(r'\bShow\b'), 'Muuji'),
    (re.compile(r'\bDefault\b'), 'Caadi'),
    (re.compile(r'\bPowers\b'), 'Awoodaha'),
    (re.compile(r'\bPower\b'), 'Awood'),
]

if not FILES:
    raise SystemExit('No so_so.json files found')

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
        # Machine output frequently joins sentences with no space after punctuation.
        new = re.sub(r'(?<=[.!?])(?=[A-ZÀ-ÖØ-Þ])', ' ', new)
        if new != value:
            data[key] = new
            changed = True
            changed_values += 1
    for i in range(1, 65):
        key = f'key.neoorigins.hotkey.{i}'
        if key in data:
            want = f'Furaha Degdegga ah {i:02d}'
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
for bad in ('Night Vision', 'Hotkey 30', 'Hotkey 33', 'Hotkey 34', 'Hotkey 37', 'Hotkey 38', 'Hotkey 39', 'Hotkey 47', 'Hotkey 48', 'Hotkey 49', 'Furaha Furaha', 'Furaha kulul', 'Asal Abuur Abuuraha Mob'):
    if bad in joined:
        raise SystemExit(f'Known Somali contextual false friend remains: {bad}')

print(f'Refined Somali terminology in {changed_files} / {len(FILES)} files; {changed_values} values changed; {len(KEY_OVERRIDES)} guarded keys found.')
