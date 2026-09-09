#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:120]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 47 locales:', '0.9.0 development currently has 48 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am.')
once('- 47: Scottish Gaelic / gd_gb\n', '- 47: Scottish Gaelic / gd_gb\n- 48: Armenian / hy_am\n')
once('FORTY-SEVEN IS NOT THE FINAL TARGET.', 'FORTY-EIGHT IS NOT THE FINAL TARGET.')

for old, new in [
    ('40. NEXT ACTION', '41. NEXT ACTION'),
    ('39. QUALITY / QA CAVEAT', '40. QUALITY / QA CAVEAT'),
    ('38. SOURCE OF TRUTH HIERARCHY', '39. SOURCE OF TRUTH HIERARCHY'),
    ('37. CURRENT PERMANENT CI / BUILD VALIDATION', '38. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('36. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '37. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '37. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''36. ARMENIAN 0.9.0 STATUS
---------------------------
Armenian locale: hy_am / Հայերեն.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Armenian is a current Minecraft Java locale (hy_am).
- It is a distinct language using the Armenian script and is not a regional duplicate of any already-supported locale.
- It therefore satisfies the regional-dedup rule.

Armenian architecture:
- 16 common namespaces: neoorigins_hy_common_01 through neoorigins_hy_common_16
- 1.21.1-specific namespace: neoorigins_hy_121
- 26.1.x uses hy_am inside neoorigins_26_1
- 26.2 uses hy_am inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive hy_am fallback files
- Gradle target switch: include_armenian_121_translations / includeArmenian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Armenian strings. Therefore all 10 Armenian add-on fallback files are required.

Armenian coverage:
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

Armenian bootstrap:
- working branch: release/0.9.0-armenian
- workflow: .github/workflows/bootstrap-armenian.yml
- workflow run 34346145423: SUCCESS
- validated localization commit 1b542a1dcfdf64aba1036785e316b2d3e0eeca27 ("Add Armenian localization fallback")
- audit artifact ID 10101840351; size 291,561 bytes; SHA256 0a718c7c0f1c396bf46323af747fb23756e911ebf7421c0ed2fb0e1dbc259707
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- title-like refinement generated 252 additional requests in 8 batches and improved 232 / 255 title-like English remnants
- final bootstrap cache contained 2,986 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile numbered-placeholder death messages were manually pre-seeded and placeholder sets were structurally audited
- bootstrap script sanity passed with 112,171 Armenian characters across 29 hy_am files

Armenian contextual refinement:
- workflow: .github/workflows/refine-armenian.yml
- workflow run 34346874201: SUCCESS
- refinement commit e9700c214e2d8eabf89a3bac4db2f4bd519e77b8 ("Refine Armenian Minecraft terminology")
- 327 values corrected across 19 files, including 241 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Power toggles, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Charge, Pavlov, Scales, XP and Origin Architect HUD labels
- final script sanity: 111,923 Armenian characters across 29 hy_am source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Armenian metadata:
- synchronization run 34347045992: SUCCESS
- metadata commit 2e5390a5635291f5c38b4a581b97f58d5451d7d1 ("Document Armenian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 48 supported locales and include hy_am / Հայերեն

Final Armenian three-target CI:
- workflow: .github/workflows/build-0.9.0-armenian.yml
- workflow commit f4c4832a8937aa8f255dd8750a409bfc55b5d2a2
- run ID 34347261076: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Armenian script sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Armenian script sanity, Gradle build, exact packaging verification and JAR upload

Armenian packaging verified by CI:
- 1.21.1: 27 hy_am files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 hy_am files = 16 common + correct 26.1 delta
- 26.2: 17 hy_am files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_hy_121 leaked into 26.x

Final Armenian JAR artifacts from run 34347261076:
- mc-1.21.1: artifact ID 10102268738; size 3,622,618 bytes; SHA256 f0883beea30c0208e188d572e943453ac4bd158b48763d6bbd14aa2d121d585b
- mc-26.1.x: artifact ID 10102254834; size 1,932,165 bytes; SHA256 f1e6420eb121f723794b111a86168212c4033f114a30698007955da8c1d5664d
- mc-26.2: artifact ID 10102246481; size 1,931,776 bytes; SHA256 b66ea19027d5acd0dcae7fa24118ac69f67484d3579c6c7bdaaec869ccb8e0d2

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 47 supported locales', '- catalog.json says 48 supported locales')
once('- README.md says 47 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie and Scottish Gaelic gd_gb', '- README.md says 48 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb and Armenian hy_am')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish and Scottish Gaelic have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic and Armenian have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 48.', 'NEXT LANGUAGE = language 49.')
once('Do not stop permanently at 48;', 'Do not stop permanently at 49;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 48 locales, Armenian #48, next #49')
