#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace("Last updated: 2026-09-08", "Last updated: 2026-09-09", 1)

old_baseline = """0.9.0 development currently has 37 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es."""
new_baseline = """0.9.0 development currently has 38 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es."""
if old_baseline in text:
    text = text.replace(old_baseline, new_baseline, 1)
elif new_baseline not in text:
    raise RuntimeError("37-locale baseline anchor missing")

old_order = "- 36: Latvian / lv_lv\n- 37: Basque / eu_es\n\nTHIRTY-SEVEN IS NOT THE FINAL TARGET."
new_order = "- 36: Latvian / lv_lv\n- 37: Basque / eu_es\n- 38: Galician / gl_es\n\nTHIRTY-EIGHT IS NOT THE FINAL TARGET."
if old_order in text:
    text = text.replace(old_order, new_order, 1)
elif new_order not in text:
    raise RuntimeError("language expansion order anchor missing")

section = r'''26. GALICIAN 0.9.0 STATUS
---------------------------
Galician locale: gl_es / Galego.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Galician is a current Minecraft Java locale (gl_es).
- It is a distinct Romance language, not merely a regional variant of Spanish or Portuguese.
- It therefore has no regional-dedup conflict with the existing 37-locale set.

Galician architecture:
- 16 common namespaces: neoorigins_gl_common_01 through neoorigins_gl_common_16
- 1.21.1-specific namespace: neoorigins_gl_121
- 26.1.x uses gl_es inside neoorigins_26_1
- 26.2 uses gl_es inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive gl_es fallback files
- Gradle target switch: include_galician_121_translations / includeGalician121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Galician strings. Therefore all 10 Galician add-on fallback files are required.

Galician coverage:
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
- Galician text sanity check passed: 1,752 Galician lexical markers across 29 gl_es source files

Galician bootstrap:
- workflow: .github/workflows/bootstrap-galician.yml
- workflow run 34307359353 succeeded completely
- validated localization commit 4bfdd1864aa5c453c375d35c88196fb0bbf2e384 ("Add Galician localization fallback")
- Galician audit artifact ID 10087178372; size 291,535 bytes; SHA256 63e62e515dc1bde4b4ae3b1a74d2dc0ba473343a7de6df5b6b322028eb5a96d8
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- refinement pass translated 174 additional title-like requests in 5 batches and improved 139/177 title-like strings left in English
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all three numbered placeholders remained protected; strict placeholder audits passed afterward

Galician metadata:
- synchronization run 34307684886 succeeded
- metadata commit a409a5ab97bfd6e1f7a14b8054874743564a3198 ("Document Galician localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 38 supported locales and include Galician gl_es

Final Galician three-target CI:
- workflow: .github/workflows/build-0.9.0-galician.yml
- workflow commit 0585f8b2f7cf7f5845ba06bc39a723185a53ccde
- run ID 34307757409: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Galician text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Galician text sanity check, Gradle build, exact packaging verification and JAR upload

Galician packaging verified by CI:
- 1.21.1: 27 gl_es files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 gl_es files = 16 common + correct 26.1 delta
- 26.2: 17 gl_es files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_gl_121 leaked into 26.x

Final Galician JAR artifacts from run 34307757409:
- mc-1.21.1: artifact ID 10087286262; size 2,746,271 bytes; SHA256 dd8af0cd88fefebbe6249a8837600c6ddcf4c9eb1bfa79ee545a2b0262843cfb
- mc-26.1.x: artifact ID 10087275789; size 1,417,966 bytes; SHA256 0ab137463709d10ba6260332d1863f70db1f1cf97bbce430580c52bbd1dcef81
- mc-26.2: artifact ID 10087276192; size 1,417,564 bytes; SHA256 bcab0af60bd76b21ed8d9ddcafae880fe3fffca8c64f098f48c53c63d52daabf

'''

if "26. GALICIAN 0.9.0 STATUS" not in text:
    anchor = "26. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "27. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("27. CURRENT PERMANENT CI / BUILD VALIDATION", "28. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("28. SOURCE OF TRUTH HIERARCHY", "29. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("29. QUALITY / QA CAVEAT", "30. QUALITY / QA CAVEAT", 1)
    text = text.replace("30. NEXT ACTION", "31. NEXT ACTION", 1)

old_truth = """As of this update:\n- catalog.json says 37 supported locales\n- README.md says 37 languages and includes Basque eu_es\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian and Basque have passed final three-target packaging validation"""
new_truth = """As of this update:\n- catalog.json says 38 supported locales\n- README.md says 38 languages and includes Galician gl_es\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque and Galician have passed final three-target packaging validation"""
if old_truth in text:
    text = text.replace(old_truth, new_truth, 1)
elif new_truth not in text:
    raise RuntimeError("source-of-truth status anchor missing")

text = text.replace("NEXT LANGUAGE = language 38.", "NEXT LANGUAGE = language 39.", 1)
text = text.replace("Do not stop permanently at 38;", "Do not stop permanently at 39;", 1)

required = [
    "0.9.0 development currently has 38 locales:",
    "- 38: Galician / gl_es",
    "THIRTY-EIGHT IS NOT THE FINAL TARGET.",
    "26. GALICIAN 0.9.0 STATUS",
    "run ID 34307757409: SUCCESS on all three jobs",
    "artifact ID 10087286262",
    "artifact ID 10087275789",
    "artifact ID 10087276192",
    "catalog.json says 38 supported locales",
    "README.md says 38 languages and includes Galician gl_es",
    "NEXT LANGUAGE = language 39.",
    "Do not stop permanently at 39;",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Galician handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Galician / language 38; next language 39")
