#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

repls = {
    '0.9.0 development currently has 59 locales:': '0.9.0 development currently has 60 locales:',
    'af_za, az_az, kn_in, cv_cu, uz_uz.\n\nExpansion order so far:': 'af_za, az_az, kn_in, cv_cu, uz_uz, mt_mt.\n\nExpansion order so far:',
    '- 59: Uzbek / uz_uz\n\nFIFTY-NINE IS NOT THE FINAL TARGET.': '- 59: Uzbek / uz_uz\n- 60: Maltese / mt_mt\n\nSIXTY IS NOT THE FINAL TARGET.',
}
for old, new in repls.items():
    if old not in text:
        raise SystemExit(f'PROJECT_HANDOFF expected text missing: {old!r}')
    text = text.replace(old, new, 1)

# Keep the current-state summary honest even though the historical language
# sections below deliberately retain their original counts.
text = re.sub(
    r'As of this update:\n- catalog\.json says \d+ supported locales\n- README\.md says \d+ languages[^\n]*',
    'As of this update:\n- catalog.json says 60 supported locales\n- README.md says 60 languages and includes Maltese mt_mt alongside the previously completed locales',
    text,
    count=1,
)

section = '''52. MALTESE 0.9.0 STATUS
--------------------------
Maltese locale: mt_mt / Malti.
Minecraft Java 26.2 language metadata verified before selection:
- language.code: mlt_MT
- language.name: Malti
- language.region: Malta

Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, AND DOCUMENTED.

Selection rationale:
- Maltese is a current Minecraft Java locale and a distinct Semitic language with substantial Romance influence.
- It is not a regional near-duplicate of any of the first 59 locales.
- NeoOrigins 2.2.27 has no official mt_mt file on any of the three supported targets, so a complete low-priority fallback is required.
- Gallo was evaluated first for language 60, but the current generation backend did not support it cleanly enough for this project's quality bar; Maltese was therefore selected instead. Re-evaluate Gallo and other remaining Minecraft locales later rather than assuming they are permanently excluded.

Staging:
- branch: release/0.9.0-maltese
- exact beta base used to create staging: 0f6703ced765303ad088077322ec55fd5e02fc00
- final build source SHA: 39a3582a22c42295e234c5e15755432025c451b1

NeoOrigins pinned refs (2.2.27):
- 1.21.1: af467a3bc118f6bbc0970d68f7e03fa631d7e6f2
- 26.1.x: aa207ef14cf3b938e28b4081162701953957c1d5
- 26.2: 511cadcafe3027d2a56b4448652ec9b74e2f3b07

Architecture:
- 16 common namespaces: neoorigins_mt_common_01 through neoorigins_mt_common_16
- 1.21.1 delta namespace: neoorigins_mt_121
- 26.1.x overlay: mt_mt inside neoorigins_26_1
- 26.2 overlay: mt_mt inside neoorigins_26_2
- all 10 supported/licensed add-ons receive mt_mt fallback files on 1.21.1
- Gradle target switch: include_maltese_121_translations / includeMaltese121Translations

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
- successful bootstrap run: 34406636751
- successful bootstrap job: 102651062952
- validated localization commit: c7300873568abb27055fd9bd6f98d41be1fba59b
- bootstrap/audit artifact ID: 10125673999
- bootstrap artifact ZIP SHA256: 5bd0359ed2f58ccddd72e6bf2404b88c1d6a4641c11560f1023f58ec41cae9c6
- generated NeoOrigins split: 2290 common + 6 / 17 / 17 target-specific keys
- generated Maltese files: 29 total
- generation: 19 manual/pre-seeded entries + 2715 newly translated strings in 79 batches
- title-like refinement: 393 requests in 12 batches; 186 / 396 title-like English remnants improved
- bootstrap sanity: 1764 Maltese lexical markers, 8309 Maltese-specific letters, 107040 Latin characters across 29 files

Contextual terminology QA:
- deterministic refinement run: 34407239933
- refinement job: 102653050567
- refinement commit: f8027a0a568436306b8dfe49c80de053bebd3087
- refined QA artifact ID: 10125799887
- refined QA artifact ZIP SHA256: 9632df91f29ed37ccc3b25fb7cf78a29e86e01e8f5785d381413ddda53d64cfa
- 189 values corrected across 20 / 29 files; 86 guarded gameplay/UI keys verified
- current Minecraft Maltese terminology was preferred where applicable, including Viżjoni bil-Lejl, Nether, Netherit and Tfaċċar terminology
- branded/project terms Origin, Origin Creator, Mob Origin Creator and Origin Architect remain canonical
- corrected gameplay terms include Klassi, Setgħat, Applika, Regoli tat-Tfaċċar, Oġġetti Mwaqqgħin, anatomical Skaldi, Reazzjoni ta' Pavlov and multiple Origins Furries false friends
- all 64 NeoOrigins hotkeys normalized as Tast Rapidu 01 through Tast Rapidu 64
- post-refinement sanity: 1688 lexical markers and 8320 Maltese-specific letters
- all strict NeoOrigins and 10 add-on audits passed again after refinement

Metadata evidence:
- metadata run: 34407430131
- metadata job: 102653676489
- metadata commit: 27e214a33031cac3e5c9ed46cbfc7ed68d61b985
- catalog.json supported_locale_count = 60
- catalog.json, CATALOG.md and README.md include mt_mt / Malti / Maltais and exact three-version coverage
- README historical seven-locale recovery wording was corrected so those 2.2.27 gaps are no longer presented as pending

Final build evidence:
- build run: 34407512286
- source SHA: 39a3582a22c42295e234c5e15755432025c451b1
- 1.21.1 job 102653926878: success; packaging 27 / 27 mt_mt files; NeoOrigins 2296 expected / 2296 packaged / 0 duplicates
  - artifact ID 10125950371
  - JAR SHA256 3d2b68ab100b8b5e165c6a3d2b98f57832892a782cdf5f9c2dd36c9a8cd7acb8
  - artifact ZIP SHA256 5d4660b592ad03808dafcf35fe549976ac350f7f7a7afd267df991223ab7b177
- 26.1.x job 102653926601: success; packaging 17 / 17 mt_mt files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10125943701
  - JAR SHA256 5844a019c1880a952d87931c59f5199cc8de15307d8871b9cbc634d9ea156ef5
  - artifact ZIP SHA256 a00972479da98c3942ee4258aa5a7e2710f40632ef1f31699d67f06e99001dc8
- 26.2 job 102653926923: success; packaging 17 / 17 mt_mt files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10125933334
  - JAR SHA256 8bb11b21929a97e35fda0c8922d3369592b47931767620a349052f8b705685b8
  - artifact ZIP SHA256 5f1fb924f42a6677d986427570d978ca140ee6bd3d9b6b8c43a56b0348a965ad

Packaging semantics verified by CI:
- 1.21.1 = 16 common + neoorigins_mt_121 + 10 add-ons = 27; no 26.x Maltese overlays
- 26.1.x = 16 common + neoorigins_26_1 = 17; no add-ons and no neoorigins_mt_121
- 26.2 = 16 common + neoorigins_26_2 = 17; no add-ons and no neoorigins_mt_121
- packaged NeoOrigins keys are unique and exactly equal to each target's English-minus-official required keyset

Integration discipline:
- release/0.9.0-beta must be refetched immediately before integration.
- Only fast-forward release/0.9.0-beta to the exact release/0.9.0-maltese HEAD when compare shows staging is ahead-only and behind_by=0.
- Never force-push.
- After integration, release/0.9.0-beta and release/0.9.0-maltese must resolve to the exact same SHA.

NEXT LANGUAGE after Maltese = language 61.
Re-evaluate the current Minecraft Java locale inventory, choose a useful distinct locale not already in the 60-locale set, verify official upstream assets first, and apply the regional-variant dedup rule before generating fallbacks.

'''
marker = '52. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 60.'
if marker not in text:
    raise SystemExit('NEXT ACTION marker for language 60 missing')
text = text.replace(marker, section + '53. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 61.', 1)

# Update only the final operational instruction block; historical sections retain their contemporaneous numbers.
text = text.replace('10. Do not stop permanently at 58; language expansion should continue unless Romain changes scope.',
                    '10. Do not stop permanently at 60; language expansion should continue unless Romain changes scope.')

p.write_text(text, encoding='utf-8')

next_chat = '''# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **60**.
- Last completed language: **#60 Maltese / Maltais — `mt_mt / Malti`**.
- **Do not redo Maltese.**
- Next language: **#61**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #60 Maltese verification

Staging branch: `release/0.9.0-maltese`

Original beta base used for staging:
`0f6703ced765303ad088077322ec55fd5e02fc00`

Final build source:
`39a3582a22c42295e234c5e15755432025c451b1`

Minecraft Java 26.2 metadata verified before selection:
- code `mlt_MT`
- name `Malti`
- region `Malta`

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
- final contextual sanity: **1688 Maltese lexical markers, 8320 Maltese-specific letters, 29 files**

Important contextual corrections include branded `Origin` terminology, `Klassi`, `Setgħat`, `Applika`, `Regoli tat-Tfaċċar`, `Oġġetti Mwaqqgħin`, official-style `Viżjoni bil-Lejl`, Nether/Netherit, anatomical `Skaldi`, `Reazzjoni ta' Pavlov`, multiple Origins Furries false friends and 64 normalized `Tast Rapidu` hotkeys. Do not revert these to raw machine translations.

Gallo `go_fr` was considered first for #60 because it is a current Minecraft locale, but the current generation backend did not support it cleanly enough for the project's quality bar. This is not a permanent exclusion: re-evaluate Gallo, Võro and the full remaining current Java locale inventory for future languages.

## Runs, commits and artifacts

Bootstrap:
- successful run `34406636751`
- job `102651062952`
- localization commit `c7300873568abb27055fd9bd6f98d41be1fba59b`
- artifact `10125673999`
- artifact ZIP SHA256 `5bd0359ed2f58ccddd72e6bf2404b88c1d6a4641c11560f1023f58ec41cae9c6`

Contextual refinement:
- run `34407239933`
- job `102653050567`
- commit `f8027a0a568436306b8dfe49c80de053bebd3087`
- artifact `10125799887`
- artifact ZIP SHA256 `9632df91f29ed37ccc3b25fb7cf78a29e86e01e8f5785d381413ddda53d64cfa`
- 189 values changed across 20/29 files; 86 guarded keys

Metadata:
- run `34407430131`
- job `102653676489`
- commit `27e214a33031cac3e5c9ed46cbfc7ed68d61b985`
- catalog locale count **60**

Final builds — run `34407512286`, source `39a3582a22c42295e234c5e15755432025c451b1`:
- 1.21.1 job `102653926878`, artifact `10125950371`, package **27/27**, JAR SHA256 `3d2b68ab100b8b5e165c6a3d2b98f57832892a782cdf5f9c2dd36c9a8cd7acb8`, ZIP SHA256 `5d4660b592ad03808dafcf35fe549976ac350f7f7a7afd267df991223ab7b177`
- 26.1.x job `102653926601`, artifact `10125943701`, package **17/17**, JAR SHA256 `5844a019c1880a952d87931c59f5199cc8de15307d8871b9cbc634d9ea156ef5`, ZIP SHA256 `a00972479da98c3942ee4258aa5a7e2710f40632ef1f31699d67f06e99001dc8`
- 26.2 job `102653926923`, artifact `10125933334`, package **17/17**, JAR SHA256 `8bb11b21929a97e35fda0c8922d3369592b47931767620a349052f8b705685b8`, ZIP SHA256 `5f1fb924f42a6677d986427570d978ca140ee6bd3d9b6b8c43a56b0348a965ad`

The build verifier opened each JAR, merged all Maltese NeoOrigins files, rejected duplicate keys and required the packaged keyset to equal the exact target English-minus-official set.

## Starting #61

Before doing anything:
1. Refetch the exact current HEAD of `release/0.9.0-beta`.
2. Verify this handoff and `PROJECT_HANDOFF.txt` agree with the repository state.
3. Re-evaluate the full current Minecraft Java locale inventory and choose a useful distinct language not already in the 60-locale set; do not assume a locale code or that the next candidate must be Gallo.
4. Verify current Minecraft language assets and official NeoOrigins/add-on translations before fallbacks.
5. Create the #61 staging branch from the exact beta HEAD.
6. Repeat generation → official-priority pruning → strict structural audits → contextual QA → three real builds → packaging verification → metadata/handoffs → safe fast-forward.

Never force-push. Immediately before integration, refetch beta, require an ahead-only compare with `behind_by=0`, update beta with `force=false`, then refetch both branches and verify exact identical SHA/state.
'''
(ROOT / 'NEXT_CHAT_HANDOFF.md').write_text(next_chat, encoding='utf-8')

print('Maltese handoffs finalized for 60 languages; NEXT LANGUAGE = 61.')
