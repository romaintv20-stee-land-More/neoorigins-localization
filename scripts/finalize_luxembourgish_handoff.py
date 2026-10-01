#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

repls = {
    '0.9.0 development currently has 60 locales:': '0.9.0 development currently has 61 locales:',
    'af_za, az_az, kn_in, cv_cu, uz_uz, mt_mt.\n\nExpansion order so far:': 'af_za, az_az, kn_in, cv_cu, uz_uz, mt_mt, lb_lu.\n\nExpansion order so far:',
    '- 60: Maltese / mt_mt\n\nSIXTY IS NOT THE FINAL TARGET.': '- 60: Maltese / mt_mt\n- 61: Luxembourgish / lb_lu\n\nSIXTY-ONE IS NOT THE FINAL TARGET.',
}
for old, new in repls.items():
    if old not in text:
        raise SystemExit(f'PROJECT_HANDOFF expected text missing: {old!r}')
    text = text.replace(old, new, 1)

text = re.sub(
    r'As of this update:\n- catalog\.json says \d+ supported locales\n- README\.md says \d+ languages[^\n]*',
    'As of this update:\n- catalog.json says 61 supported locales\n- README.md says 61 languages and includes Luxembourgish lb_lu alongside the previously completed locales',
    text,
    count=1,
)

section = '''53. LUXEMBOURGISH 0.9.0 STATUS
---------------------------------
Luxembourgish locale: lb_lu / Lëtzebuergesch.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, AND DOCUMENTED.

Selection rationale:
- Luxembourgish is a Minecraft Java locale and a distinct language, not a regional near-duplicate of another supported locale.
- NeoOrigins 2.2.27 has no official lb_lu file on any of the three supported refs, so the complete low-priority fallback is required.
- Minecraft terminology was checked against current Luxembourgish assets; use Nuechtsiicht for Night Vision and Netherit for Netherite.

Staging:
- branch: release/0.9.0-luxembourgish
- exact beta base used to create staging: 5f24096a3e6dece302dc2a31f254c7c79a5c8617
- final build source SHA: 24c15ad7a25dfc49b1ecb9ef412ba9c959f59603

NeoOrigins pinned refs (2.2.27):
- 1.21.1: af467a3bc118f6bbc0970d68f7e03fa631d7e6f2
- 26.1.x: aa207ef14cf3b938e28b4081162701953957c1d5
- 26.2: 511cadcafe3027d2a56b4448652ec9b74e2f3b07

Architecture:
- 16 common namespaces: neoorigins_lb_common_01 through neoorigins_lb_common_16
- 1.21.1 delta namespace: neoorigins_lb_121
- 26.1.x overlay: lb_lu inside neoorigins_26_1
- 26.2 overlay: lb_lu inside neoorigins_26_2
- all 10 supported/licensed add-ons receive lb_lu fallback files on 1.21.1
- Gradle target switch: include_luxembourgish_121_translations / includeLuxembourgish121Translations

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
- successful bootstrap run: 34410661769
- successful bootstrap job: 102664059776
- bootstrap/audit artifact ID: 10127180809
- bootstrap artifact ZIP SHA256: 6f627287d08267ee33b83b513cececa0ec4cd5d5a87da07984890784f4ec7451
- generated NeoOrigins split: 2290 common + 6 / 17 / 17 target-specific keys
- generated Luxembourgish files: 29 total
- initial sanity: 3406 lexical markers, 3967 accented letters and 108896 Latin characters

Contextual terminology QA:
- deterministic refinement run: 34411346403
- refinement job: 102666222361
- refined QA artifact ID: 10127342267
- refined QA artifact ZIP SHA256: 4ad9bcbf2b5bbcb30db51f187b931df93221591bb250f8b39397585c3494b241
- 419 values corrected across 25 / 29 files; 86 guarded gameplay/UI keys verified
- canonical project/game terminology includes Origin, Origin Creator, Mob Origin Creator, Origin Architect, Klass and Fäegkeeten
- current Minecraft terminology includes Nuechtsiicht and Netherit
- corrected contextual terms include Spawn-Reegelen, Schuppen and Pavlov-Reaktioun
- all 64 NeoOrigins hotkeys normalized as Schnelltast 01 through Schnelltast 64
- post-refinement sanity: 3433 lexical markers and 3980 accented letters across 29 files
- all strict NeoOrigins and 10 add-on audits passed again after refinement

Metadata evidence:
- metadata run: 34411488196
- metadata job: 102666643265
- metadata commit: d31a9a49972bf4549d5bf0b90fc3930c1c5d80f0
- catalog.json supported_locale_count = 61
- catalog.json, CATALOG.md and README.md include lb_lu / Lëtzebuergesch / Luxembourgeois and exact three-version coverage
- stale README Czech/Hungarian historical partial-coverage wording was corrected to the already-recovered full coverage

Final build evidence:
- build run: 34411581514
- source SHA: 24c15ad7a25dfc49b1ecb9ef412ba9c959f59603
- 1.21.1 job 102666974306: success; packaging 27 / 27 lb_lu files; NeoOrigins 2296 expected / 2296 packaged / 0 duplicates
  - artifact ID 10127486985
  - JAR SHA256 13a4193011778e243d4003f8f7acfaf3979df5dbc44c64e779abb22da65974c3
  - artifact ZIP SHA256 c5206533df99d25d10d1bc787d87d3efad9c353dbd21d1a917067be30e5ac0ee
- 26.1.x job 102666974486: success; packaging 17 / 17 lb_lu files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10127468957
  - JAR SHA256 1f1f6e49f32c3127b27fe2a795f4a9c958b2173bf3a433058777c93eb7384f4a
  - artifact ZIP SHA256 8172094b25b4fcde7aa2701ba4a863f00e6f2cb5b923d00b08a2905d1bae542a
- 26.2 job 102666974466: success; packaging 17 / 17 lb_lu files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10127470282
  - JAR SHA256 554e1159fbfbc2dba1978976dbc6b9ab60825c86ae252ca26ea055bdb2ef82ec
  - artifact ZIP SHA256 315e33c93a8b107b5c3c74286b3c8d3878df8cbafb66eca8974de0db3e3d1eda

Packaging semantics verified by CI:
- 1.21.1 = 16 common + neoorigins_lb_121 + 10 add-ons = 27; no 26.x Luxembourgish overlays
- 26.1.x = 16 common + neoorigins_26_1 = 17; no add-ons and no neoorigins_lb_121
- 26.2 = 16 common + neoorigins_26_2 = 17; no add-ons and no neoorigins_lb_121
- packaged NeoOrigins keys are unique and exactly equal to each target's English-minus-official required keyset

Integration discipline:
- release/0.9.0-beta must be refetched immediately before integration.
- Only fast-forward release/0.9.0-beta to the exact release/0.9.0-luxembourgish HEAD when compare shows staging is ahead-only and behind_by=0.
- Never force-push.
- After integration, release/0.9.0-beta and release/0.9.0-luxembourgish must resolve to the exact same SHA.

NEXT LANGUAGE after Luxembourgish = language 62.
Re-evaluate the current Minecraft Java locale inventory, choose a useful distinct locale not already in the 61-locale set, verify official upstream assets first, and apply the regional-variant dedup rule before generating fallbacks.

'''
marker = '53. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 61.'
if marker not in text:
    raise SystemExit('NEXT ACTION marker for language 61 missing')
text = text.replace(marker, section + '54. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 62.', 1)
text = text.replace('10. Do not stop permanently at 60; language expansion should continue unless Romain changes scope.',
                    '10. Do not stop permanently at 61; language expansion should continue unless Romain changes scope.')
p.write_text(text, encoding='utf-8')

next_chat = '''# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **61**.
- Last completed language: **#61 Luxembourgish / Luxembourgeois — `lb_lu / Lëtzebuergesch`**.
- **Do not redo Luxembourgish.**
- Next language: **#62**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #61 Luxembourgish verification

Staging branch: `release/0.9.0-luxembourgish`

Original beta base used for staging:
`5f24096a3e6dece302dc2a31f254c7c79a5c8617`

Final build source:
`24c15ad7a25dfc49b1ecb9ef412ba9c959f59603`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- final contextual sanity: **3433 Luxembourgish lexical markers, 3980 accented letters, 29 files**

Important contextual corrections include canonical `Origin` terminology, `Klass`, `Fäegkeeten`, `Spawn-Reegelen`, Minecraft `Nuechtsiicht` and `Netherit`, `Schuppen`, `Pavlov-Reaktioun`, and 64 normalized `Schnelltast` hotkeys. Do not revert these to raw machine translations such as `Urspronk`, `Hierkonft`, `Muechten`, `Nuecht Visioun`, `Skalen` or `Pavloved`.

## Runs and artifacts

Bootstrap:
- run `34410661769`
- job `102664059776`
- artifact `10127180809`
- artifact ZIP SHA256 `6f627287d08267ee33b83b513cececa0ec4cd5d5a87da07984890784f4ec7451`

Contextual refinement:
- run `34411346403`
- job `102666222361`
- artifact `10127342267`
- artifact ZIP SHA256 `4ad9bcbf2b5bbcb30db51f187b931df93221591bb250f8b39397585c3494b241`
- 419 values changed across 25/29 files; 86 guarded keys

Metadata:
- run `34411488196`
- job `102666643265`
- commit `d31a9a49972bf4549d5bf0b90fc3930c1c5d80f0`
- catalog locale count **61**

Final builds — run `34411581514`, source `24c15ad7a25dfc49b1ecb9ef412ba9c959f59603`:
- 1.21.1 job `102666974306`, artifact `10127486985`, package **27/27**, JAR SHA256 `13a4193011778e243d4003f8f7acfaf3979df5dbc44c64e779abb22da65974c3`, ZIP SHA256 `c5206533df99d25d10d1bc787d87d3efad9c353dbd21d1a917067be30e5ac0ee`
- 26.1.x job `102666974486`, artifact `10127468957`, package **17/17**, JAR SHA256 `1f1f6e49f32c3127b27fe2a795f4a9c958b2173bf3a433058777c93eb7384f4a`, ZIP SHA256 `8172094b25b4fcde7aa2701ba4a863f00e6f2cb5b923d00b08a2905d1bae542a`
- 26.2 job `102666974466`, artifact `10127470282`, package **17/17**, JAR SHA256 `554e1159fbfbc2dba1978976dbc6b9ab60825c86ae252ca26ea055bdb2ef82ec`, ZIP SHA256 `315e33c93a8b107b5c3c74286b3c8d3878df8cbafb66eca8974de0db3e3d1eda`

## Start of language #62

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
'''
(ROOT / 'NEXT_CHAT_HANDOFF.md').write_text(next_chat, encoding='utf-8')
print('Luxembourgish handoff finalized: 61 completed locales; next language 62.')
