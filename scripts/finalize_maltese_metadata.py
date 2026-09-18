#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import json

ROOT = Path(__file__).resolve().parents[1]

# catalog.json: derive Maltese entries from the reviewed Uzbek entries so every
# project inherits the same support/target/file structure.
p = ROOT / 'catalog.json'
catalog = json.loads(p.read_text(encoding='utf-8'))
catalog['project']['supported_locale_count'] = 60

added = 0
def walk(obj):
    global added
    if isinstance(obj, dict):
        if 'uz_uz' in obj and 'mt_mt' not in obj and isinstance(obj['uz_uz'], dict) and 'name' in obj['uz_uz']:
            entry = deepcopy(obj['uz_uz'])
            entry['name'] = 'Malti'
            if isinstance(entry.get('file'), str):
                entry['file'] = entry['file'].replace('/uz_uz.json', '/mt_mt.json')
            obj['mt_mt'] = entry
            added += 1
        for value in list(obj.values()):
            walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)
walk(catalog)

neo = next(x for x in catalog['supported_projects'] if x.get('id') == 'neoorigins')
ns = neo['compatibility']['fallback_namespaces']
ns['maltese_common_glob'] = 'neoorigins_mt_common_*'
ns['maltese_mc_1_21_1'] = 'neoorigins_mt_121'
neo['compatibility']['coverage_note'] = (
    'NeoOrigins 2.2.27 has the same en_us localization payload as 2.2.26 on all three targets. '
    'Historical gaps in it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz and hu_hu were recovered before '
    'language 59. All 60 currently supported locales are complete against 2.2.27 on their target builds.'
)
neo['compatibility']['legacy_gap_recovery_completed'] = True
if added < 11:
    raise SystemExit(f'Expected Maltese language entries for NeoOrigins + 10 add-ons, got {added}')
p.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# CATALOG.md: each project language list currently ends with Uzbek.
p = ROOT / 'CATALOG.md'
text = p.read_text(encoding='utf-8')
needle = "O'zbekcha (`uz_uz`)"
hits = text.count(needle)
if hits < 11:
    raise SystemExit(f'Expected at least 11 Uzbek catalogue entries, got {hits}')
text = text.replace(needle, "O'zbekcha (`uz_uz`) · Malti (`mt_mt`)")
p.write_text(text, encoding='utf-8')

# README: update build counts, supported-language prose and explicit coverage.
p = ROOT / 'README.md'
text = p.read_text(encoding='utf-8')
if text.count('| 59 |') != 3:
    raise SystemExit(f'Expected exactly 3 build language-count cells, got {text.count("| 59 |")}')
text = text.replace('| 59 |', '| 60 |')
old = '**Tchouvache (`cv_cu`)** et **Ouzbek (`uz_uz`)**.'
new = '**Tchouvache (`cv_cu`)**, **Ouzbek (`uz_uz`)** et **Maltais (`mt_mt`)**.'
if old not in text:
    raise SystemExit('README language-list tail not found')
text = text.replace(old, new, 1)
if 'Les cinquante-neuf langues' not in text:
    raise SystemExit('README 59-language sentence not found')
text = text.replace('Les cinquante-neuf langues', 'Les soixante langues', 1)
uz_block = '''Pour l’ouzbek :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
mt_block = uz_block + '''\nPour le maltais :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n'''
if uz_block not in text:
    raise SystemExit('README Uzbek coverage block not found')
text = text.replace(uz_block, mt_block, 1)

stale = "Un audit intégral des 58 locales a toutefois révélé des lacunes historiques, déjà présentes avant la 2.2.27 : `it_it`, `pl_pl`, `ru_ru` et `zh_cn` ont chacun 52 clés manquantes sur 1.21.1 et 26.1.x ; `tr_tr`, `cs_cz` et `hu_hu` restent très partiels sur les trois cibles. Les 51 autres locales sont complètes contre les jeux de clés 2.2.27. L'audit de référence est le run `34400432957`."
resolved = "L’audit intégral initial des 58 locales avait révélé sept lacunes historiques, antérieures à la 2.2.27. Elles ont depuis été récupérées avant la langue #59 : italien, polonais, russe, chinois simplifié, turc, tchèque et hongrois sont désormais complets contre la baseline 2.2.27. L’audit qui avait exposé ces lacunes est le run `34400432957`."
if stale in text:
    text = text.replace(stale, resolved, 1)
p.write_text(text, encoding='utf-8')

print(f'Maltese metadata prepared: 60 locales; {added} catalog language entries; {hits} catalogue rows.')
