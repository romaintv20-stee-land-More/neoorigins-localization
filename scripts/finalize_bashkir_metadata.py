#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 68:
    raise SystemExit(f"Expected 68 locales before Bashkir, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 69

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'bs_ba' in obj and 'ba_ru' not in obj and isinstance(obj['bs_ba'], dict) and 'name' in obj['bs_ba']:
            entry = deepcopy(obj['bs_ba'])
            entry['name'] = 'Башҡортса'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/bs_ba.json', '/ba_ru.json')
            obj['ba_ru'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['bashkir_common_glob'] = 'neoorigins_ba_common_*'
ns['bashkir_mc_1_21_1'] = 'neoorigins_ba_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 69 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Bashkir language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Bosanski (`bs_ba`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Bosnian catalogue entries, got {hits}')
text = text.replace(needle, 'Bosanski (`bs_ba`) · Башҡортса (`ba_ru`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 68 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 68 |")}')
text = text.replace('| 68 |', '| 69 |')
old = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)** et **Bosnien (`bs_ba`)**.'
new = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)** et **Bachkir (`ba_ru`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-huit langues' not in text:
    raise SystemExit('README 68-language sentence not found')
text = text.replace('Les soixante-huit langues', 'Les soixante-neuf langues', 1)

bs_block = '''Pour le bosnien :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
ba_block = bs_block + '''\nPour le bachkir :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if bs_block not in text:
    raise SystemExit('README Bosnian coverage block not found')
text = text.replace(bs_block, ba_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Bashkir metadata prepared: 69 locales; {added} catalog language entries; {hits} catalogue rows.')
