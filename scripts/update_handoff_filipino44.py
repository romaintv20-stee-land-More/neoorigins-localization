#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

# Baseline / roadmap.
text = text.replace(
    "0.9.0 development currently has 43 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir, is_is, ms_my.",
    "0.9.0 development currently has 44 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir, is_is, ms_my, fil_ph."
)
if "- 44: Filipino / fil_ph" not in text:
    text = text.replace("- 43: Malay / ms_my\n", "- 43: Malay / ms_my\n- 44: Filipino / fil_ph\n", 1)
text = text.replace(
    "FORTY-THREE IS NOT THE FINAL TARGET. Continue expanding toward essentially all useful Minecraft languages unless Romain changes scope.",
    "FORTY-FOUR IS NOT THE FINAL TARGET. Continue expanding toward essentially all useful Minecraft languages unless Romain changes scope."
)

# Insert Filipino status before the permanent audit/CI sections.
marker = "\n32. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "32. FILIPINO 0.9.0 STATUS" not in text:
    if marker not in text:
        raise RuntimeError("Origin Architect section marker not found")
    section = r'''

32. FILIPINO 0.9.0 STATUS
-------------------------
Filipino locale: fil_ph / Filipino.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, REBASED SAFELY ON TOP OF MALAY, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

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

Original Filipino generation branch:
- working branch: release/0.9.0-filipino
- bootstrap workflow: .github/workflows/bootstrap-filipino.yml
- first run 34335001139 stopped during generation because the translation service duplicated a numbered placeholder in a three-placeholder death message; no invalid localization was committed
- the fragile three-placeholder death messages were then manually pre-seeded and protected
- successful bootstrap run 34335376298: SUCCESS
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

Concurrent Malay integration / safe rebase:
- Malay became locale 43 on release/0.9.0-beta while the original Filipino staging branch was being finalized
- the obsolete Filipino fast-forward was deliberately NOT forced, so no Malay work was overwritten
- combined branch: release/0.9.0-filipino-rebased, based on Malay beta commit ed89e7c7e62c957102b84cbad05bf7713a7c124f
- rebase/transplant workflow run 34337000919: SUCCESS
- all 29 Filipino source files were transplanted onto the Malay baseline and the Gradle Malay + Filipino switches coexist

Combined 44-locale metadata:
- synchronization workflow run 34337148921: SUCCESS
- metadata commit 9295e27784be843f24f0aa4cf745d67bff765e2e ("Document Filipino as locale 44 after Malay")
- catalog.json / CATALOG.md / README.md declare 44 supported locales and include both Malay ms_my and Filipino fil_ph

Final combined Malay + Filipino three-target CI:
- workflow: .github/workflows/build-0.9.0-filipino-rebased.yml
- workflow commit a7ead5af59cd9233ef32c880eff44e7df72ac8d3 ("Add combined Malay Filipino final build")
- run ID 34337254023: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins audits for BOTH ms_my and fil_ph, strict audits for BOTH locales across all 10 add-ons, JSON validation, lexical sanity checks, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audits for BOTH locales, JSON validation, lexical sanity checks, Gradle build, exact packaging verification and JAR upload

Filipino packaging verified by combined CI:
- 1.21.1: 27 fil_ph files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 fil_ph files = 16 common + correct 26.1 delta
- 26.2: 17 fil_ph files = 16 common + correct 26.2 delta
- Malay packaging is simultaneously verified at 27 / 17 / 17 files
- no 1.21.1 add-on namespace or language-specific v121 delta leaked into 26.x

Final combined JAR artifacts from run 34337254023:
- mc-1.21.1: artifact ID 10098263076; size 3,269,150 bytes; SHA256 cf894f5f2ec17bd972d1adf91e09aa14f04cbfedde5e35962193b560e0cdd3ff
- mc-26.1.x: artifact ID 10098248552; size 1,724,816 bytes; SHA256 63a8fb01b405d5c25644e0dafef6a7c05943ac2aeb713bf806f6c4588aec01b1
- mc-26.2: artifact ID 10098258423; size 1,724,371 bytes; SHA256 dec86aaffe550b6049dabe60800bf2190b74afff429464e5eea7da74ea617bfd
'''
    text = text.replace(marker, section + marker, 1)

# Renumber following permanent sections after inserting Filipino.
text = text.replace("\n32. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", "\n33. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
text = text.replace("\n33. CURRENT PERMANENT CI / BUILD VALIDATION\n", "\n34. CURRENT PERMANENT CI / BUILD VALIDATION\n", 1)
text = text.replace("\n34. SOURCE OF TRUTH HIERARCHY\n", "\n35. SOURCE OF TRUTH HIERARCHY\n", 1)
text = text.replace("\n35. QUALITY / QA CAVEAT\n", "\n36. QUALITY / QA CAVEAT\n", 1)
text = text.replace("\n36. NEXT ACTION\n", "\n37. NEXT ACTION\n", 1)

# Source-of-truth summary and next action.
text = text.replace("- catalog.json says 43 supported locales", "- catalog.json says 44 supported locales")
text = text.replace("- README.md says 43 languages and includes Malay ms_my", "- README.md says 44 languages and includes Malay ms_my plus Filipino fil_ph")
text = text.replace(
    "Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk, Persian, Icelandic and Malay have passed final three-target packaging validation",
    "Romanian, Greek, Bulgarian, Vietnamese, Arabic, Hebrew, Thai, Slovak, Slovenian, Croatian, Serbian Cyrillic, Serbian Latin, Catalan, Estonian, Lithuanian, Latvian, Basque, Galician, Hindi, Norwegian Nynorsk, Persian, Icelandic, Malay and Filipino have passed final three-target packaging validation"
)
text = text.replace("NEXT LANGUAGE = language 44.", "NEXT LANGUAGE = language 45.")
text = text.replace("Do not stop permanently at 44; language expansion should continue unless Romain changes scope.", "Do not stop permanently at 45; language expansion should continue unless Romain changes scope.")

# Validation anchors.
required = [
    "0.9.0 development currently has 44 locales:",
    "- 44: Filipino / fil_ph",
    "32. FILIPINO 0.9.0 STATUS",
    "catalog.json says 44 supported locales",
    "README.md says 44 languages and includes Malay ms_my plus Filipino fil_ph",
    "NEXT LANGUAGE = language 45.",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Missing handoff anchors after update: {missing}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Filipino locale 44; next language 45")
