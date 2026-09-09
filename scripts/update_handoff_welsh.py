#!/usr/bin/env python3
from pathlib import Path

p=Path(__file__).resolve().parents[1]/'PROJECT_HANDOFF.txt'
text=p.read_text(encoding='utf-8')

def once(old,new):
    global text
    if old not in text: raise RuntimeError(f'handoff anchor missing: {old[:100]}')
    text=text.replace(old,new,1)

once('0.9.0 development currently has 44 locales:', '0.9.0 development currently has 45 locales:')
once('fa_ir, is_is, ms_my, fil_ph.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb.')
once('- 44: Filipino / fil_ph\n', '- 44: Filipino / fil_ph\n- 45: Welsh / cy_gb\n')
once('FORTY-FOUR IS NOT THE FINAL TARGET.', 'FORTY-FIVE IS NOT THE FINAL TARGET.')

# Make room for the Welsh status section while preserving the sequential headings.
for old,new in [
('37. NEXT ACTION','38. NEXT ACTION'),
('36. QUALITY / QA CAVEAT','37. QUALITY / QA CAVEAT'),
('35. SOURCE OF TRUTH HIERARCHY','36. SOURCE OF TRUTH HIERARCHY'),
('34. CURRENT PERMANENT CI / BUILD VALIDATION','35. CURRENT PERMANENT CI / BUILD VALIDATION'),
('33. ORIGIN ARCHITECT AUDIT IMPROVEMENT','34. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old,new)

marker='34. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
welsh='''33. WELSH 0.9.0 STATUS
-------------------------
Welsh locale: cy_gb / Cymraeg.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Welsh is a current Minecraft Java locale (cy_gb).
- It is a distinct Celtic language and is not a regional duplicate of any already-supported locale.
- It therefore satisfies the regional-dedup rule.

Welsh architecture:
- 16 common namespaces: neoorigins_cy_common_01 through neoorigins_cy_common_16
- 1.21.1-specific namespace: neoorigins_cy_121
- 26.1.x uses cy_gb inside neoorigins_26_1
- 26.2 uses cy_gb inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive cy_gb fallback files
- Gradle target switch: include_welsh_121_translations / includeWelsh121Translations

At the audited references, NeoOrigins had zero official Welsh strings. The strict 1.21.1 audits also confirmed complete fallback coverage for all 10 supported add-ons after upstream-priority pruning.

Welsh coverage:
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

Welsh bootstrap:
- working branch: release/0.9.0-welsh
- workflow: .github/workflows/bootstrap-welsh.yml
- workflow run 34339469577: SUCCESS
- validated localization commit 6125298cebcd2a256258b30c51c5b2f84617e048 ("Add Welsh localization fallback")
- audit artifact ID 10099206463; size 291,554 bytes; SHA256 b1f2c9122e2736fc2d1455dff0cb4c5650374bdfe102ac82068f2b312c71ba6c
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile numbered-placeholder death messages were manually pre-seeded and then structurally audited

Welsh contextual refinement:
- workflow: .github/workflows/refine-welsh.yml
- workflow run 34340005574: SUCCESS
- refinement commit 0a7ede387de9bcf7b3fa6210447d82fab59ce1d1 ("Refine Welsh Minecraft terminology")
- 281 values corrected across 19 files, including 244 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Apply, Ultimine, Charge, Scales, Pavlov, Nether/Netherite, Drops, Night Vision and Origin Architect HUD labels
- final lexical sanity: 5,410 Welsh markers across 29 cy_gb source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets

Welsh metadata:
- synchronization run 34340256125: SUCCESS
- metadata commit dee865a575471716b1e963a4746f3606c583f2a7 ("Document Welsh localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 45 supported locales and include cy_gb / Cymraeg

Final Welsh three-target CI:
- workflow: .github/workflows/build-0.9.0-welsh.yml
- workflow commit e5351b99b396c98038ee69a9889a5a734f059ab4
- run ID 34340363045: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Welsh lexical sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Welsh lexical sanity, Gradle build, exact packaging verification and JAR upload

Welsh packaging verified by CI:
- 1.21.1: 27 cy_gb files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 cy_gb files = 16 common + correct 26.1 delta
- 26.2: 17 cy_gb files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_cy_121 leaked into 26.x

Final Welsh JAR artifacts from run 34340363045:
- mc-1.21.1: artifact ID 10099515489; size 3,351,471 bytes; SHA256 a9df005a88f8732090522f9fe002630f051b75e3e277dbaef29508c71e20e14d
- mc-26.1.x: artifact ID 10099508793; size 1,772,992 bytes; SHA256 431f83b3cf56460580c03867f232caf9c5289cd7aed4aa04095c51932afe02dd
- mc-26.2: artifact ID 10099507515; size 1,772,484 bytes; SHA256 a9caa5ffe2692d87318ac4d4d94495a7b3581e33b1dc3914b67654871a8b0960

'''
if marker not in text: raise RuntimeError('Origin Architect section marker missing after renumbering')
text=text.replace(marker,welsh+marker,1)

once('- catalog.json says 44 supported locales', '- catalog.json says 45 supported locales')
once('- README.md says 44 languages and includes Malay ms_my plus Filipino fil_ph', '- README.md says 45 languages and includes Malay ms_my, Filipino fil_ph and Welsh cy_gb')
old='Persian, Icelandic, Malay and Filipino have passed final three-target packaging validation'
new='Persian, Icelandic, Malay, Filipino and Welsh have passed final three-target packaging validation'
once(old,new)
once('NEXT LANGUAGE = language 45.', 'NEXT LANGUAGE = language 46.')
once('Do not stop permanently at 45;', 'Do not stop permanently at 46;')

p.write_text(text,encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 45 locales, Welsh #45, next #46')
