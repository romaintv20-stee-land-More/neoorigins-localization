#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:180]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 55 locales:', '0.9.0 development currently has 56 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by, fo_fo, af_za.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by, fo_fo, af_za, az_az.')
once('- 55: Afrikaans / af_za\n', '- 55: Afrikaans / af_za\n- 56: Azerbaijani / az_az\n')
once('FIFTY-FIVE IS NOT THE FINAL TARGET.', 'FIFTY-SIX IS NOT THE FINAL TARGET.')

for old, new in [
    ('48. NEXT ACTION', '49. NEXT ACTION'),
    ('47. QUALITY / QA CAVEAT', '48. QUALITY / QA CAVEAT'),
    ('46. SOURCE OF TRUTH HIERARCHY', '47. SOURCE OF TRUTH HIERARCHY'),
    ('45. CURRENT PERMANENT CI / BUILD VALIDATION', '46. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('44. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '45. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '45. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''44. AZERBAIJANI 0.9.0 STATUS
--------------------------------
Azerbaijani locale: az_az / Azərbaycanca.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Azerbaijani is a current Minecraft Java locale (az_az).
- It is a distinct Turkic language with its own grammar, vocabulary and orthography, not a regional duplicate of Turkish tr_tr.
- It therefore satisfies the regional-dedup rule.

Azerbaijani architecture:
- 16 common namespaces: neoorigins_az_common_01 through neoorigins_az_common_16
- 1.21.1-specific namespace: neoorigins_az_121
- 26.1.x uses az_az inside neoorigins_26_1
- 26.2 uses az_az inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive az_az fallback files
- Gradle target switch: include_azerbaijani_121_translations / includeAzerbaijani121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Azerbaijani strings. Therefore all 10 Azerbaijani add-on fallback files are required.

Azerbaijani coverage:
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

Azerbaijani bootstrap:
- working branch: release/0.9.0-azerbaijani
- workflow: .github/workflows/bootstrap-azerbaijani.yml
- workflow run 34373070773: SUCCESS
- validated localization commit 55db466ae764a0b6c08799c739aa99d5ae2d5784 ("Add Azerbaijani localization fallback")
- audit artifact ID 10112824455; size 291,557 bytes; SHA256 0bc16ce4c1dd676113fa260b6246b417f6e35b5051c347da6b95948c8eaa011e
- translation generation produced 2,734 unique strings total: 18 manual/pre-seeded entries plus 2,716 newly translated strings in 79 batches
- title-like refinement generated 243 additional requests in 7 batches and improved 209 / 246 title-like English remnants
- final bootstrap cache contained 2,977 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile printf and numbered-placeholder strings were pre-seeded/protected; punctuation/digit-only sentinels use whitespace-tolerant restoration and numbered placeholders are compared as sorted sets
- bootstrap sanity passed with 1,495 Azerbaijani lexical markers and 30,357 Azerbaijani-specific letters across 29 az_az files

Azerbaijani contextual refinement:
- workflow: .github/workflows/refine-azerbaijani.yml
- refinement run 34373973302 stopped only on an intentionally strict linguistic false-friend guard after all structural NeoOrigins/add-on audits had already passed; this was not a coverage, placeholder or JSON failure
- the remaining inflected Nether -> Holland/Hollandiya false-friend forms were normalized without weakening the guard
- final workflow run 34374190590: SUCCESS
- refinement commit 1b0186bd52cd48055f6236e07ac1eac1462848ce ("Refine Azerbaijani Minecraft terminology")
- 373 values corrected across 19 files
- corrected contextual false friends and Minecraft/Origins terminology including Power/ability wording, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Pavlov, Scales, health/experience wording and Origin Architect HUD labels
- all 64 generated hotkey labels were normalized to Qısayol NN
- final sanity: 1,494 Azerbaijani lexical markers and 30,257 Azerbaijani-specific letters across 29 az_az source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Azerbaijani metadata:
- synchronization run 34374657024: SUCCESS
- metadata commit 2b6db0a8aa9d497ee2c695bde0d3ccc74c9ee080 ("Document Azerbaijani localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 56 supported locales and include az_az / Azərbaycanca

Final Azerbaijani three-target CI:
- workflow: .github/workflows/build-0.9.0-azerbaijani.yml
- workflow commit 760938c78a59ce9eae4c95cb0b8d63111c1c1354
- run ID 34374820982: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Azerbaijani terminology/lexical sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Azerbaijani terminology/lexical sanity, Gradle build, exact packaging verification and JAR upload

Azerbaijani packaging verified by CI:
- 1.21.1: 27 az_az files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 az_az files = 16 common + correct 26.1 delta
- 26.2: 17 az_az files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_az_121 leaked into 26.x

Final Azerbaijani JAR artifacts from run 34374820982:
- mc-1.21.1: artifact ID 10113468182; size 4,369,727 bytes; SHA256 eb61975ccbdec21c957c52c91e7bdb25f2fc877ed868eadf5fb7e124bd60ddab
- mc-26.1.x: artifact ID 10113449784; size 2,371,164 bytes; SHA256 883f540855115c248d6b087cd69847d67ba231c5a11aa7504223e7eb47a1099a
- mc-26.2: artifact ID 10113440446; size 2,370,727 bytes; SHA256 176439e3d32ebef039d5833783e63ce2b35189d3b30feb637cefc510c0f93a70

Azerbaijani QA caveat:
- The localization uses automated/generative translation assistance, structural QA and manual contextual refinement.
- It has not been fully reviewed by a native Azerbaijani speaker; do not present CI success as native-speaker perfection.

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 55 supported locales', '- catalog.json says 56 supported locales')
once('- README.md says 55 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk, Belarusian be_by, Faroese fo_fo and Afrikaans af_za', '- README.md says 56 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk, Belarusian be_by, Faroese fo_fo, Afrikaans af_za and Azerbaijani az_az')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian, Belarusian, Faroese and Afrikaans have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian, Belarusian, Faroese, Afrikaans and Azerbaijani have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 56.', 'NEXT LANGUAGE = language 57.')
once('Do not stop permanently at 56;', 'Do not stop permanently at 57;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 56 locales, Azerbaijani #56, next #57')
