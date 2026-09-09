#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

old_locales = "0.9.0 development currently has 42 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir, is_is."
new_locales = "0.9.0 development currently has 43 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir, is_is, fil_ph."
if old_locales not in text:
    raise SystemExit("Current 42-locale baseline anchor not found")
text = text.replace(old_locales, new_locales, 1)

order_anchor = "- 42: Icelandic / is_is\n\nFORTY-TWO IS NOT THE FINAL TARGET."
order_replacement = "- 42: Icelandic / is_is\n- 43: Filipino / fil_ph\n\nFORTY-THREE IS NOT THE FINAL TARGET."
if order_anchor not in text:
    raise SystemExit("Expansion-order anchor not found")
text = text.replace(order_anchor, order_replacement, 1)

filipino_section = r'''31. FILIPINO 0.9.0 STATUS
-------------------------
Filipino locale: fil_ph / Filipino.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Filipino is a current Minecraft Java locale (fil_ph).
- It is a distinct Philippine language locale and is not a regional duplicate of any already-supported locale.
- It therefore satisfies the regional-dedup rule and materially expands the project's language coverage.

Filipino architecture:
- 16 common namespaces: neoorigins_fil_common_01 through neoorigins_fil_common_16
- 1.21.1-specific namespace: neoorigins_fil_121
- 26.1.x uses fil_ph inside neoorigins_26_1
- 26.2 uses fil_ph inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive fil_ph fallback files
- Gradle target switch: include_filipino_121_translations / includeFilipino121Translations

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Filipino strings. Therefore all 10 Filipino add-on fallback files are required.

Filipino coverage:
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
- final Filipino sanity check passed with 8,475 Filipino lexical markers across 29 fil_ph source files

Filipino bootstrap:
- working branch: release/0.9.0-filipino
- workflow: .github/workflows/bootstrap-filipino.yml
- first run 34335001139 stopped during generation because the translation service duplicated a numbered placeholder in a three-placeholder death message; no invalid localization was committed
- the fragile three-placeholder death messages were then manually pre-seeded and protected
- successful workflow run 34335376298: SUCCESS
- validated localization commit a91e52b9b6f3de21e47846a9f53a496d38ca2d9c ("Add Filipino localization fallback")
- Filipino audit artifact ID 10097547845; size 291,734 bytes; SHA256 4d358e883bbd5cc16129317bca22666d42b96976703f172260821892f0142da9
- initial cache: 15 manual/pre-seeded entries + 2,719 newly translated strings in 79 batches
- title-like refinement generated 663 lower-case requests in 19 batches and improved 340 / 668 title-like English remnants
- final bootstrap cache contained 3,397 entries
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- add-ons: 10 fallback files / 1253 physical strings

Filipino contextual refinement:
- workflow: .github/workflows/refine-filipino.yml
- workflow run 34335919135: SUCCESS
- refinement commit 40b6611bd78257e58b8765493ab4c2a41e77663c ("Refine Filipino Minecraft terminology")
- 281 values were corrected across 19 files, including 242 safe sentence-spacing fixes
- corrected machine-translation false friends and Minecraft-specific terminology including Ultimine, Drops, Nether Born, Charge, Origin Architect HUD labels, Night Vision, Nether/Netherite, XP, Pavlov and Scales
- post-refinement NeoOrigins strict audits remained 0 overlap / 0 missing / 0 placeholder errors on all three targets
- post-refinement JSON validation passed and the Filipino lexical sanity count reached 8,475 markers across 29 files

Filipino metadata:
- synchronization run 34336093840 succeeded
- metadata commit bbd3853a686587c755c2ff440c18b75dda889418 ("Document Filipino localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 43 supported locales and include Filipino fil_ph

Final Filipino three-target CI:
- workflow: .github/workflows/build-0.9.0-filipino.yml
- workflow commit 60432934c9c84fa1fd2e53c35e65e1a80e2b33bc
- run ID 34336195625: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Filipino text sanity check, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Filipino text sanity check, Gradle build, exact packaging verification and JAR upload

Filipino packaging verified by CI:
- 1.21.1: 27 fil_ph files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 fil_ph files = 16 common + correct 26.1 delta
- 26.2: 17 fil_ph files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_fil_121 leaked into 26.x

Final Filipino JAR artifacts from run 34336195625:
- mc-1.21.1: artifact ID 10097843788; size 3,189,939 bytes; SHA256 213fb955a25b50a2a815a393c8b7ea5fcc08b7f2c5824aeb9ef205de759bf25f
- mc-26.1.x: artifact ID 10097830287; size 1,678,361 bytes; SHA256 68099705adfb5e1d5f167bdb78fb260d9783e41cc98d1fed379f06c5c5427857
- mc-26.2: artifact ID 10097836601; size 1,677,934 bytes; SHA256 77b4686e0ed69b8160fc197068c276e1cd49fef9f74164e490661caafeaad5cc

'''

insert_anchor = "31. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n--------------------------------------\n"
if insert_anchor not in text:
    raise SystemExit("Origin Architect section anchor not found")
text = text.replace(insert_anchor, filipino_section + "32. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n--------------------------------------\n", 1)

renumbers = {
    "32. CURRENT PERMANENT CI / BUILD VALIDATION": "33. CURRENT PERMANENT CI / BUILD VALIDATION",
    "33. SOURCE OF TRUTH HIERARCHY": "34. SOURCE OF TRUTH HIERARCHY",
    "34. QUALITY / QA CAVEAT": "35. QUALITY / QA CAVEAT",
    "35. NEXT ACTION": "36. NEXT ACTION",
}
for old, new in renumbers.items():
    if old not in text:
        raise SystemExit(f"Renumber anchor not found: {old}")
    text = text.replace(old, new, 1)

source_truth_old = """As of this update:
- catalog.json says 42 supported locales
- README.md says 42 languages and includes Icelandic is_is
- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk, Persian and Icelandic have passed final three-target packaging validation"""
source_truth_new = """As of this update:
- catalog.json says 43 supported locales
- README.md says 43 languages and includes Filipino fil_ph
- Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk, Persian, Icelandic and Filipino have passed final three-target packaging validation"""
if source_truth_old not in text:
    raise SystemExit("Source-of-truth anchor not found")
text = text.replace(source_truth_old, source_truth_new, 1)

if "NEXT LANGUAGE = language 43." not in text:
    raise SystemExit("Next-language anchor not found")
text = text.replace("NEXT LANGUAGE = language 43.", "NEXT LANGUAGE = language 44.", 1)
if "Do not stop permanently at 43;" not in text:
    raise SystemExit("Stop-language anchor not found")
text = text.replace("Do not stop permanently at 43;", "Do not stop permanently at 44;", 1)

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Filipino / 43 locales / next language 44")
