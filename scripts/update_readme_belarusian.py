#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/'README.md'
ASSETS=ROOT/'src/main/resources/resourcepacks/fallback_localizations/assets'
text=README.read_text(encoding='utf-8')
repl={
"`0.9.0-beta+1.21.1` | 21 | 52 |":"`0.9.0-beta+1.21.1` | 21 | 53 |",
"`0.9.0-beta+26.1` | 25 | 52 |":"`0.9.0-beta+26.1` | 25 | 53 |",
"`0.9.0-beta+26.2` | 25 | 52 |":"`0.9.0-beta+26.2` | 25 | 53 |",
"**Mongol (`mn_mn`)** et **Macédonien (`mk_mk`)**.":"**Mongol (`mn_mn`)**, **Macédonien (`mk_mk`)** et **Biélorusse (`be_by`)**.",
"Les cinquante-deux langues sont disponibles":"Les cinquante-trois langues sont disponibles",
"Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY / KA / KK / MN / MK":"Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY / KA / KK / MN / MK / BE",
}
for a,b in repl.items():
    if a not in text: raise RuntimeError(f'README anchor not found: {a}')
    text=text.replace(a,b,1)
mk_block="""Pour le macédonien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
be_block=mk_block+"""
Pour le biélorusse :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if 'Pour le biélorusse :' not in text:
    if mk_block not in text: raise RuntimeError('Macedonian coverage block not found')
    text=text.replace(mk_block,be_block,1)
counts={"Medieval Origins Revival":"401/401","ibarn's quartet origins addon":"69/69","Origins Fantasy for NeoOrigins":"240/240","Origins: Backgrounds for NeoOrigins":"65/65","Origins: More Backgrounds for NeoOrigins":"44/44","Origins: Backgrounds ISS for NeoOrigins":"79/79","Origins Furries for NeoOrigins":"117/117","Origins: Classes Extended for NeoOrigins":"124/124","Origins: Classes ISS for NeoOrigins":"99/99","Origin Architect":"22/22"}
lines=text.splitlines()
for i,line in enumerate(lines):
    for project,count in counts.items():
        if line.startswith(f'| {project} |'):
            parts=line.split('|'); coverage=parts[3].strip()
            if coverage.count(' · ')==41:
                parts[3]=f' {coverage} · {count} '; lines[i]='|'.join(parts)
            break
text='\n'.join(lines)+'\n'
if len(list(ASSETS.glob('neoorigins_be_common_*/lang/be_by.json'))) != 16: raise RuntimeError('Expected 16 Belarusian common chunks')
for p in [ASSETS/'neoorigins_be_121/lang/be_by.json',ASSETS/'neoorigins_26_1/lang/be_by.json',ASSETS/'neoorigins_26_2/lang/be_by.json']:
    if not p.exists(): raise RuntimeError(f'Missing Belarusian target delta: {p}')
addons=['medievalorigins','ibarnorigins','origins_fantasy','origins_backgrounds','origins_backgrounds_two','origins_backgrounds_iss','origins_furries','origins_classes_ex','origins_classes_iss','originsmodernui']
be_121=17+sum((ASSETS/ns/'lang/be_by.json').exists() for ns in addons)
if '- **biélorusse** :' not in text:
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('- **macédonien** :'):
            lines.insert(i+1,f'- **biélorusse** : {be_121} fichiers fallback `be_by` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;')
            break
    else: raise RuntimeError('Macedonian JAR line not found')
    text='\n'.join(lines)+'\n'
README.write_text(text,encoding='utf-8')
print(f'README.md updated for be_by / 53 locales ({be_121} fallback files on 1.21.1)')
