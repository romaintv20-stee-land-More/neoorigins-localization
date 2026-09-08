#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace(
    "0.9.0 development currently has 22 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr.",
    "0.9.0 development currently has 23 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg.",
)
text = text.replace(
    "- 22: Greek / el_gr\n\nTWENTY-TWO IS NOT THE FINAL TARGET.",
    "- 22: Greek / el_gr\n- 23: Bulgarian / bg_bg\n\nTWENTY-THREE IS NOT THE FINAL TARGET.",
)

bulgarian = r'''11. BULGARIAN 0.9.0 STATUS
--------------------------
Bulgarian locale: bg_bg / Български.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Bulgarian is an official Minecraft Java locale.
- It is a clearly distinct language and has no regional-dedup conflict with the existing 22-locale set.

Bulgarian architecture:
- 16 common namespaces: neoorigins_bg_common_01 through neoorigins_bg_common_16
- 1.21.1-specific namespace: neoorigins_bg_121
- 26.1.x uses bg_bg inside neoorigins_26_1
- 26.2 uses bg_bg inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive bg_bg fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Bulgarian strings. Therefore all 10 Bulgarian add-on fallback files are required.

Bulgarian coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed

Bootstrap history:
- first run 34259179195 failed during generation only because the local safety check required numbered printf placeholders such as %1$s / %2$s / %3$s to remain in the original order
- Bulgarian grammar legitimately reordered those numbered placeholders; this was not a missing/corrupted-placeholder defect
- fix commit 5a7fb08d299393de6396ef11da87019e54393954 changed the bootstrap safety check to compare the placeholder multiset, matching the strict project audit
- successful bootstrap run 34259481791 completed generation, pruning, all strict audits, validation and commit
- validated localization commit 1c008d4284804f59181700be967fae113d6dd010 ("Add Bulgarian localization fallback")
- Bulgarian audit artifact ID 10069356632; SHA256 20072eae012e71ae03ed112ae65a6a66b3e54b8664bd700852faf78909c4b9ab

Bulgarian metadata:
- synchronization run 34259841006 succeeded
- metadata commit 6d0b8604e3e319eb1f5db0dadfb25459195d4628 ("Document Bulgarian localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 23 supported locales and include Bulgarian bg_bg

Packaging hardening:
- build.gradle commit 1afb3c5f5395734db3e8f6734d91f4c9f89a9af0 ("Default 1.21 locale deltas by target")
- locale-specific 1.21.1 deltas now default to enabled only for source_variant=mc1_21_1, reducing the risk of any newly added 1.21.1 delta leaking into 26.x if a workflow omits an explicit flag

Final Bulgarian three-target CI:
- workflow: .github/workflows/build-0.9.0-bulgarian.yml
- workflow creation commit d87dbe99f5775af1793d0d07164b9d6396228e71
- run ID 34259941774: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Gradle build, exact packaging verification and JAR upload

Bulgarian packaging verified by CI:
- 1.21.1: 27 bg_bg files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 bg_bg files = 16 common + correct 26.1 delta
- 26.2: 17 bg_bg files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_bg_121 leaked into 26.x

Final Bulgarian JAR artifacts from run 34259941774:
- mc-1.21.1: artifact ID 10069493176; size 1,438,839 bytes; SHA256 dda6621a667465411c0a71c212bf7f3102bf8b940adb57a936a160dea10a9b2f
- mc-26.1.x: artifact ID 10069479486; size 647,754 bytes; SHA256 ed179aab799a2af0ba1ed37db54381b61be28124cb382606c7fd55823839293b
- mc-26.2: artifact ID 10069507375; size 647,335 bytes; SHA256 4b6f61fd7ab4344beda094e275b92c1711c7174c72e246309ba6b75ed47bfea8

'''
anchor = "11. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "11. BULGARIAN 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, bulgarian + "12. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("12. CURRENT PERMANENT CI / BUILD VALIDATION", "13. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("13. SOURCE OF TRUTH HIERARCHY", "14. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("14. QUALITY / QA CAVEAT", "15. QUALITY / QA CAVEAT", 1)
    text = text.replace("15. NEXT ACTION", "16. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 22 supported locales\n- README.md says 22 languages and includes Greek el_gr\n- Romanian and Greek have both passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 23 supported locales\n- README.md says 23 languages and includes Bulgarian bg_bg\n- Romanian, Greek and Bulgarian have passed final three-target packaging validation",
)
text = text.replace("NEXT LANGUAGE = language 23.", "NEXT LANGUAGE = language 24.")
text = text.replace("Do not stop permanently at 23;", "Do not stop permanently at 24;")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Bulgarian / language 23")
