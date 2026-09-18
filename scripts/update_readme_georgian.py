#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/'README.md'
ASSETS=ROOT/'src/main/resources/resourcepacks/fallback_localizations/assets'
text=README.read_text(encoding='utf-8')
repl={
"`0.9.0-beta+1.21.1` | 21 | 48 |":"`0.9.0-beta+1.21.1` | 21 | 49 |",
"`0.9.0-beta+26.1` | 25 | 48 |":"`0.9.0-beta+26.1` | 25 | 49 |",
"`0.9.0-beta+26.2` | 25 | 48 |":"`0.9.0-beta+26.2` | 25 | 49 |",
"**Gaélique écossais (`gd_gb`)** et **Arménien (`hy_am`)**.":"**Gaélique écossais (`gd_gb`)**, **Arménien (`hy_am`)** et **Géorgien (`ka_ge`)**.",
"Les quarante-huit langues sont disponibles":"Les quarante-neuf langues sont disponibles",
"Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY":"Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY / KA",
}
for a,b in repl.items():
    if a not in text: raise RuntimeError(f'README anchor not found: {a}')
    text=text.replace(a,b,1)
hy_block="""Pour l’arménien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
ka_block=hy_block+"""
Pour le géorgien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if 'Pour le géorgien :' not in text:
    if hy_block not in text: raise RuntimeError('Armenian coverage block not found')
    text=text.replace(hy_block,ka_block,1)
counts={"Medieval Origins Revival":"401/401","ibarn's quartet origins addon":"69/69","Origins Fantasy for NeoOrigins":"240/240","Origins: Backgrounds for NeoOrigins":"65/65","Origins: More Backgrounds for NeoOrigins":"44/44","Origins: Backgrounds ISS for NeoOrigins":"79/79","Origins Furries for NeoOrigins":"117/117","Origins: Classes Extended for NeoOrigins":"124/124","Origins: Classes ISS for NeoOrigins":"99/99","Origin Architect":"22/22"}
lines=text.splitlines()
for i,line in enumerate(lines):
    for project,count in counts.items():
        if line.startswith(f'| {project} |'):
            parts=line.split('|'); coverage=parts[3].strip()
            if coverage.count(' · ')==37:
                parts[3]=f' {coverage} · {count} '; lines[i]='|'.join(parts)
            break
text='\n'.join(lines)+'\n'
if len(list(ASSETS.glob('neoorigins_ka_common_*/lang/ka_ge.json'))) != 16: raise RuntimeError('Expected 16 Georgian common chunks')
for p in [ASSETS/'neoorigins_ka_121/lang/ka_ge.json',ASSETS/'neoorigins_26_1/lang/ka_ge.json',ASSETS/'neoorigins_26_2/lang/ka_ge.json']:
    if not p.exists(): raise RuntimeError(f'Missing Georgian target delta: {p}')
addons=['medievalorigins','ibarnorigins','origins_fantasy','origins_backgrounds','origins_backgrounds_two','origins_backgrounds_iss','origins_furries','origins_classes_ex','origins_classes_iss','originsmodernui']
ka_121=17+sum((ASSETS/ns/'lang/ka_ge.json').exists() for ns in addons)
if '- **géorgien** :' not in text:
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('- **arménien** :'):
            lines.insert(i+1,f'- **géorgien** : {ka_121} fichiers fallback `ka_ge` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;')
            break
    else: raise RuntimeError('Armenian JAR line not found')
    text='\n'.join(lines)+'\n'
README.write_text(text,encoding='utf-8')
print(f'README.md updated for ka_ge / 49 locales ({ka_121} fallback files on 1.21.1)')
