#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace(
    "0.9.0 development currently has 25 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa.",
    "0.9.0 development currently has 26 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il.",
)
text = text.replace(
    "- 25: Arabic / ar_sa\n\nTWENTY-FIVE IS NOT THE FINAL TARGET.",
    "- 25: Arabic / ar_sa\n- 26: Hebrew / he_il\n\nTWENTY-SIX IS NOT THE FINAL TARGET.",
)

hebrew = r'''14. HEBREW 0.9.0 STATUS
-----------------------
Hebrew locale: he_il / עברית.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Hebrew is an official Minecraft Java locale.
- It is a clearly distinct language and script with no regional-dedup conflict with the existing 25-locale set.
- Hebrew is right-to-left, so the final CI includes an additional Hebrew-script sanity check on top of the normal placeholder and JSON audits.

Hebrew architecture:
- 16 common namespaces: neoorigins_he_common_01 through neoorigins_he_common_16
- 1.21.1-specific namespace: neoorigins_he_121
- 26.1.x uses he_il inside neoorigins_26_1
- 26.2 uses he_il inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive he_il fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Hebrew strings. Therefore all 10 Hebrew add-on fallback files are required.

Hebrew coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Hebrew-script sanity check passed: 71,247 Hebrew-range codepoints across 29 he_il source files

Hebrew bootstrap:
- workflow run 34263825623 succeeded completely
- validated localization commit c77712988214f62d406d820505763538bf161fd0 ("Add Hebrew localization fallback")
- Hebrew audit artifact ID 10071108855; size 291,521 bytes; SHA256 051b0e249c2ec3cfb517a8977213727174403ce686b7df5eb843ffdd58c510bf

Hebrew metadata:
- synchronization run 34264270520 succeeded
- metadata commit fed47392320e2f3caea70ac1cded1469cbe87560 ("Document Hebrew localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 26 supported locales and include Hebrew he_il

Final Hebrew three-target CI:
- workflow: .github/workflows/build-0.9.0-hebrew.yml
- final workflow commit 427b0d6c248508dea09120b52b893ed9e4fb483e
- run ID 34264247950: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Hebrew-script sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Hebrew-script sanity check, Gradle build, exact packaging verification and JAR upload

Hebrew packaging verified by CI:
- 1.21.1: 27 he_il files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 he_il files = 16 common + correct 26.1 delta
- 26.2: 17 he_il files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_he_121 leaked into 26.x

Final Hebrew JAR artifacts from run 34264247950:
- mc-1.21.1: artifact ID 10071193066; size 1,705,893 bytes; SHA256 8d6380d760fa1cf24b82186c20fe8ee82c607027ce49df7dce4b2b6a081085f2
- mc-26.1.x: artifact ID 10071171778; size 804,617 bytes; SHA256 533e4f5140e20bfbba1cfe1e408690b59ffd4739c7dabf564bfb3015714f3fe1
- mc-26.2: artifact ID 10071182069; size 804,178 bytes; SHA256 6a2bda1ef0c60b9b611e38455f8b3cdd31ac582ab60d9ebcb47a076f478ebd29

'''
anchor = "14. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "14. HEBREW 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, hebrew + "15. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("15. CURRENT PERMANENT CI / BUILD VALIDATION", "16. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("16. SOURCE OF TRUTH HIERARCHY", "17. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("17. QUALITY / QA CAVEAT", "18. QUALITY / QA CAVEAT", 1)
    text = text.replace("18. NEXT ACTION", "19. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 25 supported locales\n- README.md says 25 languages and includes Arabic ar_sa\n- Romanian, Greek, Bulgarian, Vietnamese and Arabic have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 26 supported locales\n- README.md says 26 languages and includes Hebrew he_il\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic and Hebrew have passed final three-target packaging validation",
)
text = text.replace("NEXT LANGUAGE = language 26.", "NEXT LANGUAGE = language 27.")
text = text.replace("Do not stop permanently at 26;", "Do not stop permanently at 27;")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Hebrew / language 26")
