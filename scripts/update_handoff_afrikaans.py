#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:180]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 54 locales:', '0.9.0 development currently has 55 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by, fo_fo.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by, fo_fo, af_za.')
once('- 54: Faroese / fo_fo\n', '- 54: Faroese / fo_fo\n- 55: Afrikaans / af_za\n')
once('FIFTY-FOUR IS NOT THE FINAL TARGET.', 'FIFTY-FIVE IS NOT THE FINAL TARGET.')

for old, new in [
    ('47. NEXT ACTION', '48. NEXT ACTION'),
    ('46. QUALITY / QA CAVEAT', '47. QUALITY / QA CAVEAT'),
    ('45. SOURCE OF TRUTH HIERARCHY', '46. SOURCE OF TRUTH HIERARCHY'),
    ('44. CURRENT PERMANENT CI / BUILD VALIDATION', '45. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('43. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '44. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '44. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''43. AFRIKAANS 0.9.0 STATUS
-----------------------------
Afrikaans locale: af_za / Afrikaans.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Afrikaans is a current Minecraft Java locale (af_za).
- It is a distinct language with materially different grammar, vocabulary and usage from Dutch, not merely a regional Dutch variant.
- It therefore satisfies the regional-dedup rule.

Afrikaans architecture:
- 16 common namespaces: neoorigins_af_common_01 through neoorigins_af_common_16
- 1.21.1-specific namespace: neoorigins_af_121
- 26.1.x uses af_za inside neoorigins_26_1
- 26.2 uses af_za inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive af_za fallback files
- Gradle target switch: include_afrikaans_121_translations / includeAfrikaans121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Afrikaans strings. Therefore all 10 Afrikaans add-on fallback files are required.

Afrikaans coverage:
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

Afrikaans bootstrap:
- working branch: release/0.9.0-afrikaans
- workflow: .github/workflows/bootstrap-afrikaans.yml
- workflow run 34368581196: SUCCESS
- validated localization commit 6fae166cc0902e0e321e0d086aae6781fb7e420c ("Add Afrikaans localization fallback")
- audit artifact ID 10111026940; size 291,551 bytes; SHA256 d66d5c3ec98bf9ded5705892d547bd0fec85ffb17cfd79c855c1aebe81a114e2
- translation generation produced 2,734 unique strings total: 18 manual/pre-seeded entries plus 2,716 newly translated strings in 79 batches
- title-like refinement generated 229 additional requests in 7 batches and improved 179 / 232 title-like English remnants
- final bootstrap cache contained 2,963 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile printf and numbered-placeholder strings were pre-seeded/protected; punctuation/digit-only sentinels use whitespace-tolerant restoration and numbered placeholders are compared as sorted sets
- bootstrap lexical sanity passed with 3,265 Afrikaans lexical markers across 29 af_za files

Afrikaans contextual refinement:
- workflow: .github/workflows/refine-afrikaans.yml
- refinement runs 34369401285 and 34369627182 stopped only on an intentionally strict linguistic false-friend guard after all structural NeoOrigins/add-on audits had already passed; they were not coverage, placeholder, JSON or build failures
- the remaining Geplavei/Pavlov machine-translation false-friend forms were then normalized without weakening the guard
- final workflow run 34369946175: SUCCESS
- refinement commit 327fa0a292fff861f7de073df1a38e277c2007f3 ("Refine Afrikaans Minecraft terminology")
- 299 values corrected across 19 files
- corrected contextual false friends and Minecraft/Origins terminology including Power/ability wording, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Charge, Pavlov, Scales, experience and Origin Architect HUD labels
- all 64 generated hotkey labels were normalized to Sneltoets NN
- final sanity: 3,269 Afrikaans lexical markers across 29 af_za source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Afrikaans metadata:
- synchronization run 34370294595: SUCCESS
- metadata commit da47b89fee91f3b5c48c9a751d29025b49b9c71f ("Document Afrikaans localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 55 supported locales and include af_za / Afrikaans

Final Afrikaans three-target CI:
- workflow: .github/workflows/build-0.9.0-afrikaans.yml
- workflow commit 38614220ed18a2940ed2c3fcab96d8122929e779
- run ID 34370462722: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Afrikaans terminology/lexical sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Afrikaans terminology/lexical sanity, Gradle build, exact packaging verification and JAR upload

Afrikaans packaging verified by CI:
- 1.21.1: 27 af_za files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 af_za files = 16 common + correct 26.1 delta
- 26.2: 17 af_za files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_af_121 leaked into 26.x

Final Afrikaans JAR artifacts from run 34370462722:
- mc-1.21.1: artifact ID 10111730427; size 4,282,958 bytes; SHA256 ee23579434ad9423256d23bdda70474da8e855e04353069eccfac0cf665afa1b
- mc-26.1.x: artifact ID 10111725668; size 2,320,033 bytes; SHA256 86ec16a6abe774e79899e22ad4406a584b6098278b2d4b6b06be1543595f7272
- mc-26.2: artifact ID 10111730737; size 2,319,678 bytes; SHA256 d1e90967af95bee5c06985cb81ce6c0db2f9c6ab60e4c7dfa685056683442b56

Afrikaans QA caveat:
- The localization uses automated/generative translation assistance, structural QA and manual contextual refinement.
- It has not been fully reviewed by a native Afrikaans speaker; do not present CI success as native-speaker perfection.

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 54 supported locales', '- catalog.json says 55 supported locales')
once('- README.md says 54 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk, Belarusian be_by and Faroese fo_fo', '- README.md says 55 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk, Belarusian be_by, Faroese fo_fo and Afrikaans af_za')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian, Belarusian and Faroese have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian, Belarusian, Faroese and Afrikaans have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 55.', 'NEXT LANGUAGE = language 56.')
once('Do not stop permanently at 55;', 'Do not stop permanently at 56;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 55 locales, Afrikaans #55, next #56')
