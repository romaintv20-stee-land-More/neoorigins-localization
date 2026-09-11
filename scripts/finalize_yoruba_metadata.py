#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 74:
    raise SystemExit(f"Expected 74 locales before Yoruba, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 75

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'ig_ng' in obj and 'yo_ng' not in obj and isinstance(obj['ig_ng'], dict) and 'name' in obj['ig_ng']:
            entry = deepcopy(obj['ig_ng'])
            entry['name'] = 'Yorùbá'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/ig_ng.json', '/yo_ng.json')
            obj['yo_ng'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['yoruba_common_glob'] = 'neoorigins_yo_common_*'
ns['yoruba_mc_1_21_1'] = 'neoorigins_yo_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 75 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Yoruba language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Igbo (`ig_ng`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Igbo catalogue entries, got {hits}')
text = text.replace(needle, 'Igbo (`ig_ng`) · Yorùbá (`yo_ng`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 74 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 74 |")}')
text = text.replace('| 74 |', '| 75 |')
old = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)**, **Asturien (`ast_es`)**, **Frison occidental (`fy_nl`)**, **Occitan (`oc_fr`)** et **Igbo (`ig_ng`)**.'
new = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)**, **Asturien (`ast_es`)**, **Frison occidental (`fy_nl`)**, **Occitan (`oc_fr`)**, **Igbo (`ig_ng`)** et **Yoruba (`yo_ng`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-quatorze langues' not in text:
    raise SystemExit('README 74-language sentence not found')
text = text.replace('Les soixante-quatorze langues', 'Les soixante-quinze langues', 1)

ig_block = '''Pour l'igbo :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
yo_block = ig_block + '''\nPour le yoruba :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if ig_block not in text:
    raise SystemExit('README Igbo coverage block not found')
text = text.replace(ig_block, yo_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Yoruba metadata prepared: 75 locales; {added} catalog language entries; {hits} catalogue rows.')
