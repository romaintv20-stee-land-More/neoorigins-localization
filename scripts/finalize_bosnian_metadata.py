#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 67:
    raise SystemExit(f"Expected 67 locales before Bosnian, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 68

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'lo_la' in obj and 'bs_ba' not in obj and isinstance(obj['lo_la'], dict) and 'name' in obj['lo_la']:
            entry = deepcopy(obj['lo_la'])
            entry['name'] = 'Bosanski'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/lo_la.json', '/bs_ba.json')
            obj['bs_ba'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['bosnian_common_glob'] = 'neoorigins_bs_common_*'
ns['bosnian_mc_1_21_1'] = 'neoorigins_bs_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 68 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Bosnian language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'ລາວ (`lo_la`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Lao catalogue entries, got {hits}')
text = text.replace(needle, 'ລາວ (`lo_la`) · Bosanski (`bs_ba`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 67 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 67 |")}')
text = text.replace('| 67 |', '| 68 |')
old = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)** et **Lao (`lo_la`)**.'
new = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)** et **Bosnien (`bs_ba`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-sept langues' not in text:
    raise SystemExit('README 67-language sentence not found')
text = text.replace('Les soixante-sept langues', 'Les soixante-huit langues', 1)

lo_block = '''Pour le lao :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
bs_block = lo_block + '''\nPour le bosnien :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if lo_block not in text:
    raise SystemExit('README Lao coverage block not found')
text = text.replace(lo_block, bs_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Bosnian metadata prepared: 68 locales; {added} catalog language entries; {hits} catalogue rows.')
