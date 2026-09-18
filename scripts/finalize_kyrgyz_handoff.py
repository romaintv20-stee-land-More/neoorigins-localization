#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

project = ROOT / "PROJECT_HANDOFF.txt"
text = project.read_text(encoding="utf-8")

replacements = {
    "0.9.0 development currently has 63 locales:": "0.9.0 development currently has 64 locales:",
    "so_so, eo_uy.\n\nExpansion order so far:": "so_so, eo_uy, ky_kg.\n\nExpansion order so far:",
    "- 63: Esperanto / eo_uy\n\nSIXTY-THREE IS NOT THE FINAL TARGET.": "- 63: Esperanto / eo_uy\n- 64: Kyrgyz / ky_kg\n\nSIXTY-FOUR IS NOT THE FINAL TARGET.",
    "- catalog.json says 63 supported locales": "- catalog.json says 64 supported locales",
    "- README.md says 63 languages and includes Esperanto eo_uy alongside the previously completed locales": "- README.md says 64 languages and includes Kyrgyz ky_kg alongside the previously completed locales",
}
for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f"Expected handoff marker not found: {old!r}")
    text = text.replace(old, new, 1)

section = r'''

KYRGYZ / LANGUAGE #64 FINAL STATUS
----------------------------------
Kyrgyz locale: ky_kg / Кыргызча.
Minecraft language metadata: Кыргызстан.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND READY/INTEGRATED THROUGH THE STANDARD FAST-FORWARD PROCESS.

Selection / staging:
- staging branch: release/0.9.0-kyrgyz
- exact beta base used to create staging: b1752b55144914a8982ab42393d197188a4bb92b
- final three-target build source SHA: 4566bf7ad56ec8d72a15865c80e5340028bbffe1
- NeoOrigins has zero official ky_kg strings at all three pinned 2.2.27 refs
- all 10 supported 1.21.1 add-ons also had zero official ky_kg strings at their audited refs

Architecture / packaging:
- 16 common namespaces: neoorigins_ky_common_01 through neoorigins_ky_common_16
- 1.21.1 delta namespace: neoorigins_ky_121
- 26.1.x overlay: ky_kg inside neoorigins_26_1
- 26.2 overlay: ky_kg inside neoorigins_26_2
- 1.21.1 packages 27 ky_kg files = 16 common + 1 target delta + 10 add-ons
- 26.1.x packages 17 ky_kg files = 16 common + correct modern overlay
- 26.2 packages 17 ky_kg files = 16 common + correct modern overlay
- no wrong-version overlays or add-on files leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

Coverage / strict QA:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 supported 1.21.1 add-ons: complete
- missing: 0
- overlap: 0
- placeholder errors: 0
- scripts/validate.py: passed
- final contextual QA: 29 source files, 7,103 Kyrgyz-specific letters, 103,247 Cyrillic characters
- intentional Latin-only values are limited to JSON, NeoOrigins, Origin and Origin Architect
- final English-remnant guard passed
- official Minecraft Kyrgyz terms used in the final cleanup include Night Vision = Түндө көрүү and Rotten Flesh = Чирик эт

Final three-target CI:
- workflow: .github/workflows/build-0.9.0-kyrgyz.yml
- run: 34449980026
- source: 4566bf7ad56ec8d72a15865c80e5340028bbffe1
- mc-1.21.1 job 102783283272: SUCCESS
  - artifact 10141174534
  - JAR SHA256 9af4c8411eb33b9ea45b31d833ae323224651acc33c16565f8129f22dcf0f9e9
  - artifact ZIP SHA256 88b4ce6650d4c0a7323097333d672272b9b5d8fd65885b14d2820cf6d5a6390d
- mc-26.1.x job 102783283332: SUCCESS
  - artifact 10141175254
  - artifact ZIP SHA256 8f055c05a19f4cb7d3fa2bf19d500316ca02b13d0469a246fe5d09b53f951594
- mc-26.2 job 102783283016: SUCCESS
  - artifact 10141176895
  - artifact ZIP SHA256 4c25ce448c3650405f3201de73ba7dfaf886c15bf397372526e4d3f236530209

NEXT LANGUAGE = #65.
Before starting #65, refetch release/0.9.0-beta and use its exact current HEAD as the staging base. Do not use main. Re-audit the current Minecraft Java locale inventory, apply the regional-variant dedup rule, verify official upstream strings before generating fallbacks, preserve placeholders exactly, run contextual QA, build all three targets, inspect JAR contents, and integrate only by non-forced fast-forward after confirming the staging branch is ahead-only.
'''
if "KYRGYZ / LANGUAGE #64 FINAL STATUS" in text:
    raise SystemExit("Kyrgyz final status section already present")
text = text.rstrip() + section + "\n"
project.write_text(text, encoding="utf-8")

next_handoff = ROOT / "NEXT_CHAT_HANDOFF.md"
next_handoff.write_text(r'''# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **64**.
- Last completed language: **#64 Kyrgyz — `ky_kg / Кыргызча`**.
- **Do not redo Kyrgyz.**
- Next language: **#65**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered before #59; do not treat that recovery as pending.

## #64 Kyrgyz verification

Staging branch: `release/0.9.0-kyrgyz`

Original beta base used for staging:
`b1752b55144914a8982ab42393d197188a4bb92b`

Final three-target build source:
`4566bf7ad56ec8d72a15865c80e5340028bbffe1`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- official Kyrgyz strings upstream at audited refs: **0** for NeoOrigins and **0** for all 10 supported add-ons
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- final sanity: **29 files, 7,103 Kyrgyz-specific letters, 103,247 Cyrillic characters**
- intentional Latin-only values: `JSON`, `NeoOrigins`, `Origin`, `Origin Architect`
- final English-remnant guard: success
- final terminology cleanup uses official Minecraft Kyrgyz `Түндө көрүү` for Night Vision and `Чирик эт` for Rotten Flesh

## Final build run and artifacts

Run `34449980026`, source `4566bf7ad56ec8d72a15865c80e5340028bbffe1`: all three jobs succeeded.

- 1.21.1 job `102783283272`, artifact `10141174534`, package **27/27**, JAR SHA256 `9af4c8411eb33b9ea45b31d833ae323224651acc33c16565f8129f22dcf0f9e9`, ZIP SHA256 `88b4ce6650d4c0a7323097333d672272b9b5d8fd65885b14d2820cf6d5a6390d`
- 26.1.x job `102783283332`, artifact `10141175254`, package **17/17**, ZIP SHA256 `8f055c05a19f4cb7d3fa2bf19d500316ca02b13d0469a246fe5d09b53f951594`
- 26.2 job `102783283016`, artifact `10141176895`, package **17/17**, ZIP SHA256 `4c25ce448c3650405f3201de73ba7dfaf886c15bf397372526e4d3f236530209`

Packaging semantics:
- 1.21.1: 16 common + `neoorigins_ky_121` + 10 add-ons = **27** Kyrgyz files
- 26.1.x: 16 common + `neoorigins_26_1` = **17** Kyrgyz files
- 26.2: 16 common + `neoorigins_26_2` = **17** Kyrgyz files
- no wrong-version overlays or add-ons leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

## Start of language #65

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging to be ahead-only / `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
''', encoding="utf-8")

print("Kyrgyz handoffs finalized: 64 locales, #64 complete, next #65")
