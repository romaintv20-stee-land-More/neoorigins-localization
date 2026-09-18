#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_baseline = """0.9.0 development currently has 38 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es."""
new_baseline = """0.9.0 development currently has 39 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in."""
if old_baseline in text:
    text = text.replace(old_baseline, new_baseline, 1)
elif new_baseline not in text:
    raise RuntimeError("38-locale baseline anchor missing")

old_order = "- 37: Basque / eu_es\n- 38: Galician / gl_es\n\nTHIRTY-EIGHT IS NOT THE FINAL TARGET."
new_order = "- 37: Basque / eu_es\n- 38: Galician / gl_es\n- 39: Hindi / hi_in\n\nTHIRTY-NINE IS NOT THE FINAL TARGET."
if old_order in text:
    text = text.replace(old_order, new_order, 1)
elif new_order not in text:
    raise RuntimeError("language expansion order anchor missing")

section = r'''27. HINDI 0.9.0 STATUS
------------------------
Hindi locale: hi_in / हिन्दी.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Hindi is a current Minecraft Java locale (hi_in).
- It is a distinct Indo-Aryan language using Devanagari, not a regional duplicate of an already-supported locale.
- It therefore satisfies the regional-dedup rule and materially expands the project's language/script coverage.

Hindi architecture:
- 16 common namespaces: neoorigins_hi_common_01 through neoorigins_hi_common_16
- 1.21.1-specific namespace: neoorigins_hi_121
- 26.1.x uses hi_in inside neoorigins_26_1
- 26.2 uses hi_in inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive hi_in fallback files
- Gradle target switch: include_hindi_121_translations / includeHindi121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Hindi strings. Therefore all 10 Hindi add-on fallback files are required.

Hindi coverage:
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
- final Hindi text sanity check passed across 29 hi_in source files

Hindi bootstrap:
- branch: release/0.9.0-hindi
- workflow: .github/workflows/bootstrap-hindi.yml
- workflow run 34309032432, attempt 2: SUCCESS
- validated localization commit 95b68ab84b3eccb098f80c6e5058f8a1f6390380 ("Add Hindi localization fallback")
- Hindi audit artifact ID 10087798162; size 291,544 bytes; SHA256 14cfb240254996003592a6795290b0647e5cc33adc0fb1122a22e3ef5d4a8247
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches, followed by three additional strings
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all numbered placeholders remained protected

Hindi contextual refinement:
- workflow: .github/workflows/refine-hindi.yml
- workflow run 34309772968: SUCCESS
- refinement commit 0bbb47a02e741c73f6db4a215c80d696dc08c934 ("Refine Hindi Minecraft terminology")
- corrected machine-translation false friends and Minecraft-specific terminology including Power, Origin, vein-mining, Drops, Nether/Netherite, Creeper, Landlubber, teleport/blink wording, Raccoon, Charge and Scales
- post-refinement NeoOrigins strict audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- post-refinement JSON and Devanagari sanity checks passed

Hindi metadata:
- synchronization run 34309834335 succeeded
- metadata commit 8f5b290fcb5c601e375a73436cf420627342562b ("Document Hindi localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 39 supported locales and include Hindi hi_in

Final Hindi three-target CI:
- workflow: .github/workflows/build-0.9.0-hindi.yml
- workflow commit cd5225b9ff614e01a256611ca83e88ea9bb7ce01
- run ID 34309885890: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Hindi text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Hindi text sanity check, Gradle build, exact packaging verification and JAR upload

Hindi packaging verified by CI:
- 1.21.1: 27 hi_in files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 hi_in files = 16 common + correct 26.1 delta
- 26.2: 17 hi_in files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_hi_121 leaked into 26.x

Final Hindi JAR artifacts from run 34309885890:
- mc-1.21.1: artifact ID 10088001109; size 2,848,617 bytes; SHA256 3c94a9b4729f984e2c2cdc404b6c31f6728fecc1c25f9e35cc3f5b756d03f09f
- mc-26.1.x: artifact ID 10087997086; size 1,478,024 bytes; SHA256 b323408954b6f5fa68d6817d55f608f35aa26d7889160ccb2b45c92a008f9a2b
- mc-26.2: artifact ID 10087988065; size 1,477,615 bytes; SHA256 4e093760925ede06e12608106fa819ff33af05e674ffc406152f7c1524db6693

'''

if "27. HINDI 0.9.0 STATUS" not in text:
    anchor = "27. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "28. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("28. CURRENT PERMANENT CI / BUILD VALIDATION", "29. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("29. SOURCE OF TRUTH HIERARCHY", "30. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("30. QUALITY / QA CAVEAT", "31. QUALITY / QA CAVEAT", 1)
    text = text.replace("31. NEXT ACTION", "32. NEXT ACTION", 1)

old_truth = """As of this update:\n- catalog.json says 38 supported locales\n- README.md says 38 languages and includes Galician gl_es\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque and Galician have passed final three-target packaging validation"""
new_truth = """As of this update:\n- catalog.json says 39 supported locales\n- README.md says 39 languages and includes Hindi hi_in\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician and Hindi have passed final three-target packaging validation"""
if old_truth in text:
    text = text.replace(old_truth, new_truth, 1)
elif new_truth not in text:
    raise RuntimeError("source-of-truth status anchor missing")

text = text.replace("NEXT LANGUAGE = language 39.", "NEXT LANGUAGE = language 40.", 1)
text = text.replace("Do not stop permanently at 39;", "Do not stop permanently at 40;", 1)

required = [
    "0.9.0 development currently has 39 locales:",
    "- 39: Hindi / hi_in",
    "THIRTY-NINE IS NOT THE FINAL TARGET.",
    "27. HINDI 0.9.0 STATUS",
    "run ID 34309885890: SUCCESS on all three jobs",
    "artifact ID 10088001109",
    "artifact ID 10087997086",
    "artifact ID 10087988065",
    "catalog.json says 39 supported locales",
    "README.md says 39 languages and includes Hindi hi_in",
    "NEXT LANGUAGE = language 40.",
    "Do not stop permanently at 40;",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Hindi handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Hindi / language 39; next language 40")
