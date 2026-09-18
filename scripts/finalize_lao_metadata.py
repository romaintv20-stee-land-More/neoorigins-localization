#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
if catalog['project']['supported_locale_count'] != 66:
    raise SystemExit(f"Expected 66 locales before Lao, got {catalog['project']['supported_locale_count']}")
catalog['project']['supported_locale_count'] = 67

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'sq_al' in obj and 'lo_la' not in obj and isinstance(obj['sq_al'], dict) and 'name' in obj['sq_al']:
            entry = deepcopy(obj['sq_al'])
            entry['name'] = 'ລາວ'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/sq_al.json', '/lo_la.json')
            obj['lo_la'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['lao_common_glob'] = 'neoorigins_lo_common_*'
ns['lao_mc_1_21_1'] = 'neoorigins_lo_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 67 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Lao language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = 'Shqip (`sq_al`)'
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Albanian catalogue entries, got {hits}')
text = text.replace(needle, 'Shqip (`sq_al`) · ລາວ (`lo_la`)')
p.write_text(text, encoding='utf-8')

p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 66 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 66 |")}')
text = text.replace('| 66 |', '| 67 |')
old = '**Somali (`so_so`)**, **Espéranto (`eo_uy`)**, **Kirghize (`ky_kg`)**, **Tamoul (`ta_in`)** et **Albanais (`sq_al`)**.'
new = '**Somali (`so_so`)**, **Espéranto (`eo_uy`)**, **Kirghize (`ky_kg`)**, **Tamoul (`ta_in`)**, **Albanais (`sq_al`)** et **Lao (`lo_la`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les soixante-six langues' not in text:
    raise SystemExit('README 66-language sentence not found')
text = text.replace('Les soixante-six langues', 'Les soixante-sept langues', 1)

sq_block = '''Pour l’albanais :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
lo_block = sq_block + '''\nPour le lao :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if sq_block not in text:
    raise SystemExit('README Albanian coverage block not found')
text = text.replace(sq_block, lo_block, 1)
p.write_text(text, encoding='utf-8')

print(f'Lao metadata prepared: 67 locales; {added} catalog language entries; {hits} catalogue rows.')
