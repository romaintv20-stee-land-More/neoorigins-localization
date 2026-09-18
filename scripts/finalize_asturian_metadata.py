#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 70:
    raise SystemExit(f"Expected 70 locales before Asturian, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 71

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'br_fr' in obj and 'ast_es' not in obj and isinstance(obj['br_fr'], dict) and 'name' in obj['br_fr']:
            entry = deepcopy(obj['br_fr'])
            entry['name'] = 'Asturianu'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/br_fr.json', '/ast_es.json')
            obj['ast_es'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['asturian_common_glob'] = 'neoorigins_ast_common_*'
ns['asturian_mc_1_21_1'] = 'neoorigins_ast_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 71 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Asturian language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Brezhoneg (`br_fr`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Breton catalogue entries, got {hits}')
text = text.replace(needle, 'Brezhoneg (`br_fr`) · Asturianu (`ast_es`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 70 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 70 |")}')
text = text.replace('| 70 |', '| 71 |')
old = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)** et **Breton (`br_fr`)**.'
new = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)** et **Asturien (`ast_es`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-dix langues' not in text:
    raise SystemExit('README 70-language sentence not found')
text = text.replace('Les soixante-dix langues', 'Les soixante-et-onze langues', 1)

br_block = '''Pour le breton :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
ast_block = br_block + '''\nPour l'asturien :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if br_block not in text:
    raise SystemExit('README Breton coverage block not found')
text = text.replace(br_block, ast_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Asturian metadata prepared: 71 locales; {added} catalog language entries; {hits} catalogue rows.')
