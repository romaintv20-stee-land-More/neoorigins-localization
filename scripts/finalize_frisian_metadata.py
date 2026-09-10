#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 71:
    raise SystemExit(f"Expected 71 locales before Frisian, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 72

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'ast_es' in obj and 'fy_nl' not in obj and isinstance(obj['ast_es'], dict) and 'name' in obj['ast_es']:
            entry = deepcopy(obj['ast_es'])
            entry['name'] = 'Frysk'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/ast_es.json', '/fy_nl.json')
            obj['fy_nl'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['frisian_common_glob'] = 'neoorigins_fy_common_*'
ns['frisian_mc_1_21_1'] = 'neoorigins_fy_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 72 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Frisian language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Asturianu (`ast_es`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Asturian catalogue entries, got {hits}')
text = text.replace(needle, 'Asturianu (`ast_es`) · Frysk (`fy_nl`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 71 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 71 |")}')
text = text.replace('| 71 |', '| 72 |')
old = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)** et **Asturien (`ast_es`)**.'
new = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)**, **Asturien (`ast_es`)** et **Frison occidental (`fy_nl`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-et-onze langues' not in text:
    raise SystemExit('README 71-language sentence not found')
text = text.replace('Les soixante-et-onze langues', 'Les soixante-douze langues', 1)

ast_block = '''Pour l'asturien :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
fy_block = ast_block + '''\nPour le frison occidental :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if ast_block not in text:
    raise SystemExit('README Asturian coverage block not found')
text = text.replace(ast_block, fy_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Frisian metadata prepared: 72 locales; {added} catalog language entries; {hits} catalogue rows.')
