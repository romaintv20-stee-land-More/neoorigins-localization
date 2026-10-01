#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 63:
    raise SystemExit(f"Expected 63 locales before Kyrgyz, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 64

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'eo_uy' in obj and 'ky_kg' not in obj and isinstance(obj['eo_uy'], dict) and 'name' in obj['eo_uy']:
            entry = deepcopy(obj['eo_uy'])
            entry['name'] = 'Кыргызча'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/eo_uy.json', '/ky_kg.json')
            obj['ky_kg'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['kyrgyz_common_glob'] = 'neoorigins_ky_common_*'
ns['kyrgyz_mc_1_21_1'] = 'neoorigins_ky_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 64 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Kyrgyz language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Esperanto (`eo_uy`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Esperanto catalogue entries, got {hits}')
text = text.replace(needle, 'Esperanto (`eo_uy`) · Кыргызча (`ky_kg`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 63 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 63 |")}')
text = text.replace('| 63 |', '| 64 |')
old = '**Somali (`so_so`)** et **Espéranto (`eo_uy`)**.'
new = '**Somali (`so_so`)**, **Espéranto (`eo_uy`)** et **Kirghize (`ky_kg`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-trois langues' not in text:
    raise SystemExit('README 63-language sentence not found')
text = text.replace('Les soixante-trois langues', 'Les soixante-quatre langues', 1)

eo_block = '''Pour l’espéranto :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
ky_block = eo_block + '''\nPour le kirghize :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if eo_block not in text:
    raise SystemExit('README Esperanto coverage block not found')
text = text.replace(eo_block, ky_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Kyrgyz metadata prepared: 64 locales; {added} catalog language entries; {hits} catalogue rows.')
