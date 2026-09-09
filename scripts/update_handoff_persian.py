#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_locales = "0.9.0 development currently has 40 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no."
new_locales = "0.9.0 development currently has 41 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir."
if old_locales not in text:
    raise SystemExit("Current 40-locale baseline anchor not found")
text = text.replace(old_locales, new_locales, 1)

order_anchor = "- 40: Norwegian Nynorsk / nn_no\n\nFORTY IS NOT THE FINAL TARGET."
order_replacement = "- 40: Norwegian Nynorsk / nn_no\n- 41: Persian / fa_ir\n\nFORTY-ONE IS NOT THE FINAL TARGET."
if order_anchor not in text:
    raise SystemExit("Expansion-order anchor not found")
text = text.replace(order_anchor, order_replacement, 1)

persian_section = r'''29. PERSIAN 0.9.0 STATUS
-------------------------
Persian locale: fa_ir / فارسی.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Persian is a current Minecraft Java locale (fa_ir).
- It is a distinct Iranian language using the Persian form of the Arabic-derived script, not a regional variant of Arabic.
- It therefore satisfies the regional-dedup rule and materially expands the project's language coverage.

Persian architecture:
- 16 common namespaces: neoorigins_fa_common_01 through neoorigins_fa_common_16
- 1.21.1-specific namespace: neoorigins_fa_121
- 26.1.x uses fa_ir inside neoorigins_26_1
- 26.2 uses fa_ir inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive fa_ir fallback files
- Gradle target switch: include_persian_121_translations / includePersian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Persian strings. Therefore all 10 Persian add-on fallback files are required.

Persian coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- Medieval Origins Revival: 401 / 401
- ibarn's quartet origins addon: 69 / 69
- Origins Fantasy for NeoOrigins: 240 / 240
- Origins: Backgrounds for NeoOrigins: 65 / 65
- Origins: More Backgrounds for NeoOrigins: 44 / 44 effective (39 primary + 5 shared)
- Origins: Backgrounds ISS for NeoOrigins: 79 / 79 effective (77 primary + 2 shared)
- Origins Furries for NeoOrigins: 117 / 117
- Origins: Classes Extended for NeoOrigins: 124 / 124
- Origins: Classes ISS for NeoOrigins: 99 / 99
- Origin Architect: 22 / 22
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- final Persian sanity check passed with 89,526 Arabic-script characters and 15,136 Persian-specific characters across 29 fa_ir source files

Persian bootstrap:
- working branch: release/0.9.0-persian
- workflow: .github/workflows/bootstrap-persian.yml
- workflow run 34321520710: SUCCESS
- validated localization commit 70611d30ad745c4db54971a4327c17487d412701 ("Add Persian localization fallback")
- Persian audit artifact ID 10092092857; size 291,535 bytes; SHA256 2ec40775aac9dedaed0c0b9c8db35d7ae9f575a48479d4c8f949a1799358eb80
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all numbered placeholders remained protected

Persian contextual refinement:
- workflow: .github/workflows/refine-persian.yml
- workflow run 34321930297: SUCCESS
- refinement commit 14e06c03a46c638aeb0a8649cb67d9b4529cc7a6 ("Refine Persian Minecraft terminology")
- 62 values were corrected across 11 files
- corrected machine-translation false friends and Minecraft-specific terminology including Power, Ultimine, Apply, Drops, HP, Scales, Origin and Nether/Netherite wording
- post-refinement NeoOrigins strict audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- post-refinement JSON validation and Persian script sanity checks passed

Persian metadata:
- synchronization run 34322064617 succeeded
- metadata commit 4627959bd6fde4175c49fb239e61fdb77a939dc4 ("Document Persian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 41 supported locales and include Persian fa_ir / فارسی

Final Persian three-target CI:
- workflow: .github/workflows/build-0.9.0-persian.yml
- workflow commit 6fcb9aa28931aca0e049677dd91123ada28c223e
- run ID 34322162989: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Persian text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Persian text sanity check, Gradle build, exact packaging verification and JAR upload

Persian packaging verified by CI:
- 1.21.1: 27 fa_ir files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 fa_ir files = 16 common + correct 26.1 delta
- 26.2: 17 fa_ir files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_fa_121 leaked into 26.x

Final Persian JAR artifacts from run 34322162989:
- mc-1.21.1: artifact ID 10092326980; size 3,021,206 bytes; SHA256 73cc894dbc55c276e2d113f5aa46de6a07f9b631d81fee2aa56cfbd9e3cdae17
- mc-26.1.x: artifact ID 10092311911; size 1,579,561 bytes; SHA256 76489978665539e8a22143b82d6e8606a910a90575aae94e1a7287db991e58e7
- mc-26.2: artifact ID 10092306159; size 1,579,109 bytes; SHA256 3b52f95ebc119d7d69896971b9e76d8ab40c5c353524594c46fece1d10064704

'''

insert_anchor = "29. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n--------------------------------------\n"
if insert_anchor not in text:
    raise SystemExit("Origin Architect section anchor not found")
text = text.replace(insert_anchor, persian_section + "30. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n--------------------------------------\n", 1)

renumbers = {
    "30. CURRENT PERMANENT CI / BUILD VALIDATION": "31. CURRENT PERMANENT CI / BUILD VALIDATION",
    "31. SOURCE OF TRUTH HIERARCHY": "32. SOURCE OF TRUTH HIERARCHY",
    "32. QUALITY / QA CAVEAT": "33. QUALITY / QA CAVEAT",
    "33. NEXT ACTION": "34. NEXT ACTION",
}
for old, new in renumbers.items():
    if old not in text:
        raise SystemExit(f"Renumber anchor not found: {old}")
    text = text.replace(old, new, 1)

source_truth_old = """As of this update:
- catalog.json says 40 supported locales
- README.md says 40 languages and includes Norwegian Nynorsk nn_no
- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi and Norwegian Nynorsk have passed final three-target packaging validation"""
source_truth_new = """As of this update:
- catalog.json says 41 supported locales
- README.md says 41 languages and includes Persian fa_ir
- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk and Persian have passed final three-target packaging validation"""
if source_truth_old not in text:
    raise SystemExit("Source-of-truth anchor not found")
text = text.replace(source_truth_old, source_truth_new, 1)

if "NEXT LANGUAGE = language 41." not in text:
    raise SystemExit("Next-language anchor not found")
text = text.replace("NEXT LANGUAGE = language 41.", "NEXT LANGUAGE = language 42.", 1)
if "Do not stop permanently at 41;" not in text:
    raise SystemExit("Stop-language anchor not found")
text = text.replace("Do not stop permanently at 41;", "Do not stop permanently at 42;", 1)

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Persian / 41 locales / next language 42")
