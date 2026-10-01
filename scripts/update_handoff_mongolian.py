#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:160]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 50 locales:', '0.9.0 development currently has 51 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn.')
once('- 50: Kazakh / kk_kz\n', '- 50: Kazakh / kk_kz\n- 51: Mongolian / mn_mn\n')
once('FIFTY IS NOT THE FINAL TARGET.', 'FIFTY-ONE IS NOT THE FINAL TARGET.')

for old, new in [
    ('43. NEXT ACTION', '44. NEXT ACTION'),
    ('42. QUALITY / QA CAVEAT', '43. QUALITY / QA CAVEAT'),
    ('41. SOURCE OF TRUTH HIERARCHY', '42. SOURCE OF TRUTH HIERARCHY'),
    ('40. CURRENT PERMANENT CI / BUILD VALIDATION', '41. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('39. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '40. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '40. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''39. MONGOLIAN 0.9.0 STATUS
----------------------------
Mongolian locale: mn_mn / Монгол хэл.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Mongolian is a current Minecraft Java locale (mn_mn).
- It is a distinct language and is not a regional duplicate of any already-supported locale.
- It therefore satisfies the regional-dedup rule.

Mongolian architecture:
- 16 common namespaces: neoorigins_mn_common_01 through neoorigins_mn_common_16
- 1.21.1-specific namespace: neoorigins_mn_121
- 26.1.x uses mn_mn inside neoorigins_26_1
- 26.2 uses mn_mn inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive mn_mn fallback files
- Gradle target switch: include_mongolian_121_translations / includeMongolian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Mongolian strings. Therefore all 10 Mongolian add-on fallback files are required.

Mongolian coverage:
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

Mongolian bootstrap:
- working branch: release/0.9.0-mongolian
- workflow: .github/workflows/bootstrap-mongolian.yml
- initial workflow run 34356325263 failed during generation because the translation service transliterated a Latin placeholder sentinel; upstream discovery itself had passed and no localization commit was made from that failed run
- placeholder protection was hardened in commit 3e1d6fa46f0a98f7e330b6a43665c7a4f6b519e1 ("Harden Mongolian placeholder protection") using punctuation/digit-only sentinels that cannot be transliterated
- successful workflow run 34356704027: SUCCESS
- validated localization commit bc7d47ecc0ac542c4d901651766506ef788cb26d ("Add Mongolian localization fallback")
- successful audit artifact ID 10106126965; size 291,549 bytes; SHA256 172cc0e962ea2ddfc428638d2b26302d42a50c90c0b520cee9961617f1772a73
- initial translation set: 2,734 unique strings total; 16 manual/pre-seeded entries + 2,718 newly translated strings in 79 batches
- title-like refinement generated 123 additional requests in 4 batches and improved 115 / 126 title-like English remnants
- final bootstrap cache contained 2,857 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile printf and numbered-placeholder strings were pre-seeded/protected and all placeholder sets were structurally audited
- bootstrap sanity passed with 6,617 Mongolian-specific Ө/ө/Ү/ү letters across 29 mn_mn files

Mongolian contextual refinement:
- workflow: .github/workflows/refine-mongolian.yml
- workflow run 34357367860: SUCCESS
- refinement commit b70417e1237b2b9cb5ca5f73310094d066f52894 ("Refine Mongolian Minecraft terminology")
- 313 values corrected across 20 files, including 212 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Power, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Charge, Pavlov, Scales, health and Origin Architect HUD labels
- current Minecraft Mongolian terminology was used where available, including Харанхуйд харах for Night Vision, Недерит for Netherite, Тамын хаалга for Nether portal and Амины дээд хэмжээ for maximum health
- final sanity: 6,537 Mongolian-specific Ө/ө/Ү/ү letters across 29 mn_mn source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Mongolian metadata:
- synchronization run 34357606051: SUCCESS
- metadata commit 23ef46de6c42a3dcab8c0d61938bf5e4b736ac4d ("Document Mongolian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 51 supported locales and include mn_mn / Монгол хэл

Final Mongolian three-target CI:
- workflow: .github/workflows/build-0.9.0-mongolian.yml
- workflow commit bd5cba863b37ad8b0399f90d8be11c8f81305537
- run ID 34357718929: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Mongolian terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Mongolian terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload

Mongolian packaging verified by CI:
- 1.21.1: 27 mn_mn files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 mn_mn files = 16 common + correct 26.1 delta
- 26.2: 17 mn_mn files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_mn_121 leaked into 26.x

Final Mongolian JAR artifacts from run 34357718929:
- mc-1.21.1: artifact ID 10106502777; size 3,919,093 bytes; SHA256 7b6223ecd6b25aaad01d58784902fdc60280677017eddda22e1b7427d480b92c
- mc-26.1.x: artifact ID 10106505927; size 2,106,474 bytes; SHA256 af84e947e9a95d62aa730549c43eedb3e6c28e4b894de184ee87d232fd104c1a
- mc-26.2: artifact ID 10106516552; size 2,106,017 bytes; SHA256 10d737776c27dccb8effb2be9733d621bcc7c5e963dce76fed97042b6e2c8f15

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 50 supported locales', '- catalog.json says 51 supported locales')
once('- README.md says 50 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge and Kazakh kk_kz', '- README.md says 51 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz and Mongolian mn_mn')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian and Kazakh have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh and Mongolian have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 51.', 'NEXT LANGUAGE = language 52.')
once('Do not stop permanently at 51;', 'Do not stop permanently at 52;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 51 locales, Mongolian #51, next #52')
