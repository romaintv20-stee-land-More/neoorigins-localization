#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_baseline = """0.9.0 development currently has 39 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in."""
new_baseline = """0.9.0 development currently has 40 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no."""
if old_baseline in text:
    text = text.replace(old_baseline, new_baseline, 1)
elif new_baseline not in text:
    raise RuntimeError("39-locale baseline anchor missing")

old_order = "- 38: Galician / gl_es\n- 39: Hindi / hi_in\n\nTHIRTY-NINE IS NOT THE FINAL TARGET."
new_order = "- 38: Galician / gl_es\n- 39: Hindi / hi_in\n- 40: Norwegian Nynorsk / nn_no\n\nFORTY IS NOT THE FINAL TARGET."
if old_order in text:
    text = text.replace(old_order, new_order, 1)
elif new_order not in text:
    raise RuntimeError("language expansion order anchor missing")

section = r'''28. NORWEGIAN NYNORSK 0.9.0 STATUS
--------------------------------------
Norwegian Nynorsk locale: nn_no / Norsk nynorsk.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Norwegian Nynorsk is a current Minecraft Java locale (nn_no).
- It is a distinct official Norwegian written standard, not merely a regional spelling variant of Bokmal.
- PROJECT_HANDOFF already explicitly retained nn_no as a valid future locale separate from no_no, so it satisfies the project's regional-dedup rule.

Nynorsk architecture:
- 16 common namespaces: neoorigins_nn_common_01 through neoorigins_nn_common_16
- 1.21.1-specific namespace: neoorigins_nn_121
- 26.1.x uses nn_no inside neoorigins_26_1
- 26.2 uses nn_no inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive nn_no fallback files
- Gradle target switch: include_nynorsk_121_translations / includeNynorsk121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Nynorsk strings. Therefore all 10 Nynorsk add-on fallback files are required.

Nynorsk coverage:
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

Nynorsk bootstrap and conversion method:
- working branch: release/0.9.0-nynorsk
- workflow: .github/workflows/bootstrap-nynorsk.yml
- successful workflow run 34310606158 passed generation, pruning, all strict audits, JSON validation and packaging-switch integration
- validated localization commit 96c41b1f5ddb13705dfdf1485f88409d4c548121 ("Add Nynorsk localization fallback")
- Nynorsk audit artifact ID 10088224487; size 291,540 bytes; SHA256 c599d59da5838e3ceff53c2afb295c9273e9aa27aac1db1397d25d760e67ae40
- conversion reused the project's already-audited Bokmal no_no fallback wording, then converted it with Apertium's dedicated nob-nno Bokmal-to-Nynorsk pair
- 2,715 unique Bokmal strings were converted; no English-to-Bokmal fallback was required for missing source strings
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings
- initial sanity check found 990 Nynorsk lexical markers and 1,640 / 3,583 compared strings differed from Bokmal, confirming nn_no is not a renamed no_no copy

Nynorsk contextual refinement:
- workflow: .github/workflows/refine-nynorsk.yml
- workflow run 34310807346: SUCCESS
- refinement commit 97537eacca97bd058ec98e8ecee52df3bc3cee0b ("Refine Nynorsk Minecraft terminology")
- corrected context-sensitive false friends and Minecraft terminology including Power, Ultimine, Apply, Drops, Origin, Nether wording and several add-on terms
- post-refinement NeoOrigins strict audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- post-refinement JSON validation passed and the Nynorsk lexical sanity count increased to 992 markers across 29 nn_no source files

Nynorsk metadata:
- synchronization run 34310910613 succeeded
- metadata commit 6180a1baea4fed2833207f986518e1460f88ab05 ("Document Nynorsk localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 40 supported locales and include Norwegian Nynorsk nn_no

Final Nynorsk three-target CI:
- workflow: .github/workflows/build-0.9.0-nynorsk.yml
- workflow commit f0eff335cf374992e0970ea8ad05ee03501f58dc
- run ID 34310968849: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Nynorsk text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Nynorsk text sanity check, Gradle build, exact packaging verification and JAR upload

Nynorsk packaging verified by CI:
- 1.21.1: 27 nn_no files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 nn_no files = 16 common + correct 26.1 delta
- 26.2: 17 nn_no files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_nn_121 leaked into 26.x

Final Nynorsk JAR artifacts from run 34310968849:
- mc-1.21.1: artifact ID 10088369347; size 2,928,552 bytes; SHA256 d416136f5d227283b95163d468ec7d03dd0d65474161fad69b872885c699c815
- mc-26.1.x: artifact ID 10088357379; size 1,524,738 bytes; SHA256 93ababb2c5958dbcd00d1649dd56aa4a658873ddd701fc304cf54f6761b94e0b
- mc-26.2: artifact ID 10088354778; size 1,524,277 bytes; SHA256 994b637b62fe921f2660d5c818398e3e2392347cbde9a0c95b9d7c9020472ec0

'''

if "28. NORWEGIAN NYNORSK 0.9.0 STATUS" not in text:
    anchor = "28. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, section + "29. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("29. CURRENT PERMANENT CI / BUILD VALIDATION", "30. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("30. SOURCE OF TRUTH HIERARCHY", "31. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("31. QUALITY / QA CAVEAT", "32. QUALITY / QA CAVEAT", 1)
    text = text.replace("32. NEXT ACTION", "33. NEXT ACTION", 1)

old_truth = """As of this update:\n- catalog.json says 39 supported locales\n- README.md says 39 languages and includes Hindi hi_in\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician and Hindi have passed final three-target packaging validation"""
new_truth = """As of this update:\n- catalog.json says 40 supported locales\n- README.md says 40 languages and includes Norwegian Nynorsk nn_no\n- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi and Norwegian Nynorsk have passed final three-target packaging validation"""
if old_truth in text:
    text = text.replace(old_truth, new_truth, 1)
elif new_truth not in text:
    raise RuntimeError("source-of-truth status anchor missing")

text = text.replace("NEXT LANGUAGE = language 40.", "NEXT LANGUAGE = language 41.", 1)
text = text.replace("Do not stop permanently at 40;", "Do not stop permanently at 41;", 1)

required = [
    "0.9.0 development currently has 40 locales:",
    "- 40: Norwegian Nynorsk / nn_no",
    "FORTY IS NOT THE FINAL TARGET.",
    "28. NORWEGIAN NYNORSK 0.9.0 STATUS",
    "successful workflow run 34310606158",
    "refinement commit 97537eacca97bd058ec98e8ecee52df3bc3cee0b",
    "metadata commit 6180a1baea4fed2833207f986518e1460f88ab05",
    "run ID 34310968849: SUCCESS on all three jobs",
    "artifact ID 10088369347",
    "artifact ID 10088357379",
    "artifact ID 10088354778",
    "catalog.json says 40 supported locales",
    "README.md says 40 languages and includes Norwegian Nynorsk nn_no",
    "NEXT LANGUAGE = language 41.",
    "Do not stop permanently at 41;",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Nynorsk handoff validation failed; missing: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Norwegian Nynorsk / language 40; next language 41")
