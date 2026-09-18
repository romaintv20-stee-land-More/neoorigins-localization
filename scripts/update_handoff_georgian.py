#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:140]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 48 locales:', '0.9.0 development currently has 49 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge.')
once('- 48: Armenian / hy_am\n', '- 48: Armenian / hy_am\n- 49: Georgian / ka_ge\n')
once('FORTY-EIGHT IS NOT THE FINAL TARGET.', 'FORTY-NINE IS NOT THE FINAL TARGET.')

for old, new in [
    ('41. NEXT ACTION', '42. NEXT ACTION'),
    ('40. QUALITY / QA CAVEAT', '41. QUALITY / QA CAVEAT'),
    ('39. SOURCE OF TRUTH HIERARCHY', '40. SOURCE OF TRUTH HIERARCHY'),
    ('38. CURRENT PERMANENT CI / BUILD VALIDATION', '39. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('37. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '38. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '38. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''37. GEORGIAN 0.9.0 STATUS
---------------------------
Georgian locale: ka_ge / ქართული.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Georgian is a current Minecraft Java locale (ka_ge).
- It is a distinct Kartvelian language using the Georgian script and is not a regional duplicate of any already-supported locale.
- It therefore satisfies the regional-dedup rule.

Georgian architecture:
- 16 common namespaces: neoorigins_ka_common_01 through neoorigins_ka_common_16
- 1.21.1-specific namespace: neoorigins_ka_121
- 26.1.x uses ka_ge inside neoorigins_26_1
- 26.2 uses ka_ge inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive ka_ge fallback files
- Gradle target switch: include_georgian_121_translations / includeGeorgian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Georgian strings. Therefore all 10 Georgian add-on fallback files are required.

Georgian coverage:
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

Georgian bootstrap:
- working branch: release/0.9.0-georgian
- workflow: .github/workflows/bootstrap-georgian.yml
- workflow run 34351329405: SUCCESS
- validated localization commit 6436469c72e41bca7e27409d1d7ecf8debd15b16 ("Add Georgian localization fallback")
- audit artifact ID 10103921327; size 291,548 bytes; SHA256 28e3bf2dbf0e4cecc41f7b83a272fd957d4337644035c174e62fb12127f62d06
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- title-like refinement generated 201 additional requests in 6 batches and improved 187 / 204 title-like English remnants
- final bootstrap cache contained 2,935 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile numbered-placeholder death messages were manually pre-seeded and placeholder sets were structurally audited
- bootstrap script sanity passed with 111,478 Georgian characters across 29 ka_ge files

Georgian contextual refinement:
- workflow: .github/workflows/refine-georgian.yml
- workflow run 34352011166: SUCCESS
- refinement commit a6925a7560371bd79624f0fcf89f88fe0928baa4 ("Refine Georgian Minecraft terminology")
- 392 values corrected across 19 files, including 240 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Power, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Charge, Pavlov, Scales, XP and Origin Architect HUD labels
- final script sanity: 111,267 Georgian characters across 29 ka_ge source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Georgian metadata:
- synchronization run 34352383462: SUCCESS
- metadata commit e4d2172de0cc15a404b932b59e9f99ec20c91657 ("Document Georgian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 49 supported locales and include ka_ge / ქართული

Final Georgian three-target CI:
- workflow: .github/workflows/build-0.9.0-georgian.yml
- workflow commit 50a53adbb42fe811c8743e61c5d0edd081cf48ad
- run ID 34352511589: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Georgian script/context sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Georgian script/context sanity, Gradle build, exact packaging verification and JAR upload

Georgian packaging verified by CI:
- 1.21.1: 27 ka_ge files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 ka_ge files = 16 common + correct 26.1 delta
- 26.2: 17 ka_ge files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_ka_121 leaked into 26.x

Final Georgian JAR artifacts from run 34352511589:
- mc-1.21.1: artifact ID 10104376509; size 3,723,631 bytes; SHA256 1f056d120e14dec8884a18d3fe58fa759cb21642fea2abaf98a99edf23d03dc0
- mc-26.1.x: artifact ID 10104341232; size 1,990,691 bytes; SHA256 22e991770249c432f7296bc61baa5278dc949d38c9d8452fdefd6559770e500f
- mc-26.2: artifact ID 10104354946; size 1,990,283 bytes; SHA256 8438c4417a6031c4574e4ccd65c1d066b0bcaedca0a73b28a90880c81a3127dc

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 48 supported locales', '- catalog.json says 49 supported locales')
once('- README.md says 48 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb and Armenian hy_am', '- README.md says 49 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am and Georgian ka_ge')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic and Armenian have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian and Georgian have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 49.', 'NEXT LANGUAGE = language 50.')
once('Do not stop permanently at 49;', 'Do not stop permanently at 50;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 49 locales, Georgian #49, next #50')
