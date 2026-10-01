#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 72:
    raise SystemExit(f"Expected 72 locales before Occitan, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 73

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'fy_nl' in obj and 'oc_fr' not in obj and isinstance(obj['fy_nl'], dict) and 'name' in obj['fy_nl']:
            entry = deepcopy(obj['fy_nl'])
            entry['name'] = 'Occitan'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/fy_nl.json', '/oc_fr.json')
            obj['oc_fr'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['occitan_common_glob'] = 'neoorigins_oc_common_*'
ns['occitan_mc_1_21_1'] = 'neoorigins_oc_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 73 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Occitan language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Frysk (`fy_nl`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Frisian catalogue entries, got {hits}')
text = text.replace(needle, 'Frysk (`fy_nl`) · Occitan (`oc_fr`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 72 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 72 |")}')
text = text.replace('| 72 |', '| 73 |')
old = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)**, **Asturien (`ast_es`)** et **Frison occidental (`fy_nl`)**.'
new = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)**, **Asturien (`ast_es`)**, **Frison occidental (`fy_nl`)** et **Occitan (`oc_fr`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-douze langues' not in text:
    raise SystemExit('README 72-language sentence not found')
text = text.replace('Les soixante-douze langues', 'Les soixante-treize langues', 1)

fy_block = '''Pour le frison occidental :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
oc_block = fy_block + '''\nPour l'occitan :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if fy_block not in text:
    raise SystemExit('README Frisian coverage block not found')
text = text.replace(fy_block, oc_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Occitan metadata prepared: 73 locales; {added} catalog language entries; {hits} catalogue rows.')
