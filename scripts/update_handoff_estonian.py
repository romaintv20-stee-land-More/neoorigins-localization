#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_baseline = """0.9.0 development currently has 33 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es."""
new_baseline = """0.9.0 development currently has 34 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee."""
if old_baseline not in text and new_baseline not in text:
    raise RuntimeError("33-locale baseline anchor missing")
text = text.replace(old_baseline, new_baseline, 1)

text = text.replace(
    "- 33: Catalan / ca_es\n\nTHIRTY-THREE IS NOT THE FINAL TARGET.",
    "- 33: Catalan / ca_es\n- 34: Estonian / et_ee\n\nTHIRTY-FOUR IS NOT THE FINAL TARGET.",
    1,
)

section = r'''22. ESTONIAN 0.9.0 STATUS
--------------------------
Estonian locale: et_ee / Eesti.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Estonian is a current Minecraft Java locale (et_ee).
- It is a distinct Uralic language and is not a regional variant of Finnish.
- It therefore has no regional-dedup conflict with the existing 33-locale set.

Estonian architecture:
- 16 common namespaces: neoorigins_et_common_01 through neoorigins_et_common_16
- 1.21.1-specific namespace: neoorigins_et_121
- 26.1.x uses et_ee inside neoorigins_26_1
- 26.2 uses et_ee inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive et_ee fallback files
- Gradle target switch: include_estonian_121_translations / includeEstonian121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Estonian strings. Therefore all 10 Estonian add-on fallback files are required.

Estonian coverage:
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
- Estonian text sanity check passed: 4,125 Estonian diacritics across 29 et_ee source files

Estonian bootstrap:
- workflow: .github/workflows/bootstrap-estonian.yml
- workflow run 34274479480 succeeded completely
- validated localization commit a5b28b326e75aa332e06c072a29d51b79f5c2fd6 ("Add Estonian localization fallback")
- Estonian audit artifact ID 10075239154; size 291,530 bytes; SHA256 ece58ad663b83f6b822f8ef011c7f32cbb94ed6b6761b6c384a75e7823d3a9d0
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- refinement pass translated 223 additional title-like requests in 7 batches and improved 186/227 title-like strings left in English
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all three numbered placeholders remained protected; strict placeholder audits passed afterward

Estonian metadata:
- synchronization run 34274894696 succeeded
- metadata commit ef20499b31aa5aabb6d1d6f5fdda2265f89ecfda ("Document Estonian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 34 supported locales and include Estonian et_ee

Final Estonian three-target CI:
- workflow: .github/workflows/build-0.9.0-estonian.yml
- workflow commit 310f27f9a75bcbff304a365bcc37b90083cd33e5
- run ID 34274989745: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Estonian text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Estonian text sanity check, Gradle build, exact packaging verification and JAR upload

Estonian packaging verified by CI:
- 1.21.1: 27 et_ee files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 et_ee files = 16 common + correct 26.1 delta
- 26.2: 17 et_ee files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_et_121 leaked into 26.x

Final Estonian JAR artifacts from run 34274989745:
- mc-1.21.1: artifact ID 10075393938; size 2,407,618 bytes; SHA256 2d71b8acd17241e44cd95fca6c54e3f4f3b40f3ede6352d3048b36c9487cab8a
- mc-26.1.x: artifact ID 10075374956; size 1,217,858 bytes; SHA256 b047a95c0a72440b14989bfece38c13bad62679e0604c106adf62a67b31c91bb
- mc-26.2: artifact ID 10075360262; size 1,217,452 bytes; SHA256 57dcfd7042f3eb242d86d8232ca0e44410f34e1c1b6cd8d9ec2578e23a0d339d

'''
anchor = "22. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "22. ESTONIAN 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "23. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("23. CURRENT PERMANENT CI / BUILD VALIDATION", "24. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("24. SOURCE OF TRUTH HIERARCHY", "25. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("25. QUALITY / QA CAVEAT", "26. QUALITY / QA CAVEAT", 1)
    text = text.replace("26. NEXT ACTION", "27. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 33 supported locales\n- README.md says 33 languages and includes Catalan ca_es\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin and Catalan have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 34 supported locales\n- README.md says 34 languages and includes Estonian et_ee\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan and Estonian have passed final three-target packaging validation",
    1,
)
text = text.replace("NEXT LANGUAGE = language 34.", "NEXT LANGUAGE = language 35.", 1)
text = text.replace("Do not stop permanently at 34;", "Do not stop permanently at 35;", 1)

required = [
    "0.9.0 development currently has 34 locales:",
    "- 34: Estonian / et_ee",
    "22. ESTONIAN 0.9.0 STATUS",
    "run ID 34274989745: SUCCESS on all three jobs",
    "artifact ID 10075393938",
    "artifact ID 10075374956",
    "artifact ID 10075360262",
    "catalog.json says 34 supported locales",
    "NEXT LANGUAGE = language 35.",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Estonian handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Estonian / language 34; next language 35")
