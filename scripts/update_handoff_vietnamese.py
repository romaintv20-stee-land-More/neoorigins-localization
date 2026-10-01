#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "PROJECT_HANDOFF.txt"
text = PATH.read_text(encoding="utf-8")

text = text.replace(
    "0.9.0 development currently has 23 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg.",
    "0.9.0 development currently has 24 locales:\nfr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn.",
)
text = text.replace(
    "- 23: Bulgarian / bg_bg\n\nTWENTY-THREE IS NOT THE FINAL TARGET.",
    "- 23: Bulgarian / bg_bg\n- 24: Vietnamese / vi_vn\n\nTWENTY-FOUR IS NOT THE FINAL TARGET.",
)

vietnamese = r'''12. VIETNAMESE 0.9.0 STATUS
---------------------------
Vietnamese locale: vi_vn / Tiếng Việt.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Why selected:
- Vietnamese is an official Minecraft Java locale.
- It is a clearly distinct language and has no regional-dedup conflict with the existing 23-locale set.

Vietnamese architecture:
- 16 common namespaces: neoorigins_vi_common_01 through neoorigins_vi_common_16
- 1.21.1-specific namespace: neoorigins_vi_121
- 26.1.x uses vi_vn inside neoorigins_26_1
- 26.2 uses vi_vn inside neoorigins_26_2
- all 10 supported/licensed 1.21.1 add-ons receive vi_vn fallback files

At the audited references, NeoOrigins and ALL TEN supported add-ons had zero official Vietnamese strings. Therefore all 10 Vietnamese add-on fallback files are required.

Vietnamese coverage:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 add-ons: complete against their established effective baselines
- strict overlap audit: 0
- strict missing audit: 0
- placeholder errors: 0
- scripts/validate.py passed

Vietnamese bootstrap:
- workflow run 34261173029 succeeded completely
- validated localization commit 82b58a2a0768f133398ef7398a9a940f2b4e8103 ("Add Vietnamese localization fallback")
- Vietnamese audit artifact ID 10070026084; size 291,553 bytes; SHA256 59a6c9561387ff1285a038670a0fa74b567f0214ea9e1c9522c341517993bca2

Vietnamese metadata:
- synchronization run 34261784075 succeeded
- metadata commit ca8ae51e4db096987bbdf43fcd88a2c3b69694a0 ("Document Vietnamese localization in 0.9.0 beta")
- catalog.json / CATALOG.md / README.md now declare 24 supported locales and include Vietnamese vi_vn

Vietnamese target packaging:
- build.gradle includes include_vietnamese_121_translations
- neoorigins_vi_121 is excluded whenever the source target is not Minecraft 1.21.1

Final Vietnamese three-target CI:
- workflow: .github/workflows/build-0.9.0-vietnamese.yml
- final workflow commit 5235124c1ead8459a56c8c4f5212c8158f50c9b5
- run ID 34261836142: SUCCESS on all three jobs
- mc-1.21.1 passed strict NeoOrigins + all 10 add-on audits, JSON validation, Gradle build, exact packaging verification and JAR upload
- mc-26.1.x and mc-26.2 passed strict NeoOrigins audit, JSON validation, Gradle build, exact packaging verification and JAR upload

Vietnamese packaging verified by CI:
- 1.21.1: 27 vi_vn files = 16 common + 1 v121 delta + 10 add-ons
- 26.1.x: 17 vi_vn files = 16 common + correct 26.1 delta
- 26.2: 17 vi_vn files = 16 common + correct 26.2 delta
- no add-on namespace or neoorigins_vi_121 leaked into 26.x

Final Vietnamese JAR artifacts from run 34261836142:
- mc-1.21.1: artifact ID 10070253529; size 1,529,509 bytes; SHA256 2411bbabfe616806161a1176b028920ef65cb6c3b3cb4a6b36eb2b124eda1c73
- mc-26.1.x: artifact ID 10070224915; size 701,039 bytes; SHA256 86431a11f0e762149c3928c05258f7c9ad5a3948c328088e79913622b7cd02db
- mc-26.2: artifact ID 10070218394; size 700,664 bytes; SHA256 6a1f594f3851faecfd6859623bccad12c5035482ad0b694cc2895ab696a988ff

'''
anchor = "12. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n"
if "12. VIETNAMESE 0.9.0 STATUS" not in text:
    if anchor not in text:
        raise RuntimeError("Origin Architect section anchor missing")
    text = text.replace(anchor, vietnamese + "13. ORIGIN ARCHITECT AUDIT IMPROVEMENT\n", 1)
    text = text.replace("13. CURRENT PERMANENT CI / BUILD VALIDATION", "14. CURRENT PERMANENT CI / BUILD VALIDATION", 1)
    text = text.replace("14. SOURCE OF TRUTH HIERARCHY", "15. SOURCE OF TRUTH HIERARCHY", 1)
    text = text.replace("15. QUALITY / QA CAVEAT", "16. QUALITY / QA CAVEAT", 1)
    text = text.replace("16. NEXT ACTION", "17. NEXT ACTION", 1)

text = text.replace(
    "As of this update:\n- catalog.json says 23 supported locales\n- README.md says 23 languages and includes Bulgarian bg_bg\n- Romanian, Greek and Bulgarian have passed final three-target packaging validation",
    "As of this update:\n- catalog.json says 24 supported locales\n- README.md says 24 languages and includes Vietnamese vi_vn\n- Romanian, Greek, Bulgarian and Vietnamese have passed final three-target packaging validation",
)
text = text.replace("NEXT LANGUAGE = language 24.", "NEXT LANGUAGE = language 25.")
text = text.replace("Do not stop permanently at 24;", "Do not stop permanently at 25;")

required = [
    "0.9.0 development currently has 24 locales:",
    "- 24: Vietnamese / vi_vn",
    "12. VIETNAMESE 0.9.0 STATUS",
    "catalog.json says 24 supported locales",
    "NEXT LANGUAGE = language 25.",
]
for needle in required:
    if needle not in text:
        raise RuntimeError(f"Expected Vietnamese handoff marker missing: {needle}")

PATH.write_text(text, encoding="utf-8")
print("PROJECT_HANDOFF.txt updated for Vietnamese / language 24")
