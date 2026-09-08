#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_baseline = """0.9.0 development currently has 34 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee."""
new_baseline = """0.9.0 development currently has 35 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt."""
if old_baseline not in text and new_baseline not in text:
    raise RuntimeError("34-locale baseline anchor missing")
text = text.replace(old_baseline, new_baseline, 1)

text = text.replace(
    "- 34: Estonian / et_ee\n\nTHIRTY-FOUR IS NOT THE FINAL TARGET.",
    "- 34: Estonian / et_ee\n- 35: Lithuanian / lt_lt\n\nTHIRTY-FIVE IS NOT THE FINAL TARGET.",
    1,
)

section = r'''23. LITHUANIAN 0.9.0 STATUS
----------------------------
Lithuanian locale: lt_lt / Lietuvių.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Lithuanian is a current Minecraft Java locale (lt_lt).
- It is a distinct Baltic language, not a regional variant of any locale already supported.
- It therefore has no regional-dedup conflict with the existing 34-locale set.

Lithuanian architecture:
- 16 common namespaces: neoorigins_lt_common_01 through neoorigins_lt_common_16
- 1.21.1-specific namespace: neoorigins_lt_121
- 26.1.x uses lt_lt inside neoorigins_26_1
- 26.2 uses lt_lt inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive lt_lt fallback files
- Gradle target switch: include_lithuanian_121_translations / includeLithuanian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Lithuanian strings. Therefore all 10 Lithuanian add-on fallback files are required.

Lithuanian coverage:
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
- Lithuanian text sanity check passed: 8,246 Lithuanian diacritics across 29 lt_lt source files

Lithuanian bootstrap:
- workflow: .github/workflows/bootstrap-lithuanian.yml
- workflow run 34276420986 succeeded completely
- validated localization commit c7d80d63d5520685632476326696b4698daf5fc0 ("Add Lithuanian localization fallback")
- Lithuanian audit artifact ID 10075964861; size 291,528 bytes; SHA256 e89499ffb3751002529896ae5c3b6784d710089b7d8172943cd48b456491b302
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- refinement pass translated 186 additional title-like requests in 6 batches and improved 165/189 title-like strings left in English
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all three numbered placeholders remained protected; strict placeholder audits passed afterward

Lithuanian metadata:
- metadata synchronization succeeded
- metadata commit 7a1863a42a9aee6bea497f8c06ddb7a86f95d1c7 ("Document Lithuanian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 35 supported locales and include Lithuanian lt_lt

Final Lithuanian three-target CI:
- workflow: .github/workflows/build-0.9.0-lithuanian.yml
- workflow commit e0280084ac5ecea88fdcbbabaf2f608c74f72b55
- run ID 34276928531: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Lithuanian text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Lithuanian text sanity check, Gradle build, exact packaging verification and JAR upload

Lithuanian packaging verified by CI:
- 1.21.1: 27 lt_lt files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 lt_lt files = 16 common + correct 26.1 delta
- 26.2: 17 lt_lt files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_lt_121 leaked into 26.x

Final Lithuanian JAR artifacts from run 34276928531:
- mc-1.21.1: artifact ID 10076110046; size 2,494,502 bytes; SHA256 ec3ec97c7efb67a39170088b5e495182e03e21b4f0406346b8b214c9d30e94d5
- mc-26.1.x: artifact ID 10076111874; size 1,269,100 bytes; SHA256 1f658c25f6576c258fca0d865849b57f44447b58c259d2bf4e3fb0842a6f21eb
- mc-26.2: artifact ID 10076117965; size 1,268,703 bytes; SHA256 abb4ea16ef58fb50f98aa23a93138756d9cd4ab509bcfce63721b7c07629817e

'''
anchor = "23. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "23. LITHUANIAN 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "24. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("24. CURRENT PERMANENT CI / BUILD VALIDATION", "25. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("25. SOURCE OF TRUTH HIERARCHY", "26. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("26. QUALITY / QA CAVEAT", "27. QUALITY / QA CAVEAT", 1)
    text = text.replace("27. NEXT ACTION", "28. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 34 supported locales\n- README.md says 34 languages and includes Estonian et_ee\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan and Estonian have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 35 supported locales\n- README.md says 35 languages and includes Lithuanian lt_lt\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian and Lithuanian have passed final three-target packaging validation",
    1,
)
text = text.replace("NEXT LANGUAGE = language 35.", "NEXT LANGUAGE = language 36.", 1)
text = text.replace("Do not stop permanently at 35;", "Do not stop permanently at 36;", 1)

required = [
    "0.9.0 development currently has 35 locales:",
    "- 35: Lithuanian / lt_lt",
    "23. LITHUANIAN 0.9.0 STATUS",
    "run ID 34276928531: SUCCESS on all three jobs",
    "artifact ID 10076110046",
    "artifact ID 10076111874",
    "artifact ID 10076117965",
    "catalog.json says 35 supported locales",
    "NEXT LANGUAGE = language 36.",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Lithuanian handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Lithuanian / language 35; next language 36")
