#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

def once(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'handoff anchor missing: {old[:180]}')
    text = text.replace(old, new, 1)

once('0.9.0 development currently has 51 locales:', '0.9.0 development currently has 52 locales:')
once('fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn.', 'fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk.')
once('- 51: Mongolian / mn_mn\n', '- 51: Mongolian / mn_mn\n- 52: Macedonian / mk_mk\n')
once('FIFTY-ONE IS NOT THE FINAL TARGET.', 'FIFTY-TWO IS NOT THE FINAL TARGET.')

for old, new in [
    ('44. NEXT ACTION', '45. NEXT ACTION'),
    ('43. QUALITY / QA CAVEAT', '44. QUALITY / QA CAVEAT'),
    ('42. SOURCE OF TRUTH HIERARCHY', '43. SOURCE OF TRUTH HIERARCHY'),
    ('41. CURRENT PERMANENT CI / BUILD VALIDATION', '42. CURRENT PERMANENT CI / BUILD VALIDATION'),
    ('40. ORIGIN ARCHITECT AUDIT IMPROVEMENT', '41. ORIGIN ARCHITECT AUDIT IMPROVEMENT'),
]:
    once(old, new)

marker = '41. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n'
section = '''40. MACEDONIAN 0.9.0 STATUS
------------------------------
Macedonian locale: mk_mk / Македонски.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Macedonian is a current Minecraft Java locale (mk_mk).
- It is a distinct South Slavic language with its own standard and is not a regional duplicate of Bulgarian, Serbian or any other already-supported locale.
- It therefore satisfies the regional-dedup rule.

Macedonian architecture:
- 16 common namespaces: neoorigins_mk_common_01 through neoorigins_mk_common_16
- 1.21.1-specific namespace: neoorigins_mk_121
- 26.1.x uses mk_mk inside neoorigins_26_1
- 26.2 uses mk_mk inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive mk_mk fallback files
- Gradle target switch: include_macedonian_121_translations / includeMacedonian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Macedonian strings. Therefore all 10 Macedonian add-on fallback files are required.

Macedonian coverage:
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

Macedonian bootstrap:
- working branch: release/0.9.0-macedonian
- workflow: .github/workflows/bootstrap-macedonian.yml
- initial workflow run 34360190816 failed during generation because the translation service inserted whitespace inside a protected placeholder sentinel; upstream discovery had already passed and no localization commit was made from that failed run
- failed-run audit artifact ID 10107541367; size 204,012 bytes; SHA256 f7b7444c373791d89dc2ea0d1212d6f65cb494428bcc058df392da1c45e102e2
- placeholder restoration was hardened in commit c3393aacdd4c797457cc3ffb5724c6fe48f38957 ("Harden Macedonian placeholder restoration") so punctuation/digit-only sentinels tolerate inserted whitespace
- successful workflow run 34360492525: SUCCESS
- validated localization commit aa70bc825f6492a5bb19fae6dc2fc54c4c9bb0d8 ("Add Macedonian localization fallback")
- successful audit artifact ID 10107683527; size 291,556 bytes; SHA256 9782b4a45d6a5f0b55a6e980abd22d65a974a18653b76dfe08dc4678e2dcdd2d
- translation generation produced 2,734 unique strings total: 18 manual/pre-seeded entries plus 2,716 newly translated strings in 79 batches
- title-like refinement generated 67 additional requests in 2 batches and improved 64 / 70 title-like English remnants
- final bootstrap cache contained 2,801 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- fragile printf and numbered-placeholder strings were pre-seeded/protected and all placeholder sets were structurally audited
- bootstrap sanity passed with 2,587 Macedonian-specific letters across 29 mk_mk files

Macedonian contextual refinement:
- workflow: .github/workflows/refine-macedonian.yml
- workflow run 34361474409: SUCCESS
- refinement commit 4d4b49447985e6e310f608b7fde50ca1529e31c4 ("Refine Macedonian Minecraft terminology")
- 347 values corrected across 19 files, including 252 safe sentence-spacing fixes
- corrected contextual false friends and Minecraft terminology including Power/ability wording, Origin/Class labels, Apply, Drops, Spawn Rules, canonical Origin names, Night Vision, Ultimine, Nether/Netherite, Pavlov, Scales, health, experience and Origin Architect HUD labels
- current Minecraft Macedonian terminology was used where available, including Ноќно гледање for Night Vision, Недерот for the Nether, недерит for Netherite and Максимално здравје for maximum health
- final sanity: 2,619 Macedonian-specific letters across 29 mk_mk source files
- post-refinement NeoOrigins audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 supported add-on audits passed with 0 overlap / 0 missing / 0 placeholder errors
- post-refinement JSON validation passed

Macedonian metadata:
- synchronization run 34361736440: SUCCESS
- metadata commit 2af27bd6ebaceec0c9264208e21277e98088d175 ("Document Macedonian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md declare 52 supported locales and include mk_mk / Македонски

Final Macedonian three-target CI:
- workflow: .github/workflows/build-0.9.0-macedonian.yml
- workflow commit 07b3f97b86eb1fa9f1e92da0cbf788d81156944d
- run ID 34361874941: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Macedonian terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Macedonian terminology/specific-letter sanity, Gradle build, exact packaging verification and JAR upload

Macedonian packaging verified by CI:
- 1.21.1: 27 mk_mk files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 mk_mk files = 16 common + correct 26.1 delta
- 26.2: 17 mk_mk files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_mk_121 leaked into 26.x

Final Macedonian JAR artifacts from run 34361874941:
- mc-1.21.1: artifact ID 10108226329; size 4,016,722 bytes; SHA256 1733c952e759065a03a9ad485d38fc7d6dd6427f535091df5f21f2654476ed04
- mc-26.1.x: artifact ID 10108207419; size 2,164,246 bytes; SHA256 29ee6c1842cbdcbefaff80b4a5edaa659c6af630e4333f9a8bd617a60a3851cf
- mc-26.2: artifact ID 10108200854; size 2,163,836 bytes; SHA256 abedd58f28f3904ea486eae556c9b53bfaf3a81826479dfc9ba6c8669d211ad6

'''
if marker not in text:
    raise RuntimeError('Origin Architect section marker missing after renumbering')
text = text.replace(marker, section + marker, 1)

once('- catalog.json says 51 supported locales', '- catalog.json says 52 supported locales')
once('- README.md says 51 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz and Mongolian mn_mn', '- README.md says 52 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn and Macedonian mk_mk')
old = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh and Mongolian have passed final three-target packaging validation'
new = 'Persian, Icelandic, Malay, Filipino, Welsh, Irish, Scottish Gaelic, Armenian, Georgian, Kazakh, Mongolian and Macedonian have passed final three-target packaging validation'
once(old, new)
once('NEXT LANGUAGE = language 52.', 'NEXT LANGUAGE = language 53.')
once('Do not stop permanently at 52;', 'Do not stop permanently at 53;')

p.write_text(text, encoding='utf-8')
print('PROJECT_HANDOFF.txt updated: 52 locales, Macedonian #52, next #53')
