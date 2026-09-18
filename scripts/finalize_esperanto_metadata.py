#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 62:
    raise SystemExit(f"Expected 62 locales before Esperanto, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 63

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'so_so' in obj and 'eo_uy' not in obj and isinstance(obj['so_so'], dict) and 'name' in obj['so_so']:
            entry = deepcopy(obj['so_so'])
            entry['name'] = 'Esperanto'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/so_so.json', '/eo_uy.json')
            obj['eo_uy'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['esperanto_common_glob'] = 'neoorigins_eo_common_*'
ns['esperanto_mc_1_21_1'] = 'neoorigins_eo_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 63 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Esperanto language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Soomaali (`so_so`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Somali catalogue entries, got {hits}')
text = text.replace(needle, 'Soomaali (`so_so`) · Esperanto (`eo_uy`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 62 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 62 |")}')
text = text.replace('| 62 |', '| 63 |')
old = '**Luxembourgeois (`lb_lu`)** et **Somali (`so_so`)**.'
new = '**Luxembourgeois (`lb_lu`)**, **Somali (`so_so`)** et **Espéranto (`eo_uy`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-deux langues' not in text:
    raise SystemExit('README 62-language sentence not found')
text = text.replace('Les soixante-deux langues', 'Les soixante-trois langues', 1)

so_block = '''Pour le somali :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
eo_block = so_block + '''\nPour l’espéranto :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if so_block not in text:
    raise SystemExit('README Somali coverage block not found')
text = text.replace(so_block, eo_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Esperanto metadata prepared: 63 locales; {added} catalog language entries; {hits} catalogue rows.')
