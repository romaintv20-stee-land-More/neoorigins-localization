#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_baseline = """0.9.0 development currently has 36 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv."""
new_baseline = """0.9.0 development currently has 37 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es."""
if old_baseline not in text and new_baseline not in text:
    raise RuntimeError("36-locale baseline anchor missing")
text = text.replace(old_baseline, new_baseline, 1)

old_order = "- 35: Lithuanian / lt_lt\n- 36: Latvian / lv_lv\n\nTHIRTY-SIX IS NOT THE FINAL TARGET."
new_order = "- 35: Lithuanian / lt_lt\n- 36: Latvian / lv_lv\n- 37: Basque / eu_es\n\nTHIRTY-SEVEN IS NOT THE FINAL TARGET."
if old_order in text:
    text = text.replace(old_order, new_order, 1)
elif new_order not in text:
    raise RuntimeError("language expansion order anchor missing")

section = r'''25. BASQUE 0.9.0 STATUS
-------------------------
Basque locale: eu_es / Euskara.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Basque is a Minecraft Java locale (eu_es).
- It is a distinct language and is not a regional variant of any locale already supported.
- It therefore has no regional-dedup conflict with the existing 36-locale set.

Basque architecture:
- 16 common namespaces: neoorigins_eu_common_01 through neoorigins_eu_common_16
- 1.21.1-specific namespace: neoorigins_eu_121
- 26.1.x uses eu_es inside neoorigins_26_1
- 26.2 uses eu_es inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive eu_es fallback files
- Gradle target switch: include_basque_121_translations / includeBasque121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Basque strings. Therefore all 10 Basque add-on fallback files are required.

Basque coverage:
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
- Basque text sanity check passed: 1,675 Basque lexical markers across 29 eu_es source files

Basque bootstrap:
- workflow: .github/workflows/bootstrap-basque.yml
- workflow run 34306574713 succeeded completely
- validated localization commit d3144a1e35761970aa9970ce74bc69c007d342c8 ("Add Basque localization fallback")
- Basque audit artifact ID 10086910218; size 291,524 bytes; SHA256 0b0349621de9edbaff15fce60f365fdb696565248e1d91acd92f6f1a5c76e20a
- initial translation set: 2,734 unique strings total; 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- refinement pass translated 212 additional title-like requests in 7 batches and improved 169/215 title-like strings left in English
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- the fragile three-placeholder death message was manually pre-seeded so all three numbered placeholders remained protected; strict placeholder audits passed afterward

Basque metadata:
- synchronization run 34306827228 succeeded
- metadata commit 30151fa6a711dc263b2333dc7365ed736366e285 ("Document Basque localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 37 supported locales and include Basque eu_es

Final Basque three-target CI:
- workflow: .github/workflows/build-0.9.0-basque.yml
- workflow commit b37c775742651978c310695fb73fd49aa53f768c
- run ID 34306894163: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Basque text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Basque text sanity check, Gradle build, exact packaging verification and JAR upload

Basque packaging verified by CI:
- 1.21.1: 27 eu_es files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 eu_es files = 16 common + correct 26.1 delta
- 26.2: 17 eu_es files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_eu_121 leaked into 26.x

Final Basque JAR artifacts from run 34306894163:
- mc-1.21.1: artifact ID 10086986595; size 2,663,240 bytes; SHA256 3d4b68312136d68031bd41d38922dcb94924d2a6489c725fb7542e8cd62208c3
- mc-26.1.x: artifact ID 10086992362; size 1,368,934 bytes; SHA256 3b0468af7f22e93bd86938e31aa76bc5ef41d71493244ee1938e21e5bc5adffe
- mc-26.2: artifact ID 10086982073; size 1,368,552 bytes; SHA256 e8e9be172777222552aab9e69e4aaa2fde024c41e23ed33cb5c6e692ee3f6b42

'''

if "25. BASQUE 0.9.0 STATUS" not in text:
    anchor = "25. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "26. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("26. CURRENT PERMANENT CI / BUILD VALIDATION", "27. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("27. SOURCE OF TRUTH HIERARCHY", "28. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("28. QUALITY / QA CAVEAT", "29. QUALITY / QA CAVEAT", 1)
    text = text.replace("29. NEXT ACTION", "30. NEXT ACTION", 1)

old_truth = """As of this update:\n- catalog.json says 36 supported locales\n- README.md says 36 languages and includes Latvian lv_lv\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian and Latvian have passed final three-target packaging validation"""
new_truth = """As of this update:\n- catalog.json says 37 supported locales\n- README.md says 37 languages and includes Basque eu_es\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian and Basque have passed final three-target packaging validation"""
if old_truth in text:
    text = text.replace(old_truth, new_truth, 1)
elif new_truth not in text:
    raise RuntimeError("source-of-truth status anchor missing")

text = text.replace("NEXT LANGUAGE = language 37.", "NEXT LANGUAGE = language 38.", 1)
text = text.replace("Do not stop permanently at 37;", "Do not stop permanently at 38;", 1)

required = [
    "0.9.0 development currently has 37 locales:",
    "- 37: Basque / eu_es",
    "THIRTY-SEVEN IS NOT THE FINAL TARGET.",
    "25. BASQUE 0.9.0 STATUS",
    "run ID 34306894163: SUCCESS on all three jobs",
    "artifact ID 10086986595",
    "artifact ID 10086992362",
    "artifact ID 10086982073",
    "catalog.json says 37 supported locales",
    "README.md says 37 languages and includes Basque eu_es",
    "NEXT LANGUAGE = language 38.",
    "Do not stop permanently at 38;",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Basque handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Basque / language 37; next language 38")
