#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_locales = "0.9.0 development currently has 42 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir, is_is."
new_locales = "0.9.0 development currently has 43 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir, is_is, ms_my."
if old_locales not in text:
    raise SystemExit("Current 42-locale baseline anchor not found")
text = text.replace(old_locales, new_locales, 1)

order_anchor = "- 42: Icelandic / is_is\n\nFORTY-TWO IS NOT THE FINAL TARGET."
order_replacement = "- 42: Icelandic / is_is\n- 43: Malay / ms_my\n\nFORTY-THREE IS NOT THE FINAL TARGET."
if order_anchor not in text:
    raise SystemExit("Expansion-order anchor not found")
text = text.replace(order_anchor, order_replacement, 1)

malay_section = r'''31. MALAY 0.9.0 STATUS
----------------------
Malay locale: ms_my / Bahasa Melayu.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Malay is a current Minecraft Java locale (ms_my).
- It is intentionally distinct from Indonesian id_id under the regional-dedup rule.
- Actual Minecraft terminology differs materially: Malay uses Tetapan / Pelayan / Pek Sumber, while Indonesian uses Pengaturan / Peladen / Paket Daya.
- Therefore ms_my is not treated as a redundant regional duplicate.

Malay architecture:
- 16 common namespaces: neoorigins_ms_common_01 through neoorigins_ms_common_16
- 1.21.1-specific namespace: neoorigins_ms_121
- 26.1.x uses ms_my inside neoorigins_26_1
- 26.2 uses ms_my inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive ms_my fallback files
- Gradle target switch: include_malay_121_translations / includeMalay121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Malay strings. Therefore all 10 Malay add-on fallback files are required.

Malay coverage:
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
- final Malay lexical sanity check passed with 2,560 Malay markers across 29 ms_my source files

Malay bootstrap:
- working branch: release/0.9.0-malay
- workflow: .github/workflows/bootstrap-malay.yml
- workflow run 34334316740: SUCCESS
- validated localization commit d0e1ddc1d69f2e029ea309059372eef1bce61147 ("Add Malay localization fallback")
- Malay audit artifact ID 10097164711; size 291,551 bytes; SHA256 a4c21d2664dba0cf2ceeaac37c1b97b30eb30162c47a7382e3627d09c9c5133b
- initial translation set: 2,734 unique strings total; 10 manual/pre-seeded entries + 2,724 newly translated strings in 79 batches
- title refinement translated 205 additional requests in 6 batches and improved 119 / 208 title-like English remnants
- final bootstrap cache contained 2,939 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all numbered placeholders remained protected

Malay contextual refinement:
- workflow: .github/workflows/refine-malay.yml
- workflow run 34334913493: SUCCESS
- refinement commit 7831cbdc8abb6d7c905e0176dce6dc768b8dd2c5 ("Refine Malay Minecraft terminology")
- 373 values were corrected across 18 files
- corrected machine-translation false friends and Minecraft-specific terminology including Ultimine, Save, Apply, Spawn Rules, Drops, Origin UI, Nether wording, Scales, Charge, Pavlov, XP, health/armor wording and hotkey labels
- also repaired recurring sentence-boundary punctuation spacing from batch translation
- post-refinement NeoOrigins strict audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- post-refinement JSON validation passed and Malay lexical sanity reached 2,560 markers across 29 files

Malay metadata:
- synchronization run 34335105656 succeeded
- metadata commit e9da087e94be9b202756c534defcb1f015a72201 ("Document Malay localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 43 supported locales and include Malay ms_my / Bahasa Melayu

Final Malay three-target CI:
- workflow: .github/workflows/build-0.9.0-malay.yml
- workflow commit 87312d61d16d90cd0c6992765e70d58fe864469a
- run ID 34335211596: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Malay text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Malay text sanity check, Gradle build, exact packaging verification and JAR upload

Malay packaging verified by CI:
- 1.21.1: 27 ms_my files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 ms_my files = 16 common + correct 26.1 delta
- 26.2: 17 ms_my files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_ms_121 leaked into 26.x

Final Malay JAR artifacts from run 34335211596:
- mc-1.21.1: artifact ID 10097476817; size 3,184,948 bytes; SHA256 a7d4f69447b9ed4dcfb16356f44bf548d6af8a3385e5ab3397f75204ff1d3185
- mc-26.1.x: artifact ID 10097453460; size 1,675,548 bytes; SHA256 b2026686d63cb43c7444e2719962c9a04004e0de4973391fa9484863e1100302
- mc-26.2: artifact ID 10097460437; size 1,675,128 bytes; SHA256 6b8b75e2010e8152b19a42b82a8ec69998eed180735fb8f1fccd45eeaafab5b6

'''

insert_anchor = "31. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n--------------------------------------\n"
if insert_anchor not in text:
    raise SystemExit("Origin Architect section anchor not found")
text = text.replace(insert_anchor, malay_section + "32. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n--------------------------------------\n", 1)

renumbers = {
    "32. CURRENT PERMANENT CI / BUILD VALIDATION": "33. CURRENT PERMANENT CI / BUILD VALIDATION",
    "33. SOURCE OF TRUTH HIERARCHY": "34. SOURCE OF TRUTH HIERARCHY",
    "34. QUALITY / QA CAVEAT": "35. QUALITY / QA CAVEAT",
    "35. NEXT ACTION": "36. NEXT ACTION",
}
for old, new in renumbers.items():
    if old not in text:
        raise SystemExit(f"Renumber anchor not found: {old}")
    text = text.replace(old, new, 1)

source_truth_old = """As of this update:
- catalog.json says 42 supported locales
- README.md says 42 languages and includes Icelandic is_is
- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk, Persian and Icelandic have passed final three-target packaging validation"""
source_truth_new = """As of this update:
- catalog.json says 43 supported locales
- README.md says 43 languages and includes Malay ms_my
- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk, Persian, Icelandic and Malay have passed final three-target packaging validation"""
if source_truth_old not in text:
    raise SystemExit("Source-of-truth anchor not found")
text = text.replace(source_truth_old, source_truth_new, 1)

if "NEXT LANGUAGE = language 43." not in text:
    raise SystemExit("Next-language anchor not found")
text = text.replace("NEXT LANGUAGE = language 43.", "NEXT LANGUAGE = language 44.", 1)
if "Do not stop permanently at 43;" not in text:
    raise SystemExit("Stop-language anchor not found")
text = text.replace("Do not stop permanently at 43;", "Do not stop permanently at 44;", 1)

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Malay / 43 locales / next language 44")
