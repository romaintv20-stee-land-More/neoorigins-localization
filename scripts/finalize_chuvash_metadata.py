#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

# catalog.json: derive each Chuvash entry from the already-reviewed Kannada entry,
# preserving per-project fallback counts while changing locale/name/path.
p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
catalog['project']['supported_locale_count'] = 58

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'kn_in' in obj and 'cv_cu' not in obj and isinstance(obj['kn_in'], dict) and 'name' in obj['kn_in']:
            entry = deepcopy(obj['kn_in'])
            entry['name'] = 'Чӑвашла'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/kn_in.json', '/cv_cu.json')
            obj['cv_cu'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['chuvash_common_glob'] = 'neoorigins_cv_common_*'
ns['chuvash_mc_1_21_1'] = 'neoorigins_cv_121'
if added < 11:
    raise SystemExit(f'Expected Chuvash language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# CATALOG.md: every project already ends its language list with Kannada.
p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'ಕನ್ನಡ (`kn_in`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Kannada catalogue entries, got {hits}')
text = text.replace(needle, 'ಕನ್ನಡ (`kn_in`) · Чӑвашла (`cv_cu`)')
p.write_text(text, encoding='utf-8')

# README.md: update build counts, supported-language prose and the coverage section.
p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 57 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 57 |")}')
text = text.replace('| 57 |', '| 58 |')
old = '**Azéri (`az_az`)** et **Kannada (`kn_in`)**.'
new = '**Azéri (`az_az`)**, **Kannada (`kn_in`)** et **Tchouvache (`cv_cu`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les cinquante-sept langues' not in text:
    raise SystemExit('README 57-language sentence not found')
text = text.replace('Les cinquante-sept langues', 'Les cinquante-huit langues', 1)
kn_block = '''Pour le kannada :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
cv_block = kn_block + '''\nPour le tchouvache :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if kn_block not in text:
    raise SystemExit('README Kannada coverage block not found')
text = text.replace(kn_block, cv_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Chuvash metadata prepared: 58 locales; {added} catalog language entries; {hits} catalogue rows.')
