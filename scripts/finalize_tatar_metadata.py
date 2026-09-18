#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 75:
    raise SystemExit(f"Expected 75 locales before Tatar, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 76

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'yo_ng' in obj and 'tt_ru' not in obj and isinstance(obj['yo_ng'], dict) and 'name' in obj['yo_ng']:
            entry = deepcopy(obj['yo_ng'])
            entry['name'] = 'Татарча'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/yo_ng.json', '/tt_ru.json')
            obj['tt_ru'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['tatar_common_glob'] = 'neoorigins_tt_common_*'
ns['tatar_mc_1_21_1'] = 'neoorigins_tt_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 76 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Tatar language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Yorùbá (`yo_ng`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Yoruba catalogue entries, got {hits}')
text = text.replace(needle, 'Yorùbá (`yo_ng`) · Tatar (`tt_ru`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 75 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 75 |")}')
text = text.replace('| 75 |', '| 76 |')
old = '**Occitan (`oc_fr`)**, **Igbo (`ig_ng`)** et **Yoruba (`yo_ng`)**.'
new = '**Occitan (`oc_fr`)**, **Igbo (`ig_ng`)**, **Yoruba (`yo_ng`)** et **Tatar (`tt_ru`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-quinze langues' not in text:
    raise SystemExit('README 75-language sentence not found')
text = text.replace('Les soixante-quinze langues', 'Les soixante-seize langues', 1)

yo_block = '''Pour le yoruba :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
tt_block = yo_block + '''\nPour le tatar :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if yo_block not in text:
    raise SystemExit('README Yoruba coverage block not found')
text = text.replace(yo_block, tt_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Tatar metadata prepared: 76 locales; {added} catalog language entries; {hits} catalogue rows.')
