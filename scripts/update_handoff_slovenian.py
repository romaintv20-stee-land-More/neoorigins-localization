#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace(
    "0.9.0 development currently has 28 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk.",
    "0.9.0 development currently has 29 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si.",
)
text = text.replace(
    "- 28: Slovak / sk_sk\n\nTWENTY-EIGHT IS NOT THE FINAL TARGET.",
    "- 28: Slovak / sk_sk\n- 29: Slovenian / sl_si\n\nTWENTY-NINE IS NOT THE FINAL TARGET.",
)

section = r'''17. SLOVENIAN 0.9.0 STATUS
--------------------------
Slovenian locale: sl_si / Slovenščina.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Slovenian is an official Minecraft Java locale.
- It is a distinct South Slavic language and must not be confused with Slovak despite the similar English names.
- It has no regional-dedup conflict with the existing 28-locale set.

Slovenian architecture:
- 16 common namespaces: neoorigins_sl_common_01 through neoorigins_sl_common_16
- 1.21.1-specific namespace: neoorigins_sl_121
- 26.1.x uses sl_si inside neoorigins_26_1
- 26.2 uses sl_si inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive sl_si fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Slovenian strings. Therefore all 10 Slovenian add-on fallback files are required.

Slovenian coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Slovenian text sanity check passed: 7,503 Slovenian diacritics across 29 sl_si source files

Slovenian bootstrap:
- workflow run 34267257234 succeeded completely
- validated localization commit 4f5f5a70345474cca1ae1b45fc16c1c0cffc28bd ("Add Slovenian localization fallback")
- Slovenian audit artifact ID 10072433060; size 291,539 bytes; SHA256 38e8c06a3ce76983eda181dcac07077021564478b6602f257f9b4514e60e0658
- generated 2734 unique initial English strings plus 7 title-like refinements; NeoOrigins split 2290 common + 6/17/17 deltas; add-ons 1253 physical strings

Slovenian metadata:
- synchronization run 34267724976 succeeded
- metadata commit 3ccd78506ddc296bbce1fa35f0d51bd60e7f09b4 ("Document Slovenian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 29 supported locales and include Slovenian sl_si

Final Slovenian three-target CI:
- workflow: .github/workflows/build-0.9.0-slovenian.yml
- workflow commit b69b05780aa84fdf853b2e7226968f13f409d38d
- run ID 34267783096: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Slovenian text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Slovenian text sanity check, Gradle build, exact packaging verification and JAR upload

Slovenian packaging verified by CI:
- 1.21.1: 27 sl_si files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 sl_si files = 16 common + correct 26.1 delta
- 26.2: 17 sl_si files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_sl_121 leaked into 26.x

Final Slovenian JAR artifacts from run 34267783096:
- mc-1.21.1: artifact ID 10072584069; size 1,978,547 bytes; SHA256 d88c90e6dab6969197f7fbf66a94a4ab241b40b41fbe80938a27e1855c41fc66
- mc-26.1.x: artifact ID 10072565674; size 965,745 bytes; SHA256 f762547f443129dcfd9667d53f0aeb7e8d02fc320a0cb32c5fb94ed13b7c28cd
- mc-26.2: artifact ID 10072571476; size 965,336 bytes; SHA256 8d6b8fd5ab5cee0a76ca345297529b24e40b57781be60b288ede206898fdf54c

'''
anchor = "17. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "17. SLOVENIAN 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "18. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("18. CURRENT PERMANENT CI / BUILD VALIDATION", "19. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("19. SOURCE OF TRUTH HIERARCHY", "20. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("20. QUALITY / QA CAVEAT", "21. QUALITY / QA CAVEAT", 1)
    text = text.replace("21. NEXT ACTION", "22. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 28 supported locales\n- README.md says 28 languages and includes Slovak sk_sk\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai and Slovak have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 29 supported locales\n- README.md says 29 languages and includes Slovenian sl_si\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak and Slovenian have passed final three-target packaging validation",
)
text = text.replace("NEXT LANGUAGE = language 29.", "NEXT LANGUAGE = language 30.")
text = text.replace("Do not stop permanently at 29;", "Do not stop permanently at 30;")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Slovenian / language 29")
