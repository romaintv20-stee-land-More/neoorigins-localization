#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_baseline = """0.9.0 development currently has 31 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp."""
new_baseline = """0.9.0 development currently has 32 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs."""
if old_baseline not in text and new_baseline not in text:
    raise RuntimeError("31-locale baseline anchor missing")
text = text.replace(old_baseline, new_baseline, 1)

text = text.replace(
    "- 31: Serbian Cyrillic / sr_sp\n\nTHIRTY-ONE IS NOT THE FINAL TARGET.",
    "- 31: Serbian Cyrillic / sr_sp\n- 32: Serbian Latin / sr_cs\n\nTHIRTY-TWO IS NOT THE FINAL TARGET.",
    1,
)
text = text.replace(
    "Serbian Latin (sr_cs) is intentionally NOT merged with Serbian Cyrillic (sr_sp). Minecraft exposes them as separate script variants; sr_cs remains a valid future locale.",
    "Serbian Cyrillic (sr_sp) and Serbian Latin (sr_cs) are both supported. Minecraft exposes them as separate script variants, so they remain intentionally distinct.",
    1,
)

section = r'''20. SERBIAN LATIN 0.9.0 STATUS
---------------------------------
Serbian Latin locale: sr_cs / Srpski.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: DETERMINISTICALLY TRANSLITERATED FROM THE AUDITED SERBIAN CYRILLIC LOCALE, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Serbian Latin is an official Minecraft Java locale exposed separately from Serbian Cyrillic.
- Current Minecraft locale data exposes sr_cs (Srpski) and sr_sp (Српски) as separate script variants.
- The project therefore keeps both variants instead of regional/script deduplication.

Serbian Latin architecture:
- shares the 16 Serbian common namespaces neoorigins_sr_common_01 through neoorigins_sr_common_16, with separate sr_cs.json files
- 1.21.1-specific file: neoorigins_sr_121/lang/sr_cs.json
- 26.1.x-specific file: neoorigins_26_1/lang/sr_cs.json
- 26.2-specific file: neoorigins_26_2/lang/sr_cs.json
- all 10 supported/licensed 1.21.1 add-ons receive sr_cs fallback files
- the existing include_serbian_121_translations packaging switch governs both Serbian scripts because the 1.21.1 delta namespace is shared

Translation method:
- sr_cs was not sent through a second machine-translation pass
- it is deterministically transliterated from the already audited sr_sp Serbian wording using Serbian Cyrillic -> Latin mappings, including Ђ/Đ, Ж/Ž, Љ/Lj, Њ/Nj, Ћ/Ć, Ч/Č, Џ/Dž and Ш/Š
- upstream discovery is still performed independently for sr_cs on every target, so official Serbian Latin translations retain priority
- a common key is shared only when sr_cs is missing upstream on all three targets; target-specific gaps are kept in the relevant target delta

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Serbian Latin strings. Therefore all 10 Serbian Latin add-on fallback files are required.

Serbian Latin coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed
- Serbian Latin text sanity check passed: 3,123 Serbian Latin diacritics across 29 sr_cs source files and 0 Serbian Cyrillic letters remaining

Serbian Latin bootstrap:
- workflow: .github/workflows/bootstrap-serbian-latin.yml
- workflow run 34271772698 succeeded completely
- validated localization commit 7f6692ef31225492d86e43aa244a8bae25bd0790 ("Add Serbian Latin localization fallback")
- Serbian Latin audit artifact ID 10074090569; size 399,967 bytes; SHA256 3a0e636e4710bfe8fd3743a42ae507b9dc240b0caebe7cc15c3592f5ba03d73e
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings

Serbian Latin metadata:
- synchronization run 34272061956 succeeded
- metadata commit 29eecf94f02975be397a5eda5e2a19ab53fed3f0 ("Document Serbian Latin localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 32 supported locales and include both Serbian script variants

Final Serbian Latin three-target CI:
- workflow: .github/workflows/build-0.9.0-serbian-latin.yml
- workflow commit d262fb9dc9e85777c09720739d1448d722944aa9
- run ID 34272127322: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Serbian Latin script sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Serbian Latin script sanity check, Gradle build, exact packaging verification and JAR upload

Serbian Latin packaging verified by CI:
- 1.21.1: 27 sr_cs files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 sr_cs files = 16 common + correct 26.1 delta
- 26.2: 17 sr_cs files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_sr_121 leaked into 26.x

Final Serbian Latin JAR artifacts from run 34272127322:
- mc-1.21.1: artifact ID 10074286738; size 2,241,530 bytes; SHA256 18bd09eb49757de40194208e6f07fda8594b4d19049ab01e49e6c2eb50e0094f
- mc-26.1.x: artifact ID 10074264065; size 1,119,931 bytes; SHA256 a0eb778197667e8e9eb451f3f277728014e4af92c3280619a00e1bd88e43a7a9
- mc-26.2: artifact ID 10074280050; size 1,119,546 bytes; SHA256 d2caa78bd6f0eef0e3d3a68b1b5fcf484a722f0e4d082793b02ee6c7568e780b

'''
anchor = "20. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "20. SERBIAN LATIN 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "21. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("21. CURRENT PERMANENT CI / BUILD VALIDATION", "22. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("22. SOURCE OF TRUTH HIERARCHY", "23. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("23. QUALITY / QA CAVEAT", "24. QUALITY / QA CAVEAT", 1)
    text = text.replace("24. NEXT ACTION", "25. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 31 supported locales\n- README.md says 31 languages and includes Serbian Cyrillic sr_sp\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian and Serbian Cyrillic have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 32 supported locales\n- README.md says 32 languages and includes Serbian Cyrillic sr_sp plus Serbian Latin sr_cs\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic and Serbian Latin have passed final three-target packaging validation",
    1,
)
text = text.replace("NEXT LANGUAGE = language 32.", "NEXT LANGUAGE = language 33.", 1)
text = text.replace("Do not stop permanently at 32;", "Do not stop permanently at 33;", 1)

required = [
    "0.9.0 development currently has 32 locales:",
    "- 32: Serbian Latin / sr_cs",
    "20. SERBIAN LATIN 0.9.0 STATUS",
    "run ID 34272127322: SUCCESS on all three jobs",
    "artifact ID 10074286738",
    "catalog.json says 32 supported locales",
    "NEXT LANGUAGE = language 33.",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Serbian Latin handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Serbian Latin / language 32; next language 33")
