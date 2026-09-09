#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:180]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 52 locales:', '0.9.0 development currently has 53 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by.')
once('- 52: Macedonian / mk_mk\n', '- 52: Macedonian / mk_mk\n- 53: Belarusian / be_by\n')
once('FIFTY-TWO IS NOT THE FINAL TARGET.', 'FIFTY-THREE IS NOT THE FINAL TARGET.')

for old, new in [
    ('45. NEXT ACTION', '46. NEXT ACTION'),
    ('44. QUALITY / QA CAVEAT', '45. QUALITY / QA CAVEAT'),
    ('43. SOURCE OF TRUTH HIERARCHY', '44. SOURCE OF TRUTH HIERARCHY'),
    ('42. CURRENT PERMANENT CI / BUILD VALIDATION', '43. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('41. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '42. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '42. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''41. BELARUSIAN 0.9.0 STATUS
------------------------------
Belarusian locale: be_by / Беларуская.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Belarusian is a current Minecraft Java locale (be_by).
- It is a distinct East Slavic language and is not a regional duplicate of Russian, Ukrainian or any other already-supported locale.
- It therefore satisfies the regional-dedup rule.

Belarusian architecture:
- 16 common namespaces: neoorigins_be_common_01 through neoorigins_be_common_16
- 1.21.1-specific namespace: neoorigins_be_121
- 26.1.x uses be_by inside neoorigins_26_1
- 26.2 uses be_by inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive be_by fallback files
- Gradle target switch: include_belarusian_121_translations / includeBelarusian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Belarusian strings. Therefore all 10 Belarusian add-on fallback files are required.

Belarusian coverage:
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

Belarusian bootstrap:
- working branch: release/0.9.0-belarusian
- workflow: .github/workflows/bootstrap-belarusian.yml
- workflow run 34363769995: SUCCESS
- validated localization commit 877212f939fd57de79bac0725281062c99874efa ("Add Belarusian localization fallback")
- audit artifact ID 10109063091; size 291,551 bytes; SHA256 cb241bfc00b00dd5e1a6f98063192e0dc14530adea4b6e206a57b668e2608496
- translation generation produced 2,734 unique strings total: 18 manual/pre-seeded entries plus 2,716 newly translated strings in 79 batches
- title-like refinement generated 97 additional requests in 3 batches and improved 93 / 100 title-like English remnants
- final bootstrap cache contained 2,831 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile printf and numbered-placeholder strings were pre-seeded/protected; punctuation/digit-only sentinels use whitespace-tolerant restoration and all placeholder sets were structurally audited
- bootstrap sanity passed with 6,673 Belarusian-specific Ў/ў/І/і letters across 29 be_by files

Belarusian contextual refinement:
- workflow: .github/workflows/refine-belarusian.yml
- workflow run 34364460234: SUCCESS
- refinement commit 06b275d844b40f3e31a84670afa3a7dd4d11ef36 ("Refine Belarusian Minecraft terminology")
- 339 values corrected across 19 files, including 245 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Power/ability wording, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Pavlov, Scales, health, experience and Origin Architect HUD labels
- current Minecraft Belarusian terminology was used where available, including Начны зрок for Night Vision, Нэдар for the Nether, нэдарыт for Netherite, Здабыча for drops and з'яўленне for spawning
- final sanity: 6,669 Belarusian-specific Ў/ў/І/і letters across 29 be_by source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Belarusian metadata:
- synchronization run 34364755913: SUCCESS
- metadata commit 54c305f079fa1daffa87e960484c499d2dc35c20 ("Document Belarusian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 53 supported locales and include be_by / Беларуская

Final Belarusian three-target CI:
- workflow: .github/workflows/build-0.9.0-belarusian.yml
- workflow commit cae70b848e26d44f0e6265b63e03c84e03027d97
- run ID 34364892271: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Belarusian terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Belarusian terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload

Belarusian packaging verified by CI:
- 1.21.1: 27 be_by files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 be_by files = 16 common + correct 26.1 delta
- 26.2: 17 be_by files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_be_121 leaked into 26.x

Final Belarusian JAR artifacts from run 34364892271:
- mc-1.21.1: artifact ID 10109490233; size 4,119,783 bytes; SHA256 7f8716762429e4c4da0845312341ef589bcd42e5b1d081625c9d044bf77a0127
- mc-26.1.x: artifact ID 10109467263; size 2,224,781 bytes; SHA256 e3f6483b9e1cfd7cbcc1c1faac75b6c8a488001aa9f97ad88ae1dd08decab7ee
- mc-26.2: artifact ID 10109453937; size 2,224,371 bytes; SHA256 f6f7e4c811e83871ff82468eb087c0522ebb5fdf3c7ba11d7a72f7524538c778

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 52 supported locales', '- catalog.json says 53 supported locales')
once('- README.md says 52 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn and Macedonian mk_mk', '- README.md says 53 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk and Belarusian be_by')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian and Macedonian have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian, Macedonian and Belarusian have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 53.', 'NEXT LANGUAGE = language 54.')
once('Do not stop permanently at 53;', 'Do not stop permanently at 54;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 53 locales, Belarusian #53, next #54')
