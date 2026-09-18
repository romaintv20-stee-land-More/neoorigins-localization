#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_locales = "0.9.0 development currently has 41 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir."
new_locales = "0.9.0 development currently has 42 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir, is_is."
if old_locales not in text:
    raise SystemExit("Current 41-locale baseline anchor not found")
text = text.replace(old_locales, new_locales, 1)

order_anchor = "- 41: Persian / fa_ir\n\nFORTY-ONE IS NOT THE FINAL TARGET."
order_replacement = "- 41: Persian / fa_ir\n- 42: Icelandic / is_is\n\nFORTY-TWO IS NOT THE FINAL TARGET."
if order_anchor not in text:
    raise SystemExit("Expansion-order anchor not found")
text = text.replace(order_anchor, order_replacement, 1)

icelandic_section = r'''30. ICELANDIC 0.9.0 STATUS
---------------------------
Icelandic locale: is_is / Íslenska.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Icelandic is a current Minecraft Java locale (is_is).
- It is a distinct North Germanic language, not a regional duplicate of any already-supported locale.
- It therefore satisfies the regional-dedup rule and materially expands the project's language coverage.

Icelandic architecture:
- 16 common namespaces: neoorigins_is_common_01 through neoorigins_is_common_16
- 1.21.1-specific namespace: neoorigins_is_121
- 26.1.x uses is_is inside neoorigins_26_1
- 26.2 uses is_is inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive is_is fallback files
- Gradle target switch: include_icelandic_121_translations / includeIcelandic121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Icelandic strings. Therefore all 10 Icelandic add-on fallback files are required.

Icelandic coverage:
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
- final Icelandic sanity check passed with 6,600 Icelandic-specific characters across 29 is_is source files

Icelandic bootstrap:
- working branch: release/0.9.0-icelandic
- workflow: .github/workflows/bootstrap-icelandic.yml
- workflow run 34327080975: SUCCESS
- validated localization commit f2fe6dc1d2bae6bdc94d92337c8da617961a1b73 ("Add Icelandic localization fallback")
- Icelandic audit artifact ID 10094376872; size 291,536 bytes; SHA256 d151e7166fbe19c2bba12ff1cee32d6dbc08c0a77885ec3da02d7e08cff075de
- initial translation set: 2,734 unique strings total; 10 manual/pre-seeded entries + 2,724 newly translated strings
- title refinement generated 379 lower-case requests in 11 batches and improved 327 / 382 title-like English remnants
- final bootstrap cache contained 3,113 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all numbered placeholders remained protected

Icelandic contextual refinement:
- workflow: .github/workflows/refine-icelandic.yml
- workflow run 34327944693: SUCCESS
- refinement commit aa20723d9066fa3405980da1947d8aae14f7940d ("Refine Icelandic Minecraft terminology")
- 55 values were corrected across 4 files
- corrected machine-translation false friends and Minecraft-specific terminology including Power, Ultimine, Origin, Mob Origin Creator, Apply, Drops, Nether/Netherite, Scales, Charge, XP, Pavlov, Night Vision and armor/health wording
- post-refinement NeoOrigins strict audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- post-refinement JSON validation passed and the Icelandic-specific character sanity count reached 6,600 across 29 files

Icelandic metadata:
- synchronization run 34328141982 succeeded
- metadata commit f71f51f16b53ef18608b83368f1ecef56afb19f1 ("Document Icelandic localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 42 supported locales and include Icelandic is_is / Íslenska

Final Icelandic three-target CI:
- workflow: .github/workflows/build-0.9.0-icelandic.yml
- workflow commit c4f11baadca7fcef29a1bda71160227b9299edf3
- run ID 34328244490: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Icelandic text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Icelandic text sanity check, Gradle build, exact packaging verification and JAR upload

Icelandic packaging verified by CI:
- 1.21.1: 27 is_is files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 is_is files = 16 common + correct 26.1 delta
- 26.2: 17 is_is files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_is_121 leaked into 26.x

Final Icelandic JAR artifacts from run 34328244490:
- mc-1.21.1: artifact ID 10094699035; size 3,105,754 bytes; SHA256 102648e7ad94316ffc58f4a3be26391080809e3d5001d12b69d8427e4b336984
- mc-26.1.x: artifact ID 10094674787; size 1,629,051 bytes; SHA256 761a70a8d72993fdb162c51e76ce4b306b2e304b598cb4a229be9f9a894f0d1d
- mc-26.2: artifact ID 10094701308; size 1,628,623 bytes; SHA256 6eec1e7e8c9ce2a8f9eda5c2bad3448f7b8741c67cefd8e75a6e4da7d7ea0f1b

'''

insert_anchor = "30. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n--------------------------------------\n"
if insert_anchor not in text:
    raise SystemExit("Origin Architect section anchor not found")
text = text.replace(insert_anchor, icelandic_section + "31. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n--------------------------------------\n", 1)

renumbers = {
    "31. CURRENT PERMANENT CI / BUILD VALIDATION": "32. CURRENT PERMANENT CI / BUILD VALIDATION",
    "32. SOURCE OF TRUTH HIERARCHY": "33. SOURCE OF TRUTH HIERARCHY",
    "33. QUALITY / QA CAVEAT": "34. QUALITY / QA CAVEAT",
    "34. NEXT ACTION": "35. NEXT ACTION",
}
for old, new in renumbers.items():
    if old not in text:
        raise SystemExit(f"Renumber anchor not found: {old}")
    text = text.replace(old, new, 1)

source_truth_old = """As of this update:
- catalog.json says 41 supported locales
- README.md says 41 languages and includes Persian fa_ir
- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk and Persian have passed final three-target packaging validation"""
source_truth_new = """As of this update:
- catalog.json says 42 supported locales
- README.md says 42 languages and includes Icelandic is_is
- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk, Persian and Icelandic have passed final three-target packaging validation"""
if source_truth_old not in text:
    raise SystemExit("Source-of-truth anchor not found")
text = text.replace(source_truth_old, source_truth_new, 1)

if "NEXT LANGUAGE = language 42." not in text:
    raise SystemExit("Next-language anchor not found")
text = text.replace("NEXT LANGUAGE = language 42.", "NEXT LANGUAGE = language 43.", 1)
if "Do not stop permanently at 42;" not in text:
    raise SystemExit("Stop-language anchor not found")
text = text.replace("Do not stop permanently at 42;", "Do not stop permanently at 43;", 1)

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Icelandic / 42 locales / next language 43")
