#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
FILES = sorted(ASSETS.glob('**/lang/mt_mt.json'))

KEY_OVERRIDES = {
    'neoorigins.toggle.on': 'Setgħa attivata',
    'neoorigins.toggle.off': 'Setgħa diżattivata',
    'neoorigins.night_vision.on': 'Viżjoni bil-Lejl attivata',
    'neoorigins.night_vision.off': 'Viżjoni bil-Lejl diżattivata',
    'neoorigins.night_vision.disabled_by_server': 'Il-Viżjoni bil-Lejl hija diżattivata fuq dan is-server.',
    'neoorigins.night_vision.no_power': "L-Origin tiegħek m'għandux is-setgħa tal-Viżjoni bil-Lejl.",
    'neoorigins.ultimine.no_power': "L-Origin tiegħek m'għandux is-setgħa Ultimine.",
    'origins.layer.origin': 'Origin',
    'origins.layer.class': 'Klassi',
    'screen.neoorigins.choose_origin': 'Agħżel Origin',
    'screen.neoorigins.choose.origins.layer.origin': 'Agħżel Origin',
    'screen.neoorigins.choose.origins.layer.class': 'Agħżel Klassi',
    'gui.neoorigins.search.label': 'Fittex Origin',
    'gui.neoorigins.picker.no_results': 'Ma nstab l-ebda Origin li jaqbel mat-tfittxija',
    'gui.neoorigins.hint.select': 'Agħżel Origin biex tara d-dettalji',
    'gui.neoorigins.detail.powers_header': 'Setgħat',
    'key.neoorigins.view_info': 'Ara l-informazzjoni tal-Origin',
    'key.neoorigins.open_creator': 'Iftaħ Origin Creator',
    'key.neoorigins.open_mob_creator': 'Iftaħ Mob Origin Creator',
    'key.neoorigins.toggle_night_vision': 'Aqleb il-Viżjoni bil-Lejl',
    'key.category.neoorigins.hotkeys': 'NeoOrigins (tasti rapidi)',
    'screen.neoorigins.origin_info': 'Informazzjoni tal-Origin',
    'gui.neoorigins.info.no_origin': 'Għadu ma ntgħażel l-ebda Origin.',
    'gui.neoorigins.info.your_origin': 'L-Origin tiegħek',
    'screen.neoorigins.origin_editor': 'Editur tal-Origin',
    'gui.neoorigins.editor.layers_header': 'Saffi tal-Origin',
    'gui.neoorigins.editor.powers_header': 'Editja s-Setgħat',
    'screen.neoorigins.creator': 'Origin Creator',
    'gui.neoorigins.creator.tab.powers': 'Setgħat',
    'gui.neoorigins.creator.apply': 'Applika',
    'screen.neoorigins.mob_creator': 'Mob Origin Creator',
    'gui.neoorigins.mob_creator.tab.powers': 'Setgħat',
    'gui.neoorigins.mob_creator.tab.spawn_rules': 'Regoli tat-Tfaċċar',
    'gui.neoorigins.mob_creator.tab.drops': 'Oġġetti Mwaqqgħin',
    'gui.neoorigins.mob_creator.apply': 'Applika',
    'gui.neoorigins.debug.powers_header': 'Setgħat Mogħtija',
    'origins.neoorigins.human.name': 'Human',
    'origins.neoorigins.merling.name': 'Merling',
    'origins.neoorigins.avian.name': 'Avian',
    'origins.neoorigins.blazeling.name': 'Blazeling',
    'origins.neoorigins.elytrian.name': 'Elytrian',
    'origins.neoorigins.enderian.name': 'Enderian',
    'origins.neoorigins.arachnid.name': 'Arachnid',
    'origins.neoorigins.shulk.name': 'Shulk',
    'origins.neoorigins.phantom.name': 'Phantom',
    'power.neoorigins.blazeling_blaze_scales.name': 'Skaldi tal-Blaze',
    'power.neoorigins.blazeling_nether_born.name': 'Imwieled fin-Nether',
    'power.neoorigins.blazeling_nether_born.description': "Tiċċaqlaq aktar malajr waqt li tkun fin-Nether (mingħajr ikona ta' effett viżibbli).",
    'origin.origins_furries.fox.description': 'Il-volpijiet żgħar u makakki jħobbu jieklu t-tiġieġ u l-berries ħelwin.',
    'power.origins_furries.boing': 'Qabża',
    'power.origins_furries.charge.name': 'Attakk bil-Ġirja',
    'power.origins_furries.charge.description': 'Tagħmel aktar ħsara waqt sprint.',
    'power.origins_furries.chicken_xp.name': 'Esperjenza mit-Tiġieġ',
    'power.origins_furries.chicken_xp.description': 'Tikseb id-doppju tal-XP meta toqtol it-tiġieġ.',
    'power.origins_furries.fragile.description': "Għandek 2 qlub ta' saħħa inqas minn bniedem.",
    'power.origins_furries.hates_skels.name': 'Mibegħda lejn l-Iskeletri',
    'power.origins_furries.heavy_wool.name': 'Suf Tqil',
    'power.origins_furries.heavy_wool.description': 'Is-suf oħxon tiegħek jagħtik +2 armatura naturali.',
    'power.origins_furries.low_light_vision.name': "Viżjoni f'Dawl Baxx",
    'power.origins_furries.low_light_vision.description': "Tikseb l-effett Viżjoni bil-Lejl meta tkun 'il fuq mil-livell tal-baħar.",
    'power.origins_furries.pavlov.name': "Reazzjoni ta' Pavlov",
    'power.origins_furries.pavlov.description': "Id-daqq ta' qanpiena tar-raħal ifejqek bi skambju għall-ġuħ.",
    'power.origins_furries.raccoon_jump.name': 'Qabża tar-Rakun',
    'origin.origins_furries.raccoon.name': 'Rakun',
    'origin.origins_furries.raccoon.description': "Ir-rakuni huma annimali għaqlin li jfittxu l-ikel u spiss ifittxuh fost l-iskart.",
    'power.origins_furries.safe_magma.name': 'Reżistenza għall-Magma',
    'power.origins_furries.scales.name': 'Skaldi',
    'power.origins_furries.scales.description': 'L-iskaldi tiegħek jagħtuk +4 armatura naturali.',
    'power.origins_furries.shear_self.name': "Aqta' s-Suf Tiegħek",
    'power.origins_furries.milk_self.name': 'Aħleb Lilek Innifsek',
    'power.origins_furries.night_vision.name': 'Viżjoni bil-Lejl',
    'power.origins_furries.night_vision.description': 'Għandek Viżjoni bil-Lejl.',
    'power.origins_furries.soft.description': "Għandek qalb waħda ta' saħħa inqas minn bniedem.",
    'power.origins_furries.speed_gain.name': "Veloċità fl-Ilma",
    'power.origins_furries.starting_wool.description': 'Tibda bi 3 suf. Biżżejjed biex tagħmel sodda!',
    'power.origins_furries.trash_regen.name': "Riġenerazzjoni mill-Iskart",
    'power.origins_furries.water_vision.name': "Viżjoni taħt l-Ilma",
    'power.origins_furries.munch_grass.name': 'Kul il-Ħaxix',
    'screen.originsmodernui.title': 'Agħżel l-Origin tiegħek',
    'screen.originsmodernui.search_hint': 'Fittex Origin...',
    'screen.originsmodernui.choose_prompt': 'Agħżel Origin mil-lista',
    'key.originsmodernui.toggle_hud': "Aqleb il-HUD ta' Origin Architect",
    'originsmodernui.config.hud.show_level': "Uri l-livell ta' Origin Architect",
    'originsmodernui.config.hud.show_points': 'Uri l-punti mhux użati',
    'originsmodernui.config.hud.show_xp_popup': "Uri popup meta tikseb XP",
    'originsmodernui.config.hud.show_level_popup': "Uri popup meta titla' livell",
}

# Current Minecraft 26.2 Maltese terminology is preferred for game terms;
# branded Origin/NeoOrigins product names remain canonical.
REPLACEMENTS = [
    (re.compile(r'\bNight Vision\b', re.I), 'Viżjoni bil-Lejl'),
    (re.compile(r'\bViżjoni bil-lejl\b', re.I), 'Viżjoni bil-Lejl'),
    (re.compile(r'\bNetherite\b', re.I), 'Netherit'),
]

if not FILES:
    raise SystemExit('No mt_mt.json files found')

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
        # Safe sentence-spacing corrections exposed by the generated add-on text.
        new = new.replace('minuti.Mingħajr', 'minuti. Mingħajr')
        new = new.replace('suf.Biżżejjed', 'suf. Biżżejjed')
        if new != value:
            data[key] = new
            changed = True
            changed_values += 1
    for i in range(1, 65):
        key = f'key.neoorigins.hotkey.{i}'
        if key in data:
            want = f'Tast Rapidu {i:02d}'
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

joined = '\n'.join(
    str(v)
    for path in FILES
    for v in json.loads(path.read_text(encoding='utf-8')).values()
    if isinstance(v, str)
)
for bad in (
    'Agħżel l-Oriġini tiegħek',
    'Pavloved',
    'Hades Skeletri',
    'Ħtieġa Saħħan',
    'Ilma Gliding',
    'Trash Yummy',
    'Ilma Viżjoni',
    'Munch ħaxix',
    'minuti.Mingħajr',
    'suf.Biżżejjed',
):
    if bad in joined:
        raise SystemExit(f'Known Maltese contextual false friend remains: {bad}')

print(f'Refined Maltese terminology in {changed_files} / {len(FILES)} files; {changed_values} values changed; {len(KEY_OVERRIDES)} guarded keys found.')
