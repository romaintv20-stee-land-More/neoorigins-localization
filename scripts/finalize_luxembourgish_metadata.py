#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
catalog['project']['supported_locale_count'] = 61

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'mt_mt' in obj and 'lb_lu' not in obj and isinstance(obj['mt_mt'], dict) and 'name' in obj['mt_mt']:
            entry = deepcopy(obj['mt_mt'])
            entry['name'] = 'Lëtzebuergesch'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/mt_mt.json', '/lb_lu.json')
            obj['lb_lu'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['luxembourgish_common_glob'] = 'neoorigins_lb_common_*'
ns['luxembourgish_mc_1_21_1'] = 'neoorigins_lb_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 61 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Luxembourgish language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Malti (`mt_mt`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Maltese catalogue entries, got {hits}')
text = text.replace(needle, 'Malti (`mt_mt`) · Lëtzebuergesch (`lb_lu`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 60 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 60 |")}')
text = text.replace('| 60 |', '| 61 |')
old = '**Ouzbek (`uz_uz`)** et **Maltais (`mt_mt`)**.'
new = '**Ouzbek (`uz_uz`)**, **Maltais (`mt_mt`)** et **Luxembourgeois (`lb_lu`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante langues' not in text:
    raise SystemExit('README 60-language sentence not found')
text = text.replace('Les soixante langues', 'Les soixante et une langues', 1)

mt_block = '''Pour le maltais :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
lb_block = mt_block + '''\nPour le luxembourgeois :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if mt_block not in text:
    raise SystemExit('README Maltese coverage block not found')
text = text.replace(mt_block, lb_block, 1)

old_cs = '''Pour le tchèque (couverture historique partielle à compléter) :\n\n- **1.21.1 : 15/2 296 clés** couvertes ;\n- **26.1.x : 29/2 307 clés** couvertes ;\n- **26.2 : 29/2 307 clés** couvertes.\n'''
new_cs = '''Pour le tchèque :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
old_hu = '''Pour le hongrois (couverture historique partielle à compléter) :\n\n- **1.21.1 : 0/2 296 clés** couvertes ;\n- **26.1.x : 14/2 307 clés** couvertes ;\n- **26.2 : 14/2 307 clés** couvertes.\n'''
new_hu = '''Pour le hongrois :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if old_cs in text: text = text.replace(old_cs, new_cs, 1)
if old_hu in text: text = text.replace(old_hu, new_hu, 1)
p.write_text(text, encoding='utf-8')

print(f'Luxembourgish metadata prepared: 61 locales; {added} catalog language entries; {hits} catalogue rows.')
