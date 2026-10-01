#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
files = sorted(ASSETS.glob('**/lang/eo_uy.json'))

OVERRIDES = {
    'gui.neoorigins.editor.on': 'Ŝaltita',
    'gui.neoorigins.editor.off': 'Malŝaltita',
    'gui.neoorigins.info.close': 'Fermi',
    'gui.neoorigins.button.confirm': 'Konfirmi >',
    'power.origins_furries.grace.description': 'Vi povas ricevi 30 sekundojn da Delfena Gracio premante la Malĉefan Klavon.',
    'power.origins_furries.kb_resist.name': 'Repuŝrezisto',
    'power.origins_furries.safe_meat.description': 'Putra karno kaj kruda ŝafaĵo estas sekuraj por manĝi.',
    'power.origins_furries.safe_fishes.description': 'Krudaj fiŝoj kaj globfiŝo estas sekuraj por manĝi.',
    'power.origins_furries.shear_self.description': 'Premante la Ĉefan Klavon dum vi tenas tondilon, vi povas ricevi 2 lanojn unufoje ĉiujn 2 minutojn. Sen tondilo vi nur vundos vin.',
    'power.origins_furries.milk_self.description': 'Premante la Ĉefan Klavon dum vi tenas malplenan sitelon, vi povas ricevi sitelon da lakto unufoje ĉiujn 2 minutojn. Sen sitelo vi nur vundos vin.',
    'power.origins_furries.speed_gain.description': 'Esti en akvo dum 10 sekundoj donas al vi la efikon Rapideco.',
    'power.origins_furries.submersion.description': 'Esti en akvo dum 10 sekundoj donas al vi la efikon Rapideco.',
    'power.origins_furries.water_vision.description': 'Vi povas klare vidi subakve.',
    'originsmodernui.config.hud.enabled': 'Ŝalti la integran HUD',
    'originsmodernui.config.hud.opacity': 'HUD-opakeco',
    'originsmodernui.config.hud.x_offset': 'Horizontala deŝovo',
    'originsmodernui.config.hud.y_offset': 'Vertikala deŝovo',
}

# These are safe lexical remnants observed after the first deterministic pass.
# Keep this deliberately narrow rather than applying broad English-word substitutions.
PHRASE_REPLACEMENTS = {
    'Rotten Flesh': 'Putra karno',
    'Raw Mutton': 'kruda ŝafaĵo',
    'Pufferfish': 'globfiŝo',
    "Dolphin's Grace": 'Delfena Gracio',
    'Knockback Resistance': 'Repuŝrezisto',
}

if not files:
    raise SystemExit('No Esperanto locale files found')

seen = set()
changed = 0
changed_files = 0
for path in files:
    data = json.loads(path.read_text(encoding='utf-8'))
    dirty = False
    for key, value in OVERRIDES.items():
        if key in data:
            seen.add(key)
            if data[key] != value:
                data[key] = value
                changed += 1
                dirty = True
    for key, value in list(data.items()):
        if not isinstance(value, str):
            continue
        new = value
        for english, esperanto in PHRASE_REPLACEMENTS.items():
            new = new.replace(english, esperanto)
        if new != value:
            data[key] = new
            changed += 1
            dirty = True
    if dirty:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changed_files += 1

missing = sorted(set(OVERRIDES) - seen)
if missing:
    raise SystemExit(f'Observed Esperanto QA keys not found: {missing}')

joined = '\n'.join(
    str(v)
    for path in files
    for v in json.loads(path.read_text(encoding='utf-8')).values()
    if isinstance(v, str)
)
remaining = [english for english in PHRASE_REPLACEMENTS if english in joined]
if remaining:
    raise SystemExit(f'Observed English remnants still present: {remaining}')

print(f'Applied {changed} observed Esperanto corrections across {changed_files} files; {len(OVERRIDES)} guarded keys verified; {len(PHRASE_REPLACEMENTS)} English remnant classes cleared.')
