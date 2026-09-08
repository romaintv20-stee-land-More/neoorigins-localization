#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace(
    "0.9.0 development currently has 24 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn.",
    "0.9.0 development currently has 25 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa.",
)
text = text.replace(
    "- 24: Vietnamese / vi_vn\n\nTWENTY-FOUR IS NOT THE FINAL TARGET.",
    "- 24: Vietnamese / vi_vn\n- 25: Arabic / ar_sa\n\nTWENTY-FIVE IS NOT THE FINAL TARGET.",
)

arabic = r'''13. ARABIC 0.9.0 STATUS
-----------------------
Arabic locale: ar_sa / العربية.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Arabic is an official Minecraft Java locale.
- It is a clearly distinct language and script with no regional-dedup conflict with the existing 24-locale set.
- Arabic is right-to-left, so the final CI includes an additional Arabic-script sanity check on top of the normal placeholder and JSON audits.

Arabic architecture:
- 16 common namespaces: neoorigins_ar_common_01 through neoorigins_ar_common_16
- 1.21.1-specific namespace: neoorigins_ar_121
- 26.1.x uses ar_sa inside neoorigins_26_1
- 26.2 uses ar_sa inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive ar_sa fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Arabic strings. Therefore all 10 Arabic add-on fallback files are required.

Arabic coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Arabic-script sanity check passed: 88,611 Arabic-range codepoints across 29 ar_sa source files

Arabic bootstrap:
- workflow run 34262716603 succeeded completely
- validated localization commit 630bb368d6024917e24b8eb4148c3592b87bfe66 ("Add Arabic localization fallback")
- Arabic audit artifact ID 10070622529; size 291,540 bytes; SHA256 cf4062c580b41d2cceaf221fd0df53ecf291e3d96071cd316c980735b8558ea7

Arabic metadata:
- synchronization run 34263061455 succeeded
- metadata commit 2b27f03e446d8eb2b1671cfc280289aa7c9ac9e0 ("Document Arabic localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 25 supported locales and include Arabic ar_sa

Final Arabic three-target CI:
- workflow: .github/workflows/build-0.9.0-arabic.yml
- final workflow commit fa502c7329956eb44cf82cfa04a6169aa5aa1964
- run ID 34263122706: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Arabic-script sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Arabic-script sanity check, Gradle build, exact packaging verification and JAR upload

Arabic packaging verified by CI:
- 1.21.1: 27 ar_sa files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 ar_sa files = 16 common + correct 26.1 delta
- 26.2: 17 ar_sa files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_ar_121 leaked into 26.x

Final Arabic JAR artifacts from run 34263122706:
- mc-1.21.1: artifact ID 10070742043; size 1,621,562 bytes; SHA256 954ae10f549ce605125f083176b892a973cf0bc5b9b835ec00f0563bfa44822c
- mc-26.1.x: artifact ID 10070733439; size 755,144 bytes; SHA256 1870e661176cb5ed9f9ab7eb2c5d1545f5dd00e44ac363a5f2966ea9cdb29b2b
- mc-26.2: artifact ID 10070728913; size 754,708 bytes; SHA256 c6905a0e0c08e6692fe3c06f5956405671b7bb6baab8cadc4d3558905facc0ca

'''
anchor = "13. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "13. ARABIC 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, arabic + "14. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("14. CURRENT PERMANENT CI / BUILD VALIDATION", "15. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("15. SOURCE OF TRUTH HIERARCHY", "16. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("16. QUALITY / QA CAVEAT", "17. QUALITY / QA CAVEAT", 1)
    text = text.replace("17. NEXT ACTION", "18. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 24 supported locales\n- README.md says 24 languages and includes Vietnamese vi_vn\n- Romanian, Greek, Bulgarian and Vietnamese have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 25 supported locales\n- README.md says 25 languages and includes Arabic ar_sa\n- Romanian, Greek, Bulgarian, Vietnamese and Arabic have passed final three-target packaging validation",
)
text = text.replace("NEXT LANGUAGE = language 25.", "NEXT LANGUAGE = language 26.")
text = text.replace("Do not stop permanently at 25;", "Do not stop permanently at 26;")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Arabic / language 25")
