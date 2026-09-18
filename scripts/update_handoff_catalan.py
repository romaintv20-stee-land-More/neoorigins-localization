#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_baseline = """0.9.0 development currently has 32 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs."""
new_baseline = """0.9.0 development currently has 33 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es."""
if old_baseline not in text and new_baseline not in text:
    raise RuntimeError("32-locale baseline anchor missing")
text = text.replace(old_baseline, new_baseline, 1)

text = text.replace(
    "- 32: Serbian Latin / sr_cs\n\nTHIRTY-TWO IS NOT THE FINAL TARGET.",
    "- 32: Serbian Latin / sr_cs\n- 33: Catalan / ca_es\n\nTHIRTY-THREE IS NOT THE FINAL TARGET.",
    1,
)

section = r'''21. CATALAN 0.9.0 STATUS
-------------------------
Catalan locale: ca_es / Català.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Catalan is an official/current Minecraft Java locale (ca_es).
- It is a distinct Romance language, not a trivial regional spelling variant of Spanish or French.
- It therefore has no regional-dedup conflict with the existing 32-locale set.

Catalan architecture:
- 16 common namespaces: neoorigins_ca_common_01 through neoorigins_ca_common_16
- 1.21.1-specific namespace: neoorigins_ca_121
- 26.1.x uses ca_es inside neoorigins_26_1
- 26.2 uses ca_es inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive ca_es fallback files
- Gradle target switch: include_catalan_121_translations / includeCatalan121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Catalan strings. Therefore all 10 Catalan add-on fallback files are required.

Catalan coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Catalan text sanity check passed: 10,680 Catalan diacritics across 29 ca_es source files

Catalan bootstrap:
- workflow: .github/workflows/bootstrap-catalan.yml
- first diagnostic run 34272869095 correctly failed before any localization commit because machine translation dropped the %2$s actor from the three-placeholder death message "%1$s had their soul ripped apart by %2$s's %3$s"
- no invalid Catalan translation was accepted from that diagnostic run
- the fragile string was manually protected as "%1$s va tenir l'ànima arrencada pel %3$s de %2$s" and the manual override cache was pre-seeded before translation
- successful workflow run 34273251870 then passed generation, pruning, all strict audits, validation and packaging-switch integration
- validated localization commit 7ca7ba3b649718b5916e34f7fc2b1c5089a222a2 ("Add Catalan localization fallback")
- successful Catalan audit artifact ID 10074761577; size 399,957 bytes; SHA256 a65ab60430648f828986dc382582626ece9125791196426f5427aa5ebb97d8be
- generated 2734 unique initial English strings in 79 batches; NeoOrigins split 2290 common + 6/17/17 target deltas; add-ons 1253 physical strings

Catalan metadata:
- synchronization run 34273706166 succeeded
- metadata commit 71f9031cd2ce4aeebfb2cae7c8c3dd9ceac1ab7f ("Document Catalan localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 33 supported locales and include Catalan ca_es

Final Catalan three-target CI:
- workflow: .github/workflows/build-0.9.0-catalan.yml
- workflow commit 2690b861985c80546139b39c8c14508cd72b8138
- run ID 34273780369: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Catalan text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Catalan text sanity check, Gradle build, exact packaging verification and JAR upload

Catalan packaging verified by CI:
- 1.21.1: 27 ca_es files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 ca_es files = 16 common + correct 26.1 delta
- 26.2: 17 ca_es files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_ca_121 leaked into 26.x

Final Catalan JAR artifacts from run 34273780369:
- mc-1.21.1: artifact ID 10074921570; size 2,324,716 bytes; SHA256 c99014aa42d3a164efcb8de4671f49947e77dd4d9ebdf9c1c0254b99b5ff2c8c
- mc-26.1.x: artifact ID 10074904630; size 1,168,936 bytes; SHA256 c13b385c34c66448ad67d37e74343d6c306fea16025db6e541ca00ee1b131a79
- mc-26.2: artifact ID 10074907075; size 1,168,535 bytes; SHA256 0b5251545bc04b9e8d7cdacaf9419cb027a6d611087377cd435ba4a4b9bad393

'''
anchor = "21. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "21. CATALAN 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "22. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("22. CURRENT PERMANENT CI / BUILD VALIDATION", "23. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("23. SOURCE OF TRUTH HIERARCHY", "24. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("24. QUALITY / QA CAVEAT", "25. QUALITY / QA CAVEAT", 1)
    text = text.replace("25. NEXT ACTION", "26. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 32 supported locales\n- README.md says 32 languages and includes Serbian Cyrillic sr_sp plus Serbian Latin sr_cs\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic and Serbian Latin have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 33 supported locales\n- README.md says 33 languages and includes Catalan ca_es\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin and Catalan have passed final three-target packaging validation",
    1,
)
text = text.replace("NEXT LANGUAGE = language 33.", "NEXT LANGUAGE = language 34.", 1)
text = text.replace("Do not stop permanently at 33;", "Do not stop permanently at 34;", 1)

required = [
    "0.9.0 development currently has 33 locales:",
    "- 33: Catalan / ca_es",
    "21. CATALAN 0.9.0 STATUS",
    "run ID 34273780369: SUCCESS on all three jobs",
    "artifact ID 10074921570",
    "artifact ID 10074904630",
    "artifact ID 10074907075",
    "catalog.json says 33 supported locales",
    "NEXT LANGUAGE = language 34.",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Catalan handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Catalan / language 33; next language 34")
