#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 64:
    raise SystemExit(f"Expected 64 locales before Tamil, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 65

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'ky_kg' in obj and 'ta_in' not in obj and isinstance(obj['ky_kg'], dict) and 'name' in obj['ky_kg']:
            entry = deepcopy(obj['ky_kg'])
            entry['name'] = 'தமிழ்'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/ky_kg.json', '/ta_in.json')
            obj['ta_in'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['tamil_common_glob'] = 'neoorigins_ta_common_*'
ns['tamil_mc_1_21_1'] = 'neoorigins_ta_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 65 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Tamil language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Кыргызча (`ky_kg`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Kyrgyz catalogue entries, got {hits}')
text = text.replace(needle, 'Кыргызча (`ky_kg`) · தமிழ் (`ta_in`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 64 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 64 |")}')
text = text.replace('| 64 |', '| 65 |')
old = '**Somali (`so_so`)**, **Espéranto (`eo_uy`)** et **Kirghize (`ky_kg`)**.'
new = '**Somali (`so_so`)**, **Espéranto (`eo_uy`)**, **Kirghize (`ky_kg`)** et **Tamoul (`ta_in`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-quatre langues' not in text:
    raise SystemExit('README 64-language sentence not found')
text = text.replace('Les soixante-quatre langues', 'Les soixante-cinq langues', 1)

ky_block = '''Pour le kirghize :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
ta_block = ky_block + '''\nPour le tamoul :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if ky_block not in text:
    raise SystemExit('README Kyrgyz coverage block not found')
text = text.replace(ky_block, ta_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Tamil metadata prepared: 65 locales; {added} catalog language entries; {hits} catalogue rows.')
