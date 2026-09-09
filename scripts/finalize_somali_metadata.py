#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 61:
    raise SystemExit(f"Expected 61 locales before Somali, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 62

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'lb_lu' in obj and 'so_so' not in obj and isinstance(obj['lb_lu'], dict) and 'name' in obj['lb_lu']:
            entry = deepcopy(obj['lb_lu'])
            entry['name'] = 'Soomaali'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/lb_lu.json', '/so_so.json')
            obj['so_so'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['somali_common_glob'] = 'neoorigins_so_common_*'
ns['somali_mc_1_21_1'] = 'neoorigins_so_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 62 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Somali language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Lëtzebuergesch (`lb_lu`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Luxembourgish catalogue entries, got {hits}')
text = text.replace(needle, 'Lëtzebuergesch (`lb_lu`) · Soomaali (`so_so`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 61 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 61 |")}')
text = text.replace('| 61 |', '| 62 |')
old = '**Maltais (`mt_mt`)** et **Luxembourgeois (`lb_lu`)**.'
new = '**Maltais (`mt_mt`)**, **Luxembourgeois (`lb_lu`)** et **Somali (`so_so`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante et une langues' not in text:
    raise SystemExit('README 61-language sentence not found')
text = text.replace('Les soixante et une langues', 'Les soixante-deux langues', 1)

lb_block = '''Pour le luxembourgeois :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
so_block = lb_block + '''\nPour le somali :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if lb_block not in text:
    raise SystemExit('README Luxembourgish coverage block not found')
text = text.replace(lb_block, so_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Somali metadata prepared: 62 locales; {added} catalog language entries; {hits} catalogue rows.')
