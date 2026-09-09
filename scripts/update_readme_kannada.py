#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
ASSETS = ROOT / 'src/main/resources/resourcepacks/fallback_localizations/assets'
text = README.read_text(encoding='utf-8')

repl = {
    "`0.9.0-beta+1.21.1` | 21 | 56 |": "`0.9.0-beta+1.21.1` | 21 | 57 |",
    "`0.9.0-beta+26.1` | 25 | 56 |": "`0.9.0-beta+26.1` | 25 | 57 |",
    "`0.9.0-beta+26.2` | 25 | 56 |": "`0.9.0-beta+26.2` | 25 | 57 |",
    "**Afrikaans (`af_za`)** et **Azéri (`az_az`)**.": "**Afrikaans (`af_za`)**, **Azéri (`az_az`)** et **Kannada (`kn_in`)**.",
    "Les cinquante-six langues sont disponibles": "Les cinquante-sept langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY / KA / KK / MN / MK / BE / FO / AF / AZ": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY / KA / KK / MN / MK / BE / FO / AF / AZ / KN",
}
for a, b in repl.items():
    if a not in text:
        raise RuntimeError(f'README anchor not found: {a}')
    text = text.replace(a, b, 1)

az_block = """Pour l'azéri :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
kn_block = az_block + """
Pour le kannada :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le kannada :" not in text:
    if az_block not in text:
        raise RuntimeError('Azerbaijani coverage block not found')
    text = text.replace(az_block, kn_block, 1)

counts = {
    "Medieval Origins Revival": "401/401",
    "ibarn's quartet origins addon": "69/69",
    "Origins Fantasy for NeoOrigins": "240/240",
    "Origins: Backgrounds for NeoOrigins": "65/65",
    "Origins: More Backgrounds for NeoOrigins": "44/44",
    "Origins: Backgrounds ISS for NeoOrigins": "79/79",
    "Origins Furries for NeoOrigins": "117/117",
    "Origins: Classes Extended for NeoOrigins": "124/124",
    "Origins: Classes ISS for NeoOrigins": "99/99",
    "Origin Architect": "22/22",
}
lines = text.splitlines()
for i, line in enumerate(lines):
    for project, count in counts.items():
        if line.startswith(f'| {project} |'):
            parts = line.split('|')
            coverage = parts[3].strip()
            if coverage.count(' · ') == 45:
                parts[3] = f' {coverage} · {count} '
                lines[i] = '|'.join(parts)
            break
text = '\n'.join(lines) + '\n'

if len(list(ASSETS.glob('neoorigins_kn_common_*/lang/kn_in.json'))) != 16:
    raise RuntimeError('Expected 16 Kannada common chunks')
for p in [
    ASSETS / 'neoorigins_kn_121/lang/kn_in.json',
    ASSETS / 'neoorigins_26_1/lang/kn_in.json',
    ASSETS / 'neoorigins_26_2/lang/kn_in.json',
]:
    if not p.exists():
        raise RuntimeError(f'Missing Kannada target delta: {p}')

addons = [
    'medievalorigins', 'ibarnorigins', 'origins_fantasy', 'origins_backgrounds',
    'origins_backgrounds_two', 'origins_backgrounds_iss', 'origins_furries',
    'origins_classes_ex', 'origins_classes_iss', 'originsmodernui',
]
kn_121 = 17 + sum((ASSETS / ns / 'lang/kn_in.json').exists() for ns in addons)
if '- **kannada** :' not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('- **azéri** :'):
            lines.insert(i + 1, f'- **kannada** : {kn_121} fichiers fallback `kn_in` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;')
            break
    else:
        raise RuntimeError('Azerbaijani JAR line not found')
    text = '\n'.join(lines) + '\n'

README.write_text(text, encoding='utf-8')
print(f'README.md updated for kn_in / 57 locales ({kn_121} fallback files on 1.21.1)')
