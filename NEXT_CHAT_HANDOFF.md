# NEXT CHAT HANDOFF — NeoOrigins Localization

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
