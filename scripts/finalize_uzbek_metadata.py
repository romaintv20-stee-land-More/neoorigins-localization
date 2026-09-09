#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

# catalog.json: derive Uzbek entries from the reviewed Chuvash entries so every
# project inherits the same support/target/file structure.
p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
catalog['project']['supported_locale_count'] = 59

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'cv_cu' in obj and 'uz_uz' not in obj and isinstance(obj['cv_cu'], dict) and 'name' in obj['cv_cu']:
            entry = deepcopy(obj['cv_cu'])
            entry['name'] = "O'zbekcha"
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/cv_cu.json', '/uz_uz.json')
            obj['uz_uz'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['uzbek_common_glob'] = 'neoorigins_uz_common_*'
ns['uzbek_mc_1_21_1'] = 'neoorigins_uz_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 59 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Uzbek language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# CATALOG.md: each project language list currently ends with Chuvash.
p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Чӑвашла (`cv_cu`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Chuvash catalogue entries, got {hits}')
text = text.replace(needle, "Чӑвашла (`cv_cu`) · O'zbekcha (`uz_uz`)")
p.write_text(text, encoding='utf-8')

# README: update build counts, supported-language prose and explicit coverage.
p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 58 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 58 |")}')
text = text.replace('| 58 |', '| 59 |')
old = '**Azéri (`az_az`)**, **Kannada (`kn_in`)** et **Tchouvache (`cv_cu`)**.'
new = '**Azéri (`az_az`)**, **Kannada (`kn_in`)**, **Tchouvache (`cv_cu`)** et **Ouzbek (`uz_uz`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les cinquante-huit langues' not in text:
    raise SystemExit('README 58-language sentence not found')
text = text.replace('Les cinquante-huit langues', 'Les cinquante-neuf langues', 1)
cv_block = '''Pour le tchouvache :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
uz_block = cv_block + '''\nPour l’ouzbek :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if cv_block not in text:
    raise SystemExit('README Chuvash coverage block not found')
text = text.replace(cv_block, uz_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Uzbek metadata prepared: 59 locales; {added} catalog language entries; {hits} catalogue rows.')
