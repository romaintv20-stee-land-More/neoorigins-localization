#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 65:
    raise SystemExit(f"Expected 65 locales before Tagalog, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 66

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'ta_in' in obj and 'tl_ph' not in obj and isinstance(obj['ta_in'], dict) and 'name' in obj['ta_in']:
            entry = deepcopy(obj['ta_in'])
            entry['name'] = 'Tagalog'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/ta_in.json', '/tl_ph.json')
            obj['tl_ph'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['tagalog_common_glob'] = 'neoorigins_tl_common_*'
ns['tagalog_mc_1_21_1'] = 'neoorigins_tl_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 66 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Tagalog language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'தமிழ் (`ta_in`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Tamil catalogue entries, got {hits}')
text = text.replace(needle, 'தமிழ் (`ta_in`) · Tagalog (`tl_ph`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 65 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 65 |")}')
text = text.replace('| 65 |', '| 66 |')
old = '**Somali (`so_so`)**, **Espéranto (`eo_uy`)**, **Kirghize (`ky_kg`)** et **Tamoul (`ta_in`)**.'
new = '**Somali (`so_so`)**, **Espéranto (`eo_uy`)**, **Kirghize (`ky_kg`)**, **Tamoul (`ta_in`)** et **Tagalog (`tl_ph`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-cinq langues' not in text:
    raise SystemExit('README 65-language sentence not found')
text = text.replace('Les soixante-cinq langues', 'Les soixante-six langues', 1)

ta_block = '''Pour le tamoul :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
tl_block = ta_block + '''\nPour le tagalog :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if ta_block not in text:
    raise SystemExit('README Tamil coverage block not found')
text = text.replace(ta_block, tl_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Tagalog metadata prepared: 66 locales; {added} catalog language entries; {hits} catalogue rows.')
