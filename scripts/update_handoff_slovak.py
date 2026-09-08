#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_locales = "0.9.0 development currently has 27 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th."
new_locales = "0.9.0 development currently has 28 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk."
if old_locales not in text and new_locales not in text:
    raise RuntimeError("27-locale baseline anchor missing")
text = text.replace(old_locales, new_locales, 1)

old_order = "- 27: Thai / th_th\n\nTWENTY-SEVEN IS NOT THE FINAL TARGET."
new_order = "- 27: Thai / th_th\n- 28: Slovak / sk_sk\n\nTWENTY-EIGHT IS NOT THE FINAL TARGET."
if old_order not in text and new_order not in text:
    raise RuntimeError("language expansion anchor missing")
text = text.replace(old_order, new_order, 1)

slovak = r'''16. SLOVAK 0.9.0 STATUS
-----------------------
Slovak locale: sk_sk / Slovenčina.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Slovak is an official Minecraft Java locale.
- It is a clearly distinct language from Czech and has no regional-dedup conflict with the existing 27-locale set.
- Norwegian Nynorsk (nn_no) remains a valid future locale, but was intentionally deferred here because the current translation provider does not offer a reliable Nynorsk target. Do not synthesize/fake Nynorsk by merely reusing Bokmal.

Slovak architecture:
- 16 common namespaces: neoorigins_sk_common_01 through neoorigins_sk_common_16
- 1.21.1-specific namespace: neoorigins_sk_121
- 26.1.x uses sk_sk inside neoorigins_26_1
- 26.2 uses sk_sk inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive sk_sk fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Slovak strings. Therefore all 10 Slovak add-on fallback files are required.

Slovak coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Slovak text sanity check passed: 12,262 Slovak diacritics across 29 sk_sk source files

Slovak bootstrap:
- workflow run 34265980422 succeeded completely
- validated localization commit 0fcabe6c614dbde8f8859d23b57908aba4735069 ("Add Slovak localization fallback")
- Slovak audit artifact ID 10071940071; size 291,530 bytes; SHA256 34ee2518d49a19220405d88efd0baef2a1463112601c0b7d0588044599043d26
- generated 2734 unique initial English strings plus 3 title-like refinements; NeoOrigins split 2290 common + 6/17/17 deltas; add-ons 1253 physical strings

Slovak metadata:
- synchronization run 34266451680 succeeded
- metadata commit fd6628646f043d8f812eddef44691f66da2a0477 ("Document Slovak localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 28 supported locales and include Slovak sk_sk

Final Slovak three-target CI:
- workflow: .github/workflows/build-0.9.0-slovak.yml
- workflow commit 2336f8fbe00d3fe1af2fbeeb1d1a8037f7d33de5
- run ID 34266350634: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Slovak text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Slovak text sanity check, Gradle build, exact packaging verification and JAR upload

Slovak packaging verified by CI:
- 1.21.1: 27 sk_sk files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 sk_sk files = 16 common + correct 26.1 delta
- 26.2: 17 sk_sk files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_sk_121 leaked into 26.x

Final Slovak JAR artifacts from run 34266350634:
- mc-1.21.1: artifact ID 10072020263; size 1,895,464 bytes; SHA256 6acdd5a1af9dcaa24d2d2c6e5140e063e60d2e974f6465ee07ff7065b718c533
- mc-26.1.x: artifact ID 10072020135; size 916,591 bytes; SHA256 eb003a309b04889de9640fb93543880cf8c6052c5cb389ff5b079995127cab6c
- mc-26.2: artifact ID 10072010122; size 916,182 bytes; SHA256 e84447afd3db92f53153e48119dbfe46f23807dfc8f3da495a25bd614208da8a

'''
anchor = "16. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "16. SLOVAK 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, slovak + "17. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("17. CURRENT PERMANENT CI / BUILD VALIDATION", "18. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("18. SOURCE OF TRUTH HIERARCHY", "19. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("19. QUALITY / QA CAVEAT", "20. QUALITY / QA CAVEAT", 1)
    text = text.replace("20. NEXT ACTION", "21. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 27 supported locales\n- README.md says 27 languages and includes Thai th_th\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew and Thai have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 28 supported locales\n- README.md says 28 languages and includes Slovak sk_sk\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai and Slovak have passed final three-target packaging validation",
    1,
)
text = text.replace("NEXT LANGUAGE = language 28.", "NEXT LANGUAGE = language 29.", 1)
text = text.replace("Do not stop permanently at 28;", "Do not stop permanently at 29;", 1)

checks = [
    "0.9.0 development currently has 28 locales:",
    "- 28: Slovak / sk_sk",
    "16. SLOVAK 0.9.0 STATUS",
    "run ID 34266350634: SUCCESS on all three jobs",
    "metadata commit fd6628646f043d8f812eddef44691f66da2a0477",
    "NEXT LANGUAGE = language 29.",
]
for needle in checks:
    if needle not in text:
        raise RuntimeError(f"handoff validation marker missing: {needle}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Slovak / language 28")
