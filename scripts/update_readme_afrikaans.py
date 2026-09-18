#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/'README.md'
ASSETS=ROOT/'src/main/resources/resourcepacks/fallback_localizations/assets'
text=README.read_text(encoding='utf-8')
repl={
"`0.9.0-beta+1.21.1` | 21 | 54 |":"`0.9.0-beta+1.21.1` | 21 | 55 |",
"`0.9.0-beta+26.1` | 25 | 54 |":"`0.9.0-beta+26.1` | 25 | 55 |",
"`0.9.0-beta+26.2` | 25 | 54 |":"`0.9.0-beta+26.2` | 25 | 55 |",
"**Biélorusse (`be_by`)** et **Féroïen (`fo_fo`)**.":"**Biélorusse (`be_by`)**, **Féroïen (`fo_fo`)** et **Afrikaans (`af_za`)**.",
"Les cinquante-quatre langues sont disponibles":"Les cinquante-cinq langues sont disponibles",
"Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY / KA / KK / MN / MK / BE / FO":"Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY / KA / KK / MN / MK / BE / FO / AF",
}
for a,b in repl.items():
    if a not in text: raise RuntimeError(f'README anchor not found: {a}')
    text=text.replace(a,b,1)
fo_block="""Pour le féroïen :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
af_block=fo_block+"""
Pour l'afrikaans :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour l'afrikaans :" not in text:
    if fo_block not in text: raise RuntimeError('Faroese coverage block not found')
    text=text.replace(fo_block,af_block,1)
counts={"Medieval Origins Revival":"401/401","ibarn's quartet origins addon":"69/69","Origins Fantasy for NeoOrigins":"240/240","Origins: Backgrounds for NeoOrigins":"65/65","Origins: More Backgrounds for NeoOrigins":"44/44","Origins: Backgrounds ISS for NeoOrigins":"79/79","Origins Furries for NeoOrigins":"117/117","Origins: Classes Extended for NeoOrigins":"124/124","Origins: Classes ISS for NeoOrigins":"99/99","Origin Architect":"22/22"}
lines=text.splitlines()
for i,line in enumerate(lines):
    for project,count in counts.items():
        if line.startswith(f'| {project} |'):
            parts=line.split('|'); coverage=parts[3].strip()
            if coverage.count(' · ')==43:
                parts[3]=f' {coverage} · {count} '; lines[i]='|'.join(parts)
            break
text='\n'.join(lines)+'\n'
if len(list(ASSETS.glob('neoorigins_af_common_*/lang/af_za.json'))) != 16: raise RuntimeError('Expected 16 Afrikaans common chunks')
for p in [ASSETS/'neoorigins_af_121/lang/af_za.json',ASSETS/'neoorigins_26_1/lang/af_za.json',ASSETS/'neoorigins_26_2/lang/af_za.json']:
    if not p.exists(): raise RuntimeError(f'Missing Afrikaans target delta: {p}')
addons=['medievalorigins','ibarnorigins','origins_fantasy','origins_backgrounds','origins_backgrounds_two','origins_backgrounds_iss','origins_furries','origins_classes_ex','origins_classes_iss','originsmodernui']
af_121=17+sum((ASSETS/ns/'lang/af_za.json').exists() for ns in addons)
if '- **afrikaans** :' not in text:
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('- **féroïen** :'):
            lines.insert(i+1,f'- **afrikaans** : {af_121} fichiers fallback `af_za` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;')
            break
    else: raise RuntimeError('Faroese JAR line not found')
    text='\n'.join(lines)+'\n'
README.write_text(text,encoding='utf-8')
print(f'README.md updated for af_za / 55 locales ({af_121} fallback files on 1.21.1)')
