#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 69:
    raise SystemExit(f"Expected 69 locales before Breton, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 70

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'ba_ru' in obj and 'br_fr' not in obj and isinstance(obj['ba_ru'], dict) and 'name' in obj['ba_ru']:
            entry = deepcopy(obj['ba_ru'])
            entry['name'] = 'Brezhoneg'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/ba_ru.json', '/br_fr.json')
            obj['br_fr'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['breton_common_glob'] = 'neoorigins_br_common_*'
ns['breton_mc_1_21_1'] = 'neoorigins_br_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 70 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Breton language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Башҡортса (`ba_ru`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Bashkir catalogue entries, got {hits}')
text = text.replace(needle, 'Башҡортса (`ba_ru`) · Brezhoneg (`br_fr`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 69 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 69 |")}')
text = text.replace('| 69 |', '| 70 |')
old = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)** et **Bachkir (`ba_ru`)**.'
new = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)** et **Breton (`br_fr`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-neuf langues' not in text:
    raise SystemExit('README 69-language sentence not found')
text = text.replace('Les soixante-neuf langues', 'Les soixante-dix langues', 1)

ba_block = '''Pour le bachkir :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
br_block = ba_block + '''\nPour le breton :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if ba_block not in text:
    raise SystemExit('README Bashkir coverage block not found')
text = text.replace(ba_block, br_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Breton metadata prepared: 70 locales; {added} catalog language entries; {hits} catalogue rows.')
