#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:180]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 53 locales:', '0.9.0 development currently has 54 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by, fo_fo.')
once('- 53: Belarusian / be_by\n', '- 53: Belarusian / be_by\n- 54: Faroese / fo_fo\n')
once('FIFTY-THREE IS NOT THE FINAL TARGET.', 'FIFTY-FOUR IS NOT THE FINAL TARGET.')

for old, new in [
    ('46. NEXT ACTION', '47. NEXT ACTION'),
    ('45. QUALITY / QA CAVEAT', '46. QUALITY / QA CAVEAT'),
    ('44. SOURCE OF TRUTH HIERARCHY', '45. SOURCE OF TRUTH HIERARCHY'),
    ('43. CURRENT PERMANENT CI / BUILD VALIDATION', '44. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('42. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '43. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '43. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''42. FAROESE 0.9.0 STATUS
---------------------------
Faroese locale: fo_fo / Føroyskt.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Faroese is a current Minecraft Java locale (fo_fo).
- It is a distinct North Germanic language and is not a regional duplicate of Danish, Icelandic, Norwegian Bokmal, Norwegian Nynorsk or any other already-supported locale.
- It therefore satisfies the regional-dedup rule.

Faroese architecture:
- 16 common namespaces: neoorigins_fo_common_01 through neoorigins_fo_common_16
- 1.21.1-specific namespace: neoorigins_fo_121
- 26.1.x uses fo_fo inside neoorigins_26_1
- 26.2 uses fo_fo inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive fo_fo fallback files
- Gradle target switch: include_faroese_121_translations / includeFaroese121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Faroese strings. Therefore all 10 Faroese add-on fallback files are required.

Faroese coverage:
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

Faroese bootstrap:
- working branch: release/0.9.0-faroese
- workflow: .github/workflows/bootstrap-faroese.yml
- workflow run 34365948928: SUCCESS
- validated localization commit 3a3a397d4df719a5da1b8f5e9aaa4c1e03a1ca08 ("Add Faroese localization fallback")
- audit artifact ID 10109957860; size 291,538 bytes; SHA256 c6c479cf80137c6485dbce564f88321bd454ad0ea7e85558a69811cb1a71140c
- translation generation produced 2,734 unique strings total: 18 manual/pre-seeded entries plus 2,716 newly translated strings in 79 batches
- title-like refinement generated 34 additional requests in 1 batch and improved 16 / 37 title-like English remnants
- final bootstrap cache contained 2,768 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile printf and numbered-placeholder strings were pre-seeded/protected; punctuation/digit-only sentinels use whitespace-tolerant restoration and numbered placeholders are compared as sorted sets
- bootstrap sanity passed with 3,683 Faroese-specific Ð/ð/Ø/ø letters across 29 fo_fo files

Faroese contextual refinement:
- workflow: .github/workflows/refine-faroese.yml
- workflow run 34366799610: SUCCESS
- refinement commit 7b2d7198fd294fa262fd60cc44534f7359d01ddf ("Refine Faroese Minecraft terminology")
- 364 values corrected across 19 files
- corrected contextual false friends and Minecraft/Origins terminology including Power/ability wording, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Charge, Pavlov, Scales, experience and Origin Architect HUD labels
- all 64 generated hotkey labels were normalized to Snarlykil NN
- current Minecraft Faroese terminology was used where available, including Náttarsjón for Night Vision, Nether terminology and Netheritt for Netherite
- final sanity: 3,680 Faroese-specific Ð/ð/Ø/ø letters across 29 fo_fo source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Faroese metadata:
- synchronization run 34367019804: SUCCESS
- metadata commit 82f9c435ea0a8f56581659fe3a3c2e4aadf826eb ("Document Faroese localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 54 supported locales and include fo_fo / Føroyskt

Final Faroese three-target CI:
- workflow: .github/workflows/build-0.9.0-faroese.yml
- workflow commit c5d682f8d93689f3d5c17337dfd4146a20975e70
- run ID 34367146697: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Faroese terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Faroese terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload

Faroese packaging verified by CI:
- 1.21.1: 27 fo_fo files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 fo_fo files = 16 common + correct 26.1 delta
- 26.2: 17 fo_fo files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_fo_121 leaked into 26.x

Final Faroese JAR artifacts from run 34367146697:
- mc-1.21.1: artifact ID 10110417327; size 4,203,616 bytes; SHA256 c6083a55ac870f7380cee3fa8edf076e49c51123d46beb8fb449aee446d0a29f
- mc-26.1.x: artifact ID 10110379318; size 2,273,696 bytes; SHA256 447410434af0375a3f1b7a8c1707813cc5beedb23f30d716548da4fc5a56011e
- mc-26.2: artifact ID 10110383382; size 2,273,281 bytes; SHA256 93a6a35302abc3ed0ab0d01bd5ccbdd2a3a0751ae55cca50a6806d00da0be921

Faroese QA caveat:
- The localization uses automated/generative translation assistance, structural QA and manual contextual refinement.
- It has not been fully reviewed by a native Faroese speaker; do not present CI success as native-speaker perfection.

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 53 supported locales', '- catalog.json says 54 supported locales')
once('- README.md says 53 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk and Belarusian be_by', '- README.md says 54 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk, Belarusian be_by and Faroese fo_fo')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian and Belarusian have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian, Belarusian and Faroese have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 54.', 'NEXT LANGUAGE = language 55.')
once('Do not stop permanently at 54;', 'Do not stop permanently at 55;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 54 locales, Faroese #54, next #55')
