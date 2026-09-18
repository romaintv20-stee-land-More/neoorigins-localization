#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace(
    "0.9.0 development currently has 30 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr.",
    "0.9.0 development currently has 31 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp.",
)
text = text.replace(
    "- 30: Croatian / hr_hr\n\nTHIRTY IS NOT THE FINAL TARGET.",
    "- 30: Croatian / hr_hr\n- 31: Serbian Cyrillic / sr_sp\n\nTHIRTY-ONE IS NOT THE FINAL TARGET.",
)
text = text.replace(
    "Norwegian Nynorsk (nn_no) is intentionally NOT merged with Bokmal. It is a distinct written standard and remains a valid future locale.\n",
    "Norwegian Nynorsk (nn_no) is intentionally NOT merged with Bokmal. It is a distinct written standard and remains a valid future locale.\n\nSerbian Latin (sr_cs) is intentionally NOT merged with Serbian Cyrillic (sr_sp). Minecraft exposes them as separate script variants; sr_cs remains a valid future locale.\n",
)

section = r'''19. SERBIAN CYRILLIC 0.9.0 STATUS
----------------------------------
Serbian Cyrillic locale: sr_sp / Српски.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Serbian Cyrillic is an official Minecraft Java locale.
- Minecraft also exposes Serbian Latin separately as sr_cs, so the two script variants are intentionally not deduplicated.
- It is distinct from Croatian and Slovenian under the project's script/orthography rule.

Serbian Cyrillic architecture:
- 16 common namespaces: neoorigins_sr_common_01 through neoorigins_sr_common_16
- 1.21.1-specific namespace: neoorigins_sr_121
- 26.1.x uses sr_sp inside neoorigins_26_1
- 26.2 uses sr_sp inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive sr_sp fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Serbian Cyrillic strings. Therefore all 10 Serbian Cyrillic add-on fallback files are required.

Serbian Cyrillic coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Serbian Cyrillic text sanity check passed: 96,446 Cyrillic letters across 29 sr_sp source files

Serbian Cyrillic bootstrap:
- first two diagnostic runs exposed Serbian transliteration of internal ASCII separators/placeholders; no invalid localization commit was accepted
- final workflow run 34270381580 succeeded completely after switching internal sentinels to Unicode private-use characters
- validated localization commit 066126eb8d6824e7993702073d3433725691ea35 ("Add Serbian Cyrillic localization fallback")
- Serbian Cyrillic audit artifact ID 10073662556; size 291,540 bytes; SHA256 cc3d510e3e25fa2fc6bb4a9070b108700888a6702f284875836dd4e0fa5b5de5
- generated 2734 unique initial English strings in 79 batches; refinement pass processed 68 title-like candidates and improved 65/68; NeoOrigins split 2290 common + 6/17/17 deltas; add-ons 1253 physical strings

Serbian Cyrillic metadata:
- synchronization run 34270821374 succeeded
- metadata commit ccb30a5ff65096b5b207a3c86bf2d0bdaa5fc9e6 ("Document Serbian Cyrillic localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 31 supported locales and include Serbian Cyrillic sr_sp

Final Serbian Cyrillic three-target CI:
- workflow: .github/workflows/build-0.9.0-serbian.yml
- workflow commit a6ea54dfd1396f39eff44eb5325a85373916516e
- run ID 34270887263: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Serbian Cyrillic text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Serbian Cyrillic text sanity check, Gradle build, exact packaging verification and JAR upload

Serbian Cyrillic packaging verified by CI:
- 1.21.1: 27 sr_sp files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 sr_sp files = 16 common + correct 26.1 delta
- 26.2: 17 sr_sp files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_sr_121 leaked into 26.x

Final Serbian Cyrillic JAR artifacts from run 34270887263:
- mc-1.21.1: artifact ID 10073801783; size 2,159,870 bytes; SHA256 9c09e48ecd3c9844d4e24401629b86693f75e2c29487ca54f0b09df6db286002
- mc-26.1.x: artifact ID 10073790232; size 1,072,155 bytes; SHA256 f6c052fc01cd4d2822defd9bed606d8499fd62a12fdf4861c9f4835c68abb3a7
- mc-26.2: artifact ID 10073773611; size 1,071,694 bytes; SHA256 1da7ba2eb2ecbbdd59b561ee7bdf7e47d3772eabf91f547dcee02f3bcff1a2af

'''
anchor = "19. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "19. SERBIAN CYRILLIC 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "20. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("20. CURRENT PERMANENT CI / BUILD VALIDATION", "21. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("21. SOURCE OF TRUTH HIERARCHY", "22. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("22. QUALITY / QA CAVEAT", "23. QUALITY / QA CAVEAT", 1)
    text = text.replace("23. NEXT ACTION", "24. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 30 supported locales\n- README.md says 30 languages and includes Croatian hr_hr\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian and Croatian have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 31 supported locales\n- README.md says 31 languages and includes Serbian Cyrillic sr_sp\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian and Serbian Cyrillic have passed final three-target packaging validation",
)
text = text.replace("NEXT LANGUAGE = language 31.", "NEXT LANGUAGE = language 32.")
text = text.replace("Do not stop permanently at 31;", "Do not stop permanently at 32;")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Serbian Cyrillic / language 31")
