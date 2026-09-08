#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_baseline = """0.9.0 development currently has 35 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt."""
new_baseline = """0.9.0 development currently has 36 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv."""
if old_baseline not in text and new_baseline not in text:
    raise RuntimeError("35-locale baseline anchor missing")
text = text.replace(old_baseline, new_baseline, 1)

text = text.replace(
    "- 35: Lithuanian / lt_lt\n\nTHIRTY-FIVE IS NOT THE FINAL TARGET.",
    "- 35: Lithuanian / lt_lt\n- 36: Latvian / lv_lv\n\nTHIRTY-SIX IS NOT THE FINAL TARGET.",
    1,
)

section = r'''24. LATVIAN 0.9.0 STATUS
-------------------------
Latvian locale: lv_lv / Latviešu.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Latvian is a current Minecraft Java locale (lv_lv).
- It is a distinct Baltic language and is not a regional variant of Lithuanian.
- It therefore has no regional-dedup conflict with the existing 35-locale set.

Latvian architecture:
- 16 common namespaces: neoorigins_lv_common_01 through neoorigins_lv_common_16
- 1.21.1-specific namespace: neoorigins_lv_121
- 26.1.x uses lv_lv inside neoorigins_26_1
- 26.2 uses lv_lv inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive lv_lv fallback files
- Gradle target switch: include_latvian_121_translations / includeLatvian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Latvian strings. Therefore all 10 Latvian add-on fallback files are required.

Latvian coverage:
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
- Latvian text sanity check passed: 11,251 Latvian diacritics across 29 lv_lv source files

Latvian bootstrap:
- workflow: .github/workflows/bootstrap-latvian.yml
- workflow run 34278840372 succeeded completely
- validated localization commit e0a5f0b798d41ea1aa8275b7c81cf8cab20d9aab ("Add Latvian localization fallback")
- Latvian audit artifact ID 10076878703; size 291,540 bytes; SHA256 dc30bc70c78fc7cb8192f700d9efd0f2ed3890c6e9d61096844a33cfa7ba701d
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- refinement pass translated 210 additional title-like requests in 6 batches and improved 181/213 title-like strings left in English
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all three numbered placeholders remained protected; strict placeholder audits passed afterward

Latvian metadata:
- synchronization run 34279176856 succeeded
- metadata commit e0c5d19eff02afe2ec1b52aad9b5f60298b34b4e ("Document Latvian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 36 supported locales and include Latvian lv_lv

Final Latvian three-target CI:
- workflow: .github/workflows/build-0.9.0-latvian.yml
- workflow commit 8c67b57f59b314be6cd54e2fabda1fdde1093816
- run ID 34279238396: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Latvian text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Latvian text sanity check, Gradle build, exact packaging verification and JAR upload

Latvian packaging verified by CI:
- 1.21.1: 27 lv_lv files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 lv_lv files = 16 common + correct 26.1 delta
- 26.2: 17 lv_lv files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_lv_121 leaked into 26.x

Final Latvian JAR artifacts from run 34279238396:
- mc-1.21.1: artifact ID 10076978386; size 2,580,988 bytes; SHA256 bc9698fa2480bdfc6a879ff881f5182a1e984ac5c04ac81bf60b049b698435da
- mc-26.1.x: artifact ID 10076973662; size 1,320,108 bytes; SHA256 aac91264ef764b7b0170d63f605e1b553650d7ad7270326f3b316ce51a185dc1
- mc-26.2: artifact ID 10076979994; size 1,319,780 bytes; SHA256 197917430191815ea62cd211222a9866401ca61c292ef6169a19f042b787be08

'''
anchor = "24. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "24. LATVIAN 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "25. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("25. CURRENT PERMANENT CI / BUILD VALIDATION", "26. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("26. SOURCE OF TRUTH HIERARCHY", "27. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("27. QUALITY / QA CAVEAT", "28. QUALITY / QA CAVEAT", 1)
    text = text.replace("28. NEXT ACTION", "29. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 35 supported locales\n- README.md says 35 languages and includes Lithuanian lt_lt\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian and Lithuanian have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 36 supported locales\n- README.md says 36 languages and includes Latvian lv_lv\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian and Latvian have passed final three-target packaging validation",
    1,
)
text = text.replace("NEXT LANGUAGE = language 36.", "NEXT LANGUAGE = language 37.", 1)
text = text.replace("Do not stop permanently at 36;", "Do not stop permanently at 37;", 1)

required = [
    "0.9.0 development currently has 36 locales:",
    "- 36: Latvian / lv_lv",
    "24. LATVIAN 0.9.0 STATUS",
    "workflow run 34278840372 succeeded completely",
    "e0a5f0b798d41ea1aa8275b7c81cf8cab20d9aab",
    "artifact ID 10076878703",
    "run ID 34279238396: SUCCESS on all three jobs",
    "artifact ID 10076978386",
    "artifact ID 10076973662",
    "artifact ID 10076979994",
    "catalog.json says 36 supported locales",
    "NEXT LANGUAGE = language 37.",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Latvian handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Latvian / language 36; next language 37")
