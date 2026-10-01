#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace(
    "0.9.0 development currently has 29 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si.",
    "0.9.0 development currently has 30 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr.",
)
text = text.replace(
    "- 29: Slovenian / sl_si\n\nTWENTY-NINE IS NOT THE FINAL TARGET.",
    "- 29: Slovenian / sl_si\n- 30: Croatian / hr_hr\n\nTHIRTY IS NOT THE FINAL TARGET.",
)

section = r'''18. CROATIAN 0.9.0 STATUS
-------------------------
Croatian locale: hr_hr / Hrvatski.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Croatian is an official Minecraft Java locale.
- It is a distinct South Slavic standard and is not merged with Slovenian or Serbian under the regional-variant dedup rule.
- It has no regional-dedup conflict with the existing 29-locale set.

Croatian architecture:
- 16 common namespaces: neoorigins_hr_common_01 through neoorigins_hr_common_16
- 1.21.1-specific namespace: neoorigins_hr_121
- 26.1.x uses hr_hr inside neoorigins_26_1
- 26.2 uses hr_hr inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive hr_hr fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Croatian strings. Therefore all 10 Croatian add-on fallback files are required.

Croatian coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Croatian text sanity check passed: 3,708 Croatian diacritics across 29 hr_hr source files

Croatian bootstrap:
- workflow run 34268369121 succeeded completely
- validated localization commit 6f42d79d905b04380c0e7e6e0bdad20b044dd7e3 ("Add Croatian localization fallback")
- Croatian audit artifact ID 10072868618; size 291,548 bytes; SHA256 4a51f7a92075df78125b58d0be280ed0e572be0ef469ecc74def43d2920593a4
- generated 2734 unique initial English strings; refinement pass processed 368 strings and improved 295/370 title-like unchanged candidates; NeoOrigins split 2290 common + 6/17/17 deltas; add-ons 1253 physical strings

Croatian metadata:
- synchronization run 34268814609 succeeded
- metadata commit cca8ded487e48a563a91f0b0b9bad47e50665b20 ("Document Croatian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 30 supported locales and include Croatian hr_hr

Final Croatian three-target CI:
- workflow: .github/workflows/build-0.9.0-croatian.yml
- workflow commit 664a7cd140630d0001459a3bdb648ae87afa713c
- run ID 34268887082: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Croatian text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Croatian text sanity check, Gradle build, exact packaging verification and JAR upload

Croatian packaging verified by CI:
- 1.21.1: 27 hr_hr files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 hr_hr files = 16 common + correct 26.1 delta
- 26.2: 17 hr_hr files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_hr_121 leaked into 26.x

Final Croatian JAR artifacts from run 34268887082:
- mc-1.21.1: artifact ID 10073028620; size 2,061,651 bytes; SHA256 90c746b5f451e2f309c21cc817dc6870ff8d63e174a28449628cb0f0ecaf7f7f
- mc-26.1.x: artifact ID 10073006742; size 1,014,799 bytes; SHA256 67738ba7d27a9ad71ab60cb260cb46feded7d2c4432ccd7bba0adcee3cc6ad1e
- mc-26.2: artifact ID 10073016485; size 1,014,384 bytes; SHA256 cf4a68f919c626f6ba7edfdae6e2e49e7cc937ebdf3a883da4d388985191a3fa

'''
anchor = "18. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "18. CROATIAN 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "19. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("19. CURRENT PERMANENT CI / BUILD VALIDATION", "20. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("20. SOURCE OF TRUTH HIERARCHY", "21. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("21. QUALITY / QA CAVEAT", "22. QUALITY / QA CAVEAT", 1)
    text = text.replace("22. NEXT ACTION", "23. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 29 supported locales\n- README.md says 29 languages and includes Slovenian sl_si\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak and Slovenian have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 30 supported locales\n- README.md says 30 languages and includes Croatian hr_hr\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian and Croatian have passed final three-target packaging validation",
)
text = text.replace("NEXT LANGUAGE = language 30.", "NEXT LANGUAGE = language 31.")
text = text.replace("Do not stop permanently at 30;", "Do not stop permanently at 31;")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Croatian / language 30")
