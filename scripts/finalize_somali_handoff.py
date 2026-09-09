#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

repls = {
    'Last updated: 2026-09-09': 'Last updated: 2026-09-10',
    '0.9.0 development currently has 61 locales:': '0.9.0 development currently has 62 locales:',
    'af_za, az_az, kn_in, cv_cu, uz_uz, mt_mt, lb_lu.\n\nExpansion order so far:': 'af_za, az_az, kn_in, cv_cu, uz_uz, mt_mt, lb_lu, so_so.\n\nExpansion order so far:',
    '- 61: Luxembourgish / lb_lu\n\nSIXTY-ONE IS NOT THE FINAL TARGET.': '- 61: Luxembourgish / lb_lu\n- 62: Somali / so_so\n\nSIXTY-TWO IS NOT THE FINAL TARGET.',
}
for old, new in repls.items():
    if old not in text:
        raise SystemExit(f'PROJECT_HANDOFF expected text missing: {old!r}')
    text = text.replace(old, new, 1)

text = re.sub(
    r'As of this update:\n- catalog\.json says \d+ supported locales\n- README\.md says \d+ languages[^\n]*',
    'As of this update:\n- catalog.json says 62 supported locales\n- README.md says 62 languages and includes Somali so_so alongside the previously completed locales',
    text,
    count=1,
)

section = '''54. SOMALI 0.9.0 STATUS
-------------------------
Somali locale: so_so / Soomaali.
Minecraft Java 26.2 language metadata verified before selection:
- language.code: som_SO
- language.name: Soomaali
- language.region: Soomaaliya

Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, AND DOCUMENTED.

Selection rationale:
- Somali is a current Minecraft Java locale and a distinct Cushitic language.
- It is not a regional near-duplicate of any of the first 61 supported locales.
- NeoOrigins 2.2.27 has no official so_so strings on any supported target, and all 10 supported 1.21.1 add-ons likewise have zero official Somali strings at the audited refs; therefore a complete low-priority fallback is required.
- Official Minecraft Somali terminology was checked before refinement; Aragtida Habeenka is retained for Night Vision while project/product terms such as Origin remain canonical where appropriate.

Staging:
- branch: release/0.9.0-somali
- exact beta base used to create staging: 6bd58c02c2b8e543d8497c3ddd852d04eb55ae92
- final build source SHA: 4ef3c76ee4eb90410a4290b762f878a904fbeba4

NeoOrigins pinned refs (2.2.27):
- 1.21.1: af467a3bc118f6bbc0970d68f7e03fa631d7e6f2
- 26.1.x: aa207ef14cf3b938e28b4081162701953957c1d5
- 26.2: 511cadcafe3027d2a56b4448652ec9b74e2f3b07

Architecture:
- 16 common namespaces: neoorigins_so_common_01 through neoorigins_so_common_16
- 1.21.1 delta namespace: neoorigins_so_121
- 26.1.x overlay: so_so inside neoorigins_26_1
- 26.2 overlay: so_so inside neoorigins_26_2
- all 10 supported/licensed add-ons receive so_so fallback files on 1.21.1
- Gradle target switch: include_somali_121_translations / includeSomali121Translations

Coverage / strict audits:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- missing: 0
- overlap: 0
- placeholder errors: 0
- all 10 add-on audits: 0 missing / 0 overlap / 0 placeholder errors
- scripts/validate.py: passed

Generation / bootstrap evidence:
- first bootstrap run 34413792449 stopped after upstream discovery because Google Translate altered a Unicode placeholder mask; no localization data from that failed generation was integrated
- placeholder protection was switched to the proven ASCII-safe mechanism
- successful bootstrap run: 34413860883
- successful bootstrap job: 102674182234
- bootstrap/audit artifact ID: 10128350400
- bootstrap artifact ZIP SHA256: da94f6b6f5f3a540e53f8edfcaf24a40da7fda8cef961b895a70c9cff74ad6d8
- generated NeoOrigins split: 2290 common + 6 / 17 / 17 target-specific keys
- generated Somali files: 29 total
- generation: 19 manual/pre-seeded entries + 2715 newly translated strings in 79 batches
- title-like refinement: 245 requests; 152 / 248 title-like English remnants improved
- bootstrap sanity: 4993 Somali lexical markers, 8075 Somali orthographic markers, 121181 Latin characters across 29 files

Contextual terminology QA:
- deterministic refinement run: 34414360770
- refinement job: 102675774018
- refined QA artifact ID: 10128462525
- refined QA artifact ZIP SHA256: 4ef12306f208c8154ca9afe5a4e54f0585e9abce8f378d4d1ec1befb145eaabc
- 395 values corrected across 20 / 29 files; 109 guarded gameplay/UI keys verified
- branded/project terminology keeps Origin canonical where appropriate
- corrected gameplay/UI terminology includes Fasal, Awoodaha, Dhaqan geli, Xeerarka Dhalashada, Aragtida Habeenka, Qolofyada Blaze, anatomical Qolofyo and Falcelinta Pavlov
- all 64 NeoOrigins hotkeys normalized as Furaha Degdegga ah 01 through Furaha Degdegga ah 64
- post-refinement sanity: 4524 Somali lexical markers, 8086 Somali orthographic markers and 121946 Latin characters across 29 files
- all strict NeoOrigins and 10 add-on audits passed again after refinement

Metadata evidence:
- metadata run: 34414607834
- metadata job: 102676559755
- metadata commit: 523e495f64a90f32cf166fd7f6d87ee2d60dda1a
- catalog.json supported_locale_count = 62
- catalog.json, CATALOG.md and README.md include so_so / Soomaali / Somali and exact three-version coverage

Final build evidence:
- build run: 34414684602
- source SHA: 4ef3c76ee4eb90410a4290b762f878a904fbeba4
- 1.21.1 job 102676812909: success; packaging 27 / 27 so_so files; NeoOrigins 2296 expected / 2296 packaged / 0 duplicates
  - artifact ID 10128628531
  - JAR SHA256 1380b3b6ca0c2fad4f4ac399fd99858be81360895fdda9cf49b81d955e4ad682
  - artifact ZIP SHA256 92b75187336e45187a12d1848285be8eddae970829dc6f43cd7916d6d79de092
- 26.1.x job 102676812737: success; packaging 17 / 17 so_so files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10128619805
  - JAR SHA256 2c25043e0c71aed732445e649f32ba4a825da96bd5f86875083daa8d81673b7a
  - artifact ZIP SHA256 b388eb7155a55945791efac7fd39b7b1ee552915fd19fada0916ed86a18b912e
- 26.2 job 102676812914: success; packaging 17 / 17 so_so files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10128622615
  - JAR SHA256 f99577159cc34c22b21f15fec69e4d96569d030c2cca426495ddfa50f4b32c45
  - artifact ZIP SHA256 337e753ed7477f526825468a547412bd2770b351bd034eeb77bc93fdbdecc888

Packaging semantics verified by CI:
- 1.21.1 = 16 common + neoorigins_so_121 + 10 add-ons = 27; no 26.x Somali overlays
- 26.1.x = 16 common + neoorigins_26_1 = 17; no add-ons and no neoorigins_so_121
- 26.2 = 16 common + neoorigins_26_2 = 17; no add-ons and no neoorigins_so_121
- packaged NeoOrigins keys are unique and exactly equal to each target's English-minus-official required keyset

Integration discipline:
- release/0.9.0-beta must be refetched immediately before integration.
- Only fast-forward release/0.9.0-beta to the exact release/0.9.0-somali HEAD when compare shows staging is ahead-only and behind_by=0.
- Never force-push.
- After integration, release/0.9.0-beta and release/0.9.0-somali must resolve to the exact same SHA.

NEXT LANGUAGE after Somali = language 63.
Re-evaluate the current Minecraft Java locale inventory, choose a useful distinct locale not already in the 62-locale set, verify official upstream assets first, and apply the regional-variant dedup rule before generating fallbacks. Gallo and Võro may be re-evaluated; prior backend quality issues are not permanent exclusions.

'''
marker = '54. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 62.'
if marker not in text:
    raise SystemExit('NEXT ACTION marker for language 62 missing')
text = text.replace(marker, section + '55. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 63.', 1)

text = re.sub(
    r'10\. Do not stop permanently at \d+; language expansion should continue unless Romain changes scope\.',
    '10. Do not stop permanently at 62; language expansion should continue unless Romain changes scope.',
    text,
    count=1,
)

p.write_text(text, encoding='utf-8')

next_chat = '''# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **62**.
- Last completed language: **#62 Somali — `so_so / Soomaali`**.
- **Do not redo Somali.**
- Next language: **#63**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #62 Somali verification

Staging branch: `release/0.9.0-somali`

Original beta base used for staging:
`6bd58c02c2b8e543d8497c3ddd852d04eb55ae92`

Final build source:
`4ef3c76ee4eb90410a4290b762f878a904fbeba4`

Minecraft Java 26.2 metadata verified before selection:
- code `som_SO`
- name `Soomaali`
- region `Soomaaliya`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- official Somali strings upstream at audited refs: **0** for NeoOrigins and **0** for all 10 supported add-ons
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- refinement changed **395 values across 20/29 files**, with **109 guarded keys**
- final contextual sanity: **4524 lexical markers, 8086 orthographic markers, 121946 Latin characters, 29 files**

Important contextual corrections include canonical `Origin`, `Fasal`, `Awoodaha`, `Dhaqan geli`, `Xeerarka Dhalashada`, `Aragtida Habeenka`, `Qolofyada Blaze`, anatomical `Qolofyo`, `Falcelinta Pavlov`, and all 64 `Furaha Degdegga ah` hotkeys. Do not revert these to raw machine translations.

## Runs and artifacts

Bootstrap:
- first generation run `34413792449` failed only because the translation service altered a Unicode placeholder sentinel; no failed localization output was integrated
- successful run `34413860883`
- job `102674182234`
- artifact `10128350400`
- artifact ZIP SHA256 `da94f6b6f5f3a540e53f8edfcaf24a40da7fda8cef961b895a70c9cff74ad6d8`

Contextual refinement:
- run `34414360770`
- job `102675774018`
- artifact `10128462525`
- artifact ZIP SHA256 `4ef12306f208c8154ca9afe5a4e54f0585e9abce8f378d4d1ec1befb145eaabc`
- 395 values changed across 20/29 files; 109 guarded keys

Metadata:
- run `34414607834`
- job `102676559755`
- commit `523e495f64a90f32cf166fd7f6d87ee2d60dda1a`
- catalog locale count **62**

Final builds — run `34414684602`, source `4ef3c76ee4eb90410a4290b762f878a904fbeba4`:
- 1.21.1 job `102676812909`, artifact `10128628531`, package **27/27**, JAR SHA256 `1380b3b6ca0c2fad4f4ac399fd99858be81360895fdda9cf49b81d955e4ad682`, ZIP SHA256 `92b75187336e45187a12d1848285be8eddae970829dc6f43cd7916d6d79de092`
- 26.1.x job `102676812737`, artifact `10128619805`, package **17/17**, JAR SHA256 `2c25043e0c71aed732445e649f32ba4a825da96bd5f86875083daa8d81673b7a`, ZIP SHA256 `b388eb7155a55945791efac7fd39b7b1ee552915fd19fada0916ed86a18b912e`
- 26.2 job `102676812914`, artifact `10128622615`, package **17/17**, JAR SHA256 `f99577159cc34c22b21f15fec69e4d96569d030c2cca426495ddfa50f4b32c45`, ZIP SHA256 `337e753ed7477f526825468a547412bd2770b351bd034eeb77bc93fdbdecc888`

Packaging semantics:
- 1.21.1: 16 common + `neoorigins_so_121` + 10 add-ons = **27** Somali files
- 26.1.x: 16 common + `neoorigins_26_1` = **17** Somali files
- 26.2: 16 common + `neoorigins_26_2` = **17** Somali files
- no wrong-version overlays or add-ons leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

## Start of language #63

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule. Gallo and Võro can be reconsidered, but do not force a locale through a backend that cannot meet the quality bar.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
'''
(ROOT / 'NEXT_CHAT_HANDOFF.md').write_text(next_chat, encoding='utf-8')
print('Somali handoffs prepared: 62 completed languages; next language 63.')
