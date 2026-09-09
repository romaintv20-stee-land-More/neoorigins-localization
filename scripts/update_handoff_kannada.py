#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:180]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 56 locales:', '0.9.0 development currently has 57 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by, fo_fo, af_za, az_az.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by, fo_fo, af_za, az_az, kn_in.')
once('- 56: Azerbaijani / az_az\n', '- 56: Azerbaijani / az_az\n- 57: Kannada / kn_in\n')
once('FIFTY-SIX IS NOT THE FINAL TARGET.', 'FIFTY-SEVEN IS NOT THE FINAL TARGET.')

for old, new in [
    ('49. NEXT ACTION', '50. NEXT ACTION'),
    ('48. QUALITY / QA CAVEAT', '49. QUALITY / QA CAVEAT'),
    ('47. SOURCE OF TRUTH HIERARCHY', '48. SOURCE OF TRUTH HIERARCHY'),
    ('46. CURRENT PERMANENT CI / BUILD VALIDATION', '47. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('45. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '46. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '46. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''45. KANNADA 0.9.0 STATUS
----------------------------
Kannada locale: kn_in / ಕನ್ನಡ.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Kannada is a current Minecraft Java locale (kn_in).
- It is a distinct Dravidian language with its own Kannada script, grammar and vocabulary, with no regional-dedup conflict in the supported set.
- It therefore satisfies the regional-dedup rule.

Kannada architecture:
- 16 common namespaces: neoorigins_kn_common_01 through neoorigins_kn_common_16
- 1.21.1-specific namespace: neoorigins_kn_121
- 26.1.x uses kn_in inside neoorigins_26_1
- 26.2 uses kn_in inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive kn_in fallback files
- Gradle target switch: include_kannada_121_translations / includeKannada121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Kannada strings. Therefore all 10 Kannada add-on fallback files are required.

Kannada coverage:
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

Kannada bootstrap:
- working branch: release/0.9.0-kannada
- workflow: .github/workflows/bootstrap-kannada.yml
- workflow run 34375980559: SUCCESS
- validated localization commit 2c52327192c805d3fafff984f98458e8b3f9c81f ("Add Kannada localization fallback")
- audit artifact ID 10113935206; size 291,549 bytes; SHA256 fff9418c8fe475b5731db1d92e11fefbbec06269b7fdbf4d31dbb8582950e362
- translation generation produced 2,734 unique strings total: 18 manual/pre-seeded entries plus 2,716 newly translated strings in 79 batches
- title-like refinement generated 3 additional requests and improved 2 / 6 title-like English remnants
- final bootstrap cache contained 2,737 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile printf and numbered-placeholder strings were pre-seeded/protected; punctuation/digit-only sentinels use whitespace-tolerant restoration and numbered placeholders are compared as sorted sets
- bootstrap sanity passed with 1,573 Kannada lexical markers and 116,549 Kannada-script characters across 29 kn_in files

Kannada contextual refinement:
- workflow: .github/workflows/refine-kannada.yml
- first refinement run 34376823511 stopped only on an intentionally strict linguistic false-friend guard after all structural NeoOrigins/add-on audits had already passed; this was not a coverage, placeholder or JSON failure
- the remaining Scales -> measuring-scales false-friend form was normalized to creature scales without weakening the guard
- final workflow run 34377027911: SUCCESS
- refinement commit 657e49555bf2f94150cacc2c55843c7545a2efea ("Refine Kannada Minecraft terminology")
- 287 values corrected across 19 files
- corrected contextual false friends and Minecraft/Origins terminology including Power/ability wording, Origin/Class labels, Apply, Loot/Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether, Pavlov, creature Scales, health/XP wording and Origin Architect HUD labels
- all 64 generated hotkey labels were normalized to ಹಾಟ್‌ಕೀ NN
- final sanity: 1,575 Kannada lexical markers and 116,278 Kannada-script characters across 29 kn_in source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Kannada metadata:
- synchronization run 34377471271: SUCCESS
- metadata commit 30f4642692743bfa96bf1e341d3a2080fabd80a9 ("Document Kannada localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 57 supported locales and include kn_in / ಕನ್ನಡ

Final Kannada three-target CI:
- workflow: .github/workflows/build-0.9.0-kannada.yml
- workflow commit 611e5fa951ada19ce83c524ad10f16d8f2dc2409
- run ID 34377605054: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Kannada terminology/script sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Kannada terminology/script sanity, Gradle build, exact packaging verification and JAR upload

Kannada packaging verified by CI:
- 1.21.1: 27 kn_in files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 kn_in files = 16 common + correct 26.1 delta
- 26.2: 17 kn_in files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_kn_121 leaked into 26.x

Final Kannada JAR artifacts from run 34377605054:
- mc-1.21.1: artifact ID 10114557230; size 4,473,026 bytes; SHA256 8a211f537a39ef0c8a191eb41a12b6232bddb524e68f715d2c7235477acdb56d
- mc-26.1.x: artifact ID 10114582771; size 2,431,935 bytes; SHA256 66c31bd567a78255d4c4c912425e27ee365f1836ea7f94a2ef4ee50d7ddb006e
- mc-26.2: artifact ID 10114546850; size 2,431,538 bytes; SHA256 6214331ee1a694ddef8ae8c63035ac958f8ac8584e31764b9c417d5ab5c44d92

Kannada QA caveat:
- The localization uses automated/generative translation assistance, structural QA and manual contextual refinement.
- It has not been fully reviewed by a native Kannada speaker; do not present CI success as native-speaker perfection.

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 56 supported locales', '- catalog.json says 57 supported locales')
once('- README.md says 56 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk, Belarusian be_by, Faroese fo_fo, Afrikaans af_za and Azerbaijani az_az', '- README.md says 57 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk, Belarusian be_by, Faroese fo_fo, Afrikaans af_za, Azerbaijani az_az and Kannada kn_in')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian, Belarusian, Faroese, Afrikaans and Azerbaijani have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian, Belarusian, Faroese, Afrikaans, Azerbaijani and Kannada have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 57.', 'NEXT LANGUAGE = language 58.')
once('Do not stop permanently at 57;', 'Do not stop permanently at 58;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 57 locales, Kannada #57, next #58')
