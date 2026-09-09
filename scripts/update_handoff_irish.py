#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:120]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 45 locales:', '0.9.0 development currently has 46 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie.')
once('- 45: Welsh / cy_gb\n', '- 45: Welsh / cy_gb\n- 46: Irish / ga_ie\n')
once('FORTY-FIVE IS NOT THE FINAL TARGET.', 'FORTY-SIX IS NOT THE FINAL TARGET.')

# Make room for Irish while preserving sequential status/governance headings.
for old, new in [
    ('38. NEXT ACTION', '39. NEXT ACTION'),
    ('37. QUALITY / QA CAVEAT', '38. QUALITY / QA CAVEAT'),
    ('36. SOURCE OF TRUTH HIERARCHY', '37. SOURCE OF TRUTH HIERARCHY'),
    ('35. CURRENT PERMANENT CI / BUILD VALIDATION', '36. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('34. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '35. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '35. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
irish = '''34. IRISH 0.9.0 STATUS
-------------------------
Irish locale: ga_ie / Gaeilge.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Irish is a current Minecraft Java locale (ga_ie).
- It is a distinct Celtic language and is not a regional duplicate of Welsh or any other already-supported locale.
- It therefore satisfies the regional-dedup rule.

Irish architecture:
- 16 common namespaces: neoorigins_ga_common_01 through neoorigins_ga_common_16
- 1.21.1-specific namespace: neoorigins_ga_121
- 26.1.x uses ga_ie inside neoorigins_26_1
- 26.2 uses ga_ie inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive ga_ie fallback files
- Gradle target switch: include_irish_121_translations / includeIrish121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Irish strings. Therefore all 10 Irish add-on fallback files are required.

Irish coverage:
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

Irish bootstrap:
- working branch: release/0.9.0-irish
- workflow: .github/workflows/bootstrap-irish.yml
- workflow run 34341089048: SUCCESS
- validated localization commit 437d9f52132f583340ce406d2c1de415147438ce ("Add Irish localization fallback")
- audit artifact ID 10099842010; size 291,544 bytes; SHA256 ac212ea128114e6821aed7937940d00b7d287ef6924cd62b11e38a953468c803
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- title-like refinement generated 172 additional translations in 5 batches and improved 90 / 175 title-like English remnants
- final bootstrap cache contained 2,906 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile numbered-placeholder death messages were manually pre-seeded and placeholder sets were structurally audited

Irish contextual refinement:
- workflow: .github/workflows/refine-irish.yml
- workflow run 34341643267: SUCCESS
- refinement commit 7230b32a9b35f4121ed8c0c8e19ff1dd56d6e540 ("Refine Irish Minecraft terminology")
- 323 values corrected across 21 files, including 253 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Apply, Ultimine, NeoOrigins/Origin labels, Blazeling, Nether/Netherite, Drops, Spawn Rules, Night Vision, Charge, Pavlov and Origin Architect HUD labels
- final lexical sanity: 3,995 Irish markers across 29 ga_ie source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- post-refinement JSON validation passed

Irish metadata:
- synchronization run 34341793921: SUCCESS
- metadata commit 1e76cdb9bb173905a3450658555f2af38a6e7583 ("Document Irish localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 46 supported locales and include ga_ie / Gaeilge

Final Irish three-target CI:
- workflow: .github/workflows/build-0.9.0-irish.yml
- workflow commit b48f79e39a03c4a84a3acb2a3adfefdb19034056
- run ID 34341885267: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Irish lexical sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Irish lexical sanity, Gradle build, exact packaging verification and JAR upload

Irish packaging verified by CI:
- 1.21.1: 27 ga_ie files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 ga_ie files = 16 common + correct 26.1 delta
- 26.2: 17 ga_ie files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_ga_121 leaked into 26.x

Final Irish JAR artifacts from run 34341885267:
- mc-1.21.1: artifact ID 10100114965; size 3,437,339 bytes; SHA256 5de2785f14d56a736b9908c4187a9c1178db6e0013fef5bc9e3d6033e62296db
- mc-26.1.x: artifact ID 10100117423; size 1,823,138 bytes; SHA256 036a10ddbe3f66602d3d36bcfe4af154c723d81b4857331e87c57279b5c993eb
- mc-26.2: artifact ID 10100112461; size 1,822,706 bytes; SHA256 8abd77695138f63d3d77bf4d9a67775606a10fabc4cab3bc0f6fc4cb4ec9731b

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, irish + marker, 1)

once('- catalog.json says 45 supported locales', '- catalog.json says 46 supported locales')
once('- README.md says 45 languages and includes Malay ms_my, Filipino fil_ph and Welsh cy_gb', '- README.md says 46 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb and Irish ga_ie')
old = 'Persian, Icelandic, Malay, Filipino and Welsh have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh and Irish have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 46.', 'NEXT LANGUAGE = language 47.')
once('Do not stop permanently at 46;', 'Do not stop permanently at 47;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 46 locales, Irish #46, next #47')
