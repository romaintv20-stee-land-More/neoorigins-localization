#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 73:
    raise SystemExit(f"Expected 73 locales before Igbo, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 74

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'oc_fr' in obj and 'ig_ng' not in obj and isinstance(obj['oc_fr'], dict) and 'name' in obj['oc_fr']:
            entry = deepcopy(obj['oc_fr'])
            entry['name'] = 'Igbo'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/oc_fr.json', '/ig_ng.json')
            obj['ig_ng'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['igbo_common_glob'] = 'neoorigins_ig_common_*'
ns['igbo_mc_1_21_1'] = 'neoorigins_ig_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 74 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Igbo language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Occitan (`oc_fr`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Occitan catalogue entries, got {hits}')
text = text.replace(needle, 'Occitan (`oc_fr`) · Igbo (`ig_ng`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 73 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 73 |")}')
text = text.replace('| 73 |', '| 74 |')
old = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)**, **Asturien (`ast_es`)**, **Frison occidental (`fy_nl`)** et **Occitan (`oc_fr`)**.'
new = '**Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)**, **Asturien (`ast_es`)**, **Frison occidental (`fy_nl`)**, **Occitan (`oc_fr`)** et **Igbo (`ig_ng`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-treize langues' not in text:
    raise SystemExit('README 73-language sentence not found')
text = text.replace('Les soixante-treize langues', 'Les soixante-quatorze langues', 1)

oc_block = '''Pour l'occitan :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
ig_block = oc_block + '''\nPour l'igbo :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if oc_block not in text:
    raise SystemExit('README Occitan coverage block not found')
text = text.replace(oc_block, ig_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Igbo metadata prepared: 74 locales; {added} catalog language entries; {hits} catalogue rows.')
