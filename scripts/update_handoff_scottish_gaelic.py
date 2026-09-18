#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:120]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 46 locales:', '0.9.0 development currently has 47 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb.')
once('- 46: Irish / ga_ie\n', '- 46: Irish / ga_ie\n- 47: Scottish Gaelic / gd_gb\n')
once('FORTY-SIX IS NOT THE FINAL TARGET.', 'FORTY-SEVEN IS NOT THE FINAL TARGET.')

# Make room for Scottish Gaelic while preserving sequential status/governance headings.
for old, new in [
    ('39. NEXT ACTION', '40. NEXT ACTION'),
    ('38. QUALITY / QA CAVEAT', '39. QUALITY / QA CAVEAT'),
    ('37. SOURCE OF TRUTH HIERARCHY', '38. SOURCE OF TRUTH HIERARCHY'),
    ('36. CURRENT PERMANENT CI / BUILD VALIDATION', '37. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('35. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '36. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '36. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''35. SCOTTISH GAELIC 0.9.0 STATUS
------------------------------------
Scottish Gaelic locale: gd_gb / Gàidhlig.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Scottish Gaelic is a current Minecraft Java locale (gd_gb).
- It is a distinct Celtic language with materially different vocabulary, orthography and written standard from Irish ga_ie.
- It therefore remains separate under the regional-dedup rule.

Scottish Gaelic architecture:
- 16 common namespaces: neoorigins_gd_common_01 through neoorigins_gd_common_16
- 1.21.1-specific namespace: neoorigins_gd_121
- 26.1.x uses gd_gb inside neoorigins_26_1
- 26.2 uses gd_gb inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive gd_gb fallback files
- Gradle target switch: include_scottish_gaelic_121_translations / includeScottishGaelic121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Scottish Gaelic strings. Therefore all 10 Scottish Gaelic add-on fallback files are required.

Scottish Gaelic coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- Medieval Origins Revival: 401 / 401
- ibarn's quartet origins addon: 69 / 69
- Origins Fantasy for NeoOrigins: 240 / 240
- Origins: Backgrounds for NeoOrigins: 65 / 65
- Origins: More Backgrounds for NeoOrigins: 44 / 44 effective (39 primary + 5 shared)
- Origins: Backgrounds ISS for NeoOrigins: 79 / 79 effective (77 primary + 2 shared)
- Origins Furries: 117 / 117
- Origins: Classes Extended: 124 / 124
- Origins: Classes ISS: 99 / 99
- Origin Architect: 22 / 22
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed

Scottish Gaelic bootstrap:
- working branch: release/0.9.0-scottish-gaelic
- workflow: .github/workflows/bootstrap-scottish-gaelic.yml
- workflow run 34343738900: SUCCESS
- validated localization commit 1e7818ca8e37c1272d83e601b5a48ceed0229123 ("Add Scottish Gaelic localization fallback")
- audit artifact ID 10100898175; size 291,554 bytes; SHA256 5524494d4d7f2f26c328cc5dde2d37b81e96f3d41c24ea23012ce54a3dc83076
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- title-like refinement generated 194 additional requests in 6 batches and improved 137 / 197 title-like English remnants
- final bootstrap cache contained 2,928 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile numbered-placeholder death messages were manually pre-seeded and placeholder sets were structurally audited
- bootstrap lexical sanity passed with 4,486 Scottish Gaelic markers across 29 gd_gb files

Scottish Gaelic contextual refinement:
- workflow: .github/workflows/refine-scottish-gaelic.yml
- workflow run 34344341346: SUCCESS
- refinement commit b823e165503fa1e084ef3e7305aff1e389427559 ("Refine Scottish Gaelic Minecraft terminology")
- 338 values corrected across 21 files, including 252 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Apply, NeoOrigins/Origin labels, Merling, Avian, Blazeling, Enderian, Shulk, Night Vision, Ultimine, Nether/Netherite, Drops, Spawn Rules, Charge, Pavlov, Scales and Origin Architect HUD labels
- final lexical sanity: 4,492 Scottish Gaelic markers across 29 gd_gb source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- post-refinement JSON validation passed

Scottish Gaelic metadata:
- synchronization run 34344489324: SUCCESS
- metadata commit 0ef740a58e1990fed4977ad88a78bba0bc0464b2 ("Document Scottish Gaelic localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 47 supported locales and include gd_gb / Gàidhlig

Final Scottish Gaelic three-target CI:
- workflow: .github/workflows/build-0.9.0-scottish-gaelic.yml
- workflow commit 59c64e43c474fa99d310f6b7b2ffd79eb8ce2556
- run ID 34344582845: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Scottish Gaelic lexical sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Scottish Gaelic lexical sanity, Gradle build, exact packaging verification and JAR upload

Scottish Gaelic packaging verified by CI:
- 1.21.1: 27 gd_gb files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 gd_gb files = 16 common + correct 26.1 delta
- 26.2: 17 gd_gb files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_gd_121 leaked into 26.x

Final Scottish Gaelic JAR artifacts from run 34344582845:
- mc-1.21.1: artifact ID 10101193897; size 3,524,041 bytes; SHA256 82f24fdda35779da9305ca47e4cf32b30bc48d655532e80cf5693edc02a81d30
- mc-26.1.x: artifact ID 10101186193; size 1,873,985 bytes; SHA256 6877e40123c3b65899894a5dfd7ed1a8bdf9cc889d39fdbd95a30fd76510b2e9
- mc-26.2: artifact ID 10101179556; size 1,873,497 bytes; SHA256 cde8e89f337dacff7e655ec0e53e66dc9d99a4b04cbb9dab444c3945526b7624

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 46 supported locales', '- catalog.json says 47 supported locales')
once('- README.md says 46 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb and Irish ga_ie', '- README.md says 47 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie and Scottish Gaelic gd_gb')
old = 'Persian, Icelandic, Malay, Filipino, Welsh and Irish have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish and Scottish Gaelic have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 47.', 'NEXT LANGUAGE = language 48.')
once('Do not stop permanently at 47;', 'Do not stop permanently at 48;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 47 locales, Scottish Gaelic #47, next #48')
