#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

repls = {
    '0.9.0 development currently has 62 locales:': '0.9.0 development currently has 63 locales:',
    'af_za, az_az, kn_in, cv_cu, uz_uz, mt_mt, lb_lu, so_so.\n\nExpansion order so far:': 'af_za, az_az, kn_in, cv_cu, uz_uz, mt_mt, lb_lu, so_so, eo_uy.\n\nExpansion order so far:',
    '- 62: Somali / so_so\n\nSIXTY-TWO IS NOT THE FINAL TARGET.': '- 62: Somali / so_so\n- 63: Esperanto / eo_uy\n\nSIXTY-THREE IS NOT THE FINAL TARGET.',
}
for old, new in repls.items():
    if old not in text:
        raise SystemExit(f'PROJECT_HANDOFF expected text missing: {old!r}')
    text = text.replace(old, new, 1)

text = re.sub(
    r'As of this update:\n- catalog\.json says \d+ supported locales\n- README\.md says \d+ languages[^\n]*',
    'As of this update:\n- catalog.json says 63 supported locales\n- README.md says 63 languages and includes Esperanto eo_uy alongside the previously completed locales',
    text,
    count=1,
)

section = '''55. ESPERANTO 0.9.0 STATUS
----------------------------
Esperanto locale: eo_uy / Esperanto.
Minecraft Java language metadata was verified before selection and Esperanto was confirmed as a distinct current locale, not a regional variant of another supported language.

Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, AND DOCUMENTED.

Selection rationale:
- Esperanto is a distinct constructed language with its own grammar and vocabulary, not a regional duplicate of any of the first 62 supported locales.
- NeoOrigins 2.2.27 has zero official eo_uy strings on all three supported targets.
- All 10 supported 1.21.1 add-ons likewise have zero official eo_uy strings at the audited refs, therefore full low-priority fallback coverage is required.

Staging:
- branch: release/0.9.0-esperanto
- exact beta base used to create staging: 073908c30b0eb6f4d044db02e2208e4a3929ea16
- final build source SHA: ff46ada079431c58b496b5a423f44d159bde05ac

NeoOrigins pinned refs (2.2.27):
- 1.21.1: af467a3bc118f6bbc0970d68f7e03fa631d7e6f2
- 26.1.x: aa207ef14cf3b938e28b4081162701953957c1d5
- 26.2: 511cadcafe3027d2a56b4448652ec9b74e2f3b07

Architecture:
- 16 common namespaces: neoorigins_eo_common_01 through neoorigins_eo_common_16
- 1.21.1 delta namespace: neoorigins_eo_121
- 26.1.x overlay: eo_uy inside neoorigins_26_1
- 26.2 overlay: eo_uy inside neoorigins_26_2
- all 10 supported/licensed add-ons receive eo_uy fallback files on 1.21.1
- Gradle target switch: include_esperanto_121_translations / includeEsperanto121Translations

Coverage / strict audits:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- official Esperanto strings at audited refs: 0 for NeoOrigins and 0 for all 10 supported add-ons
- missing: 0
- overlap: 0
- placeholder errors: 0
- all 10 add-on audits: strict success
- scripts/validate.py: passed

Generation / bootstrap evidence:
- successful bootstrap run: 34427693801
- successful bootstrap job: 102716316421
- validated localization commit: f892066eb8202784997f2c1faa8356f319942a5c
- bootstrap/audit artifact ID: 10133339592
- bootstrap artifact ZIP SHA256: 262163d18febec0eca0786e77097c100310d61118e0d16c299d23956440a6651
- generated NeoOrigins split: 2290 common + 6 / 17 / 17 target-specific keys
- generated Esperanto files: 29 total
- generation: 19 manual/pre-seeded entries + 2715 newly translated strings in 79 batches
- title-like refinement: 196 requests in 6 batches; 152 / 199 title-like English remnants improved
- bootstrap sanity: 3636 Esperanto lexical markers, 2003 Esperanto diacritics and 103563 Latin characters across 29 files

Contextual terminology QA:
- first contextual run 34428106204 intentionally stopped on a single remaining English fragment after structural audits had already passed; no bad localization commit was integrated
- final successful refinement run: 34428286046
- refinement job: 102718101057
- refined QA artifact ID: 10133478568
- refined QA artifact ZIP SHA256: d0f20d508e9161beabf664f8e66dc8922aa9b00af7ee5a7f01c8777265e999e2
- main deterministic pass changed 406 values across 20 / 29 files and verified 109 guarded gameplay/UI keys
- observed-remnant pass applied 17 additional corrections across 4 files, verified 17 guarded keys and cleared 5 English-remnant classes
- canonical/project terminology includes Origin, Origin Creator, Mob Origin Creator and Origin Architect
- corrected gameplay/UI terminology includes Klaso, Povoj, Apliki, Generaj Reguloj, Faligaĵoj, Noktvido, Blaze-skvamoj, Skvamoj and Pavlova Reflekso
- all 64 NeoOrigins hotkeys normalized as Fulmoklavo 01 through Fulmoklavo 64
- post-refinement sanity: 3660 Esperanto lexical markers, 2018 Esperanto diacritics and 103603 Latin characters across 29 files
- all strict NeoOrigins and 10 add-on audits passed again after refinement

Metadata evidence:
- metadata run: 34428336352
- metadata job: 102718249903
- metadata commit: 9ad0ea92cfd0626c94515a0d34664301578d65dd
- catalog.json supported_locale_count = 63
- catalog.json, CATALOG.md and README.md include eo_uy / Esperanto and exact three-version coverage

Final build evidence:
- build run: 34428493073
- source SHA: ff46ada079431c58b496b5a423f44d159bde05ac
- 1.21.1 job 102718727355: success; packaging 27 / 27 eo_uy files; NeoOrigins 2296 expected / 2296 packaged / 0 duplicates
  - artifact ID 10133590817
  - JAR SHA256 79415d11b7b136965d15327eed20f11329a373f3549c6ddb73c654bd9c59b456
  - artifact ZIP SHA256 80201e09822aa1ea01325c39aa9e4eca905020649aea23d7a0949f9931569638
- 26.1.x job 102718727302: success; packaging 17 / 17 eo_uy files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10133580258
  - JAR SHA256 71769b255590bc7fd63c1bd74a541691567c7acae83054cab930a6a04c8059aa
  - artifact ZIP SHA256 693dee48783edced236b76171a29ce8a0f54f013a8fdc19c99c4b803956b738a
- 26.2 job 102718727118: success; packaging 17 / 17 eo_uy files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10133581176
  - JAR SHA256 b4e6e9fb0f991afbbd2942c324d1ee2f30e435e65c6d2c297cc9e1ed8ca1cca7
  - artifact ZIP SHA256 9f7bdb2e4670a15d95f09b8f9edc78694bcc65055f6b8d4b9347fbf4ec7a6d11

Packaging semantics verified by CI:
- 1.21.1 = 16 common + neoorigins_eo_121 + 10 add-ons = 27; no 26.x Esperanto overlays
- 26.1.x = 16 common + neoorigins_26_1 = 17; no add-ons and no neoorigins_eo_121
- 26.2 = 16 common + neoorigins_26_2 = 17; no add-ons and no neoorigins_eo_121
- packaged NeoOrigins keysets are exact, duplicate-free and target-correct

Integration discipline:
- release/0.9.0-beta must be refetched immediately before integration.
- Only fast-forward release/0.9.0-beta to the exact release/0.9.0-esperanto HEAD when compare shows staging is ahead-only and behind_by=0.
- Never force-push.
- After integration, release/0.9.0-beta and release/0.9.0-esperanto must resolve to the exact same SHA.

NEXT LANGUAGE after Esperanto = language 64.
Re-evaluate the current Minecraft Java locale inventory, choose a useful distinct locale not already in the 63-locale set, verify official upstream assets first, and apply the regional-variant dedup rule before generating fallbacks. Gallo and Võro remain candidates for re-evaluation but must not be forced through a backend that cannot meet the quality bar.

'''
marker = '55. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 63.'
if marker not in text:
    raise SystemExit('NEXT ACTION marker for language 63 missing')
text = text.replace(marker, section + '56. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 64.', 1)
text = re.sub(
    r'10\. Do not stop permanently at \d+; language expansion should continue unless Romain changes scope\.',
    '10. Do not stop permanently at 63; language expansion should continue unless Romain changes scope.',
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
- Completed language count: **63**.
- Last completed language: **#63 Esperanto — `eo_uy / Esperanto`**.
- **Do not redo Esperanto.**
- Next language: **#64**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #63 Esperanto verification

Staging branch: `release/0.9.0-esperanto`

Original beta base used for staging:
`073908c30b0eb6f4d044db02e2208e4a3929ea16`

Final build source:
`ff46ada079431c58b496b5a423f44d159bde05ac`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- official Esperanto strings upstream at audited refs: **0** for NeoOrigins and **0** for all 10 supported add-ons
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- main pass: **406 values across 20/29 files**, **109 guarded keys**
- observed pass: **17 additional corrections across 4 files**, **17 guarded keys**, **5 English-remnant classes cleared**
- final contextual sanity: **3660 lexical markers, 2018 Esperanto diacritics, 103603 Latin characters, 29 files**

Important contextual corrections include canonical `Origin`, `Klaso`, `Povoj`, `Apliki`, `Generaj Reguloj`, `Faligaĵoj`, `Noktvido`, `Blaze-skvamoj`, `Skvamoj`, `Pavlova Reflekso`, and all 64 `Fulmoklavo` hotkeys. Do not revert these to raw machine translations such as `Origino`, `Potencoj`, `Nokta vizio`, `Skaloj/pesiloj`, `Pavloved` or English `Hotkey` labels.

## Runs and artifacts

Bootstrap:
- run `34427693801`
- job `102716316421`
- localization commit `f892066eb8202784997f2c1faa8356f319942a5c`
- artifact `10133339592`
- artifact ZIP SHA256 `262163d18febec0eca0786e77097c100310d61118e0d16c299d23956440a6651`

Contextual refinement:
- final successful run `34428286046`
- job `102718101057`
- artifact `10133478568`
- artifact ZIP SHA256 `d0f20d508e9161beabf664f8e66dc8922aa9b00af7ee5a7f01c8777265e999e2`

Metadata:
- run `34428336352`
- job `102718249903`
- commit `9ad0ea92cfd0626c94515a0d34664301578d65dd`
- catalog locale count **63**

Final builds — run `34428493073`, source `ff46ada079431c58b496b5a423f44d159bde05ac`:
- 1.21.1 job `102718727355`, artifact `10133590817`, package **27/27**, JAR SHA256 `79415d11b7b136965d15327eed20f11329a373f3549c6ddb73c654bd9c59b456`, ZIP SHA256 `80201e09822aa1ea01325c39aa9e4eca905020649aea23d7a0949f9931569638`
- 26.1.x job `102718727302`, artifact `10133580258`, package **17/17**, JAR SHA256 `71769b255590bc7fd63c1bd74a541691567c7acae83054cab930a6a04c8059aa`, ZIP SHA256 `693dee48783edced236b76171a29ce8a0f54f013a8fdc19c99c4b803956b738a`
- 26.2 job `102718727118`, artifact `10133581176`, package **17/17**, JAR SHA256 `b4e6e9fb0f991afbbd2942c324d1ee2f30e435e65c6d2c297cc9e1ed8ca1cca7`, ZIP SHA256 `9f7bdb2e4670a15d95f09b8f9edc78694bcc65055f6b8d4b9347fbf4ec7a6d11`

Packaging semantics:
- 1.21.1: 16 common + `neoorigins_eo_121` + 10 add-ons = **27** Esperanto files
- 26.1.x: 16 common + `neoorigins_26_1` = **17** Esperanto files
- 26.2: 16 common + `neoorigins_26_2` = **17** Esperanto files
- no wrong-version overlays or add-ons leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

## Start of language #64

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule. Gallo and Võro may be re-evaluated, but do not force a locale through a backend that cannot meet the quality bar.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
'''
(ROOT / 'NEXT_CHAT_HANDOFF.md').write_text(next_chat, encoding='utf-8')
print('Esperanto handoffs prepared: project count 63, next language 64.')
