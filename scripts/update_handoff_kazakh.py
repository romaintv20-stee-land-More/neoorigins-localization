#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:140]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 49 locales:', '0.9.0 development currently has 50 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz.')
once('- 49: Georgian / ka_ge\n', '- 49: Georgian / ka_ge\n- 50: Kazakh / kk_kz\n')
once('FORTY-NINE IS NOT THE FINAL TARGET.', 'FIFTY IS NOT THE FINAL TARGET.')

for old, new in [
    ('42. NEXT ACTION', '43. NEXT ACTION'),
    ('41. QUALITY / QA CAVEAT', '42. QUALITY / QA CAVEAT'),
    ('40. SOURCE OF TRUTH HIERARCHY', '41. SOURCE OF TRUTH HIERARCHY'),
    ('39. CURRENT PERMANENT CI / BUILD VALIDATION', '40. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('38. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '39. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '39. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''38. KAZAKH 0.9.0 STATUS
-------------------------
Kazakh locale: kk_kz / Қазақша.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Kazakh is a current Minecraft Java locale (kk_kz).
- It is a distinct Turkic language with its own written standard and Kazakh-specific Cyrillic letters, not a regional duplicate of any already-supported locale.
- It therefore satisfies the regional-dedup rule.

Kazakh architecture:
- 16 common namespaces: neoorigins_kk_common_01 through neoorigins_kk_common_16
- 1.21.1-specific namespace: neoorigins_kk_121
- 26.1.x uses kk_kz inside neoorigins_26_1
- 26.2 uses kk_kz inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive kk_kz fallback files
- Gradle target switch: include_kazakh_121_translations / includeKazakh121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Kazakh strings. Therefore all 10 Kazakh add-on fallback files are required.

Kazakh coverage:
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

Kazakh bootstrap:
- working branch: release/0.9.0-kazakh
- workflow: .github/workflows/bootstrap-kazakh.yml
- workflow run 34353924273: SUCCESS
- validated localization commit c75a522f20eb06fbc07bb586aebdd1bfb9ab2368 ("Add Kazakh localization fallback")
- audit artifact ID 10105005146; size 291,561 bytes; SHA256 20e955ae39d0ea7e84d6df73c9645d587f0c0ce5b6cdd524bd050d369766fae4
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- title-like refinement generated 155 additional requests in 5 batches and improved 152 / 160 title-like English remnants
- final bootstrap cache contained 2,889 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile numbered-placeholder death messages were manually pre-seeded and placeholder sets were structurally audited
- bootstrap sanity passed with 17,526 Kazakh-specific letters across 29 kk_kz files

Kazakh contextual refinement:
- workflow: .github/workflows/refine-kazakh.yml
- workflow run 34354666913: SUCCESS
- refinement commit df8e412f7c34551174bbd317c3f5b0d085e40e78 ("Refine Kazakh Minecraft terminology")
- 313 values corrected across 19 files, including 217 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Power, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Charge, Pavlov, Scales, health, XP and Origin Architect HUD labels
- Minecraft Kazakh terminology was used where available, including Незер, Незерит, Түнде көру, саулық and тәжірибе
- final sanity: 17,426 Kazakh-specific letters across 29 kk_kz source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Kazakh metadata:
- synchronization run 34354911824: SUCCESS
- metadata commit 90c68a6cde68f043c799330e5c65f1b6317bc323 ("Document Kazakh localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 50 supported locales and include kk_kz / Қазақша

Final Kazakh three-target CI:
- workflow: .github/workflows/build-0.9.0-kazakh.yml
- workflow commit 37339662b4dd1efd5a6ca70a8936ac45351c1ec1
- run ID 34355144940: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Kazakh terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Kazakh terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload

Kazakh packaging verified by CI:
- 1.21.1: 27 kk_kz files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 kk_kz files = 16 common + correct 26.1 delta
- 26.2: 17 kk_kz files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_kk_121 leaked into 26.x

Final Kazakh JAR artifacts from run 34355144940:
- mc-1.21.1: artifact ID 10105445166; size 3,822,143 bytes; SHA256 29f24442db5bdd077a3ee8e7df3bbdaacc8696826beffaba5e2ef91991fbb06c
- mc-26.1.x: artifact ID 10105431487; size 2,049,142 bytes; SHA256 c7d4721860df13f88800b5048b0a80337b25cf503ec093f387f97f1d62dbafc5
- mc-26.2: artifact ID 10105426939; size 2,048,727 bytes; SHA256 b530c8116d6940459442449ad0c16c4168a62c052ab04df555b3809db7a57850

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 49 supported locales', '- catalog.json says 50 supported locales')
once('- README.md says 49 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am and Georgian ka_ge', '- README.md says 50 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge and Kazakh kk_kz')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian and Georgian have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian and Kazakh have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 50.', 'NEXT LANGUAGE = language 51.')
once('Do not stop permanently at 50;', 'Do not stop permanently at 51;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 50 locales, Kazakh #50, next #51')
