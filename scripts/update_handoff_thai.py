#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace(
    "0.9.0 development currently has 26 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il.",
    "0.9.0 development currently has 27 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th.",
)
text = text.replace(
    "- 26: Hebrew / he_il\n\nTWENTY-SIX IS NOT THE FINAL TARGET.",
    "- 26: Hebrew / he_il\n- 27: Thai / th_th\n\nTWENTY-SEVEN IS NOT THE FINAL TARGET.",
)

thai = r'''15. THAI 0.9.0 STATUS
---------------------
Thai locale: th_th / ภาษาไทย.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Thai is an official Minecraft Java locale.
- It is a clearly distinct language and script with no regional-dedup conflict with the existing 26-locale set.
- The final CI includes an additional Thai-script sanity check on top of the normal placeholder and JSON audits.

Thai architecture:
- 16 common namespaces: neoorigins_th_common_01 through neoorigins_th_common_16
- 1.21.1-specific namespace: neoorigins_th_121
- 26.1.x uses th_th inside neoorigins_26_1
- 26.2 uses th_th inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive th_th fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Thai strings. Therefore all 10 Thai add-on fallback files are required.

Thai coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Thai-script sanity check passed: 105,485 Thai-range codepoints across 29 th_th source files

Thai bootstrap:
- workflow run 34264864221 succeeded completely
- validated localization commit 65a192e922714d3eda475c30e54e23504a81a7f1 ("Add Thai localization fallback")
- Thai audit artifact ID 10071479848; size 291,552 bytes; SHA256 adeb8079ad071f092f32e42048b6601a6e726db231b1609be9e861b87cfc5be1
- generated 2734 unique initial English strings plus 3 title-like refinements; NeoOrigins split 2290 common + 6/17/17 deltas; add-ons 1253 physical strings

Thai metadata:
- synchronization run 34265206287 succeeded
- metadata commit 95c217a80bc9aff844fc1596b17b1b0d7e96f3de ("Document Thai localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 27 supported locales and include Thai th_th

Final Thai three-target CI:
- workflow: .github/workflows/build-0.9.0-thai.yml
- final workflow commit cb7640721b2ddcc9c66793e43d9cf2f0c26ec7f3
- run ID 34265269152: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Thai-script sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Thai-script sanity check, Gradle build, exact packaging verification and JAR upload

Thai packaging verified by CI:
- 1.21.1: 27 th_th files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 th_th files = 16 common + correct 26.1 delta
- 26.2: 17 th_th files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_th_121 leaked into 26.x

Final Thai JAR artifacts from run 34265269152:
- mc-1.21.1: artifact ID 10071615284; size 1,807,249 bytes; SHA256 b51113d6c97e912fff662e7e5b9f74c414a949d9df7f4b043fd1f154d2c9b33f
- mc-26.1.x: artifact ID 10071602798; size 864,641 bytes; SHA256 b34bf9994dc1db69fb6c440969a3707c136ead670f9562a50454b336400e9e02
- mc-26.2: artifact ID 10071576279; size 864,210 bytes; SHA256 623eea3560345ed7808f60539cf152f7a6da2e56de9023988dd987869e1cff2d

'''
anchor = "15. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "15. THAI 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, thai + "16. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("16. CURRENT PERMANENT CI / BUILD VALIDATION", "17. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("17. SOURCE OF TRUTH HIERARCHY", "18. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("18. QUALITY / QA CAVEAT", "19. QUALITY / QA CAVEAT", 1)
    text = text.replace("19. NEXT ACTION", "20. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 26 supported locales\n- README.md says 26 languages and includes Hebrew he_il\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic and Hebrew have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 27 supported locales\n- README.md says 27 languages and includes Thai th_th\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew and Thai have passed final three-target packaging validation",
)
text = text.replace("NEXT LANGUAGE = language 27.", "NEXT LANGUAGE = language 28.")
text = text.replace("Do not stop permanently at 27;", "Do not stop permanently at 28;")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Thai / language 27")
